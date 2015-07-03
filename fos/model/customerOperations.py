__author__ = 'jhawar_p'

# This file contains methods performing operations of customer

from dbOperations import *

# Inserting customer details to database
# parameters menu and customerReviews are of directory type having key value pair
def registerCustomer(customerId, fname, lname, email, contact, address, username, password):
    customer = createCustomerAccount()
    customerDetails = {
        "_id": customerId,
        "fname": fname,
        "lname": lname,
        "email": email,
        "contact": contact,
        "address": address,
        "username": username,
        "password": password
    }

    customer.insert_one(customerDetails)


