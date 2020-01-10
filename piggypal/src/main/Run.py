import cherrypy
from main.Views.Login_button import Login_button
from main.Models.Paypal_api_stub import Paypal_stub, Paypal_cred_listener

import os

def start_server():
    cherrypy.tree.mount(Login_button(), '/', '')
    cherrypy.tree.mount(Paypal_stub(), '/piggypal', 'Configs/piggypal.conf')
    cherrypy.tree.mount(Paypal_cred_listener(), '/piggypal-listens', 'Configs/piggypal.conf')
    cherrypy.config.update('Configs/Server.conf')
    cherrypy.engine.start()
    #cherrypy.engine.block()

if __name__ == '__main__': # pragma: no cover
    start_server()
