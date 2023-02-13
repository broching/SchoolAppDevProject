import secrets
import shelve

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from models.account.account_classes import Customer, Staff
from models.account.account_forms import UpdateProfileForm, UpdateSecurityForm, DeleteAccountForm, ShippingAddressForm, \
    AddNewAccountForm
from models.account.account_functions import save_image, delete_image
from models.auth.auth_functions import customer_login_required, validate_staff_password, staff_login_required, \
    validate_birthday_
from models.auth.auth_functions import get_customers, store_customer, delete_customer, account_to_dictionary_converter, \
    validate_customer_password, validate_number, validate_email, validate_username, is_valid_card_number, get_staff, \
    store_staff, \
    delete_staff
from models.auth.payment_classes import CreditCard
from models.auth.payment_forms import ProfileCreditCardForm, DeleteCreditCardForm, MakeCardDefaultForm

account = Blueprint('account', __name__)


@account.route('/customerProfile', methods=["POST", "GET"])
@customer_login_required
def customer_profile():
    # Code for the update profile page
    error_messages = {}
    update_profile_form = UpdateProfileForm()
    update_shipping_form = ShippingAddressForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']

    #  If User is submitting form

    if request.method == 'POST' and update_profile_form.submit1.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                customer.set_first_name(update_profile_form.first_name.data)
                customer.set_last_name(update_profile_form.last_name.data)
                if validate_username(update_profile_form.username.data, 'DB',
                                     exceptions=session['customer']['_Account__username']):
                    customer.set_username(update_profile_form.username.data)
                else:
                    error_messages['username'] = "The username is already taken"
                if validate_email(update_profile_form.email.data, 'DB',
                                  exceptions=session['customer']['_Account__email']):
                    customer.set_email(update_profile_form.email.data)
                else:
                    error_messages['email'] = "The email is already taken"
                if update_profile_form.phone_number.data:
                    if str(update_profile_form.phone_number.data).isdigit() and validate_number(
                            update_profile_form.phone_number.data, 'DB',
                            exceptions=session['customer']['_Account__number']):
                        customer.set_number(update_profile_form.phone_number.data)
                    else:
                        error_messages['number'] = "Invalid phone number"
                if update_profile_form.birthday.data:
                    if validate_birthday_(update_profile_form.birthday.data):
                        customer.set_birthday(update_profile_form.birthday.data.strftime('%Y-%m-%d'))
                    else:
                        error_messages['birthday'] = 'Invalid Birthday'
                if update_profile_form.image.data:
                    delete_image(session['customer']['_Account__user_image'])
                    image_file_name = save_image(update_profile_form.image.data)
                    customer.set_user_image(image_file_name)
                #     Store in DB
                store_customer(customer, 'DB')
                # Update session with new info
                customer_dict = account_to_dictionary_converter(customer)
                session['customer'] = customer_dict
                # flash and redirect
                if not error_messages:
                    flash('Account Successfully changed', category='success')
                    return redirect(url_for('account.customer_profile'))
            # If request method is get, load customer data to the update form fields
    if request.method == 'GET':
        update_profile_form.username.data = session['customer']['_Account__username']
        update_profile_form.first_name.data = session['customer']['_Account__first_name']
        update_profile_form.last_name.data = session['customer']['_Account__last_name']
        update_profile_form.email.data = session['customer']['_Account__email']
        update_profile_form.phone_number.data = session['customer']['_Account__number']

    # Check if user is logged in and renders template
    return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                           update_shipping_form=update_shipping_form, error_messages=error_messages)


@account.route('/customerSecurity', methods=["POST", "GET"])
@customer_login_required
def customer_security():
    # Code for the update security page

    error_messages = {}
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']

    #  If User is submitting form

    if request.method == 'POST' and update_security_form.submit2.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                if validate_customer_password(update_security_form.current_password.data):
                    if update_security_form.password1.data == update_security_form.password2.data:
                        customer.set_password_hash(update_security_form.password1.data)
                        #     Store in DB
                        delete_customer(customer, 'DB')
                        store_customer(customer, 'DB')
                        # Update session with new info
                        customer_dict = account_to_dictionary_converter(customer)
                        session['customer'] = customer_dict
                    else:
                        error_messages['password'] = 'Passwords do not match'
                else:
                    error_messages['current_password'] = 'Current password is wrong'
                # flash and redirect
                if not error_messages:
                    flash('Account Successfully changed', category='success')
                    return redirect(url_for('account.customer_security'))
    # Check if user is logged in and renders template
    return render_template('account/customer_security.html',
                           update_security_form=update_security_form, delete_account_form=delete_account_form,
                           error_messages=error_messages)


