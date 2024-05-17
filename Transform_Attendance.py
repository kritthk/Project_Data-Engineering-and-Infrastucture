import pandas as pd
from Fetch_Attendance import Attendance_fetch_data

def Transform_Attendance():
    df_attendance = Attendance_fetch_data()

    df_attendance['attendances'] = df_attendance['sections'].apply(lambda x: [attendance['attendances'] for attendance in x if attendance['attendances']])

    df_attendance['sections'] = df_attendance['sections'].apply(lambda x: x[0]['sec'] if len(x) == 1 and 'sec' in x[0] else x)

    df_attendance = df_attendance.explode('attendances').explode('attendances').reset_index(drop=True)

    df_attendance['numEnrolledStd'] = df_attendance['attendances'].apply(lambda x: x['numEnrolledStd'] if isinstance(x, dict) else None)
    df_attendance['numPresent'] = df_attendance['attendances'].apply(lambda x: x['numPresent'] if isinstance(x, dict) else None)
    df_attendance['percentPresent'] = df_attendance['attendances'].apply(lambda x: x['percentPresent'] if isinstance(x, dict) else None)
    df_attendance['numAbsent'] = df_attendance['attendances'].apply(lambda x: x['numAbsent'] if isinstance(x, dict) else None)
    df_attendance['percentAbsent'] = df_attendance['attendances'].apply(lambda x: x['percentAbsent'] if isinstance(x, dict) else None)
    df_attendance['numLeave'] = df_attendance['attendances'].apply(lambda x: x['numLeave'] if isinstance(x, dict) else None)
    df_attendance['percentLeave'] = df_attendance['attendances'].apply(lambda x: x['percentLeave'] if isinstance(x, dict) else None)
    df_attendance['classDate'] = df_attendance['attendances'].apply(lambda x: x['classDate'] if isinstance(x, dict) else None)
    df_attendance['classStart'] = df_attendance['attendances'].apply(lambda x: x['classStart'] if isinstance(x, dict) else None)
    df_attendance['classEnd'] = df_attendance['attendances'].apply(lambda x: x['classEnd'] if isinstance(x, dict) else None)

    df_attendance.drop(columns=['attendances'], inplace=True)
    df_attendance.drop_duplicates()

    return df_attendance

if __name__ == "__main__":
    df = Transform_Attendance()
    df.to_csv("Attendance.csv")
    
