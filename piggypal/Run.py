from Controllers.Main_controller import Piggypal_controller
import cherrypy
from cherrypy import tools
from Models.Paypal_api_stub import Paypal_stub, Paypal_cred_listener

def start_server():
    cherrypy.tree.mount(Piggypal_controller(), '/', '')
    cherrypy.tree.mount(Paypal_stub(), '/piggypal', 'Configs/piggypal.conf')
    cherrypy.tree.mount(Paypal_cred_listener(), '/piggypal-listens', 'Configs/piggypal.conf')
    cherrypy.config.update('Configs/Server.conf')
    cherrypy.engine.start()
    #cherrypy.engine.block()

if __name__ == '__main__': # pragma: no cover
    start_server()