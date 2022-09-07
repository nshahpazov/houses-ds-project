# functionality
all: clean lint test
create_env:
	python3 -m venv venv
	. venv/bin/activate
	pip install --upgrade pip

install_requirements:
	. venv/bin/activate
	pip install -r requirements.txt

train: clean preprocess
	@echo "Training a model for the $(project_name) project"
	@python -m $(project_name).modelling.lasso

preprocess: fetch
	@echo "Preprocessing the data for the $(project_name) project"
	@mkdir -p data/raw data/interim data/proccessed
	@python -m $(project_name).preprocess data/raw/train.csv data/interim/train.csv
	@python -m $(project_name).preprocess data/raw/test.csv data/interim/test.csv

fetch:
	@mkdir -p data/raw data/interim data/proccessed
	@chmod 701 ./$(project_name)/fetch/fetch_dataset.sh
	@./$(project_name)/fetch/fetch_dataset.sh data/raw

# package specific functionallity
build_source:
	@python setup.py sdist

build_wheels:
	@python setup.py bdist_wheel

build_from_source:
	@python setup.py build

install:
	@python setup.py install

install_develop:
	pip install -e ./

clean:
	@echo "Cleaning up $(project_name)"
	@rm -rf *.egg-info
	@rm -rf $(raws_to_remove)
	@rm -rf data/**/*.csv
	@rm -rf models/**/*.pkl
	@rm -rf logs/*.log*

publish: train
	./publish.sh .

test:
	@pytest .

lint:
	@pylint houses_pipeline

# ignore the following
.PHONY: preprocess, test, fetch

# variables
project_name = houses_pipeline
raws_to_remove = data/raw/*.csv, data/raw/*.zip, data/raw/*.txt
