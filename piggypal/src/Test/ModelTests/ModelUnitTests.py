import cherrypy

import cherrypy.test

from ...main.Models.Paypal_api_stub import Paypal_cred_listener as pcl, Paypal_stub as ps

class ModelUnitTests(object):
    def TestTokenSaver(self):
        