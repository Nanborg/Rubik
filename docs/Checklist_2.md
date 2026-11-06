# Rubik — Checklist 2

## 1. Modèle commun (minimum partagé)

- [x] Définir les couleurs Enum et le repère partagé. -> Neon
- [x] Définir les 12 arêtes et 8 coins, leurs positions et orientations. -> Neon
- [x] Construire l'état résolu -> Neon
- [x] parser les 18 mouvements autorisés. -> nicolsan
- [x] Implémenter les rotations sans dépendance graphique. -> nicolsan
- [x] Tester chaque mouvement, puis quatre quarts de tour, deux demi-tours et mouvement + inverse. -> nicolsan

## 2. Solver CFOP -- Nicolsan

- [ ] Fixer le repère des algorithmes CFOP avant de coder leurs cas.
- [ ] `rubik` : arguments, erreurs, stdout contenant uniquement la solution.
- [ ] Initialiser le cube à partir du mélange, sans simplement l'inverser.
- [ ] Cross, F2L, OLL, PLL, avec vérification des postconditions.
- [ ] Sortir uniquement U/R/F/D/L/B avec suffixe éventuel 2 ou apostrophe.
- [ ] Documenter les algorithmes dans `data/cfop/` et simplifier les enchaînements.
- [ ] Gérer le cube déjà résolu et toutes les erreurs sans crash.
- [ ] `tests/core/test_solutions.py` : mélange + solution = cube résolu, mélanges reproductibles, cas simples, difficiles, superflip.
- [ ] `tools/benchmark.py` : un lancement de `./rubik` par mesure, démarrage Python inclus. Moyenne ≤ 50 HTM, maximum ≤ 3 s, optimisation si besoin.

## 3. Rendu 3D simple -- Neon_05

- [ ] Choisir une bibliothèque graphique et justifier ce choix.
- [ ] `render.py` : mélange initial, instructions sur stdin, vitesse et délai.
- [ ] Cube 3D statique : cubies et stickers aux bonnes couleurs.
- [ ] Caméra orbitale.
- [ ] Animation des couches sans dérive de l'état logique.
- [ ] Lecture d'une solution : pause, reprise, pas suivant/précédent, retour au début.
- [ ] Signaler les entrées invalides.
- [ ] `tests/renderer/` : tests du rendu.

## 4. Fin de projet -- ensemble

- [ ] Vérifier le parcours `rubik` → fichier de solution → `render.py`.
- [ ] Tester depuis un clone propre sur la machine de l'école.
- [ ] Chacun sait expliquer le modèle, les mouvements, l'algorithme et le rendu.
