# Introduction Générale

La commercialisation d’une formation commence bien avant l’envoi d’un devis. Elle suppose de présenter une offre compréhensible, d’identifier le besoin du prospect, d’évaluer sa maturité et de maintenir le contact jusqu’à une décision. Le même dossier mobilise ainsi des informations pédagogiques, commerciales et administratives. Lorsque ces informations sont dispersées entre des messages, des tableaux et des fichiers, les délais de réponse deviennent variables et les relances difficiles à suivre.

Le projet ADG-10 s’inscrit dans ce contexte. Réalisé au sein d’ADBCENTER LOGISPLAN pour l’activité de formation d’Adaoui Business Centre, il vise à structurer un agent commercial automatisé autour de huit étapes, de E1 à E8. Le parcours va de la préparation de la fiche formation à l’émission des documents de contractualisation. L’objectif de cent clients signés par an constitue la cible commerciale du cadrage initial ; il ne représente pas un résultat atteint ou mesuré par le prototype.

Nous avons retenu Python pour les règles et l’orchestration, Airtable pour les données opérationnelles et des modules distincts pour la génération de contenus, le scoring, les relances, les PDF et la messagerie. La version actuelle ajoute une interface Streamlit qui rend ces fonctions accessibles depuis un navigateur. Groq assure la génération de textes en mode réel, ReportLab produit les documents commerciaux et un journal local conserve les actions envoyées afin de limiter les répétitions.

Ce rapport décrit l’état du projet au 17 septembre 2026. Il actualise les constats de la première version : la génération de contenu n’est plus uniquement simulée, une interface web existe, la contractualisation et la facturation sont codées, et des tests unitaires sont disponibles. En revanche, la publication sociale E3 reste absente, les séquences nécessitent une exécution régulière des scripts et les services externes n’ont pas fait l’objet d’une recette complète dans le cadre de cette mise à jour documentaire.

La distinction entre fonction implémentée, démonstration locale et validation en conditions réelles guide l’analyse. Elle permet de présenter les progrès sans assimiler la présence d’un module à une garantie de production. Les exemples de captures et de documents utilisent des données de démonstration. Les résultats de tests correspondent à des contrôles locaux effectivement exécutés ; aucun indicateur de vente réel n’est inventé.

Le premier chapitre présente l’organisme d’accueil, le contexte et la conduite du projet. Le deuxième formalise les besoins et la conception à travers les cas d’utilisation, les séquences et le modèle de données. Le troisième expose l’environnement et l’architecture technique. Le quatrième détaille la réalisation de chaque étape, les tests, l’interface et les perspectives d’évolution. Les annexes complètent le rapport par un dictionnaire de données, un guide d’exécution et une liste de scénarios de recette.

# Chapitre 1 : Présentation de l’organisme d’accueil

## Introduction

Ce chapitre situe ADG-10 dans son environnement organisationnel et commercial. Il présente les activités concernées, les utilisateurs et le processus de vente, puis explique les objectifs et les contraintes qui ont orienté les choix de conception. La dernière partie décrit une conduite de projet progressive et les livrables associés à chaque phase.

## 1.1 Présentation de l’organisme d’accueil

### 1.1.1 ADBCENTER LOGISPLAN

ADBCENTER LOGISPLAN constitue le cadre organisationnel du stage. Le besoin étudié concerne l’activité de formation et d’accompagnement portée par Adaoui Business Centre. La présentation métier fournie avec le projet décrit des formations destinées aux particuliers, aux salariés, aux cadres et aux entreprises, avec des formats interentreprises ou adaptés à une organisation.

L’activité commerciale doit rapprocher le contenu pédagogique du besoin exprimé par le client. Le titre seul ne suffit pas : la durée, le public, les prérequis, les objectifs et les modalités d’intervention déterminent la pertinence d’une offre. Ces éléments alimentent ensuite les messages de présentation, les réponses aux questions et la proposition commerciale. ADG-10 fournit un cadre pour réutiliser ces informations de façon cohérente.

L’application ne remplace pas l’organisation du centre. Les responsables conservent la validation du catalogue, des prix, des engagements et des documents transmis. Le rôle de l’automatisation consiste à préparer les actions répétitives et à rendre les priorités plus visibles, afin de réserver l’intervention humaine aux échanges nécessitant compréhension, arbitrage ou négociation.

### 1.1.2 Adaoui Business Centre

Adaoui Business Centre représente l’activité bénéficiaire décrite dans le cadrage. Le catalogue présenté dans l’ancien rapport couvre notamment les outils numériques et l’intelligence artificielle, l’entrepreneuriat, le BIM, la communication agile, le management et le leadership, ainsi que des formations sur mesure. Cette description donne le contexte du projet ; elle ne constitue pas un inventaire actualisé du catalogue Airtable.

Les segments mentionnés comprennent des particuliers, des professionnels, des entreprises locales et nationales, ainsi que des Marocains résidant à l’étranger. Les informations utiles à une vente diffèrent selon le segment. Une entreprise demande, par exemple, un périmètre pédagogique et un calendrier pour plusieurs participants, tandis qu’un particulier peut surtout rechercher la date, le programme et les modalités d’inscription. Le système doit donc permettre une personnalisation fondée sur des données vérifiées.

### 1.1.3 Organisation et responsabilités

Le projet implique des rôles complémentaires. Le tableau suivant présente une répartition fonctionnelle adaptée au prototype. Il décrit les responsabilités attendues, sans affirmer l’existence d’un service ou d’un poste supplémentaire au sein de l’organisme.

@table Tableau 1.1 : Répartition des responsabilités
| Rôle | Responsabilité | Livrable ou décision |
| Direction / commanditaire | Définir les objectifs, les offres et les règles commerciales. | Catalogue et priorités validés. |
| Encadrant | Orienter les choix et examiner les résultats. | Retour métier sur les démonstrations. |
| Commercial | Qualifier le besoin, appeler et négocier. | Décision du prospect et prochaine action. |
| Formateur | Préciser programme, objectifs et modalités. | Données pédagogiques fiables. |
| Stagiaire développeur | Analyser, concevoir, réaliser et vérifier. | Modules, interface, tests et documentation. |
| Responsable administratif | Vérifier les informations de contractualisation. | Convention et facture approuvées. |

### 1.1.4 Catalogue et segments

Le catalogue est représenté par la table Formations d’Airtable. Les champs principaux décrivent le titre, la durée, le public et le prix interentreprises. Les champs de contenu contiennent le pitch court, le pitch long, les bénéfices et la FAQ. Des informations optionnelles précisent le lieu, la date de session, la modalité, les objectifs et les méthodes pédagogiques. Le nombre d’entrées reste dépendant de la base utilisée ; le rapport ne fige donc pas le volume historique de sept formations comme une donnée actuelle.

La segmentation sert à orienter l’argumentation et le traitement commercial. Dans le code actuel, le score utilise notamment la taille de l’entreprise, le rôle du contact et son canal d’entrée. Le système ne dispose pas encore d’un module complet d’analyse par segment, campagne ou marché. Une exploitation future devra normaliser ces catégories pour pouvoir comparer les résultats sans multiplier des libellés équivalents.

### 1.1.5 Processus commercial existant

Le processus décrit dans les documents de cadrage repose sur la préparation de contenus, la diffusion, la réception de demandes, la qualification, l’offre et la relance. L’enchaînement nécessite plusieurs reprises de données. Une modification de prix peut, par exemple, devoir être répercutée dans un message et dans une proposition déjà préparée. Une relance oubliée ou un envoi répété peut dégrader l’expérience du prospect.

Le besoin d’automatisation porte donc sur la continuité du dossier. Il faut pouvoir retrouver la formation demandée, le score calculé, la date de premier contact, la date de proposition et les documents émis. La version actuelle centralise une partie de ces éléments dans Airtable et complète le suivi par un journal local d’envoi. Le retour du prospect, les objections et la validation finale continuent de nécessiter un traitement humain et une mise à jour des données.

## 1.2 Présentation du contexte du projet

### 1.2.1 Vue d’ensemble du projet

Le pipeline ADG-10 décompose le parcours commercial en huit étapes. E1 enrichit la fiche de formation ; E2 adapte le contenu au canal ; E3 correspond à la publication ; E4 qualifie les prospects ; E5 entretient le contact ; E6 produit la proposition ; E7 organise son suivi ; E8 prépare les documents après décision commerciale. Cette décomposition relie chaque automatisation à un objectif identifiable.

@diagram pipeline|Figure 1.1 : Pipeline ADG-10 et périmètre actuel des huit étapes

Dans la réalisation actuelle, le pipeline principal orchestre E4 à E7. E1 et E8 disposent de commandes séparées. E2 construit des textes LinkedIn et WhatsApp puis les affiche. Aucune intégration E3 ne publie ces contenus. La présence d’un adaptateur WhatsApp pour les relances ne doit pas être confondue avec une plateforme de publication sociale.

### 1.2.2 Étude de l’existant

L’ancien rapport décrivait un prototype principalement fondé sur des scripts, un générateur de textes simulés et une proposition PDF simple. Plusieurs de ses limites ont depuis été traitées. La comparaison ci-dessous donne une lecture précise de cette évolution et évite de conserver des conclusions qui ne correspondent plus au dépôt.

