from urlextract import URLExtract
import matplotlib.pyplot as plt
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=  df[df["user"] == selected_user]

    num_message = df.shape[0]
    words=[]
    for mess in df['message']:
        words.extend(mess.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links=[]
    for mess in df['message']:
        links.extend(extract.find_urls(mess))

    return num_message,len(words),num_media_messages, len(links)

    

def most_busy_users(df):
    x = df['user'].value_counts().head()
    # plt.bar(name, count)
    # plt.xticks(rotation='vertical')
    # plt.show()
    return x