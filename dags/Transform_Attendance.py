import pandas as pd

def Transform_Attendance(attendance_data):
    df_attendance = attendance_data

    df_attendance['attendances'] = df_attendance['sections'].apply(lambda x: [attendance['attendances'] for attendance in x if attendance['attendances']])

    df_attendance['sections'] = df_attendance['sections'].apply(lambda x: x[0]['sec'] if len(x) == 1 and 'sec' in x[0] else x)
    
    df_attendance = df_attendance.explode('sections').reset_index(drop=True)
    
    
    
    # df_attendance['numEnrolledStd'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['numEnrolledStd'] if isinstance(x, dict) else None)
    # df_attendance['numPresent'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['numPresent'] if isinstance(x, dict) else None)
    # df_attendance['numAbsent'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['numAbsent'] if isinstance(x, dict) else None)
    # df_attendance['numLeave'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['numLeave'] if isinstance(x, dict) else None)
    # df_attendance['classDate'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['classDate'] if isinstance(x, dict) else None)
    # df_attendance['classStart'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['classStart'] if isinstance(x, dict) else None)
    # df_attendance['classEnd'] = df_attendance['sections'].apply(lambda x: x['attendances'][0]['classEnd'] if isinstance(x, dict) else None)

    # df_attendance.drop_duplicates()

    return df_attendance 
    
