import os
import shelve

import flask
from flask import Blueprint, render_template, request, url_for, redirect, Flask, session
from wtforms import form

# from models.Services import update_Service
from models.Services.Forms import AddNewService
from models.Services.services import Service
from models.Services.update_Services import update_Service

# from models.Services.update_Services import update_Service
from models.Services.update_Service import update_service_form

service = Blueprint('service', __name__)

app = Flask(__name__)


@service.route('/services')
def services():
    return render_template('services/services.html')


@service.route('/Services/haircut.html')
def haircut():
    return render_template('Services/haircut.html')


@service.route('/Services/hairwash.html')
def hairwash():
    return render_template('Services/hairwash.html')


@service.route('/Services/hairstyling.html')
def hairstyling():
    return render_template('Services/hairstyling.html')


@service.route('/Services/hairdye.html')
def hairdyeing():
    return render_template('Services/hairdye.html')


@service.route('/Services/addNewServiceform')
def add_new_service():
    form = AddNewService()
    return render_template('Services/addNewServiceform.html',
                           form=form)



@service.route('/addNewServiceform')
def appointment():
    service_list = []
    try:
        service_dict = {}
        with shelve.open('/Services/service_2.db', 'c') as db:
            if 'Service' in db:
                service_dict = db['Service']
            for key in service_dict:
                service = service_dict.get(key)
                service_list.append(service)
    except IOError as ex:
        print(f"Error in retrieving customers from service_2.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from service_2.db - {ex}")
    print("1")
    return render_template('Services/service.html', count=len(service_dict), form=form)


@service.route('/addNewServiceform', methods=['POST','GET'])
def book_appointment():
    print("1")
    Apointment_booking_form = AddNewService(request.form)
    if request.method == 'GET' and Apointment_booking_form.validate():
        try:
            with shelve.open('service_2.db', 'c') as db:

                service_dict = {}
                if 'Service' in db:
                    service_dict = db['Service']
                service = Service(Apointment_booking_form.first_name.data,
                                  Apointment_booking_form.last_name.data,
                                  Apointment_booking_form.gender.data,
                                  Apointment_booking_form.appointment_date.data,
                                  Apointment_booking_form.appointment_time.data,
                                  Apointment_booking_form.remarks.data)

                service_dict[service.get_first_Name()] = service
                db['Service'] = service_dict
                print("2")
                return ("Submission Succesful")
        except IOError as ex:
            print("Error in retrieving Appointment")
            return render_template('/Services/servicebase.html', form=Apointment_booking_form)

    else:
        print("3")
        return render_template('/Services/addNewServiceform.html', form=Apointment_booking_form)


@service.route('/Services/addNewServiceform', methods=['POST', 'GET'])  # Datepicker(appointmentbooking)
def index():
    form = AddNewService()
    if form.validate_on_submit():
        session['apointment_date'] = form.apointment_date.data
        return redirect('/Services/retrieveAppointment.html')
    return render_template('/Services/addNewServiceform.html', form=form)


# @service.route('/date', methods=['GET', 'POST'])
# def date():
#     appointment_date = session['appointment_date']
#     return render_template('date.html')


@service.route("/Services/retrieveAppointment")
def retrieve_appt():
    appt_list = []
    try:
        appt_dict = {}
        with shelve.open('service_2.db', 'r') as db:
            if 'Service' in db:
                appt_dict = db['Service']
            for key in appt_dict:
                service = appt_dict.get(key)
                appt_list.append(service)
    except IOError as ex:
        print(f"Error in retrieving products from product.db (inventory route)- {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")
    return render_template('/Services/retrieveAppointment.html', count=len(appt_list), appt_list=appt_list)


# Route for update service forms
@service.route('/Services/updateServices', methods=['GET', 'POST'])
def add_new():
    add_new_form = update_service_form(request.form)
    if request.method == 'POST' and add_new_form.validate():
        appt_dict = {}
        db = shelve.open('service_2.db', 'c')
        try:
            appt_dict = db['hairstylist']
        except:
            print("Error in retrieving appointment records from service.db")
        service = update_Service.Service(add_new_form.service.data,
                                         add_new_form.hairstylist.data,
                                         add_new_form.appointment_time.data,
                                         add_new_form.appointment_date.data
                                         )
        print("1")
        appt_dict[service.get_hairstylist()] = service
        db['hairstylist'] = appt_dict
        db.close()
        return redirect('/Services/retrieveAppointment.html')
    return render_template('/Services/updateServices.html', form=add_new_form)


