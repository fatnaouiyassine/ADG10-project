"""Configuration centralisee du projet ADG-10.

Le chargement de ce module ne declenche aucun appel externe. Les validations
sont effectuees au moment ou une integration est utilisee, afin que les tests
et le mode simulation puissent fonctionner sans secrets.
"""

from dataclasses import dataclass
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(path: Path) -> None:
        """Charge les paires simples CLE=VALEUR quand python-dotenv est indisponible."""
        if not path.exists():
            return
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            clean_value = value.strip().strip("'").strip('"')
            os.environ.setdefault(key.strip(), clean_value)


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class ConfigurationError(RuntimeError):
    """Erreur de configuration explicite et presentable dans l'interface."""


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "oui", "on"}


def _project_path(name: str, default: str) -> Path:
    raw_path = Path(_env(name, default))
    return raw_path if raw_path.is_absolute() else BASE_DIR / raw_path


@dataclass(frozen=True)
class Settings:
    airtable_token: str
    airtable_base_id: str
    groq_api_key: str
    gmail_address: str
    gmail_app_password: str
    dry_run: bool
    output_dir: Path
    state_dir: Path
    company_name: str
    company_legal_name: str
    company_address: str
    company_phone: str
    company_email: str
    company_website: str
    company_rc: str
    company_ice: str
    company_if: str
    company_tp: str
    company_cnss: str
    company_bank: str
    company_rib: str
    signatory_name: str
    signatory_title: str
    payment_terms: str
    cancellation_terms: str

    @property
    def sender_email(self) -> str:
        return self.company_email or self.gmail_address


settings = Settings(
    airtable_token=_env("AIRTABLE_TOKEN"),
    airtable_base_id=_env("AIRTABLE_BASE_ID"),
    groq_api_key=_env("GROQ_API_KEY"),
    gmail_address=_env("GMAIL_ADDRESS"),
    gmail_app_password=_env("GMAIL_APP_PASSWORD"),
    dry_run=_env_bool("ADG10_DRY_RUN", default=True),
    output_dir=_project_path("ADG10_OUTPUT_DIR", "output/pdf"),
    state_dir=_project_path("ADG10_STATE_DIR", ".runtime"),
    company_name=_env("ADG10_COMPANY_NAME", "ADBCENTER LOGISPLAN"),
    company_legal_name=_env("ADG10_COMPANY_LEGAL_NAME", "ADBCENTER LOGISPLAN"),
    company_address=_env(
        "ADG10_COMPANY_ADDRESS",
        "Bureau 53, Galeries Mamounia, Cite Dakhla, Agadir",
    ),
    company_phone=_env("ADG10_COMPANY_PHONE"),
    company_email=_env("ADG10_COMPANY_EMAIL"),
    company_website=_env("ADG10_COMPANY_WEBSITE"),
    company_rc=_env("ADG10_COMPANY_RC", "67223"),
    company_ice=_env("ADG10_COMPANY_ICE"),
    company_if=_env("ADG10_COMPANY_IF"),
    company_tp=_env("ADG10_COMPANY_TP"),
    company_cnss=_env("ADG10_COMPANY_CNSS"),
    company_bank=_env("ADG10_COMPANY_BANK"),
    company_rib=_env("ADG10_COMPANY_RIB"),
    signatory_name=_env("ADG10_SIGNATORY_NAME", "Azouguigh El Houssaine"),
    signatory_title=_env("ADG10_SIGNATORY_TITLE", "Représentant habilité"),
    payment_terms=_env(
        "ADG10_PAYMENT_TERMS",
        "Paiement sous 30 jours à compter de la date de facture.",
    ),
    cancellation_terms=_env(
        "ADG10_CANCELLATION_TERMS",
        "Toute demande de report ou d'annulation doit être adressée par écrit. "
        "Les conditions applicables sont confirmées avant la session.",
    ),
)


def require_configuration(*attribute_names: str) -> None:
    """Verifie que les parametres demandes sont renseignes."""
    missing = [name for name in attribute_names if not getattr(settings, name, "")]
    if missing:
        variables = ", ".join(name.upper() for name in missing)
        raise ConfigurationError(f"Configuration manquante : {variables}")


# Compatibilite avec les imports historiques du prototype.
AIRTABLE_TOKEN = settings.airtable_token
AIRTABLE_BASE_ID = settings.airtable_base_id
