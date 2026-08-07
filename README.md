# Carrière Kit

Un système de pilotage de recherche d'emploi / de candidatures, conçu pour être opéré avec un agent IA (Claude Code, Cursor, ou n'importe quel assistant qui lit des fichiers dans un dossier).

Ce n'est pas un template de CV. C'est un **dossier de travail structuré + une méthode écrite**, construits à partir d'une campagne réelle de plus de 25 candidatures (fédérations, cabinets de conseil, institutions européennes, entreprises tech) menée sur trois mois : ce qui a marché, ce qui a bouncé, ce qui a été refusé par un filtre automatique en 48h, et pourquoi.

> Langue : français. Les templates de CV et d'emails existent en FR et EN.

---

## Le problème que ça résout

Une recherche d'emploi sérieuse, c'est 20 à 40 pistes en parallèle, chacune avec son contact, sa langue, son angle, sa date de relance, son statut. Sans structure, deux choses arrivent : on oublie des relances, et on envoie des emails génériques parce qu'on n'a plus le contexte en tête au moment d'écrire.

Le kit répond aux deux :

| Symptôme | Réponse du kit |
|---|---|
| « J'ai oublié de relancer » | `calendrier.md` : toutes les dates, un seul endroit, ordre chronologique |
| « Où j'en suis avec eux, déjà ? » | `tracker.md` : une ligne par piste, statut + dernière action + prochaine action |
| « Mon email sonne comme un template » | `methode/01-outreach-email.md` : 7 anti-patterns nommés, tirés de diffs réels |
| « L'adresse a bouncé » | `methode/02-verification-contact.md` : vérifier avant d'envoyer, dans cet ordre |
| « J'ai écrit en français à quelqu'un qui bosse en anglais » | `methode/03-langue-et-region.md` |
| « Je refais le même CV pour la dixième fois » | `templates/cv/` : un CV HTML une page, A4, → PDF en une commande |
| « Mon agent IA me sort du coaching carrière générique » | `methode/04-anti-patterns-carriere.md` : garde-fous explicites |

---

## Installation

```bash
git clone <url-du-repo> ma-carriere
cd ma-carriere
```

Puis :

```bash
./init.sh
```

Le script copie les templates à la racine sous leur nom de travail (`CLAUDE.md`, `profil.md`, `tracker.md`, `calendrier.md`, `entreprises.md`, `vision.md`, `positionnement.md`, `storytelling.md`) et crée `candidatures/` et `prive/`. Il est idempotent : il n'écrase jamais un fichier existant, on peut le relancer sans risque.

Ensuite, dans l'ordre :

1. **Remplir `profil.md`.** Source de vérité unique sur qui vous êtes : tous les CV et emails en découlent, aucun chiffre ne doit être cité s'il n'y figure pas avec sa date de vérification.
2. **Adapter `CLAUDE.md`.** C'est le fichier que votre agent IA lit à chaque session : positionnement, non-négociables, structure du dossier. Remplacer tous les `{{PLACEHOLDERS}}`.
3. **Lire la méthode.** `methode/00-vue-densemble.md` (5 minutes) puis `methode/01-outreach-email.md` avant votre premier envoi.

## Utilisation quotidienne

```
ma-carriere/
├── CLAUDE.md              # règles lues par l'agent à chaque session
├── profil.md              # qui vous êtes, source de vérité unique
├── tracker.md             # une ligne par piste — la vue d'ensemble
├── calendrier.md          # toutes les dates, ordre chronologique
├── entreprises.md         # traçabilité : postulé + en exploration
├── vision.md              # cadre de décision long terme
├── positionnement.md      # ce que le marché dit de votre profil
├── storytelling.md        # le pitch, les preuves, les angles par cible
├── candidatures/
│   └── {entreprise}/      # un dossier par candidature sérieuse
│       ├── README.md      # objectif, angle, contact, langue, brouillon
│       └── CV-{entreprise}.html
└── prive/                 # gitignored — CV réels, PDF, notes sensibles
```

**La boucle** (détaillée dans `methode/00-vue-densemble.md`) :

```
repérer → qualifier → dossier → vérifier contact → trancher la langue → rédiger → envoyer → tracer → relancer → clore
```

Chaque étape a une règle écrite. Le point non négociable : **une candidature sérieuse = un sous-dossier**, jamais un email improvisé dans une conversation.

## Ce que contient le kit

**`methode/` — la partie qui vaut le coup d'être lue**

| Fichier | Contenu |
|---|---|
| `00-vue-densemble.md` | La boucle en 10 étapes, la règle de propagation entre les 3 fichiers de suivi, les 3 disciplines de fond |
| `01-outreach-email.md` | Trancher l'objectif avant d'écrire, le plafond de 150 mots, PATTE-OUT-01 à 07, le protocole de relecture, la boucle de calibration par diff |
| `02-verification-contact.md` | Les deux questions dans l'ordre (encore en poste ? adresse réelle ?), cas de bounce, force des accroches |
| `03-langue-et-region.md` | Les 4 signaux classés par fiabilité, marchés multilingues, cohérence CV / email |
| `04-anti-patterns-carriere.md` | PATTE-CAR-01 à 07 : les garde-fous qui empêchent un agent IA de produire du coaching générique, + le cadre de vérification en 6 points |
| `05-suivi-et-relances.md` | Les 8 statuts exclusifs, la cadence de relance, l'anatomie d'une relance en 4 lignes, la lecture du délai de refus |
| `06-lecons-apprises.md` | Ce que la campagne réelle a appris et qui ne s'invente pas en amont |

**`templates/`** : `CLAUDE.md.template`, `profil.md`, `tracker.md`, `calendrier.md`, `entreprises.md`, `vision.md`, `positionnement.md`, `storytelling.md`, `candidature/{README,brief-entretien}.md`, `emails/outreach.md` (7 squelettes + checklist avant envoi), `cv/{cv-template.html,README.md}`.

## Commandes Claude Code incluses

`.claude/commands/` contient trois commandes prêtes à l'emploi :

| Commande | Effet |
|---|---|
| `/nouvelle-candidature <entreprise>` | Crée le dossier, lance la recherche contact + langue, pré-remplit le README |
| `/relances` | Balaie `calendrier.md`, liste ce qui est dû aujourd'hui et rédige les relances |
| `/carriere-status` | Synthèse : pistes actives, en attente, closes, prochaines actions |

Elles fonctionnent telles quelles une fois le dossier initialisé. Sur un autre outil que Claude Code, elles se lisent comme des procédures à suivre à la main.

## Ce que le kit ne contient pas

- **Aucune donnée personnelle** : ni contacts, ni adresses email, ni noms d'entreprises ciblées, ni chiffres de portfolio. Tout est en `{{PLACEHOLDER}}`.
- **Aucun outil payant.** Pas de CRM, pas de Mailtrack. Des fichiers markdown et un dossier git.
- **Aucune promesse de résultat.** La méthode réduit les erreurs évitables (bounce, relance oubliée, email générique). Elle ne remplace pas un bon profil.

## Licence

MIT. Forkez, adaptez, gardez ce qui sert.
