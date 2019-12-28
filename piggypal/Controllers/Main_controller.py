import cherrypy

class Piggypal_controller(object):
    @cherrypy.expose
    def index(self):
        return open('Views/index.html')