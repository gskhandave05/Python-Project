__author__ = 'khandave_g'

import fos.model.dbOperations as fosdb

def authenticateAdmin(username,password):
    admins = fosdb.getAllAdminsFromDb()
    isValid = False
    for admin in admins:
        if username == admin["username"] and password == admin["password"]:
            isValid = True

    return isValid

def authenticateVendor(username,password):
    vendors = fosdb.getAllVendorsFromDb()
    isValid = False
    for vendor in vendors:
        if username == vendor["username"] and password == vendor["password"]:
            if vendor["isActive"]:
                isValid = True

    return isValid

def authenticateCustomer(username,password):
    customers =fosdb.getAllCustomersFromDb()
    isValid = False
    for customer in customers:
        if username == customer["username"] and password == customer["password"]:
            if customer["isRegistered"]:
                isValid = True

    return isValid


