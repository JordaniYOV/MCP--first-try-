import requests
from datetime import datetime, timedelta
from fastapi import FastAPI

app = FastAPI()

CLIENT_ID = "Yopb4qGMJ61aETKwtNkb"
CLIENT_SECRET = "j6j_jwmw2S5IOJGhqoHvHnfTsudweRcZwazT5WjK"
AUTHORIZATION_CODE = "iUri_NmeS-ud6R1rcTaTUQ&"
REDIRECT_URL = "https://getprodai.ru"

@app.get('/', tags=['token'])
def get_avito_token():
    auth_url = 'https://api.avito.ru/token'
    auth_data = {
        'grant_type': 'client_credentials', 
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
       
    }

    response = requests.post(auth_url, data=auth_data)
    tokens = response.json()

    # access_token = tokens['access_token']
    # expires_in = tokens['expires_in']

    # expire_time = datetime.now() + timedelta(seconds=expires_in)

    # print(f"Access Token получен! Истекает: {expire_time}")
    return tokens

@app.get('/auth_code', tags=['token'])
def get_tokens():
    auth_url = 'https://api.avito.ru/token'
    auth_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTHORIZATION_CODE,
        'redirect_uri': REDIRECT_URL
    }

    response = requests.post(auth_url, data=auth_data)
    tokens = response.json()
    
    # access_token = tokens['access_token']
    # expires_in = tokens['expires_in'] 
    # refresh_token = tokens['refresh_token']
    
    # expire_time = datetime.now() + timedelta(seconds=expires_in)
    
    # print(f"Access Token получен! Истекает: {expire_time}")
    # return access_token, expire_time, refresh_token
    return tokens



