# Email d'outreach — méthode et anti-patterns

> Ce fichier est né d'une pratique précise : comparer systématiquement le brouillon produit par un assistant IA et l'email **réellement envoyé** après correction manuelle. Les écarts se répètent. Ils sont listés ici comme anti-patterns nommés, pour que le brouillon suivant parte déjà de la bonne forme.

## Étape 0 — Trancher l'objectif avant d'écrire une ligne

Non négociable. Un email rédigé sans objectif tranché produit une clôture molle du type « je suis disponible pour échanger », qui est le premier signal d'un texte non pensé.

| Objectif | Registre | CTA type | Longueur |
|---|---|---|---|
| **Stage / traineeship** | Motivé, jamais suppliant, disponibilité à une date précise | « Disponible à partir de [date]. Je me tiens à disposition pour un échange. » | ~120-150 mots |
| **Poste ouvert précis** | Direct sur le fit poste ↔ profil, pas de storytelling long | « Seriez-vous disponible pour échanger autour de ce sujet ! » | Court à moyen |
| **Candidature spontanée** | Constat factuel → valeur ajoutée concrète, jamais présomptueux | Proposition d'échange ouverte, jamais de demande d'embauche directe | Court |
| **Mission consultant / freelance** | Proposition de valeur dès la deuxième phrase, diplôme et CV en retrait | Proposition de call ouverte, aucune promesse de démo non demandée | ~100 mots |
| **Prise de contact réseau** | Curiosité réelle, référence vérifiable | Question ouverte, pas de CTA commercial | Très court |

Si l'objectif n'est pas déjà écrit dans le README du dossier, le trancher là d'abord.

## Le plafond : 150 mots

Un email de candidature au-delà de 150 mots ne se lit pas en entier. La contrainte force à choisir un seul argument, et c'est exactement ce qu'il faut.

Structure qui tient dans le budget :

1. Salutation nommée
2. Une phrase : qui vous êtes, avec la preuve la plus coûteuse à falsifier
3. Une ou deux phrases : le lien concret avec **eux** (un projet, une annonce, une pratique identifiée), pas un compliment
4. « CV en pièce jointe. »
5. CTA ouvert, une ligne
6. Formule + signature

## Les six anti-patterns

### PATTE-OUT-01 — Email sans salutation nommée

**Pattern** : commencer directement par l'argumentaire.

**Pourquoi** : un mail sans salutation se lit comme un extrait de lettre de motivation recyclé, pas comme un message adressé à une personne.

**Contre-exemple** : toujours « Bonjour [Prénom], » par défaut sur un cold outreach. « Monsieur / Madame [Nom], » si le contact a un rang senior ou si le registre de l'organisation est formel.

### PATTE-OUT-02 — Surenchère en fin de phrase

