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
from models.auth.auth_functions import account_to_dictionary_converter, store_customer, get_customers, \
    staff_login_required, customer_login_required

productr = Blueprint('productr', __name__, template_folder='templates', static_folder='static')

load_dotenv('.env')
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


# Show all products
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


# Show specific product (Also page right before external Stripe payment page)
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


# Stripe external payment page
@productr.route('/products/order/<int:id>/')
@customer_login_required
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
                billing_address_collection='required',
            )

    except IOError as ex:
        print(f"Error in trying to open product.db in payment page (Order and payment page) - {ex}")

    return redirect(checkout_session.url)


@productr.route('/products/cartorder/<int:id>/')
@customer_login_required
def productOrderCart(id):
    try:
        # Get customer id from current session
        cust_list = get_customers('DB')
        # print(session['customer'])
        target_id = session['customer']['_Account__user_id']

        print('Checks:')
        print(f"Target ID = Account user ID = {target_id}")
        print(f"Cart ID = Account user ID = {id}")

        total = 0
        for customer in cust_list:
            if customer.get_user_id() == target_id:
                print('Customer found')
                print(customer)

                # Get cart list
                cust_cart = customer.get_cart()
                print(cust_cart)

                # Create line items for each item in the cart
                line_items = []
                mulidList = []
                for item in cust_cart:
                    pid = item['_Product__id']
                    price = float(item['_Product__price'])
                    name = item['_Product__productName']
                    line_items.append({'price_data': {
                        'product_data': {'name': f"ID: {pid} | {name}",
                                         'images': [
                                             "https://th.bing.com/th/id/OIP.eqxBQW-U29nnvWcva2d1VwAAAA?pid=ImgDet&rs=1"],
                                         },
                        'unit_amount': int(price * 100),
                        'currency': 'sgd',
                    },
                        'quantity': 1,
                    })

                    # Append product IDs to multiple id list (mulidList)
                    mulidList.append(int(pid))

                # Assign multiple ID list (mulidList) to 'mulid' session
                print(f"Multiple ID List (mulidList at productOrderCart): {mulidList}")
                session['mulid'] = mulidList
                print(f"'mulid' session content: {session['mulid']}")

                # Create a checkout session with the line items
                checkout_session = stripe.checkout.Session.create(
                    line_items=line_items,
                    payment_method_types=['card'],
                    mode='payment',
                    success_url=request.host_url + 'products/order/successCart',
                    cancel_url=request.host_url + 'products/order/cancel',
                    billing_address_collection='required',
                )

                return redirect(checkout_session.url)

    except IOError as ex:
        print(f'Error in product order for cart - {ex}')

    # products_dict = {}
    # with shelve.open('DB/products/product.db', 'w') as pdb:
    #     if 'Products' in pdb:
    #         products_dict = pdb['Products']
    #     if cart in products_dict:
    #         product = products_dict.get(cart)
    #         product_quantity_temp = product.get_product_quantity()
    #         print(product_quantity_temp)
    #     pdb['Products'] = products_dict
    #     session['temp_product_id'] = cart
    #     print(session['temp_product_id'])
    #
    #     if cart not in products_dict:
    #         abort(404)

    # product_id = product.get_product_id()
    # product_name = product.get_product_name()
    # product_image_for_stripe = product.get_product_image()
    # print(product_image_for_stripe)

    # checkout_session = stripe.checkout.Session.create(
    #     line_items=[{'price_data': {
    #         'product_data': {'name': f"ID: {product_id} | {product_name}",
    #                          'images': [
    #                              "https://th.bing.com/th/id/OIP.eqxBQW-U29nnvWcva2d1VwAAAA?pid=ImgDet&rs=1"],
    #                          },
    #         'unit_amount': int(product.get_product_price() * 100),
    #         'currency': 'sgd',
    #     },
    #         'quantity': 1,
    #     },
    #     ],
    #
    #     payment_method_types=['card'],
    #     mode='payment',
    #     success_url=request.host_url + 'products/order/success',
    #     cancel_url=request.host_url + 'products/order/cancel',
    # )

    # except IOError as ex:
    #     print(f"Error in trying to open product.db in payment page (Order and payment page) - {ex}")
    # #
    # return redirect(checkout_session.url)


