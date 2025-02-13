def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=  df[df["user"] == selected_user]

    num_message = df.shape[0]
    words=[]
    for mess in df['message']:
        words.extend(mess.split())

    return num_message,len(words)

    