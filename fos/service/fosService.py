__author__ = 'khandave_g'

import web
import loginService
import json
import fos.model.dbOperations as fosdb

urls = (
  '/vendorLogin', 'VendorLogin',
  '/vendorRegister','VendorRegister',
  '/customerLogin', 'CustomerLogin',
  '/adminLogin', 'AdminLogin',
  '/registerCustomer', 'RegisterCustomer',
  '/customerProfile','CustomerProfile',
  '/customerAddress','CustomerAddress',
  '/restaurantList','RestaurantList',
  '/foodMenu','FoodMenu'
)

app = web.application(urls, globals())

store = web.session.DiskStore('/var/www/sessions')

if web.config.get('_session') is None:
    session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'username':'anonymous','loggedin':False,'userId':0})
    web.config._session = session
else:
    session = web.config._session

sessionData = session._initializer
render = web.template.render('view/',globals={'session':sessionData,'username':sessionData['username'],'userId':sessionData['userId']})

class VendorLogin(object):
    def GET(self):
        return render.vendorLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateVendor(form.username,form.password):
            sessionData['username'] = form.username
            return render.vendorHome(session = sessionData)
        else:
            return "Invalid Credentials"

class CustomerLogin(object):
    def GET(self):
        return render.customerLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateCustomer(form.username, form.password):
            customer = fosdb.getRegisteredCustomer(form.username,form.password)
            print customer
            sessionData['username'] = customer[6]
            sessionData['customerID'] = customer[0]
            return render.customerHome(session = sessionData)
        else:
            return "Invalid credentials"


class RegisterCustomer(object):
    def GET(self):
        print "Inside GET"
        return render.customerRegisteration()

    def POST(self):
        print "inside post"
        form = web.data()
        data = json.loads(form)
        print data
        fosdb.addCustomer(data['name'],data['contact'],data['email'],"1",data['userName'],data['password'],
                          data['flat_no'],data['building'],data['street'],data['area'],data['city'],data['state'],data['pincode'])
        print "done!!"

class CustomerProfile(object):
    def GET(self):
        print "inside customerProfile GET"
        customerID = sessionData['customerID']
        customerProfile = fosdb.getCustomerByCustomerID(customerID)
        print customerID
        return render.customerProfile(profile = customerProfile)

    def POST(self):
        form = web.data()
        data = json.loads(form)
        fosdb.updateCustomerProfile(data['name'],data['contact'],data['email'],data['username'],data['password'],data['customerId'])

class CustomerAddress(object):
    def GET(self):
        customerID = sessionData['customerID']
        customerAddress = fosdb.getAddressByCustomerId(customerID)
        return render.customerAddress(address = customerAddress)

    def POST(self):
        form = web.data()
        data = json.loads(form)
        fosdb.updateAddress(data['flat_no'],data['building'],data['street'],data['area'],data['city'],data['state'],data['pincode'],data['address_id'])

class RestaurantList(object):
    def POST(self):
        # return vendors list acc. to city
        form = web.input(city=None)
        city = form.city
        vendors = fosdb.getAllVendorsByCity(city)
        return render.restaurantsList(restaurants = vendors)

class FoodMenu(object):
    def GET(self):
        form = web.input(asdf = None)
        vendorId = form.asdf
        menu = fosdb.getMenuByVendorId(vendorId)
        print menu
        return render.foodMenu(menu = menu)

class AdminLogin(object):
    def GET(self):
        return render.adminLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateAdmin(form.username, form.password):
            sessionData['username'] = form.username
            vendors = fosdb.getAllVendorsFromDb()
            return render.adminHome(session = sessionData, vendorData = vendors)
        else:
            return "Invalid credentials"


if __name__ == "__main__":
    app.run()
