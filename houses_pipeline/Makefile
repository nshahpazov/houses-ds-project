build_source:
	python setup.py sdist
build_wheels:
	python setup.py bdist_wheel
build_from_source:
	python setup.py build
install:
	python setup.py install
install_develop:
	pip install -e ./

tests:
	pytest .
lint:
	pylint .

# package specific functionality
fetch:
	mkdir -p data/raw data/interim data/proccessed
	chmod 701 ./fetch/fetch_dataset.sh
	./fetch/fetch_dataset.sh data/raw

preprocess:
	mkdir -p data/raw data/interim data/proccessed
	python -m preprocess data/raw/train.csv
	python -m preprocess data/raw/test.csv

train:
	# TODO: THIS IS BROKEN
	python modelling/lasso.py

.PHONY: fetch preprocess