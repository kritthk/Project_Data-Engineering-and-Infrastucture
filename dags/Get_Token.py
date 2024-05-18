import requests

def Get_Api_Token():
    url_api = 'https://de.ict.mahidol.ac.th/data-service/v1/Authen/apikey'
    params = {
        'apiKey': '7YTzkxTT8n7i2FEMX7eS67Ba+BnN2PtUZTSazeiUFX4='
    }
    headers = {
        'accept': 'text/plain; v=1.0'
    }

    response = requests.post(url_api, params=params, headers=headers, data={})

    if response.status_code == 200:
        api_json = response.json()
        return api_json["data"]["token"]
