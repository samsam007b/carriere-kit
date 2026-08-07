# Vue d'ensemble — comment le système tourne

## Le principe

Trois fichiers portent tout le suivi, avec une hiérarchie stricte et pas de redondance :

| Fichier | Contient | Granularité |
|---|---|---|
| `entreprises.md` | **Tout** ce qui a été repéré, contacté ou juste exploré | Une ligne par organisation, avec le verdict |
| `tracker.md` | Les pistes **actives** uniquement | Une ligne par piste : statut, dernière action, prochaine action |
| `calendrier.md` | Les **dates** uniquement | Une ligne par échéance, ordre chronologique |

**La règle de propagation** : toute nouvelle piste entre d'abord dans `entreprises.md`. Si elle devient active, elle passe dans `tracker.md`. Dès qu'une date existe (envoi, relance, deadline portail, retour de congé d'un contact), elle apparaît dans `calendrier.md`.

Une date ne vit jamais à deux endroits comme source de vérité. `calendrier.md` fait foi ; si une date change ailleurs, on la répercute.

## La boucle, étape par étape

### 1. Repérer

Sources qui produisent réellement des pistes, par ordre de rendement observé :

- Offres publiées sur le site carrières de l'organisation (pas les agrégateurs, souvent périmés)
- LinkedIn Jobs, filtre 30 jours, requêtes par **intitulé de practice** plutôt que par titre de poste
- Le réseau : une offre partagée par un contact vaut dix offres trouvées seul
- Les organisations qui n'ont **aucune** offre ouverte mais un besoin visible (site daté, équipe qui vient de se créer, practice lancée il y a six mois) → candidature spontanée, c'est là que la concurrence est la plus faible

Un signal fort et sous-exploité : **une équipe qui recrute un profil trop senior pour vous**. Ça prouve que le budget existe et que l'équipe grandit. On ne postule pas sur ce poste, on écrit au responsable.

Tout ce qui est repéré va dans `entreprises.md`, même écarté — écrire pourquoi ça a été écarté évite de refaire la recherche trois semaines plus tard.

### 2. Qualifier

Avant d'ouvrir un dossier, trancher trois questions :

- **Le poste existe-t-il vraiment ?** Vérifier la page d'origine, pas le résumé d'un agrégateur ou d'un agent de recherche. Les offres expirées sont légion.
- **La voie est-elle l'email ou le portail ?** Beaucoup de grandes structures n'acceptent **que** le portail. Un cold email au recrutement y sera poliment renvoyé vers le formulaire. Voir `06-lecons-apprises.md`.
- **Le niveau correspond-il ?** « 2-5 ans d'expérience » sur un profil junior, ce n'est pas une piste, c'est un signal de croissance (cf. étape 1).

### 3. Ouvrir le dossier

`candidatures/{entreprise}/README.md`, à partir de `templates/candidature/README.md`. Le dossier se remplit **avant** de rédiger quoi que ce soit. Sections obligatoires : Objectif, Angle, Contact, Langue, CV, Brouillon, Prochaine étape.

Pourquoi obligatoire : un email rédigé sans objectif tranché produit un « je suis disponible pour échanger » générique. L'objectif détermine le ton, la longueur et le CTA. Voir `01-outreach-email.md` §Étape 0.

### 4. Vérifier le contact

Dans cet ordre, sans sauter d'étape — chaque saut coûte un cycle complet (bounce + recherche + relance) :

1. La personne travaille-t-elle **encore** là ? (LinkedIn, poste courant)
2. Son adresse réelle est-elle visible quelque part ? (page profil officielle, `mailto:`, article co-signé)
3. Seulement à défaut : pattern déduit, en assumant explicitement le risque de bounce dans le README

Détail complet et cas réels : `02-verification-contact.md`.

### 5. Choisir la langue

Jamais par défaut. Vérifier la langue du profil du contact, du site carrières, l'ancrage régional. Documenter la preuve dans une section `## Langue` du README. Détail : `03-langue-et-region.md`.

### 6. Rédiger

CV décliné pour la cible (`templates/cv/`), email selon `01-outreach-email.md`. Le brouillon vit dans le README du dossier, pas dans une conversation qui disparaît.

### 7. Envoyer

Une confirmation explicite avant chaque envoi externe, systématiquement. Un envoi est irréversible.

Cadence observée comme tenable : **une vague de candidatures ciblées par semaine**, pas plus. Au-delà, la qualité de personnalisation s'effondre et les relances s'empilent.

### 8. Tracer

Immédiatement après l'envoi, mettre à jour les trois fichiers :

- `tracker.md` : statut → « Email envoyé, en attente », dernière action datée avec le contact et la voie
- `calendrier.md` : la date de relance
- `entreprises.md` : la ligne de traçabilité

Écrire dans la ligne de tracker **si l'adresse était confirmée ou déduite**. Au moment de la relance, cette information décide si on relance ou si on cherche une autre adresse.

### 9. Relancer

| Situation | Délai |
|---|---|
| Silence complet | 7 jours ouvrables |
| Out of office reçu | 3 à 5 jours ouvrables **après** la date de retour, pas le jour même |
| Processus explicitement gelé | Aucune relance courte. Recontacter à la date annoncée + marge |
| Bounce | Pas de relance. Retour à l'étape 4 |

Une relance dépasse rarement quatre lignes : rappel du contexte en une phrase, un élément nouveau si possible, réitération du CTA.

### 10. Clore

Une piste morte se clôt explicitement, avec la raison. Trois catégories utiles :

- **Refusée** — noter le délai entre soumission et refus. Moins de 72h et message template = filtre automatique, l'humain n'a probablement rien lu. Plusieurs jours = examen réel, le profil a été vu.
- **Jamais délivrée** (bounce) — la piste n'a jamais été tentée, elle reste ouvrable
- **Écartée volontairement** — écrire pourquoi, c'est ce qui évite de la rouvrir par réflexe

## Les trois disciplines qui font la différence

1. **Zéro enjolivement.** Aucun chiffre arrondi dans le bon sens, aucun titre gonflé, aucun résultat extrapolé. Un chiffre faux découvert détruit la crédibilité de tout le reste. En cas de doute, vérifier ou omettre.
2. **Le contexte vit dans les fichiers, pas dans la conversation.** Une session d'agent IA se termine ; le dossier reste. Tout ce qui compte est écrit.
3. **Écrire les échecs.** Le fichier `06-lecons-apprises.md` de ce kit vient entièrement de bounces, de refus ATS et de portails cassés. C'est la partie la plus utile du système.
