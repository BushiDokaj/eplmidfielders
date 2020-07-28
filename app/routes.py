from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session
import pandas as pd

@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html')