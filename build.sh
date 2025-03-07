#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd) 