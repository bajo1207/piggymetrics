import cherrypy
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

#Fixed Sandbox variables -> have to be separately obtained by live application for each user
sandbox_client_id = "AcMTMpvdMv1KMcweEIO_-KXrs4Y7AkHduqkf6r6u_e6-juZ1ZUxiP3QZIGp99zWba09_2AcihuENUgAR"
sandbox_client_secret = "EIJGGRdItg83VE3mh0FIJ-9mR_Jd7ak4adK29VlZ4ygVETofhfr1PGG6afutUyoUj2rS7D6m69_gBrGG"
sandbox_auth_url = "https://api.sandbox.paypal.com/v1/oauth2/token"

class Paypal_stub(object):
    """
    A stub class to communicate with the PayPal OAuth2 API as if it was a simple non-remote RESTful DB
    """

    auth_url = sandbox_auth_url # TODO: change this class var once app goes live

    def __init__(self):
        #obtain OAuth2 Token
        self.client_id, self.client_secret = self.getClientIdAndSecret()
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(
            token_url=self.auth_url,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
    def getClientIdAndSecret(self) -> {str, str}:
        """
        Leads the User to a PayPal Auth Site and fetches authorized values for client_id and secret

        Returns values as strings in a list. Does not alter class or object variables.
        """
        # TODO: once the app goes live, this function should lead to the Paypal Auth screen
        # ! Have Privacy in Mind
        
        return sandbox_client_id, sandbox_client_secret

    @cherrypy.expose
    def getTransactionHistory(self) -> str:
        pass

if __name__ == '__main__':
   cherrypy.quickstart(Paypal_stub(), '/')