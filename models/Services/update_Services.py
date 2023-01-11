class update_Service:
    def __init__(self, service, hairstylist, appointment_date, appointment_time):
        self.__service = service
        self.__hairstylist = hairstylist
        self.__appointment_date = appointment_date
        self.__appointment_time = appointment_time

    def get_service(self):
        return self.__service

    def get_hairstylist(self):
        return self.__hairstylist

    def get_appointment_date(self):
        return self.__appointment_date

    def get_appointment_time(self):
        return self.__appointment_time

    def set_service(self, service):
        self.__service = service

    def set_hairstylist(self, hairstylist):
        self.__hairstylist = hairstylist

    def set_appointment_date(self, appointment_date):
        self.__appointment_date = appointment_date

    def set_appointment_time(self, appointment_time):
        self.__appointment_time = appointment_time
