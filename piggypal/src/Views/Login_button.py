import cherrypy

class Login_button(object):
    @cherrypy.expose
    def GET(self):
        return open('Views/login.html')
