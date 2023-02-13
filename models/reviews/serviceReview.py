from datetime import datetime


class serviceReview:
    def __init__(self, user_id, user_name, service_selection, stylist_selection, service_rating, service_image, service_video,
                 service_comment):
        unique_id = datetime.now()
        unique_id = int(unique_id.strftime('%Y%m%d%H%M%S'))
        self.__service_id = unique_id
        self.__user_id = user_id
        self.__user_name = user_name
        self.__service_selection = service_selection
        self.__stylist_selection = stylist_selection
        self.__service_rating = service_rating
        self.__service_comment = service_comment
        self.__service_image = service_image
        self.__service_video = service_video

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_service_selection(self):
        return self.__service_selection

    def set_service_selection(self, service_selection):
        self.__service_selection = service_selection

    def get_stylist_selection(self):
        return self.__stylist_selection

    def set_stylist_selection(self, stylist_selection):
        self.__stylist_selection = stylist_selection

    def get_service_id(self):
        return self.__service_id

    def set_service_id(self, service_id):
        self.__service_id = service_id

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
