#!/usr/bin/env bash
PYTHONPATH=./src python -m unittest discover -s tests -p "test_*.py"