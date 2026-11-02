# Rubik — Obligatoire d’abord, bonus séparé

Références : [conventions](CONVENTIONS.md), [sujet](SUJET.md),
[points à vérifier](POINTS_A_VERIFIER.md). Tous les fichiers Python sont des TODO.

## 1. Modèle commun — ensemble

- [ ] Définir les couleurs Enum et le repère partagé.
- [ ] Définir les 12 arêtes et 8 coins, leurs positions et orientations.
- [ ] Construire l’état résolu et parser les 18 mouvements autorisés.
- [ ] Implémenter les rotations sans dépendance graphique.
- [ ] Tester chaque mouvement avec des états attendus indépendants.
- [ ] Tester quatre quarts de tour, deux demi-tours et mouvement + inverse.
- [ ] Fixer le repère des algorithmes CFOP avant de coder leurs cas.

## 2. Solver obligatoire — neon_05

- [ ] `rubik` : arguments, erreurs, stdout contenant uniquement la solution.
- [ ] Initialiser le cube à partir du mélange, sans simplement l’inverser.
- [ ] Cross : résoudre la croix.
- [ ] F2L : résoudre les quatre paires coin/arête.
- [ ] OLL : orienter la dernière couche.
- [ ] PLL : permuter la dernière couche et terminer l’alignement.
- [ ] Vérifier les postconditions des étapes sans casser les précédentes.
- [ ] Sortir uniquement U/R/F/D/L/B avec suffixe éventuel 2 ou apostrophe.
- [ ] Documenter les algorithmes dans `data/cfop/` et simplifier les enchaînements.
- [ ] Gérer le cube déjà résolu et toutes les erreurs sans crash.

## 3. Validation et performances obligatoires — ensemble

- [ ] `tests/core/` : parser, modèle, rotations et solutions.
- [ ] Vérifier par simulation que mélange + solution donne le cube résolu.
- [ ] Tester mélanges variés reproductibles, cas simples, difficiles et superflip.
- [ ] `tools/benchmark.py` : mesurer chaque lancement de `./rubik` séparément.
- [ ] Inclure démarrage Python et affichage texte dans le chronométrage.
- [ ] Vérifier moyenne ≤ 50 HTM et temps maximal ≤ 3 secondes, pas seulement le temps moyen.
- [ ] Optimiser CFOP si les mesures dépassent les objectifs.
- [ ] Tout vérifier sans installer ni lancer le renderer.
- [ ] Tester depuis un clone propre sur la machine de l’école.
- [ ] Chacun sait expliquer le modèle, les mouvements et l’algorithme.

## 4. Renderer bonus — nicolsan

Travail possible en parallèle avec des séquences de test. Aucune tâche de cette
section n’est une condition pour développer, tester ou chronométrer le solver.
Les bonus ne sont évalués que si l’obligatoire est parfait.

- [ ] Choisir une bibliothèque graphique et justifier ce choix.
- [ ] `render.py` : mélange initial, instructions sur stdin, vitesse et délai.
- [ ] Mode logs, puis cube statique et lecture des mouvements.
- [ ] Cubies, stickers, éclairage et caméra orbitale.
- [ ] Animation exacte des couches sans dérive de l’état logique.
- [ ] Pause, reprise, pas suivant/précédent et retour au début.
- [ ] Contrôler le résultat de la lecture et signaler les entrées invalides.
- [ ] `tests/renderer/` : tests du bonus indépendants de `make test`.
- [ ] Import/export JSON d’états : extension facultative après la base.
- [ ] Vérifier le parcours `rubik → fichier de solution → render.py`.

Les fichiers `SUJET.md` et `POINTS_A_VERIFIER.md` restent inchangés.
Leurs anciennes mentions C++ se lisent avec cette organisation Python.
