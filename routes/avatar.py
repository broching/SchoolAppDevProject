import shelve, os
from flask import Blueprint, render_template, request, session
from models.avatar.Avatar import *

avatar_blueprint = Blueprint('avatar', __name__)

@avatar_blueprint.route("/avatar", methods=['GET', 'POST'])
def avatar():
    hairstyle_dir = os.listdir(hairstyle_path)
    hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]

    stock = Avatar(hairstyle_assets[0], faceshape_assets[0], eyes_assets[0], lips_assets[0], 0)
    stock.save_avatar("stock")

    if "customer" in session:
        user_id = session["customer"].get("_Account__user_id")
    else:
        print("Need to be logged in to access avatar feature")

    avatar_list = [stock]
    try:
        avatar_lists_dict = {}
        with shelve.open('DB/avatar_temporary/avatar', 'c') as db:
            if 'Avatars' in db:
                avatar_lists_dict = db['Avatars']
            else:
                pass

            if user_id not in avatar_lists_dict:
                path = "static/media/images/avatar_assets/images/"+str(user_id)
                if not os.path.exists(path):
                    os.makedirs(path)
                avatar_lists_dict[user_id] = avatar_list
            else:
                pass

            avatar_list = avatar_lists_dict[user_id]
            avatar = avatar_list[-1]

            if request.method == "POST":
                if 'next hairstyle' in request.form:
                    avatar.next_hairstyle()
                    avatar.save_avatar("avatar")

                elif 'save' in request.form:
                    pass

    except IOError as ex:
        print(f"Error in retrieving avatars from avatar.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving avatars from avatar.db - {ex}")

    return render_template('avatar/customer_avatar.html', avatar=avatar)

    # avatar_list = []
    # try:
    #     avatar_dict = {}
    #     with shelve.open('DB/avatar_temporary/avatar.db', 'c') as db:
    #         if user_id in db:
    #             avatar_dict = db[user_id]
    #             print(avatar_dict)
    #         else:
    #             path = "static/media/images/avatar_assets/images/" + str(user_id)
    #             if not os.path.exists(path):
    #                 os.makedirs(path)
    #             db[user_id] = avatar_dict
    #             print(db[user_id])
    #
    #         if "stock" not in user_id:
    #             stock.save_avatar(str(user_id)+"/stock")
    #         else:
    #             pass
    #
    #         for key in avatar_dict:
    #             avatar = avatar_dict.get(key)
    #             avatar_list.append(avatar)
    #
    # except IOError as ex:
    #     print(f"Error in retrieving customers from customer.db - {ex}")
    # except Exception as ex:
    #     print(f"Unknown error in retrieving customers from customer.db - {ex}")
    #
    # return render_template('avatar/customer_avatar.html', avatar_list=avatar_list)

@avatar_blueprint.route("/avatarStaff", methods=['GET', 'POST'])
def avatarStaff():
    hairstyle_dir = os.listdir(hairstyle_path)
    hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]
    total_assets = [hairstyle_assets, faceshape_assets, eyes_assets, lips_assets]
    assets = total_assets
    return render_template('avatar/staff_avatar.html', assets=assets, enumerate=enumerate)


@avatar_blueprint.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save("static/media/images/avatar_assets/hairstyles/"+f.filename)
        return render_template("avatar/acknowledgement.html", name=f.filename)

