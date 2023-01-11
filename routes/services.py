import shelve

from flask import Blueprint, render_template, request, url_for, redirect, Flask
from wtforms import form

from models.Services import update_Service
from models.Services.Forms import AddNewService
from models.Services.services import Service

service = Blueprint('service', __name__)

app = Flask(__name__)


@service.route('/services')
def services():
    return render_template('services/services.html')


@service.route('/Services/addNewServiceform')
def add_new_service():
    form = AddNewService()
    return render_template('Services/addNewServiceform.html',
                           form=form)


@service.route('/Services/updateServices')
def update_service():
    form = update_Service()
    return render_template('Services/update_Services.html',
                           form=form)


@service.route('/addNewServiceform')
def appointment():
    service_list = []
    try:
        service_dict = {}
        with shelve.open('/Services/service.db', 'r') as db:
            if 'Service' in db:
                Service_dict = db['Service']
            for key in Service_dict:
                product = service_dict.get(key)
                service_list.append(product)
    except IOError as ex:
        print(f"Error in retrieving customers from customer.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('Services/service.html', count=len(service_dict), form=form)


@service.route('/Services/addNewServiceform', methods=['POST'])
def book_appointment():
    Apointment_booking_form = AddNewService(request.form)
    if request.method == 'POST' and Apointment_booking_form.validate():
        try:
            with shelve.open('service.db', 'c') as db:

                Service_dict = {}
                if 'Products' in db:
                    service_dict = db['Service']
                service = Service(Apointment_booking_form.first_name.data,
                                  Apointment_booking_form.last_name.data,
                                  Apointment_booking_form.gender.data,
                                  Apointment_booking_form.membership.data,
                                  Apointment_booking_form.appointment_date.data,
                                  Apointment_booking_form.appointment_time.data,
                                  Apointment_booking_form.remarks.data)

                service.set_membership_ID(service.get_membership_ID())

                Service_dict[service.get_membership_ID()] = service
                db['Service'] = Service_dict
                return ("Submission Succesful")
        except IOError as ex:
            print("Error in retrieving Appointment")
            return render_template('/Services/servicebase.html', form=AddNewService)

    else:
        return render_template('/Services/addNewService.html', form=AddNewService)
