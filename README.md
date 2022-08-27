# Houses Data Science Pipeline

This is a Houses Data Science pipeline produced from an analysis you can see as
steps in notebooks/


## Requirements

* conda

## Installation

Run the following to install the project as a python package

```bash
pip install houses_pipeline
```

## Starting and exploring the project

```bash
conda create -f environment.yml
conda activate houses
```

## Building the package

```bash
python setup.py bdist_wheel
```


## Pipeline steps

#### Fetch the dataset

```bash
./houses_pipeline/fetch/fetch_dataset.sh data/raw
```

Or simply a one-liner of

```bash
kaggle competitions download -c house-prices-advanced-regression-techniques -p data/raw ;
unzip -o data/raw/*.zip -d data/raw/
```

#### Preprocess

* python houses_pipeline/preprocess data/raw/train.csv data/interim/train.csv

#### Data Splitting

* Not Yet Implemented

#### Model Training
* Not Yet Implemented


### Running tests

```bash
conda develop .
pytest
```

## Usage


## Contributing\Developing

```bash
pip install -e .[dev]
```

