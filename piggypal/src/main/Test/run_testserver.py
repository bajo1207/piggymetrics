import os
import cherrypy
from contextlib import contextmanager
from Models.Paypal_api_stub import Paypal_cred_listener as pcl, Paypal_stub as ps
from utils import SRC_DIR
conf = os.path.join(os.path.join(SRC_DIR, "Configs"), "piggypal.conf")
testPort = 4710

@contextmanager
def run_server():
    """
    Starts cherrypy engine to run tests in proper environment
    """
    cherrypy.config.update({'global': {'server.socket_host': "127.0.0.1", 'server.socket_port': testPort}})
    cherrypy.tree.mount(ps(), '/piggypal', conf)
    cherrypy.tree.mount(pcl(), '/piggypal-listens', conf)
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()
