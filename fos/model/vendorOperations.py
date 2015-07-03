__author__ = 'khandave_g'
# This file contains methods performing operations of vendor

from pymongo import MongoClient
from dbOperations import *

# Inserting vendor details to database
#parameters menu and customerReviews are of directory type having key value pair
def insertVendor(id,name,email,contact,username,password,menu,customerReviews):
    vendor = createVendorAccount()
    vendorDetails = {
        "_id":id,
        "name":name,
        "email":email,
        "contact":contact,
        "username":username,
        "password":password,
        "menu":menu,
        "customerReviews":customerReviews
    }

    vendor.insert_one(vendorDetails)


