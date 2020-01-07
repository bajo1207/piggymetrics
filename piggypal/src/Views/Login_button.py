import cherrypy

class Login_button(object):
    @cherrypy.expose
    def index(self):
        return open('Views/login.html')
