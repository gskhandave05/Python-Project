__author__ = 'khandave_g'

import MySQLdb as mdb

# For connecting to remote mysql database.
con = mdb.connect('10.20.1.50', 'fos', 'root', 'fosdb')

# Method is used for adding vendor information to vendors table.
# Takes vendors name,contact,email,city,username,password,isActive,menu (list) as parameters.
def addVendor(name, contact, email,city, username, password, isActive, menu):
    with con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO VENDORS(name,contact,email,city,username, password,isActive) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, contact, email,city, username, password, isActive))

    addMenu(menu)

# Method is used to add vendor food menu in menu table.
# Menu is a dictionary having two lists : price and itemName.
# Takes menu list as a parameter.
def addMenu(menu):
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT VENDOR_ID FROM VENDORS ORDER BY VENDOR_ID DESC LIMIT 1")
        vendorId = cur.fetchone()
        for item in menu:
            i = 0
            for itemName in menu[0]['itemName']:
                cur.execute("INSERT INTO MENU(vendor_id,item_name,price) values (%s,%s,%s)",
                            (vendorId['VENDOR_ID'], itemName, item['price'][i]))
                i = i + 1

# Method is used to fetch all admins from admins table.
# returns admins list.
def getAllAdminsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from admins")
        adminList = cur.fetchall()
        return adminList

# Method is used to fetch all vendors from vendors table.
# returns vendors list.
def getAllVendorsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from vendors")
        vendorsList = cur.fetchall()
        return vendorsList

# Method is used to fetch registered vendor from vendors table.
# Takes username and password and returns a vendor.
def getRegisteredVendor(username, password):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VENDORS WHERE USERNAME = %s and password = %s", (username, password))
        vendor = cur.fetchone()
        return vendor

# Method is used to fetch vendor from vendors table by providing vendorId.
# Takes vendorId as a parameter and returns a vendor.
def getVendorByVendorId(vendorId):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VENDORS WHERE vendor_id = %s", (vendorId))
        vendor = cur.fetchone()
        return vendor

# Method is used to update vendor profile.
# Updates vendor information in vendors table according to vendorId.
def updateVendorProfile(name, contact, email,city, username, password, vendorId):
    with con:
        cur = con.cursor()
        cur.execute(
            "UPDATE vendors SET name = %s, contact = %s, email = %s,city = %s, username = %s,password = %s where vendor_id = %s",
            (name, contact, email,city, username, password, vendorId))

# Method is used to fetch all menu items of a vendor by providing vendorId.
def getMenuByVendorId(vendorId):
    with con:
        cur = con.cursor()
        cur.execute("SELECT item_id,item_name,price FROM MENU WHERE vendor_id = %s", (vendorId))
        menu = cur.fetchall()
        return menu

# Method is used to remove any food item from menu table by providing itemCode.
def removeFoodItem(itemCode):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM MENU WHERE ITEM_ID = %s", (itemCode))

# Method is used to update food item by providing itemCode.
def updateFoodItem(vendorId, itemCode, itemName, price):
    with con:
        cur = con.cursor()
        cur.execute(
            "UPDATE MENU SET vendor_id = %s, item_id = %s, item_name = %s, price = %s WHERE item_id=%s",
            (vendorId, itemCode, itemName, price, itemCode))

# Method is used to get food item by providing itemCode.
def getItemByItemId(itemCode):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM MENU WHERE item_id = %s", (itemCode))
        item = cur.fetchone()
        return item

# Method is used to add more food items to menu table according to vendorId.
def addMoreFoodByVendorId(menu, vendorId):
    with con:
        cur = con.cursor()
        i = 0
        for item in menu['itemName']:
            cur.execute("INSERT INTO MENU(vendor_id,item_name,price) values (%s,%s,%s)",
                        (vendorId, item, menu['price'][i]))
            i = i + 1

# Method is used to fetch orders placed by customers to a particular vendor from orders table by providing vendorId.
def getFoodOrdersByVendorId(vendorId):
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT orders.`order_id`,customers.name,customers.`contact`,customers.email,"
            "addresses.`flat_no`,addresses.`building`,addresses.`area`,addresses.`street`,addresses.`city`, "
            "orders.`order_time` FROM orders JOIN customers ON orders.`cust_id`= customers.`cust_id` "
            "JOIN addresses ON customers.`address_id`=addresses.`address_id` WHERE orders.`vendor_id`=%s AND orders.`isAccepted`=0",
            (vendorId))
        orders = cur.fetchall()
        return orders

# Method is used to get details of order placed from items_list table by providing orderId.
def getOrderDescriptionByOrderId(orderId):
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT orders.`order_id`,menu.`item_name`,menu.`price`,items_list.`quantity`,menu.price*items_list.`quantity` AS amount "
            "FROM orders JOIN items_list ON orders.`list_id`=items_list.`list_id` "
            "JOIN menu ON items_list.`item_id`=menu.`item_id` WHERE orders.`order_id`=%s",
            (orderId))
        orderDetails = cur.fetchall()
        return orderDetails

# Method is used to update the isAccepted column from orders table if vendor accepts any order.
# Takes orderId as parameter
def updateAcceptedOrder(orderId):
    with con:
        cur = con.cursor()
        cur.execute(
            "UPDATE orders SET isAccepted = 1 WHERE order_id=%s",
            (orderId))

# Method is used to delete the order from orders table if vendor rejects any order.
# Takes orderId as parameter
def deleteRejectedOrder(orderId):
    with con:
        cur = con.cursor()
        cur.execute(
            "DELETE from orders WHERE order_id=%s",
            (orderId))
