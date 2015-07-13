__author__ = 'khandave_g'

import web
import loginService
import json
import fos.model.dbOperations as fosdb

urls = (
  '/vendorLogin', 'VendorLogin','/vendorRegister','VendorRegister',
    '/logout','Logout'
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

class VendorRegister(object):
    def GET(self):
        return render.RegisterVendor()

    def POST(self):
        rForm = web.data()
        data = json.loads(rForm)
        fosdb.addVendor(data['name'],data['contact'],data['email'],data['username'],data['password'],"0",data['menu'])


class Logout(object):
    def GET(self):
        session.logged_in = False
        session.kill()
        raise web.seeother('/')

if __name__ == "__main__":
    app.run()