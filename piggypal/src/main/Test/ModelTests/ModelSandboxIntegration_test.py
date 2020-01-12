import requests
from Test.run_testserver import run_server


"""
Contains Integration Tests for Model

! This Test suite only targets the Paypal Sandbox Environment.
"""
def test_stub_get_response():
    """
    Check if response from Paypal contains Transaction details

    This test uses a sandbox variable for auth_code.
    It is possible that the given Authentication code will expire in the near future and has to be replaced.
    """
    with run_server():
        auth_code = "C21AAHDIxiyrYK1LehrmxlR8lNy2T_rXv9KYgsK806lGziPqx0DU3SnbVBHJNZmuTefIX8nwbSs8KdKTrGHQ13S96WEzxPHZA"

        requests.get("http://localhost:4710/piggypal-listens", params={"code": auth_code, "scope": "openid"})
        response = requests.get("http://localhost:4710/piggypal", params={"start_date": "2019-12-12T12:00:00.00Z", "end_date": "2020-01-10T12:00:00.00Z"})

        assert ("transaction_details" in response.text)
