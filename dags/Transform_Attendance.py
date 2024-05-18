import pandas as pd

def Transform_Attendance(attendance_data):
    df_attendance = attendance_data

    # Define a function to extract the attendance data
    def extract_attendance_data(row):
        section_data = row['sections']
        all_attendances = []

        for section in section_data:
            attendances = section['attendances']
            for attendance in attendances:
                attendance_record = attendance.copy()
                attendance_record['section'] = section['sec']
                attendance_record['subjectCode'] = row['subjectCode']
                attendance_record['subjectName'] = row['subjectName']
                all_attendances.append(attendance_record)
        
        return all_attendances

    # Apply the function and create a DataFrame with all the attendance records
    attendance_records = df_attendance.apply(extract_attendance_data, axis=1).explode().tolist()
    df_all_attendance = pd.DataFrame(attendance_records)
    df_all_attendance.drop(columns=['percentPresent','percentAbsent','percentLeave'], inplace=True)
    return df_all_attendance
