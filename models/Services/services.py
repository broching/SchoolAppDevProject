class Service:
    appointment_id = 0

    def __init__(self, first_name, last_name, gender, membership, appointment_date, appointment_time,remarks):
        Service.appointment_id += 1
        self.__first_Name = first_name
        self.__last_Name = last_name
        self.__gender = gender
        self.__membership_ID = membership
        self.__appointment_Date = appointment_date
        self.__appointment_Time = appointment_time
        self.__remarks=remarks

    def get_first_Name(self):
        return self.__first_Name

    def get_last_Name(self):
        return self.__last_Name

    def get_gender(self):
        return self.__gender

    def get_membership_ID(self):
        return self.__membership_ID

    def get_appointment_Date(self):
        return self.__appointment_Date

    def get_appointment_Time(self):
        return self.__appointment_Time
    def get_remarks(self):
        return self.__remarks

    def set_first_Name(self, first_name):
        self.__first_Name = first_name

    def set_last_Name(self, last_name):
        self.__last_Name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership_ID(self, membership):
        self.__membership_ID = membership

    def set_appointment_Date(self, appointment_Date):
        self.__appointment_Date = appointment_Date

    def get_appointment_Time(self, appointment_Time):
        self.__appointment_Time = appointment_Time
    def set_remarks(self,remarks):
        self.__remarks=remarks
