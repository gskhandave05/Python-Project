__author__ = 'khandave_g'

# importing mongo db package for mongoclient
from pymongo import MongoClient

# creating connection with MongoClient
def connectToDb():
    client = MongoClient()
    db = client["fosDb"]
    return db

# creating customers Collection to fosDb
def createCustomerAccount():
    db = connectToDb()
    customer = db["customers"]
    return customer

# creating Admins collection to fosDb
def createAdminAccount():
    db = connectToDb()
    admins = db["admins"]
    return admins

# creating Vendors collection to fosDb
def createVendorAccount():
    db = connectToDb()
    vendors = db["vendors"]
    return vendors