@account.route('/CustomerShipping', methods=['POST', 'GET'])
@customer_login_required
def customer_shipping_address():
    """Code for changing customer shipping address"""
    error_messages = {}
    update_profile_form = UpdateProfileForm()
    update_shipping_form = ShippingAddressForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']
    if request.method == 'POST' and update_shipping_form.submit4.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                if len(str(update_shipping_form.postal.data)) != 6:
                    error_messages['postal'] = 'Invalid Postal code'
                if error_messages == {}:
                    shipping_dict = {}
                    street_address = update_shipping_form.street_address.data
                    country = update_shipping_form.country.data
                    postal = update_shipping_form.postal.data
                    shipping_dict['street_address'] = street_address
                    shipping_dict['country'] = country
                    shipping_dict['postal'] = postal
                    customer.set_shipping_address(shipping_dict)

                    store_customer(customer, 'DB')
                    # Update session with new info
                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

                    flash("Shipping address successfully Changed", category='success')
                    return redirect(url_for('account.customer_profile'))

        # Check if user is logged in and renders template
        render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                        update_shipping_form=update_shipping_form, error_messages=error_messages)


@account.route('/customerDelete', methods=['POST', 'GET'])
@customer_login_required
def customer_delete():
    """Code for deleted customer account"""
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']
    if request.method == 'POST' and delete_account_form.submit3.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                customer.set_status("deactivated")
                store_customer(customer, "DB")

                session.pop('customer', None)
                flash("Account successfully deleted", category='info')
                return redirect(url_for('home'))
    # Check if user is logged in and renders template
    return render_template('account/customer_profile.html',
                           update_security_form=update_security_form, delete_account_form=delete_account_form, )


@account.route('/CustomerBilling//')
@customer_login_required
def customer_billing():
    delete_card_form = DeleteCreditCardForm()
    default_card_form = MakeCardDefaultForm()
    current_customer_id = session['customer']['_Account__user_id']
    customer_list = get_customers('DB')
    credit_card_list = session['customer']['_Customer__payment_details']
    if request.method == "GET":
        if len(credit_card_list) == 1:
            target_card = credit_card_list[0]
            card_default = True
            card_cvv = target_card['_CreditCard__card_cvv']
            card_expiry = target_card['_CreditCard__card_expiry']
            card_id = target_card['_CreditCard__card_id']
            card_name = target_card['_CreditCard__card_name']
            card_number = target_card['_CreditCard__card_number']
            street_address = target_card['_CreditCard__street_address']
            country = target_card['_CreditCard__country']
            postal = target_card['_CreditCard__postal']
            new_card = CreditCard(card_id, card_number, card_name, card_cvv, card_expiry, street_address, country,
                                  postal, card_default=card_default)
            for customer in customer_list:
                if customer.get_user_id() == current_customer_id:
                    credit_card_list[0] = account_to_dictionary_converter(new_card)
                    customer.set_payment_details(credit_card_list)
                    store_customer(customer, "DB")

                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

    return render_template('account/customer_billing.html', credit_card_list=credit_card_list,
                           delete_card_form=delete_card_form, default_card_form=default_card_form)


