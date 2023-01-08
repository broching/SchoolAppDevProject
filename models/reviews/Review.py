class Review:
    count_id = 0

    def __init__(self, product_id, service_id, stylist, rating, comment, image, video):
        Review.count_id += 1
        self.__review_id = Review.count_id
        self.__product_id = product_id
        self.__service_id = service_id
        self.__stylist = stylist
        self.__rating = rating
        self.__comment = comment
        self.__image = image
        self.__video = video

    def get_review_id(self):
        return self.__review_id

    def set_review_id(self, review_id):
        self.__review_id = review_id

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_service_id(self):
        return self.__service_id

    def set_service_id(self, service_id):
        self.__service_id = service_id

    def get_stylist(self):
        return self.__stylist

    def set_stylist(self, stylist):
        self.__stylist = stylist

    def get_rating(self):
        return self.__rating

    def set_rating(self, rating):
        self.__rating = rating

    def get_comment(self):
        return self.__comment

    def set_comment(self, comment):
        self.__comment = comment

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_video(self):
        return self.__video

    def set_video(self, video):
        self.__video = video
