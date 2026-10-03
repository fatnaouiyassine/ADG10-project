"""Diagnostic Airtable manuel. N'est jamais execute lors d'une collecte de tests."""


def main():
    from airtable_client import get_all_records

    formations = get_all_records("Formations")
    print(f"{len(formations)} formation(s) trouvee(s).")
    for formation in formations:
        print(formation["fields"].get("titre", "Sans titre"))


if __name__ == "__main__":
    main()
