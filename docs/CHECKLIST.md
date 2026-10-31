# Rubik — Instructions pas à pas

Suivez les étapes **dans l'ordre**. Cochez quand c'est fini.
Règles partagées : [CONVENTIONS.md](CONVENTIONS.md). Sujet : [SUJET.md](SUJET.md).

**Plan :** Python = interface + vérification. C++ = moteur de résolution. Lien = `rubik_core.solve()`.

---

## Étape 0 — Démarrer (ensemble)

- [ ] Cloner le dépôt, lancer `make venv` puis `make`.
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

✅ Fini quand : tous les mélanges de test sont résolus, **sans Python**.

---

## Étape 4 — Brancher Python et C++

**C++**
- [ ] `bindings.cpp` : exposer `solve(scramble)` avec pybind11.
- [ ] Convertir les exceptions (voir [CONVENTIONS.md](CONVENTIONS.md)).

**Python**
- [ ] `main.py` et `rubik` : lire l'argument, appeler `rubik_core.solve`.
- [ ] Vérifier la solution avec `verifier.py` avant d'afficher.
- [ ] Afficher **uniquement** la solution sur stdout.
- [ ] Gérer les erreurs : message sur stderr, code 1.

✅ Fini quand : `./rubik "F R U2 B' L' D'"` affiche une solution valide.

---

## Étape 5 — Mesurer et améliorer

**Python**
- [ ] `benchmark.py` : mélanges reproductibles, longueurs variées.
- [ ] Mesurer le nombre de mouvements (moyenne).
- [ ] Mesurer le temps **total** (lancement + tables + recherche).
- [ ] `tests/test_performance.py`.

**C++**
- [ ] Réduire le temps et la mémoire si besoin.
- [ ] Chercher des solutions plus courtes si le temps le permet.

✅ Fini quand : moyenne ≤ 50 mouvements et ≤ 3 secondes.

---

## Étape 6 — Livraison

**Ensemble**
- [ ] Tester depuis un dossier **vide** : `git clone`, `make venv`, `make`, `./rubik`.
- [ ] Tester sur la machine d'évaluation.
- [ ] Mettre à jour le `README.md` (retirer « seule la structure existe »).
- [ ] Documenter l'algorithme (simple, avec schémas).
- [ ] Vérifier avec la fiche « points à vérifier ».
- [ ] Chacun s'entraîne à **expliquer tout l'algorithme**.
