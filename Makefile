NAME = rubik

VENV = .venv
PY = $(VENV)/bin/python

CXX = c++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -Werror
INCLUDES = -Icpp/include

# Engine sources (everything except bindings.cpp). Add new C++ files here.
ENGINE_SRCS = cube.cpp moves.cpp coordinates.cpp tables.cpp phase1.cpp phase2.cpp solver.cpp
ENGINE_OBJS = $(addprefix build/,$(ENGINE_SRCS:.cpp=.o))

EXT_SUFFIX = $(shell python3 -c "import sysconfig;print(sysconfig.get_config_var('EXT_SUFFIX'))")
MODULE = rubik_core$(EXT_SUFFIX)

all: $(MODULE)

$(VENV)/.ready: requirements.txt
	python3 -m venv $(VENV)
	$(PY) -m pip install -q -r requirements.txt
	@touch $@

venv: $(VENV)/.ready

build/%.o: cpp/src/%.cpp $(wildcard cpp/include/*.hpp)
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $(INCLUDES) -fPIC -c $< -o $@

$(MODULE): $(VENV)/.ready $(ENGINE_OBJS) cpp/src/bindings.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -shared -fPIC \
		$$($(PY) -m pybind11 --includes) cpp/src/bindings.cpp $(ENGINE_OBJS) -o $@

build/%: cpp/tests/%.cpp $(ENGINE_OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $^ -o $@

# Standalone C++ tests (cpp/tests/test_*.cpp, each with its own main). Add the binaries here.
CPP_TESTS =

test-cpp: $(addprefix build/,$(CPP_TESTS))
	@for t in $(CPP_TESTS); do ./build/$$t || exit 1; done

test-py: all
	$(PY) -m unittest discover -s tests -v

test: test-cpp test-py

bench: all
	$(PY) python/benchmark.py

clean:
	rm -rf build

fclean: clean
	rm -f rubik_core*.so
	rm -rf $(VENV)

re: fclean all

.PHONY: all venv test test-cpp test-py bench clean fclean re
