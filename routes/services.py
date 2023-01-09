import shelve

#from F import addNewServiceform
from flask import Blueprint, render_template, request, url_for,redirect, Flask
service = Blueprint('service', __name__)

app = Flask(__name__)


@service.route('/services')
def services():
    return render_template('services/services.html')


@service.route('/Services/addNewServiceform')
def add_new_service():
    return render_template('Services/addNewServiceform.html')


@service.route('/addNewServiceform')
def retrieve_appointment():
    service_dict = {}
    db = shelve.open('service.db', 'r')
    service_dict = db['service.db']
    db.close()

    service_list = []
    for key in service_dict:
        appointment = service_dict.get(key)
        service_list.append(services)
    return render_template('add_new_service.html')





