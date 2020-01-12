import requests
from Models.Paypal_api_stub import Paypal_stub as ps
from Test.run_testserver import run_server


"""
Contains Unit Tests for Model

! This Test suite only targets the Paypal Sandbox Environment.
"""


def test_stub_init_sandbox():
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
    assert stub._token == token
    assert stub.token_url == "https://api.sandbox.paypal.com/v1/oauth2/token"
    assert stub._extra_info, {"Authorization": ""}
    assert stub._client_id == "AcMTMpvdMv1KMcweEIO_-KXrs4Y7AkHduqkf6r6u_e6-juZ1ZUxiP3QZIGp99zWba09_2AcihuENUgAR"
    # TODO: change _client_id assert once live
    assert stub._client_secret =="EIJGGRdItg83VE3mh0FIJ-9mR_Jd7ak4adK29VlZ4ygVETofhfr1PGG6afutUyoUj2rS7D6m69_gBrGG"
    # TODO: change client secret assert once live


def test_stub_getAuthorization():
    """
    Check if _getAuthorization returns correct token format

    This test uses a sandbox variable for auth_code.
    It is possible that the given Authentication code will expire in the near future and has to be replaced.
    """
    with run_server():
        stub = ps()
        auth_code = "C21AAHDIxiyrYK1LehrmxlR8lNy2T_rXv9KYgsK806lGziPqx0DU3SnbVBHJNZmuTefIX8nwbSs8KdKTrGHQ13S96WEzxPHZA"
        requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
        token = stub.getAuthorization()
        assert ("access_token" in token)
        assert ("token_type" in token)
        assert ("expires_in" in token)
        assert ("scope" in token)

def test_stub_get_incorrect_date_handling():
    """
    Assert wrong Date Format raises Error
    """
    try:
        stub = ps()
        stub.GET("worngFormat", "definitlyNoValidDate")
    except ValueError:
        assert (True)
    else:
        assert (False)

def test_stub_get_correct_date_handling():
    """
    Check if proper Date Format will be accepted

    This test uses a sandbox variable for auth_code.
    It is possible that the given Authentication code will expire in the near future and has to be replaced.
    """
    with run_server():
        try:
            auth_code = "C21AAHDIxiyrYK1LehrmxlR8lNy2T_rXv9KYgsK806lGziPqx0DU3SnbVBHJNZmuTefIX8nwbSs8KdKTrGHQ13S96WEzxPHZA"

            requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
            requests.get("http://localhost:4710/piggypal",
                         params={"start_date": "2019-12-12T12:00:00.00Z", "end_date": "2020-01-10T12:00:00.00Z"})

        except AttributeError:
            assert (False)
        else:
            assert (True)