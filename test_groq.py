"""Diagnostic Groq manuel. Un appel reel n'est effectue que par lancement direct."""


def main():
    from generation_contenu import generer_contenu_formation

    result = generer_contenu_formation(
        titre="MBTI et connaissance de soi",
        duree="2-3 jours",
        prix_inter="2500-3500",
        public="Managers et cadres",
    )
    print(result)


if __name__ == "__main__":
    main()