@account.route('/AddCard', methods=['POST', 'GET'])
@customer_login_required
def customer_add_card():
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']

    error_messages = {}
    profile_credit_card_form = ProfileCreditCardForm()
    if request.method == "POST" and profile_credit_card_form.submit.data:
        if not str(profile_credit_card_form.card_number.data).isdigit():
            error_messages['card_number'] = 'Please enter a numeric card number'
        else:
            if not is_valid_card_number(str(profile_credit_card_form.card_number.data)):
                error_messages['card_number'] = 'Please enter a valid card number'
        if not profile_credit_card_form.card_holder.data.replace(' ', "").isalpha():
            error_messages['card_holder'] = 'Please enter a valid name'
        if len(str(profile_credit_card_form.cvv.data)) != 3 and str(profile_credit_card_form.cvv.data).isdigit():
            error_messages['cvv'] = 'Invalid CVV'
        card_expiry = str(profile_credit_card_form.expiration_month.data) + str(
            profile_credit_card_form.expiration_year.data)
        if len(str(profile_credit_card_form.postal.data)) != 6 and str(profile_credit_card_form.postal.data).isdigit():
            error_messages['postal'] = 'Invalid Postal code'
        if error_messages == {}:
            credit_card = CreditCard(secrets.token_hex(15), profile_credit_card_form.card_number.data,
                                     profile_credit_card_form.card_holder.data, profile_credit_card_form.cvv.data,
                                     card_expiry, profile_credit_card_form.street_address.data,
                                     profile_credit_card_form.country.data,
                                     profile_credit_card_form.postal.data)
            for customer in customer_list:
                if customer.get_user_id() == current_customer_id:
                    customer_credit_cards = customer.get_payment_details()
                    customer_credit_cards.append(account_to_dictionary_converter(credit_card))
                    customer.set_payment_details(customer_credit_cards)
                    store_customer(customer, "DB")

                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

                    flash('Credit Card Successfully added', category='success')
                    return redirect(url_for('account.customer_billing'))

    return render_template('account/customer_add_card.html', profile_credit_card_form=profile_credit_card_form,
                           error_messages=error_messages)


@account.route('/EditCard/<card_id>', methods=['POST', 'GET'])
@customer_login_required
def customer_edit_card(card_id):
    current_customer_id = session['customer']['_Account__user_id']
    customer_list = get_customers('DB')
    error_messages = {}
    profile_credit_card_form = ProfileCreditCardForm()
    if request.method == "POST" and profile_credit_card_form.submit.data:
        if not str(profile_credit_card_form.card_number.data).isdigit():
            error_messages['card_number'] = 'Please enter a numeric card number'
        else:
            if not is_valid_card_number(str(profile_credit_card_form.card_number.data)):
                error_messages['card_number'] = 'Please enter a valid card number'
        if not profile_credit_card_form.card_holder.data.replace(' ', "").isalpha():
            error_messages['card_holder'] = 'Please enter a valid name'
        if len(str(profile_credit_card_form.cvv.data)) != 3 and str(profile_credit_card_form.cvv.data).isdigit():
            error_messages['cvv'] = 'Invalid CVV'
        card_expiry = str(profile_credit_card_form.expiration_month.data) + str(
            profile_credit_card_form.expiration_year.data)
        if len(str(profile_credit_card_form.postal.data)) != 6 and str(profile_credit_card_form.postal.data).isdigit():
            error_messages['postal'] = 'Invalid Postal code'
        if error_messages == {}:
            credit_card = CreditCard(secrets.token_hex(15), profile_credit_card_form.card_number.data,
                                     profile_credit_card_form.card_holder.data, profile_credit_card_form.cvv.data,
                                     card_expiry, profile_credit_card_form.street_address.data,
                                     profile_credit_card_form.country.data,
                                     profile_credit_card_form.postal.data)
            for customer in customer_list:
                if customer.get_user_id() == current_customer_id:
                    credit_card_list = customer.get_payment_details()
                    for card in credit_card_list:
                        customer_card_id = card['_CreditCard__card_id']
                        if customer_card_id == card_id:
                            index = credit_card_list.index(card)
                            credit_card_list[index] = account_to_dictionary_converter(credit_card)
                            customer.set_payment_details(credit_card_list)
                            store_customer(customer, "DB")

                            customer_dict = account_to_dictionary_converter(customer)
                            session['customer'] = customer_dict

                            flash('Credit Card Successfully Changed', category='success')
                            return redirect(url_for('account.customer_billing'))
    if request.method == 'GET':
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                credit_card_list = customer.get_payment_details()
                for card in credit_card_list:
                    customer_card_id = card['_CreditCard__card_id']
                    if customer_card_id == card_id:
                        profile_credit_card_form.card_number.data = card['_CreditCard__card_number']
                        profile_credit_card_form.card_holder.data = card['_CreditCard__card_name']
                        expiration_month = card['_CreditCard__card_expiry'][0] + \
                                           card['_CreditCard__card_expiry'][1]
                        expiration_year = card['_CreditCard__card_expiry'][2] + \
                                          card['_CreditCard__card_expiry'][3]
                        profile_credit_card_form.expiration_month.data = expiration_month
                        profile_credit_card_form.expiration_month.data = expiration_year
                        profile_credit_card_form.cvv.data = card['_CreditCard__card_cvv']
                        profile_credit_card_form.street_address.data = card['_CreditCard__street_address']
                        profile_credit_card_form.country.data = card['_CreditCard__country']
                        profile_credit_card_form.postal.data = card['_CreditCard__postal']

    return render_template('account/customer_edit_card.html', profile_credit_card_form=profile_credit_card_form,
                           error_messages=error_messages)


