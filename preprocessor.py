
import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)


    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Extract date without the trailing "- "
    df['message_date'] = df['message_date'].str.extract(r'([\d/]+, \d+:\d+)')[0]

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M', errors='coerce')
    if df['message_date'].isna().sum() > 0:  
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M', errors='coerce')

    # Rename the column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users, messages = [], []
    for message in df['user_message']:
        entry = re.split(r'(^[\w\s]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional time-based features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create 'period' column for hourly grouping
    if not df.empty:
        df['period'] = df['hour'].astype(str) + '-' + (df['hour'] + 1).mod(24).astype(str)
    else:
        df['period'] = []

    return df

