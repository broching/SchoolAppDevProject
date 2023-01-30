class CreditCard:
    def __init__(self, card_type, card_number, card_name, card_cvv, card_expiry):
        self.__card_type = card_type
        self.__card_number = card_number
        self.__card_name = card_name
        self.__card_cvv = card_cvv
        self.__card_expiry = card_expiry

    def get_card_type(self):
        return self.__card_type

    def set_card_type(self, card_type):
        self.__card_type = card_type

    def get_card_number(self):
        return self.__card_number

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def get_card_name(self):
        return self.__card_name

    def set_card_name(self, card_name):
        self.__card_name = card_name

    def get_card_cvv(self):
        return self.__card_cvv

    def set_card_cvv(self, card_cvv):
        self.__card_cvv = card_cvv

    def get_card_expiry(self):
        return self.__card_expiry

    def set_card_expiry(self, card_expiry):
        self.__card_expiry = card_expiry
