__author__ = 'khandave_g'

# importing Mongo db package for MongoClient
from pymongo import MongoClient

# creating connection with MongoClient
def connectToDb():
    client = MongoClient()
    db = client["fosDb"]
    return db

# creating customers Collection to fosDb
def getCustomersCollection():
    db = connectToDb()
    customer = db["customers"]
    return customer

# creating Admins collection to fosDb
def getAdminsCollection():
    db = connectToDb()
    admins = db["admins"]
    return admins

# creating Vendors collection to fosDb
def getVendorsCollection():
    db = connectToDb()
    vendors = db["vendors"]
    return vendors

# creating Orders collection to fosDb
def getOrdersCollection():
    db = connectToDb()
    orders = db["orders"]
    return orders

