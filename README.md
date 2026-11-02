*This project has been created as part of the 42 curriculum by nicolsan and neon_05.*

# Rubik

Projet 42 de Rubik's Cube 3×3×3, entièrement en Python.
Résolution avec CFOP ; visualisation 3D animée pour voir et vérifier la solution.

## Répartition

| Partie | Responsable | Objectif |
| --- | --- | --- |
| Solver | neon_05 | Trouver la solution : Cross → F2L → OLL → PLL |
| Renderer | nicolsan | Représenter le cube en 3D et animer les mouvements reçus |
| Modèle commun et contrat | Ensemble | Même état initial, mêmes couleurs, mêmes mouvements |

## État actuel

Seule la structure est préparée pour cette nouvelle direction.
**Tous les fichiers Python contiennent uniquement des commentaires TODO.**
Aucun modèle, parser, solver, renderer ou test n’est implémenté.
Les interfaces décrites ci-dessous sont les objectifs à développer ensemble.

## Dossiers

```text
rubik                 entrée compatible avec le sujet → solver
solver.py             CLI du solver
render.py             CLI du renderer
common/
  colors.py           Enum Color
  state.py            12 arêtes + 8 coins ; positions fixes
  moves.py            parsing commun de la notation
  cube.py             rotations du modèle logique à implémenter
solving/              neon_05
  cli.py              mélange → solution sur stdout
  cfop.py             orchestration des quatre étapes
  cross.py
  f2l.py
  oll.py
  pll.py
rendering/            nicolsan
  cli.py              état initial + instructions sur stdin
  scene.py            cube, stickers, lumière et caméra
  animation.py        lecture des mouvements et transitions
  verifier.py         contrôle des états et de la solution
tools/benchmark.py    temps total et nombre de mouvements
tests/                modèle, solver, renderer et intégration
data/cfop/            algorithmes CFOP documentés à ajouter
docs/                 sujet, contrat et étapes du projet
```

Les anciens fichiers C++ et le solveur Python d'apprentissage étaient des
squelettes ; ils sont remplacés par cette structure Python.

## Démarrer

Python 3.10 ou plus récent et make. Le noyau utilise la bibliothèque standard.
La bibliothèque graphique sera choisie et documentée avant de développer la 3D ;
elle ne doit pas être nécessaire pour lancer le solver.

```sh
make
make test
```

`make` vérifie la syntaxe Python ; il ne compile aucun moteur C++.
`make test` ne lance actuellement aucun test réel : les fichiers de tests sont
des emplacements à compléter. Un succès avec zéro test ne valide rien.

## Interfaces prévues

Ces commandes sont à implémenter ; elles ne fonctionnent pas encore.

```sh
./rubik "F R U2 B' L' D'"
./solver.py "F R U2 B' L' D'"
./render.py "F R U2 B' L' D'" --output 3d --speed 2 --delay 0.5 < solution.txt
```

Le solver reçoit le mélange en un argument et écrit uniquement la solution.
Le renderer reçoit le même mélange pour reconstruire l'état initial et lit
la solution sur stdin. L'import d'un état cubie JSON est aussi prévu avec
`--state initial.json`. Ces deux modes d'entrée sont exclusifs.

Une fois les composants implémentés, exécution en deux temps :

```sh
MIX="F R U2 B' L' D'"
./solver.py "$MIX" > solution.txt &&
./render.py "$MIX" --output 3d --speed 2 --delay 0.5 < solution.txt
```

La première étape doit réussir avant de lancer la seconde. Pas de JSON, logs,
labels CFOP ou données graphiques dans la sortie standard du solver.

## Objectifs à mesurer

Le sujet impose une moyenne d'au plus 50 mouvements HTM et au plus 3 secondes
par résolution. **Le choix de CFOP ne garantit pas ces performances** : il faudra
mesurer puis optimiser les étapes et les enchaînements. Le renderer est lancé
séparément pour que son animation ne ralentisse pas la commande de résolution.

## Documents

- [Sujet résumé](docs/SUJET.md) et [PDF](Rubik.subject.pdf).
- [Points à vérifier](docs/POINTS_A_VERIFIER.md).
- [Contrat solver / renderer](docs/CONVENTIONS.md).
- [Checklist de travail](docs/CHECKLIST.md).
- [Objectifs du rendu 3D](docs/RENDERER.md).

Les fichiers `docs/SUJET.md` et `docs/POINTS_A_VERIFIER.md` sont conservés
tels quels comme références. Certaines mentions de l'ancienne architecture dans
ces références ne décrivent plus l'organisation du code.
