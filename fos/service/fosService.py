__author__ = 'khandave_g'

import web
import loginService
import json
import fos.model.dbOperations as fosdb

urls = (
  '/vendorLogin', 'VendorLogin','/vendorRegister','VendorRegister',
    '/logout','Logout','/vendorProfile','VendorProfile','/updateMenu','UpdateFoodMenu','/removeItem','RemoveItem',
    '/editItem','EditItem','/addMoreFoodMenu','AddMoreFoodMenu'
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
            vendor = fosdb.getRegisteredVendor(form.username,form.password)
            sessionData['username'] = vendor[4]
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
        fosdb.addVendor(data['name'],data['contact'],data['email'],data['username'],data['password'],"0",data['menu'])

class VendorProfile(object):
    def GET(self):
        vendorId = sessionData['userId']
        vendorProfile = fosdb.getVendorByVendorId(vendorId)
        return render.vendorProfile(profile = vendorProfile)

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        print data
        fosdb.updateVendorProfile(data['name'],data['contact'],data['email'],data['username'],data['password'],data['vendorId'])

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


class Logout(object):
    def GET(self):
        session.logged_in = False
        session.kill()
        raise web.seeother('/')

if __name__ == "__main__":
    app.run()