__author__ = 'jhawar_p'
# This file contains methods performing operations of admin

from dbOperations import *

# Inserting admin details to database
def insetAdmin(_id, name, email, username, password, contact):
    admin = createAdminAccount()
    adminDetails = {
        "_id" : _id,
        "name": name,
        "email": email,
        "username": username,
        "password" : password,
        "contact": contact
    }

    admin.insert_one(adminDetails)
