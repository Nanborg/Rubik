# Rubik — Instructions pas à pas

Suivez les étapes **dans l'ordre**. Cochez quand c'est fini.
Règles partagées : [CONVENTIONS.md](CONVENTIONS.md). Sujet : [SUJET.md](SUJET.md).

**Plan :** Python = interface + tests. C++ = tout le calcul. Lien = l'exécutable `./rubik_engine`.
Le simulateur Python sert pendant le projet, pas dans `./rubik`.

---

## Étape 0 — Démarrer (ensemble)

- [ ] Cloner le dépôt, lancer `make`.
- [ ] Lire [CONVENTIONS.md](CONVENTIONS.md) ensemble.
- [ ] Ajouter le PDF du sujet dans `docs/`.

---

## Étape 1 — Le cube et les mouvements

Chacun code **sa propre version** du cube. Pas de code partagé.

**Python** (`python/`)
- [ ] `parser.py` : lire `F R U2 B' L' D'`, refuser le reste (`M E S x y z`, etc.).
- [ ] `verifier.py` : simuler un cube, appliquer des mouvements.
- [ ] Tests dans `tests/test_parser.py` et `tests/test_rotations.py`.

**C++** (`cpp/`)
- [ ] `cube.hpp/.cpp` : 8 coins, 12 arêtes (position + orientation).
- [ ] `moves.hpp/.cpp` : les 18 mouvements.
- [ ] Test dans `cpp/tests/test_moves.cpp`.

**Ensemble**
- [ ] Python crée `data/vectors/moves.txt` avec `python/gen_vectors.py`.
- [ ] Le test C++ relit ce fichier : états identiques.

✅ Fini quand : Python et C++ donnent **le même cube** pour chaque mélange.

---

## Étape 2 — Coordonnées et tables

**C++ seul** (Python avance sur l'étape 4)
- [ ] `coordinates.cpp` : coordonnées de la phase 1 et de la phase 2.
- [ ] `tables.cpp` : tables de transition.
- [ ] `tables.cpp` : tables de pruning.
- [ ] `make` crée les tables dans `data/tables/` (nouvelle règle du `Makefile`).
- [ ] `./rubik` les charge seulement, sans les recalculer.
- [ ] Tests : chaque coordonnée revient bien à l'état d'origine.

✅ Fini quand : les tables se génèrent et se chargent sans erreur.

---

## Étape 3 — Le solveur

**C++**
- [ ] `phase1.cpp` : recherche IDA* jusqu'au groupe H.
- [ ] `phase2.cpp` : recherche IDA* pour finir.
- [ ] `solver.cpp` : enchaîner les deux phases, renvoyer la solution.
- [ ] Test `cpp/tests/test_solver.cpp` : la solution résout le cube.

**Python**
- [ ] Aider à tester : mélanges variés, cas difficiles.
- [ ] *(optionnel, hors rendu)* `python/solver.py` : ton solveur Two-Phase, même algorithme. Lent, pour apprendre et comparer avec le C++.

✅ Fini quand : tous les mélanges de test sont résolus, **sans Python**.

---

## Étape 4 — Brancher Python et C++

**C++**
- [ ] `main.cpp` : lire le mélange en argument, afficher la solution (contrat dans [CONVENTIONS.md](CONVENTIONS.md)).
- [ ] `main.cpp` : option `--build-tables` (appelée par `make`).
- [ ] Codes de retour : 0 ok, 1 mélange invalide, 2 erreur interne. Message `Error: ...` sur stderr.

**Python**
- [ ] `main.py` et `rubik` : lire l'argument, lancer `./rubik_engine` avec `subprocess`.
- [ ] Si `./rubik_engine` est absent : message « lancez make ».
- [ ] Tests : `mélange + solution` = cube résolu, vérifié par `verifier.py`.
- [ ] Afficher **uniquement** la solution sur stdout.
- [ ] Gérer les erreurs : relayer le message sur stderr, code 1.

✅ Fini quand : `./rubik "F R U2 B' L' D'"` affiche une solution valide.

---

## Étape 5 — Mesurer et améliorer

**Python**
- [ ] `benchmark.py` : mélanges reproductibles, longueurs variées.
- [ ] Mesurer le nombre de mouvements (moyenne).
- [ ] Mesurer le temps **total** d'un `./rubik` (démarrage + chargement des tables + recherche).
- [ ] Lancer plusieurs `./rubik` à la suite : chaque temps doit rester < 3 s.
- [ ] Tester le superflip (voir [POINTS_A_VERIFIER.md](POINTS_A_VERIFIER.md)).
- [ ] `tests/test_performance.py`.

**C++**
- [ ] Réduire le temps et la mémoire si besoin.
- [ ] Chercher des solutions plus courtes si le temps le permet.

✅ Fini quand : moyenne ≤ 50 mouvements et ≤ 3 secondes.

---

## Étape 6 — Livraison

**Ensemble**
- [ ] Tester depuis un dossier **vide** : `git clone`, `make`, `./rubik`.
- [ ] Tester sur la machine de la soutenance.
- [ ] Mettre à jour le `README.md` (retirer « seule la structure existe »).
- [ ] Documenter l'algorithme (simple, avec schémas).
- [ ] Vérifier avec [POINTS_A_VERIFIER.md](POINTS_A_VERIFIER.md).
- [ ] Chacun s'entraîne à **expliquer tout l'algorithme**.
