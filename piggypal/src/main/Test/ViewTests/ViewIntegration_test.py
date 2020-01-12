import os
import cherrypy
import requests
from contextlib import contextmanager
from Views.Login_button import Login_button as lb
from utils import SRC_DIR
from Test.run_testserver import run_server
conf = os.path.join(os.path.join(SRC_DIR, "Configs"), "Server.conf")

"""
Contains Tests for View
"""


@contextmanager
def run_server():
    """
    Starts cherrypy engine to run tests in proper environment
    """
    cherrypy.config.update({'global': {'server.socket_host': "127.0.0.1", 'server.socket_port': 4710}})
    cherrypy.tree.mount(lb(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()


def test_index():
    """
    Fails if request on "/" errors
    """

    with run_server():
        url = "http://127.0.0.1:4710/"
        r = requests.get(url)
        assert r.status_code == 200


def test_button():
    """
    Test for Code loss during request handling
    """
    url = "http://127.0.0.1:4710/"
    with run_server():
        r = requests.get(url)
        # "PiggyPal Button.html" contains working HTML sourcecode before script execution
        f = open(SRC_DIR + "/Test/ViewTests/PiggyPal Button.html", "r")
        html = r.text
        content = f.read()
        html = html.replace(" ", "")
        html = html.replace("\n", "")
        content = content.replace(" ", "")
        content = content.replace("\n", "")
        r.close()
        f.close()
        assert html == content
