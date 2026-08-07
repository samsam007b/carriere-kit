---
description: Ouvre un dossier de candidature complet pour une organisation (recherche contact, langue, angle, brouillon)
---

Ouvrir un dossier de candidature pour : **$ARGUMENTS**

Si aucun argument n'est fourni, demander le nom de l'organisation avant de continuer.

## Procédure

### 1. Contexte

Lire `profil.md`, `storytelling.md` et `CLAUDE.md`. Ne jamais inventer un chiffre : tout ce qui est cité doit figurer dans `profil.md`.

Vérifier dans `entreprises.md` si cette organisation a déjà été explorée ou écartée. Si elle a été écartée, le signaler et demander confirmation avant de rouvrir.

### 2. Qualifier

Vérifier **à la source primaire**, pas via un résumé :

- Le poste ou le besoin existe-t-il encore ? Ouvrir la page d'origine
- La voie est-elle l'email ou le portail obligatoire ?
- Le niveau correspond-il ? Un poste trop senior n'est pas une piste, c'est un signal que l'équipe grandit

Si la piste ne passe pas la qualification : l'écrire dans `entreprises.md` avec la raison et s'arrêter là.

### 3. Contact

Appliquer `methode/02-verification-contact.md` **dans l'ordre** :

1. La personne travaille-t-elle encore là ? Vérifier LinkedIn en premier
2. Son adresse est-elle visible directement ? Chercher un `mailto:` sur sa page profil officielle, un article co-signé, une page équipe
3. À défaut seulement : pattern déduit, en marquant explicitement l'adresse comme NON CONFIRMÉE

Identifier aussi un contact de backup et une **accroche concrète** : un fait précis qui justifie d'écrire à cette personne. Pas un compliment.

### 4. Langue

Appliquer `methode/03-langue-et-region.md`. Documenter les preuves, pas seulement la conclusion.

### 5. Créer le dossier

`candidatures/{nom-en-minuscules-avec-tirets}/README.md`, à partir de `templates/candidature/README.md`. Remplir toutes les sections : Statut, Objectif, Angle, Contact, Langue, CV, Brouillon, Historique, Prochaine étape.

### 6. Brouillon email

Appliquer `methode/01-outreach-email.md` :

- Trancher l'objectif avant d'écrire (Étape 0)
- Maximum 150 mots
- Relire contre PATTE-OUT-01 à 07, en insistant sur les tics de texte généré
- **Zéro tiret cadratin**

### 7. Propager

- `entreprises.md` : la ligne de traçabilité
- `tracker.md` : la piste en statut « Dossier ouvert »
- `calendrier.md` : rien tant que rien n'est envoyé

### 8. Rendre compte

Un résumé court : ce qui a été trouvé, le contact retenu et le statut de son adresse (confirmée ou déduite), la langue et pourquoi, l'angle, et ce qui reste à valider.

**Ne rien envoyer.** L'envoi exige une confirmation explicite dans le tour où il a lieu.
