from flask_mail import Mail, Message
from datetime import timedelta, datetime
from flask import Flask, render_template, flash, redirect, url_for, request, session
from models.message.message_functions import *
from models.message.message_classes import EmailMessage
from models.account.account_forms import ContactUsForm
from models.auth.auth_forms import NewPasswordForm, LoginForm, GetEmailForm
from models.auth.auth_functions import get_customers, store_customer, customer_login_authentication
from routes.services import service
from routes.auth import auth
from routes.account import account
from routes.review import review
from routes.products import productr
from routes.avatar import avatar_blueprint

import jwt

app = Flask(__name__)

# app config
app.config["SECRET_KEY"] = "641z69bc491f8cb891fc0417d2eb29bb5"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "onesalonsg05@gmail.com"
app.config['MAIL_PASSWORD'] = "ggyoqxoweuefqguz"

mail = Mail(app)

# registered blueprints to app
app.register_blueprint(auth)
app.register_blueprint(account)
app.register_blueprint(review)
app.register_blueprint(productr)
app.register_blueprint(service)
app.register_blueprint(avatar_blueprint)

# session config
app.permanent_session_lifetime = timedelta(days=15)


# starting route / home route
@app.route('/home')
@app.route('/')
def home():
    return render_template('home/home.html')


@app.route('/AboutUs')
def about_us():
    return render_template('home/about_us.html')


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def page_not_found_500(e):
    return render_template('error_pages/500.html'), 500


def send_reset_email(user_id, email):
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=1)},
                       key="user_id")
    msg = Message()
    msg.subject = "Password reset"
    msg.recipients = [email]
    msg.sender = 'onesalonsg05@gmail.com'
    msg.html = render_template('auth/reset_password_email.html', token=token)

    mail.send(msg)


def send_contact_email(email, subject, message):
    msg = Message()
    msg.subject = subject
    msg.recipients = [email]
    msg.sender = 'onesalonsg05@gmail.com'
    msg.body = message
    mail.send(msg)


@app.route('/ContactUs', methods=["POST", "GET"])
def contact_us():
    contact_us_form = ContactUsForm()
    if request.method == "POST" and contact_us_form.submit.data:
        message = EmailMessage(contact_us_form.email.data, contact_us_form.subject.data, contact_us_form.message.data)
        store_message(message, "DB")
        flash('Message successfully sent', category='success')
        return redirect(url_for('home'))
    return render_template('home/contact_us.html', contact_us_form=contact_us_form)


@app.route('/SendMessage/<email>/<subject>/<message>', methods=["POST", "GET"])
def send_email(email, subject, message):
    send_contact_email(email, subject, message)
    flash(f'Email sent successfully to {email}', category='success')
    return redirect(url_for('account.staff_messages'))


@app.route('/CustomerLogin', methods=["POST", "GET"])
def customer_login():
    login_form = LoginForm()
    get_email_form = GetEmailForm()
    if request.method == "POST" and login_form.submit.data:
        customer_dict = customer_login_authentication(login_form.username.data, login_form.password.data, 'DB')
        if customer_dict != {}:
            if login_form.remember.data:
                session.permanent = True
            else:
                session.permanent = False
            session['customer'] = customer_dict
            flash(f"Account {login_form.username.data} successfully logged in!", category="success")
            return redirect(url_for('home'))
        else:
            flash("Login failed! Please check your username or password again", category='danger')

    if request.method == "POST" and get_email_form.submit5.data:
        email = get_email_form.email.data
        for customer in get_customers('DB'):
            if customer.get_email() == email:
                print('account found')
                send_reset_email(customer.get_user_id(), email)
        flash('Email Successfully Sent, Please check your email', category='success')
    return render_template('auth/customer_login.html', form=login_form, get_email_form=get_email_form)


@app.route('/ResetPassword/<token>', methods=["POST", "GET"])
def reset_password(token):
    id_list = []
    error_messages = {}
    new_password_form = NewPasswordForm()
    try:
        user_id = jwt.decode(token, "user_id", algorithms=["HS256"])['user_id']
        for customer in get_customers('DB'):
            id_list.append(customer.get_user_id())
        if user_id not in id_list:
            flash('That is an expired or invalid password request, please send another password request email', category='warning')
            return redirect(url_for('customer_login'))
        else:
            if request.method == 'POST' and new_password_form.submit.data:
                if new_password_form.password1.data != new_password_form.password2.data:
                    error_messages['password'] = 'Passwords do not match'
                if error_messages == {}:
                    for accounts in get_customers('DB'):
                        if accounts.get_user_id() == int(user_id):
                            accounts.set_password_hash(new_password_form.password1.data)
                            store_customer(accounts, "DB")
                            flash('Password successfully changed', category='success')
                            return redirect(url_for('customer_login'))
    except jwt.ExpiredSignatureError:
        flash("The password reset request has been expired, please try again", category="warning")
        return redirect(url_for("home"))
    return render_template('auth/reset_password.html', new_password_form=new_password_form,
                           error_messages=error_messages)


if __name__ == "__main__":
    app.run(debug=True)
