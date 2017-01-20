# make all runs main.py

PYTHON_LIBS="./point_creators;./tools;./results;./simulator;./data_parsers;./data_fetchers;./Strategies;./Strategies/ml_models;./Models"

run_main_py:
	PYTHONPATH=${PYTHON_LIBS} python main.py

all: run_main_py

