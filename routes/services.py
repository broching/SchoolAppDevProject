import shelve
from flask import Blueprint, render_template, request, url_for, flash, redirect, Flask
service = Blueprint('service', __name__)

app = Flask(__name__)


@service.route('/services')
def services():
    return render_template('services/services.html')


@service.route('/retrieve_appointment')
def retrieve_appointment():
    appointment_dict = {}
    db = shelve.open('appointment.db', 'r')
    appointment_dict = db['services.db']
    db.close()

    appointment_list = []
    for key in appointment_dict:
        appointment = appointment_dict.get(key)
        appointment_list.append(services)
    return render_template('add_new_service.html')
