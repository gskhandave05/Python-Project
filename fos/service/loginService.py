__author__ = 'khandave_g'

import fos.model.dbOperations as fosdb
import MySQLdb as mdb

con = fosdb.connectToDb()

def getAdminsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select username,password from admins")
        adminList = cur.fetchall()
        return adminList

def getVendorsFromDb():
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("Select username,password,isActive from vendors")
        vendorsList = cur.fetchall()
        return vendorsList

def authenticateAdmin(username,password):
    admins = getAdminsFromDb()
    isValid = False
    for admin in admins:
        if username == admin["username"] and password == admin["password"]:
            isValid = True

    return isValid

def authenticateVendor(username,password):
    vendors = getVendorsFromDb()
    isValid = False
    for vendor in vendors:
        if username == vendor["username"] and password == vendor["password"]:
            if vendor["isActive"]:
                isValid = True

    return isValid