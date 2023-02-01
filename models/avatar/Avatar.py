import os
from PIL import Image

class Avatar:
    def __init__(self, hairstyle, faceshape, eyes, lips, image):
        self.hairstyle = hairstyle
        self.faceshape = faceshape
        self.eyes = eyes
        self.lips = lips
        self.image = image

    def save_avatar(self, name):
        base_image = Image.open(self.faceshape)
        img2 = Image.open(self.eyes)
        img3 = Image.open(self.lips)
        img4 = Image.open(self.hairstyle)

        img = [img2, img3, img4]

        for i in img:
            base_image.paste(i, (0, 0), mask=i)

        base_image.save("static/media/images/avatar_assets/images/"+name+".png", "PNG")
        self.image = "static/media/images/avatar_assets/images/"+name+".png"

    def next_hairstyle(self):
        hairstyle_dir = os.listdir(hairstyle_path)
        hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]
        index = hairstyle_assets.index(self.hairstyle)
        if index == len(hairstyle_assets) - 1:
            self.hairstyle = hairstyle_assets[0]
        else:
            self.hairstyle = hairstyle_assets[index + 1]
        print(len(hairstyle_assets), index)


hairstyle_path = "static/media/images/avatar_assets/hairstyles"
hairstyle_dir = os.listdir(hairstyle_path)
hairstyle_assets = [hairstyle_path+"/"+hairstyle for hairstyle in hairstyle_dir]

faceshape_dir = os.listdir("static/media/images/avatar_assets/faceshape")
faceshape_assets = ["static/media/images/avatar_assets/faceshape/"+faceshape for faceshape in faceshape_dir]

eyes_dir = os.listdir("static/media/images/avatar_assets/eyes")
eyes_assets = ["static/media/images/avatar_assets/eyes/"+eyes for eyes in eyes_dir]

lips_dir = os.listdir("static/media/images/avatar_assets/lips")
lips_assets = ["static/media/images/avatar_assets/lips/"+lips for lips in lips_dir]

