# Rubik — Conventions figées (Python ↔ C++)

Ce document est le **contrat** entre le codeur Python et le codeur C++. Rien ici n'est à rediscuter : si un point doit changer, on modifie ce fichier par une PR validée par les deux, jamais seul dans son code.

Voir aussi [CHECKLIST.md](CHECKLIST.md) (architecture et tâches).

## 1. Répartition

| | Python | C++ |
|---|---|---|
| Dossiers | `rubik`, `python/`, `tests/` | `cpp/`, `data/tables/` |
| Responsable de | CLI, parsing, erreurs, sortie, vérificateur, benchmarks | modèle du cube, coordonnées, tables, Two-Phase, binding |

Règle : on ne modifie pas les dossiers de l'autre. `Makefile`, `README.md`, `docs/` : modifications par PR relue par l'autre.

## 2. Contrat de la ligne de commande

- Appel : `./rubik "F R U2 B' L' D'"` — **exactement 1 argument** (une chaîne). 0 ou 2+ arguments → erreur d'usage.
- Mouvements valides : `U R F D L B`, suffixe optionnel `'` (apostrophe ASCII `'`) ou `2`. Rien d'autre (`M E S x y z`, minuscules, `U3`, `U2'`, `U'2`, `Uw`, apostrophe typographique `’` → invalides).
- Séparateurs : un ou plusieurs espaces, tabulations ou retours à la ligne. Les mouvements **doivent** être séparés (`RU` invalide).
- Chaîne vide ou uniquement des espaces : **valide**, cube déjà résolu → sortie = une ligne vide, code 0.
- Une séquence qui ramène au cube résolu (`R R'`) → même sortie : ligne vide, code 0.
- Le parsing est fait **deux fois** : en Python (rejet rapide, vérification) et en C++ (même grammaire, exception `ValueError`).

## 3. Sorties et erreurs

- **stdout** : uniquement la solution, mouvements séparés par **un seul espace**, terminée par `\n`. Rien d'autre (pas de debug, pas de timing).
- **stderr** : en cas d'erreur, une ligne `Error: <message>` (le mot `Error` est fixe).
- Codes de retour : `0` succès, `1` toute erreur (usage, entrée invalide, erreur interne). Jamais de traceback Python visible.
- En cas d'erreur, stdout reste vide.
- Python vérifie **toujours** la solution avec son simulateur avant d'afficher ; si elle est fausse → `Error: internal error ...`, code 1.
- Solution canonique attendue du C++ : pas deux mouvements consécutifs sur la même face (`R R2` interdit), pas de séquence `U D U` (axe opposé répété sans intercalaire utile).

## 4. Modèle du cube (convention Kociemba)

Orientation de référence : **U** = haut, **F** = face avant, **R** = droite. Un mouvement sans suffixe = quart de tour **horaire vu de face** de cette face.

- Ordre des faces : `U R F D L B` → indices 0 à 5.
- Ordre des coins (index 0–7) : `URF UFL ULB UBR DFR DLF DBL DRB`.
- Ordre des arêtes (index 0–11) : `UR UF UL UB DR DF DL DB FR FL BL BR`.
- Index de mouvement (0–17) : `face * 3 + (puissance - 1)` avec puissance 1 = quart horaire, 2 = demi-tour, 3 = quart anti-horaire. Ordre : `U U2 U' R R2 R' F F2 F' D D2 D' L L2 L' B B2 B'`.
- État : `cp[8]` (quel coin est à la position i), `co[8]` (twist 0..2), `ep[12]` (quelle arête est à la position i), `eo[12]` (flip 0..1).
- Orientation des coins : 0 si l'autocollant U/D du coin est sur une face U/D ; 1 / 2 = vrillé dans le sens horaire / anti-horaire. Facelets d'un coin listés dans l'ordre horaire en commençant par U/D (ex. `URF` = U, R, F).
- Orientation des arêtes : 0 si l'autocollant « principal » (première lettre du nom de l'arête dans la liste ci-dessus, ex. `U` pour `UR`, `F` pour `FR`, `B` pour `BL`) est sur la première face de l'emplacement ; sinon 1.
- Composition : `(a * b)` = « a puis b ». Appliquer un mouvement m à un état s = `s * m`.
- Les définitions de référence viennent de <https://kociemba.org/math/cubielevel.htm> et de l'implémentation de H. Kociemba (`pykociemba`) ; en cas de doute, ces sources font foi.
- Invariants à tester des deux côtés : somme des `co` ≡ 0 (mod 3), somme des `eo` ≡ 0 (mod 2), parité de permutation des coins = parité des arêtes, chaque mouvement d'ordre 4 (ou 2 pour `X2`), `(R U R' U')` d'ordre 6, `(R U)` d'ordre 105.

## 5. Vérification croisée (Python ↔ C++)

