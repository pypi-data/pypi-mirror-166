import json
import os
import sys
from flask import render_template

def display_home():
    return render_template('backtest.html', name='zyd')

def display_data():
    with open(os.path.join(os.getcwd(), '__btcache__/backtest.json')) as f:
        return json.load(f)
