import cherrypy, sys, os
from cherrypy.test import helper
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../.."))
from src.main.Views.Login_button import Login_button as lb
from contextlib import contextmanager
import requests


@contextmanager
def run_server():
    cherrypy.config.update({'global': {'server.socket_host': "127.0.0.1", 'server.socket_port': 4710}})
    cherrypy.tree.mount(lb(), "/", "")
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()


@staticmethod
def _setup():
    cherrypy.tree.mount(lb(), "/", "")
    cherrypy.config.update('Configs/Server.conf')


class ViewIntegrationTests(helper.CPWebCase):

    def test_index(self):
        """
        Fails if request on "/" errors
        """

        with run_server():
            url = "http://127.0.0.1:4710/"
            r = requests.get(url)
            print(r.status_code)
            self.assertEqual(r.status_code, 200)

    def test_button(self):
        """
        Fails if returned object varys != Paypal Login button
        """
        url = "http://127.0.0.1:4710/"
        with run_server():
            r = requests.get(url)
            print(r.content)
            f = open("PiggyPal Button.html", "r")
            html = r.text
            content = f.read()
            html = html.replace(" ", "")
            html = html.replace("\n", "")
            content = content.replace(" ", "")
            content = content.replace("\n", "")
            r.close()
            f.close()
            self.assertEqual(html, content)
