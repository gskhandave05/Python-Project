__author__ = 'khandave_g'
# This file contains methods performing operations of vendor

from dbOperations import *

# Inserting vendor details to database
#parameters menu and customerReviews are of directory type having key value pair
def insertVendor(id,name,email,contact,username,password,menu,customerReviews):
    vendor = getVendorsCollection()
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

def acceptOrder(orderId,customerId,customerName,contact,email,order):
    orders = getOrdersCollection()
    cust_order = {
        "_id":orderId,
        "customer_id":customerId,
        "customer_name":customerName,
        "contact":contact,
        "email":email,
        "order":order
    }
    orders.insert_one(cust_order)