@table Tableau 1.2 : Évolution entre l’ancien rapport et la version actuelle
| Domaine | Ancien état décrit | État actuel vérifié dans le code |
| Génération de contenu | Fonctions simulées. | Appel Groq, réponse JSON et contrôle des champs. |
| Interface | Airtable et terminal uniquement. | Tableau de bord Streamlit avec filtres et actions. |
| Documents | Proposition simple avec FPDF2. | ReportLab, thème commun, proposition, convention et facture. |
| Contractualisation | E8 absente. | Génération documentaire et envoi pour les leads signés. |
| Suivi des envois | Pas de persistance dédiée. | Journal JSON local et réconciliation de certaines écritures CRM. |
| Qualité | Pas de tests automatisés. | Onze tests unitaires métier réussis. |
| Documentation | README et exclusions insuffisants. | Guide d’installation, schéma Airtable et fichiers exclus. |
| Publication et cadence | Intégrations à développer. | E3 et planificateur persistant toujours absents. |

### 1.2.3 Problématique

La problématique peut être formulée ainsi : comment automatiser le traitement d’un dossier commercial de formation tout en conservant la cohérence des données, la maîtrise des envois et une intervention humaine aux étapes décisives ? Cette question associe la productivité et la fiabilité. Un système qui prépare rapidement une proposition erronée, ou qui envoie plusieurs fois le même message, ne répond pas au besoin.

L’enjeu technique consiste à coordonner des composants qui ne partagent pas une transaction unique : Airtable, le système de fichiers, SMTP et WhatsApp. Si l’envoi réussit mais que l’écriture CRM échoue, une exécution ultérieure doit reconnaître l’action déjà réalisée. La version actuelle réduit ce risque par un journal local, mais ne garantit pas encore l’unicité d’une action exécutée simultanément par plusieurs processus.

### 1.2.4 Solution proposée

La solution repose sur des modules spécialisés et des règles explicites. Airtable fournit les données. Les fonctions métier calculent le score, choisissent le scénario et construisent les messages. Les générateurs produisent les PDF. Les adaptateurs transmettent les messages uniquement lorsque le mode réel est demandé. Le dashboard rend visibles le portefeuille, les priorités et les commandes d’exécution.

La simulation est activée par défaut pour permettre d’examiner le comportement prévu. Elle n’est pas entièrement hors ligne : les scripts peuvent lire Airtable et préparer des documents locaux. Elle empêche en revanche les envois et les écritures CRM des traitements concernés. Cette définition précise aide l’utilisateur à comprendre les effets d’un lancement depuis l’interface.

### 1.2.5 Enjeux du projet

Le premier enjeu est l’homogénéité du suivi : deux prospects présentant les mêmes critères doivent obtenir le même score et le même routage. Le deuxième est la cohérence documentaire : la proposition et la convention doivent concerner la formation effectivement demandée. Le troisième est la traçabilité : l’opérateur doit distinguer une action préparée, une action envoyée et une action encore à traiter.

La mesure des gains constitue un enjeu complémentaire. Le nombre de modules réalisés ne permet pas de déduire un taux de conversion ni un gain de temps. Ces résultats devront être observés sur une période de pilote, à partir d’événements horodatés et de définitions stables des indicateurs. Le dashboard actuel fournit des volumes et des scores, mais pas une mesure complète de la performance commerciale.

### 1.2.6 Contraintes

@table Tableau 1.3 : Contraintes et conséquences sur la conception
| Contrainte | Conséquence pour ADG-10 |
| Budget et accès aux services | Choisir des intégrations accessibles et vérifier leurs quotas ; aucun coût nul n’est garanti. |
| Qualité du catalogue | Contrôler la formation liée, le tarif et les informations pédagogiques avant émission. |
| Connexion réseau | Prévoir les échecs de lecture, de génération et d’envoi. |
| Données personnelles | Limiter l’exposition des contacts et définir l’accès, la conservation et les oppositions. |
| Responsabilité commerciale | Conserver la validation des offres, les appels et la négociation. |
| Environnement local | Prendre en compte le poste, les fichiers d’état et la session WhatsApp Web. |
| Maintenance | Documenter les paramètres et disposer de tests reproductibles. |

## 1.3 Conduite du projet

### 1.3.1 Démarche itérative inspirée de SCRUM

La démarche présentée dans le cadrage repose sur des incréments démontrables : accès aux données, scoring, proposition, messagerie, relances et contractualisation. Elle reprend des principes de SCRUM, comme le découpage du besoin, la revue d’un résultat et l’ajustement des priorités. L’organisation d’un stage avec un développeur ne permet pas d’assimiler automatiquement cette démarche à une équipe SCRUM complète.

Chaque incrément doit avoir une entrée, une sortie et un critère d’acceptation. Pour le scoring, l’entrée est un ensemble de critères commerciaux et la sortie est un score reproductible. Pour l’envoi documentaire, le critère dépasse la création du PDF : les pièces jointes doivent exister, le destinataire être renseigné et le CRM ne doit être marqué qu’après le succès de l’étape d’envoi.

### 1.3.2 Répartition des rôles

L’encadrant apporte la compréhension du besoin et examine les livrables ; le stagiaire assure l’analyse, la conception, la réalisation et les vérifications. Les futurs utilisateurs commerciaux sont les destinataires des fonctions de pilotage. La validation du prix, des modalités pédagogiques et des informations administratives doit rester rattachée aux responsables métier concernés.

Dans une phase de déploiement, cette répartition devra être complétée par une responsabilité d’exploitation : surveillance des exécutions, gestion des incidents, sauvegarde de l’état et renouvellement des accès. Le prototype contient des outils utiles à ces tâches, mais leur présence ne définit pas à elle seule une organisation de support.

### 1.3.3 Réunions et validations

Les validations utiles portent sur le catalogue, le vocabulaire des critères de score, les délais, les messages, les documents et le comportement attendu en cas d’erreur. Une démonstration doit montrer le dossier de départ, le mode choisi, l’action effectuée et la trace finale. Le rapport ne reconstruit pas un calendrier de réunions ni des comptes rendus qui ne sont pas disponibles.

Pour les évolutions futures, une revue courte à la fin de chaque incrément permettra de décider de son acceptation. Une anomalie de données doit être distinguée d’un défaut du code ou d’un refus du service externe. Cette distinction aide à prioriser le travail et à attribuer chaque correction au bon responsable.

### 1.3.4 Phases de travail

Le travail peut être organisé en six phases liées : cadrage du parcours commercial, structuration des données, réalisation des fonctions métier, intégration documentaire et messagerie, création de l’interface, puis validation et documentation. La version actuelle matérialise ces phases par des modules séparés, des scripts d’exécution, un thème PDF commun et une suite de tests.

L’ordre de réalisation suit les dépendances. La sélection de formation précède la proposition ; la confirmation d’envoi précède la mise à jour de suivi ; une convention et une facture exigent des informations administratives plus complètes qu’un simple premier contact. Les étapes de qualité ne doivent donc pas être ajoutées uniquement après la démonstration.

### 1.3.5 Planning

@diagram planning|Figure 1.2 : Planning indicatif des phases de réalisation et de validation

Ce planning sur huit semaines représente une organisation possible du travail, conforme au format du rapport de stage. Il ne constitue pas un relevé de temps ni une preuve de dates réellement exécutées. Les contrôles de qualité et la documentation accompagnent les développements. La recette réelle des services constitue un jalon distinct de la validation des fonctions locales.

## Conclusion

Le contexte d’ADG-10 conduit à privilégier une automatisation progressive, fondée sur un catalogue structuré et des règles compréhensibles. Les améliorations réalisées répondent à des besoins concrets de pilotage et de fiabilité. Le chapitre suivant traduit ces besoins en exigences vérifiables et en modèles décrivant les interactions entre les composants.

# Chapitre 2 : Analyse et conception

## Introduction

L’analyse fonctionnelle relie le besoin commercial aux comportements attendus. Elle précise ce que le système doit produire, les conditions de déclenchement et les limites d’automatisation. La conception est présentée à travers les besoins, les acteurs, les cas d’utilisation, les séquences et les données. Les modèles décrivent l’implémentation actuelle ou une évolution explicitement identifiée.

## 2.1 Spécifications des besoins

### 2.1.1 Besoins fonctionnels

@table Tableau 2.1 : Besoins fonctionnels et critères d’acceptation
| ID | Besoin | Critère vérifiable |
| BF01 | Centraliser les formations | Une fiche identifiable fournit titre, durée, public, prix et contenus. |
| BF02 | Générer et décliner les textes | Quatre champs de contenu sont récupérables ; les sorties sont adaptées aux canaux supportés. |
| BF03 | Publier les campagnes | Une publication possède canal, date et statut ; fonction encore à développer. |
| BF04 | Qualifier les leads | Le score et le routage sont reproductibles à partir des cinq critères. |
| BF05 | Préparer les séquences | Le message du jour correspond au scénario et à sa date d’ancrage. |
| BF06 | Produire et envoyer l’offre | Le PDF correspond au lead et à la formation ; la date CRM suit l’envoi réussi. |
| BF07 | Suivre la proposition | Les jalons J5, J8 et J12 sont distingués, y compris l’appel humain. |
| BF08 | Préparer le dossier client | Convention et facture sont reliées au dossier, sans marquage après un envoi échoué. |
| BF09 | Piloter l’activité | Volumes, scores, statuts et actions sont accessibles depuis l’interface. |
| BF10 | Maîtriser l’exécution | Le mode simulation est explicite et l’historique est consultable. |

E4 couvre le calcul et le routage des fiches déjà présentes dans Airtable. La capture automatique depuis des formulaires ou des réseaux sociaux n’est pas intégrée dans le code actuel. De même, E8 couvre la production et l’envoi documentaire ; un onboarding complet, une signature électronique ou un suivi du paiement ne sont pas livrés par cette seule étape.

