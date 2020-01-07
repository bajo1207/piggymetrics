import cherrypy

#deprecated/ moved to view
class Piggypal_controller(object):
    @cherrypy.expose
    def GET(self):
        return open('Views/login.html')
