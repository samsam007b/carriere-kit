---
description: Balaie le calendrier, liste ce qui est dû aujourd'hui et prépare les relances
---

Passage en revue des relances dues.

## Procédure

### 1. Échéances

Lire `calendrier.md`. Lister tout ce qui est **échu ou dû dans les trois jours**, en séparant :

- Bloquant (deadline de portail, échéance administrative non rattrapable)
- Relances dues
- À surveiller

### 2. Cohérence du tracker

Lire `tracker.md`. Signaler :

- Toute ligne « Envoyé, en attente » de plus de 10 jours ouvrables sans date de relance
- Toute ligne sans prochaine action datée
- Toute ligne dont le statut ne correspond plus au dernier événement de son dossier
- Tout écart entre une date du tracker et `calendrier.md` (le calendrier fait foi)

### 3. Vérifier avant de relancer

Pour chaque relance due, ouvrir le README du dossier et vérifier :

- L'adresse était-elle **confirmée** ou **déduite** ? Si déduite et silence total, envisager que l'email n'ait jamais été délivré : chercher une adresse réelle plutôt que relancer dans le vide
- Un out of office avait-il été reçu ? Si oui, la relance se cale 3 à 5 jours ouvrables **après** la date de retour, jamais le jour même
- Le processus a-t-il été annoncé comme gelé ? Si oui, pas de relance courte, elle serait contre-productive
- Une deuxième relance sans réponse a-t-elle déjà été envoyée ? Si oui, proposer de clore ou de changer de porte d'entrée plutôt que d'insister

### 4. Rédiger

Pour chaque relance retenue, produire un brouillon selon `templates/emails/outreach.md` §4 ou §5 :

- Quatre lignes maximum
- Un élément nouveau si possible. Sans élément nouveau, c'est une répétition : le dire plutôt que de meubler
- Jamais de reproche sur le silence, jamais de nouvelle pièce jointe, jamais de changement d'argument

### 5. Rendre compte

Un tableau : piste, ce qui est dû, action proposée. Puis les brouillons.

**Ne rien envoyer.** Chaque envoi exige une confirmation explicite dans le tour où il a lieu.