Le score repose sur cinq sous-notes. Le budget pèse 30 %, l’urgence 25 %, le pouvoir de décision 20 %, la taille 15 % et le canal 10 %. Chaque sous-note vaut 0, 5 ou 10 selon les valeurs reconnues. La somme est arrondie à une décimale. Ces seuils sont des règles du prototype et doivent être validés au regard de la stratégie commerciale.

@table Tableau 2.2 : Pondération et règles effectives de scoring
| Critère | Poids | Règles codées |
| Budget | 30 % | Montant au moins égal à 5 000 : 10 ; montant positif inférieur : 5 ; sinon : 0. |
| Urgence | 25 % | Moins d’un mois : 10 ; libellé 3-6 mois : 5 ; autre : 0. |
| Décideur | 20 % | PDG, DRH ou PDG/DRH : 10 ; prescripteur : 5 ; autre : 0. |
| Taille | 15 % | PME 10-250 ou PME 10-250+ : 10 ; TPE 1-9 : 5 ; autre : 0. |
| Canal | 10 % | Recommandation : 10 ; email direct : 5 ; autre : 0. |

La normalisation supprime les différences d’accents, de casse et d’espaces. Elle permet, par exemple, de reconnaître une valeur saisie avec une majuscule sans modifier sa signification. Elle ne traduit pas tous les synonymes possibles : une valeur inconnue reçoit zéro. La qualité des listes de choix Airtable reste donc déterminante.

Le routage utilise les seuils réels 5 et 8 : score au moins égal à 8, priorité ; score de 5 inclus à 8 exclu, qualification courte ; score inférieur à 5, nurturing. Cette formulation couvre correctement les scores décimaux, contrairement à une présentation limitée aux plages entières 5-7 ou 0-4. La consigne d’appel sous quatre heures et de proposition sous vingt-quatre heures est un objectif de traitement affiché, sans garantie automatique de délai.

### 2.1.2 Besoins non fonctionnels

@table Tableau 2.3 : Exigences non fonctionnelles et état de réponse
| Exigence | Réponse actuelle | Complément nécessaire |
| Fiabilité | Gestion d’erreur par lead et journal local. | Reprises robustes et maîtrise de la concurrence. |
| Sécurité | Simulation, configuration séparée et exclusions Git. | Rotation des secrets historiques et protection du déploiement. |
| Maintenabilité | Modules métier et tests unitaires. | Versions verrouillées et organisation en paquet si le projet grandit. |
| Observabilité | Sorties d’exécution, codes retour et historique des envois. | Journal centralisé et alertes d’exploitation. |
| Ergonomie | Dashboard, recherche et filtres. | Validation avec les utilisateurs et gestion des dossiers incomplets. |
| Confidentialité | Paramètres sensibles non reproduits dans les rapports. | Droits d’accès, durées de conservation et procédure d’opposition. |
| Performance | Score local et cache de lecture de quinze secondes. | Mesures de charge et de latence en situation réelle. |

Une exigence n’est pas satisfaite uniquement parce qu’un mécanisme existe. Le journal évite certains doublons, mais sa portée reste locale. Le cache réduit les lectures répétées, mais ne prouve pas une capacité à traiter un volume donné. La suite de tests valide des règles ciblées, sans couvrir la délivrabilité des messages. Les critères de recette du chapitre 4 rendent ces limites mesurables.

### 2.1.3 Acteurs du système

Le commercial consulte les prospects, examine leur priorité et lance les traitements autorisés. Le responsable du catalogue complète les fiches et relit les contenus. Le responsable administratif vérifie les informations avant l’émission documentaire. Dans la version actuelle, ces rôles ne correspondent pas à des comptes applicatifs avec permissions distinctes ; ils décrivent des responsabilités métier.

Les acteurs techniques sont Airtable, Groq, le serveur SMTP et WhatsApp Web. Ils fournissent des services au programme et peuvent échouer indépendamment les uns des autres. Le prospect intervient comme destinataire et comme source d’informations. Ses réponses ne sont pas automatiquement interprétées ni converties en changements de scénario par un module de lecture de boîte mail.

### 2.1.4 Langage de modélisation

Les diagrammes utilisent une notation UML simplifiée pour représenter les rôles, les messages et les relations. Le cas d’utilisation montre le périmètre accessible à un acteur ; le diagramme de séquence décrit l’ordre d’un scénario ; le modèle de classes présente les concepts métier. Les schémas sont conçus pour être confrontés aux modules du dépôt.

Le prototype manipule principalement des dictionnaires Airtable. Le diagramme de classes constitue donc un modèle conceptuel ; il ne signifie pas que des classes Python Lead ou Facture ont déjà été créées. De même, un état cible ou une future intégration est explicitement indiqué pour éviter de le présenter comme un composant opérationnel.

## 2.2 Diagramme de cas d’utilisation

@diagram usecases|Figure 2.1 : Cas d’utilisation du système et interventions humaines

### 2.2.1 Consultation et qualification

Le scénario commence lorsqu’un utilisateur consulte les leads présents dans Airtable. Le dashboard affiche leur score enregistré, leur statut dérivé et leurs coordonnées. L’utilisateur peut rechercher un nom, une entreprise ou un email, puis limiter la vue par statut. Le recalcul du score est une action distincte : une simple consultation n’écrit pas un nouveau score dans le CRM.

La précondition est l’accès à la base et à la table Leads. La sortie attendue est une vue exploitable du portefeuille. Si Airtable ne répond pas ou si la configuration est incomplète, l’interface affiche une erreur et interrompt le chargement. Elle ne présente pas des données vides comme la preuve que le portefeuille ne contient aucun prospect.

### 2.2.2 Exécution des automatisations

L’opérateur choisit le mode et la commande. En simulation, il examine les actions prévues ; en production, une confirmation dans la barre latérale déverrouille les boutons. Le dashboard exécute le script sélectionné et restitue sa sortie ainsi que les erreurs. Les commandes portent sur E1, E4, le pipeline E4-E7 et E8.

Le scénario nominal aboutit à un bilan d’actions, d’éléments ignorés et d’erreurs. Un échec de subprocess ou un dépassement de quinze minutes est présenté à l’utilisateur. Le lancement d’une commande longue occupe l’exécution concernée ; aucune file de travaux persistante ne permet actuellement de reprendre automatiquement ce traitement après l’arrêt du poste.

### 2.2.3 Documents et suivi administratif

Le scénario documentaire associe un lead à une formation, produit le PDF puis prépare l’email. E8 ajoute une condition de signature commerciale et l’absence d’un numéro de facture existant. L’opérateur doit vérifier que le sens de client_signe est partagé par l’équipe, car le message E8 demande encore le retour d’une convention signée. Ce champ ne prouve donc pas à lui seul qu’une signature juridique a été recueillie.

Le cas d’utilisation ne comprend pas le paiement, une signature électronique intégrée ou l’ouverture automatique d’un espace apprenant. Ces fonctions appartiennent aux perspectives. Leur séparation permet de décrire précisément ce que la version actuelle apporte à l’administration des dossiers.

## 2.3 Diagramme de séquence

@diagram sequence|Figure 2.2 : Séquence actuelle de proposition et réconciliation CRM

Le pipeline lit les leads et le catalogue, puis traite chaque lead dans un bloc de gestion d’erreur. Il sélectionne la formation et calcule le score. En mode réel, le score est écrit dans Airtable. Si une date de proposition existe, le programme examine d’abord le closing. Sans proposition antérieure, un score élevé mène à la création d’une offre ; les autres scores conduisent aux séquences de qualification ou de nurturing.

La proposition possède une référence déterminée à partir de l’identifiant du lead et de l’année. Le programme construit une clé d’action et consulte le journal. Si cette action a déjà été enregistrée, il peut rétablir la date de proposition dans Airtable sans renvoyer le message. Sinon, il génère le document, vérifie l’adresse et appelle l’adaptateur d’email.

Après un succès d’envoi, le journal est enregistré avant l’écriture de la date CRM. Cet ordre permet de traiter un échec tardif d’Airtable. Il subsiste une fenêtre entre l’envoi externe et l’écriture locale : une interruption à cet instant peut laisser l’envoi sans trace. La séquence explique donc à la fois le progrès réalisé et la limite de la garantie anti-doublon.

### 2.3.1 Séquence de nurturing

@table Tableau 2.4 : Jalons des séquences de qualification et de nurturing
| Jour | Canal actuel | Objet métier | Scénario |
| J0 | Email | Remercier et préciser objectifs, participants et calendrier. | Qualification et nurturing. |
| J3 | WhatsApp | Proposer le programme et un échange sur le besoin. | Qualification et nurturing. |
| J7 | Email | Relier le format aux situations professionnelles. | Qualification et nurturing. |
| J14 | WhatsApp | Vérifier l’avancement et les disponibilités. | Nurturing uniquement. |
| J21 | Email | Clore la séquence en restant disponible. | Nurturing uniquement. |

La qualification courte utilise les jours 0, 3 et 7 ; le nurturing long ajoute les jours 14 et 21. L’ancrage est date_premier_contact. Si cette date manque, le pipeline ignore le nurturing pour le lead et l’annonce dans la sortie. Une date mal formée provoque une erreur de traitement du dossier.

Le programme recherche le jour exact dans la séquence. Si un traitement prévu à J3 n’est relancé qu’à J4, il n’existe pas de rattrapage automatique. Il n’y a pas non plus de synchronisation avec les réponses reçues. Pour une utilisation régulière, il faudra définir la politique de rattrapage, la suspension et l’annulation des contacts futurs lorsqu’un prospect répond ou s’oppose aux sollicitations.

