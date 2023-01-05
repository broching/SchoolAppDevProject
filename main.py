from datetime import timedelta
from flask import Flask, render_template
from routes.auth import auth
from routes.account import account

# app initialization
app = Flask(__name__)

# app config
app.config["SECRET_KEY"] = "64169bc491f8cb891fc0417d2eb29bb5"

# registered blueprints to app
app.register_blueprint(auth)
app.register_blueprint(account)

# session config
app.permanent_session_lifetime = timedelta(days=15)


# starting route / home route
@app.route('/')
def home():
    return render_template('home/home.html')


if __name__ == "__main__":
    app.run(debug=True)

#charmain was here
# test add
# test again
