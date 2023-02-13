import shelve
from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from models.auth.auth_functions import customer_login_required, staff_login_required
from models.reviews.productReview import productReview
from models.reviews.serviceReview import serviceReview
from models.reviews.createProductReview import CreateProductReview
from models.reviews.createServiceReview import CreateServiceReview

from routes.account import customer_profile, staff_profile

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

                with shelve.open('DB/reviews/productReviews/Staff/productReview.db', 'c') as db:
                    staff_product_reviews_dict = {}
                    if 'Staff_Product_Reviews' in db:
                        staff_product_reviews_dict = db['Staff_Product_Reviews']
                    staff_product_review = productReview(
                        create_product_review_form.user_name.data,
                        create_product_review_form.user_id.data,
                        create_product_review_form.product_selection.data,
                        create_product_review_form.product_rating.data,
                        create_product_review_form.product_comment.data,
                        create_product_review_form.product_image.data,
                        create_product_review_form.product_video.data)

                    staff_product_review.set_product_id(staff_product_review.get_product_id())

                    staff_product_reviews_dict[staff_product_review.get_product_id()] = staff_product_review
                    db['Staff_Product_Reviews'] = staff_product_reviews_dict

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

@review.route('/staffProductReviews')
def staffProductReviews():
    staff_product_reviews_list = []
    try:
        staff_product_reviews_dict = {}
        with shelve.open('DB/reviews/productReviews/Staff/productReview.db', 'r') as db:
            if 'Staff_Product_Reviews' in db:
                staff_product_reviews_dict = db['Staff_Product_Reviews']
            for key in staff_product_reviews_dict:
                staff_product_review = staff_product_reviews_dict.get(key)
                staff_product_reviews_list.append(staff_product_review)
    except IOError as ex:
        print(f"Error in retrieving staff product reviews from staff_product_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving staff product reviews from staff_product_reviews.db - {ex}")

    return render_template('reviews/staffProductReviews.html', count=len(staff_product_reviews_list),
                           staff_product_reviews_list=staff_product_reviews_list)

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
                    flash('Your product review has been successfully deleted.', category='success')

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


                else:
                    flash('You are not authorised to delete this product review.', category='error')

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

                # filter db for Hair Cut
                if service_review.get_service_selection() == 'Hair Cut':
                    with shelve.open('DB/reviews/serviceReviews/Service1/serviceReview.db', 'c') as db:
                        service1_reviews_dict = {}
                        if 'Service1_Reviews' in db:
                            service1_reviews_dict = db['Service1_Reviews']

                        service1_reviews_dict[service_review.get_service_id()] = service_review
                        db['Service1_Reviews'] = service1_reviews_dict
                # end of filter

                # filter db for Hair Styling
                if service_review.get_service_selection() == 'Hair Styling':
                    with shelve.open('DB/reviews/serviceReviews/Service2/serviceReview.db', 'c') as db:
                        service2_reviews_dict = {}
                        if 'Service2_Reviews' in db:
                            service2_reviews_dict = db['Service2_Reviews']

                        service2_reviews_dict[service_review.get_service_id()] = service_review
                        db['Service2_Reviews'] = service2_reviews_dict
                # end of filter

                # filter db for Hair Dye
                if service_review.get_service_selection() == 'Hair Dye':
                    with shelve.open('DB/reviews/serviceReviews/Service3/serviceReview.db', 'c') as db:
                        service3_reviews_dict = {}
                        if 'Service3_Reviews' in db:
                            service3_reviews_dict = db['Service3_Reviews']

                        service3_reviews_dict[service_review.get_service_id()] = service_review
                        db['Service3_Reviews'] = service3_reviews_dict
                # end of filter

                # filter db for Stylist 1 - not tested
                if service_review.get_stylist_selection() == 'Hairstylist 1':
                    with shelve.open('DB/reviews/serviceReviews/Stylist1/serviceReview.db', 'c') as db:
                        stylist1_reviews_dict = {}
                        if 'Stylist1_Reviews' in db:
                            stylist1_reviews_dict = db['Stylist1_Reviews']

                        stylist1_reviews_dict[service_review.get_service_id()] = service_review
                        db['Stylist1_Reviews'] = stylist1_reviews_dict
                # end of filter

                # filter db for Stylist 2 - not tested
                if service_review.get_stylist_selection() == 'Hairstylist 2':
                    with shelve.open('DB/reviews/serviceReviews/Stylist2/serviceReview.db', 'c') as db:
                        stylist2_reviews_dict = {}
                        if 'Stylist2_Reviews' in db:
                            stylist2_reviews_dict = db['Stylist2_Reviews']

                        stylist2_reviews_dict[service_review.get_service_id()] = service_review
                        db['Stylist2_Reviews'] = stylist2_reviews_dict
                # end of filter

                # filter db for Stylist 3 - not tested
                if service_review.get_stylist_selection() == 'Hairstylist 3':
                    with shelve.open('DB/reviews/serviceReviews/Stylist3/serviceReview.db', 'c') as db:
                        stylist3_reviews_dict = {}
                        if 'Stylist3_Reviews' in db:
                            stylist3_reviews_dict = db['Stylist3_Reviews']

                        stylist3_reviews_dict[service_review.get_service_id()] = service_review
                        db['Stylist3_Reviews'] = stylist3_reviews_dict
                # end of filter


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


