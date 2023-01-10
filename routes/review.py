import shelve
from flask import Blueprint, render_template, request, url_for, redirect
from models.reviews.Review import Review
from models.reviews.productReview import productReview
from models.reviews.serviceReview import serviceReview
from models.reviews.createProductReview import CreateProductReview
from models.reviews.createServiceReview import CreateServiceReview

review = Blueprint('review', __name__)


@review.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')


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
        return redirect(url_for('review.productReviews'))
    else:
        return render_template('reviews/createProductReview.html', form=create_product_review_form)


@review.route('/productReviews')
def productReviews():
    product_reviews_list = []
    try:
        product_reviews_dict = {}
        with shelve.open('DB/reviews/productReviews.db', 'r') as db:
            if 'Product_Reviews' in db:
                product_reviews_dict = db['Product_Reviews']
            for key in product_reviews_dict:
                product_review = product_reviews_dict.get(key)
                product_reviews_list.append(product_review)
    except IOError as ex:
        print(f"Error in retrieving product reviews from Product_Reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving product reviews from Product_Reviews.db - {ex}")

    return render_template('reviews/productReviews.html', count=len(product_reviews_list),
                           product_reviews_list=product_reviews_list)


@review.route('/createServiceReview', methods=['GET', 'POST'])
def createServiceReview():
    create_service_review_form = CreateServiceReview(request.form)
    if request.method == 'POST' and create_service_review_form.validate():
        try:
            with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'c') as db:
                service_reviews_dict = {}
                if 'Service_Reviews' in db:
                    service_reviews_dict = db['Service_Reviews']
                service_review = serviceReview(create_service_review_form.service_rating.data,
                                               create_service_review_form.service_comment.data,
                                               create_service_review_form.service_image.data,
                                               create_service_review_form.service_video.data)
                service_review.set_service_review_id(service_review.get_service_review_id())

                service_reviews_dict[service_review.get_service_review_id()] = service_review
                db['Service_Reviews'] = service_reviews_dict
        except IOError:
            print("Error in retrieving Service Reviews from Service_Reviews.db.")
        return redirect(url_for('review.reviewsStorage'))
    else:
        return render_template('reviews/createServiceReview.html', form=create_service_review_form)


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
