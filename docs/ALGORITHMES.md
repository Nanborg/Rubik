# Rubik — Tables CFOP

## Chargement

Les séquences sont dans `data/cfop/f2l.txt`, `oll.txt` et `pll.txt`.
Une ligne contient une séquence.
Les en-têtes F2L, comme `# [UFR FR]`, identifient la paire cible.

`load_table_algorithms()` lit les fichiers.
Chaque module construit ses clés en inversant les séquences sur le cube résolu.
Les fonctions `load_*_table()` gardent les tables en cache.

## Provenance F2L

Les séquences ont été générées depuis `f2l_actions()` du projet.
Dijkstra suivait les positions et orientations d’une paire.
Le coût comptait les mouvements avant simplification.
Les séquences ont ensuite été simplifiées.
L’outil de génération n’est pas encore versionné.

Les actions utilisent déjà le jaune sur D et le blanc sur U.
Chaque paire possède 384 clés, cas résolu inclus.
Les clés couvrent aussi les pièces mal insérées et leurs orientations.

La recherche reste disponible.
Une séquence de table doit être plus courte après simplification.
Elle doit résoudre la paire et restaurer la croix et les paires protégées.

## OLL et PLL

Le projet suit les étapes de la méthode CFOP.
L'implémentation, la reconnaissance des cas et les recherches sont propres au projet.
Les séquences OLL/PLL sont adaptées au repère blanc sur U et jaune sur D.
La construction des tables vérifie qu'OLL préserve F2L et que PLL préserve OLL.

Le chargement essaie quatre côtés par renommage des faces.
Aucune rotation x/y/z n’est ajoutée.
Les solveurs essaient les alignements D ; PLL inclut l’alignement final.

CFOP choisit le plus petit total simplifié parmi les 24 ordres F2L.
Aucun minimum absolu n’est garanti.
