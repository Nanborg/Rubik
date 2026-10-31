# Rubik — Règles fixes

Ces règles sont **finales**. On ne les rediscute pas.
Pour changer une règle : on modifie ce fichier à deux, par PR.

Voir aussi : [CHECKLIST.md](CHECKLIST.md) (les tâches).

---

## 1. Qui fait quoi

| | Python | C++ |
|---|---|---|
| Dossiers | `rubik`, `python/`, `tests/` | `cpp/`, `data/tables/` |
| Travail | CLI, erreurs, vérification, benchmark | cube, tables, solveur, binding |

- Je ne touche pas aux dossiers de l'autre.
- `Makefile`, `README.md`, `docs/` : on se relit.

---

## 2. Entrée

Commande :

```sh
./rubik "F R U2 B' L' D'"
```

- **1 seul argument** (une chaîne). Sinon : erreur.
- Mouvements permis : `U R F D L B`.
- Suffixes permis : `'` ou `2`.
- Séparateur : espace, tabulation ou retour ligne.
- Il faut séparer : `RU` est **invalide**.

**Invalide** (erreur) :
- `M E S x y z`
- minuscules (`r`)
- `U3`, `U2'`, `U'2`
- `Uw`
- apostrophe courbe `’`

**Valide, cube déjà résolu** :
- chaîne vide
- espaces seuls
- `R R'`

Sortie dans ces cas : une ligne vide, code 0.

Le parsing existe **en Python et en C++**, avec la même règle.

---

## 3. Sortie

**Succès :**
- stdout = la solution seule
- 1 espace entre les mouvements
- fin avec `\n`
- rien d'autre (pas de debug)

**Erreur :**
- stderr = `Error: <message>`
- stdout vide
- code de retour `1`
- jamais de traceback Python

**Codes :** `0` = ok, `1` = erreur.

**Vérification :** Python vérifie la solution **avant** d'afficher. Si fausse → `Error: internal error`.

**Solution propre (C++) :**
- pas deux fois la même face : `R R2` interdit
- pas `U D U`

---

## 4. Le cube (convention Kociemba)

**Repère :** U = haut, F = devant, R = droite.
**Mouvement seul** = quart de tour horaire, vu de face.

**Faces :** `U R F D L B` (index 0 à 5)

**Coins :** `URF UFL ULB UBR DFR DLF DBL DRB` (index 0 à 7)

**Arêtes :** `UR UF UL UB DR DF DL DB FR FL BL BR` (index 0 à 11)

**Mouvements (index 0 à 17) :**
`U U2 U' R R2 R' F F2 F' D D2 D' L L2 L' B B2 B'`

Formule : `face * 3 + (puissance - 1)`
- puissance 1 = horaire
- puissance 2 = demi-tour
- puissance 3 = anti-horaire

**État du cube :**

| Nom | Taille | Sens |
|---|---|---|
| `cp` | 8 | quel coin est à la position i |
| `co` | 8 | rotation du coin (0, 1, 2) |
| `ep` | 12 | quelle arête est à la position i |
| `eo` | 12 | retournement de l'arête (0, 1) |

**Orientation d'un coin :**
- 0 = l'autocollant U/D est sur U/D
- 1 = tourné horaire
- 2 = tourné anti-horaire

**Orientation d'une arête :**
- 0 = autocollant principal bien placé
- 1 = retournée
- Principal = 1re lettre du nom (`UR` → U, `FR` → F, `BL` → B)

**Composition :** `a * b` = « a puis b ».

**Sources en cas de doute :**
- https://kociemba.org/math/cubielevel.htm
- https://kociemba.org/math/coordlevel.htm

**Tests obligatoires (des deux côtés) :**
- somme `co` = 0 modulo 3
- somme `eo` = 0 modulo 2
- parité coins = parité arêtes
- un quart de tour 4 fois = cube résolu
- `R U R' U'` répété 6 fois = résolu
- `R U` répété 105 fois = résolu

---

