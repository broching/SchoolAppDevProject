from datetime import datetime
from bcrypt import hashpw, gensalt


class Account:
    time = datetime.now()
    time = int(round(time.timestamp()))
    user_count = 0

    def __init__(self, username, email, password_hash):
        Account.user_count += 1
        self.__user_id = Account.time
        self.__username = username
        self.__email = email
        self.__password_hash = hashpw(password_hash.encode(), gensalt())
        self.__number = None
        self.__account_type = None
        self.__user_image = None
        self.__first_name = None
        self.__last_name = None
        self.__birthday = None

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_password_hash(self):
        return self.__password_hash

    def set_password_hash(self, password_hash):
        if password_hash:
            self.__password_hash = hashpw(password_hash.encode(), gensalt())

    def get_account_type(self):
        return self.__account_type

    def set_account_type(self, account_type):
        self.__account_type = account_type

    def get_user_image(self):
        return self.__user_image

    def set_user_image(self, img):
        self.__user_image = img

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_birthday(self):
        return self.__birthday

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def get_number(self):
        return self.__number

    def set_number(self, number):
        self.__number = number


class Customer(Account):
    customer_count = 0

    def __init__(self, username, email, password_hash):
        super().__init__(username, email, password_hash)
        Customer.customer_count += 1
        self.__account_type = "customer"
        self.__user_id = "C" + str(self.get_user_id())
        self.__cart = None
        self.__wish_list = None
        self.__booked_services = None
        self.__payment_details = None
        self.__customizations = None

    def get_cart(self):
        return self.__cart

    def set_cart(self, cart):
        self.__cart = cart

    def get_booked_services(self):
        return self.__booked_services

    def set_booked_services(self, booked_services):
        self.__booked_services = booked_services

    def get_customizations(self):
        return self.__customizations

    def set_customizations(self, customizations):
        self.__customizations = customizations


class Staff(Account):
    staff_count = 0

    def __init__(self, username, email, password_hash):
        super().__init__(username, email, password_hash)
        Staff.staff_count += 1
        self.__account_type = "staff"
        self.__user_id = "S" + str(self.get_user_id())
        self.__appointments = None

    def get_appointments(self):
        return self.__appointments

    def set_appointments(self, appointments):
        self.__appointments = appointments
