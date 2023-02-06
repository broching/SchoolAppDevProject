import shelve
from flask import redirect, url_for, session, flash
from bcrypt import checkpw


def customer_login_required():
    """Returns True if customer is logged in"""
    if 'customer' in session:
        return True
    else:
        return False


def staff_login_required():
    """Returns True if staff is logged in"""
    if 'staff' in session:
        return True
    else:
        return False


def restricted_customer_error():
    """Flashes error message and redirects account to the login page"""
    flash("Please log in to your account first to access this page", category='danger')
    return redirect(url_for('auth.customer_login'))


def restricted_staff_error():
    """Flashes error message and redirects account to the login page"""
    flash("Please log in to your account first to access this page", category='danger')
    return redirect(url_for('auth.staff_login'))


def validate_username(username_to_validate, relative_path_to_db, exceptions=None):
    """Return True if username is not taken, False if username is taken"""
    is_valid = True
    username_list = []
    customer_list = get_customers(relative_path_to_db)
    for customer in customer_list:
        username_list.append(customer.get_username())
    if exceptions:
        username_list.remove(exceptions)
    for username in username_list:
        if username == username_to_validate:
            is_valid = False
    return is_valid


def validate_password(password_to_validate):
    """Validates password with session"""
    return checkpw(password_to_validate.encode(), session['customer']['_Account__password_hash'])


def validate_email(email_to_validate, relative_path_to_db, exceptions=None):
    """Return True if email is not taken, False if email is taken"""
    is_valid = True
    email_list = []
    customer_list = get_customers(relative_path_to_db)
    for customer in customer_list:
        email_list.append(customer.get_email())
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
    for customer in customer_list:
        number_list.append(customer.get_number())
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
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")
    for customer in transfer_dict.values():
        customer_list.append(customer)
    print(transfer_dict.values())
    print(customer_list)
    return customer_list


def store_customer(customer_object, relative_path_to_db):
    """Stores customer object inside the customer database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/account/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
            print('The transfer dict before storing:', transfer_dict)
        else:
            db['customer'] = transfer_dict
        transfer_dict[customer_object.get_user_id()] = customer_object
        print('The transfer dict after storing:', transfer_dict)
        db['customer'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")


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
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")


def customer_login_authentication(username_email, password, relative_path_to_db):
    """Checks if customer login matches the database and returns valid (T or F) and a dictionary of the customer
    object """
    customer_dict = {}
    customers = get_customers(relative_path_to_db)
    for customer in customers:
        if customer.get_email() == username_email or customer.get_username() == username_email:
            if checkpw(password.encode(), customer.get_password_hash()):
                customer_dict = account_to_dictionary_converter(customer)
    return customer_dict


def account_to_dictionary_converter(account_object):
    account_dict = vars(account_object)
    return account_dict


def is_valid_card_number(card_input):
    card_input = card_input[::- 1]
    card_input = [int(x) for x in card_input]
    for i in range(1, len(card_input), 2):
        card_input[i] *= 2

        if card_input[i] > 9:
            card_input[i] = card_input[i] % 10 + 1

    total = sum(card_input)

    return total % 10 == 0


def store_credit_card(credit_card_object, relative_path_to_db):
    """Stores credit card object inside the credit card database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/credit_cards/credit_card", 'c')
        if "credit_card" in db:
            transfer_dict = db['credit_card']
            print('The transfer dict before storing:', transfer_dict)
        else:
            db['credit_card'] = transfer_dict
        transfer_dict[credit_card_object.get_card_id()] = credit_card_object
        print(credit_card_object.get_card_id())
        print(credit_card_object)
        print(transfer_dict)
        db['credit_card'] = transfer_dict
        print(db['credit_card'])
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")
