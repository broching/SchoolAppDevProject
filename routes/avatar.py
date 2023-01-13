import shelve, os
from flask import Blueprint, render_template, request
from models.avatar.Avatar import *

avatar_blueprint = Blueprint('avatar', __name__)

@avatar_blueprint.route("/avatar", methods=['GET', 'POST'])
def avatar():

    stock = Avatar(hairstyle_assets[0], faceshape_assets[0], eyes_assets[0], lips_assets[0], 0)
    stock.save_avatar("stock")

    with shelve.open("DB/avatar_temporary/avatar", "c") as db:
        if "stock" not in db:
            db["stock"] = stock
        else:
            pass

        if "avatar" in db:
            avatar = db["avatar"]
        else:
            avatar = db["stock"]

        if request.method == "POST":
            avatar.hairstyle = hairstyle_assets[1]
            avatar.save_avatar("avatar")

    return render_template('avatar/customer_avatar.html', avatar=avatar)