# @service.route("/Services/retrieveAppointment")
# def retrieve_appt():
#     appt_dict = {}
#     db = shelve.open("service.db", 'r')
#     appt_dict = db['hairstylist']
#     db.close()
#
#     appt_list = []
#     for hairstylist in appt_dict:
#         appt = appt_dict.get(hairstylist)
#         appt_list.append(appt)
#     return render_template('/Services/retrieveAppointment.html', count=len(appt_list), appt_list=appt_list)


# @service.route('/Services/updateService', methods=['POST', 'GET'])
# def update_Service():
#     print("1")
#     update_Service_form = update_service_form(request.form)
#     if request.method == 'POST' and update_Service_form.validate():
#         try:
#             with shelve.open('service.db', 'c') as db:
#
#                 update_Service_dict = {}
#                 if 'service' in db:
#                     update_Service_dict = db['Service']
#                 service = Service(update_Service_form.service.data,
#                                   update_Service_form.service_id.data,
#                                   update_Service_form.hairstylist.data,
#                                   update_Service_form.appointment_date.data,
#                                   update_Service_form.appointment_time.data,
#                                   update_Service_form.remarks.data)
#
#                 service.set_service_id(service.get_service_id())
#
#                 update_Service_dict[service.get_service_id()] = update_service
#                 db['service'] = update_Service_dict
#                 return ("Submission Succesful")
#         except IOError as ex:
#             print("Error in retrieving Appointment")
#             return render_template('/Services/servicebase.html', form=update_service_form)
#
#     else:
#         return render_template('/Services/addNewService.html', form=update_service_form)


@service.route('/updateService.html', methods=['GET', 'POST'])  # Datepicker-update service
def add_appt_date():
    form = update_service_form
    if form.validate_on_submit():
        session['add_appointment_date'] = form.appointment_date.data
        return redirect('/Services/updateService.html')
    return render_template('/Services/servicebase.html', form=update_service_form)


@service.route('/date', methods=['GET', 'POST'])
def appointmentDate():
    appointment_Date = session['appointment_date']
    return render_template('/Services/retrieveAppoinment.html')

# return render_template('/Services/retrieveAppointment.html')


# @service.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
# def updateAppointment(id):
# update_Appointment_form = (request.form)
# if request.method == 'POST' and AddNewService.validate():
# try:
# with shelve.open('service.db', 'w') as db:
# service_dict = {}
# if 'Service' in db:
# service_dict = db['service']
# if id in service_dict:
# appointment = service_dict.get(id)
# appointment.set_first_Name(AddNewService.first_name.data)
# appointment.set_last_Name(AddNewService.last_name.data)
# appointment.set_gender(AddNewService.gender.data)
# appointment.set_membership_ID(AddNewService.membership_ID.data)
# appointment.set_appointment_Date(AddNewService.appointment_date.data)
# appointment.set_appointment_Time(AddNewService.appointment_time.data)
# db['service'] = service_dict

# except IOError as ex:
# print(f"Error in updating products to products.db - {ex}")

# return redirect(url_for('retrieveAppointment.html'))
# else:
# try:
# with shelve.open('service.db', 'w') as db:
# appointment_dict = {}
# if 'service' in db:
# appointment_dict = db['appointment']
# if id in appointment_dict:
# appointment = appointment_dict.get(id)
# AddNewService.first_name.data = Service.get_first_Name()
# AddNewService.last_Name.data = Service.get_last_Name()
# AddNewService.gender.data = Service.get_gender()
# AddNewService.membership_ID.data = Service.get_membership_ID()
# AddNewService.appointment_date.data = Service.get_appointment_Date()
# AddNewService.appointment_time.data = Service.get_appointment_Time()

# except IOError as ex:
# print(f"Error in retrieving products from products.db - {ex}.")
# return render_template('Services/retrieveAppointment.html', form=AddNewService)
