# make all runs main.py

##PYTHON_LIBS="./data_fetchers;./data_processors;./Models;./evaluate;./testing;../nitrogenspider"
PYTHON_LIBS=""

run_main_py:
	PYTHONPATH=${PYTHON_LIBS} python main.py

all: run_main_py

