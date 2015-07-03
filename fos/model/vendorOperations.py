__author__ = 'khandave_g'
# This file contains methods performing operations of vendor

from pymongo import MongoClient

def createVendorAccount(name,email,contact,username,password,menu,customerReviews):
    employees = db["vendors"]


