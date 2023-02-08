class CreditCard:
    def __init__(self, card_id, card_number, card_name, card_cvv, card_expiry, street_address, state, postal,
                 card_default=False):
        self.__card_id = card_id
        self.__card_number = card_number
        self.__card_name = card_name
        self.__card_cvv = card_cvv
        self.__card_expiry = card_expiry
        self.__card_default = card_default
        self.__street_address = street_address
        self.__state = state
        self.__postal = postal

    def get_card_id(self):
        return self.__card_id

    def set_card_id(self, card_id):
        self.__card_id = card_id

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

    def get_card_default(self):
        return self.__card_default

    def set_card_default(self, card_default):
        self.__card_default = card_default

    def get_street_address(self):
        return self.__street_address

    def set_street_address(self, street_address):
        self.__street_address = street_address

    def get_state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state

    def get_postal(self):
        return self.__postal

    def set_postal(self, postal):
        self.__postal = postal
