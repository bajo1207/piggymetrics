import cherrypy, requests, re
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import datetime
#tracing
from opencensus.trace.tracer import Tracer
from opencensus.trace import time_event as time_event_module
from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.status import Status
#monitoring
import time
from opencensus.ext.prometheus import stats_exporter as prometheus
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_key as tag_key_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.tags import tag_value as tag_value_module

# monitoring measures
# The latency in milliseconds
m_latency_ms = measure_module.MeasureFloat("repl_latency", "The latency in milliseconds per REPL loop", "ms")
#Views for Prometheus
stats_recorder = stats_module.stats.stats_recorder
key_method = tag_key_module.TagKey("method")
key_status = tag_key_module.TagKey("status")
key_error = tag_key_module.TagKey("error")
latency_view = view_module.View("demo_latency", "The distribution of the latencies",
    [key_method, key_status, key_error],
    m_latency_ms,
    # Latency in buckets:
    # [>=0ms, >=25ms, >=50ms, >=75ms, >=100ms, >=200ms, >=400ms, >=600ms, >=800ms, >=1s, >=2s, >=4s, >=6s]
    aggregation_module.DistributionAggregation([0, 25, 50, 75, 100, 200, 400, 600, 800, 1000, 2000, 4000, 6000]))


#zipkin specs
ze = ZipkinExporter(service_name="paypal-api-stub",
                                host_name='localhost',
                                port=9411,
                                endpoint='/api/v2/spans')
tracer = Tracer(exporter=ze, sampler=AlwaysOnSampler())

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
        """
        Receives the authorization code and the scope provided by the Paypal ReturnURL functionality from the "connect with paypal"-workflow
        """
        with tracer.span(name="credListenerGET") as span:
            self._auth_code = code
            span.status = Status(0, "Assigned one-time auth code")

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self):
        """
        Returns the current Authorization code and erases confidential info from local variables there-after
        """
        with tracer.span(name="credListenerDEL") as span:
            _auth_code = self._auth_code
            del self._auth_code
            span.status = Status(0, "Called and deleted auth code.")
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
        #prometheus setup
        mod_stats = stats_module.stats
        view_manager = mod_stats.view_manager
        exporter = prometheus.new_stats_exporter(prometheus.Options(namespace="oc_python", port=42069))
        view_manager.register_exporter(exporter)
        view_manager.register_view(latency_view)
        
    def _token_saver(self, token):
        with tracer.span(name="token_saver") as span:
            span.status = Status(0, "Token refreshed.")
            self._token = token

    def getAuthorization(self) -> str:
        """
        Returns User Authorization from Piggypal Credential Listener
        
        CAUTION: Due to privacy enhancements authorization can only be called ONCE per Session!
        """
        with tracer.span(name="get_authorization") as span:
            auth_code = requests.delete("http://localhost:4710/piggypal-listens")
            span.status = Status(0, "Fetched auth code")
            try:
                auth_code.raise_for_status()
            except:
                span.status = Status(15, "Auth code not retrieved correctly")
            auth = HTTPBasicAuth(self._client_id, self._client_secret)
            client = BackendApplicationClient(client_id=self._client_id)
            oauth = OAuth2Session(client=client)
            span.status = Status(0, "Fetching token from Paypal")
            return oauth.fetch_token(token_url=self.token_url, auth=auth, kwargs={"code": auth_code})
 
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, start_date:'Internet Date/Time Format'=None, end_date:'Internet Date/Time Format'=None, **request_kwargs:dict) -> dict:
        """
        Fetches Transaction History or Current Account Balance from PayPal API via OAuth2 communication

        - `start_date` and `end_date` should be provided in Internet Date/Time Format (https://tools.ietf.org/html/rfc3339#section-5.6)
        - if no dates are provided, the request will automatically be redirected to https://api.sandbox.paypal.com/v2/wallet/balance-accounts to fetch the current account balance.
        - Fine-tuning in requests can be done via options specified in https://developer.paypal.com/docs/api/sync/v1/.
        """
        with tracer.span(name="main_get_request") as span:
            start = time.time()
            transaction_url = self.transaction_url
            if not (start_date and end_date):
                span.status = Status(16, "Changing to fetching the account-balance is currently not supported.")
                transaction_url = "https://api.sandbox.paypal.com/v2/wallet/balance-accounts"
            elif not (dt_pattern.match(start_date) and dt_pattern.match(end_date)):
                span.status = Status(3, "Wrong date format or missing date.")
                raise ValueError("start_date or end_date are not in the right format.")

            if not self._token["access_token"]:
                span.status = Status(0, "Fetchin auth token")
                self._token = self.getAuthorization()

            try:
                span.status = Status(0, "Attempting request with token")
                client = OAuth2Session(
                    client_id=self._client_id,
                    token=self._token,
                    auto_refresh_url=self.token_url,
                    auto_refresh_kwargs=self._extra_info,
                    token_updater=self._token_saver
                )
            except:
                span.status = Status(2, "Something went wrong while requesting the refresh token")
            
            response = client.get(transaction_url, params={"start_date":start_date, "end_date":end_date, **request_kwargs})

            mmap = stats_recorder.new_measurement_map()
            end_ms = (time.time() - start) * 1000.0 # Seconds to milliseconds
            #record latency
            mmap.measure_float_put(m_latency_ms, end_ms)

            tmap = tag_map_module.TagMap()
            tmap.insert(key_method, tag_value_module.TagValue("repl"))
            tmap.insert(key_status, tag_value_module.TagValue("OK"))

            # Insert the tag map finally
            mmap.record(tmap)

            return response.json()    

if __name__ == '__main__': # pragma: no cover
    cherrypy.tree.mount(Paypal_stub(), '/piggypal', 'Configs/piggypal.conf')
    cherrypy.tree.mount(Paypal_cred_listener(), '/piggypal-listens', 'Configs/piggypal.conf')
    cherrypy.config.update('Configs/Server.conf')
    cherrypy.engine.start()
    #possible testing-request: curl -v -X GET "http://127.0.0.1:4710/piggypal?start_date=2019-12-01t00:00:01.0%2B00:00&end_date=2019-12-24t00:00:01.0-23:00"
    # or omit the dates and get the current balance
    #Do not forget to inject the authorization code into piggypal-listens before you trigger /piggypal


