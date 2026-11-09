# Mémo Python — partie solving

Une ligne = une définition. Exemples tirés du projet.

## Lancer le programme

- `#!/usr/bin/env python3` : première ligne, permet de lancer `./rubik` sans écrire `python3`
- `chmod +x` : rend le fichier exécutable (nécessaire pour `./rubik`)
- `python3 -m module` : lance un module Python comme un programme (`-m unittest`, `-m compileall`)
- `compileall` / `py_compile` : vérifie que le code se compile (erreurs de syntaxe), utilisé par `make`
- `unittest` : module de tests intégré à Python, lancé par `make test`
- `__pycache__` : dossier de fichiers compilés `.pyc` créé automatiquement, supprimé par `make clean`
- `if __name__ == "__main__":` : bloc exécuté seulement si on lance le fichier directement, pas quand on l'importe

## Imports

- `import module` : charge un module, on écrit ensuite `module.nom`
- `from module import nom` : charge seulement `nom`, utilisable directement
- `from common.cube import SOLVED` : `common/cube.py` → on écrit le chemin avec des points
- `import ... as ...` : renomme à l'import (`Positions as pos`)
- Module : un fichier `.py` ; paquet : un dossier de modules (`common`, `solving`)

## Les 4 conteneurs

- `list` `[1, 2]` : suite ordonnée **modifiable** (append, pop…) — le cube pendant les calculs
- `tuple` `(1, 2)` : suite ordonnée **non modifiable** — une pièce, une séquence de mouvements
- `dict` `{"U": 1}` : associe une clé à une valeur, accès rapide par clé — tables OLL/PLL
- `set` `{1, 2}` : ensemble sans ordre et sans doublon — `allowed` dans `parse_moves`
- `set(piece) == set(colors)` : compare les couleurs sans tenir compte de l'ordre (trouver une pièce retournée)
- Hashable : objet non modifiable (str, int, tuple) → seul type accepté comme clé de dict ou élément de set
- Pourquoi des tuples comme clés : une liste ne peut pas être clé de dict, un tuple oui

## [] () {} — qui sert à quoi

