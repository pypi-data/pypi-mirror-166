import requests
import logging
import json


class Gc2:
    def __init__(
            self,
            url="https://swarm.gc2.io/",
            api_version="v3",
            user=None,
            pw=None,
            db=None,
    ):
        self.api_version = api_version
        self.base_url = url
        self.headers = {"content-type": "application/json; charset=utf-8"}
        self.user = None
        self.db = None
        self.__password = None
        self.__auth = None
        self.token = None
        self.auth_response = None
        if user and pw and db:
            self.set_authentication(user, pw, db)
        self.__set_url()

    def __set_url(self):
        self.url = f"{self.base_url}/api/{self.api_version}"

    def __check_auth(self):
        url = f"{self.url}/oauth/token"
        creds = {
            "grant_type": "password",
            "username": self.user,
            "password": self.__password,
            "database": self.db,
            "client_id": "xxxxxxxxxx",
            "client_secret": "xxxxxxxxxx",
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(creds))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        else:
            logging.info(f"{self.user} is logged in.")
            self.auth_response = json.loads(resp.text)
            self.token = self.auth_response["access_token"]
            self.headers.update({"Authorization": "Bearer " + self.token})

    def set_authentication(self, user, pw, db):
        self.user = user
        self.db = db
        self.__password = pw
        self.__auth = (user, pw, db)
        try:
            self.__check_auth()
        except Exception as e:
            self.user = None
            self.db = None
            self.__password = None
            self.__auth = None
            self.token = None
            self.auth_response = None
            raise e
