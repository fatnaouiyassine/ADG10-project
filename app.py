"""Interface Streamlit du systeme commercial ADG-10."""

import os
from pathlib import Path
import subprocess
import sys

import pandas as pd
import streamlit as st

from airtable_client import get_all_records
from config import ConfigurationError, settings
from state_store import DispatchLedger


PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="ADG-10 | Pilotage commercial",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --navy: #102A43;
        --blue: #1F5A94;
        --teal: #13A89E;
        --ink: #243B53;
        --muted: #627D98;
        --surface: #F5F8FB;
        --border: #D9E2EC;
    }
    .stApp { background: #F5F8FB; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C2238 0%, #102A43 100%);
    }
    [data-testid="stSidebar"] * { color: #F8FAFC; }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stCheckbox label { color: #E6EEF6 !important; }
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #102A43 0%, #1F5A94 70%, #13A89E 130%);
        color: white;
        margin-bottom: 1.1rem;
        box-shadow: 0 12px 30px rgba(16, 42, 67, .12);
    }
    .hero-kicker {
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .14em;
        opacity: .8;
        text-transform: uppercase;
    }
    .hero h1 { margin: .35rem 0 .25rem; font-size: 2rem; color: white; }
    .hero p { margin: 0; opacity: .86; font-size: .98rem; }
    .section-label {
        color: #627D98;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
        margin: .7rem 0 .2rem;
    }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #D9E2EC;
        padding: 1rem 1.1rem;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(16, 42, 67, .05);
    }
    [data-testid="stMetricLabel"] { color: #627D98; }
    [data-testid="stMetricValue"] { color: #102A43; }
    .status-card {
        background: white;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        height: 100%;
    }
    .status-title { color: #102A43; font-weight: 700; margin-bottom: .35rem; }
    .status-copy { color: #627D98; font-size: .86rem; line-height: 1.45; }
    .mode-sim {
        background: #E8F4FD;
        color: #1F5A94;
        border: 1px solid #B8D9F2;
        padding: .55rem .75rem;
        border-radius: 10px;
        font-size: .82rem;
        margin-bottom: .8rem;
    }
    .mode-live {
        background: #FFF4E5;
        color: #8A4B08;
        border: 1px solid #FFD59A;
        padding: .55rem .75rem;
        border-radius: 10px;
        font-size: .82rem;
        margin-bottom: .8rem;
    }
    .stButton > button { border-radius: 10px; min-height: 2.65rem; font-weight: 650; }
    div[data-testid="stDataFrame"] {
        background: white;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _lead_status(fields: dict) -> str:
    try:
        score = float(fields.get("score", 0) or 0)
    except (TypeError, ValueError):
        score = 0.0
    if fields.get("numero_facture"):
        return "Facturé"
    if fields.get("client_signe"):
        return "Signé"
    if fields.get("date_envoi_proposition"):
        return "Closing"
    if score >= 8:
        return "Prioritaire"
    if score >= 5:
        return "Qualification"
    return "Nurturing"


@st.cache_data(ttl=15, show_spinner=False)
def load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    leads = get_all_records("Leads")
    formations = get_all_records("Formations")

    lead_rows = []
    for record in leads:
        fields = record.get("fields", {})
        lead_rows.append(
            {
                "Nom": fields.get("nom_prenom", ""),
                "Entreprise": fields.get("entreprise")
                or fields.get("raison_sociale", ""),
                "Email": fields.get("email", ""),
                "Téléphone": fields.get("telephone", ""),
                "Score": fields.get("score", 0),
                "Statut": _lead_status(fields),
                "Urgence": fields.get("urgence", ""),
                "Decideur": fields.get("decideur", ""),
                "Proposition": fields.get("date_envoi_proposition", ""),
                "Facture": fields.get("numero_facture", ""),
            }
        )

    formation_rows = []
    for record in formations:
        fields = record.get("fields", {})
        formation_rows.append(
            {
                "Titre": fields.get("titre", ""),
                "Duree": fields.get("duree", ""),
                "Prix HT": fields.get("prix_inter", ""),
                "Public": fields.get("public", ""),
                "Contenu IA": "Prêt"
                if fields.get("pitch_100_mots") and fields.get("benefices")
                else "À compléter",
            }
        )

    lead_columns = [
        "Nom",
        "Entreprise",
        "Email",
        "Téléphone",
        "Score",
        "Statut",
        "Urgence",
        "Decideur",
        "Proposition",
        "Facture",
    ]
    formation_columns = ["Titre", "Duree", "Prix HT", "Public", "Contenu IA"]
    lead_df = pd.DataFrame(lead_rows, columns=lead_columns)
    formation_df = pd.DataFrame(formation_rows, columns=formation_columns)
    lead_df["Score"] = pd.to_numeric(lead_df["Score"], errors="coerce").fillna(0.0)
    return lead_df, formation_df


def run_script(filename: str, live: bool) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["ADG10_DRY_RUN"] = "false" if live else "true"
    mode_argument = "--live" if live else "--dry-run"
    return subprocess.run(
        [sys.executable, str(PROJECT_ROOT / filename), mode_argument],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
        check=False,
    )


def render_execution(filename: str, live: bool) -> None:
    try:
        with st.spinner(f"Exécution de {filename}..."):
            result = run_script(filename, live)
    except subprocess.TimeoutExpired:
        st.error("L'opération a dépassé 15 minutes et a été interrompue.")
        return
    except Exception as exc:
        st.error(f"Impossible de lancer l'opération : {exc}")
        return

    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    if result.returncode == 0:
        st.success("Opération terminée avec succès.")
        if live:
            load_dashboard_data.clear()
    else:
        st.error(f"Opération terminée avec le code {result.returncode}.")
    st.code(output or "Aucun message retourné.", language="text")


with st.sidebar:
    st.markdown("## ◈ ADG-10")
    st.caption("Pilotage commercial")
    st.divider()
    mode = st.radio(
        "Mode d'exécution",
        ["Simulation", "Production"],
        help="La simulation ne modifie pas Airtable et n'envoie aucun message.",
    )
    live_mode = mode == "Production"
    if live_mode:
        st.markdown(
            '<div class="mode-live">Production active : des emails, messages et mises à jour '
            "Airtable peuvent être exécutés.</div>",
            unsafe_allow_html=True,
        )
        confirmed = st.checkbox("Je confirme les actions réelles")
    else:
        st.markdown(
            '<div class="mode-sim">Simulation active : aucun envoi et aucune écriture CRM.</div>',
            unsafe_allow_html=True,
        )
        confirmed = True

    st.markdown("### Intégrations")
    st.caption(
        ("● Airtable configuré" if settings.airtable_token and settings.airtable_base_id else "○ Airtable incomplet")
    )
    st.caption(
        ("● Groq configuré" if settings.groq_api_key else "○ Groq incomplet")
    )
    st.caption(
        ("● Gmail configuré" if settings.gmail_address and settings.gmail_app_password else "○ Gmail incomplet")
    )
    st.divider()
    if st.button("Actualiser les données", use_container_width=True):
        load_dashboard_data.clear()
        st.rerun()


st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">ADBCENTER LOGISPLAN</div>
        <h1>Pilotage commercial</h1>
        <p>Suivez les opportunités, orchestrez les relances et préparez les documents clients.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    leads_df, formations_df = load_dashboard_data()
except ConfigurationError as exc:
    st.error(str(exc))
    st.info("Complétez le fichier .env à partir de .env.example, puis rechargez l'application.")
    st.stop()
except Exception as exc:
    st.error(f"Connexion Airtable impossible : {exc}")
    st.stop()

total_leads = len(leads_df)
average_score = leads_df["Score"].mean() if total_leads else 0
hot_leads = int((leads_df["Score"] >= 8).sum()) if total_leads else 0
signed_clients = int(leads_df["Statut"].isin(["Signé", "Facturé"]).sum()) if total_leads else 0

metric_columns = st.columns(4)
metric_columns[0].metric("Leads actifs", total_leads)
metric_columns[1].metric("Score moyen", f"{average_score:.1f}/10")
metric_columns[2].metric("Opportunités prioritaires", hot_leads)
metric_columns[3].metric("Clients signés", signed_clients)

st.markdown('<div class="section-label">Operations</div>', unsafe_allow_html=True)
action_columns = st.columns(4)
disabled = live_mode and not confirmed
actions = [
    ("Générer les contenus", "run_e1_content.py", "Met à jour les pitchs et bénéfices."),
    ("Recalculer les scores", "run_e4_scoring.py", "Actualise la qualification des leads."),
    ("Lancer le pipeline", "run_pipeline.py", "Exécute scoring, nurturing et closing."),
    ("Contrats et factures", "run_e8_contract.py", "Prépare les dossiers des clients signés."),
]
selected_action = None
for column, (label, script, description) in zip(action_columns, actions):
    with column:
        st.markdown(
            f'<div class="status-card"><div class="status-title">{label}</div>'
            f'<div class="status-copy">{description}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button(label, key=script, use_container_width=True, disabled=disabled):
            selected_action = script

if disabled:
    st.warning("Confirmez le mode Production dans la barre latérale avant de lancer une action.")
if selected_action:
    render_execution(selected_action, live_mode)

overview_tab, leads_tab, formations_tab, activity_tab = st.tabs(
    ["Vue d'ensemble", "Leads", "Formations", "Activité"]
)

with overview_tab:
    left, right = st.columns([1.15, 0.85])
    with left:
        st.subheader("Répartition du portefeuille")
        if leads_df.empty:
            st.info("Aucun lead disponible.")
        else:
            distribution = (
                leads_df["Statut"]
                .value_counts()
                .rename_axis("Statut")
                .reset_index(name="Leads")
                .set_index("Statut")
            )
            st.bar_chart(distribution, color="#13A89E", height=320)
    with right:
        st.subheader("Priorités")
        priorities = leads_df[
            leads_df["Statut"].isin(["Prioritaire", "Closing", "Signé"])
        ][["Nom", "Entreprise", "Score", "Statut"]].sort_values(
            "Score", ascending=False
        )
        if priorities.empty:
            st.info("Aucune action prioritaire identifiée.")
        else:
            st.dataframe(priorities, hide_index=True, use_container_width=True)

with leads_tab:
    search = st.text_input("Rechercher un lead", placeholder="Nom, entreprise ou email")
    statuses = sorted(leads_df["Statut"].dropna().unique().tolist())
    selected_statuses = st.multiselect("Filtrer par statut", statuses, default=statuses)
    filtered = leads_df[leads_df["Statut"].isin(selected_statuses)]
    if search:
        mask = filtered[["Nom", "Entreprise", "Email"]].astype(str).apply(
            lambda column: column.str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask.any(axis=1)]
    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=10, format="%.1f"
            )
        },
    )

with formations_tab:
    st.dataframe(formations_df, hide_index=True, use_container_width=True)

with activity_tab:
    st.subheader("Derniers envois confirmés")
    try:
        recent_events = DispatchLedger().recent(30)
    except Exception as exc:
        recent_events = []
        st.error(f"Journal d'activité illisible : {exc}")
    if recent_events:
        activity_df = pd.DataFrame(recent_events)
        st.dataframe(activity_df, hide_index=True, use_container_width=True)
    else:
        st.info("Aucun envoi confirmé dans le journal local.")
    generated_count = (
        len(list(settings.output_dir.glob("*.pdf"))) if settings.output_dir.exists() else 0
    )
    st.caption(f"{generated_count} document(s) PDF dans {settings.output_dir}")
