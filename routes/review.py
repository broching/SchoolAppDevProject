import shelve
from flask import Blueprint, render_template, request, url_for, redirect
from models.reviews.Review import Review
from models.reviews.productReview import productReview
from models.reviews.createProductReview import CreateProductReview

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


@review.route('/createProductReview', methods=['GET', 'POST'])
def createProductReview():
    create_product_review_form = CreateProductReview(request.form)
    if request.method == 'POST' and create_product_review_form.validate():
        try:
            with shelve.open('DB/reviews/productReviews/productReview.db', 'c') as db:
                product_reviews_dict = {}
                if 'Product_Reviews' in db:
                    product_reviews_dict = db['Product_Reviews']
                product_review = productReview(create_product_review_form.product_rating.data,
                                               create_product_review_form.product_comment.data,
                                               create_product_review_form.product_image.data,
                                               create_product_review_form.product_video.data)
                product_review.set_product_review_id(product_review.get_product_review_id())

                product_reviews_dict[product_review.get_product_review_id()] = product_review
                db['Product_Reviews'] = product_reviews_dict
        except IOError:
            print("Error in retrieving Product Reviews from Product_Reviews.db.")
        return redirect(url_for('review.reviewsStorage'))
    else:
        return render_template('reviews/createProductReview.html', form=create_product_review_form)

#still doing
@review.route('/createServiceReview', methods=['GET', 'POST'])
def createServiceReview():
    create_product_review_form = CreateProductReview(request.form)
    if request.method == 'POST' and create_product_review_form.validate():
        try:
            with shelve.open('DB/reviews/productReviews/productReview.db', 'c') as db:
                product_reviews_dict = {}
                if 'Product_Reviews' in db:
                    product_reviews_dict = db['Product_Reviews']
                product_review = productReview(create_product_review_form.product_rating.data,
                                               create_product_review_form.product_comment.data,
                                               create_product_review_form.product_image.data,
                                               create_product_review_form.product_video.data)
                product_review.set_product_review_id(product_review.get_product_review_id())

                product_reviews_dict[product_review.get_product_review_id()] = product_review
                db['Product_Reviews'] = product_reviews_dict
        except IOError:
            print("Error in retrieving Product Reviews from Product_Reviews.db.")
        return redirect(url_for('review.reviewsStorage'))
    else:
        return render_template('reviews/createProductReview.html', form=create_product_review_form)



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
