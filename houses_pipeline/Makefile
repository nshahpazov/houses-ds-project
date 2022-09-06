# functionality
train: preprocess
	@echo "Training a model for the $(project_name) project"
	@python modelling/lasso.py

preprocess: fetch
	@echo "Preprocessing the data for the $(project_name) project"
	@mkdir -p data/raw data/interim data/proccessed
	@python -m preprocess data/raw/train.csv data/interim/train.csv
	@python -m preprocess data/raw/test.csv data/interim/test.csv

fetch:
	@mkdir -p data/raw data/interim data/proccessed
	@chmod 701 ./fetch/fetch_dataset.sh
	@./fetch/fetch_dataset.sh data/raw

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
	@rm -rf logs/*.log*

test:
	@pytest .
lint:
	@pylint .

# ignore the following
.PHONY: preprocess, test, fetch

# variables
project_name = houses_pipeline
raws_to_remove = data/raw/*.csv, data/raw/*.zip, data/raw/*.txt
