from flask import render_template, request
from app import app

GITHUB_CLIENT = 'Iv1.21156d618ca695a2'

OWNER = 'andrew-pettus'
REPO  = 'forkin'

@app.route('/')
def home():
    return render_template("index.html", clientID = GITHUB_CLIENT)

