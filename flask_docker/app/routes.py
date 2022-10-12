from flask import render_template, request
from app import app

GITHUB_CLIENT = '1234'
SCOPES = '??'

OWNER = 'andrew-pettus'
REPO  = 'forkin'

@app.route('/')
def home():
    return render_template("index.html", clientID = GITHUB_CLIENT, scopes = SCOPES)

