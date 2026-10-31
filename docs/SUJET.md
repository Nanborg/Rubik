# Rubik — Résumé du sujet (v5)

Le sujet complet est en PDF (à ajouter dans `docs/`). Ici : l'essentiel.

## À faire

- Programme `rubik` : prend un mélange en argument.
- Affiche une solution sur la sortie standard.
- Cube 3×3×3 seulement.

## Notation

- Faces : `F R U B L D`.
- Suffixes : `'` (anti-horaire) et `2` (demi-tour).
- Séparés par un ou plusieurs espaces.
- **Interdit** : `M E S` (tranches) et `x y z` (rotations).
- Aucune autre notation.

Exemple valide :
`R2 D' B' D F2 R F2 R2 U L' F2 U' B' L2 R D B' R' B2 L2 F2 L2 R2 U2 D2`

## Score

- 1 quart de tour = 1 mouvement.
- 1 demi-tour = 1 mouvement.
- Score = `./rubik "..." | wc -w`.

## Pour valider

- Moyenne : **50 mouvements** max.
- Temps : **3 secondes** max.
- Erreurs bien gérées.

## Interdit

- Renvoyer l'inverse du mélange.
- Ajouter des mouvements inutiles à l'inverse.
- Segfault, fuite mémoire, double free, boucle infinie.
- Une bibliothèque qui résout à notre place.

## Obligatoire

- `Makefile` avec les règles habituelles.
- Savoir expliquer l'algorithme avec des mots simples et des images.
- Justifier chaque bibliothèque utilisée.

## Bonus (seulement si la partie obligatoire est PARFAITE)

- Affichage graphique du cube.
- Solution plus courte en temps raisonnable.
- Plusieurs algorithmes.
- Générateur de mélange.
- Solution en étapes compréhensibles.
- Autres puzzles.
- Les options de bonus commencent par `-`.