## 5. Vérifier Python contre C++

**Vérificateur Python :**
- indépendant du C++
- il ne copie ni tables ni modèle du C++
- idée : simuler les autocollants en 3D

**Fichier partagé :** `data/vectors/moves.txt`
- créé par Python : `python/gen_vectors.py`
- graine fixe : `42`
- lu par un test C++
- une ligne : `scramble|cp|co|ep|eo`
- on le régénère seulement à deux, par PR

**Test du solveur :** `mélange + solution` doit donner un cube résolu (selon Python).

---

## 6. Lien Python ↔ C++

- Module : `rubik_core`
- Une seule fonction : `solve(scramble: str) -> str`
- Déjà résolu → renvoie `""`
- `std::invalid_argument` → `ValueError`
- `std::runtime_error` → `RuntimeError`
- Aucune autre exception ne sort
- **1 seul appel** C++ par résolution
- Le C++ doit marcher **sans Python** (`cpp/tests/*.cpp`, chacun avec son `main`)
- `rubik_core*.so` est créé par `make`, jamais commité

---

## 7. Algorithme : Two-Phase

- Kociemba, recherche IDA*
- On l'écrit **nous-mêmes** (ni `kociemba` pip, ni code copié)
- On doit pouvoir tout expliquer

**Phase 1** → entrer dans le groupe H = ⟨U, D, R2, L2, F2, B2⟩
- `twist` : 2187
- `flip` : 2048
- `UDSlice` : 495
- 18 mouvements

**Phase 2** → finir dans H
- coins : 40320
- arêtes U/D : 40320
- arêtes du milieu : 24
- 10 mouvements : `U U2 U' D D2 D' R2 L2 F2 B2`

**Tables :**
- transitions + pruning
- créées au 1er lancement si absentes
- stockées dans `data/tables/` (ignoré par git)
- dossier changeable : variable `RUBIK_TABLES_DIR`
- `make` peut les pré-générer
- binaire, petit-boutiste, 1 fichier par table

**Longueur :**
- après la 1re solution, on cherche plus court
- limite : 1,5 s depuis le début de `solve`
- on s'arrête dès que ≤ 30 mouvements

---

## 8. Objectifs

| Critère | Valeur |
|---|---|
| Moyenne | ≤ 50 mouvements (visé : < 30) |
| Temps | ≤ 3 s, de bout en bout |
| Benchmark | `python python/benchmark.py [nombre] [longueur] [graine]` |
| Défaut | 20 mélanges, longueur 25, graine 1 |

Le benchmark sort en erreur si : un échec, temps > 3 s, ou moyenne > 50.

**Tests à prévoir :**
- mélanges fixes (graine), longueurs 1 à 40
- vide
- déjà résolu
- un seul mouvement
- superflip
- mouvements répétés

---

## 9. Outils

- Ubuntu 24.04 (WSL ok)
- Python **3.12**
- `g++` : `-std=c++17 -O2 -Wall -Wextra -Werror`
- GNU Make
- `.venv` via `make venv`
- seule dépendance : `pybind11` (version dans `requirements.txt`)
- tests Python : `unittest`
- pas de `sudo pip`

| Commande | Effet |
|---|---|
| `make` | compile `rubik_core` |
| `make test` | tous les tests |
| `make bench` | benchmark |
| `make clean` / `fclean` / `re` | nettoyage |

**Nouveau fichier `.cpp`** → l'ajouter dans `ENGINE_SRCS` (Makefile).
**Nouveau test C++** → l'ajouter dans `CPP_TESTS` (Makefile).

**Style :**
- C++ : tabulations
- Python : 4 espaces
- fichiers en `snake_case`

---

## 10. Git

- `main` = stable
- Branches : `py/<sujet>` ou `cpp/<sujet>`
- Merge par PR, relue par l'autre
- Commits en anglais, courts : `Add move parsing`
- 1 commit = 1 étape qui compile
- Jamais commité : `.venv/`, `build/`, `*.so`, `data/tables/*`
