import sys
from threading import Timer
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os, os.path
from datetime import date
from numpy import NaN
import pandas as pd
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from werkzeug.utils import secure_filename
import time
import uuid
import shutil
import math
import csv

#from modules import permit_prep

#upload folder
UPLOAD_FOLDER = 'uploads/'
KEYWORD_FOLDER = 'keywords/'

#List for allowed file types to be uploaded to dashboard
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)

app.secret_key = 'key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KEYWORD_FOLDER'] = KEYWORD_FOLDER
    

#Checks if a file has an approved extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/home")
def hello_world():
    #return render_template('home.jinja2')
    return render_template('table.html')

@app.route("/")
def main_page():
    return render_template('to_upload.jinja2')
      
#headings = ["Segment ID", "Cell ID", "Voltage", "Temp"]
#data = { 
    #"Segment ID": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                   #2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
                   #3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                   #4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 
    #"Cell ID": [i for i in range(1, 19)] * 4, 
    #"Voltage": [3.6, 3.7, 3.8, 3.9, 4.0, 3.6, 3.7, 3.8, 3.9, 4.0, 3.6, 3.7, 3.8, 3.9, 4.0, 3.6, 3.7, 3.8] * 4, 
    #"Temp": [25, 26, 27, 28, 29, 25, 26, 27, 28, 29, 25, 26, 27, 28, 29, 25, 26, 27] * 4
#}


headings = [""] * 11  # 11 columns, including empty headers

# Example data, adjust as necessary
segment_data = [
    {"Voltage": 3.6},
    {"Voltage": 3.7},
    {"Voltage": 3.8},
    {"Voltage": 3.9},
    {"Voltage": 4.0},
    {"Voltage": 3.6},
    {"Voltage": 3.7},
    {"Voltage": 3.8},
    {"Voltage": 3.9},
]

# Generate data for 4 segments
data = []
for segment_id in range(1, 5):
    segment = []
    for i in range(2):
        row = [{"Segment ID": segment_id, "Cell ID": cell_id, "Voltage": segment_data[cell_id-1]["Voltage"]} for cell_id in range(1, 10)]
        segment.append(row)
    data.append(segment)

# unused but represents the graphics
@app.route("/markSent")
def mark_sent_pre():
    return render_template('table.html', headings=headings, data=data)

@app.route("/open")
def open_apps():
    return render_template('live_monitor.jinja2')

def open_browser():
      webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
      Timer(1, open_browser).start()
      app.run(port=5000)
