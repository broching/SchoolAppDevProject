import shelve
from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from models.auth.auth_functions import customer_login_required
from models.reviews.productReview import productReview
from models.reviews.serviceReview import serviceReview
from models.reviews.createProductReview import CreateProductReview
from models.reviews.createServiceReview import CreateServiceReview

from routes.account import customer_profile

review = Blueprint('review', __name__)


@review.route('/createProductReview', methods=['GET', 'POST'])
@customer_login_required
def createProductReview():
    create_product_review_form = CreateProductReview(request.form)
    if request.method == 'POST' and create_product_review_form.validate():
        try:
            with shelve.open('DB/reviews/productReviews/productReview.db', 'c') as db:
                product_reviews_dict = {}
                if 'Product_Reviews' in db:
                    product_reviews_dict = db['Product_Reviews']
                product_review = productReview(
                    create_product_review_form.user_name.data,
                    create_product_review_form.user_id.data,
                    create_product_review_form.product_selection.data,
                    create_product_review_form.product_rating.data,
                    create_product_review_form.product_comment.data,
                    create_product_review_form.product_image.data,
                    create_product_review_form.product_video.data)

                product_review.set_product_id(product_review.get_product_id())

                if customer_profile():
                    username = session['customer']['_Account__username']
                    product_review.set_user_name(username)

                    user_id = session['customer']['_Account__user_id']
                    product_review.set_user_id(user_id)

                product_reviews_dict[product_review.get_product_id()] = product_review
                db['Product_Reviews'] = product_reviews_dict

                # testing filter for product 1
                if product_review.get_product_selection() == 'Product 1':
                    with shelve.open('DB/reviews/productReviews/Product1/productReview.db', 'c') as db:
                        product1_reviews_dict = {}
                        if 'Product1_Reviews' in db:
                            product1_reviews_dict = db['Product1_Reviews']

                        product1_reviews_dict[product_review.get_product_id()] = product_review
                        db['Product1_Reviews'] = product1_reviews_dict
                # end of testing filter

                # testing filter for product 2
                elif product_review.get_product_selection() == 'Product 2':
                    with shelve.open('DB/reviews/productReviews/Product2/productReview.db', 'c') as db:
                        product2_reviews_dict = {}
                        if 'Product2_Reviews' in db:
                            product2_reviews_dict = db['Product2_Reviews']

                        product2_reviews_dict[product_review.get_product_id()] = product_review
                        db['Product2_Reviews'] = product2_reviews_dict
                # end of testing filter

                # testing filter for product 3
                elif product_review.get_product_selection() == 'Product 3':
                    with shelve.open('DB/reviews/productReviews/Product3/productReview.db', 'c') as db:
                        product3_reviews_dict = {}
                        if 'Product3_Reviews' in db:
                            product3_reviews_dict = db['Product3_Reviews']

                        product3_reviews_dict[product_review.get_product_id()] = product_review
                        db['Product3_Reviews'] = product3_reviews_dict
                # end of testing filter

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


@review.route('/product1Reviews')
def product1_filter():
    product1_reviews_list = []
    try:
        product1_reviews_dict = {}
        with shelve.open('DB/reviews/productReviews/Product1/productReview.db', 'c') as db:
            if 'Product1_Reviews' in db:
                product1_reviews_dict = db['Product1_Reviews']
                for key in product1_reviews_dict:
                    product1_review = product1_reviews_dict.get(key)
                    product1_reviews_list.append(product1_review)
    except IOError as ex:
        print(f"Error in retrieving product1 reviews from product1_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving product1 reviews from product1_reviews.db - {ex}")

    return render_template('reviews/product1Reviews.html', count=len(product1_reviews_list),
                           product1_reviews_list=product1_reviews_list)


@review.route('/product2Reviews')
def product2_filter():
    product2_reviews_list = []
    try:
        product2_reviews_dict = {}
        with shelve.open('DB/reviews/productReviews/Product2/productReview.db', 'c') as db:
            if 'Product2_Reviews' in db:
                product2_reviews_dict = db['Product2_Reviews']
                for key in product2_reviews_dict:
                    product2_review = product2_reviews_dict.get(key)
                    product2_reviews_list.append(product2_review)
    except IOError as ex:
        print(f"Error in retrieving product2 reviews from product2_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving product2 reviews from product2_reviews.db - {ex}")

    return render_template('reviews/product2Reviews.html', count=len(product2_reviews_list),
                           product2_reviews_list=product2_reviews_list)


