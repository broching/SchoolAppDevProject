import shelve
from flask import Blueprint, render_template, request, url_for, redirect
from models.reviews.productReview import productReview
from models.reviews.serviceReview import serviceReview
from models.reviews.createProductReview import CreateProductReview
from models.reviews.createServiceReview import CreateServiceReview

from models.reviews.product_review_functions import save_image


review = Blueprint('review', __name__)


@review.route('/reviews')
def reviews():
    return render_template('reviews/reviews.html')


@review.route('/createProductReview', methods=['GET', 'POST'])
def createProductReview():
    create_product_review_form = CreateProductReview(request.form)
    if request.method == 'POST' and create_product_review_form.submit_p.data:
        try:
            with shelve.open('DB/reviews/productReviews/productReview.db', 'c') as db:
                product_reviews_dict = {}
                if 'Product_Reviews' in db:
                    product_reviews_dict = db['Product_Reviews']
                product_review = productReview(create_product_review_form.product_rating.data,
                                               create_product_review_form.product_comment.data,
                                               create_product_review_form.product_image.data,
                                               create_product_review_form.product_video.data)
                product_review.set_product_id(product_review.get_product_id())

                print(type(create_product_review_form.product_image.data))


                # save image
                if create_product_review_form.product_image.data:
                    image_file_name = save_image(create_product_review_form.product_image.data)
                    product_review.set_product_image(image_file_name)

                product_reviews_dict[product_review.get_product_id()] = product_review
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
        with shelve.open('DB/reviews/productReviews/productReview.db', 'r') as db:
            if 'Product_Reviews' in db:
                product_reviews_dict = db['Product_Reviews']
            for key in product_reviews_dict:
                product_review = product_reviews_dict.get(key)
                product_reviews_list.append(product_review)
    except IOError as ex:
        print(f"Error in retrieving product reviews from product_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving product reviews from product_reviews.db - {ex}")

    return render_template('reviews/productReviews.html', count=len(product_reviews_list),
                           product_reviews_list=product_reviews_list)


@review.route('/deleteProductReview/<int:id>', methods=['POST'])
def deleteProductReview(id):
    product_reviews_dict = {}
    try:
        with shelve.open('DB/reviews/productReviews/productReview.db', 'w') as db:
            if 'Product_Reviews' in db:
                product_reviews_dict = db['Product_Reviews']
            product_reviews_dict.pop(id)  # Step 1: Updates are handled using dictionaries first.
            db['Product_Reviews'] = product_reviews_dict

    except IOError as ex:
        print(f"Error in retrieving product reviews from productReviews.db - {ex}")
    return redirect(url_for('review.productReviews'))

@review.route('/productRating')
def productRating():
    return render_template('reviews/productRating.html')


@review.route('/createServiceReview', methods=['GET', 'POST'])
def createServiceReview():
    create_service_review_form = CreateServiceReview(request.form)
    if request.method == 'POST' and create_service_review_form.validate():
        try:
            with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'c') as db:
                service_reviews_dict = {}
                if 'Service_Reviews' in db:
                    service_reviews_dict = db['Service_Reviews']
                service_review = serviceReview(create_service_review_form.service_selection.data,
                                               create_service_review_form.service_rating.data,
                                               create_service_review_form.service_comment.data,
                                               create_service_review_form.service_image.data,
                                               create_service_review_form.service_video.data)
                service_review.set_service_id(service_review.get_service_id())

                service_reviews_dict[service_review.get_service_id()] = service_review
                db['Service_Reviews'] = service_reviews_dict
        except IOError:
            print("Error in retrieving Service Reviews from Service_Reviews.db.")
        return redirect(url_for('review.serviceReviews'))
    else:
        return render_template('reviews/createServiceReview.html', form=create_service_review_form)


@review.route('/serviceReviews')
def serviceReviews():
    service_reviews_list = []
    try:
        service_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'r') as db:
            if 'Service_Reviews' in db:
                service_reviews_dict = db['Service_Reviews']
            for key in service_reviews_dict:
                service_review = service_reviews_dict.get(key)
                service_reviews_list.append(service_review)
    except IOError as ex:
        print(f"Error in retrieving service reviews from service_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving service reviews from service_reviews.db - {ex}")

    return render_template('reviews/serviceReviews.html', count=len(service_reviews_list),
                           service_reviews_list=service_reviews_list)


@review.route('/deleteServiceReview/<int:id>', methods=['POST'])
def deleteServiceReview(id):
    service_reviews_dict = {}
    try:
        with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'w') as db:
            if 'Service_Reviews' in db:
                service_reviews_dict = db['Service_Reviews']
            service_reviews_dict.pop(id)  # Step 1: Updates are handled using dictionaries first.
            db['Service_Reviews'] = service_reviews_dict

    except IOError as ex:
        print(f"Error in retrieving service reviews from serviceReviews.db - {ex}")
    return redirect(url_for('review.serviceReviews'))