@account.route('/DeleteCard/<card_id>', methods=['POST', 'GET'])
@customer_login_required
def customer_delete_card(card_id):
    current_customer_id = session['customer']['_Account__user_id']
    customer_list = get_customers('DB')
    delete_card_form = DeleteCreditCardForm()
    if request.method == "POST" and delete_card_form.submit.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                credit_card_list = customer.get_payment_details()
                for card in credit_card_list:
                    customer_card_id = card['_CreditCard__card_id']
                    if customer_card_id == card_id:
                        index = credit_card_list.index(card)
                        del credit_card_list[index]
                        customer.set_payment_details(credit_card_list)
                        store_customer(customer, "DB")

                        customer_dict = account_to_dictionary_converter(customer)
                        session['customer'] = customer_dict

                        flash('Credit Card Successfully Deleted', category='success')
                        return redirect(url_for('account.customer_billing'))

    return render_template('account/customer_billing.html', delete_card_form=delete_card_form)


@account.route('/DefaultCard/<card_id>', methods=['POST', 'GET'])
@customer_login_required
def customer_default_card(card_id):
    current_customer_id = session['customer']['_Account__user_id']
    customer_list = get_customers('DB')
    default_card_form = MakeCardDefaultForm()
    if request.method == "POST" and default_card_form.submit.data:

        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                new_credit_card_list = []
                credit_card_list = customer.get_payment_details()
                for card in credit_card_list:
                    credit_card_id = card['_CreditCard__card_id']
                    card_number = card['_CreditCard__card_number']
                    card_name = card['_CreditCard__card_name']
                    card_cvv = card['_CreditCard__card_cvv']
                    card_expiry = card['_CreditCard__card_expiry']
                    street_address = card['_CreditCard__street_address']
                    country = card['_CreditCard__country']
                    postal = card['_CreditCard__postal']
                    card_default = False
                    new_card = CreditCard(credit_card_id, card_number, card_name, card_cvv, card_expiry, street_address,
                                          country, postal, card_default=card_default)
                    new_credit_card_list.append(account_to_dictionary_converter(new_card))

                    customer.set_payment_details(new_credit_card_list)
                    store_customer(customer, "DB")

                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                new_credit_card_list = []
                credit_card_list = customer.get_payment_details()
                for card in credit_card_list:
                    if card['_CreditCard__card_id'] == card_id:
                        credit_card_id = card['_CreditCard__card_id']
                        card_number = card['_CreditCard__card_number']
                        card_name = card['_CreditCard__card_name']
                        card_cvv = card['_CreditCard__card_cvv']
                        card_expiry = card['_CreditCard__card_expiry']
                        street_address = card['_CreditCard__street_address']
                        country = card['_CreditCard__country']
                        postal = card['_CreditCard__postal']
                        card_default = True
                        new_card = CreditCard(credit_card_id, card_number, card_name, card_cvv, card_expiry,
                                              street_address, country, postal, card_default=card_default)

                        index = credit_card_list.index(card)
                        new_credit_card_list = credit_card_list
                        new_credit_card_list[index] = account_to_dictionary_converter(new_card)
                        customer.set_payment_details(new_credit_card_list)
                        store_customer(customer, "DB")

                        customer_dict = account_to_dictionary_converter(customer)
                        session['customer'] = customer_dict

                        flash(f'Credit Card {card_name} has been set to Default', category='success')
                        return redirect(url_for('account.customer_billing'))

                print(new_credit_card_list)

    return render_template('account/customer_billing.html', default_card_form=default_card_form,
                           )


