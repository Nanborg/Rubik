# Rubik — Checklist 2

## 1. Modèle commun (minimum partagé)

- [x] Définir les couleurs Enum et le repère partagé. -> Neon
- [x] Définir les 12 arêtes et 8 coins, leurs positions et orientations. -> Neon
- [x] Construire l'état résolu. -> Neon
- [x] Parser les 18 mouvements autorisés. -> nicolsan
- [x] Implémenter les rotations sans dépendance graphique. -> nicolsan
- [x] Tester chaque mouvement, puis quatre quarts de tour, deux demi-tours et mouvement + inverse. -> nicolsan

## 2. Solveur CFOP — nicolsan

- [x] Fixer le repère des algorithmes CFOP avant de coder leurs cas : blanc sur U, jaune sur D.
- [ ] `rubik` : arguments, erreurs, stdout contenant uniquement la solution.
- [x] Initialiser le cube à partir du mélange, sans simplement l'inverser.
- [x] Première recherche de solution pour la croix, testée sur des mélanges courts.
- [ ] Optimiser et tester la croix sur des mélanges longs.
- [x] F2L avec vérification du résultat et restauration des paires protégées.
- [x] OLL avec vérification du résultat.
- [x] PLL avec vérification du résultat.
- [x] Comparer les solutions CFOP complètes pour les 24 ordres F2L.
- [x] Charger les tables F2L, OLL et PLL en cache.
- [ ] Sortir uniquement U/R/F/D/L/B avec suffixe éventuel 2 ou apostrophe.
- [x] Simplifier les enchaînements de mouvements.
- [x] Documenter le format des tables et la provenance F2L dans `docs/ALGORITHMES.md`.
- [ ] Compléter la provenance initiale et les adaptations des algorithmes OLL/PLL.
- [x] Gérer le cube déjà résolu dans `solve()`.
- [ ] Gérer toutes les erreurs CLI proprement, sans crash.
- [x] Tester une résolution CFOP complète et le cube déjà résolu.
- [ ] `tests/core/test_solutions.py` : mélange + solution = cube résolu, mélanges reproductibles, cas simples, difficiles, superflip.
- [ ] `tools/benchmark.py` : un lancement de `./rubik` par mesure, démarrage Python inclus. Moyenne ≤ 50 HTM, maximum ≤ 3 s, optimisation si besoin.

Le `rubik` actuel génère 100 mélanges aléatoires et affiche leur bilan.
Les chronométrages réutilisent les caches et excluent le démarrage Python.
La CLI obligatoire et le benchmark en processus séparés restent à faire.

## 3. Affichage 3D — neon_05

- [x] Commencer un prototype avec Pygame.
- [ ] Justifier le choix de la bibliothèque graphique.
- [ ] `render.py` : mélange initial, instructions sur stdin, vitesse et délai.
- [ ] Cube 3D statique : cubies et stickers aux bonnes couleurs.
- [ ] Caméra orbitale.
- [ ] Animation des couches sans dérive de l'état logique.
- [ ] Lecture d'une solution : pause, reprise, pas suivant/précédent, retour au début.
- [ ] Signaler les entrées invalides.
- [ ] `tests/renderer/` : tests de l'affichage 3D.

## 4. Fin de projet — ensemble

- [ ] Vérifier le parcours `rubik` → fichier de solution → `render.py`.
- [ ] Tester depuis un clone propre sur la machine de l'école.
- [ ] Chacun sait expliquer le modèle, les mouvements, l'algorithme et l'affichage 3D.
