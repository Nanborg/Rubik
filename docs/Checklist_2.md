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
- [x] `rubik` : arguments, erreurs, stdout contenant uniquement la solution.
- [x] Initialiser le cube à partir du mélange, sans simplement l'inverser.
- [x] Première recherche de solution pour la croix, testée sur des mélanges courts.
- [x] Tester la croix sur des mélanges longs. Optimisation supplémentaire non nécessaire.
- [x] F2L avec vérification du résultat et restauration des paires protégées.
- [x] OLL avec vérification du résultat.
- [x] PLL avec vérification du résultat.
- [x] Comparer les solutions CFOP complètes pour les 24 ordres F2L.
- [x] Charger les tables F2L, OLL et PLL en cache.
- [x] Sortir uniquement U/R/F/D/L/B avec suffixe éventuel 2 ou apostrophe.
- [x] Simplifier les enchaînements de mouvements.
- [x] Documenter le format des tables et la provenance F2L dans `docs/ALGORITHMES.md`.
- [x] Documenter l'approche CFOP et l'adaptation OLL/PLL au repère du projet.
- [x] Gérer le cube déjà résolu dans `solve()`.
- [x] Gérer toutes les erreurs CLI proprement, sans crash.
- [x] Tester une résolution CFOP complète et le cube déjà résolu.
- [x] `tests/core/test_solutions.py` : mélange + solution = cube résolu, mélanges reproductibles, cas simples, difficiles, superflip.
- [x] Vérifier les performances : moyenne ≤ 50 HTM avec `rubik_perf`, maximum ≤ 3 s par lancement complet de `./rubik`

`rubik_perf` génère par défaut 100 mélanges aléatoires et affiche leur bilan.
Les chronométrages réutilisent les caches et excluent le démarrage Python.
Le temps complet de lancement se vérifie séparément avec `time ./rubik "<mélange>"`.

## 3. Affichage 3D — neon_05

- [x] Commencer un prototype avec Pygame.
- [x] Justifier le choix de la bibliothèque graphique.
- [x] `render.py` : mélange initial, instructions sur stdin, vitesse (`-s=`) et délai (`-d=`).
- [x] Cube 3D statique : cubies et stickers aux bonnes couleurs.
- [x] Caméra orbitale à la souris.
- [x] Animation des couches sans dérive de l'état logique.

## 4. Fin de projet — ensemble

- [x] Vérifier le parcours `rubik` → `render.py` (solution envoyée sur stdin).
- [ ] Tester depuis un clone propre sur la machine de l'école.
- [ ] Chacun sait expliquer le modèle, les mouvements, l'algorithme et l'affichage 3D.
