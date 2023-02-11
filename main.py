
from datetime import timedelta
from flask import Flask, render_template

from routes.services import service
from routes.auth import auth
from routes.account import account
from routes.review import review
from routes.products import productr
from routes.avatar import avatar_blueprint

app = Flask(__name__)

# app config
app.config["SECRET_KEY"] = "641z69bc491f8cb891fc0417d2eb29bb5"
app.config["PRODUCT_UPLOAD"] = 'static/media/images/product'
app.config["PRODUCT_REVIEW_UPLOAD"] = 'static/media/images/reviews/product_reviews'

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
@app.route('/home')
@app.route('/')
def home():
    return render_template('home/home.html')


@app.errorhandler(404)
def page_not_found_404(e):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def page_not_found_500(e):
    return render_template('error_pages/500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)


#     greg was here
