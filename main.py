import shelve
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for

from routes.services import service
from routes.auth import auth
from routes.account import account
from routes.review import review
from routes.products import productr
from routes.avatar import avatar_blueprint

app = Flask(__name__)

# app config
app.config["SECRET_KEY"] = "64169bc491f8cb891fc0417d2eb29bb5"

# registered blueprints to app
app.register_blueprint(auth)
app.register_blueprint(account)
app.register_blueprint(review)
app.register_blueprint(productr)
app.register_blueprint(service)
app.register_blueprint(avatar_blueprint)

# session config
app.permanent_session_lifetime = timedelta(days=15)


# starting route / home route
@app.route('/')
def home():
    return render_template('home/home.html')

if __name__ == "__main__":
    app.run(debug=True)
