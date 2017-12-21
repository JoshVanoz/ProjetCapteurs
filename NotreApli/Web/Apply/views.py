from .app import app
from flask import render_template
from .models import get_parterres

@app.route("/")
def home():
    return render_template(
        "home.html",
        title="Hello World!")

@app.route("/Parterre/")
def parterre():
    return render_template(
        "parterre.html",
        mesParterre = get_parterres())