# Cart functions and pages
# TODO: Add to cart (Add to database)

# When customer press add to cart,
# Open cart shelve (Cart shelve is tied to customer ID)
# Mirror shelve to local dictionary
# create cart object, the object is a convert_to_dictionary(product, for specific product ID)
# Mirror dictionary to shelve
# return redirect back to same page.
# in the same page flash successful addition to cart
@productr.route('/addtocart/<int:id>', methods=['POST'])
@customer_login_required
def addToCart(id):
    try:
        with shelve.open('DB/products/product.db', 'w') as pdb:
            if 'Products' in pdb:
                products_dict = pdb['Products']
            product = products_dict.get(id)
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

                    # Get cart list
                    cust_cart = customer.get_cart()

                    # Append product dictionary into customer cart list
                    cust_cart.append(product_dict_for_storing)

                    # Set new cart list to the updated one that has the product appended.
                    customer.set_cart(cust_cart)
                    print(customer.get_cart())
                    store_customer(customer, 'DB')

                    # Update session with new info
                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

            # message = f"Added {product.get_product_name()} to <a href='/cart'>cart</a>."
            # flash(message, category='success')
            session['addItemToCart'] = product.get_product_name()

            # cartCount = len(cust_cart)
            # try:
            #     with shelve.open('cartcount', 'c') as cdb:
            #         cdb['Count'] = cartCount
            #
            # except IOError as ex:
            #     print(f"Error at productr.addToCart while trying to open cartcount.db - {ex}")


    except IOError as ex:
        print(f"Error in opening product.db in add_to_cart - {ex}")
    return redirect(url_for('productr.productsSpecific', id=id))


# TODO: View cart (Take from database)
@productr.route('/cart')
@customer_login_required
def viewCart():
    cust_cart = []
    # Get customer id from current session
    cust_list = get_customers('DB')
    print(session['customer'])
    target_id = session['customer']['_Account__user_id']
    print(target_id)
    for customer in cust_list:
        if customer.get_user_id() == target_id:
            print('Customer found')
            print(customer)

            # Get cart list
            cust_cart = customer.get_cart()
            print(cust_cart)

            # Check if ID of products in customer cart exists in product.db
            #         Loop through customer's cart
            # If it does not exist, remove the product from customer's cart
            try:
                with shelve.open('DB/products/product.db', 'c') as pdb:
                    if 'Products' in pdb:
                        products_dict = pdb['Products']

                    # set a list to store current existing product IDs
                    productIDList = []

                    # Loop through product db
                    for key in products_dict:
                        product = products_dict.get(key)
                        productID = product.get_product_id()
                        productIDList.append(productID)

                        # Update products by checking against product.db Product class instance attributes
                        for itemToUpdate in cust_cart:
                            if itemToUpdate['_Product__id'] == productID:
                                if itemToUpdate['_Product__quantity'] != product.get_product_quantity():
                                    itemToUpdate['_Product__quantity'] = product.get_product_quantity()

                                if itemToUpdate['_Product__image'] != product.get_product_image():
                                    itemToUpdate['_Product__image'] = product.get_product_image()

                                if itemToUpdate['_Product__productName'] != product.get_product_name():
                                    itemToUpdate['_Product__image'] = product.get_product_name()

                                if itemToUpdate['_Product__price'] != product.get_product_price():
                                    itemToUpdate['_Product__price'] = product.get_product_price()

                                if itemToUpdate['_Product__productCost'] != product.get_product_cost():
                                    itemToUpdate['_Product__productCost'] = product.get_product_cost()

                                if itemToUpdate['_Product__description'] != product.get_product_description():
                                    itemToUpdate['_Product__description'] = product.get_product_description()

                                if itemToUpdate['_Product__productType'] != product.get_product_type():
                                    itemToUpdate['_Product__productType'] = product.get_product_type()

                                print(f"(viewCart)Updated list item: {itemToUpdate}")

                    pdb['Products'] = products_dict

                    print(f"(viewCart)List of product IDs (All products that exist in db): {productIDList}")
                    for cart_item in cust_cart:
                        if cart_item['_Product__id'] not in productIDList:
                            print(f"(viewCart) Cart item about to get removed from list: {cart_item}")
                            print(f"(viewCart) Cart before cart item gets removed: {cust_cart}")
                            cust_cart.remove(cart_item)
                            print(f"(viewCart) Cart left after cart item got removed: {cust_cart}")

                    # Set new cart list to the updated one that has the product appended.
                    customer.set_cart(cust_cart)
                    print(customer.get_cart())
                    store_customer(customer, 'DB')

                    # Update session with new info
                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

            except IOError as ex:
                print(f"Error in view cart (Opening product.db) - {ex}")

    # def removeitem(itemId):
    #     cust_cart.pop(itemId)

    # Note: cart_id is the same as customer id, hence we use target_id for cart id.
    return render_template('account/customer_cart.html', count=len(cust_cart), cust_cart=cust_cart, cart_id=target_id)


