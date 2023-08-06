import requests
import json
import os

def get_players(id=None):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/players/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    if id != None: 
        url += id
    response = requests.get(url=url, headers=headers)
    return response.json()

def update_players(id, payload):
    bearerToken = os.getenv('BEARER_TOKEN') 
    url = f'https://mlssoccerapi.com/players/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.put(url=url, headers=headers, data=payload)
    return response.json()

def delete_players(id): 
    bearerToken = os.getenv('BEARER_TOKEN')
    url = f'https://mlssoccerapi.com/players/{id}'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    payload = json.dumps({
        'id': id
    })
    response = requests.delete(url=url, headers=headers, data=payload)
    return response.json()

def add_players(payload):
    bearerToken = os.getenv('BEARER_TOKEN')
    url = 'https://mlssoccerapi.com/players/'
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {bearerToken}'
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()