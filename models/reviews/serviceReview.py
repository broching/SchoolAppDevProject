class serviceReview:
    count_id = 0

    def __init__(self, service_rating, service_comment, service_image, service_video):
        serviceReview.count_id += 1
        self.__service_review_id = serviceReview.count_id
        self.__service_rating = service_rating
        self.__service_comment = service_comment
        self.__service_image = service_image
        self.__service_video = service_video

    def get_service_review_id(self):
        return self.__service_review_id

    def set_service_review_id(self,service_review_id):
        self.__service_review_id = service_review_id

    def get_service_rating(self):
        return self.__service_rating

    def set_service_rating(self, service_rating):
        self.__service_rating = service_rating

    def get_service_comment(self):
        return self.__service_comment

    def set_service_comment(self, service_comment):
        self.__service_comment = service_comment

    def get_service_image(self):
        return self.__service_image

    def set_service_image(self, service_image):
        self.__service_image = service_image

    def get_service_video(self):
        return self.__service_video

    def set_service_video(self, service_video):
        self.__service_video = service_video