- `[1, 2]` : crée une liste
- `x[0]` : lit l'élément 0 (liste, tuple, str)
- `d["U"]` : lit la valeur de la clé `"U"` dans un dict (erreur `KeyError` si absente)
- `d[a, b]` : clé tuple `(a, b)` sans écrire les parenthèses — `transitions[source, color_index]`
- `list[tuple]` : dans une annotation, veut dire « liste de tuples »
- `(1, 2)` : crée un tuple
- `f(x)` : appelle une fonction
- `()` : tuple vide
- `("D",)` : tuple d'un seul élément, **la virgule est obligatoire** (`("D")` = juste la chaîne `"D"`)
- `(a + b)` : parenthèses de priorité ou pour couper une longue ligne
- `{"U": 1}` : dict (deux-points entre clé et valeur)
- `{1, 2}` : set (pas de deux-points)
- `{}` : dict vide (un set vide s'écrit `set()`)
- `f"...{x}..."` : accolades dans une f-string = insérer une valeur

## Index et tranches (slicing)

- `x[0]` : premier élément ; `x[-1]` : dernier élément (`result[-1]`)
- `x[1:]` : tout sauf le premier — `move[1:]` = suffixe `"'"` ou `"2"`
- `x[:12]` : les 12 premiers — `state[:12]` = les arêtes
- `x[3:-1]` : du 4e à l'avant-dernier exclu — retire `# [` et `]`
- `x[a:b]` : de `a` inclus à `b` **exclu**
- `s[1:] + s[:1]` : décale d'un cran (rotation circulaire) — `face_map`, `rotate_algorithm`
- `(index + 1) % len(positions)` : `%` = reste de la division, revient à 0 à la fin (boucle circulaire)

## Chaînes de caractères (str)

- `text.split()` : découpe aux espaces → liste de mots
- `" ".join(liste)` : colle les éléments avec un espace → affichage final
- `text.strip()` : retire espaces et retour à la ligne aux extrémités
- `text.startswith("#")` / `endswith("'")` : teste le début / la fin
- `text.replace(a, b)` : remplace `a` par `b` — retire la face précédente du scramble
- `str.maketrans("RFLB", "FLBR")` : crée une table de remplacement lettre par lettre
- `move.translate(table)` : applique cette table — change le point de vue d'un algo
- `x.index(valeur)` : position de la première occurrence (str, list, tuple) — `piece.index(Colors.WHITE)`
- `f"Erreur : {error}"` : f-string, insère la valeur d'une variable dans le texte
- `"\033[38;5;46m"` : code ANSI, change la couleur du terminal ; `"\033[0m"` remet à zéro
- `face + suffix` : `+` concatène deux chaînes

## Fonctions intégrées

- `len(x)` : nombre d'éléments
- `range(n)` : nombres de 0 à n-1 ; `range(4)` → 0, 1, 2, 3
- `enumerate(x)` : donne `(index, valeur)` à chaque tour de boucle
- `zip(a, b)` : avance dans deux suites en même temps, par paires
- `dict(zip(a, b))` : crée un dict à partir de deux suites (clés, valeurs)
- `reversed(x)` : parcourt à l'envers sans créer de copie
- `all(...)` : `True` si toutes les conditions sont vraies — `is_cross_solved`
- `list(x)` / `tuple(x)` / `set(x)` : convertit vers ce type (et crée une copie)
- `print(x, end="")` : affiche sans retour à la ligne
- `print(x, file=stderr)` : affiche sur la sortie d'erreur
- `open(path, encoding="utf-8")` : ouvre un fichier texte

## Boucles et conditions

- `for x in suite:` : répète pour chaque élément
- `for _ in range(n):` : `_` = variable dont on ne se sert pas, juste répéter n fois
- `while cond:` : répète tant que la condition est vraie — `bidirectional_search`
- `continue` : passe directement au tour suivant
- `return` dans une boucle : arrête la boucle **et** la fonction
- `if / elif / else` : conditions ; `elif` = sinon si
- `and` / `or` / `not` : et / ou / non
- `x in d` : la clé existe dans le dict (ou l'élément dans la liste/set/str)
- `x not in allowed` : l'élément est absent
- `if result and ...` : une liste vide vaut `False`, une liste remplie vaut `True`

## Compréhensions (créer en une ligne)

- `[f(x) for x in suite]` : liste
- `{f(x) for x in suite}` : set — `allowed` dans `parse_moves`
- `{k: v for k in suite}` : dict — `transitions = {move: edge_transitions(move) ...}`
- `tuple(f(x) for x in suite)` : tuple (expression génératrice dans `tuple(...)`)
- `for face in "UDLRFB" for suffix in (...)` : deux `for` = boucles imbriquées → 18 mouvements
- `all(cond for x in suite)` : vérifie chaque élément sans créer de liste

## Déballage (unpacking)

- `a, b = b, a` : échange deux valeurs en une ligne — `cycle`
- `for p, i in pieces:` : chaque élément `(p, i)` est séparé en deux variables
- `destination, _ = locate_piece(...)` : garde la première valeur, ignore la seconde
- `return next_frontier, key` : renvoie deux valeurs (en réalité un tuple)
- `is_pair_solved(result, *p)` : `*` étale le tuple `p` en plusieurs arguments

## Fonctions

- `def nom(param):` : définit une fonction
- `return x` : renvoie une valeur ; sans `return` → renvoie `None`
- `def f(length=20):` : valeur par défaut si l'argument n'est pas donné
- `protected=()` : défaut en tuple vide, pas `[]` (une liste par défaut serait partagée entre les appels)
- `None` : « pas de valeur » ; tester avec `is None` / `is not None`
- `dict.get(clé)` : renvoie `None` si la clé est absente, au lieu d'une erreur
- Fonction passée en argument : `bidirectional_search(..., inverse_move)` reçoit une fonction et l'appelle
- Alias : `load_oll_algorithms = load_table_algorithms` → deux noms pour la même fonction
- `"""texte"""` : docstring, description de la fonction sous le `def`
- `@decorateur` : ligne au-dessus d'un `def`, ajoute un comportement à la fonction

## Listes : méthodes utilisées

- `l.append(x)` : ajoute un élément à la fin
- `l.extend(autre)` : ajoute tous les éléments d'une autre suite
- `l.pop()` : retire et renvoie le dernier élément — `simplify_move`
- `a + b` : nouvelle liste/tuple = `a` puis `b` — `cross + f2l + oll + pll`
- `list(state)` : copie de la liste → modifier la copie ne touche pas l'original

## Comparaisons

- `==` : compare le contenu (deux listes de tuples égales case par case) — `state == SOLVED`
- `is` : vérifie que c'est le même objet (utilisé avec `None`)
- `(a, b) < (c, d)` : compare `a` et `c`, puis `b` et `d` si égalité — `score = (len(solution), len(f2l))`

## Erreurs

- `raise ValueError("...")` : déclenche une erreur (valeur incorrecte)
- `NotImplementedError` : erreur « pas encore codé »
- `Exception` : la famille de toutes les erreurs classiques
- `try: ... except ValueError as error:` : attrape l'erreur et la met dans `error`
- `raise SystemExit(1)` : quitte le programme avec le code de retour 1
- `KeyError` : clé absente d'un dict avec `d[clé]`

## Fichiers

- `with open(...) as file:` : ouvre et **ferme automatiquement** le fichier à la fin du bloc
- `for line in file:` : lit le fichier ligne par ligne

## Modules externes utilisés

- `sys.argv` : liste des arguments ; `argv[0]` = nom du programme, `argv[1]` = le mélange
- `sys.stderr` : sortie d'erreur (séparée de l'affichage normal)
- `random.choice(suite)` : prend un élément au hasard — `random_scramble`
- `itertools.permutations(x)` : tous les ordres possibles ; 4 paires → 24 ordres
- `functools.cache` : mémorise le résultat d'une fonction pour les mêmes arguments → calculée une seule fois
- `@cache` exige des arguments hashables (tuples, pas listes)
- `pathlib.Path` : objet chemin de fichier, plus pratique qu'une chaîne
- `__file__` : chemin du fichier Python en cours
- `Path(__file__).resolve()` : chemin absolu complet
- `.parents[1]` : le dossier parent du parent (`solving/f2l.py` → racine du projet)
- `chemin / "data/cfop/f2l.txt"` : `/` colle deux morceaux de chemin
- `enum.IntEnum` : classe de constantes nommées qui se comportent comme des entiers
- `Positions.UF` : constante qui vaut 0, utilisable comme index de liste
- `FU = UF = 0` : deux noms pour la même valeur (alias)
- `position.name` : nom texte de la constante (`"UFR"`)

## Annotations de type (indicatives, non vérifiées)

- `def f(move: str) -> int:` : `move` est une chaîne, la fonction renvoie un entier
- `-> None` : ne renvoie rien
- `tuple[str, ...]` : tuple de chaînes, longueur quelconque
- `list[tuple]` : liste de tuples
- Python n'empêche pas d'envoyer un autre type : c'est de la documentation

## Classe

- `class Colors(IntEnum):` : définit un nouveau type qui hérite de `IntEnum`
- Héritage : `Colors` récupère le comportement d'`IntEnum`

## Vocabulaire algo du projet

- État / clé : tuple qui résume ce qui compte (positions + orientations des pièces suivies)
- Transition : dict « case de départ → case d'arrivée » pour un mouvement
- Recherche en largeur (BFS) : teste tous les chemins de 1 coup, puis 2, puis 3…
- Frontière : les états atteints au dernier niveau, à explorer ensuite
- Recherche bidirectionnelle : une recherche part du départ, une du résolu, on s'arrête quand elles se croisent
- Table d'algos : dict « cas → séquence » construit à partir des fichiers `data/cfop/*.txt`
- Inverse d'une séquence : ordre inversé + chaque mouvement inversé (`R` ↔ `R'`, `R2` reste `R2`)
