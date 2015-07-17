__author__ = 'khandave_g'

import web
import loginService
import json
import fos.model.dbOperations as fosdb


urls = (
  '/vendorLogin', 'VendorLogin','/vendorRegister','VendorRegister',
    '/logout','Logout','/vendorProfile','VendorProfile','/updateMenu','UpdateFoodMenu','/removeItem','RemoveItem',
    '/editItem','EditItem','/addMoreFoodMenu','AddMoreFoodMenu','/foodOrders','FoodOrders',
  '/orderDescription','OrderDescription','/acceptOrder','AcceptOrder','/rejectOrder','RejectOrder'
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

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'fosystem3@gmail.com'
web.config.smtp_password = 'fos12345'
web.config.smtp_starttls = True

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

class VendorRegister(object):
    def GET(self):
        return render.registerVendor()

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.addVendor(data['name'],data['contact'],data['email'],data['city'],data['username'],data['password'],"0",data['menu'])

class VendorProfile(object):
    def GET(self):
        vendorId = sessionData['userId']
        vendorProfile = fosdb.getVendorByVendorId(vendorId)
        return render.vendorProfile(profile = vendorProfile)

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        print data
        fosdb.updateVendorProfile(data['name'],data['contact'],data['email'],data['city'],data['username'],data['password'],data['vendorId'])

class UpdateFoodMenu(object):
    def GET(self):
        vendorId = sessionData['userId']
        vendorMenu = fosdb.getMenuByVendorId(vendorId)
        return render.vendorFoodMenu(menu = vendorMenu)

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
        return render.addMoreFood()

    def POST(self):
        vendorId = sessionData['userId']
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.addMoreFoodByVendorId(data,vendorId)

class FoodOrders(object):
    def GET(self):
        vendorId=sessionData['userId']
        orders = fosdb.getFoodOrdersByVendorId(vendorId)
        #print orders
        return  render.foodOrders(orders=orders)

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
        session.logged_in = False
        session.kill()
        raise web.seeother('/')

if __name__ == "__main__":
    app.run()