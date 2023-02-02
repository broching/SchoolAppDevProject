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
        user_id = str(user_id)
        print(user_id)
    else:
        pass

    try:
        with shelve.open("DB/avatar_temporary/avatar_lists", "c") as db:
            if user_id not in db:
                path = "static/media/images/avatar_assets/images/" + str(user_id)
                if not os.path.exists(path):
                    os.makedirs(path)

                db[user_id] = [stock, []]
                print("not in db")
            else:
                print("in db")

            preview, avatar_list = db[user_id][0], db[user_id][1]

            if request.method == "POST":
                if 'next hairstyle' in request.form:
                    preview.next_hairstyle()
                    preview.save_avatar(user_id+"/preview")
                    db[user_id] = [preview, avatar_list]

                elif 'save' in request.form:
                    preview.save_avatar(user_id+"/"+str(len(avatar_list)))
                    avatar_list.append(preview)
                    db[user_id] = [preview, avatar_list]

    except IOError as ex:
        print(f"Error in retrieving avatars from avatar_list.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving avatars from avatar_list.db - {ex}")

    return render_template('avatar/customer_avatar.html', preview=preview, avatar_list=avatar_list)

# @avatar_blueprint.route("/avatarStaff", methods=['GET', 'POST'])
# def avatarStaff():
#     hairstyle_dir = os.listdir(hairstyle_path)
#     hairstyle_assets = [hairstyle_path + "/" + hairstyle for hairstyle in hairstyle_dir]
#     total_assets = [hairstyle_assets, faceshape_assets, eyes_assets, lips_assets]
#     assets = total_assets
#     return render_template('avatar/staff_avatar.html', assets=assets, enumerate=enumerate)
#
#
# @avatar_blueprint.route('/success', methods = ['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save("static/media/images/avatar_assets/hairstyles/"+f.filename)
#         return render_template("avatar/acknowledgement.html", name=f.filename)

