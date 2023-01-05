class Product:
    count_id = 0

    def __init__(self, name, productType, id, quantity, image, price, priceRange, description):
        Product.count_id += 1
        self.__productName = name
        self.__id = id
        self.__quantity = quantity
        self.__image = image
        self.__price = price
        self.__priceRange = priceRange
        self.__description = description
        self.__productType = productType

    # getters
    def get_product_name(self):
        return self.__productName

    def get_product_id(self):
        return self.__id

    def get_product_image(self):
        return self.__image

    def get_product_quantity(self):
        return self.__quantity

    def get_product_price(self):
        return self.__price

    def get_product_price_range(self):
        return self.__priceRange

    def get_product_description(self):
        return self.__description

    # setters
    def set_product_name(self, name):
        self.__productName = name

    def set_product_id(self, id):
        self.__id = id

    def set_product_quantity(self, quantity):
        self.__quantity = quantity

    def set_product_price(self, price):
        self.__price = price

    def set_product_price_range(self, priceRange):
        self.__priceRange = priceRange

    def set_product_description(self, description):
        self.__description = description
