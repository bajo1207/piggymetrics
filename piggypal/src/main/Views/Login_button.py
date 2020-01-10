import cherrypy
from utils import get_project_root


class Login_button(object):
    @cherrypy.expose
    def index(self):
        src = get_project_root()
        return open(src + "/main/Views/login.html")
