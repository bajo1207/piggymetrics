import cherrypy
from utils import SRC_DIR


class Login_button(object):
    @cherrypy.expose
    def index(self):
        return open(SRC_DIR + "/main/Views/login.html")
