# Suivi, statuts et relances

## Le vocabulaire de statut

Un statut flou rend une ligne de tracker inutilisable trois semaines plus tard. Huit statuts suffisent, et ils sont exclusifs :

| Statut | Signification | Action par défaut |
|---|---|---|
| **En exploration** | Repéré, pas encore qualifié | Qualifier ou écarter |
| **Dossier ouvert** | Dossier créé, rien d'envoyé | Finaliser contact + langue + brouillon |
| **Envoyé, en attente** | Parti, pas de retour | Relance à J+7 ouvrables |
| **Out of office** | Absence automatique reçue | Relance à J+3-5 ouvrables **après** la date de retour |
| **Bounce** | Jamais délivré | Retour à la vérification contact. **La piste n'a jamais été tentée** |
| **En cours** | Réponse humaine reçue, processus vivant | Suivre le rythme imposé par eux |
| **Gelé** | Processus suspendu de leur côté, dossier conservé | Aucune relance courte. Date de reprise + marge |
| **Clos** | Refusé, écarté, ou poste disparu | Écrire la raison, ne rien réactiver par réflexe |

La distinction **Bounce** vs **Envoyé** est celle qui se perd le plus vite et qui coûte le plus cher : un bounce n'est pas un silence, c'est une piste intacte qu'on croit morte.

## Cadence de relance

| Situation | Délai | Registre |
|---|---|---|
| Silence complet | 7 jours ouvrables | Quatre lignes maximum |
| Deuxième silence | 10 à 14 jours après la première relance, puis stop | Encore plus court, ou changement de contact |
| Out of office | 3 à 5 jours ouvrables après le retour | Ne jamais le jour même du retour : la boîte est saturée |
| Processus gelé annoncé | À la date annoncée + 2 semaines | Viser la personne rencontrée, pas la boîte générique |
| Après un entretien | 5 jours ouvrables si aucun délai n'a été annoncé | Remerciement + un élément de fond, jamais une simple relance |
| Refus | Aucune relance | Éventuellement une demande de feedback, une fois, sans insistance |

Deux relances sans réponse valent une réponse. Passer à autre chose ou changer de porte d'entrée.

## Anatomie d'une relance

Quatre lignes, pas plus :

1. Rappel du contexte en une phrase, avec la date de l'envoi initial
2. Un élément **nouveau** si possible : une avancée de votre côté, une actualité de leur côté. Sans élément nouveau, la relance n'est qu'une répétition
3. Réitération du CTA, plus courte que la première fois
4. Formule + signature

Ce qu'on ne fait jamais : reprocher le silence, réexpliquer tout le profil, ajouter une deuxième pièce jointe, changer d'argument en cours de route.

## Lire un refus

Le délai en dit plus que le texte.

| Délai entre soumission et refus | Lecture |
|---|---|
| Moins de 72h, message template | Filtre automatique. Un humain n'a probablement rien lu. Le profil n'a pas été évalué |
| Plusieurs jours à deux semaines, message template | Examen humain rapide, tri de volume |
| Deux semaines et plus, ou message avec un élément spécifique | Examen réel. Le profil a été vu, il n'a pas été retenu |

Cette distinction change la suite. Un rejet ATS en 48h ne dit rien sur le profil : il dit que la voie du portail, seule, ne fonctionne pas pour ce profil sur cette organisation. La réponse n'est pas de réécrire le CV, c'est de trouver un chemin interne. Un refus après examen réel, lui, mérite une révision du positionnement.

Noter le délai dans la ligne de tracker. C'est une donnée, pas une anecdote.

## Ce qu'on écrit dans une ligne de tracker

Une ligne utile contient cinq choses, et tient sur une ligne :

```
| Organisation | Type | Statut + date | Dernière action : quoi, à qui, par quelle voie,
adresse confirmée ou déduite, où est le dossier | Prochaine action + date |
```

Les erreurs qui rendent une ligne inutile :

- « En attente » sans date → impossible de savoir si la relance est due
- « Envoyé à [Nom] » sans l'adresse ni son statut → impossible d'interpréter un silence
- « Relancer » sans date → ne sera jamais fait
- Un statut positif sur une piste morte, gardé par optimisme → fausse la vue d'ensemble

## Le passage en revue hebdomadaire

Vingt minutes, une fois par semaine, dans cet ordre :

1. Ouvrir `calendrier.md`, traiter tout ce qui est échu
2. Balayer `tracker.md` : chaque ligne « En attente » de plus de 10 jours passe en relance ou en clos
3. Vérifier les bounces éventuels dans la boîte d'envoi
4. Ajouter les nouvelles pistes repérées dans `entreprises.md`
5. Décider de la vague de la semaine : trois à cinq candidatures ciblées, pas quinze

C'est la seule routine du système. Sans elle, les trois fichiers divergent en deux semaines et le dossier devient un cimetière.
