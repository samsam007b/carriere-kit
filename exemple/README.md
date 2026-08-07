# Exemple rempli

Ce dossier montre le système en marche sur **une** piste, du repérage à la clôture. Il répond à la question que les templates vides ne répondent pas : à quel niveau de détail faut-il écrire ?

> **Tout est fictif.** L'organisation « Norvent », les personnes et les faits n'existent pas. Les chiffres du candidat fictif sont marqués comme tels. Aucun élément de ce dossier ne doit être copié dans une vraie candidature.

- [`candidature-norvent.md`](candidature-norvent.md) : le dossier de candidature complet, tel qu'il ressemble après trois semaines de processus

Ci-dessous, les trois fichiers de suivi tels qu'ils portent cette piste au même moment.

---

## Extrait de `entreprises.md`

La piste apparaît d'abord ici, avant même qu'un dossier existe.

```markdown
### Fédérations professionnelles

| Organisation | Repérée le | Statut | Note |
|---|---|---|---|
| Norvent | 12/03 | Candidature ouverte | Pas d'offre publiée. Contact identifié via la page équipe. Recrutement probable : deux départs annoncés en janvier |
| {{Autre fédération}} | 12/03 | Écartée | Aucun poste comms, structure de 4 personnes, pas de budget visible |
| {{Autre fédération}} | 12/03 | À creuser | Offre junior publiée mais fermée depuis. Regarder à la rentrée |
```

La deuxième ligne compte autant que la première : écrire pourquoi une piste a été écartée évite de refaire la recherche trois semaines plus tard.

---

## Extrait de `tracker.md`

```markdown
| Piste | Statut | Contact | Adresse | Dernière action | Prochaine action |
|---|---|---|---|---|---|
| Norvent | Entretien passé | {{Prénom Nom}}, Responsable comms | CONFIRMÉE (mailto page équipe) | Entretien 02/04, email de suivi envoyé le 03/04 | Relance le 21/04 si silence (délai annoncé par eux : 16/04, + 3 jours ouvrables) |
```

Une ligne, six colonnes, aucune ambiguïté sur ce qui vient ensuite. Le statut de l'adresse reste visible même après une réponse : c'est ce qui permet, plus tard, de distinguer un silence d'un email jamais délivré.

---

## Extrait de `calendrier.md`

```markdown
## Avril

| Date | Piste | Échéance |
|---|---|---|
| 03/04 | Norvent | Email de suivi post-entretien (fait) |
| 16/04 | Norvent | Fin du délai annoncé par eux |
| 21/04 | Norvent | Relance si toujours pas de réponse (délai + 3 jours ouvrables de marge) |
| 22/04 | {{Autre piste}} | Deadline de dépôt sur portail, non rattrapable |
```

Le calendrier fait foi en cas de divergence avec le tracker. Une seule source de vérité par date.

---

## Ce que l'exemple illustre

| Point | Où le voir |
|---|---|
| Une accroche qui ne fonctionnerait chez personne d'autre | Section « Angle » du dossier |
| Un contact vérifié dans le bon ordre, avec la preuve écrite | Section « Contact » |
| Une langue tranchée sur des signaux, pas sur une supposition | Section « Langue » |
| Un email sous les 150 mots, avec le diff de ce qui a été corrigé à la main | Sections « Email envoyé » et « Diff » |
| Un historique daté qui permet de reprendre le dossier six semaines plus tard | Section « Historique » |