@account.route('/StaffDashboard')
@staff_login_required
def staff_dashboard():
    appt_list = []
    try:
        appt_dict = {}
        with shelve.open('DB/service/service.db', 'r') as db:
            if 'service' in db:
                appt_dict = db['service']
            for key in appt_dict:
                service = appt_dict.get(key)
                appt_list.append(service)
    except IOError as ex:
        print(f"Error in retrieving products from service.db (inventory route)- {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from service.db - {ex}")
    upcoming_appointments = len(appt_list)
    account_list = get_customers('DB') + get_staff('DB')
    print(appt_list)

    product_list = []
    product_dict = {}
    totalProfits = 0
    try:
        totalProfits = 0
        with shelve.open('DB/products/product.db', 'c') as pdb:
            if 'Products' in pdb:
                product_dict = pdb['Products']
            for key in product_dict:
                product = product_dict.get(key)
                product_list.append(product)
                profits = product.get_product_profitTotal()
                totalProfits += profits

            pdb['Products'] = product_dict

            numProducts = len(product_list) if product_list else 0

    except IOError as ex:
        print(f"E(staff_dashboard) Error while trying to open product.db - {ex}")

    return render_template('account/staff_dashboard.html', account_list=account_list, account_count=len(account_list),
                           upcoming_appointments=upcoming_appointments, product_list=product_list,
                           numProducts=numProducts, totalProfits=totalProfits)


@account.route('/StaffProfile', methods=["POST", "GET"])
@staff_login_required
def staff_profile():
    # Code for the update profile page
    error_messages = {}
    update_profile_form = UpdateProfileForm()
    staff_list = get_staff('DB')
    current_staff_id = session['staff']['_Account__user_id']

    #  If User is submitting form

    if request.method == 'POST' and update_profile_form.submit1.data:
        for staff in staff_list:
            if staff.get_user_id() == current_staff_id:
                staff.set_first_name(update_profile_form.first_name.data)
                staff.set_last_name(update_profile_form.last_name.data)
                if validate_username(update_profile_form.username.data, 'DB',
                                     exceptions=session['staff']['_Account__username']):
                    staff.set_username(update_profile_form.username.data)
                else:
                    error_messages['username'] = "The username is already taken"
                if validate_email(update_profile_form.email.data, 'DB',
                                  exceptions=session['staff']['_Account__email']):
                    staff.set_email(update_profile_form.email.data)
                else:
                    error_messages['email'] = "The email is already taken"
                if update_profile_form.phone_number.data:
                    if str(update_profile_form.phone_number.data).isdigit() and validate_number(
                            update_profile_form.phone_number.data, 'DB',
                            exceptions=session['staff']['_Account__number']):
                        staff.set_number(update_profile_form.phone_number.data)
                    else:
                        error_messages['number'] = "Invalid phone number"
                if update_profile_form.birthday.data:
                    if validate_birthday_(update_profile_form.birthday.data):
                        staff.set_birthday(update_profile_form.birthday.data.strftime('%Y-%m-%d'))
                    else:
                        error_messages['birthday'] = 'Invalid Birthday'
                if update_profile_form.image.data:
                    delete_image(session['staff']['_Account__user_image'])
                    image_file_name = save_image(update_profile_form.image.data)
                    staff.set_user_image(image_file_name)
                #     Store in DB
                store_staff(staff, 'DB')
                # Update session with new info
                staff_dict = account_to_dictionary_converter(staff)
                session['staff'] = staff_dict
                # flash and redirect
                if not error_messages:
                    flash('Staff Account Successfully changed', category='success')
                    return redirect(url_for('account.staff_profile'))
            # If request method is get, load customer data to the update form fields
    if request.method == 'GET':
        update_profile_form.username.data = session['staff']['_Account__username']
        update_profile_form.first_name.data = session['staff']['_Account__first_name']
        update_profile_form.last_name.data = session['staff']['_Account__last_name']
        update_profile_form.email.data = session['staff']['_Account__email']
        update_profile_form.phone_number.data = session['staff']['_Account__number']
    return render_template('account/staff_profile.html', update_profile_form=update_profile_form,
                           error_messages=error_messages)


