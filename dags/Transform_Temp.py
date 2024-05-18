def Transform_Temp(df_temp):
    df_temp = df_temp.rename(columns={'Temp': 'Celsius'})
    df_temp.drop(columns=['Humidity','Heat'], inplace=True)
    return df_temp