### 2.3.2 Séquence de closing

@diagram timeline|Figure 2.3 : Chronologie du suivi commercial après proposition

Le closing utilise date_envoi_proposition comme date d’ancrage. À J5, un message WhatsApp demande si la proposition a été consultée. À J8, un email ouvre la discussion sur le budget, l’organisation et le contenu. À J12, le programme affiche une action humaine d’appel. Il ne passe pas l’appel et ne l’enregistre pas comme un message envoyé.

Le journal intervient pour les actions email et WhatsApp, à partir du lead, du jour, de la séquence, de l’ancrage et du canal. La présence d’une date de proposition donne priorité à cette branche sur le nurturing. La version actuelle ne vérifie pas explicitement le statut signé avant cette branche : un client signé peut donc continuer à être candidat à une relance si les dates correspondent. Cette règle d’exclusion doit être ajoutée avant une exploitation autonome.

### 2.3.3 Séquence de contractualisation et facturation

E8 lit les leads signés et ignore ceux qui possèdent déjà un numéro de facture. Il recherche ensuite une action de facturation antérieure dans le journal. Si elle existe, il réconcilie le numéro dans Airtable ; sinon, il calcule le prochain numéro, le réserve dans l’exécution et génère la convention ainsi que la facture.

Les deux documents sont joints au même email. Un échec d’envoi empêche la mise à jour du numéro de facture dans le CRM. Un succès conduit à l’enregistrement du journal puis à l’écriture CRM. Ce numéro signale l’émission du dossier, pas son règlement. La convention reprend le suffixe de la facture, ce qui facilite la correspondance documentaire sans constituer un système comptable complet.

## 2.4 Diagramme de classes et modèle de données

@diagram classes|Figure 2.4 : Modèle conceptuel des données manipulées par ADG-10

Le noyau est constitué du Lead et de la Formation. Une formation peut concerner plusieurs leads ; une proposition relie un dossier à une offre. Une action de suivi référence le lead, la séquence et le canal. La facturation associe une convention et une facture au dossier commercial. Ces relations sont réparties entre les tables Airtable, les fichiers PDF et le journal JSON.

Le modèle conceptuel aide à identifier les informations actuellement implicites. Le lead porte un seul numéro de facture et une seule date de proposition, ce qui limite le suivi de plusieurs offres ou commandes pour un même contact. Il n’existe pas de table dédiée aux versions de propositions ni aux paiements. Une évolution vers un historique complet devra introduire des entités distinctes et des identifiants stables.

### 2.4.1 Règles d’intégrité

L’association à la formation accepte une liste d’identifiants, un identifiant simple ou un titre reconnu. En l’absence de correspondance, le code retourne la première formation. Ce repli permet une compatibilité avec les anciennes données, mais il peut produire une offre sans rapport avec la demande. La règle cible est de bloquer l’émission et de demander une correction lorsque la relation n’est pas certaine.

Les montants doivent être stockés sous une forme non ambiguë, avec une devise et une règle fiscale validée. La priorité actuelle entre prix_ht, prix_facture et prix_inter diffère de l’affichage de prix_inter dans la proposition. Sans contrôle d’égalité, le montant proposé et celui facturé peuvent diverger. Une source tarifaire unique et une version de prix par offre sont nécessaires pour éviter cet écart.

Les dates de contact et de proposition utilisent le format AAAA-MM-JJ ; le journal enregistre un horodatage UTC. Les statuts doivent utiliser des types cohérents. Le traitement E8 reconnaît plusieurs valeurs textuelles de signature, tandis que le dashboard teste directement leur vérité logique. Une chaîne telle que « false » peut ainsi produire une représentation erronée dans l’interface si le champ n’est pas un booléen réel.

### 2.4.2 Indicateurs de pilotage

@table Tableau 2.5 : Indicateurs disponibles et indicateurs à instrumenter
| Indicateur | Calcul ou source | Disponibilité |
| Volume de leads | Nombre de lignes chargées. | Affiché ; inclut aussi les dossiers signés et facturés. |
| Score moyen | Moyenne des scores enregistrés. | Affiché, avec conversion numérique. |
| Opportunités prioritaires | Nombre de scores au moins égaux à 8. | Affiché, sans exclusion des clients signés. |
| Clients signés | Statuts dérivés Signé ou Facturé. | Affiché selon les données renseignées. |
| Délai de première réponse | Première action moins date de capture. | À instrumenter de manière complète. |
| Taux de conversion | Clients acquis / population et période définies. | À construire ; non mesuré dans ce rapport. |
| Taux d’échec | Actions échouées / actions tentées. | Bilan par exécution ; agrégation à développer. |

## Conclusion

Les besoins et les diagrammes montrent que la continuité du dossier dépend autant des données que des fonctions d’envoi. La version actuelle relie les principales étapes et conserve une partie de l’état. Les prochaines améliorations concernent surtout les règles d’intégrité, les changements de scénario et la persistance des actions. L’étude technique précise comment ces responsabilités sont réparties dans le code.

# Chapitre 3 : Étude technique

## Introduction

Ce chapitre présente le langage, les bibliothèques, les services et les outils employés. Il décrit ensuite l’architecture du prototype, le parcours des données et les mécanismes de gestion d’erreur. L’analyse de la sécurité et de la dette technique distingue les corrections déjà réalisées des points à traiter avant un déploiement partagé.

## 3.1 Technologies de développement

### 3.1.1 Langages

Python porte les règles métier, les traitements de données et les intégrations. Son organisation en modules permet de tester le scoring ou la numérotation sans lancer l’interface ni communiquer avec un service externe. Les scripts principaux exposent une fonction main et un point d’entrée protégé, ce qui limite les effets indésirables lors d’un import. La documentation officielle est utilisée comme référence du langage et de sa bibliothèque standard [1].

L’interface est construite en Python avec Streamlit. Un bloc CSS intégré définit les couleurs, les cartes d’indicateurs, la barre latérale et les boutons. Il ne s’agit pas d’un frontend Angular, React développé séparément ou TypeScript : le code du projet ne contient pas ce type de couche applicative. JSON représente les réponses de contenu et le journal d’envoi ; les PDF sont les artefacts documentaires livrés aux utilisateurs.

### 3.1.2 Bibliothèques et frameworks

@table Tableau 3.1 : Bibliothèques et responsabilités actuelles
| Composant | Responsabilité dans ADG-10 |
| Streamlit | Interface, onglets, formulaires de pilotage, affichage et cache. |
| pandas | Construction des tableaux, conversion des scores et agrégations. |
| pyairtable | Lecture et mise à jour des tables du CRM. |
| groq | Client de génération des contenus de formation. |
| python-dotenv | Chargement de la configuration locale. |
| ReportLab | Mise en page des propositions, conventions et factures. |
| pywhatkit | Pilotage de WhatsApp Web pour les envois réels. |
| email et smtplib | Construction MIME et transmission des emails. |
| unittest | Vérification automatisée des fonctions métier. |

Streamlit permet de construire des applications de données avec une interface Python [2]. Dans ADG-10, il simplifie le passage du terminal à un écran de pilotage. Le cache de quinze secondes limite les lectures répétées d’Airtable. Il doit être invalidé après une exécution pour que l’utilisateur puisse consulter les données mises à jour.

ReportLab remplace FPDF2 pour la génération documentaire. Le projet partage un thème entre les trois documents et utilise des composants réutilisables pour les titres, blocs d’identité, tableaux et signatures. Les polices DejaVu sont intégrées depuis le projet, ce qui évite de dépendre d’une police installée sur le poste de destination. La documentation ReportLab sert de référence pour la construction des PDF [5].

### 3.1.3 Services web et messagerie

Le client Airtable est créé à la demande et mis en cache. Les fonctions get_all_records et update_record encapsulent les opérations nécessaires aux scripts. Les données reviennent sous forme de dictionnaires avec un identifiant et un ensemble de champs. Cette approche est adaptée au prototype ; elle laisse aux fonctions métier la validation du schéma et des valeurs [3].

La génération appelle Groq avec le modèle configuré dans le code, openai/gpt-oss-120b, une température de 0,45 et une limite de 2 000 tokens. Le prompt fixe le public, la formation et les contraintes éditoriales. Ces paramètres décrivent le code observé ; ils ne garantissent pas la disponibilité future du modèle ni le coût d’un compte. La documentation du service est référencée pour son interface [4].

L’email utilise smtp.gmail.com sur le port 587, avec STARTTLS et un délai de connexion de trente secondes. EmailMessage construit le texte, l’option HTML éventuelle et les pièces jointes ; un identifiant de message et une adresse de réponse sont ajoutés. Le succès de l’appel SMTP indique une acceptation par le serveur, sans prouver l’arrivée en boîte de réception ni la lecture [6].

WhatsApp utilise pywhatkit et une session WhatsApp Web. L’import est différé jusqu’à un envoi réel, ce qui permet aux tests et à la simulation de fonctionner sans automatiser le navigateur. La validation du numéro se limite actuellement à la présence d’un préfixe « + ». Une API professionnelle et des accusés de livraison constitueraient une évolution distincte ; ils ne sont pas présents dans le dépôt.

### 3.1.4 Système de gestion des données

Airtable est le référentiel principal pour les formations et les leads. Son intérêt est de rendre les fiches accessibles à l’équipe métier tout en proposant une API aux scripts. Le programme ne crée pas automatiquement un schéma complet ni des migrations. L’installation suppose donc des tables et des champs compatibles avec le README et le dictionnaire fourni en annexe.

