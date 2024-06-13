import requests

from .firewall import Firewall
from .util import Constants, reliable_b64_decode


class Opnsense(object):

    def __init__(self, api_key=None, api_secret=None, api_url=None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._api_url = api_url

        # Raise an exception and quit if we're missing the key, secret, or host.
        if self._api_key is None: raise Exception("API key not found!")
        if self._api_secret is None: raise Exception("API secret not found!")
        if self._api_url is None: raise Exception("API host not found!")


    def _authenticated_request(self, method, path, body=None):
        if method == 'POST':
            post_response = requests.post(f'{self._api_url}/api/{path}',
                                          json=body,
                                          auth=(self._api_key,self._api_secret),
                                          verify=False)
            return post_response.json()
        elif method == 'GET':
            get_response = requests.get(f'{self._api_url}/api/{path}',
                                          data=None,
                                          auth=(self._api_key,self._api_secret),
                                          verify=False)
            return get_response.json()

    @property
    def firewall(self) -> Firewall:
        return Firewall(self)
