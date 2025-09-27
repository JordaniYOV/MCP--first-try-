from os import access
from urllib import response
from pydantic import HttpUrl
from urllib.parse import parse_qs
import requests
import json
from datetime import datetime, timedelta


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://getprodai.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


class TokenManager():
    def __init__(self, token_file='tokens.json'):
        self.token_file = token_file
        self.tokens = self.load_tokens()
        
    def load_tokens(self):
        with open(self.token_file, 'r') as f: 
            return json.load(f)

    def save_tokens(self, access_token, expires_in):
        self.tokens = {
            'access_token': access_token, 
         
            'expires_in': expires_in,
            'created_at': datetime.now().isoformat()
        }
        
        with open(self.token_file, 'w') as f: 
            json.dump(self.tokens, f)

    def is_token_expired(self): 
        created_at = datetime.fromisoformat(self.tokens['created_at'])
        expires_in = self.tokens.get('expires_in')
        extra_time = 300

        expiration_time = created_at + timedelta(seconds=expires_in)

        if datetime.now() < (expiration_time - timedelta(seconds=extra_time)):
            print(expiration_time)
            return False 
        else: 
            return True

token_manager = TokenManager()

CLIENT_ID = "Yopb4qGMJ61aETKwtNkb"
CLIENT_SECRET = "j6j_jwmw2S5IOJGhqoHvHnfTsudweRcZwazT5WjK"
REDIRECT_URL = "https://getprodai.ru"

# @app.get('/', tags=['token'])
# def get_avito_token():
    # if token_manager.is_token_expired(): 
    #     auth_url = 'https://api.avito.ru/token'
    #     auth_data = {
    #         'grant_type': 'client_credentials', 
    #         'client_id': CLIENT_ID,
    #         'client_secret': CLIENT_SECRET,
    #     }

    #     response = requests.post(auth_url, data=auth_data)
    #     tokens = response.json()

    #     access_token = tokens['access_token']
    #     expires_in = tokens['expires_in']

    #     token_manager.save_tokens(access_token, expires_in)

    #     expire_time = datetime.now() + timedelta(seconds=expires_in)
    #     print(f"Access Token получен! Истекает: {expire_time}")
    #     return tokens
    # else: 
    #     print("Токен действителен")

@app.get('/get_access_token', tags=['token'])
def get_tokens(url: HttpUrl):
    query = parse_qs(url.query)
    AUTHORIZATION_CODE = query.get('code')

    auth_url = 'https://api.avito.ru/token'
    auth_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTHORIZATION_CODE,
    }

    response = requests.post(auth_url, data=auth_data)
    tokens = response.json()
    
    access_token = tokens['access_token']
    expires_in = tokens['expires_in'] 
    refresh_token = tokens['refresh_token']
    
    expire_time = datetime.now() + timedelta(seconds=expires_in)
    
    token_manager.save_tokens(access_token, refresh_token, expires_in)

    print(f"Access Token получен! Истекает: {expire_time}")
    return access_token, expire_time, refresh_token

@app.get('/get_messages', tags=['get_massages'])
def get_messages():
    if token_manager.is_token_expired():
        auth_link = 'https://api.avito.ru/token'
        auth_data = {
            'grant_type': 'refresh_token', 
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET,
            'refresh_token': token_manager.tokens['refresh_token']
        }
        
        response = requests.post(auth_link, data=auth_data)
        tokens = response.json()

        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        expires_in = tokens['expires_in']

        token_manager.save_tokens(access_token, refresh_token, expires_in)
    
 

