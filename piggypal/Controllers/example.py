import cherrypy
from Controllers.base import BaseController


class exampleController(BaseController):
    @cherrypy.expose
    def index(self):
        return self.render_template()