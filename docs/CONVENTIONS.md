# Rubik — Contrat Python ↔ C++

Seulement ce qu'on doit **partager**. Le reste : voir [SUJET.md](SUJET.md) et [CHECKLIST.md](CHECKLIST.md).

## 1. Le lien

- Module : `rubik_core`
- Une fonction : `solve(scramble: str) -> str`
- Entrée : le mélange tel quel, ex. `"F R U2 B' L' D'"`
- Sortie : la solution, mouvements séparés par 1 espace
- Déjà résolu → `""`
- **1 seul appel** par résolution

## 2. Erreurs

| C++ lance | Python reçoit |
|---|---|
| `std::invalid_argument` | `ValueError` |
| `std::runtime_error` | `RuntimeError` |

Python affiche `Error: ...` sur stderr, code 1.

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
- Fichier commun : `data/vectors/moves.txt`
  - créé par Python (`python/gen_vectors.py`, graine `42`)
  - lu par un test C++
  - ligne : `scramble|cp|co|ep|eo`
- Vérité finale : `mélange + solution` = cube résolu, selon Python.

## 5. Fichiers

- Le C++ marche **sans Python** (`cpp/tests/*.cpp`).
- Tables dans `data/tables/` (non commitées), dossier changeable via `RUBIK_TABLES_DIR`.
- Nouveau `.cpp` → `ENGINE_SRCS` (Makefile). Nouveau test C++ → `CPP_TESTS`.
- `rubik_core*.so` : fait par `make`, jamais commité.

## 6. Qui touche quoi

| Python | C++ |
|---|---|
| `rubik`, `python/`, `tests/` | `cpp/`, `data/tables/` |

`Makefile`, `README.md`, `docs/` : on se relit.

## 7. Git

- `main` stable. Branches `py/<sujet>` et `cpp/<sujet>`.
- Merge par PR, relue par l'autre.
- Commits en anglais, courts : `Add move parsing`.
