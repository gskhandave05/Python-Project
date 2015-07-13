__author__ = 'khandave_g'

import MySQLdb as mdb
def connectToDb():
    return mdb.connect('localhost', 'fos', 'root', 'fosdb')

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