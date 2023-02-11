import shelve
from flask import redirect, url_for, session, flash
from bcrypt import checkpw
from models.account.account_classes import Customer, Staff
from functools import wraps
import datetime


def log_out():
    """Deletes session for customer and staff without flashing info message"""
    session.pop('customer', None)
    session.pop('staff', None)


def customer_login_required(func):
    """Decorator that validates customer login"""
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if 'customer' not in session:
            log_out()
            flash("Please log in to your account first to access this page", category='danger')
            return redirect(url_for('auth.customer_login'))
        else:
            return func(*args, **kwargs)

    return wrapper_func


def staff_login_required(func):
    """Decorator that validates staff login"""
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if 'staff' not in session:
            log_out()
            flash("Please log in to your account first to access this page", category='danger')
            return redirect(url_for('auth.staff_login'))
        else:
            return func(*args, **kwargs)

    return wrapper_func


def validate_username(username_to_validate, relative_path_to_db, exceptions=None):
    """Return True if username is not taken, False if username is taken"""
    is_valid = True
    username_list = []
    customer_list = get_customers(relative_path_to_db)
    staff_list = get_staff(relative_path_to_db)
    for customer in customer_list:
        username_list.append(customer.get_username())
    for staff in staff_list:
        username_list.append(staff.get_username())
    if exceptions:
        username_list.remove(exceptions)
    for username in username_list:
        if username == username_to_validate:
            is_valid = False
    return is_valid


def validate_customer_password(password_to_validate):
    """Validates password with session"""
    return checkpw(password_to_validate.encode(), session['customer']['_Account__password_hash'])


def validate_staff_password(password_to_validate):
    """Validates password with session"""
    return checkpw(password_to_validate.encode(), session['staff']['_Account__password_hash'])


def validate_email(email_to_validate, relative_path_to_db, exceptions=None):
    """Return True if email is not taken, False if email is taken"""
    is_valid = True
    email_list = []
    customer_list = get_customers(relative_path_to_db)
    staff_list = get_staff(relative_path_to_db)
    for customer in customer_list:
        email_list.append(customer.get_email())
    for staff in staff_list:
        email_list.append(staff.get_email())
    if exceptions:
        email_list.remove(exceptions)
    for email in email_list:
        if email == email_to_validate:
            is_valid = False
    return is_valid


def validate_number(number_to_validate, relative_path_to_db, exceptions=None):
    """Return True if number is not taken, False if number is taken"""
    is_valid = True
    number_list = []
    customer_list = get_customers(relative_path_to_db)
    staff_list = get_staff(relative_path_to_db)
    for customer in customer_list:
        number_list.append(customer.get_number())
    for staff in staff_list:
        number_list.append(staff.get_number())
    if exceptions:
        number_list.remove(exceptions)
    for number in number_list:
        if number == number_to_validate:
            is_valid = False
    return is_valid


