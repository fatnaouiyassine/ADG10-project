from fpdf import FPDF
from datetime import datetime


def nettoyer_texte(texte) -> str:
    if texte is None or texte == "":
        return "Non renseigné"
    return str(texte).strip()


class DocumentPDF(FPDF):
    def __init__(self, titre_document):
        super().__init__()
        self.titre_document = titre_document
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", "fonts/DejaVuSans-Oblique.ttf")

    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "ADBCENTER LOGISPLAN", ln=True, align="C")
        self.set_font("DejaVu", "", 10)
        self.cell(0, 6, self.titre_document, ln=True, align="C")
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


def calculer_prix_ht(prix_str: str) -> float:
    """Extrait un prix numerique approximatif depuis un texte type '2500-3500' ou '2500'."""
    try:
        chiffres = "".join(c for c in prix_str if c.isdigit() or c == "-")
        premiere_valeur = chiffres.split("-")[0]
        return float(premiere_valeur) if premiere_valeur else 0.0
    except Exception:
        return 0.0


def generer_contrat_pdf(lead: dict, formation: dict, numero_contrat: str) -> str:
    pdf = DocumentPDF("Convention de formation")
    pdf.add_page()

    date_jour = datetime.now().strftime("%d/%m/%Y")

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, f"Convention N° : {numero_contrat}", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Date : {date_jour}", ln=True)
    pdf.ln(6)

    pdf.section_title("Entre les soussignes")
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 6, "ADBCENTER LOGISPLAN, RC 67223, Bureau 53, Galeries Mamounia, Cite Dakhla, Agadir, ci-apres denomme \"le Prestataire\",")
    pdf.ln(2)
    pdf.multi_cell(0, 6, f"Et {nettoyer_texte(lead.get('nom_prenom'))}, ci-apres denomme \"le Client\",")
    pdf.ln(6)

    pdf.section_title("Objet de la convention")
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 6,
        f"La presente convention a pour objet la formation \"{nettoyer_texte(formation.get('titre'))}\", "
        f"d'une duree de {nettoyer_texte(formation.get('duree'))}, dispensee par le Prestataire au profit du Client."
    )
    pdf.ln(6)

    pdf.section_title("Conditions financieres")
    prix_ht = calculer_prix_ht(formation.get("prix_inter", "0"))
    tva = prix_ht * 0.20
    ttc = prix_ht + tva
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Montant HT : {prix_ht:.2f} MAD", ln=True)
    pdf.cell(0, 6, f"TVA (20%) : {tva:.2f} MAD", ln=True)
    pdf.cell(0, 6, f"Montant TTC : {ttc:.2f} MAD", ln=True)
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 10)
    pdf.cell(95, 6, "Le Prestataire", align="C")
    pdf.cell(95, 6, "Le Client", align="C", ln=True)
    pdf.ln(15)
    pdf.cell(95, 6, "Azouguigh El Houssaine", align="C")
    pdf.cell(95, 6, nettoyer_texte(lead.get("nom_prenom")), align="C", ln=True)

    nom_fichier = f"contrat_{numero_contrat}.pdf"
    pdf.output(nom_fichier)
    return nom_fichier


def generer_facture_pdf(lead: dict, formation: dict, numero_facture: str) -> str:
    pdf = DocumentPDF("Facture")
    pdf.add_page()

    date_jour = datetime.now().strftime("%d/%m/%Y")
    prix_ht = calculer_prix_ht(formation.get("prix_inter", "0"))
    tva = prix_ht * 0.20
    ttc = prix_ht + tva

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, f"Facture N° : {numero_facture}", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Date : {date_jour}", ln=True)
    pdf.ln(6)

    pdf.section_title("Client")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, nettoyer_texte(lead.get("nom_prenom")), ln=True)
    pdf.cell(0, 6, nettoyer_texte(lead.get("email")), ln=True)
    pdf.ln(6)

    pdf.section_title("Detail")
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Formation : {nettoyer_texte(formation.get('titre'))}", ln=True)
    pdf.cell(0, 6, f"Montant HT : {prix_ht:.2f} MAD", ln=True)
    pdf.cell(0, 6, f"TVA (20%) : {tva:.2f} MAD", ln=True)
    pdf.set_font("DejaVu", "B", 10)
    pdf.cell(0, 6, f"Total TTC : {ttc:.2f} MAD", ln=True)

    nom_fichier = f"facture_{numero_facture}.pdf"
    pdf.output(nom_fichier)
    return nom_fichier