@productr.route('/cart/<int:id>', methods=['POST'])
def deleteItemFromCart(id):
    cust_list = get_customers('DB')

    # Get customer id from current session
    print(session['customer'])
    target_id = session['customer']['_Account__user_id']
    print(target_id)
    for customer in cust_list:
        if customer.get_user_id() == target_id:
            print('Customer found')
            print(customer)

            # Get cart list
            cust_cart = customer.get_cart()

            # # Append product dictionary into customer cart list
            # print(cust_cart)
            # flash(f"Removed item {cust_cart[id]['_Product__productName']} from cart.", category='info')
            # del cust_cart[id]
            for item in cust_cart:
                if item['_Product__id'] == id:
                    session['deleteCartItem'] = item['_Product__productName']
                    # flash(f"Removed item {item['_Product__productName']} from cart.", category='info')
                    cust_cart.remove(item)
                    break

            # # Reset customer cart (USE FOR EMERGENCIES)
            # cust_cart = []

            # Set new cart list to the updated one that has the product appended.
            customer.set_cart(cust_cart)
            print(customer.get_cart())
            store_customer(customer, 'DB')

            # Update session with new info
            customer_dict = account_to_dictionary_converter(customer)
            session['customer'] = customer_dict

    return redirect(url_for('productr.viewCart', id=id))


# Clear cart
@productr.route('/cart', methods=['POST'])
def clearCart():
    cust_list = get_customers('DB')

    # Get customer id from current session
    print(session['customer'])
    target_id = session['customer']['_Account__user_id']
    print(target_id)
    for customer in cust_list:
        if customer.get_user_id() == target_id:
            print('Customer found')
            print(customer)

            # Set cart to empty list
            cust_cart = []

            # # Reset customer cart (USE FOR EMERGENCIES)
            # cust_cart = []

            # Set new cart list to the updated one that has the product appended.
            customer.set_cart(cust_cart)
            print(customer.get_cart())
            store_customer(customer, 'DB')

            # Update session with new info
            customer_dict = account_to_dictionary_converter(customer)
            session['customer'] = customer_dict

    return redirect(url_for('productr.viewCart'))


# Payment success page TODO: Receipt
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

            cust_list = get_customers('DB')
            # Get customer id from current session
            print(session['customer'])
            target_id = session['customer']['_Account__user_id']
            print(target_id)
            for customer in cust_list:
                if customer.get_user_id() == target_id:
                    print('Customer found')
                    print(customer)

                    # Get cart list
                    cust_cart = customer.get_cart()
                    for item in cust_cart:
                        if item['_Product__id'] == productStripeId:
                            cust_cart.remove(item)
                            break

                    # # Append product dictionary into customer cart list
                    # print(cust_cart)
                    # flash(f"Removed item {cust_cart[id]['_Product__productName']} from cart.", category='info')
                    # del cust_cart[id]

                    # # Reset customer cart (USE FOR EMERGENCIES)
                    # cust_cart = []

                    # # Append product dictionary into customer cart list
                    # print(cust_cart)
                    # flash(f"Removed item {cust_cart[id]['_Product__productName']} from cart.", category='info')
                    # del cust_cart[id]

                    # Set new cart list to the updated one that has the product appended.
                    customer.set_cart(cust_cart)
                    print(customer.get_cart())
                    store_customer(customer, 'DB')

                    # Update session with new info
                    customer_dict = account_to_dictionary_converter(customer)
                    session['customer'] = customer_dict

    except IOError as ex:
        print(f"Error in new_event for billing history - {ex}")

    return render_template('products/success.html')


