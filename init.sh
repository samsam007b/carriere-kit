#!/usr/bin/env bash
# Initialise un dossier de travail carrière à partir des templates du kit.
# Idempotent : n'écrase jamais un fichier existant.

set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$RACINE"

copier() {
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then
    echo "  = $dst (existe déjà, laissé tel quel)"
  else
    cp "$src" "$dst"
    echo "  + $dst"
  fi
}

echo "Initialisation du dossier carrière dans : $RACINE"
echo

echo "Fichiers de travail :"
copier templates/CLAUDE.md.template CLAUDE.md
copier templates/profil.md          profil.md
copier templates/tracker.md         tracker.md
copier templates/calendrier.md      calendrier.md
copier templates/entreprises.md     entreprises.md
copier templates/vision.md          vision.md
copier templates/positionnement.md  positionnement.md
copier templates/storytelling.md    storytelling.md

echo
echo "Dossiers :"
for d in candidatures prive; do
  if [[ -d "$d" ]]; then
    echo "  = $d/ (existe déjà)"
  else
    mkdir -p "$d"
    echo "  + $d/"
  fi
done

[[ -f prive/.gitkeep ]] || touch prive/.gitkeep

cat <<'FIN'

Terminé.

Prochaines étapes, dans l'ordre :

  1. Remplir profil.md          — source de vérité unique, tous les chiffres viennent de là
  2. Adapter CLAUDE.md          — remplacer les {{PLACEHOLDERS}}, notamment le positionnement
  3. Lire methode/00-vue-densemble.md   (5 minutes)
  4. Lire methode/01-outreach-email.md  avant le premier envoi

Puis, pour ouvrir une candidature :

  /nouvelle-candidature <organisation>

Rappel : prive/ est gitignored. Y ranger tout document contenant des données
personnelles ou des coordonnées de contacts.
FIN
