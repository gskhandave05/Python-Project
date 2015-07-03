__author__ = 'khandave_g'

from pymongo import MongoClient

def connectToDb():
    client = MongoClient()
    db = client["fosDb"]
    return db

def createCustomerAccount():
    db = connectToDb()
    customer = db["customers"]
    return customer

def createAdminAccount():
    db = connectToDb()
    admins = db["admins"]
    return admins

def createVendorAccount():
    db = connectToDb()
    vendors = db["vendors"]
    return vendors

