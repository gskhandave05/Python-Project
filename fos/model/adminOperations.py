__author__ = 'jhawar_p'
# This file contains methods performing operations of admin

from dbOperations import *

# Inserting admin details to database
def insetAdmin(adminId, name, email, username, password, contact):
    admin = createAdminAccount()
    adminDetails = {
        "_id" : adminId,
        "name": name,
        "email": email,
        "username": username,
        "password" : password,
        "contact": contact
    }

    admin.insert_one(adminDetails)
