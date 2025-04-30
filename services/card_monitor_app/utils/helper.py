import requests
import os

def test(): 
    base_uri = os.getenv('CARDTRADER_BASE_URL')
    return base_uri