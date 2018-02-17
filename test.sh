#!/bin/sh
python main.py > output.py &&
python test_data.py
python output.py
