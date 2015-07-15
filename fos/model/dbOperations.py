__author__ = 'khandave_g'

import MySQLdb as mdb

con = mdb.connect('localhost', 'fos', 'root', 'fosDb')


def addVendor(name, contact, email, username, password, isActive, menu):
    with con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO VENDORS(name,contact,email,username, password,isActive) VALUES (%s,%s,%s,%s,%s,%d)",
            (name, contact, email,username,password,isActive))
        vendor_id = cur.execute("SELECT VENDOR_ID FROM VENDORS ORDER BY VENDOR_ID DESC LIMIT 1")
        for menuItem in menu:
            cur.execute("INSERT INTO MENU(vendor_id,item_name,price) values (%d,%s,%f)",
                        (vendor_id, menuItem.name, menuItem.price))



def addCustomer(name, contact, email, isRegistered, username, password, flat_no, building, street, area, city, state, pincode):
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO ADDRESSES(flat_no, building, street, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (flat_no, building, street, area, city, state, pincode))

        cur.execute("SELECT ADDRESS_ID FROM ADDRESSES ORDER BY ADDRESS_ID DESC LIMIT 1 ")
        address_id = cur.fetchone()

        cur.execute("INSERT INTO CUSTOMERS(name, contact, email, address_id, isRegistered, username, password)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (name, contact, email, address_id[0], isRegistered, username, password))


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


def getAllCustomersFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from customers")
        customerList = cur.fetchall()
        return customerList

def getRegisteredCustomer(username,password):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM CUSTOMERS WHERE USERNAME = %s AND PASSWORD = %s",(username,password))
        customer = cur.fetchone()
        print customer
        return customer

def getCustomerByCustomerID(customerID):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM CUSTOMERS WHERE cust_id = %s",(customerID))
        customer = cur.fetchone()
        return customer


def updateCustomerProfile(name,contact,email,username,password,customerId):
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("UPDATE CUSTOMERS SET name=%s, contact=%s, email=%s, username=%s, password=%s WHERE cust_id = %s",
                    (name,contact,email,username,password,customerId))


def getAddressByCustomerId(customerID):
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT ADDRESSES.* FROM ADDRESSES JOIN CUSTOMERS ON ADDRESSES.address_id = CUSTOMERS.address_id WHERE CUSTOMERS.cust_id = %s",
            (customerID))
        address = cur.fetchone()
        return address


def updateAddress(flat_no,building,street,area,city,state,pincode,addressId):
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("UPDATE ADDRESSES SET flat_no=%s, building=%s, street=%s, area=%s, city=%s, state=%s, pincode=%s WHERE address_id=%s",
                    (flat_no,building,street,area,city,state,pincode,addressId))