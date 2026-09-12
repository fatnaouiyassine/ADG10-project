# ADG-10 — Systeme d'automatisation commerciale

Systeme fonctionnel d'automatisation du cycle commercial, inspire du cahier des charges
ADG-10 (ADBCENTER LOGISPLAN), developpe entierement avec des outils gratuits.

## Fonctionnalites

| Etape | Description | Statut |
|-------|-------------|--------|
| E1 | Generation de contenu marketing (pitch, benefices, FAQ) via IA | ✅ Reel (Groq) |
| E2 | Contenu multicanal (LinkedIn, WhatsApp) | ✅ Reel (Groq) |
| E3 | Diffusion sur les reseaux sociaux | ❌ Non implemente (necessite un outil payant type Buffer) |
| E4 | Scoring et qualification automatique des leads | ✅ Reel |
| E5 | Sequences de nurturing (email + WhatsApp) | ✅ Reel |
| E6 | Generation de proposition commerciale PDF + envoi email | ✅ Reel |
| E7 | Relance et closing (email + WhatsApp) | ✅ Reel (l'appel telephonique reste humain) |
| E8 | Generation de contrat + facture PDF + envoi email | ✅ Reel |

## Stack technique (100% gratuit)

- **Python 3.14**
- **Airtable** (plan gratuit) — CRM (tables Formations, Leads)
- **Groq API** (plan gratuit) — generation de contenu via Llama / gpt-oss-120b
- **Gmail SMTP** (gratuit) — envoi d'emails reels avec pieces jointes
- **pywhatkit** (WhatsApp Web) — envoi de messages WhatsApp reels
- **fpdf2** + police DejaVu Sans — generation de documents PDF (proposition, contrat, facture)
- **Git** — gestion de version

## Structure du projet