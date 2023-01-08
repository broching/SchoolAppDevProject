import shelve
from flask import Blueprint, render_template, request, redirect, url_for

reviews = Blueprint('reviews', __name__)


@reviews.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')


@reviews.route('/reviewsList')
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
