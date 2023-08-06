from orijin_sdk.helpers.query_builder import me
from .defaults import ENDPOINTS
from .auth import login_full as login, register                             # Connection Manager
from .gql import useQueryAsOn, useMutationAsOn      # Connection Manager
from .types import APIs, User

#region: Connection Manager

class Connection:
    domain: str
    token: str | None
    endpoints: APIs
    user_data: User = None
    user_id: int = None

    def __init__(
        self, 
        domain: str = "https://staging.orijinplusserver.com", 
        token: str | None = None
    ):
        """Default values are hard-coded, not taken from the environment!"""
        self.domain = domain.strip('/')
        self.token = token
        self.endpoints = APIs(self.domain)
    
    def user(self) -> User | None:
        if (self.token == None): return None
        if (self.user_data != None): return self.user_data
        query, _, decoder = me()
        self.user_data = decoder(self.useQuery(query))
        return self.user_data

    def logout(self):
        self.user_id = None
        self.user_data = None
        self.token = None
        # TODO: Call logout to invalidate token from further use

    def brand_login(self, username: str, password: str) -> None:
        self.logout()
        r = login(username, password, self.endpoints.brand_login)
        try:
            self.token = r["data"]["token"]
            self.user_id = r["data"]["auther"]["id"]
        except:
            print("Failed to login, got:", r)
    
    def consumer_login(self, username: str, password: str) -> None:
        self.logout()
        r = login(username, password, self.endpoints.consumer_login)
        try:
            self.token = r["data"]["token"]
            self.user_id = r["data"]["auther"]["id"]
        except:
            print("Failed to login, got:", r)
    
    def login(self, username: str, password: str): 
        """Default login is assumed to be brand platform."""
        self.brand_login(username, password)

    def consumer_register(
        self, 
        email: str,
        phone: str,
        password: str,
        firstName: str = "Made By",
        lastName: str = "Orijin-SDK (Python)",
        referralCode: str = "",
        purchaseToken: str = "",
        productRegisterID: str = "",
    ):
        result = register(
            register_url=self.endpoints.consumer_register,
            email=email,
            phone=phone,
            password=password,
            firstName=firstName,
            lastName=lastName,
            referralCode=referralCode,
            purchaseToken=purchaseToken,
            productRegisterID=productRegisterID,
        )
        try:
            self.token = result["data"]["token"]
            self.user_data = result["data"]["auther"]
        except:
            print("Failed to register, got:", result)
    
    def useQuery(self, query: str, variables = {}):
        return useQueryAsOn(query, variables, self.token, self.endpoints.gql)

    def useMutation(self, mutation: str, input = {}):
        return useMutationAsOn(mutation, input, self.token, self.endpoints.gql)

#endregion

