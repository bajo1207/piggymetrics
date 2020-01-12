from Models.Paypal_api_stub import Paypal_cred_listener as pcl, Paypal_stub as ps


"""
Contains Unit Tests for Model
"""


def test_credential_listener_get():
    """
    Checks if GET saves Paypal Authorization Code
    """
    listener = pcl()
    teststring = "teststring"
    listener.GET(code=teststring, scope="")
    assert listener._auth_code == teststring


def test_credential_listener_delete():
    """
    Checks is DELETE returns _auth_code and removes _auth_code object

    Since _auth_code only exists once per session the object should be deleted after getting it.
    """
    listener = pcl()
    teststring = "teststring"
    listener.GET(code=teststring, scope="")
    auth_code = listener._auth_code
    assert auth_code == teststring
    auth_code = listener.DELETE()
    assert auth_code == teststring
    try:
        auth_code = listener._auth_code
    except AttributeError:
        pass
    else:
        assert auth_code != listener._auth_code

def test_token_saver():
    """
    Asserts proper token saving
    """
    assertion_token = "TokenTest"
    stub = ps()
    stub._token_saver(token=assertion_token)
    assert stub._token == assertion_token







