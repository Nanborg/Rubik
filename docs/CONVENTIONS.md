# Rubik — Contrat solver / renderer Python

Contrat proposé pour votre travail à deux ; les détails sont à valider ensemble.
Aucune des API décrites n’est encore implémentée. Les exemples sont documentaires.

## Répartition

neon_05 développe `solving/`. nicolsan développe `rendering/`.
`common/`, les interfaces, les tests d'intégration et les documents se décident
ensemble. Le solver fonctionne sans importer le renderer ou une bibliothèque 3D.

## Entrées et sorties

- `./solver.py "<mélange>"` et `./rubik "<mélange>"` ont le même comportement.
- Entrée : un argument contenant le mélange, appliqué à un cube résolu.
- Sortie standard : mouvements de solution séparés par un espace, puis newline.
- Cube déjà résolu : ligne vide, une fois le solver implémenté.
- Erreurs et diagnostics sur stderr ; aucun log sur stdout.
- Codes : 0 succès, 1 entrée invalide, 2 erreur interne ou fonction non implémentée.
- Ne pas renvoyer simplement l'inverse du mélange.

Renderer :
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

## État du cube : deux listes ordonnées

`Color` est une Enum partagée, pas une couleur propre à une bibliothèque 3D.
`CubeState` contient `edges` (12 tuples de deux couleurs) et `corners`
(8 tuples de trois couleurs). Les six centres sont fixes et implicites.

L'index décrit **la position actuelle**, pas l'identité d'une pièce.

- Arêtes : `UR UF UL UB DR DF DL DB FR FL BL BR`.
- Coins : `URF UFL ULB UBR DFR DLF DBL DRB`.

Dans chaque tuple, l'ordre suit les lettres de sa position :
`edges[1] = (WHITE, GREEN)` signifie WHITE sur U, GREEN sur F à la position UF.
`corners[0] = (WHITE, RED, GREEN)` signifie WHITE sur U, RED sur R,
GREEN sur F à la position URF.

**Ne pas trier les couleurs des tuples** : leur ordre porte l'orientation.
Une simple collection de pièces sans positions ni orientation ne suffit pas.
Les deux listes correspondent à l'idée « 12 arêtes + 8 coins », en séparant
clairement leurs tailles et leur rôle.

```python
from common.state import CubeState

state = CubeState.solved()
# state.edges[1] == (Color.WHITE, Color.GREEN)
# state.corners[0] == (Color.WHITE, Color.RED, Color.GREEN)
```

Le modèle, l'état résolu, la validation physique et les rotations
sont tous à implémenter dans le modèle commun.

## Format JSON des états

À implémenter pour `--state` et les fixtures d'intégration :
objet avec `version: 1`, `edges` et `corners`.
Les couleurs sont les valeurs textuelles de l'Enum, par exemple `"WHITE"`.
Les listes et tuples respectent exactement les ordres ci-dessus.

Valider : longueurs, couleurs connues, inventaire des pièces, absence de doublons,
orientation des arêtes et coins, et parité compatible des permutations.
Un état physiquement impossible doit être rejeté avant l'animation.
L'import/export JSON est à implémenter, comme le reste du modèle.

## API prévue

- `parse_moves(text) -> tuple[str, ...]` : parsing commun, à implémenter.
- `solve(moves) -> list[str]` : solution CFOP ; reçoit le mélange parsé.
- `CubeState.solved()` : nouvel état résolu indépendant à chaque appel.
- `apply_move(state, move) -> CubeState` : retourne un nouvel état, à implémenter.
- `apply_moves(state, moves) -> CubeState` : même convention, à implémenter.
- `is_solved(state) -> bool` : comparer au repère résolu, à implémenter.

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

Le renderer aide à voir les erreurs, mais ne remplace pas les tests.
Tester les mouvements avec des états attendus écrits indépendamment, et les
solutions par simulation. Réutiliser un seul modèle peut masquer une erreur
commune aux deux composants.

Branches `solver/<sujet>`, `renderer/<sujet>`, `shared/<sujet>`.
PR relue par l'autre ; commits courts en anglais.
Ne pas ajouter automatiquement de trailer de coauteur IA aux commits.