Le stockage local complète le CRM. Les PDF sont placés dans output/pdf ; les événements envoyés sont enregistrés dans .runtime/dispatch_log.json. Ce partage répond aux besoins d’un prototype sur un poste, mais impose de sauvegarder l’état local. La suppression ou la perte du journal peut rendre des actions anciennes invisibles au mécanisme anti-doublon.

### 3.1.5 Outils de développement

Git conserve les modifications du code ; le README explique l’installation et les commandes ; .env.example expose les paramètres attendus sans fournir les secrets. L’environnement virtuel isole les dépendances Python. Les tests unitaires sont regroupés dans tests/test_business_rules.py, tandis que les scripts manuels d’intégration sont protégés contre une exécution au simple import.

L’ancien rapport présentait Visual Studio Code comme outil d’édition. Le fonctionnement de l’application n’exige pas cet éditeur en particulier. La version actuelle comporte encore des modifications non commitées et des suppressions préparées dans l’index Git. Cet état de travail doit être distingué d’une livraison versionnée, taguée et déployée.

#### 3.1.5.1 Environnement matériel

Le projet est examiné sur un poste Windows. Les traitements locaux concernent principalement le calcul de règles, la préparation de tableaux et la génération de documents. Le modèle de langage est appelé à distance ; aucun modèle volumineux n’est exécuté localement. Le rapport ne fournit pas de spécifications matérielles non mesurées, telles qu’un processeur ou une quantité de mémoire supposée.

La disponibilité du réseau et de la session graphique compte davantage que la puissance de calcul pour certains scénarios. En particulier, WhatsApp Web dépend d’un navigateur connecté. Cette dépendance rend un déploiement sur un serveur sans interface graphique différent d’un lancement sur le poste du stagiaire.

#### 3.1.5.2 Environnement logiciel

L’environnement du projet contient les dépendances de requirements.txt et un interpréteur dans .venv. Le contrôle pip check exécuté pour le rapport n’a détecté aucun conflit de dépendances installé. Il ne constitue pas un audit de vulnérabilités. Les versions ne sont pas verrouillées dans le fichier de dépendances ; une réinstallation future pourrait donc résoudre des versions différentes.

Une configuration reproductible devra documenter la version de Python, figer les dépendances retenues et séparer les paramètres de test et de production. Le chargement .env est ancré sur le répertoire du projet. Les sorties et les polices utilisent également des chemins explicites, ce qui réduit les erreurs liées au répertoire depuis lequel une commande est lancée [7].

## 3.2 Architecture technique

@diagram architecture|Figure 3.1 : Architecture technique actuelle du prototype ADG-10

La couche de présentation est app.py. Elle consulte les données et lance des scripts dans des processus distincts. La couche d’orchestration regroupe run_pipeline.py et les commandes run_e*.py. Les modules métier définissent les scores, les séquences, les références et les textes. Les adaptateurs communiquent avec Airtable, Groq, SMTP et WhatsApp Web. Les générateurs PDF utilisent le thème partagé.

Cette organisation constitue une application modulaire à plat. Elle facilite l’identification d’une responsabilité, mais les scripts partagent encore une configuration globale et des accès directs aux modules. L’ajout de plusieurs utilisateurs, d’une file de travaux ou d’une API devra s’accompagner d’un service d’exécution commun et d’un stockage transactionnel. Une architecture distribuée n’est pas justifiée par la seule présence de services externes.

### 3.2.1 Flux de données

Le flux commence par la lecture d’Airtable. Pour E1, la formation alimente le prompt, la réponse JSON est analysée, puis les champs validés sont mis à jour en mode réel. Pour E4-E7, les critères du lead alimentent le score et le choix de traitement. La proposition et les messages combinent les données du lead, de la formation et de l’entreprise. E8 utilise en plus les informations administratives et les références de facturation.

La configuration ne doit jamais être jointe à un message ni exposée dans un PDF. Les secrets servent uniquement à initialiser les clients des services. Les journaux et documents contiennent toutefois des informations de contact nécessaires à leur fonction. Leur accès et leur conservation doivent être définis au même titre que les accès au CRM.

### 3.2.2 Gestion des erreurs

Le chargement Airtable est une condition initiale : un échec empêche l’exécution utile du pipeline et retourne un code non nul. Pendant le traitement, une erreur propre à un lead est comptabilisée et permet de poursuivre sur les autres dossiers. Le bilan indique les actions, les éléments ignorés et les erreurs. Cette granularité évite qu’un seul contact mal renseigné arrête systématiquement tout le lot.

ContentGenerationError protège les contenus existants contre une réponse Groq invalide. La validation vérifie que le résultat est un objet et que les quatre champs attendus existent avec une représentation textuelle non vide. Elle ne garantit pas les bornes exactes de mots, le nombre de bénéfices ou la qualité factuelle. Des valeurs de types inattendus peuvent être converties en chaînes : un schéma strict reste une amélioration nécessaire.

L’email retourne False lorsqu’un destinataire est invalide, qu’une pièce jointe manque ou qu’une exception survient lors de la connexion ou de l’envoi. Une validation fondée sur la seule présence de « @ » reste élémentaire. Il n’existe pas encore de classification complète des erreurs temporaires, de reprises avec attente progressive ou de file d’examen manuel.

Le journal écrit d’abord un fichier temporaire puis remplace le fichier principal. Cette opération limite les écritures incomplètes, sans verrouiller les exécutions concurrentes. Un JSON syntaxiquement corrompu provoque une erreur ; en revanche, un JSON valide de type liste est actuellement interprété comme un journal vide. Cette différence doit être corrigée pour éviter de perdre silencieusement la capacité de détection des actions antérieures.

### 3.2.3 Sécurité et confidentialité

La simulation par défaut et la confirmation de production constituent des protections opérationnelles. Le dashboard ne fournit cependant pas d’authentification applicative, de rôles ou de limitation d’accès multiutilisateur. Son exposition au-delà d’un poste de confiance exige une protection d’accès et une gestion explicite des opérateurs autorisés.

Le fichier .env et plusieurs artefacts locaux ont été retirés du suivi Git dans les modifications préparées ; les exclusions ont été complétées. Les anciens commits peuvent toujours contenir les secrets qui avaient été versionnés. Leur rotation et le traitement de l’historique restent des opérations à réaliser et à vérifier. Le rapport ne reproduit aucune valeur de jeton, aucun mot de passe ni information bancaire réelle.

La collecte de coordonnées impose aussi un cadre organisationnel de protection des données. Les ressources de la CNDP rappellent notamment l’information des personnes lors de la collecte et l’existence de formalités adaptées aux traitements. Pour ADG-10, il convient de faire valider la finalité, les accès, la conservation, l’opposition et les éventuels transferts liés aux prestataires. Le prototype ne fournit pas un module de gestion de ces demandes et aucune conformité complète n’est attestée dans ce rapport [9].

### 3.2.4 Dette technique observée

@table Tableau 3.2 : Dette technique résiduelle et conséquences
| Point observé | Conséquence | Évolution proposée |
| Relation formation facultative | Offre potentiellement associée à la première formation. | Relation obligatoire et contrôle bloquant. |
| Tarifs textuels et sources multiples | Écart possible entre proposition et facture. | Données monétaires structurées et versionnées. |
| Journal JSON sans verrou | Risque de doublon entre exécutions. | Stockage transactionnel et réservation atomique. |
| Jours exacts sans rattrapage | Une échéance peut être manquée. | Planificateur et politique de reprise. |
| Pas d’arrêt automatique sur réponse | Contact inadapté après décision ou opposition. | État commercial explicite et suspension. |
| Dépendances non figées | Réinstallation non strictement reproductible. | Verrouillage et vérification régulière. |
| E3 absente | Publication encore manuelle. | Connecteur autorisé et validation éditoriale. |

## Conclusion

Les choix Python, Airtable et Streamlit répondent à un objectif de prototype lisible et démontrable. La configuration, les modèles partagés et les tests constituent des progrès concrets. Les limites se concentrent désormais sur la qualité des données, les transactions entre services et l’exploitation régulière. Le chapitre suivant présente les fonctions réalisées et les résultats qui permettent de les apprécier.

# Chapitre 4 : Mise en œuvre

## Introduction

La réalisation transforme les modèles précédents en modules exécutables et en écrans. Ce chapitre détaille les étapes E1 à E8, les communications, la génération documentaire, les tests et le dashboard. Les captures sont issues de l’application actuelle avec un jeu fictif ; les documents présentés sont générés localement par les fonctions du projet.

## 4.1 Structure du projet

@table Tableau 4.1 : Organisation des modules Python
| Fichier ou groupe | Responsabilité |
| app.py | Dashboard et lancement des commandes. |
| config.py / airtable_client.py | Configuration et accès aux tables. |
| generation_contenu.py / run_e1_content.py | Génération IA et mise à jour des formations. |
| multichannel_generator.py / run_e2_multichannel.py | Déclinaisons LinkedIn et WhatsApp. |
| scoring.py / run_e4_scoring.py | Qualification et écriture des scores. |
| nurturing.py / closing.py | Messages et jours des séquences. |
| commercial_templates.py | Emails de proposition et de documents à signer. |
| proposal_generator.py / pdf_theme.py | Proposition et composants graphiques communs. |
| contract_generator.py / run_e8_contract.py | Convention, facture et orchestration E8. |
| email_sender.py / whatsapp_sender.py | Adaptateurs d’envoi et simulation. |
| pipeline_utils.py / state_store.py | Formation, numérotation et mémoire des envois. |
| run_pipeline.py | Traitement commercial E4 à E7. |
| tests/test_business_rules.py | Tests unitaires indépendants des envois externes. |

