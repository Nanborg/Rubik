# Rubik — Modèle commun, solver obligatoire et renderer bonus

Contrat proposé pour votre travail à deux ; les détails sont à valider ensemble.
Le modèle et le solver sont implémentés. La CLI et les interfaces du renderer restent à terminer.

## Répartition

nicolsan développe `solving/`. neon_05 développe `rendering/`.
`common/`, les interfaces, les tests d'intégration et les documents se décident
ensemble. Le solver fonctionne sans importer le renderer ou une bibliothèque 3D.

## Priorité et indépendance

La partie obligatoire est `rubik` : moyenne ≤ 50 HTM, maximum ≤ 3 secondes
par résolution, démarrage Python et sortie texte compris. Le renderer est un
bonus facultatif, lancé après la résolution et jamais importé par le solver.
Les tests du noyau et le benchmark ne nécessitent pas de bibliothèque graphique.
Les bonus ne sont évalués que si la partie obligatoire est parfaite.

## Entrées et sorties

Contrat cible : `rubik` lance actuellement des essais aléatoires.

- `./rubik "<mélange>"` est l’unique entrée du solver.
- Le parsing CLI et les erreurs sont à écrire dans `rubik`, le calcul dans `solving/`.
- Entrée : un argument contenant le mélange, appliqué à un cube résolu.
- Sortie standard : mouvements de solution séparés par un espace, puis newline.
- Cube déjà résolu : ligne vide.
- Erreurs et diagnostics sur stderr ; aucun log sur stdout.
- Codes : 0 succès, 1 entrée invalide, 2 erreur interne ou fonction non implémentée.
- Ne pas renvoyer simplement l'inverse du mélange.

Affichage 3D bonus, entrée et options prévues dans `render.py` :
```sh
./render.py "<mélange initial>" --output 3d --speed 1 --delay 0 < solution.txt
./render.py --state initial.json --output logs < solution.txt
```

Le mélange initial et `--state` sont exclusifs. `--state` désigne un fichier
contenant l'état cubie décrit plus bas. Les mouvements de solution viennent de
stdin, pas du mélange initial. Le renderer n'appelle pas le solver.
`--speed` = mouvements par seconde, strictement positif ;
`--delay` = attente initiale en secondes, positive ou nulle.
`--output 3d` ouvre la scène ; `--output logs` sert au débogage sans fenêtre.
Ces deux sorties restent à implémenter.

## Notation et repère commun

- Seulement `U R F D L B`, éventuellement suivis de `2` ou de `'`.
- Un quart de tour est horaire en regardant la face depuis l'extérieur.
- Un demi-tour compte pour un mouvement HTM.
- `M E S x y z`, suffixes multiples et autres notations sont refusés.
- Le déplacement de la caméra ne modifie pas le repère logique du cube.
- Les formules CFOP utilisant des rotations globales ou des tranches doivent
  être adaptées à la notation autorisée avant usage/sortie.

| Face | Position | Couleur résolue |
| --- | --- | --- |
| U | haut (+Y) | WHITE |
| D | bas (-Y) | YELLOW |
| F | devant (+Z) | GREEN |
| B | derrière (-Z) | BLUE |
| R | droite (+X) | RED |
| L | gauche (-X) | ORANGE |

Le repère 3D est direct : X vers la droite, Y vers le haut, Z vers l'avant.

## État du cube : une liste ordonnée

`Colors` est une Enum partagée, pas une couleur propre à une bibliothèque 3D.
L'état contient 12 tuples d'arêtes puis 8 tuples de coins dans une seule liste.
Il est défini dans `common/cube.py`. Les six centres sont fixes et implicites.

L'index décrit **la position actuelle**, pas l'identité d'une pièce.

- Arêtes : `UF RF DF UR BR DR UB LB DB UL FL DL`.
- Coins : `URF UFL UBR ULB DFR DLF DRB DBL`.

Dans chaque tuple, l'ordre suit `POSITION_FACE` :
`state[Positions.UF] = (WHITE, GREEN)` signifie WHITE sur U, GREEN sur F.
`state[Positions.URF] = (WHITE, RED, GREEN)` signifie WHITE sur U, RED sur R,
GREEN sur F. Les alias de `Positions` ne changent pas cet ordre.

**Ne pas trier les couleurs des tuples** : leur ordre porte l'orientation.
Une simple collection de pièces sans positions ni orientation ne suffit pas.
La liste contient d'abord les 12 arêtes, puis les 8 coins.

```python
from common.cube import Positions, SOLVED
from common.colors import Colors

state = list(SOLVED)
# state[Positions.UF] == (Colors.WHITE, Colors.GREEN)
# state[Positions.URF] == (Colors.WHITE, Colors.RED, Colors.GREEN)
```

Le modèle, l'état résolu et les rotations sont implémentés.
La validation d'un état importé reste à faire.

## Extension facultative : format JSON des états

Après le noyau obligatoire, à envisager pour `--state` et les fixtures du bonus :
objet avec `version: 1`, `edges` et `corners`.
Les couleurs sont les valeurs textuelles de l'Enum, par exemple `"WHITE"`.
Ce format reste une proposition distincte de la liste interne du cube.

Valider : longueurs, couleurs connues, inventaire des pièces, absence de doublons,
orientation des arêtes et coins, et parité compatible des permutations.
Un état physiquement impossible doit être rejeté avant l'animation.
L'import/export JSON reste à implémenter.

## API implémentée

- `parse_moves(text) -> tuple[str, ...]` : parsing commun.
- `solve(moves) -> list[str]` : solution CFOP ; reçoit le mélange parsé.
- `solve(moves, with_steps=True)` : solution et détail des étapes.
- `list(SOLVED)` : nouvel état résolu indépendant à chaque appel.
- `apply_move(state, move) -> list[tuple]` : retourne un nouvel état.
- `apply_moves(state, moves) -> list[tuple]` : même convention.
- `is_cube_solved(state) -> bool` : compare à `SOLVED`, dans `solving/pll.py`.

L'animation garde un état de départ, une progression visuelle et un état cible.
Le nouvel état logique n'est validé qu'à la fin du mouvement ; pas de petites
rotations flottantes accumulées dans les données du cube.

## CFOP

Ordre : Cross → F2L → OLL → PLL. Dans notre repère, la croix blanche est sur U
et la dernière couche jaune sur D. Les formules pédagogiques CFOP qui placent
la croix blanche sur D doivent être remappées explicitement, sans changer les
couleurs du contrat et sans émettre x/y/z. Tester ce remapping avant de remplir
les cas CFOP ; ne pas mélanger les deux conventions.

Les algorithmes sont dans `data/cfop/` avec cas, repère, préconditions et
provenance. Pas de bibliothèque qui résout le cube à notre place.
Vérifier les postconditions de chaque étape ; garder les étapes et statistiques
en interne ou sur stderr, jamais dans la ligne de solution.

## Vérification et Git

Les tests obligatoires sont dans `tests/core/` ; ceux du bonus dans `tests/renderer/`.
Le renderer aide à voir les erreurs, mais ne remplace pas les tests du noyau.
Tester les mouvements avec des états attendus écrits indépendamment, et les
solutions par simulation. Réutiliser un seul modèle peut masquer une erreur
commune aux deux composants.

Branches `solver/<sujet>`, `renderer/<sujet>`, `shared/<sujet>`.
PR relue par l'autre ; commits courts en anglais.
Ne pas ajouter automatiquement de trailer de coauteur IA aux commits.
