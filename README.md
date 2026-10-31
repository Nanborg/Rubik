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
2. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) → les règles fixes
3. [docs/CHECKLIST.md](docs/CHECKLIST.md) → les tâches

## Dossiers

| Dossier | Rôle | Qui |
|---|---|---|
| `rubik` | point d'entrée | Python |
| `python/` | CLI, vérificateur, benchmark | Python |
| `tests/` | tests Python | Python |
| `cpp/` | moteur de résolution | C++ |
| `data/tables/` | tables générées (non commitées) | C++ |
| `docs/` | règles et tâches | les deux |

## Démarrer

```sh
git clone git@github.com:Nanborg/Rubik.git
cd Rubik
make venv
make
```

Besoin de : Ubuntu 24.04, Python 3.12, `g++`, `make`.

## Commandes

| Commande | Effet |
|---|---|
| `make` | compile `rubik_core` |
| `make test` | lance les tests |
| `make bench` | mesure vitesse et longueur |
| `make clean` | supprime `build/` |
| `make fclean` | supprime tout le généré |
| `make re` | `fclean` puis `make` |
