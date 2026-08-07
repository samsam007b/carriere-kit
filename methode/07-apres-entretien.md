# Après l'entretien

La méthode s'arrêtait à la porte de l'entretien. Ce qui suit couvre le reste : les 24h qui suivent, l'attente, l'offre, la négociation, le refus, le désistement.

> Avertissement de portée : cette partie touche à des règles de droit du travail et à des usages de rémunération qui changent d'un pays à l'autre. Rien ici n'est un conseil juridique. Tout montant, tout délai légal, tout barème doit être vérifié auprès d'une source officielle du pays concerné avant d'être utilisé dans une négociation.

---

## 1. Les 24 heures qui suivent

Deux actions, dans cet ordre.

**Écrire le compte rendu pendant que c'est frais**, dans le README du dossier. Ce qui se perd en 48h et ne se reconstitue jamais :

```markdown
### Entretien du {{date}} avec {{Prénom Nom}}, {{titre}}

**Format** : {{visio / sur place / téléphone}}, {{durée réelle}}
**Prochaine étape annoncée par eux** : {{formulation exacte}}, d'ici {{délai annoncé}}

**Questions posées qui ont surpris** :
- {{question}} → ce que j'ai répondu / ce que j'aurais dû répondre

**Ce qu'ils ont dit sur le poste que l'annonce ne disait pas** :
- {{point}}

**Signaux sur l'équipe et le contexte** : {{turnover, réorganisation, budget, urgence}}
**Mon niveau d'envie après l'échange** : {{monté / descendu / stable}}, et pourquoi
```

La dernière ligne compte autant que les autres. Une envie qui descend après un entretien est une donnée, pas une faiblesse à corriger.

**Envoyer l'email de suivi** dans les 24h, modèle 6 de `templates/emails/outreach.md`. Il porte du fond, pas un remerciement seul : une réponse plus complète à une question posée, ou un point précis discuté. Sans fond, il vaut mieux ne pas l'envoyer.

---

## 2. L'attente

Le délai annoncé par eux fait foi. Il va dans `calendrier.md`, avec **trois jours ouvrables de marge** avant toute relance.

| Situation | Ce qu'on fait |
|---|---|
| Délai annoncé dépassé de moins de 3 jours ouvrables | Rien. Les processus glissent, relancer trop tôt se voit |
| Délai dépassé de plus de 3 jours ouvrables | Relance de quatre lignes, sans reproche, en rappelant le délai qu'**ils** ont annoncé |
| Aucun délai annoncé | Relance à 10 jours ouvrables |
| Une autre offre arrive avec une échéance | Le dire, factuellement, avec la date. Ce n'est pas un ultimatum, c'est une contrainte de calendrier réelle. Ne jamais inventer une offre concurrente |
| Deuxième relance sans réponse | Clore la piste dans `tracker.md`. Ne pas en envoyer une troisième |

---

## 3. L'offre arrive

**Ne rien accepter dans l'appel.** Remercier, se montrer positif, demander l'offre par écrit et un délai de réflexion. Un délai de quelques jours ouvrables est une demande normale ; un employeur qui le refuse vient de donner une information sur lui.

Ce qui se vérifie sur le document écrit, avant toute discussion de montant :

- Intitulé exact, rattachement hiérarchique, lieu, présentiel ou télétravail et sa formalisation
- Type de contrat, durée, période d'essai et ses conditions de rupture
- Rémunération : fixe, variable et **la condition exacte qui déclenche le variable**, avantages chiffrés
- Date de début, congés, préavis
- Toute clause qui vous engage au-delà du contrat : non-concurrence, propriété intellectuelle, exclusivité. Les lire ligne à ligne. Elles pèsent surtout sur les profils qui ont des projets à côté

Comparer les éléments à des données de marché **localisées** : même pays, même secteur, même niveau d'expérience. Une grille salariale importée d'un autre marché ne vaut rien (voir PATTE-CAR-05).

---

## 4. Négocier

Trois principes, et rien d'autre.

**Un seul cycle de négociation.** Rassembler toutes les demandes en une fois. Négocier point par point sur plusieurs échanges use la bonne volonté et fait passer pour indécis.

**Justifier par le marché ou par le périmètre, jamais par le besoin personnel.** « Le poste inclut {{responsabilité}}, qui n'était pas dans l'annonce » est un argument. « J'ai un loyer à payer » n'en est pas un.

**Ne demander que ce qu'on accepterait de recevoir.** Toute demande obtenue engage à signer. Demander pour tester, puis refuser quand même, brûle le contact et le réseau derrière lui.

Le montant n'est pas la seule variable. Souvent plus faciles à obtenir : date de début, jours de télétravail, budget de formation, révision salariale programmée à date fixe, intitulé du poste.

---

## 5. Refuser une offre, ou se désister

Ça arrive plus souvent qu'on ne l'imagine, et c'est le moment qui construit ou détruit une relation à long terme. Trois règles :

- **Vite.** Dès la décision prise. Chaque jour de retard bloque un processus et un autre candidat
- **Par le même canal, avec la même personne.** Pas de disparition, pas de délégation à un formulaire
- **Sans fausse raison.** « J'ai accepté un autre poste » ou « le périmètre ne correspond pas à ce que je cherche » suffisent. Inventer une raison crée une histoire qu'il faudra tenir si le contact réapparaît dans deux ans

Le secteur est plus petit que le nombre d'offres ne le laisse croire. La personne à qui vous dites non aujourd'hui peut être celle qui recrute là où vous voudrez aller ensuite.

---

## 6. Clore la ligne dans le suivi

Quelle que soit l'issue, la piste se ferme proprement :

- `tracker.md` : statut final, date, et **une ligne sur ce qu'on en retient**
- `calendrier.md` : supprimer les échéances devenues sans objet
- `entreprises.md` : garder l'organisation avec son historique. Un refus n'est pas une porte fermée, c'est une porte datée
- `methode/06-lecons-apprises.md` : si l'issue a appris quelque chose de transposable, l'y écrire. C'est le seul fichier qui grossit avec l'expérience
