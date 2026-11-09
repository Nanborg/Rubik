# Chemin des commandes

Tous les mélanges suivent le même parcours

```bash
./rubik "R U F' D2"
```

## Le cube en mémoire

- Un cube = une liste de 20 tuples (une case par pièce)
- Cases 0 à 11 = les 12 arêtes (tuples de 2 couleurs)
- Cases 12 à 19 = les 8 coins (tuples de 3 couleurs)
- `Positions` (cube.py) donne un nom à chaque case : `Positions.UF` = 0, `Positions.URF` = 12
- `SOLVED` (cube.py) = le cube résolu, sert de modèle pour toutes les comparaisons
- L'ordre des couleurs dans un tuple suit les faces du nom de la case (`POSITION_FACE`)
- Croix blanche sur U, dernière couche jaune sur D

## Vue d'ensemble

- Croix (fondation) → F2L (2 étages) → OLL (couleur du dernier étage) → PLL (rangement du dernier étage)

```mermaid
flowchart TD
    A["rubik<br/>Vérifie qu'il y a un seul argument"] --> B["parse_moves — moves.py<br/>Découpe le texte et valide chaque mouvement"]
    B --> C["solve — cfop.py<br/>apply_moves(SOLVED, moves) construit le cube mélangé"]
    C --> D{"Déjà résolu ?"}
    D -->|Oui| Z["Renvoie une liste vide"]
    D -->|Non| E["solve_cross — cross.py<br/>Place les 4 arêtes blanches"]
    E --> F["Boucle sur les 24 ordres des paires<br/>permutations(F2L_PAIRS)"]
    F --> G["solve_f2l_order — f2l.py<br/>Résout les 4 paires coin/arête"]
    G --> H["solve_oll — oll.py<br/>Oriente le jaune de la dernière couche"]
    H --> I["solve_pll — pll.py<br/>Place les pièces de la dernière couche"]
    I --> J["simplify_move — moves.py<br/>Fusionne croix + F2L + OLL + PLL"]
    J --> K{"Plus courte que la meilleure ?"}
    K -->|Oui| L["Garde cette solution"]
    K -->|Non| F
    L --> F
    F -->|24 ordres testés| M["rubik<br/>Affiche les mouvements séparés par des espaces"]
```

## Croix — `solve_cross`

- Le but : un « plus » blanc sur la face du haut, et la 2e couleur de chaque arête sous le bon centre
- Le programme ne regarde que les 4 arêtes blanches : où elles sont et de quel côté est leur blanc
- Il essaie les 18 mouvements depuis le cube mélangé, puis 18 depuis chaque résultat, et ainsi de suite
- En même temps, il fait pareil en partant d'un cube résolu
- Dès que les deux côtés tombent sur la même position, il recolle : chemin depuis le mélange + chemin vers le résolu joué à l'envers
- Comme il avance coup par coup, la première rencontre donne une croix très courte

```mermaid
flowchart TD
    A["solve_cross — cross.py"] --> B{"is_cross_solved ?"}
    B -->|Oui| Z["Renvoie []"]
    B -->|Non| C["Crée les 18 mouvements possibles"]
    C --> D["edge_transitions<br/>Pour chaque mouvement : où va chaque arête et son orientation"]
    D --> E["cross_key<br/>Clé de départ = position + orientation des 4 arêtes blanches"]
    E --> F["bidirectional_search — search.py<br/>Cherche depuis le départ ET depuis le cube résolu"]
    F --> G["expand_layer<br/>Avance d'un mouvement le côté le plus petit"]
    G --> H{"Les deux recherches se rencontrent ?"}
    H -->|Non| G
    H -->|Oui| I["Chemin aller + chemin retour inversé avec inverse_move"]
```

## F2L — `solve_f2l_order`