### 4.1.1 Ingestion et génération de contenu

E1 lit les formations disponibles et transmet au générateur le titre, la durée, le prix et le public. Le prompt demande un pitch court de 25 à 35 mots, un pitch long de 80 à 110 mots, trois bénéfices et trois questions-réponses. Il impose un ton B2B précis et demande de ne pas inventer de certification, de remise, de statistique ou de référence client. Ces contraintes orientent la rédaction ; elles ne remplacent pas une vérification du résultat.

La réponse du service est analysée comme JSON. Les quatre champs attendus sont pitch_30_mots, pitch_100_mots, benefices et faq. Les éventuelles balises Markdown autour du JSON sont retirées avant l’analyse. Si la structure est invalide, l’erreur est signalée et les contenus précédents de la fiche sont conservés. En simulation, la commande annonce les générations prévues sans appeler Groq.

Cette réalisation corrige l’état ancien de génération uniquement simulée. Elle ne réalise pas encore un circuit d’approbation éditoriale dans le dashboard. Le prix transmis au prompt est présenté comme HT ; la donnée source doit donc être fiable. Une formation sans description pédagogique suffisamment précise peut conduire à un texte trop général, même si sa structure est valide.

### 4.1.2 Génération multicanale

E2 transforme le pitch long en publication LinkedIn et le pitch court en message WhatsApp. Le texte LinkedIn ajoute une entrée centrée sur les compétences, le prix indicatif et une invitation à échanger. Le message WhatsApp adopte un format plus court, avec le nom de la formation et une proposition de programme. Les deux variantes réutilisent les mêmes informations de référence.

La commande affiche les textes. Elle ne crée pas de publication programmée et ne conserve pas un historique de campagne dans Airtable. Les formats carrousel, Reels, Instagram, Facebook et newsletter mentionnés dans la cible initiale ne sont pas produits par ces deux fonctions. E2 est donc partiellement couvert au regard de l’ensemble du cahier des charges, tandis qu’E3 reste à développer.

Un contrôle éditorial doit également confirmer les formulations de disponibilité. Le gabarit WhatsApp annonce de nouvelles sessions ; cette phrase ne doit être utilisée que si le calendrier est validé. La personnalisation améliore la présentation, mais ne rend pas automatiquement exactes toutes les affirmations d’un modèle de message.

### 4.1.3 Scoring et routage

La fonction calculer_score additionne les cinq contributions et arrondit le total. Elle ne dépend ni d’Airtable ni d’un modèle de langage. Cette indépendance permet d’expliquer la décision et de tester des valeurs limites. La fonction get_routing associe le score à une consigne commerciale. La définition dupliquée signalée dans l’ancien rapport n’est plus présente dans le module examiné.

Prenons un cas fictif : budget de 6 000 MAD, démarrage sous un mois, contact DRH, entreprise PME et canal email direct. Les contributions sont respectivement 3,0 ; 2,5 ; 2,0 ; 1,5 et 0,5. Le total est 9,5 sur 10, donc prioritaire. Avec un budget de 2 000, une urgence de trois à six mois, un prescripteur, une TPE et un email direct, le total devient 5,0 : le lead suit la qualification courte.

Ces exemples illustrent les règles sans mesurer la probabilité réelle d’achat. Le score constitue une priorité opérationnelle. Son efficacité prédictive devra être étudiée en comparant les décisions commerciales et les conversions observées. Les pondérations ne sont pas apprises automatiquement à partir des résultats.

### 4.1.4 Nurturing

Les messages de nurturing sont désormais rédigés comme des échanges utilisables : salutation, contexte de formation, proposition d’aide et prochaine étape. Le nom du contact, le titre de la formation et la signature sont injectés par des fonctions partagées. Cette centralisation évite la répétition de textes légèrement différents dans chaque script.

Le programme calcule les jours écoulés depuis le premier contact. Il choisit ensuite la séquence courte ou longue en fonction du score. La clé d’envoi tient compte du scénario ; un même jour peut donc correspondre à une action distincte si le scénario change. Cette souplesse exige de définir les règles de transition pour ne pas créer de sollicitations redondantes après une requalification.

L’ancien rapport indiquait des messages seulement descriptifs et une couverture multicanale incomplète. Les gabarits actuels sont personnalisés et l’adaptateur WhatsApp existe. La limite principale reste la cadence d’exécution et le suivi des réponses : aucun service permanent n’exécute les échéances sans un lancement programmé ou manuel.

### 4.1.5 Proposition et e-mail

La proposition est produite par generer_proposition_pdf. Elle contient une référence stable pour le lead dans l’année, une date, une validité de trente jours, les coordonnées du prospect, la solution, les bénéfices attendus, l’approche pédagogique, l’investissement et les étapes de validation. Les conditions et une zone de bon pour accord complètent le document. Le thème commun définit la typographie, les couleurs et la pagination.

@image proposition-1.png|Figure 4.1 : Première page d’une proposition générée par le code actuel, données fictives|425

La proposition utilise le prix_inter affiché comme investissement HT. Elle ne produit pas un calcul exhaustif HT, TVA et TTC, contrairement à la facture. Elle ne contient pas automatiquement une biographie validée du formateur, des témoignages ou un programme détaillé par séquence pédagogique. Ces éléments doivent provenir du catalogue et être ajoutés si le besoin commercial les exige.

L’email de proposition reprend la référence dans son objet et précise le contenu de la pièce jointe. Il invite à un échange pour valider les prochaines étapes. L’adaptateur contrôle l’existence de chaque pièce jointe avant la simulation ou l’envoi. Le support de plusieurs fichiers est utilisé par E8. La génération d’un Message-ID facilite l’identification technique, mais ce champ ne remplace pas un identifiant métier stable de dossier.

### 4.1.6 Relances et closing

Les messages de closing cherchent à identifier le point qui bloque la décision. Le message J8 évoque trois possibilités concrètes : budget, organisation et contenu. Il propose un ajustement du périmètre ou du calendrier sans promettre de remise automatique. La séquence conserve un appel humain à J12 pour clarifier la décision et convenir d’une prochaine action datée.

Le module WhatsApp peut déclencher un envoi via le navigateur connecté. Son retour True traduit l’absence d’exception pendant l’automatisation, et non une confirmation métier de réception. Une erreur peut être liée au numéro, à la session, au chargement du navigateur ou au service. Le rapport ne présente donc pas cette fonction comme une intégration WhatsApp Business avec suivi de délivrance.

### 4.1.7 Convention, facture et phase E8

La convention structure les parties, le périmètre de formation, les objectifs, les obligations, les conditions financières, le report ou l’annulation, la confidentialité et les signatures. Les informations de l’organisme proviennent de Settings. Le document utilise les champs administratifs du client lorsqu’ils sont disponibles. Les clauses doivent être examinées par le responsable compétent avant une diffusion réelle.

@image convention-1.png|Figure 4.2 : Première page de la convention actuelle, exemple sans valeur contractuelle|420

La facture présente l’émetteur, le client, les dates, une ligne de prestation, le montant HT, la taxe et le total. La numérotation recherche le plus grand suffixe du préfixe annuel et tient compte des réservations de l’exécution. Par exemple, si FAC-2026-001 et FAC-2026-003 existent, le candidat suivant est FAC-2026-004. La convention correspondante utilise CONV-2026-004.

@image facture-1.png|Figure 4.3 : Facture produite avec un jeu de démonstration, non destinée à émission|400

Des limites financières doivent être traitées. La quantité est fixée à un. Le parseur prend le premier montant d’une fourchette et peut transformer une valeur illisible en zéro. Les calculs utilisent des flottants. L’expression actuelle du taux remplace une valeur numérique zéro par 20 ; l’échéance est fixée à trente jours. Ces comportements sont des constats techniques et ne constituent pas une règle fiscale recommandée.

La réussite d’E8 est la préparation ou l’envoi de deux documents et la mise à jour de suivi après succès. Elle n’inclut pas de preuve de signature, de rapprochement bancaire, d’avoir, de relance de paiement ou d’onboarding pédagogique. La matrice de conformité conserve donc un état partiel pour E8 au regard de la cible complète, malgré l’existence effective du module documentaire.

### 4.1.8 Professionnalisation des communications

Les modèles partagés uniformisent la salutation, la présentation de la formation et la signature. Les textes évitent les promesses non étayées et proposent une prochaine action explicite. Les coordonnées de signature proviennent de la configuration de l’entreprise. Leur absence doit être corrigée avant un envoi afin de ne pas diffuser un message sans interlocuteur identifiable.

@example Exemple de message de proposition
Objet : Votre proposition de formation | PROP-2026-DEMO

Bonjour Contact Alpha,

Merci pour l’intérêt porté à notre accompagnement. Vous trouverez en pièce jointe notre proposition pour « Intelligence artificielle appliquée aux métiers ».

Elle reprend le format recommandé, les objectifs, les modalités d’intervention et l’investissement correspondant. Nous restons disponibles pour l’ajuster à vos priorités, au niveau des participants et à votre calendrier.

Je vous propose un court échange afin de valider ensemble les prochaines étapes.

Cordialement,
Équipe pédagogique - exemple de démonstration
@endexample

Cet exemple reprend le modèle applicatif avec une identité fictive. Il illustre le contenu préparé et ne constitue pas une preuve d’envoi réel. L’ancienne capture d’email du rapport initial n’est pas réutilisée comme preuve de recette de la version actuelle.

## 4.2 Tests de bon fonctionnement

