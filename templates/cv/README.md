# CV — HTML une page, export PDF

## Pourquoi du HTML plutôt qu'un traitement de texte

- **Décliner par cible coûte trente secondes** : copier le fichier, changer le titre de positionnement, réordonner deux blocs de compétences.
- **Le rendu est déterministe** : contrairement à un fichier Word ouvert sur une autre machine, un PDF généré depuis du HTML contrôlé sort toujours pareil.
- **C'est du texte versionnable** : un `git diff` montre exactement ce qui a changé entre la version envoyée à A et celle envoyée à B.

## Générer le PDF

```bash
# Chromium headless — le plus fidèle, gère @page et print-color-adjust
chromium --headless --disable-gpu \
  --print-to-pdf=CV-{{Organisation}}.pdf \
  --no-pdf-header-footer \
  CV-{{Organisation}}.html
```

Sur macOS, remplacer `chromium` par :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

Alternative si Node est installé :

```bash
npx --yes puppeteer-cli print CV.html CV.pdf --format A4 --print-background
```

## La checklist de vérification, avant chaque envoi

- [ ] **Une seule page.** Vérifier le nombre de pages du PDF, pas l'aperçu navigateur. Le `overflow: hidden` du template masque le débordement au lieu de créer une page 2 : un dépassement se traduit par du **contenu tronqué**, pas par une page supplémentaire.
- [ ] **Format A4 réel** : la MediaBox doit être 595 × 842 points.
- [ ] **Les fonds sombres sont présents.** S'ils ont disparu, `print-color-adjust: exact` manque ou n'a pas été respecté par le moteur.
- [ ] **Zéro tiret cadratin** (—, –) dans le texte.
- [ ] **Zéro résidu de la langue d'origine** si le CV a été traduit. Vérifier les mois, les intitulés de diplôme, les libellés de sections.
- [ ] **Chaque chiffre existe dans `profil.md`.**
- [ ] L'adresse email du CV est bien celle depuis laquelle vous envoyez.
- [ ] Le nom du fichier est propre : `CV-{{Prénom-Nom}}-{{Organisation}}.pdf`, pas `cv_final_v3.pdf`.

Vérifier le nombre de pages et le format en une commande :

```bash
# macOS
mdls -name kMDItemNumberOfPages CV.pdf
# multiplateforme, si poppler est installé
pdfinfo CV.pdf | grep -E "Pages|Page size"
```

## Polices

Deux options.

**Option 1, portable — embarquer les polices en base64.** Le PDF est identique partout, le HTML pèse quelques centaines de kilooctets. À privilégier pour un CV.

```css
@font-face {
  font-family: 'Ma Police';
  font-style: normal;
  font-weight: 300 600;
  font-display: block;
  src: url('data:font/woff2;base64,d09GMgABAAAA...') format('woff2');
}
```

Pour produire la chaîne base64 :

```bash
base64 -i MaPolice.woff2 | tr -d '\n' > police.b64
```

Vérifier la licence de la police avant d'embarquer. Les polices sous SIL Open Font License (Space Grotesk, JetBrains Mono, Inter, IBM Plex) le permettent explicitement.

**Option 2, léger — polices système avec fallback.** Le template livré fonctionne ainsi. Le rendu dépend de ce qui est installé sur la machine qui génère le PDF, ce qui est acceptable si vous générez toujours depuis la même machine.

## Règles de mise en page qui tiennent la page unique

- `@page { size: A4; margin: 0 }` et le corps dimensionné en millimètres : la marge est gérée par le padding interne, pas par le moteur d'impression.
- `overflow: hidden` sur `body` et `.cv` : garantit qu'aucune deuxième page ne se crée. Contrepartie : il faut vérifier visuellement qu'on ne coupe rien.
- `margin-top: auto` sur le dernier bloc de chaque colonne (langues, formation) : ils s'ancrent en bas, la colonne respire quel que soit le volume au-dessus.
- Une seule couleur d'accent. Deux couleurs d'accent sur un CV, c'est déjà trop.
- Grille à deux colonnes fixes : la colonne latérale à 66 mm accueille contact, compétences et langues sans jamais bouger d'une déclinaison à l'autre.

## Décliner par cible

Ce qui change d'une candidature à l'autre :

| Élément | Change ? |
|---|---|
| Titre de positionnement (`.cv-role`) | **Toujours** — c'est la ligne qui parle à la cible |
| Résumé (`.cv-resume`) | **Souvent** — recentrer sur l'angle du dossier |
| Ordre des blocs de compétences | **Souvent** — le bloc le plus pertinent en premier |
| Ordre et volume des expériences | Parfois |
| Langue | Selon `methode/03-langue-et-region.md` |
| Chiffres, dates, intitulés | **Jamais** |

Documenter les adaptations dans la section `## CV` du README de la candidature. Deux mois plus tard, en entretien, il faut savoir quelle version la personne en face a sous les yeux.

## Version anglaise

`cv-template-en.html` est le même gabarit avec les libellés de section, les commentaires et les placeholders en anglais. Mise en page, CSS et procédure d'export identiques.

La langue du CV suit celle de l'email, jamais l'inverse : voir `methode/03-langue-et-region.md`. Un CV anglais accompagnant un email français signale que le CV a été recyclé sans être relu.
