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






def decryptpass(encrypted_password: str, key: bytes) -> str:
    # Create a Fernet object with the given key
    f = Fernet(key)
    # Decrypt the password
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()



    

class Products:
    def __init__(self, connection):
        try:
            self.connection = connection
            self.cursor = connection.cursor()
        except Exception as err:
            print('Something went wrong! Internet connection or database connection.')
            print(f'Error: {err}')
    


    def create_product(self,Product_name,Product_price,selling_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity):
        sql = "INSERT INTO products(Product_name,Product_price,selling_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            self.cursor.execute(sql, (Product_name,Product_price,selling_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,))
            self.connection.commit()
            print("si sax eh aya roo xareeyey product")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la xareeyo product: {e}")
            return False, f"error: {e}"
        
    def view_category_name(self,category_name):
        sql = "SELECT category_name FROM products where category_name = %s"
        try:
            self.cursor.execute(sql, (category_name,))
            category_name = self.cursor.fetchall()
            print(f"category_name: {category_name}")
            return category_name
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"
    

    def dispay_product_info(self):
        sql  = "select * from products"
        try:
            self.cursor.execute(sql)
            products = self.cursor.fetchall()

            # print(f"all products info: {products}")

            return products

        except Exception as e:
            print(f"erro while display product: {e}")
            return False, f"error while displaying product info: {e}"
    
    # update_products
    def update_products(self,Product_name,Product_price,selling_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,Product_id):
        sql = "UPDATE products SET Product_name = %s,Product_price = %s,selling_price = %s,Product_img_1 = %s,Product_img_2 = %s,Product_descrpt_1 = %s,Product_descrpt_2 = %s,category_name = %s,inventory_quantity = %s WHERE Product_id = %s"
        try:
            self.cursor.execute(sql, (Product_name,Product_price,selling_price,Product_img_1,Product_img_2,Product_descrpt_1,Product_descrpt_2,category_name,inventory_quantity,Product_id,))
            self.connection.commit()
            print("si sax eh aya loo update gareeyey product")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la update gareeyo product: {e}")
            return False, f"error: {e}"
        

    
    # ...delete product
    def delete_product(self,Product_id):
        sql = "DELETE FROM products WHERE Product_id = %s"
        try:
            self.cursor.execute(sql, (Product_id,))
            self.connection.commit()
            print("si sax eh aya loo tirtiray product")
            return True, "si sax ayd u tirtiray"
        
        except Exception as e:
            print(f"error ayaa jiro, in la tirtiro product: {e}")
            return False, f"error: {e}"
    #  display porduct inventory
    def display_product_inventory(self,product_id):
        sql = "SELECT inventory_quantity from products where product_id = %s "
        try:
            self.cursor.execute(sql, (product_id,))
            product_inventory = self.cursor.fetchall()
            print(f"product_inventory db: {product_inventory[0][0]}")
            if product_inventory:
                return product_inventory[0][0]  # Return the actual quantity
            else:
                return 0    
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"
        

    # product cart, storing user_id,product_id,qty
    def product_cart(self,user_id,product_id,qty):
        sql = "INSERT INTO product_carts(user_id,product_id,qty) VALUES (%s,%s,%s)"
        try:
            self.cursor.execute(sql, (user_id,product_id,qty,))
            self.connection.commit()
            print("si sax eh aya loo xareeyey product cart")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la xareeyo product cart: {e}")
            return False, f"error: {e}"
        
    # ... get_product_cart by product_id and user_id , not to store dublicate
    def get_product_cart(self,user_id,product_id):
        sql = "SELECT * FROM product_carts WHERE user_id = %s AND product_id = %s"
        try:
            self.cursor.execute(sql, (user_id,product_id,))
            product_cart = self.cursor.fetchall()
            print(f"product_cart: {product_cart}")
            return product_cart
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"
    # ... display products carts table the with the user_id
    def display_product_cart(self,user_id):
        sql = """

          select product_carts.product_id,  products.Product_name,products.     selling_price,
            products.Product_img_1,
            product_carts.qty
			from products join  product_carts
            on product_carts.product_id  = products.Product_id
            where product_carts.user_id = %s;
        """
        try:
            self.cursor.execute(sql, (user_id,))
            product_cart = self.cursor.fetchall()
            # print(f"product_cart: {product_cart}")
            return product_cart
        except Exception as e:
            print(f"error ayaa jiro, in la soo xa: {e}")
            return False, f"error: {e}"
    
    # ....... update the qty in product_carts where user_id
    def update_product_cart(self,qty,user_id,product_id):
        sql = "UPDATE product_Carts SET qty = %s WHERE user_id = %s AND product_id = %s"
        try:
            self.cursor.execute(sql, (qty,user_id,product_id,))
            self.connection.commit()
            print("si sax eh aya loo update gareeyey product cart")
            return True, "si sax ayd u xareysay"
        
        except Exception as e:
            print(f"error ayaa jiro, in la update gareeyo product cart: {e}")
            return False, f"error: {e}"
# ...... soo bandhig dhamaan cartiga.
    def count_product_carts(self, user_id):
        sql = "SELECT COUNT(*) FROM product_Carts WHERE user_id = %s"
        try:
            self.cursor.execute(sql, (user_id,))
            # No need to commit after a SELECT query
            count_product_carts = self.cursor.fetchall()
            print(f"dhamaan product count: {count_product_carts}")
            return count_product_carts, "si sax ayd u xareysay"
        except Exception as e:
            print(f"error ayaa jiro, count all product_carts: {e}")
            return False, f"error: {e}"
    # display_product_carts
    def get_product_cart_quantity(self, product_id):
        sql = "SELECT qty FROM product_Carts WHERE product_id = %s"
        try:
            self.cursor.execute(sql, (product_id,))
            # No need to commit after a SELECT query
            count_product_carts = self.cursor.fetchall()
            print(f"product qty: : {count_product_carts}")
            return count_product_carts, "si sax ayd u xareysay"
        except Exception as e:
            print(f"error ayaa jiro, product_qty: {e}")
            return False, f"error: {e}"
        
        
    def remove_cart(self, user_id, product_id):
        sql = "DELETE FROM product_carts WHERE product_id = %s AND user_id = %s"

        try:
            self.cursor.execute(sql, (product_id, user_id))  
            self.connection.commit()
            return True, "Product successfully removed from cart."  

        except Exception as e:
            print(f"Error removing product from cart: {e}")
          
            return False, "An error occurred."  

        

    # clear_product_cart_after_place_order

    def clear_cart_after_place_order(self, user_id):
        sql = "DELETE FROM product_carts WHERE user_id = %s"
        try:
            self.cursor.execute(sql, (user_id,))
            # No need to commit after a SELECT query
            self.connection.commit()
            return True, "si sax ayaa loo clear gareeyey porduct carts"
        except Exception as e:
            print(f"error ayaa jiro, clear gareynta product cart: {e}")
            return False, f"error: {e}"
    

        


    




   

   
  
    
  




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
        trainee = Products(mysql_connect.connection)
        return True, trainee
    except Exception as e:
        print(f'creating roduct error database: {e}')
        return False, f'Error: {e}.'
        
        
       

    
   