Les vérifications ont été exécutées le 17 septembre 2026. La commande unittest a terminé avec onze tests réussis. L’analyse syntaxique a porté sur vingt-huit fichiers Python propres au projet. Le contrôle de dépendances a renvoyé « No broken requirements found ». Les scripts temporaires de génération de ce rapport ne sont pas inclus dans le compte des fichiers applicatifs.

@table Tableau 4.2 : Tests unitaires effectivement exécutés
| Domaine | Cas couvert | Résultat |
| Scoring | Score maximal avec valeurs normalisées. | Réussi. |
| Routage | Score intermédiaire vers la qualification courte. | Réussi. |
| Formation | Sélection par identifiant de fiche lié. | Réussi. |
| Messages | Personnalisation sans certaines affirmations non vérifiées. | Réussi. |
| Prix | Formats usuels de prix. | Réussi. |
| Proposition | Stabilité de la référence. | Réussi. |
| Facture | Maximum existant et numéros réservés. | Réussi. |
| Convention | Réutilisation du suffixe de facture. | Réussi. |
| Journal | Enregistrement et détection d’une action. | Réussi. |
| Réconciliation | Recherche d’un envoi pour le suivi CRM. | Réussi. |
| Journal corrompu | Erreur sur un JSON syntaxiquement invalide. | Réussi. |

La couverture ne doit pas être surestimée. Le test de prix ne valide pas toutes les valeurs fiscales ni toutes les ambiguïtés textuelles. Le test du journal corrompu ne couvre pas encore le cas d’un JSON valide de type inattendu. Les tests de messages vérifient des formulations ciblées, sans certifier tout texte futur produit par l’IA.

Les captures du dashboard ont été obtenues avec le code app.py exécuté sur six leads et une formation fictifs. Les indicateurs affichent six leads, un score moyen de 7,4, quatre scores prioritaires et deux dossiers signés ou facturés. Cette observation vérifie le rendu de l’interface sur ce jeu ; elle ne prouve pas l’état d’un CRM réel. Aucun bouton d’envoi n’a été utilisé pour produire ces captures.

### 4.2.1 Critères de recette

La recette complète doit examiner les transitions du dossier et les cas d’échec, au-delà des fonctions isolées. Un lead incomplet doit être signalé sans émission erronée. Un envoi réussi suivi d’un échec CRM doit pouvoir être reconnu. Une nouvelle exécution ne doit pas répéter une action déjà confirmée. Un client signé ou opposé aux contacts doit sortir des séquences concernées.

@table Tableau 4.3 : Scénarios de recette et état de validation
| Scénario | Attendu | État actuel |
| Simulation du pipeline | Aucun envoi ni écriture CRM, PDF local possible. | Mécanisme présent ; recette intégrée à compléter. |
| Réponse IA invalide | Conservation du contenu antérieur. | Traitement codé ; essais fournisseurs à prévoir. |
| Pièce jointe absente | Échec explicite avant transmission. | Contrôle présent dans l’adaptateur. |
| Envoi réussi puis erreur CRM | Réconciliation sans renvoi. | Logique présente pour proposition et E8. |
| Deux exécutions simultanées | Une seule réservation et un seul envoi. | Garantie absente. |
| Échéance manquée | Politique de rattrapage définie. | Non implémentée. |
| Client signé ou désinscrit | Suspension des relances commerciales. | Contrôle à compléter dans le pipeline. |
| Réception réelle | Pièces jointes et message vérifiés côté destinataire. | Non validée dans cet audit. |

### 4.2.2 Matrice de conformité

@table Tableau 4.4 : Couverture actualisée des étapes E1 à E8
| Étape | Réalisation actuelle | Écart à la cible complète |
| E1 | Groq et quatre contenus JSON ; protection sur erreur. | Validation stricte, SEO et approbation éditoriale à compléter. |
| E2 | Formats LinkedIn et WhatsApp. | Autres formats et historique de campagne absents. |
| E3 | Aucune publication automatique. | Étape à développer. |
| E4 | Score pondéré, routage et écriture CRM. | Capture multicanale et schéma strict à intégrer. |
| E5 | Messages personnalisés, canaux et journal. | Planification, rattrapage et arrêt sur réponse manquants. |
| E6 | Proposition enrichie, validité, accord et email. | Programme détaillé, validation tarifaire et versionnage. |
| E7 | J5 WhatsApp, J8 email, J12 appel humain. | Suspension, délivrance et supervision à fiabiliser. |
| E8 | Convention, facture, email et réconciliation. | Fiscalité, signature, paiement et onboarding à compléter. |

La matrice évite d’attribuer un pourcentage global d’avancement sans méthode de mesure. Plusieurs étapes disposent désormais d’une réalisation substantielle, tout en restant partielles au regard du cahier des charges. La priorité est de valider les scénarios commercialement sensibles avant d’étendre le nombre de canaux ou de fonctionnalités.

## 4.3 Interfaces graphiques et résultats

L’interface actuelle remplace le terminal comme point d’entrée principal pour la consultation et le lancement des opérations. La barre latérale regroupe le mode d’exécution, les indications de configuration et l’actualisation. La zone principale présente les indicateurs, les commandes et les onglets. La palette bleu marine et turquoise et les cartes structurent la lecture.

@image dashboard.png|Figure 4.4 : Dashboard actuel exécuté avec six prospects fictifs|270

Les indications « configuré » signalent la présence de paramètres attendus. Elles ne représentent pas un test de connexion réussi. Les captures utilisent une source de données locale substituée pour la démonstration ; leur rôle est d’illustrer le rendu exact de l’application sans exposer les contacts réels. Le mode simulation est visible dans la barre latérale.

### 4.3.1 Tableau de bord actuel

@table Tableau 4.5 : Vues et commandes effectivement disponibles
| Élément | Contenu ou action |
| Vue d’ensemble | Répartition par statut et tableau des priorités. |
| Leads | Recherche nom/entreprise/email, filtres par statut et score visuel. |
| Formations | Titre, durée, prix, public et indication de contenu prêt. |
| Activité | Trente derniers envois du journal et nombre de PDF locaux. |
| Générer les contenus | Lance run_e1_content.py. |
| Recalculer les scores | Lance run_e4_scoring.py. |
| Lancer le pipeline | Lance run_pipeline.py. |
| Contrats et factures | Lance run_e8_contract.py. |

@image leads.png|Figure 4.5 : Recherche et filtrage des leads, jeu de démonstration|270

Le statut affiché est dérivé selon un ordre précis : facture renseignée, signature, proposition envoyée, score prioritaire, score intermédiaire, puis nurturing. L’étiquette « Leads actifs » compte en réalité toutes les lignes chargées. Le compteur prioritaire compte tous les scores élevés, y compris les dossiers déjà signés. Ces détails doivent être ajustés ou expliqués pour éviter une interprétation erronée des indicateurs.

Le dashboard affiche des tableaux de consultation ; il ne propose pas encore une fiche complète d’édition, une suspension de séquence, une assignation de commercial ou une gestion de campagne. Le journal « Derniers envois confirmés » est alimenté par le succès déclaré de l’adaptateur. Ce libellé doit être compris comme un retour technique, sans preuve systématique de réception externe.

### 4.3.2 Feuille de route d’industrialisation

La première priorité est la cohérence du dossier : relation obligatoire à la formation, prix structuré, types de statuts unifiés et arrêt des relances après décision. La deuxième porte sur la sécurité de l’exploitation : secrets renouvelés, accès protégé, environnement reproductible et sauvegarde de l’état. Ces travaux rendent les scénarios existants plus fiables.

@table Tableau 4.6 : Feuille de route et livrables attendus
| Horizon | Travaux | Preuve attendue |
| Court terme | Données obligatoires, prix, taxes, statuts et contrôle des documents. | Jeux de tests de limites et validation métier. |
| Court terme | Secrets, version des dépendances et accès au dashboard. | Configuration de livraison documentée. |
| Moyen terme | Journal transactionnel, réservation et planificateur. | Essais de concurrence, reprise et rattrapage. |
| Moyen terme | Recette Airtable, Groq, SMTP et WhatsApp. | Scénarios exécutés avec destinataires de test. |
| Moyen terme | Historique d’offre et gestion des réponses. | Dossier complet consultable et suspendable. |
| Long terme | Publication E3, autres formats et onboarding. | Intégrations approuvées et mesure de leur usage. |
| Long terme | Pilotage de conversion et amélioration des règles. | Indicateurs calculés sur une période définie. |

La montée en charge devra être décidée à partir d’un volume et d’une organisation réels. Pour plusieurs opérateurs, une base centrale et une file de tâches peuvent remplacer le journal local et les lancements directs. Un connecteur WhatsApp professionnel devra être évalué séparément si le suivi de délivrance devient indispensable. Aucune de ces évolutions n’est présentée comme déjà déployée.

## Conclusion

La réalisation actuelle couvre la génération IA, la qualification, les séquences, les documents commerciaux et un tableau de bord utilisable. Elle corrige plusieurs limites de l’ancien rapport et ajoute une base de tests. Les validations restantes concernent essentiellement les données engageantes, les services externes et l’exécution régulière. Le résultat constitue une base de pilote supervisé dont le périmètre et les limites sont identifiés.

# Conclusion Générale et Perspectives

Le projet ADG-10 répond au besoin de relier les étapes du cycle commercial d’une formation, depuis la préparation du contenu jusqu’aux documents client. La démarche d’analyse a permis d’expliciter les critères de qualification, les séquences, les relations entre les données et les responsabilités humaines. L’architecture Python modulaire traduit ces règles en fonctions et en scripts que l’on peut examiner séparément.

