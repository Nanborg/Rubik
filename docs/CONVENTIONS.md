# Rubik — Contrat Python ↔ C++

Seulement ce qu'on doit **partager**. Le reste : voir [SUJET.md](SUJET.md) et [CHECKLIST.md](CHECKLIST.md).

## 1. Le lien

- Le C++ est un **exécutable** : `./rubik_engine` (fait par `make`).
- Python le lance avec `subprocess`. Aucune bibliothèque externe, ni côté C++ ni côté Python.
- Appel : `./rubik_engine "F R U2 B' L' D'"` (le mélange en **un seul argument**)
- Sortie (stdout) : la solution, mouvements séparés par 1 espace, fin avec `\n`
- Déjà résolu → une ligne vide
- **1 seul appel** par résolution
- Option interne : `./rubik_engine --build-tables` (appelée par `make`, crée les tables)

## 2. Erreurs

| Code de retour du C++ | Sens | Stderr |
|---|---|---|
| `0` | ok | rien |
| `1` | mélange invalide | `Error: <message>` |
| `2` | erreur interne (tables manquantes, bug) | `Error: <message>` |

Python relaie le message `Error: ...` sur stderr et sort avec le code `1`.
Le moteur C++ revalide le mélange : il ne fait pas confiance à Python.

## 3. Le cube (Kociemba)

Chiffres identiques des deux côtés.

- Faces : `U R F D L B` → 0 à 5
- Coins : `URF UFL ULB UBR DFR DLF DBL DRB` → 0 à 7
- Arêtes : `UR UF UL UB DR DF DL DB FR FL BL BR` → 0 à 11
- Mouvement : `face * 3 + (puissance - 1)` → 0 à 17
  - puissance 1 = horaire, 2 = demi-tour, 3 = anti-horaire
  - ordre : `U U2 U' R R2 R' F F2 F' D D2 D' L L2 L' B B2 B'`
- État : `cp` `co` `ep` `eo`
  - `cp`/`ep` : quelle pièce est à la position i
  - `co` : 0, 1, 2 (coins) — `eo` : 0, 1 (arêtes)
- `a * b` = « a puis b »
- Référence : https://kociemba.org/math/cubielevel.htm

## 4. Tests croisés

- Python a son **propre** simulateur (pas de code partagé avec le C++).
- Il sert **pendant le projet** et dans les tests. `./rubik` ne l'appelle pas (rendu rapide).
- Fichier commun : `data/vectors/moves.txt`
  - créé par Python (`python/gen_vectors.py`, graine `42`)
  - lu par un test C++
  - ligne : `scramble|cp|co|ep|eo`
- Vérité finale : `mélange + solution` = cube résolu, selon Python.

## 5. Fichiers

- Le C++ marche **sans Python** (`cpp/tests/*.cpp`).
- Tables : **créées par `make`**, jamais au lancement de `./rubik`.
- Elles sont dans `data/tables/` (non commitées).
- `./rubik` les **charge seulement**. Si elles manquent : erreur « lancez make ».
- Pourquoi : chaque `./rubik` est un nouveau processus, et il doit tenir 3 s.
- Nouveau `.cpp` → `ENGINE_SRCS` (Makefile). Nouveau test C++ → `CPP_TESTS`.
- `rubik_engine` : fait par `make`, jamais commité.
- `python/solver.py` : solveur Python **d'apprentissage**, même algorithme. Hors rendu, jamais appelé par `./rubik`.

## 6. Qui touche quoi

| Python | C++ |
|---|---|
| `rubik`, `python/`, `tests/` | `cpp/`, `data/tables/` |

`Makefile`, `README.md`, `docs/` : on se relit.

## 7. Git

- `main` stable. Branches `py/<sujet>` et `cpp/<sujet>`.
- Merge par PR, relue par l'autre.
- Commits en anglais, courts : `Add move parsing`.