@review.route('/service1Reviews')
def service1_filter():
    service1_reviews_list = []
    try:
        service1_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Service1/serviceReview.db', 'c') as db:
            if 'Service1_Reviews' in db:
                service1_reviews_dict = db['Service1_Reviews']
                for key in service1_reviews_dict:
                    service1_review = service1_reviews_dict.get(key)
                    service1_reviews_list.append(service1_review)
    except IOError as ex:
        print(f"Error in retrieving service1 reviews from service1_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving service1 reviews from service1_reviews.db - {ex}")

    return render_template('reviews/service1Reviews.html', count=len(service1_reviews_list),
                           service1_reviews_list=service1_reviews_list)


@review.route('/service2Reviews')
def service2_filter():
    service2_reviews_list = []
    try:
        service2_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Service2/serviceReview.db', 'c') as db:
            if 'Service2_Reviews' in db:
                service2_reviews_dict = db['Service2_Reviews']
                for key in service2_reviews_dict:
                    service2_review = service2_reviews_dict.get(key)
                    service2_reviews_list.append(service2_review)
    except IOError as ex:
        print(f"Error in retrieving service2 reviews from service2_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving service2 reviews from service2_reviews.db - {ex}")

    return render_template('reviews/service2Reviews.html', count=len(service2_reviews_list),
                           service2_reviews_list=service2_reviews_list)


@review.route('/service3Reviews')
def service3_filter():
    service3_reviews_list = []
    try:
        service3_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Service3/serviceReview.db', 'c') as db:
            if 'Service3_Reviews' in db:
                service3_reviews_dict = db['Service3_Reviews']
                for key in service3_reviews_dict:
                    service3_review = service3_reviews_dict.get(key)
                    service3_reviews_list.append(service3_review)
    except IOError as ex:
        print(f"Error in retrieving service3 reviews from service3_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving service3 reviews from service3_reviews.db - {ex}")

    return render_template('reviews/service3Reviews.html', count=len(service3_reviews_list),
                           service3_reviews_list=service3_reviews_list)


@review.route('/stylist1Reviews')
def stylist1_filter():
    stylist1_reviews_list = []
    try:
        stylist1_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Stylist1/serviceReview.db', 'c') as db:
            if 'Stylist1_Reviews' in db:
                stylist1_reviews_dict = db['Stylist1_Reviews']
                for key in stylist1_reviews_dict:
                    stylist1_review = stylist1_reviews_dict.get(key)
                    stylist1_reviews_list.append(stylist1_review)
    except IOError as ex:
        print(f"Error in retrieving service2 reviews from service2_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving service2 reviews from service2_reviews.db - {ex}")

    return render_template('reviews/stylist1Reviews.html', count=len(stylist1_reviews_list),
                           stylist1_reviews_list=stylist1_reviews_list)


