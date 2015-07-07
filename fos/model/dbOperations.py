__author__ = 'khandave_g'

import MySQLdb as mdb


def connectToDb():
    return mdb.connect('localhost', 'fos', 'root', 'fosdb')


def addVendor(name, contact, email, username, password, isActive, menu):
    con = connectToDb()
    with con:
        cur = con.cursor()
        menu_id = cur.execute("SELECT MENU_ID FROM MENU ORDER BY MENU_ID DESC LIMIT 1")
        for menuItem in menu:
            cur.execute("INSERT INTO MENU(menu_id,item_name,price) values (%d,%s,%s)",
                        (menu_id + 1, menuItem.name, menuItem.price))
        cur.execute(
            "INSERT INTO VENDORS(name,contact,email,username, password,isActive,menu_id) VALUES (%s,%s,%s,%s,%s,%d,%d)",
            (name, contact, email,username,password,isActive, menu_id + 1))
