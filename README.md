*This project has been created as part of the 42 curriculum by nicolsan and neon_05.*

# Rubik

Résolveur de Rubik’s Cube 3×3×3 entièrement en Python, avec l’algorithme CFOP.

## Priorité : la partie obligatoire

```sh
./rubik "F R U2 B' L' D'"
```

Le programme reçoit le mélange et affiche uniquement les mouvements de solution.
Objectifs du sujet : **moyenne ≤ 50 mouvements HTM et temps maximal ≤ 3 secondes
par résolution**, démarrage Python et affichage de la solution compris.
Le choix de CFOP ne garantit pas ces performances : elles doivent être mesurées.

Le renderer 3D est un **bonus secondaire**, lancé séparément. La résolution
ne charge aucune bibliothèque graphique et n’attend aucune animation.
Les bonus ne sont évalués que si la partie obligatoire est parfaite.

## Répartition

| Partie | Responsable | Rôle |
| --- | --- | --- |
| Solver obligatoire | neon_05 | Cross → F2L → OLL → PLL |
| Renderer bonus | nicolsan | Visualisation 3D et lecture des mouvements |
| Modèle commun et validation | Ensemble | Couleurs, état du cube, rotations, tests et performances |

nicolsan peut préparer la 3D avec des séquences de test sans bloquer le solver.
La vérification des solutions et les benchmarks fonctionnent sans renderer.

## État actuel

**Structure uniquement : les fichiers Python contiennent des commentaires TODO.**
Aucun code Python ni test n’est implémenté. Les commandes décrites sont les
interfaces à construire ensemble ; elles ne résolvent ni n’affichent encore de cube.

## Organisation

```text
rubik                       unique entrée du solver : arguments et sortie
common/
  colors.py                 Enum des six couleurs
  state.py                  12 arêtes + 8 coins ordonnés
  moves.py                  notation et parsing
  cube.py                   rotations et état résolu
solving/                    neon_05 — CFOP
  cfop.py                   orchestration
  cross.py
  f2l.py
  oll.py
  pll.py
tools/benchmark.py          temps total et nombre de mouvements
tests/core/                 modèle, parsing, rotations, solutions, performances
data/cfop/                  algorithmes documentés à ajouter
render.py                   entrée du renderer bonus : arguments et stdin
rendering/                  nicolsan — bonus indépendant
  scene.py                  cube 3D, stickers et caméra
  animation.py              mouvements et contrôles de lecture
  verifier.py               vérifications propres à la lecture visuelle
tests/renderer/             tests du bonus
docs/                       références, contrat et tâches
```

## Commandes de travail

Python 3.10 ou plus récent et make pour le noyau. La bibliothèque graphique
reste à choisir et ne sera nécessaire qu’au bonus.

| Commande | Rôle |
| --- | --- |
| `make` | Vérifier la syntaxe du noyau obligatoire |
| `make test` | Lancer uniquement les tests du noyau |
| `make bench` | Mesurer le solver en processus séparés, une fois implémenté |
| `make check-renderer` | Vérifier la syntaxe du bonus |
| `make test-renderer` | Lancer les tests du renderer séparément |
| `make clean`, `make fclean`, `make re` | Nettoyer les caches Python / revérifier le noyau |

Actuellement les tests sont des TODO : un résultat « zéro test » ne valide rien.
Le benchmark est également à écrire.

## Visualisation facultative, après résolution

Interface prévue, à implémenter :

```sh
MIX="F R U2 B' L' D'"
./rubik "$MIX" > solution.txt &&
./render.py "$MIX" --output 3d --speed 2 --delay 0.5 < solution.txt
```

Le renderer reconstruit l’état initial à partir du mélange et rejoue la solution
lue sur stdin. Son démarrage et la durée des animations sont séparés du temps
mesuré pour `./rubik`. L’import d’un état JSON est une extension facultative.

## Documents

- [Auteurs](docs/author).
- [Sujet résumé](docs/SUJET.md) et [PDF](docs/Rubik.subject.pdf).
- [Points à vérifier](docs/POINTS_A_VERIFIER.md).
- [Conventions du modèle et interfaces](docs/CONVENTIONS.md).
- [Checklist : obligatoire puis bonus](docs/CHECKLIST.md).
- [Renderer bonus](docs/RENDERER.md).

`docs/SUJET.md` et `docs/POINTS_A_VERIFIER.md` sont conservés sans modification.
Le PDF et le fichier `author` sont rangés dans `docs/`.
`.gitignore` et `.editorconfig` restent à la racine pour appliquer leurs règles
à tout le dépôt.
Leurs mentions historiques C++ ne décrivent pas l’organisation actuelle.
