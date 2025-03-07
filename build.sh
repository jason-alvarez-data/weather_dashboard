#!/bin/bash

# Create necessary directories
mkdir -p data
mkdir -p static/images

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd) 