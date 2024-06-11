import requests
import json
from dataclasses import dataclass

@dataclass
class OPNsenceAPI:
    api_url: str
    api_key: str
    api_secret: str

    def add_rule(self, **kwargs):
        pass
    
    def delete_rule(self, **kwargs):
        pass