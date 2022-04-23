from json import loads

from django.test import Client, TestCase


class APIClient(Client):
    def __init__(self, **defaults):
        self.token = None
        self.version = "v1"
        self.path = "/api"
        super().__init__(**defaults)

    def generic(self, method, path, *args, **kwargs):
        path = f"{self.path}/{self.version}/{path}"

        if self.token:
            kwargs["HTTP_AUTHORIZATION"] = self.token
        response = super().generic(method, path, *args, **kwargs)
        try:
            response.json = loads(response.content)
        except ValueError:
            response.json = None
        return response

    def login(self, username, password):
        data = {"username": username, "password": password}
        response = self.post("auth/", data=data)
        if response.status_code == 200 and "token" in response.json:
            self.token = f"Token {response.json['token']}"
            return response
        else:
            self.token = None
            return response


class BaseTestCase(TestCase):
    maxDiff = None
    fixtures = None

    def setUp(self):
        self.api_client = APIClient()
        super().setUp()
