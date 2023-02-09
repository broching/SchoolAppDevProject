from datetime import datetime


class productReview():
    unique_id = datetime.now()
    unique_id = int(unique_id.strftime('%Y%m%d%H%M%S'))

    def __init__(self, user_name, product_rating, product_comment, product_image, product_video):
        self.__product_id = productReview.unique_id
        self.__user_name = user_name
        self.__product_rating = product_rating
        self.__product_comment = product_comment
        self.__product_image = product_image
        self.__product_video = product_video

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_product_rating(self):
        return self.__product_rating

    def set_product_rating(self, product_rating):
        self.__product_rating = product_rating

    def get_product_comment(self):
        return self.__product_comment

    def set_product_comment(self, product_comment):
        self.__product_comment = product_comment

    def get_product_image(self):
        return self.__product_image

    def set_product_image(self, product_image):
        self.__product_image = product_image

    def get_product_video(self):
        return self.__product_video

    def set_product_video(self, product_video):
        self.__product_video = product_video
