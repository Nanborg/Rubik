PYTHON ?= python3

all:
	$(PYTHON) -m compileall -q common solving rendering tools tests solver.py render.py

test: all
	$(PYTHON) -m unittest discover -s tests -v

bench:
	$(PYTHON) tools/benchmark.py

clean:
	find common solving rendering tools tests -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf __pycache__

fclean: clean

re:
	$(MAKE) fclean
	$(MAKE) all

.PHONY: all test bench clean fclean re
