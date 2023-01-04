from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from models.auth.auth_functions import customer_login_required, restricted_customer_error, staff_login_required, \
    restricted_staff_error

from models.account.account_forms import UpdateProfileForm, UpdateSecurityForm, DeleteAccountForm

from models.auth.auth_functions import get_customers, store_customer, delete_customer, account_to_dictionary_converter, \
    validate_password, validate_number, validate_email, validate_username

from models.account.account_functions import save_image, delete_image

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
    error_messages = []
    update_profile_form = UpdateProfileForm()
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']
    if request.method == 'POST' and update_profile_form.submit1.data:
        for customer in customer_list:
            if customer.get_user_id() == current_customer_id:
                customer.set_first_name(update_profile_form.first_name.data)
                customer.set_last_name(update_profile_form.last_name.data)
                if validate_username(update_profile_form.username.data, 'DB',
                                     exceptions=session['customer']['_Account__username']):
                    customer.set_username(update_profile_form.username.data)
                else:
                    error_messages.append("The username is already taken")
                if validate_email(update_profile_form.email.data, 'DB',
                                  exceptions=session['customer']['_Account__email']):
                    customer.set_email(update_profile_form.email.data)
                else:
                    error_messages.append("The email is already taken")
                if update_profile_form.phone_number.data:
                    if validate_number(update_profile_form.phone_number.data, 'DB',
                                       exceptions=session['customer']['_Account__number']):
                        customer.set_number(update_profile_form.phone_number.data)
                    else:
                        error_messages.append("The phone number is already taken")
                if update_profile_form.birthday.data:
                    customer.set_birthday(update_profile_form.birthday.data.strftime('%Y-%m-%d'))
                if update_profile_form.image.data:
                    delete_image(session['customer']['_Account__user_image'])
                    image_file_name = save_image(update_profile_form.image.data)
                    customer.set_user_image(image_file_name)
                #     Store in DB
                delete_customer(customer, 'DB')
                store_customer(customer, 'DB')
                # Update session with new info
                customer_dict = account_to_dictionary_converter(customer)
                session['customer'] = customer_dict
                # flash and redirect
                if error_messages:
                    for error in error_messages:
                        flash(error, category='danger')
                else:
                    flash('Account Successfully changed', category='success')
                    return redirect(url_for('account.customer_dashboard'))
    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form)
    else:
        return restricted_customer_error()


@account.route('/customerSecurity', methods=["POST", "GET"])
def customer_security():
    # Code for the update security page
    error_messages = []
    update_profile_form = UpdateProfileForm()
    update_security_form = UpdateSecurityForm()
    delete_account_form = DeleteAccountForm()
    customer_list = get_customers('DB')
    current_customer_id = session['customer']['_Account__user_id']
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
                        error_messages.append('Passwords do not match')
                else:
                    error_messages.append('Current password is wrong')
                # flash and redirect
                if error_messages:
                    for error in error_messages:
                        flash(error, category='danger')
                else:
                    flash('Account Successfully changed', category='success')
                    return redirect(url_for('account.customer_dashboard'))
    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form)
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
                print(True)
                session.pop('customer', None)
                flash("Account successfully deleted", category='info')
                return redirect(url_for('home'))
    # Check if user is logged in and renders template
    if customer_login_required():
        return render_template('account/customer_profile.html', update_profile_form=update_profile_form,
                               update_security_form=update_security_form, delete_account_form=delete_account_form)
    else:
        return restricted_customer_error()


@account.route('/StaffProfile')
def staff_profile():
    if staff_login_required():
        return render_template('account/staff_profile.html')
    else:
        return restricted_staff_error()
