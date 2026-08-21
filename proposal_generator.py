from fpdf import FPDF
from datetime import datetime, timedelta


def nettoyer_texte(texte) -> str:
    """Convertit en texte propre, gère les valeurs vides/None."""
    if texte is None or texte == "":
        return "Non renseigné"
    return str(texte).strip()


class PropositionPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", "fonts/DejaVuSans-Oblique.ttf")

    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "ADBCENTER LOGISPLAN", ln=True, align="C")
        self.set_font("DejaVu", "", 10)
        self.cell(0, 6, "Proposition Commerciale", ln=True, align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, titre):
        self.set_font("DejaVu", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, titre, ln=True, fill=True)
        self.ln(2)


def generer_proposition_pdf(lead: dict, formation: dict, numero_prop: str) -> str:
    pdf = PropositionPDF()
    pdf.add_page()

    date_aujourdhui = datetime.now().strftime("%d/%m/%Y")
    date_validite = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")

    # Référence et dates
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, f"Référence : {numero_prop}", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Date : {date_aujourdhui}   |   Validité : {date_validite}", ln=True)
    pdf.ln(6)

    # Destinataire
    pdf.section_title("Destinataire")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Nom : {nettoyer_texte(lead.get('nom_prenom'))}", ln=True)
    pdf.cell(0, 6, f"Email : {nettoyer_texte(lead.get('email'))}", ln=True)
    pdf.cell(0, 6, f"Téléphone : {nettoyer_texte(lead.get('telephone'))}", ln=True)
    pdf.ln(6)

    # Formation
    pdf.section_title("Programme proposé")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Formation : {nettoyer_texte(formation.get('titre'))}", ln=True)
    pdf.cell(0, 6, f"Durée : {nettoyer_texte(formation.get('duree'))}", ln=True)
    pdf.cell(0, 6, f"Public : {nettoyer_texte(formation.get('public'))}", ln=True)
    pdf.ln(4)

    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 6, "Pitch :", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 6, nettoyer_texte(formation.get("pitch_100_mots")))
    pdf.ln(4)

    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 6, "Bénéfices clés :", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 6, nettoyer_texte(formation.get("benefices")))
    pdf.ln(6)

    # Prix
    pdf.section_title("Investissement")
    pdf.set_font("DejaVu", "", 10)
    prix = nettoyer_texte(formation.get("prix_inter"))
    pdf.cell(0, 6, f"{prix} MAD HT / personne (+ TVA 20%)", ln=True)
    pdf.ln(6)

    # Conditions
    pdf.set_font("DejaVu", "I", 9)
    pdf.multi_cell(
        0, 5,
        f"Cette proposition est valable jusqu'au {date_validite}. "
        "Éligible à une prise en charge partielle OFPPT pour les entreprises marocaines cotisantes."
    )

    nom_fichier = f"proposition_{numero_prop}.pdf"
    pdf.output(nom_fichier)
    return nom_fichier