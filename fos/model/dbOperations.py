__author__ = 'khandave_g'

import MySQLdb as mdb

con=mdb.connect('localhost', 'fos', 'root', 'fosdb')

def addVendor(name, contact, email, username, password, isActive, menu):
    with con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO VENDORS(name,contact,email,username, password,isActive) VALUES (%s,%s,%s,%s,%s,%s)",
            (name, contact, email,username,password,isActive))

    addMenu(menu)

def addMenu(menu):
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT VENDOR_ID FROM VENDORS ORDER BY VENDOR_ID DESC LIMIT 1")
        vendorId=cur.fetchone()
        for item in menu:
            i=0
            for itemName in menu[0]['itemName']:
                cur.execute("INSERT INTO MENU(vendor_id,item_name,price) values (%s,%s,%s)",
                        (vendorId['VENDOR_ID'], itemName, item['price'][i]))
                i=i+1

def getAllAdminsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from admins")
        adminList = cur.fetchall()
        return adminList

def getAllVendorsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from vendors")
        vendorsList = cur.fetchall()
        return vendorsList

def getRegisteredVendor(username,password):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VENDORS WHERE USERNAME = %s and password = %s",(username,password))
        vendor = cur.fetchone()
        return vendor

def getVendorByVendorId(vendorId):
     with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM VENDORS WHERE vendor_id = %s",(vendorId))
        vendor = cur.fetchone()
        return vendor

def updateVendorProfile(name, contact, email, username, password,vendorId):
    with con:
        cur = con.cursor()
        cur.execute(
            "UPDATE vendors SET name = %s, contact = %s, email = %s, username = %s,password = %s where vendor_id = %s",
            (name, contact, email,username,password,vendorId))

def getMenuByVendorId(vendorId):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM MENU WHERE vendor_id = %s",(vendorId))
        menu = cur.fetchall()
        return menu

def removeFoodItem(itemCode):
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM MENU WHERE ITEM_ID = %s",(itemCode))

def updateFoodItem(vendorId,itemCode,itemName,price):
    with con:
        cur = con.cursor()
        cur.execute(
            "UPDATE MENU SET vendor_id = %s, item_id = %s, item_name = %s, price = %s WHERE item_id=%s",
            (vendorId,itemCode,itemName,price,itemCode))

def getItemByItemId(itemCode):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM MENU WHERE item_id = %s",(itemCode))
        item = cur.fetchone()
        return item

def addMoreFoodByVendorId(menu,vendorId):
    with con:
        cur = con.cursor()
        i=0
        for item in menu['itemName']:
            cur.execute("INSERT INTO MENU(vendor_id,item_name,price) values (%s,%s,%s)",
                        (vendorId, item, menu['price'][i]))
            i=i+1