@account.route('/StaffSecurity', methods=["POST", "GET"])
@staff_login_required
def staff_security():
    # Code for the update security page

    error_messages = {}
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    staff_list = get_staff('DB')
    current_staff_id = session['staff']['_Account__user_id']

    #  If User is submitting form

    if request.method == 'POST' and update_security_form.submit2.data:
        for staff in staff_list:
            if staff.get_user_id() == current_staff_id:
                if validate_staff_password(update_security_form.current_password.data):
                    if update_security_form.password1.data == update_security_form.password2.data:
                        staff.set_password_hash(update_security_form.password1.data)
                        #     Store in DB
                        delete_staff(staff, 'DB')
                        store_staff(staff, 'DB')
                        # Update session with new info
                        staff_dict = account_to_dictionary_converter(staff)
                        session['staff'] = staff_dict
                    else:
                        error_messages['password'] = 'Passwords do not match'
                else:
                    error_messages['current_password'] = 'Current password is wrong'
                # flash and redirect
                if not error_messages:
                    flash('Staff Account Successfully changed', category='success')
                    return redirect(url_for('account.staff_security'))
    # Check if user is logged in and renders template
    return render_template('account/staff_security.html',
                           update_security_form=update_security_form, delete_account_form=delete_account_form,
                           error_messages=error_messages)


@account.route('/StaffDelete', methods=['POST', 'GET'])
@staff_login_required
def staff_delete():
    """Code for deleted customer account"""
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    staff_list = get_staff('DB')
    current_staff_id = session['staff']['_Account__user_id']
    if request.method == 'POST' and delete_account_form.submit3.data:
        for staff in staff_list:
            if staff.get_user_id() == current_staff_id:
                staff.set_status("deactivated")
                store_staff(staff, "DB")
                session.pop('staff', None)
                flash("Staff Account successfully deleted", category='info')
                return redirect(url_for('home'))
    return render_template('account/staff_security.html',
                           update_security_form=update_security_form, delete_account_form=delete_account_form, )


@account.route('/AccountManagement', methods=['POST', 'GET'])
@staff_login_required
def staff_account_management():
    delete_account_form = DeleteAccountForm()
    customer_list = []
    staff_list = []
    account_list = get_customers('DB') + get_staff('DB')
    for customer in get_customers('DB'):
        if customer.get_status() == 'active':
            customer_list.append(customer)
    for staff in get_staff('DB'):
        if staff.get_status() == 'active':
            staff_list.append(staff)
    new_account_list = customer_list + staff_list
    account_count = len(new_account_list)
    staff_count = len(staff_list)
    customer_count = len(customer_list)
    deactivated_count = (len(get_staff('DB')) + len(get_customers('DB'))) - account_count
    if request.method == "GET":
        customer_list = []
        staff_list = []
        for customer in get_customers('DB'):
            if customer.get_status() == 'active':
                customer_list.append(customer)
        for staff in get_staff('DB'):
            if staff.get_status() == 'active':
                staff_list.append(staff)
        new_account_list = customer_list + staff_list
        account_count = len(new_account_list)
        staff_count = len(staff_list)
        customer_count = len(customer_list)
        deactivated_count = len(account_list) - account_count

    return render_template('account/account_management.html', account_list=account_list,
                           delete_account_form=delete_account_form, account_count=account_count,
                           customer_count=customer_count, staff_count=staff_count, deactivated_count=deactivated_count)


@account.route('/StaffAccountDelete/<user_id>', methods=['POST', 'GET'])
@staff_login_required
def staff_account_management_delete(user_id):
    delete_account_form = DeleteAccountForm()
    account_list = get_customers("DB") + get_staff("DB")
    if request.method == 'POST' and delete_account_form.submit3.data:
        for user in account_list:
            if str(user.get_user_id()) == str(user_id):
                if user.get_account_type() == 'customer':
                    delete_image(user.get_user_image())
                    delete_customer(user, "DB")
                else:
                    delete_image(user.get_user_image())
                    delete_staff(user, "DB")
                flash(f'Account {user.get_username()} successfully deleted', category='info')
                return redirect(url_for('account.staff_account_management'))
    return render_template('account/account_management.html', account_list=account_list,
                           delete_account_form=delete_account_form)


