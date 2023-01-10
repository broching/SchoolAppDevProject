import shelve
from flask import Blueprint, render_template, request, url_for, redirect, Flask

from models.Services.Forms import AddNewService

service = Blueprint('service', __name__)

app = Flask(__name__)


@service.route('/services')
def services():
    return render_template('services/services.html')


@service.route('/Services/addNewServiceform')
def add_new_service():
    return render_template('Services/addNewServiceform.html')


@service.route('/addNewServiceform')
def inventory():
    service_list = []
    try:
        service_dict = {}
        with shelve.open('DB/Services/service.db', 'r') as db:
            if 'Service' in db:
                Service_dict = db['Service']
            for key in Service_dict:
                product = service_dict.get(key)
                service_list.append(product)
    except IOError as ex:
        print(f"Error in retrieving customers from customer.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('products/inventory.html', count=len(service_dict), service_list=service_list)


@service.route('/addNewServiceform', methods=['GET', 'POST'])
def book_appointment():
    Apointment_booking_form = AddNewService(request.form)
    if request.method == 'POST' and Apointment_booking_form.validate():
        try:
            with shelve.open('DB/Services/service.db', 'c') as db:
                Service_dict = {}
                if 'Products' in db:
                    Service_dict = db['Service']
                Service = AddNewService(Apointment_booking_form.first_name.data, Apointment_booking_form.last_name.data,
                                        Apointment_booking_form.gender.data,
                                        Apointment_booking_form.membership_ID.data,
                                        Apointment_booking_form.appointment_Date.data,
                                        Apointment_booking_form.appointment_Time.data)

                Service.set_membership_ID(Service.get_membership_ID())

                Service_dict[Service.get_membership_ID()] = Service
                db['Service'] = Service_dict
        except IOError:
            print("Error in retrieving Appointment")

    else:
        return render_template('Services/addNewService.html', form=Apointment_booking_form)
