# Vérifier un contact avant d'envoyer

> Un email qui bounce coûte un cycle complet : l'attente, la recherche corrective, le renvoi. Sur une campagne de 25 candidatures, les bounces ont été la première cause de pistes perdues, devant les refus. Toutes évitables.

## L'ordre des vérifications

Deux questions distinctes, dans cet ordre. Inverser les deux fait perdre du temps sur des adresses qui ne pouvaient pas fonctionner.

### 1. Cette personne travaille-t-elle encore là ?

Avant même de chercher son adresse. Ouvrir son profil LinkedIn, vérifier :

- L'intitulé de poste courant et l'absence de date de fin
- Les publications récentes : quelqu'un qui vient de partir l'annonce souvent
- La cohérence entre le poste affiché et l'accroche prévue

**Cas réel** : un contact identifié via la page « équipe » officielle de l'entreprise. Premier envoi sur `initiale.nom@` → bounce. Recherche du pattern dominant via trois agrégateurs (94 % de concordance sur `prenom.nom@`) → renvoi → bounce à nouveau. Vérification LinkedIn : la personne avait quitté l'entreprise après dix ans et travaillait ailleurs. Les deux adresses ne pouvaient jamais fonctionner ; le pattern n'avait jamais été le problème. Deux cycles perdus pour une vérification de trente secondes.

Les agrégateurs (RocketReach, LeadIQ, Clay, SignalHire) confirment des **patterns de domaine historiques**, pas un statut d'emploi en temps réel. Leurs données peuvent avoir plusieurs mois de retard. LinkedIn est la source la plus fraîche sur « est-ce que cette personne est encore la bonne cible ».

Si LinkedIn indique un départ ou un poste incohérent : ne pas envoyer. Chercher le remplaçant ou abandonner la piste.

### 2. Quelle est son adresse réelle ?

Chercher une **source directe** avant tout pattern déduit :

1. Page profil publique sur le site de l'entreprise (« meet the team », « our people », bio de practice) — contient souvent un `mailto:`
2. Article, publication ou communiqué co-signé avec adresse de contact visible
3. Signature d'email dans un échange public, PDF, présentation
4. Adresse générique de service (`careers@`, `rh@`) confirmée par un `mailto:` sur la page emploi — souvent négligée, mais elle a l'avantage d'être **certaine**
5. À défaut seulement : pattern déduit, en assumant explicitement le risque

**Cas réel** : sur un grand cabinet, le pattern déduit `prenom.nom@` a bouncé. La vraie adresse, `initialenom@` sans point, était visible dans un `mailto:` sur la page profil officielle du contact, sur le site de l'entreprise. Trouvable en deux minutes, pas cherchée avant le premier envoi. Les grandes structures ont fréquemment plusieurs formats qui coexistent selon l'ancienneté.

**Cas réel** : sur une très grande entreprise tech, `prenom.nom@` a bouncé aussi. Certaines organisations utilisent des identifiants non déterministes qu'aucun pattern ne peut deviner. Sur celles-là, ne pas insister : passer par LinkedIn en direct ou par le portail.

## Ce qu'on écrit dans le dossier

Section `## Contact` du README de la candidature :

```markdown
## Contact

**Retenu** : [Prénom Nom] — [Titre exact]

**Vérification LinkedIn** ([date]) : profil `linkedin.com/in/...`, titre confirmé,
poste courant. [Relations en commun s'il y en a / contact froid.]

**Adresse** : `xxx@domaine.com`
Source : mailto trouvé sur [URL] — CONFIRMÉE
   (ou : pattern déduit, corroboré par [n] agrégateurs — NON CONFIRMÉE, risque de bounce assumé)

**Backup si silence** : [Prénom Nom], [Titre] — [pourquoi lui/elle en second]

**Accroche concrète trouvée** : [le fait précis qui justifie d'écrire à cette
personne plutôt qu'à une autre]
```

Le statut confirmée / non confirmée est ce qui, au moment de la relance, décide si on relance ou si on cherche une autre adresse. Sans lui, un silence de sept jours est ininterprétable.

## Trouver l'accroche

Un contact vérifié ne suffit pas : il faut une raison d'écrire à **cette** personne. Par ordre de force :

| Accroche | Force | Où la trouver |
|---|---|---|
| Une offre publiée par le contact lui-même, même trop senior | Très forte — prouve que l'équipe grandit | Activité LinkedIn du contact |
| Une prise de position publique récente sur un sujet où vous avez une pratique | Forte | Posts, articles, interviews |
| Un projet, une offre ou une practice lancée récemment | Forte | Site, communiqués |
| Une relation en commun | Forte, mais à ne pas verbaliser (cf. PATTE-OUT-07) | LinkedIn |
| Une observation factuelle sur leur communication | Moyenne — n'est jamais formulée comme une critique | Leur site, leurs réseaux |
| « J'admire votre travail » | Nulle | — |

Une accroche vraie et vérifiable vaut mieux qu'une accroche flatteuse. Si aucune n'existe, la candidature est probablement mal ciblée.

## Le contact chaud

Une piste portée par quelqu'un à l'intérieur ne suit pas ce protocole : pas de cold email, pas de vérification d'adresse. On prépare le dossier et on le fait remonter par le contact. Le taux de réponse est sans commune mesure.

C'est aussi le seul chemin qui fonctionne sur les grandes structures à ATS strict : le portail traite la candidature, le contact interne la fait exister. Voir `06-lecons-apprises.md`.
