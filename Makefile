NAME = rubik_engine

CXX = c++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -Werror
INCLUDES = -Icpp/include

# Engine sources (everything except main.cpp). Add new C++ files here.
ENGINE_SRCS = cube.cpp moves.cpp coordinates.cpp tables.cpp phase1.cpp phase2.cpp solver.cpp
ENGINE_OBJS = $(addprefix build/,$(ENGINE_SRCS:.cpp=.o))

TABLES_READY = data/tables/.ready

all: $(NAME) $(TABLES_READY)

$(NAME): $(ENGINE_OBJS) build/main.o
	$(CXX) $(CXXFLAGS) $^ -o $@

# Tables are built once here, never when ./rubik runs.
$(TABLES_READY): $(NAME)
	./$(NAME) --build-tables
	@touch $@

build/%.o: cpp/src/%.cpp $(wildcard cpp/include/*.hpp)
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

build/%: cpp/tests/%.cpp $(ENGINE_OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $^ -o $@

# Standalone C++ tests (cpp/tests/test_*.cpp, each with its own main). Add the binaries here.
CPP_TESTS =

test-cpp: $(addprefix build/,$(CPP_TESTS))
	@for t in $(CPP_TESTS); do ./build/$$t || exit 1; done

test-py: all
	python3 -m unittest discover -s tests -v

test: test-cpp test-py

bench: all
	python3 python/benchmark.py

clean:
	rm -rf build

fclean: clean
	rm -f $(NAME)
	find data/tables -type f ! -name .gitkeep -delete

re: fclean all

.PHONY: all test test-cpp test-py bench clean fclean re
