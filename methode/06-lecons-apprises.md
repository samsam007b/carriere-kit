# Leçons apprises

> Retours de terrain d'une campagne réelle : plus de 25 organisations contactées en trois mois (fédérations sectorielles, cabinets de conseil, institutions européennes, entreprises tech, ESN). Toutes les organisations sont anonymisées. Ce qui compte ici, ce sont les mécanismes, pas les noms.

## Sur les canaux

### Le portail seul ne suffit pas sur les grandes structures

Deux candidatures déposées sur des portails de très grands groupes ont été refusées par message template, l'une en 48h, l'autre en 15h. Dans les deux cas, aucun retour spécifique, aucun signe d'examen humain.

En parallèle, un cold email au responsable du recrutement campus de l'un de ces groupes a reçu une réponse courtoise mais fermée : « toutes les candidatures doivent passer par le portail », sans aucune ouverture à un traitement hors canal.

**Le mécanisme** : sur ces structures, le portail est obligatoire **et** insuffisant. La candidature doit exister dans le système, mais c'est un contact interne qui la fait remonter. Postuler sans relais interne, c'est nourrir un filtre.

**La conséquence pratique** : avant de postuler à un grand groupe, chercher un alumni de son école, une relation de deuxième degré, n'importe qui à l'intérieur. Si personne, ajuster ses attentes en conséquence plutôt que de conclure quoi que ce soit sur son profil à partir du refus.

### La candidature spontanée bien ciblée bat l'offre ouverte

Les réponses humaines réelles obtenues dans cette campagne sont venues de candidatures **spontanées** vers un contact nommé, pas de réponses à des offres publiées. Sur une offre publiée, on est un dossier parmi deux cents. Sur une candidature spontanée bien accrochée, on est le seul.

Corollaire contre-intuitif : les organisations **sans** poste ouvert sont souvent les meilleures cibles, à condition d'avoir une accroche réelle (équipe qui vient de se créer, practice lancée récemment, besoin visible).

### Un appel peut rediriger vers un autre poste

Une candidature sur un poste trop senior a débouché sur un appel où l'interlocuteur a lui-même redirigé vers un poste junior dans une autre équipe, avec passage de relais nommé en interne. Postuler légèrement au-dessus de son niveau, avec un dossier sérieux, produit parfois cette redirection. Postuler très au-dessus produit du silence.

## Sur les offres

### Vérifier que l'offre existe encore, à la source

Une offre repérée par un agent de recherche s'est révélée expirée à la vérification directe. Une autre a été dépubliée entre la création du brouillon de candidature et la tentative de soumission : trois tentatives d'envoi ont échoué sur une erreur serveur opaque, dont la cause réelle n'est apparue qu'en rouvrant la candidature depuis le compte candidat (« cette offre n'est plus publiée »).

**Leçon** : quand un portail renvoie une erreur technique inexplicable, vérifier d'abord que l'offre est encore en ligne, avant de soupçonner un champ mal rempli.

### Les fiches de poste peuvent être vides côté serveur

Sur un portail carrières, dix-neuf postes affichés mais les descriptions renvoyaient un contenu vide via l'API sous-jacente. Impossible de qualifier quoi que ce soit. Recoupement externe nécessaire, ou abandon.

### Les agents de recherche inventent des détails plausibles

Une recherche déléguée a produit des deadlines, des volumes de recrutement et des liens qui ne se vérifiaient pas à la source. Tout ce qui est repris d'une recherche automatisée dans un dossier de candidature doit être **revérifié à la source primaire** avant d'être cité dans un email. Un fait faux cité à un recruteur qui connaît sa maison est plus coûteux qu'un email plus court.

## Sur les contacts

### Trois causes de bounce, dans l'ordre de fréquence

1. **La personne a quitté l'entreprise.** Le pattern d'adresse était bon, la boîte n'existe plus. Vérification LinkedIn, trente secondes.
2. **Le format d'adresse n'est pas celui du domaine.** Les grandes structures ont plusieurs formats coexistants. La vraie adresse est souvent dans un `mailto:` sur la page profil publique.
3. **L'organisation utilise des identifiants non déterministes.** Aucun pattern ne fonctionne. Passer par LinkedIn ou le portail.

### Les agrégateurs donnent des probabilités, pas des confirmations

Trois agrégateurs concordant à 94 % sur un pattern n'ont pas empêché deux bounces successifs : le problème n'était pas le format mais le statut d'emploi. Un agrégateur confirme un historique de domaine, pas une boîte mail active.

### Les adresses génériques sont sous-estimées

Une adresse `rh@` ou `careers@` confirmée par un `mailto:` sur la page emploi a le mérite d'être **certaine**. Sur une petite structure ou une association, c'est souvent le meilleur point d'entrée, et le message atterrit chez la bonne personne.

## Sur le calendrier

### L'été est un piège documenté

Sur une vague de candidatures mi-juillet, plus d'un tiers ont produit une réponse automatique d'absence, avec des dates de retour s'étalant sur trois semaines. Chacune impose de reporter la relance et de la caler 3 à 5 jours ouvrables après le retour, pour ne pas se noyer dans le rattrapage d'inbox.

**Ce n'est pas une raison de ne pas envoyer** : l'out of office donne une date de retour précise et un contact de backup, ce qui est plus d'information qu'un silence. Mais il faut l'anticiper dans le calendrier plutôt que le subir.

### Les cycles graduate rouvrent en fin d'été

Un balayage de postes juniors mené en plein été peut revenir totalement vide sans que ça signifie quoi que ce soit sur le marché. Repasser le scan trois à quatre semaines plus tard.

## Sur les fichiers

### Les décisions d'écartement doivent être écrites

Plusieurs pistes ont été explorées deux fois faute d'avoir noté pourquoi elles avaient été écartées la première fois. Une ligne « écarté volontairement, raison : X » dans `entreprises.md` économise une demi-journée de recherche.

### Un README de candidature vaut plus qu'un CV

Au moment d'un entretien deux mois après l'envoi, c'est le README qui permet de retrouver l'angle exact, l'accroche utilisée, ce qui avait été promis. Le CV, lui, se régénère.

---

## Ajouter vos propres leçons

Ce fichier est fait pour grossir. Après chaque bounce, chaque refus, chaque erreur de portail, ajouter une entrée : **le mécanisme observé, pas l'anecdote**. La question à se poser est « qu'est-ce que je ferais différemment la prochaine fois, et à quel moment exact du processus ».
