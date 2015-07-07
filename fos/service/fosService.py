__author__ = 'khandave_g'

import web
import loginService

urls = (
  '/vendorLogin', 'VendorLogin','/vendorRegister','VendorRegister'
)

app = web.application(urls, globals())

render = web.template.render('../view/')

class VendorLogin(object):
    def GET(self):
        return render.vendorLogin()

    def POST(self):
        form = web.input(username=None, password=None)
        if loginService.authenticateVendor(form.username,form.password):
            user = form.username
            return render.index(user = user.upper())
        else:
            return "Invalid Credentials"