from flask import Blueprint, render_template, request, url_for, flash, redirect, Flask

services = Blueprint('Services', __name__)

app = Flask(__name__)


@app.route('/services')
def services():
    return render_template('services/services.html')
