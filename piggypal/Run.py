from Controllers.example import exampleController
import cherrypy
from cherrypy import tools

def start_server():
    cherrypy.tree.mount(exampleController(), '/', 'Configs/example.conf')
    cherrypy.config.update('Server.conf')
    cherrypy.engine.start()
    #cherrypy.engine.block()

if __name__ == '__main__':
    start_server()