- Le simulateur Python (`verifier.py`) doit être **indépendant** du moteur C++ : il ne réutilise ni ses tables ni ses conventions internes (suggestion : simulation 3D des autocollants plutôt qu'un clone du modèle cubie).
- Fichier de vecteurs partagé `data/vectors/moves.txt`, **généré par Python** (`python/gen_vectors.py`, graine fixe `42`) et **relu par le test C++**. Format d'une ligne : `scramble|cp|co|ep|eo`, valeurs séparées par un espace. Ce fichier est versionné ; on ne le régénère que par PR commune.
- Tout test de solveur : `scramble + solution` doit donner un cube résolu selon le vérificateur Python.

## 6. Interface Python ↔ C++ (pybind11)

- Module : `rubik_core`, fonction unique `solve(scramble: str) -> str`.
- Entrée : chaîne en notation officielle (déjà validée par Python, mais C++ revalide). Sortie : solution en notation officielle, `""` si déjà résolu.
- Erreurs : `std::invalid_argument` → `ValueError` ; `std::runtime_error` → `RuntimeError`. Aucune autre exception ne doit sortir. Python les convertit en `Error: ...` (section 3).
- **Un seul appel** C++ par résolution. Aucun aller-retour Python ↔ C++ dans la recherche.
- Le moteur C++ doit aussi compiler et être testable **sans Python** (`cpp/tests/*.cpp` avec leur propre `main`).
- Le module compilé `rubik_core*.so` est généré à la racine par `make` et n'est jamais versionné.

## 7. Algorithme (Two-Phase, réécrit par nous)

- Algorithme : Two-Phase de Kociemba, recherche IDA*. Aucun solveur externe (ni `kociemba` pip, ni code copié). On doit pouvoir tout expliquer.
- Phase 1 : amener le cube dans le groupe H = ⟨U, D, R2, L2, F2, B2⟩. Coordonnées : `twist` (2187), `flip` (2048), `UDSlice` (495). 18 mouvements.
- Phase 2 : résoudre dans H avec 10 mouvements `U U2 U' D D2 D' R2 L2 F2 B2`. Coordonnées : permutation des coins (40320), permutation des 8 arêtes U/D (40320), permutation des 4 arêtes de la couche du milieu (24).
- Définition des coordonnées : celles de <https://kociemba.org/math/coordlevel.htm>.
- Tables : transitions (par coordonnée × mouvement) et pruning (twist×slice, flip×slice, corners×slice, edges×slice).
- Les tables sont générées au premier lancement si absentes, puis stockées dans `data/tables/` (binaire, petit-boutiste, un fichier par table, ignoré par git). Le dossier peut être redéfini par la variable d'environnement `RUBIK_TABLES_DIR`. `make` peut aussi les pré-générer. Le temps de génération compte dans la limite des 3 s au premier lancement : il doit rester assez court ou être déclenché par `make`.
- Stratégie de longueur : après la première solution, continuer à chercher plus court tant que le temps écoulé depuis le début de `solve` est < 1,5 s ; renvoyer la meilleure trouvée. On arrête si la longueur ≤ 30.

## 8. Performance et critères d'acceptation

- Moyenne ≤ **50 mouvements HTM** (objectif réel visé : < 30).
- ≤ **3 s** par résolution, **mesuré de bout en bout** (lancement Python + chargement des tables + recherche), sur la machine d'évaluation.
- Benchmark : `python python/benchmark.py [nombre] [longueur] [graine]` — par défaut 20 mélanges de 25 mouvements, graine 1. Sort avec un code ≠ 0 si un échec, un temps > 3 s ou une moyenne > 50.
- Jeux de tests : mélanges reproductibles (graine fixe), longueurs 1 à 40, plus cas particuliers (vide, déjà résolu, un seul mouvement, superflip, mouvements répétés).

## 9. Environnement et outils

- Linux / Ubuntu 24.04 (WSL accepté), Python **3.12**, `g++` avec `-std=c++17 -O2 -Wall -Wextra -Werror`, GNU Make.
- Python : environnement virtuel `.venv` créé par `make venv`, dépendance unique `pybind11` (version figée dans `requirements.txt`). Tests : `unittest` de la bibliothèque standard. Pas de `sudo pip`.
- Commandes : `make` (compile `rubik_core`), `make test`, `make bench`, `make clean`, `make fclean`, `make re`.
- Quand on ajoute un fichier `.cpp`, il doit être listé dans `ENGINE_SRCS` du `Makefile` ; un nouveau test C++ dans `CPP_TESTS`.
- Style : C++ en tabulations, Python en 4 espaces (voir `.editorconfig`). Noms de fichiers en `snake_case`.

## 10. Git

- Branche `main` stable. Travail dans `py/<sujet>` ou `cpp/<sujet>`, intégré par PR relue par l'autre.
- Messages de commit en anglais, impératif, courts : `Add move parsing`, `Add corner twist coordinate`.
- Un commit = une étape qui compile. Ne jamais versionner `.venv/`, `build/`, `*.so`, `data/tables/*`.
