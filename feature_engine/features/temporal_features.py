import pandas as pd

def mean_conv_msg_duration(df,on_column):


    #convert timestamp column to datetime type (in minutes)
    df[on_column] = pd.to_datetime(df[on_column])

    # calculate difference between consecutive timestamps
    df['time_diff'] = df[on_column].diff().dt.total_seconds()/60
    return  df['time_diff'].mean() 

def stddev_conv_msg_duration(df,on_column):


    #convert timestamp column to datetime type (in minutes)
    df[on_column] = pd.to_datetime(df[on_column])

    # calculate difference between consecutive timestamps
    df['time_diff'] = df[on_column].diff().dt.total_seconds()/60

    return  df['time_diff'].std()

df = pd.DataFrame({'timestamp': ['2023-02-20 09:00:00', '2023-02-20 09:05:00', '2023-02-20 09:10:00']})
mean_conv_msg_duration(df,'timestamp')
stddev_conv_msg_duration(df,'timestamp')