@productr.route('/products/order/successCart')
def successCart():
    if request.method == 'GET':
        print(session['customer'])

    # Handle billing history
    print(session['mulid'])
    if 'mulid' in session:
        productStripeIdList = session['mulid']
    else:
        # Handle the case where the key is not found in the dictionary
        # for example, you can raise an exception or set a default value
        raise KeyError("Key 'mulid' not found in session")

    # productStripeId = session['temp_product_id']
    print(productStripeIdList)

    for productStripeId in productStripeIdList:
        print("Line 454 productStripeId", productStripeId)
        try:
            with shelve.open('DB/products/product.db', 'w') as pdb:
                if 'Products' in pdb:
                    products_dict = pdb['Products']
                if productStripeId in products_dict:
                    product = products_dict.get(productStripeId)

                    product_dict_for_storing = account_to_dictionary_converter(product)
                pdb['Products'] = products_dict

                cust_list = get_customers('DB')
                # Update billing history
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

                # Update cart (Delete items purchased)
                cust_list = get_customers('DB')
                # Get customer id from current session
                print(session['customer'])
                target_id = session['customer']['_Account__user_id']
                print(target_id)
                for customer in cust_list:
                    if customer.get_user_id() == target_id:
                        print('Customer found')
                        print(customer)

                        # Get cart list
                        cust_cart = customer.get_cart()

                        # # Append product dictionary into customer cart list
                        # print(cust_cart)
                        # flash(f"Removed item {cust_cart[id]['_Product__productName']} from cart.", category='info')
                        # del cust_cart[id]
                        for item in cust_cart:
                            if item['_Product__id'] == productStripeId:
                                cust_cart.remove(item)
                                break

                        # # Reset customer cart (USE FOR EMERGENCIES)
                        # cust_cart = []

                        # Set new cart list to the updated one that has the product appended.
                        customer.set_cart(cust_cart)
                        print(customer.get_cart())
                        store_customer(customer, 'DB')

                        # Update session with new info
                        customer_dict = account_to_dictionary_converter(customer)
                        session['customer'] = customer_dict

        except IOError as ex:
            print(f"Error in new_event for billing history - {ex}")

    return render_template('products/success.html')


# Cancel order page
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
        total_items = 0
        product_ids = []  # List to store product IDs
        print(f'Sale to {session.customer_details.email}:')
        for item in session.line_items.data:
            # Print item sold and customer email
            print(f'  - {item.quantity} {item.description} '
                  f'${item.amount_total / 100:.02f} {item.currency.upper()}')

            # Total items to determine total number of items sold
            total_items += 1

            # Handle product quantity
            string = str(item.description)
            print(string)
            id_value = int(string.split(" ")[1])
            productStripeId = id_value
            print(f"id_value: {productStripeId}")
            print(f"id type: {type(productStripeId)}")
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

                        # Handle product profit
                        profit_in_shelve = float(product.get_product_price()) - float(product.get_product_cost())
                        product.set_product_profit(profit_in_shelve)

                        current_profit = profit_in_shelve
                        total_profit = float(product.get_product_profitTotal()) + float(current_profit)
                        product.set_product_profitTotal(total_profit)

                    pdb['Products'] = products_dict
            except IOError as ex:
                print(f"Error in opening product.db in new_event - {ex}")

            # Add the product ID to the list of product IDs
            product_ids.append(productStripeId)
        print(f"Total number of products iterated: {total_items}")
        print(f"List of product IDs: {product_ids}")

        # Add the list of product IDs to the session
        session['mulid'] = product_ids
        print('Session for multiple_product_ids', session['mulid'])

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


