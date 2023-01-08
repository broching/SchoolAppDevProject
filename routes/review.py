import shelve
from flask import Blueprint, render_template, request, url_for, redirect
from models.reviews.Review import Review
from models.reviews.createReview import CreateNewReview

review = Blueprint('review', __name__)


@review.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')


@review.route('/reviewsStorage')
def reviewsStorage():
    reviews_storage = []
    try:
        reviews_dict = {}
        with shelve.open('review.db', 'r') as db:
            if 'Reviews' in db:
                reviews_dict = db['Reviews']
            for key in reviews_dict:
                review = reviews_dict.get(key)
                reviews_storage.append(review)
    except IOError as ex:
        print(f"Error in retrieving reviews from review.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving reviews from review.db - {ex}")

    return render_template('reviews/reviewsStorage.html', count=len(reviews_storage), reviews_storage=reviews_storage)


@review.route('/createReview', methods=['GET', 'POST'])
def createReview():
    create_review_form = CreateNewReview(request.form)
    if request.method == 'POST' and create_review_form.validate():
        try:
            with shelve.open('DB/reviews/review.db', 'c') as db:
                reviews_dict = {}
                if 'Reviews' in db:
                    reviews_dict = db['Reviews']
                review = Review(create_review_form.rating.data,
                                create_review_form.comment.data,
                                create_review_form.image.data,
                                create_review_form.video.data
                                )

                reviews_dict[review.get_review_id()] = review
                db['Reviews'] = reviews_dict
        except IOError:
            print("Error in retrieving Reviews from Review.db.")
        return redirect(url_for('review.reviewsList'))
    else:
        return render_template('reviews/createReview.html', form=create_review_form)


@review.route('/filterReview', methods=['GET', 'POST'])
def filterReview():
    product_id_list = []
    try:
        with shelve.open('DB/reviews/review.db', 'r') as db:
            if 'Reviews' in db:
                reviews_dict = db['Reviews']
                if Review.get_review_id() in product_id_list:
                    with shelve.open('DB/reviews/product_reviews.db', 'a') as db:
                        product_reviews_dict = {}
                        if 'Product Reviews' in db:
                            product_reviews_dict = db['Product Reviews']
                            product_reviews_dict.pop()
    except IOError:
        print("Error in filtering the reviews made for products.")
    return redirect(url_for('review.reviewsStorage'))


@review.route('/deleteReview/<int:id>', methods=['POST'])
def deleteReview(review_id):
    reviews_dict = {}
    try:
        with shelve.open('DB/reviews/review.db', 'w') as db:
            if 'Reviews' in db:
                reviews_dict = db['Reviews']

            reviews_dict.pop(review_id)
            db['Reviews'] = reviews_dict
            db.close()

    except IOError:
        print("Error in deleting reviews from Review.db")
    return redirect(url_for('review.reviewsList'))
