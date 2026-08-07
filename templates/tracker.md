# Tracker — pistes actives

> Une ligne par piste active. Les pistes closes descendent en bas. Les pistes seulement repérées vivent dans `entreprises.md`, pas ici.
>
> Statuts autorisés : En exploration · Dossier ouvert · Envoyé, en attente · Out of office · Bounce · En cours · Gelé · Clos.
> Détail : `methode/05-suivi-et-relances.md`.

## Actives

| Piste | Type | Statut | Dernière action | Prochaine action |
|---|---|---|---|---|
| **{{Organisation}}** | Candidature externe | **Envoyé, en attente ({{date}})** | Envoyé le {{date}} à {{Prénom Nom}} ({{adresse}} — **confirmée via mailto** / *déduite par pattern, bounce possible*) depuis {{email d'envoi}}, en {{langue}}, CV en pièce jointe. Angle : {{une phrase}}. Dossier `candidatures/{{nom}}/` | Relance le {{date}} si silence |
| **{{Organisation}}** | Candidature formelle (portail) | **Soumis le {{date}}** | Déposé sur {{portail}}, référence {{id}}. {{Contacts recruteurs identifiés}} | {{Email de signalement à un contact interne / attendre}} |
| **{{Organisation}}** | Piste via contact interne | **Dossier en préparation** | Contact interne identifié, pas de cold outreach nécessaire. Dossier `candidatures/{{nom}}/` | Valider le dossier puis transmettre |
| **{{Échéance administrative}}** | Admin / juridique | **À trancher** | {{Ce qui est en jeu et la date limite}} | {{Rendez-vous ou vérification à faire}} |

## Closes

| Piste | Issue | Date | Ce qu'on en retient |
|---|---|---|---|
| {{Organisation}} | ❌ Refusé | {{date}} | {{Délai entre soumission et refus + lecture : filtre automatique ou examen humain}} |
| {{Organisation}} | ❌ Bounce, jamais délivré | {{date}} | {{Cause : personne partie / format d'adresse / identifiants non déterministes}}. **La piste n'a jamais été tentée** |
| {{Organisation}} | Écarté volontairement | {{date}} | {{Raison explicite, pour ne pas la rouvrir par réflexe}} |
| {{Organisation}} | Offre dépubliée | {{date}} | Rien à retenter |

---

**Rappel** : une ligne sans date de prochaine action ne sera jamais traitée. Une ligne qui ne dit pas si l'adresse était confirmée ou déduite rend le silence ininterprétable.
