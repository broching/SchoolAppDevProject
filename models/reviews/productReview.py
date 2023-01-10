class productReview:

    def __init__(self, product_review_id, product_rating, product_comment, product_image, product_video):
        self.__product_review_id = product_review_id
        self.__product_rating = product_rating
        self.__product_comment = product_comment
        self.__product_image = product_image
        self.__product_video = product_video

    def get_product_review_id(self):
        return self.__product_review_id

    def set_product_review_id(self, product_review_id):
        self.__product_review_id = product_review_id

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
