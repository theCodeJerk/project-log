#!/bin/bash

# Script used to delete all the python cache
# files and folders that are generated.

find . -name "*.pyc" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;