@review.route('/product3Reviews')
def product3_filter():
    product3_reviews_list = []
    try:
        product3_reviews_dict = {}
        with shelve.open('DB/reviews/productReviews/Product3/productReview.db', 'c') as db:
            if 'Product3_Reviews' in db:
                product3_reviews_dict = db['Product3_Reviews']
                for key in product3_reviews_dict:
                    product3_review = product3_reviews_dict.get(key)
                    product3_reviews_list.append(product3_review)
    except IOError as ex:
        print(f"Error in retrieving product3 reviews from product3_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving product3 reviews from product3_reviews.db - {ex}")

    return render_template('reviews/product3Reviews.html', count=len(product3_reviews_list),
                           product3_reviews_list=product3_reviews_list)


@review.route('/deleteProductReview/<int:id>/<int:pid>', methods=['POST'])
@customer_login_required
def deleteProductReview(id, pid):
    product_reviews_dict = {}
    try:
        # delete for all reviews
        with shelve.open('DB/reviews/productReviews/productReview.db', 'w') as db:
            if 'Product_Reviews' in db:
                product_reviews_dict = db['Product_Reviews']

            if customer_profile():
                delete_id = session['customer']['_Account__user_id']

                if delete_id == id:
                    product_reviews_dict.pop(pid)
                    next_pid = pid
                    db['Product_Reviews'] = product_reviews_dict

                    # delete from product1 filter
                    product1_reviews_dict = {}
                    with shelve.open('DB/reviews/productReviews/Product1/productReview.db', 'w') as db:
                        if 'Product1_Reviews' in db:
                            product1_reviews_dict = db['Product1_Reviews']

                        if next_pid in product1_reviews_dict:
                            product1_reviews_dict.pop(next_pid)
                            db['Product1_Reviews'] = product1_reviews_dict

                    # delete from product2 filter
                    product2_reviews_dict = {}
                    with shelve.open('DB/reviews/productReviews/Product2/productReview.db', 'w') as db:
                        if 'Product2_Reviews' in db:
                            product2_reviews_dict = db['Product2_Reviews']

                        if next_pid in product2_reviews_dict:
                            product2_reviews_dict.pop(next_pid)
                            db['Product2_Reviews'] = product2_reviews_dict

                    # delete from product3 filter
                    product3_reviews_dict = {}
                    with shelve.open('DB/reviews/productReviews/Product3/productReview.db', 'w') as db:
                        if 'Product3_Reviews' in db:
                            product3_reviews_dict = db['Product3_Reviews']

                        if next_pid in product3_reviews_dict:
                            product3_reviews_dict.pop(next_pid)
                            db['Product3_Reviews'] = product3_reviews_dict


    except IOError as ex:
        print(f"Error in retrieving product reviews from productReviews.db - {ex}")
    return redirect(url_for('review.productReviews'))


@review.route('/createServiceReview', methods=['GET', 'POST'])
@customer_login_required
def createServiceReview():
    create_service_review_form = CreateServiceReview(request.form)
    if request.method == 'POST' and create_service_review_form.validate():
        try:
            with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'c') as db:
                service_reviews_dict = {}
                if 'Service_Reviews' in db:
                    service_reviews_dict = db['Service_Reviews']
                service_review = serviceReview(create_service_review_form.user_id.data,
                                               create_service_review_form.user_name.data,
                                               create_service_review_form.service_selection.data,
                                               create_service_review_form.stylist_selection.data,
                                               create_service_review_form.service_rating.data,
                                               create_service_review_form.service_image.data,
                                               create_service_review_form.service_video.data,
                                               create_service_review_form.service_comment.data)

                service_review.set_service_id(service_review.get_service_id())

                if customer_profile():
                    username = session['customer']['_Account__username']
                    service_review.set_user_name(username)

                    user_id = session['customer']['_Account__user_id']
                    service_review.set_user_id(user_id)

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


@review.route('/deleteServiceReview/<int:id>/<int:pid>', methods=['POST'])
@customer_login_required
def deleteServiceReview(id, pid):
    service_reviews_dict = {}
    try:
        with shelve.open('DB/reviews/serviceReviews/serviceReview.db', 'w') as db:
            if 'Service_Reviews' in db:
                service_reviews_dict = db['Service_Reviews']

            if customer_profile():
                delete_id = session['customer']['_Account__user_id']

                if delete_id == id:
                    service_reviews_dict.pop(pid)  # Step 1: Updates are handled using dictionaries first.
                    db['Service_Reviews'] = service_reviews_dict

    except IOError as ex:
        print(f"Error in retrieving service reviews from serviceReviews.db - {ex}")
    return redirect(url_for('review.serviceReviews'))
