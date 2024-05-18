def Transform_Booking(booking_data):
    df_booking = booking_data
    df_booking = df_booking.rename(columns={'activity.activityName': 'activity_activityName'})
    df_booking = df_booking[df_booking['activity_activityName'] == 'การเรียนการสอน']
    df_booking[['semester', 'subjectCode', 'section']] = df_booking['remarks'].str.split('|', expand=True)
    columns_to_keep = [
        'subjectCode','section', 'room','activity_activityName', 
        'bookingStartDate', 'bookingEndDate'
    ]
    df_booking = df_booking[columns_to_keep]
    return df_booking
