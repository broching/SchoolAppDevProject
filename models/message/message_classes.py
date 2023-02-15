from datetime import datetime


class EmailMessage:
    def __init__(self, email, subject, body):
        time = datetime.now()
        time = int(round(time.timestamp()))
        self.__id = 'message' + str(time)
        self.__email = email
        self.__subject = subject
        self.__body = body
        self.__date = datetime.today().date()
        self.__status = 'unanswered'

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_subject(self):
        return self.__subject

    def set_subject(self, subject):
        self.__subject = subject

    def get_body(self):
        return self.__body

    def set_body(self, body):
        self.__body = body

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status
