*This project has been created as part of the 42 curriculum by nicolsan.*

# Rubik

> Résolveur de Rubik's Cube 3×3×3 · projet 42 · Python + C++

## But

```sh
./rubik "F R U2 B' L' D'"
```

Le programme affiche comment résoudre le cube.

- Moyenne : 50 mouvements max
- Temps : 3 secondes max
- Interdit : inverser le mélange

## État

Seule la **structure** existe. Les fichiers sont vides (`TODO`).

## Lire d'abord

1. [docs/SUJET.md](docs/SUJET.md) → le sujet en résumé
2. [docs/POINTS_A_VERIFIER.md](docs/POINTS_A_VERIFIER.md) → check pour rendu
3. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) → les règles fixes 
4. [docs/CHECKLIST.md](docs/CHECKLIST.md) → les étapes à suivre

## Dossiers

| Dossier | Rôle | Qui |
|---|---|---|
| `rubik` | point d'entrée | Python |
| `python/` | CLI, vérificateur, benchmark, `solver.py` (apprentissage) | Python |
| `tests/` | tests Python | Python |
| `cpp/` | moteur de résolution | C++ |
| `data/tables/` | tables générées (non commitées) | C++ |
| `docs/` | règles et tâches | les deux |

## Démarrer

```sh
git clone git@github.com:Nanborg/Rubik.git
cd Rubik
make
```

Besoin de : Linux, Python 3 (bibliothèque standard seulement), `g++`, `make`.

## Ordre des opérations

**Une fois**
- `make` → compile le C++ (`rubik_engine`) et **génère les tables** dans `data/tables/`.

**À chaque `./rubik "..."`** (moins de 3 s)
1. Python lit et vérifie le mélange.
2. Python lance `./rubik_engine` (un seul appel).
3. Le C++ charge les tables.
4. Le C++ cherche la solution (phase 1 puis phase 2).
5. Python affiche la solution.

**Pendant le projet, à part**
- `make test` → tests C++ et Python.
- `make bench` → moyenne de mouvements et temps le plus lent.
- `python python/solver.py "..."` → solveur Python d'apprentissage (hors rendu).

**Nettoyage** : `make clean`, `make fclean`, `make re`. Après `fclean`, refaire `make` avant `./rubik`.

## Commandes

| Commande | Effet |
|---|---|
| `make` | compile `rubik_engine` et crée les tables |
| `make test` | lance les tests |
| `make bench` | mesure vitesse et longueur |
| `make clean` | supprime `build/` |
| `make fclean` | supprime tout le généré |
| `make re` | `fclean` puis `make` |
