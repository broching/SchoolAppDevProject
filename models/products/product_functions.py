import secrets
import os
import shelve

from PIL import Image

# Cart shelve (NOT FINISHED, NEED CUSTOMER ID)
def save_to_cart():
    try:
        cart_dict = {}
        with shelve.open('DB/products/cart.db', 'c') as db:
            if 'Cart' in db:
                cart_dict = db['Cart']
    except IOError as ex:
        print(f"Failed to open cart.db - {ex}")

def save_image(image):
    """Saves image to static directory"""
    if image:
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.split(image.filename)
        image_file_name = random_hex + file_ext
        file_path = 'static/media/images/product/' + image_file_name
        img = Image.open(image)
        img.thumbnail((300, 300))
        img.save(file_path)
        return image_file_name


def delete_image(image_from_object):
    """Deletes image from static directory"""
    if image_from_object:
        """Deletes image from static directory"""
        file_path = 'static/media/images/product/' + image_from_object
        if os.path.isfile(file_path):
            os.remove(file_path)
