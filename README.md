*This project has been created as part of the 42 curriculum by nicolsan and neon_05.*

# Rubik

Résolveur de Rubik’s Cube 3×3×3 en Python avec la méthode CFOP.
Croix blanche sur U, dernière couche jaune sur D.

## Lancer les essais

Python 3.10 ou plus récent. Le solveur utilise la bibliothèque standard.

```sh
python3 rubik
```

Le programme génère 100 mélanges de 20 mouvements.
Il détaille le premier, puis affiche les mouvements moyens et le temps moyen.
Le premier calcul charge les tables. Les suivants réutilisent les caches.
Le temps affiché exclut le démarrage Python et l’affichage.

## État du projet

- Croix, F2L, OLL et PLL implémentés.
- Tables F2L, OLL et PLL chargées en cache.
- Comparaison des 24 ordres F2L sur le total CFOP simplifié.
- Affichage 3D avec Pygame en développement, indépendant du solveur.

L’entrée du sujet reste à faire : `./rubik "<mélange>"`.
Elle devra afficher uniquement la solution et gérer les erreurs.
Le sujet demande une moyenne ≤ 50 HTM et un temps maximal ≤ 3 secondes.
Le benchmark complet reste à écrire dans `tools/benchmark.py`.

## Structure des fichiers

```text
rubik                   essais et statistiques
common/
  colors.py             couleurs
  cube.py               positions, etat du cube et rotations
  moves.py              mouvements, tables et melanges
solving/
  cfop.py               orchestration et choix de la solution
  cross.py              croix blanche
  f2l.py                paires coin/arete
  oll.py                orientation de la derniere couche
  pll.py                permutation de la derniere couche
  search.py             recherche bidirectionnelle
data/cfop/              tables F2L, OLL et PLL
tests/core/             tests du solveur
tools/benchmark.py      benchmark a completer
render.py               entree de l'affichage 3D
rendering/              modules d'affichage 3D
tests/renderer/         tests de l'affichage 3D
docs/                   sujet et documentation
```

## Commandes

| Commande | Rôle |
| --- | --- |
| `make` | Vérifier la syntaxe du solveur |
| `make test` | Lancer les tests du noyau |
| `make bench` | Benchmark encore à implémenter |
| `make check-renderer` | Vérifier la syntaxe de l’affichage 3D |
| `make test-renderer` | Tester l’affichage 3D |
| `make clean` | Nettoyer les caches Python |

## Répartition

- nicolsan : solveur CFOP.
- neon_05 : affichage 3D.
- Ensemble : modèle commun et intégration.

## Documents

- [Sujet](docs/SUJET.md) et [PDF](docs/Rubik.subject.pdf).
- [Conventions](docs/CONVENTIONS.md).
- [Tables et provenance](docs/ALGORITHMES.md).
- [Checklist](docs/Checklist_2.md).
- [Vérifications finales](docs/POINTS_A_VERIFIER.md).
- [Affichage 3D](docs/RENDERER.md).
- [Auteurs](docs/author).