- Le but : finir les 2 premières couches sous la croix, donc remplir les 4 coins blancs et les 4 arêtes du milieu
- On les range par paires : un coin + l'arête juste en dessous = une paire, il y a 4 emplacements
- Il range une paire à la fois
- Il n'utilise que des gestes qui gardent la croix : tourner la couche du bas, ou ouvrir un côté (`R`), tourner le bas, refermer (`R'`)
- Il cherche la plus courte suite de gestes qui place la paire et remet les paires déjà faites (même recherche que la croix)
- Il regarde aussi la liste d'algos connus `f2l.txt` et prend l'algo s'il est plus court
- L'ordre des paires change la solution, donc il essaie les 24 ordres possibles

```mermaid
flowchart TD
    A["solve_f2l_order — f2l.py<br/>Reçoit un ordre des 4 paires"] --> B["solve_pair<br/>Une paire à la fois"]
    B --> C["f2l_key<br/>Clé = paires déjà faites (protected) + paire visée"]
    C --> D["f2l_actions<br/>27 séquences qui ne cassent pas la croix"]
    D --> E["f2l_transitions — @cache<br/>Trajet des pièces pour chaque séquence"]
    E --> F["bidirectional_search<br/>Trouve une solution par recherche"]
    F --> G["load_f2l_table — @cache<br/>Lit data/cfop/f2l.txt une seule fois"]
    G --> H{"La table a plus court<br/>et garde croix + paires ?"}
    H -->|Oui| I["Prend l'algo de la table"]
    H -->|Non| J["Prend la recherche"]
    I --> K["Ajoute la paire à protected"]
    J --> K
    K -->|Paire suivante| B
    K -->|4 paires faites| L["is_f2l_solved<br/>Vérifie, sinon ValueError"]
```

## OLL et PLL — `solve_oll` puis `solve_pll`

OLL
- Le but : il ne reste que la couche jaune, on veut toute la face jaune jaune, même si les pièces ne sont pas à leur place
- Le programme regarde de quel côté pointe le jaune sur les 8 pièces : ce dessin = le « cas »
- Au départ, il joue chaque algo de `oll.txt` à l'envers sur un cube résolu pour voir quel cas il résout
- Il range tout ça dans un dictionnaire : cas → algo le plus court
- Il tourne la face jaune 4 fois (rien, `D`, `D2`, `D'`) pour reconnaître le cas sous tous les angles

PLL
- Le but : la face jaune est faite, mais les côtés de la dernière couche sont mélangés, il faut échanger les pièces pour les remettre à leur place
- Le cas = quelle pièce est dans quelle case
- Même méthode que l'OLL, avec la liste `pll.txt`
- Si besoin, un dernier tour du bas (`D`, `D2` ou `D'`) aligne la couche → cube fini

```mermaid
flowchart TD
    A["load_oll_table / load_pll_table — @cache<br/>Lit oll.txt ou pll.txt"] --> B["rotate_algorithm<br/>Ajoute chaque algo vu sous 4 angles"]
    B --> C["oll_case / pll_case<br/>Applique l'algo à l'envers sur SOLVED pour trouver son cas"]
    C --> D["build_oll_table / build_pll_table<br/>Dictionnaire cas → algo le plus court"]
    D --> E["solve_oll / solve_pll<br/>Essaie 4 placements : rien, D, D2, D'"]
    E --> F["oll_key : où est le jaune de chaque pièce<br/>pll_key : quelle pièce est dans chaque case"]
    F --> G["table.get(clé)<br/>Garde la séquence la plus courte"]
```

- Une table est construite une seule fois grâce à `@cache`, puis réutilisée pour les 24 ordres
- La PLL teste aussi 4 finitions (`D`, `D2`, `D'`) pour aligner la dernière couche

## Erreurs

- Pas exactement un argument → `Usage : ./rubik "<melange>"`, code 1
- Mouvement inconnu → `Erreur : mouv invalide : X`, code 1
- Problème pendant la résolution → `Erreur de resolution : ...`, code 2
