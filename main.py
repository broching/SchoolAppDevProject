import shelve
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for
from routes.auth import auth
from routes.account import account
from routes.products import products
from models.products.Inventorybackend import CreateNewProduct
from models.products.Product import Product
from models.reviews.Review import Review

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

@app.route('/services')
def services():
    return render_template('services/services.html')



@app.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')

@app.route('/reviewsList')
def reviewsList():
    reviews_list = []
    try:
        reviews_dict = {}
        with shelve.open('review.db', 'r') as db:
            if 'Reviews' in db:
                reviews_dict = db['Reviews']
            for key in reviews_dict:
                review = reviews_dict.get(key)
                reviews_list.append(review)
    except IOError as ex:
        print(f"Error in retrieving reviews from review.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving reviews from review.db - {ex}")

    return render_template('reviews/reviewsList.html', count=len(reviews_list), reviews_list=reviews_list)

if __name__ == "__main__":
    app.run(debug=True)
