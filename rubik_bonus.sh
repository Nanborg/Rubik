#!/bin/sh
# Demande un melange, montre le melange, puis propose la resolution
cd "$(dirname "$0")" || exit 1

# Utilise le .venv du projet s'il existe
python=python3
[ -x .venv/bin/python3 ] && python=.venv/bin/python3
# Masque le message d'accueil de pygame
export PYGAME_HIDE_SUPPORT_PROMPT=1
if ! $python -c "import pygame" 2>/dev/null; then
    echo "Erreur : pygame manquant (pip install pygame dans .venv)" >&2
    exit 1
fi

printf "Melange : "
read scramble
solution=$(./rubik "$scramble") || exit 1

# Cube propre -> cube melange
echo "$scramble" | $python render.py &
render=$!
# Ferme cette fenetre si le script s'arrete (Ctrl+C compris)
trap 'kill $render 2>/dev/null' EXIT
trap 'exit 130' INT TERM

printf "Voulez-vous voir la solution ? (y/n) "
read answer

if [ "$answer" = "y" ]; then
    echo "Solution : $solution"
    # Cube melange -> cube propre
    echo "$solution" | $python render.py "$scramble"
fi
wait
