import secrets

from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from models.account.account_forms import UpdateProfileForm, UpdateSecurityForm, DeleteAccountForm
from models.account.account_functions import save_image, delete_image
from models.auth.auth_functions import customer_login_required, restricted_customer_error, staff_login_required, \
    restricted_staff_error
from models.auth.auth_functions import get_customers, store_customer, delete_customer, account_to_dictionary_converter, \
    validate_password, validate_number, validate_email, validate_username, is_valid_card_number
from models.auth.payment_classes import CreditCard
from models.auth.payment_forms import ProfileCreditCardForm, DeleteCreditCardForm, MakeCardDefaultForm

account = Blueprint('account', __name__)


@account.route('/CustomerDashboard')
def customer_dashboard():
    if customer_login_required():
        return render_template('account/customer_dashboard.html')
    else:
        return restricted_customer_error()


@account.route('/StaffDashboard')
def staff_dashboard():
    if staff_login_required():
        return render_template('account/staff_dashboard.html')
    else:
        return restricted_staff_error()


@account.route('/customerProfile', methods=["POST", "GET"])
def customer_profile():
    # Code for the update profile page
    error_messages = {}
    update_profile_form = UpdateProfileForm()
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
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
                    if validate_number(update_profile_form.phone_number.data, 'DB',
                                       exceptions=session['customer']['_Account__number']):
                        customer.set_number(update_profile_form.phone_number.data)
                    else:
                        error_messages['number'] = "The phone number is already taken"
                if update_profile_form.birthday.data:
                    customer.set_birthday(update_profile_form.birthday.data.strftime('%Y-%m-%d'))
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
                    return redirect(url_for('account.customer_dashboard'))
            # If request method is get, load customer data to the update form fields
    if request.method == 'GET':
        update_profile_form.username.data = session['customer']['_Account__username']
        update_profile_form.first_name.data = session['customer']['_Account__first_name']
        update_profile_form.last_name.data = session['customer']['_Account__last_name']
        update_profile_form.email.data = session['customer']['_Account__email']
        update_profile_form.phone_number.data = session['customer']['_Account__number']

    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form,
                               error_messages=error_messages)
    else:
        return restricted_customer_error()


@account.route('/customerSecurity', methods=["POST", "GET"])
def customer_security():
    # Code for the update security page

    error_messages = {}
    update_profile_form = UpdateProfileForm()
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']

    #  If User is submitting form

    if request.method == 'POST' and update_security_form.submit2.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                if validate_password(update_security_form.current_password.data):
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
                    return redirect(url_for('account.customer_dashboard'))
    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form,
                               error_messages=error_messages)
    else:
        return restricted_customer_error()


@account.route('/customerDelete', methods=['POST', 'GET'])
def customer_delete():
    """Code for deleted customer account"""
    update_profile_form = UpdateProfileForm()
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']
    if request.method == 'POST' and delete_account_form.submit3.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                delete_image(session['customer']['_Account__user_image'])
                delete_customer(customer, 'DB')
                session.pop('customer', None)
                flash("Account successfully deleted", category='info')
                return redirect(url_for('home'))
    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form)
    else:
        return restricted_customer_error()


@account.route('/CustomerBilling//')
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
            new_card = CreditCard(card_id, card_number, card_name, card_cvv, card_expiry, card_default=card_default)
            for customer in customer_list:
                if customer.get_user_id() == current_customer_id:
                    credit_card_list[0] = account_to_dictionary_converter(new_card)
                    customer.set_payment_details(credit_card_list)
                    store_customer(customer, "DB")

                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

    if customer_login_required():
        return render_template('account/customer_billing.html', credit_card_list=credit_card_list,
                               delete_card_form=delete_card_form, default_card_form=default_card_form)
    else:
        return restricted_staff_error()


@account.route('/AddCard', methods=['POST', 'GET'])
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
        if error_messages == {}:
            credit_card = CreditCard(secrets.token_hex(15), profile_credit_card_form.card_number.data,
                                     profile_credit_card_form.card_holder.data, profile_credit_card_form.cvv.data,
                                     card_expiry)
            for customer in customer_list:
                if customer.get_user_id() == current_customer_id:
                    customer_credit_cards = customer.get_payment_details()
                    customer_credit_cards.append(account_to_dictionary_converter(credit_card))
                    customer.set_payment_details(customer_credit_cards)
                    store_customer(customer, "DB")

                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict
                    print('sesson dict')
                    print(session['customer'])

                    flash('Credit Card Successfully added', category='success')
                    return redirect(url_for('home'))

    return render_template('account/customer_add_card.html', profile_credit_card_form=profile_credit_card_form,
                           error_messages=error_messages)


@account.route('/EditCard/<card_id>', methods=['POST', 'GET'])
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
        if error_messages == {}:
            credit_card = CreditCard(secrets.token_hex(15), profile_credit_card_form.card_number.data,
                                     profile_credit_card_form.card_holder.data, profile_credit_card_form.cvv.data,
                                     card_expiry)
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
                            return redirect(url_for('home'))
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

    return render_template('account/customer_edit_card.html', profile_credit_card_form=profile_credit_card_form,
                           error_messages=error_messages)


@account.route('/DeleteCard/<card_id>', methods=['POST', 'GET'])
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
                    card_default = False
                    new_card = CreditCard(credit_card_id, card_number, card_name, card_cvv, card_expiry, card_default)
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
                        card_default = True
                        new_card = CreditCard(credit_card_id, card_number, card_name, card_cvv, card_expiry, card_default)

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


@account.route('/StaffProfile')
def staff_profile():
    if staff_login_required():
        return render_template('account/staff_profile.html')
    else:
        return restricted_staff_error()
