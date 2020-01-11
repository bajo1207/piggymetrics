import os
import cherrypy
import requests
from cherrypy.test import helper
from contextlib import contextmanager
from Models.Paypal_api_stub import Paypal_cred_listener as pcl, Paypal_stub as ps
from utils import SRC_DIR

conf = os.path.join(os.path.join(SRC_DIR, "Configs"), "piggypal.conf")


@contextmanager
def run_server():
    """
    Starts cherrypy engine to run tests in proper environment
    """
    cherrypy.config.update({'global': {'server.socket_host': "127.0.0.1", 'server.socket_port': 4710}})
    cherrypy.tree.mount(ps(), '/piggypal', conf)
    cherrypy.tree.mount(pcl(), '/piggypal-listens', conf)
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()


class ModelUnitTests(helper.CPWebCase):
    """
    Contains Unit Tests for Model
    """
    def test_credential_listener_get(self):
        """
        Checks if GET saves Paypal Authorization Code
        """
        listener = pcl()
        teststring = "teststring"
        listener.GET(code=teststring, scope="")
        self.assertEqual(listener._auth_code, teststring)

    def test_credential_listener_delete(self):
        """
        Checks is DELETE returns _auth_code and removes _auth_code object

        Since _auth_code only exists once per session the object should be deleted after getting it.
        """
        listener = pcl()
        teststring = "teststring"
        listener.GET(code=teststring, scope="")
        auth_code = listener._auth_code
        self.assertEqual(auth_code, teststring)
        auth_code = listener.DELETE()
        self.assertEqual(auth_code, teststring)
        try:
            auth_code = listener._auth_code
        except AttributeError:
            pass
        else:
            self.assertNotEqual(auth_code, listener._auth_code)

    def test_token_saver(self):
        """
        Asserts proper token saving
        """
        assertion_token = "TokenTest"
        stub = ps()
        stub._token_saver(token=assertion_token)
        self.assertEqual(stub._token, assertion_token)


class ModelSandboxUnitTest(helper.CPWebCase):
    """
    Contains Unit Tests for Model

    ! This Test suite only targets the Paypal Sandbox Environment.
    """

    def test_stub_init_sandbox(self):
        """
        Checks if Paypal Stub is properly initialized

        This test uses sandbox variables for client_id and client_secret
        """
        stub = ps()
        token = {
            "access_token": "",
            "refresh_token": "",
            "token_type": "Bearer",
            "expires_in": "-30"
        }
        self.assertEqual(stub._token, token)
        self.assertEqual(stub.token_url, "https://api.sandbox.paypal.com/v1/oauth2/token")
        self.assertEqual(stub._extra_info, {"Authorization": ""})
        self.assertEqual(stub._client_id,
                         "AcMTMpvdMv1KMcweEIO_-KXrs4Y7AkHduqkf6r6u_e6-juZ1ZUxiP3QZIGp99zWba09_2AcihuENUgAR")
        # TODO: change _client_id assert once live
        self.assertEqual(stub._client_secret,
                         "EIJGGRdItg83VE3mh0FIJ-9mR_Jd7ak4adK29VlZ4ygVETofhfr1PGG6afutUyoUj2rS7D6m69_gBrGG")
        # TODO: change client secret assert once live


    def test_stub_getAuthorization(self):
        """
        Check if _getAuthorization returns correct token format

        This test uses a sandbox variable for auth_code.
        It is possible that the given Authentication code will expire in the near future and has to be replaced.
        """
        with run_server():
            stub = ps()
            auth_code = "C21AAFz4MLiqcHFKYwgvdPf2FGNa1YhyUVF8SegZHYf7IPSCygY6pLZFFtO3u9Bh195eHyT-UJRzmajzVjQC0629dUHe36jgA"
            requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
            token = stub.getAuthorization()
            self.assertTrue("access_token" in token)
            self.assertTrue("token_type" in token)
            self.assertTrue("expires_in" in token)
            self.assertTrue("scope" in token)

    def test_stub_get_incorrect_date_handling(self):
        """
        Assert wrong Date Format raises Error
        """
        try:
            stub = ps()
            stub.GET("worngFormat", "definitlyNoValidDate")
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_stub_get_correct_date_handling(self):
        """
        Check if proper Date Format will be accepted

        This test uses a sandbox variable for auth_code.
        It is possible that the given Authentication code will expire in the near future and has to be replaced.
        """
        with run_server():
            try:
                auth_code = "C21AAFz4MLiqcHFKYwgvdPf2FGNa1YhyUVF8SegZHYf7IPSCygY6pLZFFtO3u9Bh195eHyT-UJRzmajzVjQC0629dUHe36jgA"

                requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
                requests.get("http://localhost:4710/piggypal",
                             params={"start_date": "2019-12-12T12:00:00.00Z", "end_date": "2020-01-10T12:00:00.00Z"})

            except AttributeError:
                self.assertTrue(False)
            else:
                self.assertTrue(True)


class ModelSandboxIntegrationTest(helper.CPWebCase):
    """
    Contains Integration Tests for Model

    ! This Test suite only targets the Paypal Sandbox Environment.
    """
    def test_stub_get_response(self):
        """
        Check if response from Paypal contains Transaction details

        This test uses a sandbox variable for auth_code.
        It is possible that the given Authentication code will expire in the near future and has to be replaced.
        """
        with run_server():
            auth_code = "C21AAFz4MLiqcHFKYwgvdPf2FGNa1YhyUVF8SegZHYf7IPSCygY6pLZFFtO3u9Bh195eHyT-UJRzmajzVjQC0629dUHe36jgA"

            requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
            response = requests.get("http://localhost:4710/piggypal", params={"start_date": "2019-12-12T12:00:00.00Z", "end_date": "2020-01-10T12:00:00.00Z"})

            self.assertTrue("transaction_details" in response.text)


