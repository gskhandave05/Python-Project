__author__ = 'khandave_g'

import web
import loginService

urls = (
  '/vendorLogin', 'VendorLogin','/vendorRegister','VendorRegister'
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


if __name__ == "__main__":
    app.run()