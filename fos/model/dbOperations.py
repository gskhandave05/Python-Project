__author__ = 'khandave_g'

import MySQLdb as mdb

def connectToDb():
    return mdb.connect('localhost', 'fos', 'root', 'fosDb')


def addVendor(name, contact, email, username, password, isActive, menu):
    con = connectToDb()
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
    con = connectToDb()
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO ADDRESSES(flat_no, building, street, area, city, state, pincode) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (flat_no, building, street, area, city, state, pincode))

        cur.execute("SELECT ADDRESS_ID FROM ADDRESSES ORDER BY ADDRESS_ID DESC LIMIT 1 ")
        address_id = cur.fetchone()

        cur.execute("INSERT INTO CUSTOMERS(name, contact, email, address_id, isRegistered, username, password)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (name, contact, email, address_id[0], isRegistered, username, password))


def getAllAdminsFromDb():
    con = connectToDb()
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from admins")
        adminList = cur.fetchall()
        return adminList


def getAllVendorsFromDb():
    con = connectToDb()
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from vendors")
        vendorsList = cur.fetchall()
        return vendorsList


def getAllCustomersFromDb():
    con = connectToDb()
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select * from customers")
        customerList = cur.fetchall()
        return customerList