@account.route('/StaffAddAccount', methods=['POST', 'GET'])
@staff_login_required
def staff_add_account():
    error_messages = {}
    add_account_form = AddNewAccountForm()

    #  If User is submitting form

    if request.method == 'POST' and add_account_form.submit1.data:
        if not validate_username(add_account_form.username.data, 'DB', ):
            error_messages['username'] = "The username is already taken"
        if not validate_email(add_account_form.email.data, 'DB', ):
            error_messages['email'] = "The email is already taken"
        if add_account_form.phone_number.data:
            if str(add_account_form.phone_number.data).isdigit() and validate_number(
                    add_account_form.phone_number.data, 'DB',
                    exceptions=session['customer']['_Account__number']):
                pass
            else:
                error_messages['number'] = "Invalid phone number"
        if error_messages == {}:
            if add_account_form.account_type.data == 'customer':
                customer = Customer(add_account_form.username.data, add_account_form.email.data,
                                    add_account_form.password1.data)
                customer.set_account_type('customer')
                customer.set_status(add_account_form.status.data)
                customer.set_first_name(add_account_form.first_name.data)
                customer.set_last_name(add_account_form.last_name.data)
                customer.set_number(add_account_form.phone_number.data)
                #     Store in DB
                store_customer(customer, 'DB')
            else:
                staff = Staff(add_account_form.username.data, add_account_form.email.data,
                              add_account_form.password1.data)
                staff.set_account_type('staff')
                staff.set_status(add_account_form.status.data)
                staff.set_first_name(add_account_form.first_name.data)
                staff.set_last_name(add_account_form.last_name.data)
                staff.set_number(add_account_form.phone_number.data)
                #     Store in DB
                store_staff(staff, 'DB')
            # flash and redirect
            flash(f'Account {add_account_form.username.data} Successfully Added', category='success')
            return redirect(url_for('account.staff_account_management'))
    return render_template('account/staff_add_account.html', add_account_form=add_account_form,
                           error_messages=error_messages)


@account.route('/StaffEditAccount/<user_id>', methods=['POST', 'GET'])
def staff_edit_account(user_id):
    error_messages = {}
    add_account_form = AddNewAccountForm()
    user_list = get_customers("DB") + get_staff("DB")

    #  If User is submitting form

    if request.method == 'POST' and add_account_form.submit1.data:
        for target_user in user_list:
            if str(target_user.get_user_id()) == str(user_id):
                username = target_user.get_username()
                email = target_user.get_email()
                number = target_user.get_number()
                if validate_username(add_account_form.username.data, 'DB', exceptions=username):
                    target_user.set_username(add_account_form.username.data)
                else:
                    error_messages['username'] = "The username is already taken"
                if validate_email(add_account_form.email.data, 'DB', exceptions=email):
                    target_user.set_email(add_account_form.email.data)
                else:
                    error_messages['email'] = "The email is already taken"
                if add_account_form.phone_number.data:
                    if str(add_account_form.phone_number.data).isdigit() and validate_number(
                            add_account_form.phone_number.data, 'DB', exceptions=number):
                        target_user.set_number(add_account_form.phone_number.data)
                    else:
                        error_messages['number'] = "The phone number is already taken"
                if error_messages == {}:
                    target_user.set_password_hash(add_account_form.password1.data)
                    target_user.set_status(add_account_form.status.data)
                    target_user.set_first_name(add_account_form.first_name.data)
                    target_user.set_last_name(add_account_form.last_name.data)
                    #     Store in DB
                    if target_user.get_account_type() == 'customer':
                        store_customer(target_user, "DB")
                    else:
                        store_staff(target_user, "DB")
                    # flash and redirect
                    flash(f'Account {target_user.get_username()} Successfully Edited', category='success')
                    return redirect(url_for('account.staff_account_management'))
    if request.method == "GET":
        for target_user in user_list:
            if str(target_user.get_user_id()) == str(user_id):
                add_account_form.username.data = target_user.get_username()
                add_account_form.first_name.data = target_user.get_first_name()
                add_account_form.last_name.data = target_user.get_last_name()
                add_account_form.email.data = target_user.get_email()
                add_account_form.phone_number.data = target_user.get_number()
                add_account_form.password1.data = target_user.get_password_hash()
                add_account_form.status.data = target_user.get_status()

    return render_template('account/staff_edit_account.html', add_account_form=add_account_form,
                           error_messages=error_messages)