**Pattern** : ajouter une clause après un point déjà fait (« ...sans être développeur de formation, **en pilotant l'IA pour exécuter vite** »), ou un adjectif d'emphase (« l'intersection **exacte** de vos deux mandats »).

**Pourquoi** : la couche supplémentaire dilue au lieu de renforcer. Dans les diffs observés, c'est la correction manuelle la plus fréquente.

**Contre-exemple** : relire chaque phrase et demander « est-ce que la seconde moitié ajoute une information, ou juste de l'emphase ? ». Si emphase seule, couper.

### PATTE-OUT-03 — Article indéfini sur un poste identifié

**Pattern** : écrire « **un** traineeship chez X » alors que le poste visé est précisément identifié.

**Pourquoi** : « un » signale un envoi de masse ; « le » signale que la recherche a été faite. Signal de sérieux à coût nul.

**Contre-exemple** : dès qu'un rôle nommé apparaît dans le README du dossier, article défini dans l'email.

### PATTE-OUT-04 — Pièce jointe non mentionnée

**Pattern** : joindre le CV sans jamais l'évoquer dans le corps.

**Pourquoi** : lève l'ambiguïté et donne un point d'ancrage juste avant la clôture.

**Contre-exemple** : une phrase courte, « CV en pièce jointe. », avant le CTA.

### PATTE-OUT-05 — CTA absent, ou trop commercial

**Pattern, partie 1** : terminer sur l'argumentaire sans invitation explicite, ou omettre formule et signature.

**Pattern, partie 2** : un CTA qui chiffre une durée (« un échange de 20 minutes ») ou promet une démo non sollicitée (« je peux vous montrer concrètement ce que ça donnerait »).

**Pourquoi** : sans CTA, la balle reste dans le camp du lecteur sans action facile. Avec un CTA chiffré, ça bascule en prospection commerciale. Cas source réel : la version « échange de 20 minutes + je peux montrer concrètement » avait été proposée comme bonne pratique après un premier diff, puis **retirée manuellement** au diff suivant. La table des cas réels prime toujours sur la règle générique.

**Contre-exemple** : invitation ouverte, sans chiffre et sans livrable promis, puis formule + signature. Terminer par « ! » plutôt que « ? » adoucit le registre sans le rendre familier.

### PATTE-OUT-06 — Tics lexicaux et structurels reconnaissables d'un texte généré

**Pattern** : les marqueurs qui reviennent de façon disproportionnée dans le texte de LLM. À vérifier avant chaque envoi :

- **Ponctuation** : tiret cadratin et tiret moyen (—, –) utilisés comme liaison. C'est le marqueur numéro un. Remplacer par virgule, point, deux-points ou parenthèses. Le tiret court d'un mot composé reste normal. Point-virgule utilisé comme liaison stylistique plutôt que grammaticale, même problème.
- **Vocabulaire « boost »** : levier, exploiter le potentiel, façonner, accélérer en série, transformer employé comme mot creux, déployer hors contexte technique.
- **Ouvertures formulaïques** : « Je me permets de vous contacter », « J'espère que ce mail vous trouve bien », « Dans le monde actuel de... ».
- **Emphase vide** : vraiment, clairement, « à la fois... et », triplets rhétoriques (« rapide, efficace et pertinent »).
- **Contraste artificiel** : « je ne me contente pas de X, je Y », « pas seulement X, mais Y ». Figure de renforcement qui sonne creuse. Remplacer par le constat factuel brut.
- **Clôtures génériques** : « N'hésitez pas à me contacter », « Je reste à votre entière disposition ».
- **Symétrie trop parfaite** : trois paragraphes de longueur quasi identique, structurés pareil (constat → lien → bénéfice). Un humain varie.

**Pourquoi** : un email de candidature qui sonne généré nuit d'autant plus que le profil revendique une maîtrise réelle de ces outils.

**Contre-exemple** : préférer une syntaxe légèrement irrégulière. Longueur de phrase variable, une observation factuelle posée sans connecteur logique explicite. Relire phrase par phrase en cherchant spécifiquement cette liste.

### PATTE-OUT-07 — Souligner un point commun évident

**Pattern** : énoncer explicitement le lien (« la même école que vous », « nous partageons ce parcours »).

**Pourquoi** : mentionner le fait suffit, le destinataire fait le lien lui-même. Le souligner infantilise le lecteur et sonne comme une technique de vente.

**Contre-exemple** : laisser le fait parler. Pas de « comme vous », pas de « nous partageons ».

## Le protocole de relecture

Dans cet ordre, à chaque brouillon :

1. Objectif tranché (Étape 0) — sinon ne pas écrire
2. Rédiger
3. Compter les mots. Plus de 150 → couper, pas reformuler
4. Relire contre PATTE-OUT-01 à 07, en insistant sur 06
5. Vérifier chaque chiffre cité contre `profil.md`. Aucun chiffre non vérifié ne part
6. Confirmation explicite avant envoi
7. **Après envoi**, si le texte a été corrigé à la main : noter le diff dans le README du dossier. C'est ce qui fait progresser la calibration

## Tenir sa propre table de diffs

La partie la plus rentable de cette méthode : après chaque envoi, comparer le brouillon et l'email réellement parti (dans les *Envoyés*, pas le brouillon, qui a pu changer avant l'envoi), et consigner les écarts.

| Brouillon | Envoyé | Pattern déduit |
|---|---|---|
| _(exemple)_ « l'intersection **exacte** de vos deux mandats » | « l'intersection de vos deux mandats » | Retirer les adjectifs d'emphase |
| | | |

Cinq ou six lignes suffisent à faire converger les brouillons suivants.
