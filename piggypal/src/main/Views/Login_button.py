import cherrypy
from utils import SRC_DIR

class Login_button(object):
    @cherrypy.expose
    def index(self):
        """
        Returns the "connect with paypal"-button as valid HTML.
        Acts as Index page to piggypal
        """
        return open(SRC_DIR + "/main/Views/login.html")
