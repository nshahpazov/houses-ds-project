all: lint, test, train, publish

test:
	@python -m pytest

lint:
	echo "Linting the entire project"
	@pylint houses_pipeline
	@pylint houses_api

install_pipeline_develop:
	pip install -e ./houses_pipeline

clean:
	@echo "Cleaning up $(project_name)"
	@rm -rf *.egg-info
	@rm -rf $(raws_to_remove)
	@rm -rf data/**/*.csv
	@rm -rf logs/*.log*

# functionality
train: clean preprocess
	@echo "Training a model for the $(project_name) project"
	@python -m $(pipeline_dir).modelling.lasso.py

preprocess: fetch
	@echo "Preprocessing the data for the $(project_name) project"
	@mkdir -p $(pipeline_dir)/data/raw data/interim data/proccessed
	@python -m $(pipeline_dir).preprocess data/raw/train.csv data/interim/train.csv
	@python -m $(pipeline_dir).preprocess data/raw/test.csv data/interim/test.csv

fetch:
	@mkdir -p data/raw data/interim data/proccessed
	@chmod 701 ./$(pipeline_dir)/fetch/fetch_dataset.sh
	@./$(pipeline_dir)/fetch/fetch_dataset.sh data/raw

clean_pipeline:
	@echo "Cleaning up generated data, logs and models"
	@rm -rf data/**/*.csv
	@rm -rf models/**/*.pkl
	# @rm -rf logs/*.log*

publish: train
	.$(houses_pipeline)/scripts/publish_model.sh .


# ignore the following
# .PHONY: preprocess, test, fetch

# variables
project_name = houses_pipeline
pipeline_dir = houses_pipeline
raws_to_remove = data/raw/*.csv, data/raw/*.zip, data/raw/*.txt
