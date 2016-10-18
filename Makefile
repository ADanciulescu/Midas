# make all runs main.py

PYTHON_LIBS="./tools;./simulator;./data_parsers;./data_fetchers;./Strategies;./Strategies/helpers;./Models"

run_main_py:
	PYTHONPATH=${PYTHON_LIBS} python main.py

all: run_main_py

