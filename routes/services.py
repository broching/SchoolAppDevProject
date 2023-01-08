import shelve
from flask import Blueprint, render_template, request, url_for, flash, redirect, Flask

service = Blueprint('service', __name__)

app = Flask(__name__)


@app.route('/services')
def services():
    return render_template('services/services.html')


@app.route('/addNewService')
def add_new_service():
    services_dict = {}
    db = shelve.open('services.db', 'r')
    services_dict = db['services.db']
    db.close()

    service_list = []
    for key in services_dict:
        services = services_dict,get(key)
        service_list.append(services)
    return render_template('add_new_service.html')
