__author__ = 'khandave_g'

import web
import loginService

urls = (
  '/vendorLogin', 'VendorLogin',
  '/vendorRegister','VendorRegister',
  '/customerLogin', 'CustomerLogin',
  '/customerRegister', 'CustomerRegister',
  '/adminLogin', 'AdminLogin',
  '/registerCustomer', 'RegisterCustomer'
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
            sessionData['username'] = form.username
            return render.customerHome(session = sessionData)
        else:
            return "Invalid credentials"

class AdminLogin(object):
    def GET(self):
        return render.adminLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateAdmin(form.username, form.password):
            sessionData['username'] = form.username
            return render.adminHome(session = sessionData)
        else:
            return "Invalid credentials"


if __name__ == "__main__":
    app.run()
