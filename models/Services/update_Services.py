class update_Service:
    def __init__(self, service, hairstylist, appointment_date, appointment_time, service_id, remarks):
        self.__service = service
        self.__hairstylist = hairstylist
        self.__appointment_date = appointment_date
        self.__appointment_time = appointment_time
        self.__service_id = service_id
        self.__remarks = remarks

    def get_service(self):
        return self.__service

    def get_service_id(self):
        return self.__service_id

    def get_hairstylist(self):
        return self.__hairstylist

    def get_appointment_date(self):
        return self.__appointment_date

    def get_appointment_time(self):
        return self.__appointment_time

    def get_remarks(self):
        return self.__remarks

    def set_service(self, service):
        self.__service = service

    def set_service_id(self, service_id):
        self.__service_id = service_id

    def set_hairstylist(self, hairstylist):
        self.__hairstylist = hairstylist

    def set_appointment_date(self, appointment_date):
        self.__appointment_date = appointment_date

    def set_appointment_time(self, appointment_time):
        self.__appointment_time = appointment_time

    def set_remarks(self, remarks):
        self.__remarks = remarks
