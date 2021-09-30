import requests
import json


class SfAuth:

    def get_session_id_un_pw(self, username, password, security_token, base_path='https://login.salesforce.com'):
        pass

    def get_session_id_conn_app(self, client_id, client_secret, username, password, base_path='https://login.salesforce.com'):
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
            'redirect_uri': 'https://localhost:8443/RestTest/oauth/_callback',
            'grant_type': 'password'
        }
        endpoint = base_path + self.get_auth_path()
        resp = requests.post(endpoint, params=payload)
        return resp.json()

    def get_session_id_sfdx(self):
        pass

    def get_auth_path(self):
        return '/services/oauth2/token'
