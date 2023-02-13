import os
from PIL import Image

class Avatar:
    def __init__(self, hairstyles, faceshape, eyes, lips, image):
        self.hairstyles = hairstyles
        self.faceshape = faceshape
        self.eyes = eyes
        self.lips = lips
        self.image = image

    def save_avatar(self, name):
        base_image = Image.open(self.faceshape)
        img2 = Image.open(self.eyes)
        img3 = Image.open(self.lips)
        img4 = Image.open(self.hairstyles)

        img = [img2, img3, img4]

        for i in img:
            base_image.paste(i, (0, 0), mask=i)

        base_image.save("static/media/images/avatar_assets/images/"+name+".png", "PNG")
        self.image = "static/media/images/avatar_assets/images/"+name+".png"

    # def next_hairstyle(self):
    #     hairstyle_dir = os.listdir(hairstyle_path)
    #     hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]
    #     index = hairstyle_assets.index(self.hairstyles)
    #     if index == len(hairstyle_assets) - 1:
    #         self.hairstyles = hairstyle_assets[0]
    #     else:
    #         self.hairstyles = hairstyle_assets[index + 1]

    def next(self, attr):
        path = "static/media/images/avatar_assets/"+attr
        asset_dir = os.listdir(path)
        assets = [path+"/"+asset for asset in asset_dir]

        index = assets.index(getattr(self, attr))
        if index == len(assets) - 1:
            setattr(self, attr, assets[0])
        else:
            setattr(self, attr, assets[index + 1])

    def select(self, asset, attr):
        setattr(self, attr, asset)

    def check_exists(self, obj):
        pass

class Menu:
    def __init__(self, tabs, selected_tab, tab_items):
        self.tabs = tabs
        self.selected_tab = selected_tab
        self.tab_items = tab_items

    def next(self):
        if self.selected_tab == len(self.tabs) - 1:
            self.selected_tab = 0
        else:
            self.selected_tab += 1

    def prev(self):
        if self.selected_tab == 0:
            self.selected_tab = len(self.tabs) - 1
        else:
            self.selected_tab -= 1


hairstyle_path = "static/media/images/avatar_assets/hairstyles"
hairstyle_dir = os.listdir(hairstyle_path)
hairstyle_assets = [hairstyle_path+"/"+hairstyle for hairstyle in hairstyle_dir]

faceshape_path = "static/media/images/avatar_assets/faceshape"
faceshape_dir = os.listdir(faceshape_path)
faceshape_assets = [faceshape_path+"/"+faceshape for faceshape in faceshape_dir]

eyes_path = "static/media/images/avatar_assets/eyes"
eyes_dir = os.listdir(eyes_path)
eyes_assets = [eyes_path+"/"+eyes for eyes in eyes_dir]

lips_path = "static/media/images/avatar_assets/lips"
lips_dir = os.listdir(lips_path)
lips_assets = [lips_path+"/"+lips for lips in lips_dir]

assets = [hairstyle_assets, faceshape_assets, eyes_assets, lips_assets]

