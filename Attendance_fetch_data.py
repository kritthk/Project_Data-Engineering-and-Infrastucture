import pandas as pd
import numpy as np
import requests
import re
from datetime import datetime
from get_token import get_api_token
from Booking_fetch_data import Booking_fetch_data

def Attendance_fetch_data():
    df_all_attendance = pd.DataFrame()
    api_token = get_api_token()

    if api_token:
        df_booking_data = Booking_fetch_data()
        df_booking_data_remarks = df_booking_data["remarks"]
        df_subjectCode = df_booking_data_remarks.str.split('|').str[1]
        df_subjectCode = df_subjectCode.rename("subjectCode")
        df_subjectCode = df_subjectCode.dropna().drop_duplicates()
        

        df_semester = df_booking_data_remarks.str.split('|').str[0]
        df_semester = df_semester.str.extractall('(\d{3})').values
        df_semester = set(np.concatenate(df_semester))
        df_semester = pd.DataFrame(df_semester, columns=['semester'])
        df_semester = df_semester['semester']

        df_section = df_booking_data_remarks.str.split('|').str[2]
        df_section = df_section.rename("section")
        df_section = df_section.dropna().drop_duplicates()
        

        url = 'https://de.ict.mahidol.ac.th/data-service/v1/ClassInfo/AttendaceSummary'
        headers = {
            'accept': 'text/plain; v=1.0',
            'Authorization': 'Bearer ' + api_token
        }
        for semester in df_semester:
            for subjectCode in df_subjectCode:
                for section in df_section:
                    params = {
                        'semester': semester,
                        'subjectCode': subjectCode,
                        'section': section,
                    }

                    response = requests.get(url, headers=headers, params=params)

                    if response.status_code == 200:
                        json_data = response.json()
                        df_attendance = pd.json_normalize(json_data["data"])
                        df_all_attendance = pd.concat([df_all_attendance, df_attendance])
        return df_all_attendance
    else:
        return None