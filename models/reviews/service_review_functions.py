import secrets
import os

from PIL import Image

def save_image(image):
    """Saves image to static directory"""
    if image:
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.split(image.filename)
        image_file_name = random_hex + file_ext
        file_path = 'static/media/images/reviews/service_reviews/' + image_file_name
        img = Image.open(image)
        img.thumbnail((300, 300))
        img.save(file_path)
        return image_file_name


def delete_image(image_from_object):
    """Deletes image from static directory"""
    if image_from_object:
        """Deletes image from static directory"""
        file_path = 'static/media/images/reviews/service_reviews/' + image_from_object
        if os.path.isfile(file_path):
            os.remove(file_path)