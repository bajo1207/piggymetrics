import cherrypy, sys, os
from cherrypy.test import helper
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../.."))
from main.Views.Login_button import Login_button as lb




class ViewIntegrationTests(helper.CPWebCase):
    @staticmethod
    def _setup():
        cherrypy.tree.mount(lb(), "/", "")
        cherrypy.config.update('Configs/Server.conf')

    def test_index(self):
        """
        Fails if request on "/" errors
        """
        self.getPage("http://127.0.0.1:4710/")
        self.assertStatus('200 OK')

    def test_button(self):
        """
        Fails if returned object varys != Paypal Login button
        """
        url = "http://127.0.0.1:4710/"
        self.getPage(url, method='GET')
        f = open("Views/login.html", "r")
        self.assertBody(f)

