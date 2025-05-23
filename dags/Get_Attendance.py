import pandas as pd
import requests

def Get_Attendance(api_token,df_booking_data):
    df_all_attendance = pd.DataFrame()
    if api_token:
        url = 'https://de.ict.mahidol.ac.th/data-service/v1/ClassInfo/AttendaceSummary'
        headers = {
            'accept': 'text/plain; v=1.0',
            'Authorization': 'Bearer ' + api_token
        }
        df_booking_data = df_booking_data["remarks"]
        df_booking_data = df_booking_data.drop_duplicates()
        df_booking_data = df_booking_data[df_booking_data != ""]
        for index, row in df_booking_data.items():
            row_values = row.split('|')
            if len(row_values) == 3:
                semester, subjectCode, section = row_values
            params = {
                'semester': semester,
                'subjectCode': subjectCode,
                'section': section,
                }

            response = requests.get(url, headers=headers, params=params)
    
            if response.status_code == 200:
                json_data = response.json()
                df_attendance = pd.DataFrame()
                df_attendance = pd.json_normalize(json_data["data"])
                df_all_attendance = pd.concat([df_all_attendance, df_attendance])
        return df_all_attendance
    else:
        return None
    

    