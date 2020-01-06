import cherrypy, requests, re
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

#Fixed Sandbox variables -> have to be separately obtained by live application for each user
sandbox_client_id = "AcMTMpvdMv1KMcweEIO_-KXrs4Y7AkHduqkf6r6u_e6-juZ1ZUxiP3QZIGp99zWba09_2AcihuENUgAR"
sandbox_transaction_url = "https://api.sandbox.paypal.com/v1/reporting/transactions"
sandbox_token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
sandbox_client_secret = "EIJGGRdItg83VE3mh0FIJ-9mR_Jd7ak4adK29VlZ4ygVETofhfr1PGG6afutUyoUj2rS7D6m69_gBrGG"

#Internet Date/Time Format
dt_pattern = re.compile("^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])[T,t]([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)([.][0-9]+)?([Zz]|[+-][0-9]{2}:[0-9]{2})$")

@cherrypy.expose
class Paypal_cred_listener(object):
    """
    Listens for Credentials being transmitted after successful "connect w/ paypal"
    """

    @cherrypy.tools.json_in()
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, code, scope, **kwargs):
        self._auth_code = code

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self):
        """
        Returns the current Authorization and erases confidential info from variables there-after
        """
        _auth_code = self._auth_code
        del self._auth_code
        return _auth_code


@cherrypy.expose
class Paypal_stub(object):
    """
    A stub class to communicate with the PayPal OAuth2 API as if it was a simple non-remote RESTful database
    """

    #This stub is easily expandable for whatever OAuth service is desired. For now Paypal is hardcoded.
    transaction_url = sandbox_transaction_url # TODO: change this class var once app goes live

    def __init__(self):
        self._token = {
            "access_token": "",
            "refresh_token": "",
            "token_type": "Bearer",
            "expires_in": "-30"
        }
        self.token_url = sandbox_token_url
        self._extra_info = {"Authorization": ""}
        self._client_id = sandbox_client_id # TODO: change when going live
        self._client_secret = sandbox_client_secret # TODO: see above
        
    def token_saver(self, token):
        self._token = token

    def _getAuthorization(self) -> str:
        """
        Returns User Authorization from Piggypal Credential Listener
        
        CAUTION: Due to privacy enhancements authorization can only be called ONCE per Session!
        """
        auth_code = requests.delete("http://localhost:4710/piggypal-listens")
        auth_code.raise_for_status()
        auth = HTTPBasicAuth(self._client_id, self._client_secret)
        client = BackendApplicationClient(client_id=self._client_id)
        oauth = OAuth2Session(client=client)
        return oauth.fetch_token(token_url=self.token_url, auth=auth, kwargs={"code": auth_code})
 
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, start_date:'Internet Date/Time Format', end_date:'Internet Date/Time Format', **request_kwargs:dict) -> dict:
        """
        Fetches Transaction History from PayPal API via OAuth2 communication

        - `start_date` and `end_date` should be provided in Internet Date/Time Format (https://tools.ietf.org/html/rfc3339#section-5.6)
        - Fine-tuning in requests can be done via options specified in https://developer.paypal.com/docs/api/sync/v1/.
        """

        if not self._token["access_token"]:
            self._token = self._getAuthorization()

        client = OAuth2Session(
            client_id=self._client_id,
            token=self._token,
            auto_refresh_url=self.token_url,
            auto_refresh_kwargs=self._extra_info,
            token_updater=self.token_saver
        )
        
        response = client.get(self.transaction_url, params={"page"=1, **request_kwargs})
        return response.json()    

if __name__ == '__main__': # pragma: no cover
    cherrypy.tree.mount(Paypal_stub(), '/piggypal', 'Configs/piggypal.conf')
    cherrypy.tree.mount(Paypal_cred_listener(), '/piggypal-listens', 'Configs/piggypal.conf')
    cherrypy.config.update('Configs/Server.conf')
    cherrypy.engine.start()
    #possible testing-request: curl -v -X GET "http://127.0.0.1:4710/piggypal?start_date=2019-12-01t00:00:01.0%2B00:00&end_date=2019-12-24t00:00:01.0-23:00"
    #Do not forget to inject the authorization code into piggypal-listens before you trigger /piggypal
