#!/bin/sh
python handler.py > output.py &&
python test_data.py &&
python output.py