@review.route('/stylist2Reviews')
def stylist2_filter():
    stylist2_reviews_list = []
    try:
        stylist2_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Stylist2/serviceReview.db', 'c') as db:
            if 'Stylist2_Reviews' in db:
                stylist2_reviews_dict = db['Stylist2_Reviews']
                for key in stylist2_reviews_dict:
                    stylist2_review = stylist2_reviews_dict.get(key)
                    stylist2_reviews_list.append(stylist2_review)
    except IOError as ex:
        print(f"Error in retrieving stylist2 reviews from stylist2_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving stylist2 reviews from stylist2_reviews.db - {ex}")

    return render_template('reviews/stylist2Reviews.html', count=len(stylist2_reviews_list),
                           stylist2_reviews_list=stylist2_reviews_list)


@review.route('/stylist3Reviews')
def stylist3_filter():
    stylist3_reviews_list = []
    try:
        stylist3_reviews_dict = {}
        with shelve.open('DB/reviews/serviceReviews/Stylist3/serviceReview.db', 'c') as db:
            if 'Stylist3_Reviews' in db:
                stylist3_reviews_dict = db['Stylist3_Reviews']
                for key in stylist3_reviews_dict:
                    stylist3_review = stylist3_reviews_dict.get(key)
                    stylist3_reviews_list.append(stylist3_review)
    except IOError as ex:
        print(f"Error in retrieving stylist3 reviews from stylist3_reviews.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving stylist3 reviews from stylist3_reviews.db - {ex}")

    return render_template('reviews/stylist3Reviews.html', count=len(stylist3_reviews_list),
                           stylist3_reviews_list=stylist3_reviews_list)


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
                    service_reviews_dict.pop(pid)
                    next_pid = pid
                    db['Service_Reviews'] = service_reviews_dict
                    flash('Your service review has been successfully deleted.', category='success')

                    # delete from service1 filter
                    service1_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Service1/serviceReview.db', 'w') as db:
                        if 'Service1_Reviews' in db:
                            service1_reviews_dict = db['Service1_Reviews']

                        if next_pid in service1_reviews_dict:
                            service1_reviews_dict.pop(next_pid)
                            db['Service1_Reviews'] = service1_reviews_dict

                    # delete from service2 filter
                    service2_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Service2/serviceReview.db', 'w') as db:
                        if 'Service2_Reviews' in db:
                            service2_reviews_dict = db['Service2_Reviews']

                        if next_pid in service2_reviews_dict:
                            service2_reviews_dict.pop(next_pid)
                            db['Service2_Reviews'] = service2_reviews_dict

                    # delete from service3 filter
                    service3_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Service3/serviceReview.db', 'w') as db:
                        if 'Service3_Reviews' in db:
                            service3_reviews_dict = db['Service3_Reviews']

                        if next_pid in service3_reviews_dict:
                            service3_reviews_dict.pop(next_pid)
                            db['Service3_Reviews'] = service3_reviews_dict

                    # delete from stylist1 filter
                    stylist1_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Stylist1/serviceReview.db', 'w') as db:
                        if 'Stylist1_Reviews' in db:
                            stylist1_reviews_dict = db['Stylist1_Reviews']

                        if next_pid in stylist1_reviews_dict:
                            stylist1_reviews_dict.pop(next_pid)
                            db['Stylist1_Reviews'] = stylist1_reviews_dict

                    # delete from stylist2 filter
                    stylist2_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Stylist2/serviceReview.db', 'w') as db:
                        if 'Stylist2_Reviews' in db:
                            stylist2_reviews_dict = db['Stylist2_Reviews']

                        if next_pid in stylist2_reviews_dict:
                            stylist2_reviews_dict.pop(next_pid)
                            db['Stylist2_Reviews'] = stylist2_reviews_dict

                    # delete from stylist3 filter
                    stylist3_reviews_dict = {}
                    with shelve.open('DB/reviews/serviceReviews/Stylist3/serviceReview.db', 'w') as db:
                        if 'Stylist3_Reviews' in db:
                            stylist3_reviews_dict = db['Stylist3_Reviews']

                        if next_pid in stylist3_reviews_dict:
                            stylist3_reviews_dict.pop(next_pid)
                            db['Stylist3_Reviews'] = stylist3_reviews_dict
                else:
                    flash('You are not authorised to delete this service review.', category='error')

    except IOError as ex:
        print(f"Error in retrieving service reviews from serviceReviews.db - {ex}")
    return redirect(url_for('review.serviceReviews'))
