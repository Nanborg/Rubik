*This project has been created as part of the 42 curriculum by nicolsan.*

# Rubik

> Résolveur de Rubik's Cube 3×3×3 · projet 42 · binôme Python / C++

| Metric | Value |
| --- | --- |
| 🧠 Focus | Notation officielle, modèle du cube, Two-Phase (Kociemba), vérification |
| 🛠️ Stack | Python 3.12 · C++17 · pybind11 · Makefile |
| 📄 Sujet | `docs/` (à ajouter : `rubik_subject.pdf`) |

## Description

`rubik` reçoit en argument une séquence de mélange (`F R U2 B' L' D'`) et affiche une séquence de résolution : moyenne ≤ 50 mouvements, ≤ 3 s, sans inverser le mélange.

Le dépôt ne contient que la **structure** : les fichiers sont vides (`TODO`). Tout le code reste à écrire.

## Où lire quoi

| Document | Contenu |
| --- | --- |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | **Décisions figées** : CLI, erreurs, conventions du cube, API, algorithme, outils, Git |
| [docs/CHECKLIST.md](docs/CHECKLIST.md) | Architecture et tâches de chaque codeur |

## Structure

```text
rubik            point d'entrée (Python)
python/          CLI, parsing, vérificateur, benchmark      -> codeur Python
tests/           tests unittest                             -> codeur Python
cpp/             moteur C++ (include/, src/, tests/)        -> codeur C++
data/tables/     tables générées (ignorées par git)
docs/            conventions et checklist
Makefile         compilation du module rubik_core
```

## Environnement

```sh
git clone git@github.com:Nanborg/Rubik.git
cd Rubik
make venv   # .venv + pybind11
make        # compile rubik_core
```

Prérequis : Ubuntu 24.04, Python 3.12, `g++`, `make`.

| Commande | Effet |
| --- | --- |
| `make` | compile le module `rubik_core` |
| `make test` | tests C++ puis Python |
| `make bench` | benchmark |
| `make clean` / `fclean` / `re` | nettoyage |