La version actualisée présente des avancées concrètes. Groq remplace la génération de texte uniquement simulée. Les communications sont personnalisées par des gabarits partagés. ReportLab harmonise la proposition, la convention et la facture. E8 existe désormais sous forme d’un flux documentaire et d’envoi. Le dashboard Streamlit offre une vue du portefeuille et un accès aux principales commandes. La configuration centralisée et la simulation par défaut rendent le comportement plus prévisible.

Le suivi des envois constitue un autre progrès. La référence des propositions ne dépend plus de l’ordre des leads, la numérotation des factures tient compte du maximum connu et les traitements peuvent réconcilier certaines erreurs d’écriture CRM. Les onze tests unitaires réussis apportent une base de non-régression. Les captures et les documents de démonstration montrent les résultats visuels de la version examinée.

Ces résultats ne démontrent pas une autonomie complète. E3 reste absent, les jours de relance exigent une exécution régulière et le journal local ne protège pas contre tous les cas d’interruption ou de concurrence. Les réponses des prospects ne sont pas automatiquement intégrées au scénario. Les données tarifaires, les règles de taxe et les informations contractuelles doivent être validées avant une émission réelle. La recette des services reste une étape distincte des tests métier.

La perspective immédiate consiste à consolider les scénarios existants dans un pilote contrôlé. Il faudra d’abord fiabiliser les données obligatoires et les états commerciaux, puis vérifier les envois et les reprises sur des comptes de test. L’étape suivante pourra introduire une persistance centrale, une planification et un suivi de dossier plus complet. Les canaux supplémentaires et l’onboarding viendront ensuite, selon les priorités du centre et les résultats mesurés.

Le travail mobilise l’analyse fonctionnelle, la modélisation, la programmation Python, l’intégration de services et la conception d’interfaces et de documents. Il met en évidence une exigence essentielle du projet : une automatisation commerciale utile doit conserver une relation fiable entre le besoin du prospect, la décision du programme et l’action effectivement réalisée. Cette exigence fournit le critère de progression pour les prochaines versions d’ADG-10.

# Webographie

Les ressources ci-dessous complètent l’analyse du code. Les liens documentaires concernent les technologies employées ; ils ne constituent pas une preuve de fonctionnement de l’installation locale. Les pages accessibles ont été consultées le 17 septembre 2026.

[1] Python Software Foundation. Documentation Python 3. https://docs.python.org/3/

[2] Streamlit. Documentation officielle. https://docs.streamlit.io/

[3] pyAirtable. Documentation du client Python pour Airtable. https://pyairtable.readthedocs.io/en/stable/

[4] Groq. Documentation de l’API et vue d’ensemble. https://console.groq.com/docs/overview

[5] ReportLab. Documentation officielle. https://docs.reportlab.com/

[6] Python Software Foundation. Module smtplib. https://docs.python.org/3/library/smtplib.html

[7] python-dotenv. Documentation du projet. https://pypi.org/project/python-dotenv/

[8] Git. Documentation officielle. https://git-scm.com/doc

[9] CNDP. Foire aux questions et formalités de protection des données. https://www.cndp.ma/faq/ ; https://www.cndp.ma/formalites/

[10] Rapport_Stage_ADG10_Yassine_Fatnaoui.pdf. Rapport de référence fourni pour le projet ; état antérieur à la présente mise à jour.

[11] exemple de rapport.docx. Modèle de structure fourni pour le rapport de stage.

[12] Dépôt ADG10-project. Code, README, configuration d’exemple et tests examinés le 17 septembre 2026. L’analyse porte sur l’espace de travail, comprenant des modifications non commitées.

# Annexes

## Annexe A : Dictionnaire des données

Ce dictionnaire décrit les champs consommés par le code. Il ne constitue pas une migration automatique d’Airtable. Les types indiqués sont ceux à privilégier pour éviter les conversions implicites et les valeurs ambiguës.

@table Tableau A.1 : Champs de la table Formations
| Champ | Type conseillé | Utilisation |
| titre | Texte obligatoire | Identification de la formation et documents. |
| duree / public | Texte | Cadrage du contenu et présentation de l’offre. |
| prix_inter | Nombre ou montant normalisé | Prompt, publication et proposition. |
| prix_ht / prix_facture | Nombre monétaire | Prioritaires dans le calcul de convention et facture. |
| taux_tva | Nombre validé | Calcul documentaire ; cas zéro à corriger. |
| pitch_30_mots / pitch_100_mots | Texte long | Messages courts, publication et offre. |
| benefices / faq | Texte long structuré | Argumentaire et réponses aux questions. |
| modalite / lieu / date_session | Texte ou date selon champ | Organisation de la session. |
| objectifs / methodes_pedagogiques | Texte long | Convention et approche pédagogique. |

@table Tableau A.2 : Champs de la table Leads
| Champ | Type conseillé | Utilisation |
| nom_prenom / entreprise | Texte | Identité et personnalisation. |
| email / telephone | Coordonnées validées | Destinataires des canaux. |
| adresse / ice / if / rc / tp / cnss | Texte administratif | Parties et mentions des documents. |
| budget_declare | Nombre | Critère de scoring. |
| urgence / decideur / taille_entreprise / canal_entree | Choix normalisés | Sous-notes de qualification. |
| formation | Relation vers Formations | Offre demandée ; à rendre obligatoire. |
| score | Nombre de 0 à 10 | Consultation et routage. |
| date_premier_contact | Date AAAA-MM-JJ | Ancrage des séquences E5. |
| date_envoi_proposition | Date AAAA-MM-JJ | Ancrage du closing. |
| client_signe | Booléen | Éligibilité E8 et statut ; sens métier à préciser. |
| numero_facture | Texte | Suivi d’émission et prévention de retraitement. |

## Annexe B : Guide d’installation et d’exécution

Le lancement s’effectue depuis le dossier ADG10-project. Un environnement Python est créé, les dépendances sont installées puis .env est renseigné à partir de .env.example. Les tables Airtable doivent correspondre aux champs décrits. Les paramètres d’entreprise et de signature doivent être relus avant une utilisation documentaire réelle.

@code
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
@endcode

Une fois Streamlit lancé, le dashboard est accessible sur http://localhost:8501 tant que le processus reste actif. La présence des paramètres n’atteste pas l’accès aux services. En cas d’erreur Airtable, vérifier la base, les permissions et les noms de tables sans afficher les secrets dans les journaux ou dans un rapport.

@code
.\.venv\Scripts\python.exe run_e1_content.py --dry-run
.\.venv\Scripts\python.exe run_e4_scoring.py --dry-run
.\.venv\Scripts\python.exe run_pipeline.py --dry-run
.\.venv\Scripts\python.exe run_e8_contract.py --dry-run
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
@endcode

Le paramètre --live autorise les effets externes des scripts concernés. Il doit être utilisé seulement sur le périmètre de dossiers retenu et après validation des données. Le mode simulation peut créer des fichiers locaux ; il ne fournit pas une prévisualisation intégrale de toutes les réponses des services. E1, notamment, n’appelle pas Groq dans ce mode.

Les répertoires output/pdf et .runtime ne doivent pas être confondus : le premier contient les documents ; le second conserve la mémoire des envois. Une sauvegarde d’exploitation doit tenir compte des deux. La perte du journal peut permettre la répétition d’actions que le CRM ne suffit pas à reconnaître.

## Annexe C : Protocole de recette proposé

La recette doit être menée sur une base et des destinataires de test identifiables. Elle commence par les fonctions locales, puis vérifie séparément l’accès aux services, avant un parcours complet. Chaque essai doit conserver l’entrée, l’action attendue, le résultat et l’état final du dossier, sans inclure les mots de passe ni les jetons dans les preuves.

@table Tableau C.1 : Parcours de recette à exécuter
| Essai | Données / action | Résultat à contrôler |
| R01 | Formation valide, E1 réel en test. | Quatre contenus exploitables et aucun champ antérieur perdu sur erreur. |
| R02 | Scores bas, intermédiaire et élevé. | Calculs, seuils et routages conformes aux règles. |
| R03 | Lead prioritaire complet. | Offre liée à la bonne formation, email de test et date CRM. |
| R04 | Deuxième lancement du même dossier. | Absence de second envoi reconnu par le journal. |
| R05 | Erreur CRM après envoi enregistré. | Réconciliation lors de la reprise. |
| R06 | Email invalide ou fichier absent. | Échec explicite sans marquage facturé. |
| R07 | Client signé avec données complètes. | Convention, facture et numéro cohérents. |
| R08 | Prix nul, fourchette, TVA zéro. | Correction préalable ; émission bloquée si données ambiguës. |
| R09 | Jour manqué ou opposition du prospect. | Politique de rattrapage et suspension validée après développement. |
| R10 | Deux traitements concurrents. | Vérifier la garantie après stockage central et verrouillage. |

## Annexe D : Traçabilité de la mise à jour

Le plan conserve les quatre chapitres et leurs grandes rubriques : organisme et conduite du projet, analyse et conception, étude technique, mise en œuvre. Les éléments d’un autre projet présents dans le Word ont été remplacés par les contenus propres à ADG-10. Les diagrammes et la matrice sont actualisés ; les captures anciennes ne sont pas utilisées comme preuves de la nouvelle version.

La page de garde est reprise sans modification depuis le PDF de référence le plus récent, qui porte l’année 2025-2026. Les chapitres décrivent l’état examiné le 17 septembre 2026. Les exemples documentaires portent des références de démonstration et utilisent des coordonnées fictives. Le code applicatif n’a pas été modifié pour produire le rapport ; seule une source illustrative temporaire a alimenté les captures.
