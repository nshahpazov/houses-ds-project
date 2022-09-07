#!/usr/bin/env bash
# TODO: might be good to change that to work on windows as well
kaggle competitions download -c house-prices-advanced-regression-techniques -p $1
unzip -o $1/*.zip -d $1/