def get_customers(relative_path_to_db):
    """Returns a list of customer objects"""
    transfer_dict = {}
    customer_list = []
    try:
        db = shelve.open(f"{relative_path_to_db}/account/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
        else:
            db['customer'] = transfer_dict
    except IOError:
        print("Error occurred while trying to open the shelve file - get customer function")
    except Exception as ex:
        print(f"Error occurred as {ex} - get customer function")
    for customer in transfer_dict.values():
        customer_list.append(customer)
    return customer_list


def store_customer(customer_object, relative_path_to_db):
    """Stores customer object inside the customer database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/account/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
        else:
            db['customer'] = transfer_dict
        transfer_dict[customer_object.get_user_id()] = customer_object
        db['customer'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - store customer function")
    except Exception as ex:
        print(f"Error occurred as {ex} - store customer function")


def delete_customer(customer_object, relative_path_to_db):
    """Deletes customer object inside the customer database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/account/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
        else:
            db['customer'] = transfer_dict
        transfer_dict.pop(customer_object.get_user_id(), None)
        db['customer'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - delete customer function")
    except Exception as ex:
        print(f"Error occurred as {ex} - delete customer function")


def customer_login_authentication(username_email, password, relative_path_to_db):
    """Checks if customer login matches the database and returns a dictionary of the customer
    object """
    customer_dict = {}
    customers = get_customers(relative_path_to_db)
    for customer in customers:
        if customer.get_status() == 'active':
            if customer.get_email() == username_email or customer.get_username() == username_email:
                if checkpw(password.encode(), customer.get_password_hash()):
                    customer_dict = account_to_dictionary_converter(customer)
    return customer_dict


def account_to_dictionary_converter(account_object):
    """Converts an object into a dictionary"""
    account_dict = vars(account_object)
    return account_dict


def is_valid_card_number(card_input):
    """Validates the credit card number"""
    card_input = card_input[::- 1]
    card_input = [int(x) for x in card_input]
    for i in range(1, len(card_input), 2):
        card_input[i] *= 2

        if card_input[i] > 9:
            card_input[i] = card_input[i] % 10 + 1

    total = sum(card_input)

    return total % 10 == 0


def get_staff(relative_path_to_db):
    """Returns a list of staff objects"""
    transfer_dict = {}
    staff_list = []
    try:
        db = shelve.open(f"{relative_path_to_db}/account/staff/staff", 'c')
        if "staff" in db:
            transfer_dict = db['staff']
        else:
            db['staff'] = transfer_dict
    except IOError:
        print("Error occurred while trying to open the shelve file - get staff function")
    except Exception as ex:
        print(f"Error occurred as {ex} - get staff function")
    for staff in transfer_dict.values():
        staff_list.append(staff)
    return staff_list


def store_staff(staff_object, relative_path_to_db):
    """Stores staff object inside the staff database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/account/staff/staff", 'c')
        if "staff" in db:
            transfer_dict = db['staff']
        else:
            db['staff'] = transfer_dict
        transfer_dict[staff_object.get_user_id()] = staff_object
        db['staff'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - store staff function")
    except Exception as ex:
        print(f"Error occurred as {ex} - store staff function")


def delete_staff(staff_object, relative_path_to_db):
    """Deletes customer object inside the customer database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/account/staff/staff", 'c')
        if "staff" in db:
            transfer_dict = db['staff']
        else:
            db['staff'] = transfer_dict
        transfer_dict.pop(staff_object.get_user_id(), None)
        db['staff'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file - delete Staff function")
    except Exception as ex:
        print(f"Error occurred as {ex} - delete Staff function")


def staff_login_authentication(username_email, password, relative_path_to_db):
    """Checks if staff login matches the database and returns a dictionary of the staff
    object """
    staff_dict = {}
    staff_list = get_staff(relative_path_to_db)
    for staff in staff_list:
        if staff.get_status() == 'active':
            if staff.get_email() == username_email or staff.get_username() == username_email:
                if checkpw(password.encode(), staff.get_password_hash()):
                    staff_dict = account_to_dictionary_converter(staff)
    return staff_dict


def add_mass_customer(number_of_customer_to_add, id_to_start):
    """Adds alot of customer"""
    for number in range(id_to_start, number_of_customer_to_add + id_to_start + 1):
        username = 'customer' + str(number)
        email = username + "@gmail.com"
        password = 'testtest'
        customer = Customer(username, email, password)
        store_customer(customer, "../../DB")


def add_mass_staff(number_of_staff_to_add, id_to_start):
    """Adds alot of staff"""
    for number in range(id_to_start, number_of_staff_to_add + id_to_start + 1):
        username = 'staff' + str(number)
        email = username + "@gmail.com"
        password = 'testtest'
        staff = Staff(username, email, password)
        store_staff(staff, "../../DB")


def validate_birthday_(birthday_to_validate):
    if birthday_to_validate > datetime.datetime.now().date():
        return False
    else:
        return True
