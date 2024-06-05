from app import app
from flask import Flask, json,request, render_template,redirect,session,flash,url_for
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.users_db import customers
from flask_bcrypt import Bcrypt
from app.models.products.products_db import Products
from app.models.orders.order_db import Orders
import datetime

# ..... bycrpt waye
bcrypt  =Bcrypt()



my_configuration = MyConfiguration()
def check_connection():
    try:
        mysql_connect = Database(
            host=my_configuration.DB_HOSTNAME,
            port=3306,
            user=my_configuration.DB_USERNAME,
            password=my_configuration.DB_PASSWORD,
            database=my_configuration.DB_NAME
        )
        # Create an instance of the Store class
        mysql_connect.make_connection()
        trainee = customers(mysql_connect.connection)
        products_instance = Products(mysql_connect.connection)
        Orders_instance = Orders(mysql_connect.connection)

        return True, trainee,products_instance,Orders_instance
    except Exception as e:
        print(f'')
        return False, None, None,None


app.config["SECRET_KEY"] = "abdi@12"


@app.route("/E-keyboard/register", methods = ["POST", "GET"])
def user_register():
    if session.get('user_email'):
        return redirect(url_for('home_page'))
    else:
        
    
        connection_status, customers,_ = check_connection()
        print("after requies")
        if request.method == "GET":
            
            if connection_status:
                return render_template("users/register.html")
            else:
                return "Connection failed"
        elif request.method == "POST":
            # Process registration form data here
            firstName = request.form.get("first_name")
            secondName = request.form.get("second_name")
            address = request.form.get("address")
            phone = request.form.get("phone")
            email = request.form.get("email")
            password = request.form.get("password")
            # .... passowrd into hash
            
            password_to = bcrypt.generate_password_hash(password).decode('utf-8')
            if not firstName:
                flash("geli magacaaga koowaad")
                return redirect(url_for("user_register"))
            if not secondName:
                flash("geli magacaaga labaad")
                return redirect(url_for("user_register"))
            if not address:
                flash("geli address-kaaga")
                return redirect(url_for("user_register"))
            if not phone:
                flash("geli numberkaa-ga")
                return redirect(url_for("user_register"))
            if not email:
                flash("geli email-kaaga")
                return redirect(url_for("user_register"))
            if not password:
                flash("geli password-kaaga")
                return redirect(url_for("user_register"))
            print(f"all users info is: name:{firstName}, second: {secondName} \n address: {address}, phone: {phone}, \n  email: {email}, passowrd: {password}")
            check_user_email = customers.find_user_email(email)

            if check_user_email:
                flash("emailkan wuu jiraa")
                return redirect(url_for("user_register"))
            else:

                insert_into_database = customers.register_user(firstName,secondName,email,password_to, phone,address)
                print(f"user inserted is: {insert_into_database}")
                user_id = customers.find_user_id(email)
                session["user_id"] = user_id
                session['user_email'] = email
                # products = products_instance.dispay_product_info()

    
                return redirect(url_for("home_page"))
    
                # return render_template("productHomePage/index.html",products = products)

            # ........ geli database-ka
            # Perform registration logic here


# create a ptyhon fucntion adds two number



  

    
    
@app.route("/",  methods = ["POST", "GET"])
@app.route("/E-keyboard/login", methods = ["POST", "GET"])
def user_login():
    print(f"userka ku jiro session: {session.get('user_email')}")
    connection_status, _,customers, _ = check_connection()
    if session.get('user_email'):
        return redirect(url_for('home_page'))
    else:

        if request.method == "GET":
          
            if connection_status:
                return render_template("users/login.html")
            else:
                return "Connection failed"
        elif request.method == "POST":
            # Process registration form data here
            email = request.form.get("email")
            password = request.form.get("password")

            if not email:
                flash("geli emaail-kaaga")
                return redirect(url_for("user_login"))
            if not password:
                flash("geli password-kaaga")
                return redirect(url_for("user_login"))
            user_id = customers.find_user_id(email)
            make_login = customers.login_user(email,password)
            print(f"make login: {make_login}")
            # Perform registration logic here
            if make_login:
                session["user_id"] = user_id
                session['user_email'] = email
                flash("si sax ayad login u sameysay")
                return redirect(url_for("home_page"))
            else:
                flash("email ama password-kaaga waa xad")
                return redirect(url_for("user_login"))
           



@app.route("/E-keyboard/logout")
def user_logout():
    if session.get('user_email'):
        session.pop('user_email')
        return redirect(url_for("user_login"))  

    else:
        return redirect(url_for("user_login"))
    

