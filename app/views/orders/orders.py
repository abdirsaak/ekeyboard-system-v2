from app import app
from flask import Flask, json,request, render_template,redirect,session,flash,url_for
from app.DB_configration import MyConfiguration
from app.models.users_db import Database
from app.models.users_db import customers
from app.models.orders.order_db import Orders
from flask_bcrypt import Bcrypt
from app.models.products.products_db import Products

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
    
        

        return True, trainee, products_instance,Orders_instance
    except Exception as e:
        print(f'')
        return False,None, None, None


app.config["SECRET_KEY"] = "abdi@12"


    
# ............. admin part



@app.route("/E-keyboard/admin/login/completed_Orders", methods = ["GET", "POST"])
def completed_Orders():
    if session.get('admin_email'):
        connection_status, trainee, products_instance, Orders_instance = check_connection()
        if connection_status:
            if request.method == "GET":
                get_all_orders = Orders_instance.display_orders_by_admin()
                all_order_to_dict = []

                for order in get_all_orders:
                    formatted_date = order[11].strftime("%Y/%m/%d") if order[11] else ""
                    all_order_to_dict.append({
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
                        "order_date": formatted_date,
                        "user_id": order[12]
                    })
                return render_template("orders/order.html", all_order_to_dict = all_order_to_dict)

           
        

            else:
                order_id = request.form.get("order_id")
                user_id = request.form.get("user_id")
                print(f"value of user_id: {user_id} vaue of order_id: {order_id}")
                order_status = "canceled"
                cancel_order  = Orders_instance.cancel_order(user_id,order_id,order_status)
                print(f"canceled order succes: {cancel_order}")

                return redirect(url_for("completed_Orders"))
        else:
            print("connecton falided")
            return render_template("orders/order.html")
    
    else:
        return redirect(url_for('admin_login'))
    











# .............. user part
@app.route("/E-keyboard/place-order", methods=["POST", "GET"])
def place_order():
    if session.get('user_email'):
        connection_status, trainee, products_instance, Orders_instance = check_connection()
        if connection_status:
            if request.method == "GET":
                user_id = session.get("user_id")
                product_carts = products_instance.display_product_cart(user_id)
                return render_template("productHomePage/place_order.html", product_carts=product_carts)
               
            elif request.method == "POST":
                user_id = session.get("user_id")
                customer_name = request.form.get("customer_name")
                customer_email = request.form.get("customer_email")
                customer_address = request.form.get("customer_address")
                customer_city = request.form.get("customer_city")

                product_ids = request.form.getlist("product_id[]")
                product_qtys = request.form.getlist("product_qty[]")
                product_totals = request.form.getlist("product_total[]")

                print(f"customer_name: {customer_name} customer_email:{customer_email} \n customer_address: {customer_address} customer_city: {customer_city} \n product_ids: {product_ids} product_qtys: {product_qtys} product_totals: {product_totals}")

                # Loop through each product and insert it into the database
                for product_id, product_qty, product_total in zip(product_ids, product_qtys, product_totals):
                    order_status = "Completed"  # Example status, change as needed
                    Orders_instance.insert_orders(
                        user_id, product_id, product_qty, product_total, order_status,
                        customer_name, customer_email, customer_address, customer_city
                    )
                clear_cart_after_place_order = products_instance.clear_cart_after_place_order(user_id)
                print(f"waa la tiray carts true", clear_cart_after_place_order)
                flash("si sax ayad u sameysay place order")
                return redirect(url_for('home_page'))
        else:
            flash('Failed to connect to the database.')
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('user_login'))
   




@app.route("/E-keyboard/orders")
def display_orders():
    if session.get('user_email'):
        connection_status, trainee, products_instance, Orders_instance = check_connection()
        if connection_status:
            if request.method == "GET":
                user_id = session.get("user_id")
                show_order = Orders_instance.display_orders(user_id)
                print(f"views show orders: {show_order}")
                return render_template("productHomePage/place_order.html", show_order=show_order)
               
            elif request.method == "POST":
                user_id = session.get("user_id")
                
            
        else:
            flash('Failed to connect to the database.')
            return redirect(url_for('home_page'))
    else:
        return redirect(url_for('user_login'))
       
       
       
       
       
       
       
       
