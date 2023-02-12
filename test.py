from main import app
from flask_mail import Message, Mail
from flask import url_for

mail = Mail(app)


def send_reset_email(user):
    token = user.get_reset_token(expires_secs=1800)
    msg = Message()
    msg.subject = "Password reset"
    msg.recipients = ['onesalonsg05@gmail.com']
    msg.sender = 'onesalonsg05@gmail.com'
    msg.body = f"""
To Reset Your Password, Vist the Following Link:

{url_for('auth.reset_password', token=token, _external=True)}

If you did not send a reset password request, simply ignore this email and have a nice day!
"""
    mail.send(msg)

def get_reset_token(self, expires_secs=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_secs)
    return s.dumps({'user_id': self.__user_id}).decode('utf-8')

@staticmethod
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return user_id