@app.route("/E-keyboard/homePage", methods=["GET", "POST"])
def home_page():
    if session.get('user_email'):
        message = ""
        connection_status, _, products_instance, Orders_instance = check_connection()
        user_id = session.get("user_id")

        if request.method == "GET":
            products = products_instance.dispay_product_info()
            count_product_carts = products_instance.count_product_carts(user_id)
            product_carts = products_instance.display_product_cart(user_id)

            show_order = Orders_instance.display_orders(user_id)

            order_to_dict = []

            for order in show_order:
                formatted_date = order[11].strftime("%Y/%m/%d") if order[11] else ""
                order_to_dict.append({
                    "order_id": order[0],
                    "user_name": order[1] + order[2],
                    "product_name": order[3],
                    "quantity": order[4],
                    "total": order[5],
                    "order_status": order[6],
                    "billing_name": order[7],
                    "billing_email": order[8],
                    "billing_address": order[9],
                    "billing_city": order[10],
                    "order_date": formatted_date
                })
            print(f"views show orders: {order_to_dict}")
            return render_template("productHomePage/index.html", products=products, product_carts=product_carts, count_product_carts=count_product_carts, order_to_dict=order_to_dict)
        
        elif request.method == "POST":
            if request.content_type == 'application/json':
                # This is the JSON request for updating product quantities
                product_quantities = request.json
                print(f"Received product quantities: {product_quantities}")  # Debugging line
                for product_id, quantity in product_quantities.items():
                    quantity = int(quantity)
                    print(f"Updating product_id: {product_id} with quantity: {quantity}")  # Debugging line
                    inventory_quantity = products_instance.display_product_inventory(product_id)

                    if inventory_quantity >= quantity:
                        update_product_cart = products_instance.update_product_cart(quantity, user_id, product_id)
                        print(f"Updated product cart: {update_product_cart}")  # Debugging line
                    else:
                        message = "Insufficient stock for product ID {}".format(product_id)
                        products = products_instance.dispay_product_info()
                        product_carts = products_instance.display_product_cart(user_id)
                        count_product_carts = products_instance.count_product_carts(user_id)
                        return render_template("productHomePage/index.html", products=products, product_carts=product_carts, message=message, count_product_carts=count_product_carts)

                return redirect(url_for('place_order'))
            else:
                # This is the form submission for cancelling an order
                order_id = request.form.get("order_id")
                print(f"click order_id: {order_id}")

                if order_id:
                    # Call your function to cancel the order
                    order_status = "canceled"
                    Orders_instance.cancel_order(user_id, order_id,order_status)
                    message = f"Order {order_id} has been cancelled."
                else:
                    message = "Failed to cancel the order."

                products = products_instance.dispay_product_info()
                product_carts = products_instance.display_product_cart(user_id)
                count_product_carts = products_instance.count_product_carts(user_id)
                show_order = Orders_instance.display_orders(user_id)

                order_to_dict = []
                for order in show_order:
                    formatted_date = order[11].strftime("%Y/%m/%d") if order[11] else ""
                    order_to_dict.append({
                        "order_id": order[0],
                        "user_name": order[1] + order[2],
                        "product_name": order[3],
                        "quantity": order[4],
                        "total": order[5],
                        "order_status": order[6],
                        "billing_name": order[7],
                        "billing_email": order[8],
                        "billing_address": order[9],
                        "billing_city": order[10],
                        "order_date": formatted_date
                    })

                return render_template("productHomePage/index.html", products=products, product_carts=product_carts, count_product_carts=count_product_carts, order_to_dict=order_to_dict, message=message)
    else:
        return redirect(url_for('user_login'))




# @app.route("/E-keyboard/place-order", methods=["POST", "GET"])
# def place_order():
#     if session.get('user_email'):
#         connection_status, _, products_instance = check_connection()
#         if request.method == "GET":  
#             user_id = session.get("user_id")
#             product_carts = products_instance.display_product_cart(user_id)
#             return render_template("productHomePage/place_order.html", product_carts=product_carts)
           
#         elif request.method == "POST":
#             print("i am post")
#             user_id = session.get("user_id")
#             customer_name = request.form.get("customer_name")
#             customer_email = request.form.get("customer_email")
#             customer_address = request.form.get("customer_address")
#             customer_city = request.form.get("customer_city")

#             product_ids = request.form.getlist("product_id[]")
#             product_qtys = request.form.getlist("product_qty[]")
#             product_totals = request.form.getlist("product_total[]")
            
#             print(f"customer_name: {customer_name} customer_email:{customer_email} \n customer_address: {customer_address} customer_city: {customer_city} \n product_ids: {product_ids} product_qtys: {product_qtys} product_totals: {product_totals}")

#             # Logic to place the order

#             return redirect(url_for('home_page'))
#     else:
#         return redirect(url_for('user_login'))




    
@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def product_detail(product_id):
    # Check database connection
    connection_status, _, products_instance,_ = check_connection()
    if not connection_status:
        return "Database connection error", 500

    # Initialize product_id
    product = None

    # Handle GET request
    if request.method == "GET":
        # Retrieve product information
        products = products_instance.dispay_product_info()
        product = next((product for product in products if product[0] == product_id), None)

        # If product is not found, return 404 error
        if product is None:
            return "Product not found", 404

    # Handle POST request
    elif request.method == "POST":
        # Retrieve form data
        quantity = request.form.get('quantity')
        user_id = session.get("user_id")
        quantity = int(quantity)

       

        try:
            # Check if product_id is valid before attempting to add to cart
            products = products_instance.dispay_product_info()
            product = next((product for product in products if product[0] == product_id), None)

            # ...chech if the product already in the cart
            product_in_cart = products_instance.get_product_cart(user_id, product_id)
            invenotry_quantity = products_instance.display_product_inventory(product_id)
            if product_in_cart:
                flash('mar hore ayad gelisay cart-ga')
                return render_template('productHomePage/product_description.html', product=product,  product_id=product_id)

            else:

                if product is not None:
                    print(f"value quantity detail")
                    # Attempt to add product to cart
                    if invenotry_quantity >= quantity:
                        pass
                        insert_cart = products_instance.product_cart(user_id, product_id, quantity)
                    else:
                        flash("ma heyno hadigaasi macaamiil")
                        return redirect(url_for("product_detail"))
                    
                    # Check if product was successfully added to cart
                    if insert_cart:
                        flash("si sax ayad u ugu dartay")
                    else:
                        flash('wax baa qaldan macaamiil')
                else:
                    # Product not found, set error message
                    flash("wax product malahan")
        except Exception as e:
            # Handle any exceptions that occur during insertion
            print(f"Error inserting product into cart: {e}")
            success_message = f"Error adding product to cart: {e}"

    # Render template with product information and success message
    return render_template('productHomePage/product_description.html', product=product,  product_id=product_id)


