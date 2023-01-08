import shelve
from flask import Blueprint, render_template, request, redirect, url_for
from models.products.Inventorybackend import CreateNewProduct
from models.products.Product import Product

productr = Blueprint('productr', __name__)


@productr.route('/products')
def products():
    return render_template('products/products.html')


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
        print(f"Error in retrieving customers from customer.db - {ex}")
    except Exception as ex:
        print(f"Unknown error in retrieving customers from customer.db - {ex}")

    return render_template('products/inventory.html', count=len(products_list), products_list=products_list)


@productr.route('/createProduct', methods=['GET', 'POST'])
def createProduct():
    create_product_form = CreateNewProduct(request.form)
    if request.method == 'POST' and create_product_form.validate():
        try:
            with shelve.open('DB/products/product.db', 'c') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                product = Product(create_product_form.product_name.data, create_product_form.product_type.data,
                                  create_product_form.product_quantity.data,
                                  create_product_form.product_image.data,
                                  create_product_form.product_price.data, create_product_form.product_price_range.data,
                                  create_product_form.product_description.data, create_product_form.product_cost.data,
                                  create_product_form.product_id.data)
                product.set_product_id(product.get_product_id())

                products_dict[product.get_product_id()] = product
                db['Products'] = products_dict
        except IOError:
            print("Error in retrieving Products from Product.db.")
        return redirect(url_for('productr.inventory'))
    else:
        return render_template('products/createProduct.html', form=create_product_form)


@productr.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def updateProduct(id):
    update_product_form = CreateNewProduct(request.form)
    if request.method == 'POST' and update_product_form.validate():
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
                    product.set_product_price_range(update_product_form.product_price_range.data)
                    product.set_product_cost(update_product_form.product_cost.data)
                    product.set_product_id(update_product_form.product_id.data)
                    product.set_product_description(update_product_form.product_description.data)
                    db['Products'] = products_dict

        except IOError as ex:
            print(f"Error in updating products to products.db - {ex}")

        return redirect(url_for('productr.inventory'))
    else:
        try:
            with shelve.open('DB/products/product.db', 'w') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                if id in products_dict:
                    product = products_dict.get(id)
                    update_product_form.product_name.data = product.get_product_name()
                    update_product_form.product_type.data = product.get_product_type()
                    update_product_form.product_quantity.data = product.get_product_quantity()
                    update_product_form.product_price.data = product.get_product_price()
                    update_product_form.product_price_range.data = product.get_product_price_range()
                    update_product_form.product_description.data = product.get_product_description()
                    update_product_form.product_cost.data = product.get_product_cost()
                    update_product_form.product_id.data = product.get_product_id()
                    update_product_form.product_image.data = product.get_product_image()

        except IOError as ex:
            print(f"Error in retrieving products from products.db - {ex}.")
        return render_template('products/updateProduct.html', form=update_product_form)


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
