from app import app
import mysql.connector

from flask import Flask,json,jsonify
from flask_bcrypt import Bcrypt
from app.DB_configration import MyConfiguration

bcrypt = Bcrypt()
class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def make_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def my_cursor(self):
        return self.cursor








class Orders:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')

    def insert_orders(self, user_id, product_id, product_qty, total, order_status, billing_name, billing_email, billing_address, billing_city):
        sql = """
                INSERT INTO orders (user_id, product_id, product_qty, total, order_status, billing_name, billing_email, billing_address, billing_city) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        try:
            self.cursor.execute(sql, (user_id, product_id, product_qty, total, order_status, billing_name, billing_email, billing_address, billing_city))
            self.connection.commit()
            print('Order successfully inserted')
            return True, 'Order successfully inserted'
        except Exception as e:
            print('Failed to insert order')
            print(f'Error: {e}')
            return False, f'Error: {e}'
        
    
    
    def display_orders(self, user_id):
        sql = """
         
          select orders.order_id,users.f_name,users.s_name,products.Product_name,
		orders.product_qty,orders.total,orders.order_status,orders.billing_name,
        orders.billing_email,orders.billing_address,orders.billing_city,orders.order_date
		from 
		orders join products on orders.product_id = products.product_id
        join Users on orders.user_id  =users.user_id where orders.user_id  = %s ;
           
             """
        try:

            self.cursor.execute(sql, (user_id,))
            orders = self.cursor.fetchall()
            # print(f"orders based on user_id: {orders}")

            return orders


        except Exception as e:
            print(f"error while displaying orders: {e}")

            return False
        

    def display_orders_by_admin(self):
        sql = """
         
           select orders.order_id,users.f_name,users.s_name,products.Product_name,
		orders.product_qty,orders.total,orders.order_status,orders.billing_name,
        orders.billing_email,orders.billing_address,orders.billing_city,orders.order_date,
        orders.user_id
		from 
		orders join products on orders.product_id = products.product_id
        join Users on orders.user_id  =users.user_id ;
           
             """
        try:

            self.cursor.execute(sql)
            orders = self.cursor.fetchall()
            # print(f"orders based on user_id: {orders}")

            return orders


        except Exception as e:
            print(f"error while displaying : {e}")

            return False
    

    def cancel_order(self,user_id,order_id,order_status):
        # .... update only order.status

        sql = """
        UPDATE orders
        SET order_status = %s
        WHERE user_id = %s AND order_id = %s
        """
        try:
            self.cursor.execute(sql, (order_status, user_id, order_id))
            self.connection.commit()
            print(f"si sax aya loo cancely order")
            return True
        except Exception as e:
           
            print(f"Failed to update order status: {e}")
            return False
    
    

    

    

   

    



 

   

   
  
    
  




my_configuration = MyConfiguration()
def check_admin_connection():
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
        trainee = Orders(mysql_connect.connection)

        

        return True, trainee
    except Exception as e:
        print(f'')
        return False, f'Error: {e}.'
        
        
       

    
   