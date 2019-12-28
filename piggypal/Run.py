from Controllers.example import exampleController
import cherrypy
from cherrypy import tools
import piggypal.Models.paypal_api_stub as piggypal

def start_server():
    cherrypy.tree.mount(exampleController(), '/', 'Configs/example.conf')
    cherrypy.tree.mount(piggypal.Paypal_stub(), '/piggypal', {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            #'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    })
    cherrypy.config.update('Server.conf')
    cherrypy.engine.start()
    #cherrypy.engine.block()

if __name__ == '__main__':
    start_server()