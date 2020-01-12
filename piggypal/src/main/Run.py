import cherrypy
from Views.Login_button import Login_button
from Models.Paypal_api_stub import Paypal_stub, Paypal_cred_listener



import os

def start_server():
    """
    Starts the services:
        - Index (/)
        - Paypal_stub (/piggypal)
        - Paypal_cred_listener (/piggypal-listens)
    """
    cherrypy.tree.mount(Login_button(), '/', '')
    cherrypy.tree.mount(Paypal_stub(), '/piggypal', 'Configs/piggypal.conf')
    cherrypy.tree.mount(Paypal_cred_listener(), '/piggypal-listens', 'Configs/piggypal.conf')
    cherrypy.config.update('Configs/Server.conf')
    cherrypy.engine.start()
    #cherrypy.engine.block()


if __name__ == '__main__': # pragma: no cover
    start_server()
