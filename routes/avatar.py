import shelve, os, imghdr
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.avatar.Avatar import *
from models.auth.auth_functions import customer_login_required, staff_login_required

avatar_blueprint = Blueprint('avatar', __name__)


# TODO: 1. Figure out how to shelve images as objects
# TODO: 2. Create nice GUI for avatar staff and avatar customer
# TODO: 3. Create better looking avatar assets
# TODO: 4. Fix avatar navbar issues with login button
# TODO: 5. Add flash warnings
# TODO: 6. Add delete functions to avatars
# TODO: 7. Set avatar png for profile pic


@avatar_blueprint.route("/avatar", methods=['GET', 'POST'])
def avatar():
    # hairstyle_dir = os.listdir(hairstyle_path)
    # hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]

    stock = Avatar(hairstyle_assets[0], faceshape_assets[0], eyes_assets[0], lips_assets[0], 0)
    stock.save_avatar("stock")

    menu = Menu(["HAIRSTYLES", "FACESHAPE", "EYES", "LIPS"], 0, assets)

    if "customer" in session:
        user_id = session["customer"].get("_Account__user_id")
        user_id = str(user_id)
    else:
        user_id = "notloggedin"

    try:
        with shelve.open("DB/avatar_temporary/avatar_lists", "c") as db:
            if user_id not in db:
                path = "static/media/images/avatar_assets/images/" + str(user_id)
                if not os.path.exists(path):
                    os.makedirs(path)

                db[user_id] = [stock, []]
            else:
                pass

            preview, avatar_list = db[user_id][0], db[user_id][1]

            if request.method == "POST":
                if 'next' in request.form:
                    attr = (request.form["next"])

                    preview.next(attr)
                    preview.save_avatar(user_id + "/preview")
                    db[user_id] = [preview, avatar_list]

                elif 'save' in request.form:
                    # preview.save_avatar(user_id+"/"+str(len(avatar_list)))
                    # avatar_list.append(preview)
                    # db[user_id] = [preview, avatar_list]
                    avatarSave(preview, user_id, avatar_list, db)

                elif 'select' in request.form:
                    asset = request.form['select']
                    attr = asset.split("/")
                    attr = attr[4]
                    print(asset, attr)
                    preview.select(asset, attr)
                    preview.save_avatar(user_id + "/preview")
                    db[user_id] = [preview, avatar_list]

                elif 'select_avatar' in request.form:
                    index = int(request.form['select_avatar'])
                    extract = avatar_list[index]
                    preview = Avatar(extract.hairstyles, extract.faceshape, extract.eyes, extract.lips, extract.image)
                    preview.save_avatar(user_id + "/preview")
                    db[user_id] = [preview, avatar_list]

                # elif 'delete' in request.form:
                #     extract = preview
                #     for i in avatar_list:
                #         if extract.__dict__.pop("image") == i.__dict__.pop("image"):
                #             print("exists")
                else:
                    pass

    except IOError as ex:
        print(f"Error in retrieving avatars from avatar_list.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving avatars from avatar_list.db - {ex}")

    try:
        with shelve.open("DB/avatar_temporary/menu", "c") as db:
            if user_id not in db:
                db[user_id] = menu
            else:
                pass

            menu = db[user_id]

            if request.method == "POST":
                if "slider" in request.form:
                    if request.form["slider"] == "next":
                        menu.next()
                    else:
                        menu.prev()

                    db[user_id] = menu

            else:
                pass

    except IOError as ex:
        print(f"Error in retrieving menu from menu.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving menu from menu.db - {ex}")

    return render_template('avatar/customer_avatar.html', preview=preview, avatar_list=avatar_list, menu=menu)


@avatar_blueprint.route("/avatarSave", methods=['GET', 'POST'])
@customer_login_required
def avatarSave(preview, user_id, avatar_list, db):
    print("test", preview, user_id, avatar_list, db)
    preview.save_avatar(user_id + "/" + str(len(avatar_list)))
    avatar_list.append(preview)
    db[user_id] = [preview, avatar_list]


@avatar_blueprint.route("/avatarStaff", methods=['GET', 'POST'])
@staff_login_required
def avatarStaff():
    hairstyle_path = "static/media/images/avatar_assets/hairstyles"
    hairstyle_dir = os.listdir(hairstyle_path)
    hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]

    faceshape_path = "static/media/images/avatar_assets/faceshape"
    faceshape_dir = os.listdir(faceshape_path)
    faceshape_assets = [faceshape_path + "/" + faceshape for faceshape in faceshape_dir]

    eyes_path = "static/media/images/avatar_assets/eyes"
    eyes_dir = os.listdir(eyes_path)
    eyes_assets = [eyes_path + "/" + eyes for eyes in eyes_dir]

    lips_path = "static/media/images/avatar_assets/lips"
    lips_dir = os.listdir(lips_path)
    lips_assets = [lips_path + "/" + lips for lips in lips_dir]

    total_assets = [hairstyle_assets, faceshape_assets, eyes_assets, lips_assets]
    assets = total_assets

    if request.method == 'POST':
        f = request.files['file']
        if imghdr.what(f) != 'png':
            text = "You must upload a png file!"
            flash(text, 'error')

        else:
            f.save("static/media/images/avatar_assets/"+request.form['Upload']+"/"+f.filename)
            text = "Upload succesful"
            flash(text, 'info')


    return render_template('avatar/staff_avatar.html', hairstyle_assets=hairstyle_assets,
                           faceshape_assets=faceshape_assets, eyes_assets=eyes_assets, lips_assets=lips_assets,
                           enumerate=enumerate)

# @avatar_blueprint.route('/success', methods=['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         if imghdr.what(f) != 'png':
#             text = "You must upload a png file!"
#         else:
#             f.save("static/media/images/avatar_assets/hairstyles/"+f.filename)
#             text = "Upload succesful"
#
#         return render_template("avatar/acknowledgement.html", name=f.filename, text=text)
