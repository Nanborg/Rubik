PYTHON ?= python3

# Partie obligatoire : aucune dépendance graphique.
all:
	$(PYTHON) -m compileall -q common solving tools
	$(PYTHON) -m py_compile rubik

test: all
	$(PYTHON) -m unittest discover -s tests/core -v

bench: all
	$(PYTHON) tools/benchmark.py

# Bonus : uniquement sur demande.
check-renderer:
	$(PYTHON) -m compileall -q rendering render.py

test-renderer: all check-renderer
	$(PYTHON) -m unittest discover -s tests/renderer -v

clean:
	find common solving rendering tools tests -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf __pycache__

fclean: clean

re:
	$(MAKE) fclean
	$(MAKE) all

.PHONY: all test bench check-renderer test-renderer clean fclean re
