import sys
import requests

from orijin_sdk.defaults import ENDPOINTS

def login_full(email: str, password: str, custom_endpoint = ENDPOINTS.brand_login):
    """
    Request a login token to the Orijin system.
    Returns a json of the response, which if successful should include a user token at ["data"]["token"]
    """
    try:
        r = requests.post(url=custom_endpoint, json={"email":email, "password":password})
    except Exception as e:
        print(e, sys.stderr)
    return r.json()

def login(email: str, password: str, custom_endpoint = ENDPOINTS.brand_login) -> str | None:
    """
    Request a login token to the Orijin system.
    Same as login_full(), but only the auth token is returned.
    """
    try:
        return login_full(email, password, custom_endpoint)["data"]["token"]
    except:
        return None

def register(
    email: str,
    phone: str,
    password: str,
    register_url: str = ENDPOINTS.consumer_register,
    firstName: str = "Made By",
    lastName: str = "Orijin-SDK (Python)",
    referralCode: str = "",
    purchaseToken: str = "",
    productRegisterID: str = "",
):
    try:
        r = requests.post(url=register_url, json={
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "password": password,
            "referralCode": referralCode,
            "purchaseToken": purchaseToken,
            "productRegisterID": productRegisterID
        })
    except Exception as e:
        print(e, sys.stderr)
    return r.json()
