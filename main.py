import shelve
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for
from routes.auth import auth
from routes.account import account
from models.products.Inventorybackend import CreateNewProduct
from models.products.Product import Product

# app initialization
app = Flask(__name__)

# app config
app.config["SECRET_KEY"] = "64169bc491f8cb891fc0417d2eb29bb5"

# registered blueprints to app
app.register_blueprint(auth)
app.register_blueprint(account)

# session config
app.permanent_session_lifetime = timedelta(days=15)


# starting route / home route
@app.route('/')
def home():
    return render_template('home/home.html')


@app.route('/products')
def products():
    return render_template('products/products.html')


@app.route('/inventory')
def inventory():
    products_list = []
    try:
        products_dict = {}
        with shelve.open('product.db', 'r') as db:
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


@app.route('/createProduct', methods=['GET', 'POST'])
def createProduct():
    create_product_form = CreateNewProduct(request.form)
    if request.method == 'POST' and create_product_form.validate():
        try:
            with shelve.open('product.db', 'c') as db:
                products_dict = {}
                if 'Products' in db:
                    products_dict = db['Products']
                product = Product(create_product_form.product_name.data, create_product_form.product_type.data,
                                  create_product_form.product_id.data, create_product_form.product_quantity.data,
                                  create_product_form.product_image.data,
                                  create_product_form.product_price.data, create_product_form.product_price_range.data,
                                  create_product_form.product_description.data)

                products_dict[product.get_product_id()] = product
                db['Products'] = products_dict
        except IOError:
            print("Error in retrieving Products from Product.db.")
        return redirect(url_for('inventory'))
    else:
        return render_template('products/createProduct.html', form=create_product_form)


if __name__ == "__main__":
    app.run(debug=True)
