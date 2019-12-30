import cherrypy, requests, re
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session

#Fixed Sandbox variables -> have to be separately obtained by live application for each user
sandbox_client_id = "AcMTMpvdMv1KMcweEIO_-KXrs4Y7AkHduqkf6r6u_e6-juZ1ZUxiP3QZIGp99zWba09_2AcihuENUgAR"
sandbox_client_secret = "EIJGGRdItg83VE3mh0FIJ-9mR_Jd7ak4adK29VlZ4ygVETofhfr1PGG6afutUyoUj2rS7D6m69_gBrGG"
sandbox_auth_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
sandbox_transaction_url = "https://api.sandbox.paypal.com/v1/reporting/transactions"

#Internet Date/Time Format
dt_pattern = re.compile("^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])[T,t]([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)([.][0-9]+)?([Zz]|[+-][0-9]{2}:[0-9]{2})$")


@cherrypy.expose
class Paypal_stub(object):
    """
    A stub class to communicate with the PayPal OAuth2 API as if it was a simple non-remote RESTful database
    """

    #This stub is easily expandable for whatever OAuth service is desired. For now Paypal is hardcoded.
    auth_url = sandbox_auth_url # TODO: change this class var once app goes live
    transaction_url = sandbox_transaction_url # TODO: see above

    def __init__(self):
        self._client_id, self._client_secret = self._getClientIdAndSecret()
        self._token = self._getOauthToken(self._client_id, self._client_secret)
        
    def _getClientIdAndSecret(self) -> {str, str}:
        """
        Leads the User to a PayPal Auth Site and fetches authorized values for client_id and secret for a Session

        Returns values as strings in a list. Does not alter class or object variables.
        """
        # TODO: once the app goes live, this function should lead to the Paypal Auth screen
        # ! Have Privacy in Mind
        return sandbox_client_id, sandbox_client_secret

    def _getOauthToken(self, client_id, client_secret) -> dict:
        """
        Requests an OAuth2 Token for provided client id and secret from the Paypal API
        """

        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.auth_url,
            client_id=client_id,
            client_secret=client_secret
        )
        return token
 
    @cherrypy.tools.json_in()
    #@cherrypy.tools.json_out()
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, start_date:'Internet Date/Time Format', end_date:'Internet Date/Time Format', **request_kwargs:dict) -> dict:
        """
        Fetches Transaction History from PayPal API via OAuth2 communication

        - `start_date` and `end_date` should be provided in Internet Date/Time Format (https://tools.ietf.org/html/rfc3339#section-5.6)
        - Fine-tuning in requests can be done via options specified in https://developer.paypal.com/docs/api/sync/v1/.
        """
        if not (start_date and end_date):
            data = cherrypy.request.json
            start_date = data["start-date"]
            end_date = data["end_date"]

        if not (dt_pattern.match(start_date) and dt_pattern.match(end_date)):
            raise ValueError("start_date or end_date are not in the right format.")
        try:
            client = OAuth2Session(client_id=self._client_id, token=self._token)
            response = client.get(self.transaction_url, params={"start_date":start_date, "end_date":end_date, **request_kwargs})
        except TokenExpiredError as tee:
            self._token = self._getOauthToken(self._client_id, self._client_secret)
            client = OAuth2Session(client_id=self._client_id, token=self._token)
            response = client.get(self.transaction_url, **request_kwargs)
        #TODO format response as JSON
        return response
        

    # TODO Define automatic Token refresh & update
    # TODO Then update getTransactionHistory(...) and omit try...except...
    # # (https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#third-recommended-define-automatic-token-refresh-and-update)
    def _refreshToken(self):
        pass

if __name__ == '__main__': # pragma: no cover
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            #'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(Paypal_stub(), '/', conf)
    """
    stub = Paypal_stub()
    print("Token: " + str(stub._token))
    history = stub.getTransactionHistory(start_date="2019-12-01t00:00:01.0+00:00", end_date="2019-12-24t00:00:01.0-23:00")
    print("History type: " + str(type(history)),
    "History content: " + str(history.json()))
    """