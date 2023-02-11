import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for, abort, session
from werkzeug.datastructures import FileStorage

from models.products.InventorybackendFlaskForm import CreateNewProduct, PaymentForm, UpdateNewProduct
from models.products.Order import Order
from models.products.product_functions import save_image, delete_image

from models.products.Product import Product
import stripe
import os
from dotenv import load_dotenv
from models.auth.auth_functions import account_to_dictionary_converter, store_customer, get_customers


productr = Blueprint('productr', __name__, template_folder='templates', static_folder='static')

load_dotenv('.env')
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


@productr.route('/products')
def products():
    products_list = []
    try:
        products_dict = {}
        with shelve.open('DB/products/product.db', 'c') as db:
            if 'Products' in db:
                products_dict = db['Products']
            for key in products_dict:
                product = products_dict.get(key)
                products_list.append(product)
    except IOError as ex:
        print(f"Error in retrieving customers from customer.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('products/products.html', count=len(products_list), products_list=products_list)


@productr.route('/products/<int:id>/')
def productsSpecific(id):
    products_list = []
    try:
        products_dict = {}
        with shelve.open('DB/products/product.db', 'c') as db:
            if 'Products' in db:
                products_dict = db['Products']
            for key in products_dict:
                product = products_dict.get(key)
                products_list.append(product)

    except IOError as ex:
        print(f"Error in retrieving products from product.db for Product specific page - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving products from product.db for Product specific page  - {ex}")

    return render_template('products/payment1.html', count=len(products_list), products_list=products_list, id=id)


@productr.route('/products/order/<int:id>/')
def productOrder(id):
    try:
        products_dict = {}
        with shelve.open('DB/products/product.db', 'w') as pdb:
            if 'Products' in pdb:
                products_dict = pdb['Products']
            if id in products_dict:
                product = products_dict.get(id)
                product_quantity_temp = product.get_product_quantity()
                print(product_quantity_temp)
            pdb['Products'] = products_dict
            session['temp_product_id'] = id
            print(session['temp_product_id'])

            if id not in products_dict:
                abort(404)

            product_id = product.get_product_id()
            product_name = product.get_product_name()
            product_image_for_stripe = product.get_product_image()
            print(product_image_for_stripe)

            checkout_session = stripe.checkout.Session.create(
                line_items=[{'price_data': {
                    'product_data': {'name': f"ID: {product_id} | {product_name}",
                                     'images': [
                                         "https://th.bing.com/th/id/OIP.eqxBQW-U29nnvWcva2d1VwAAAA?pid=ImgDet&rs=1"],
                                     },
                    'unit_amount': int(product.get_product_price() * 100),
                    'currency': 'sgd',
                },
                    'quantity': 1,
                },
                ],

                payment_method_types=['card'],
                mode='payment',
                success_url=request.host_url + 'products/order/success',
                cancel_url=request.host_url + 'products/order/cancel',
            )

    except IOError as ex:
        print(f"Error in trying to open product.db in payment page (Order and payment page) - {ex}")

    return redirect(checkout_session.url)


@productr.route('/products/order/success')
def success():
    # if request.method == 'GET':
    #     print(session['customer'])
    # Handle billing history
    productStripeId = session['temp_product_id']
    print(productStripeId)
    try:
        with shelve.open('DB/products/product.db', 'w') as pdb:
            if 'Products' in pdb:
                products_dict = pdb['Products']
            if productStripeId in products_dict:
                product = products_dict.get(productStripeId)
                product_dict_for_storing = account_to_dictionary_converter(product)
                cust_list = get_customers('DB')
            pdb['Products'] = products_dict

            # Get customer id from current session
            print(session['customer'])
            target_id = session['customer']['_Account__user_id']
            print(target_id)
            for customer in cust_list:
                if customer.get_user_id() == target_id:
                    print('Customer found')
                    print(customer)

                    # Get billing history list
                    cust_billing_history = customer.get_billing_history()

                    # Append product dictionary into billing history list
                    cust_billing_history.append(product_dict_for_storing)

                    # Set new billing history list to the updated one that has the product appended.
                    customer.set_billing_history(cust_billing_history)
                    print(customer.get_billing_history())
                    store_customer(customer, 'DB')

                    # Update session with new info
                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

    except IOError as ex:
        print(f"Error in new_event for billing history - {ex}")
    return render_template('products/success.html')


@productr.route('/products/order/cancel')
def cancel():
    return render_template('products/cancel.html')


# Creating a Stripe Webhook
# Below you can see a very simple webhook that handles new orders by
# printing the order contents to the terminal.
@productr.route('/event', methods=['POST'])
def new_event():
    event = None
    payload = request.data
    signature = request.headers['STRIPE_SIGNATURE']

    # Verifying the data passed from Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, os.environ['STRIPE_WEBHOOK_SECRET'])
    except Exception as e:
        # If the payload could not be verified, return a 400 error
        abort(400)

    # Checking if the event type is checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        # Retrieving the Session object that corresponds to the order
        session = stripe.checkout.Session.retrieve(
            event['data']['object'].id, expand=['line_items'])

        # Handling things
        print(f'Sale to {session.customer_details.email}:')
        for item in session.line_items.data:
            # Print item sold and customer email
            print(f'  - {item.quantity} {item.description} '
                  f'${item.amount_total / 100:.02f} {item.currency.upper()}')

            # Handle product quantity
            string = str(item.description)
            print(string)
            id_value = int(string.split(" ")[1])
            productStripeId = id_value
            print(f"id_value: {productStripeId}")
            products_dict = {}
            try:
                with shelve.open('DB/products/product.db', 'w') as pdb:
                    if 'Products' in pdb:
                        products_dict = pdb['Products']
                    if productStripeId in products_dict:
                        product = products_dict.get(productStripeId)
                        product_quantity_temp = product.get_product_quantity()
                        print(f"Product quantity old: {product_quantity_temp}")
                        product_quantity_temp -= item.quantity
                        product.set_product_quantity(product_quantity_temp)
                        print(f"Product quantity new: {product_quantity_temp}")
                    pdb['Products'] = products_dict
            except IOError as ex:
                print(f"Error in opening product.db in new_event - {ex}")

            # # Handle billing history
            # try:
            #     with shelve.open('DB/products/product.db', 'w') as pdb:
            #         if 'Products' in pdb:
            #             products_dict = pdb['Products']
            #         if productStripeId in products_dict:
            #             product = products_dict.get(productStripeId)
            #             product_dict_for_storing = account_to_dictionary_converter(product)
            #             cust_list = get_customers('DB')
            #         pdb['Products'] = products_dict
            #
            #         # Get customer id from current session
            #         print(session['customer'])
            #         customer_id = session['customer']['_Account__userid']
            #         customer = cust_list.get(customer_id)
            #
            #         # Get billing history list
            #         cust_billing_history = customer.get_billing_history()
            #
            #         # Append product dictionary into billing history list
            #         cust_billing_history.append(product_dict_for_storing)
            #
            #         # Set new billing history list to the updated one that has the product appended.
            #         customer.set_billing_history(cust_billing_history)
            #         store_customer(customer, 'DB')
            #
            # except IOError as ex:
            #     print(f"Error in new_event for billing history - {ex}")

    return {'success': True}


@productr.route('/products/<int:id>/paymentspecific', methods=['GET', 'POST'])
def productpayment(id):
    payment_form = PaymentForm()
    if request.method == 'POST' and payment_form.submit2.data:

        try:
            products_dict = {}
            with shelve.open('DB/products/product.db', 'w') as pdb:
                if 'Products' in pdb:
                    products_dict = pdb['Products']
                if id in products_dict:
                    product = products_dict.get(id)
                    product_quantity_temp = product.get_product_quantity()
                    product_quantity_temp -= 1
                    print(product_quantity_temp)
                    product.set_product_quantity(product_quantity_temp)
                    print(product.get_product_quantity())
                pdb['Products'] = products_dict

                orders_dict = {}
                with shelve.open('DB/products/order.db', 'c') as db:
                    if 'Orders' in db:
                        orders_dict = db['Orders']

                    with shelve.open("DB/products/ordercount.db", writeback=True) as ocounter:
                        if "coupon" not in ocounter:
                            orderid = 1
                        else:
                            orderid = ocounter["coupon"]
                        ocounter["coupon"] = orderid
                        print(ocounter["coupon"])

                        order = Order(orderid, product)
                        orders_dict[order.get_id()] = order

        except IOError as ex:
            print(f"Error in trying to open product.db in payment page (Order and payment page) - {ex}")
        return redirect(url_for('productr.orders'))

    else:

        products_list = []
    try:
        products_dict = {}
        with shelve.open('DB/products/product.db', 'r') as db:
            if 'Products' in db:
                products_dict = db['Products']
            for key in products_dict:
                product = products_dict.get(key)
                products_list.append(product)
            print(products_list)
    except IOError as ex:
        print(f"Error in retrieving products from product.db for Product specific page - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving products from product.db for Product specific page  - {ex}")

    return render_template('products/payment2.html', count=len(products_list), products_list=products_list, id=id,
                           form=payment_form)


@productr.route('/orders')
def orders():
    orders_list = []
    try:
        orders_dict = {}
        with shelve.open('DB/products/order.db', 'r') as db:
            if 'Orders' in db:
                orders_list = db['Orders']
            for key in orders_list:
                order = orders_dict.get(key)
                orders_list.append(order)
                print(order)

    except IOError as ex:
        print(f"Error in retrieving customers from customer.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('products/orders.html', count=len(orders_list), orders_list=orders_list)


@productr.route('/inventory')
def inventory():
    products_list = []
    try:
        products_dict = {}
        with shelve.open('DB/products/product.db', 'r') as db:
            if 'Products' in db:
                products_dict = db['Products']
            for key in products_dict:
                product = products_dict.get(key)
                products_list.append(product)
    except IOError as ex:
        print(f"Error in retrieving products from product.db (inventory route)- {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('products/inventory.html', count=len(products_list), products_list=products_list)


# @productr.route('/createProduct', methods=['GET', 'POST'])
# def createProduct():
#     cid = 0
#     create_product_form = CreateNewProduct(request.form)
#     if request.method == 'POST' and create_product_form.validate():
#         try:
#             with shelve.open("DB/products/counter.db", writeback=True) as counter:
#                 if "coupon" not in counter:
#                     cid = 1
#                 else:
#                     cid = counter["coupon"]
#                 counter["coupon"] = cid
#                 print(counter["coupon"])
#         except IOError as ex:
#             print(f"Error in opening counter.db - {ex}")
#         except Exception as ex:
#             print(f"Unknown error occured while trying to open counter.db - {ex}")
#
#         try:
#             with shelve.open('DB/products/product.db', 'c') as db:
#                 products_dict = {}
#                 if 'Products' in db:
#                     products_dict = db['Products']
#                 product = Product(create_product_form.product_name.data, create_product_form.product_type.data,
#                                   create_product_form.product_quantity.data,
#                                   create_product_form.product_image.data,
#                                   create_product_form.product_price.data, create_product_form.product_description.data,
#                                   create_product_form.product_cost.data,
#                                   cid)
#
#                 print(type(create_product_form.product_image.data))
#                 print(create_product_form.product_image.data)
#
#                 # save image
#
#                 products_dict[product.get_product_id()] = product
#                 db['Products'] = products_dict
#         except IOError:
#             print("Error in retrieving Products from Product.db.")
#         return redirect(url_for('productr.inventory'))
#     else:
#         try:
#             with shelve.open("DB/products/counter.db", "c", writeback=True) as counter:
#                 if "coupon" not in counter:
#                     cid = 1
#                 else:
#                     cid = counter["coupon"] + 1
#                 counter["coupon"] = cid
#                 print(counter["coupon"])
#         except IOError as ex:
#             print(f"Error in opening counter.db - {ex}")
#         except Exception as ex:
#             print(f"Unknown error occured while trying to open counter.db - {ex}")
#
#         return render_template('products/createProduct.html', form=create_product_form, prdid=cid)

@productr.route('/createProduct', methods=['GET', 'POST'])
def createProduct():
    cid = 0
    create_product_form = CreateNewProduct()
    if request.method == 'POST' and create_product_form.submit1.data:
        try:
            with shelve.open("DB/products/counter.db", writeback=True) as counter:
                if "coupon" not in counter:
                    cid = 1
                else:
                    cid = counter["coupon"]
                counter["coupon"] = cid
                print(counter["coupon"])
        except IOError as ex:
            print(f"Error in opening counter.db - {ex}")
        except Exception as ex:
            print(f"Unknown error occured while trying to open counter.db - {ex}")

        try:
            with shelve.open('DB/products/product.db', 'c') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                product = Product(create_product_form.product_name.data, create_product_form.product_type.data,
                                  create_product_form.product_quantity.data,
                                  create_product_form.product_image.data,
                                  create_product_form.product_price.data, create_product_form.product_description.data,
                                  create_product_form.product_cost.data,
                                  cid)

                print(type(create_product_form.product_image.data))

                # save image
                if create_product_form.product_image.data:
                    image_file_name = save_image(create_product_form.product_image.data)
                    product.set_product_image(image_file_name)

                products_dict[product.get_product_id()] = product
                db['Products'] = products_dict
        except IOError:
            print("Error in retrieving Products from Product.db.")
        return redirect(url_for('productr.inventory'))
    else:
        try:
            with shelve.open("DB/products/counter.db", "c", writeback=True) as counter:
                if "coupon" not in counter:
                    cid = 1
                else:
                    cid = counter["coupon"] + 1
                counter["coupon"] = cid
                print(counter["coupon"])
        except IOError as ex:
            print(f"Error in opening counter.db - {ex}")
        except Exception as ex:
            print(f"Unknown error occured while trying to open counter.db - {ex}")

        return render_template('products/createProductFlaskForm.html', form=create_product_form, prdid=cid)


@productr.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def updateProduct(id):
    update_product_form = UpdateNewProduct()
    if request.method == 'POST' and update_product_form.submit1.data:
        try:
            with shelve.open('DB/products/product.db', 'w') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                if id in products_dict:
                    product = products_dict.get(id)
                    product.set_product_name(update_product_form.product_name.data)
                    product.set_product_type(update_product_form.product_type.data)
                    product.set_product_quantity(update_product_form.product_quantity.data)
                    product.set_product_price(update_product_form.product_price.data)
                    product.set_product_cost(update_product_form.product_cost.data)
                    product.set_product_description(update_product_form.product_description.data)
                    product.set_product_image(update_product_form.product_image.data)
                    print(type(update_product_form.product_image.data))

                    # save image
                    if not update_product_form.product_image.data:
                        image_file_name = request.form['current_image']
                    else:
                        image_file_name = save_image(update_product_form.product_image.data)
                    product.set_product_image(image_file_name)

                    db['Products'] = products_dict

        except IOError as ex:
            print(f"Error in updating products to products.db - {ex}")

        return redirect(url_for('productr.inventory'))
    else:
        products_list = []
        try:
            with shelve.open('DB/products/product.db', 'w') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                #     Getting products and putting them in list for jinjja html to process it later on
                for key in products_dict:
                    product = products_dict.get(key)
                    products_list.append(product)

                if id in products_dict:
                    product = products_dict.get(id)
                    update_product_form.product_name.data = product.get_product_name()
                    update_product_form.product_type.data = product.get_product_type()
                    update_product_form.product_quantity.data = product.get_product_quantity()
                    update_product_form.product_price.data = product.get_product_price()
                    update_product_form.product_description.data = product.get_product_description()
                    update_product_form.product_cost.data = product.get_product_cost()
                    cid = product.get_product_id()


        except IOError as ex:
            print(f"Error in retrieving products from products.db (GET in update products) - {ex}.")

        return render_template('products/updateProductFlaskForm.html', form=update_product_form, prdid=cid,
                               count=len(products_list), id=id, products_list=products_list)


@productr.route('/deleteProduct/<int:id>', methods=['POST'])
def deleteProduct(id):
    products_dict = {}
    try:
        with shelve.open('DB/products/product.db', 'w') as db:
            if 'Products' in db:
                products_dict = db['Products']
            products_dict.pop(id)  # Step 1: Updates are handled using dictionaries first.
            db['Products'] = products_dict

            # Step 2: Updates are then pointed to and stored back to the database using the database variable.

            # Step 3: The 'shelve' database closes since 'with' boolean is used. If it is not used, have to manually close using 'db.close' function.

    except IOError as ex:
        print(f"Error in retrieving products from product.db - {ex}")
    return redirect(url_for('productr.inventory'))
