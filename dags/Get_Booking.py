import pandas as pd
import requests
from datetime import datetime

def Get_Booking(api_token):

    if api_token:
        url = 'https://de.ict.mahidol.ac.th/data-service/v1/Booking/FetchData'
        headers = {
            'accept': 'text/plain; v=1.0',
            'Authorization': 'Bearer ' + api_token
        }

        current_time = datetime.now()
        end_date = current_time.strftime('%Y-%m-%d')

        params = {
            'startDate': '2023-03-20',
            'endDate': end_date,
            'room': 'IT 105',
            'floor': '1'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            json_data = response.json()
            df = pd.json_normalize(json_data["data"])
            return df
    else:
        return None
