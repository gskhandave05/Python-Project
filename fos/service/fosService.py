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

# Code for enabling session storage. Used type is DiskStore.
store = web.session.DiskStore('/var/www/sessions')
if web.config.get('_session') is None:
    session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'username':'anonymous',
                                                         'loggedin':False,'userId':None})
    web.config._session = session
else:
    session = web.config._session
sessionData = session._initializer

# Code for rendering the html templates and
# declared the session variables globally so that they can be accessed directly in html templates.
render = web.template.render('view/',globals={'session':sessionData,'username':sessionData['username'],
                                              'userId':sessionData['userId']})

# Configuration code for using gmail as a SMTP server for sending mails using python.
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'fosystem3@gmail.com'
web.config.smtp_password = 'fos12345'
web.config.smtp_starttls = True

# Class for controlling vendor login operation.
# Gets vendor credentials from template and renders to vendorHome template if authenticated vendor is found.
class VendorLogin(object):
    def GET(self):
        return render.vendorLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateVendor(form.username,form.password):
            vendor = fosdb.getRegisteredVendor(form.username,form.password)
            sessionData['username'] = vendor[1]
            sessionData['userId'] = vendor[0]
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

# Class for controlling vendor register operation.
# Gets data from register form and sends the data to database.
class VendorRegister(object):
    def GET(self):
        return render.registerVendor()

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.addVendor(data['name'],data['contact'],data['email'],data['city'],data['username'],data['password'],"0",data['menu'])

# Class for controlling vendor profile related operations.
# Gets the vendor Id,sends it to database related methods,returns vendor profile object. Sends it to the template.
class VendorProfile(object):
    def GET(self):
        if sessionData['userId']!=None:
            vendorId = sessionData['userId']
            vendorProfile = fosdb.getVendorByVendorId(vendorId)
            return render.vendorProfile(profile = vendorProfile)
        else:
            return "<h1>You need to log in first.<h1>"

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        print data
        fosdb.updateVendorProfile(data['name'],data['contact'],data['email'],data['city'],data['username'],data['password'],data['vendorId'])

# Class for controlling the update food menu operations.
class UpdateFoodMenu(object):
    def GET(self):
        if sessionData['userId']!=None:
            vendorId = sessionData['userId']
            vendorMenu = fosdb.getMenuByVendorId(vendorId)
            return render.vendorFoodMenu(menu = vendorMenu)
        else:
            return "<h1>You need to log in first.<h1>"

class RemoveItem(object):
    def POST(self):
        form = web.input(buttonId=None)
        itemCode = form.buttonId
        print (itemCode)
        fosdb.removeFoodItem(itemCode)

class EditItem(object):
    def GET(self):
        form = web.input(buttonId=None)
        itemCode = form.buttonId
        foodItem = fosdb.getItemByItemId(itemCode)
        return render.editFoodItem(foodItem = foodItem)

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.updateFoodItem(data['vendorId'],data['itemId'],data['itemName'],data['price'])

class AddMoreFoodMenu(object):
    def GET(self):
        if sessionData['userId']!=None:
            return render.addMoreFood()
        else:
            return "Invalid credentials"

    def POST(self):
        vendorId = sessionData['userId']
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.addMoreFoodByVendorId(data,vendorId)

class FoodOrders(object):
    def GET(self):
        if sessionData['userId']!=None:
            vendorId=sessionData['userId']
            orders = fosdb.getFoodOrdersByVendorId(vendorId)
            return  render.foodOrders(orders=orders)
        else:
            return "<h1>You need to log in first.<h1>"

class OrderDescription(object):
    def GET(self):
        form = web.input(mailId=None,orderId=None)
        print form.mailId,form.orderId
        orderDetails = fosdb.getOrderDescriptionByOrderId(form.orderId)
        return render.orderDescription(orderDetails = orderDetails,mailId=form.mailId)

class AcceptOrder(object):
    def POST(self):
        form = web.data()
        data = json.loads(form)
        mailId = data['mailId']
        orderId = data['orderId']
        fosdb.updateAcceptedOrder(orderId)
        web.sendmail('fosystem3@gmail.com',mailId,'Order Accepted','Dear Customer,\nYour Order is accepted by Vendor.'
                                                                    '\nYou will receive a call from vendor soon.'
                                                                    '\nThank You.')

class RejectOrder(object):
    def POST(self):
        form = web.data()
        data = json.loads(form)
        mailId = data['mailId']
        orderId = data['orderId']
        #fosdb.deleteRejectedOrder(orderId)
        web.sendmail('fosystem3@gmail.com',mailId,'Order Rejected','Dear Customer,\nYour Order can not be processed by Vendor.'
                                                                    '\nWe are sorry for the inconvinience'
                                                                    '\nThank You.')

class Logout(object):
    def GET(self):
        sessionData['username']=None
        sessionData['userId']=None
        session._cleanup()
        session.kill()
        print sessionData['username']
        raise web.seeother('/')



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