# Defunct payment page (OLD, NOT USED ANYMORE)
# @productr.route('/products/<int:id>/paymentspecific', methods=['GET', 'POST'])
# def productpayment(id):
#     payment_form = PaymentForm()
#     if request.method == 'POST' and payment_form.submit2.data:
#
#         try:
#             products_dict = {}
#             with shelve.open('DB/products/product.db', 'w') as pdb:
#                 if 'Products' in pdb:
#                     products_dict = pdb['Products']
#                 if id in products_dict:
#                     product = products_dict.get(id)
#                     product_quantity_temp = product.get_product_quantity()
#                     product_quantity_temp -= 1
#                     print(product_quantity_temp)
#                     product.set_product_quantity(product_quantity_temp)
#                     print(product.get_product_quantity())
#                 pdb['Products'] = products_dict
#
#                 orders_dict = {}
#                 with shelve.open('DB/products/order.db', 'c') as db:
#                     if 'Orders' in db:
#                         orders_dict = db['Orders']
#
#                     with shelve.open("DB/products/ordercount.db", writeback=True) as ocounter:
#                         if "coupon" not in ocounter:
#                             orderid = 1
#                         else:
#                             orderid = ocounter["coupon"]
#                         ocounter["coupon"] = orderid
#                         print(ocounter["coupon"])
#
#                         order = Order(orderid, product)
#                         orders_dict[order.get_id()] = order
#
#         except IOError as ex:
#             print(f"Error in trying to open product.db in payment page (Order and payment page) - {ex}")
#         return redirect(url_for('productr.orders'))
#
#     else:
#
#         products_list = []
#     try:
#         products_dict = {}
#         with shelve.open('DB/products/product.db', 'r') as db:
#             if 'Products' in db:
#                 products_dict = db['Products']
#             for key in products_dict:
#                 product = products_dict.get(key)
#                 products_list.append(product)
#             print(products_list)
#     except IOError as ex:
#         print(f"Error in retrieving products from product.db for Product specific page - {ex}")
#     except Exception as ex:
#         print(f"Unknown error in retrieving products from product.db for Product specific page  - {ex}")
#
#     return render_template('products/payment2.html', count=len(products_list), products_list=products_list, id=id,
#                            form=payment_form)


# Defunct orders page (OLD, NOT USED ANYMORE)
# @productr.route('/orders')
# def orders():
#     orders_list = []
#     try:
#         orders_dict = {}
#         with shelve.open('DB/products/order.db', 'r') as db:
#             if 'Orders' in db:
#                 orders_list = db['Orders']
#             for key in orders_list:
#                 order = orders_dict.get(key)
#                 orders_list.append(order)
#                 print(order)
#
#     except IOError as ex:
#         print(f"Error in retrieving customers from customer.db - {ex}")
#     except Exception as ex:
#         print(f"Unknown error in retrieving customers from customer.db - {ex}")
#
#     return render_template('products/orders.html', count=len(orders_list), orders_list=orders_list)


# Staff pages
# View created products inventory page
@productr.route('/inventory', methods=['GET', 'POST'])
@staff_login_required
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

    return render_template('products/inventory_onstaffbase.html', count=len(products_list), products_list=products_list)


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
@staff_login_required
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

                flash(f"Product {product.get_product_name()} has been added.", category="success")

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
@staff_login_required
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

                    # session['product_updated'] = product.get_product_name()
                    flash(f"Product {product.get_product_name()} has been updated.", category="success")

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
@staff_login_required
def deleteProduct(id):
    products_dict = {}
    try:
        with shelve.open('DB/products/product.db', 'w') as db:
            if 'Products' in db:
                products_dict = db['Products']

            # products_list = list(products_dict.values())
            # last_item = products_list[-1]
            # print(last_item)
            if id in products_dict:
                product = products_dict.get(id)
                product_img_name = product.get_product_image()
                delete_image(product_img_name)

            products_dict.pop(id)  # Step 1: Updates are handled using dictionaries first.
            db['Products'] = products_dict

            flash(f"Product {product.get_product_name()} has been deleted.", category="success")

            # Step 2: Updates are then pointed to and stored back to the database using the database variable.

            # Step 3: The 'shelve' database closes since 'with' boolean is used. If it is not used, have to manually close using 'db.close' function.

    except IOError as ex:
        print(f"Error in retrieving products from product.db - {ex}")
    return redirect(url_for('productr.inventory'))
