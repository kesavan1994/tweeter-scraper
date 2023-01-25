
import pandas as pd
import streamlit as st
import datetime
import snscrape.modules.twitter as sntwitter
from PIL import Image
import certifi
ca = certifi.where()

PAGE_CONFIG={"page_title":"StColab.io","page_icon":"smiley",
       "Layout":"centered",'background-color':'green'
}

# mongodb Connection
import pymongo
client = pymongo.MongoClient("mongodb+srv://abcd:abcd@cluster0.naa5p8i.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)

db = client.test
records=db.twitter




st.set_page_config(
    page_title="Twitter Scraper",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

#st.image('/content/pexels-pixabay-531880.jpg')

img=Image.open("Twitter-Logo-2010.png")
st.image(img,width=400)

# Create a form
with st.form('Twitter_form'):

    search_term=st.text_input("What you want to search","Type here") #Search Text input

    today = datetime.date.today() 

    level=st.slider('tweet count',0,1000) #Slider


    start_date = st.date_input('Start date', datetime.date(2020,1,1)) #Start Date 
    end_date = st.date_input('End date',today)                        #End Date 

    if start_date <= end_date:
        if  end_date <= datetime.date.today():
          st.success('sucess')
          
        else:
          st.error("Error: End date must fall befor today's date.")
    else:
        st.error('Error: End date must fall after start date.')

    submitted = st.form_submit_button('Submit')
    


        
twitter=[]

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_term} since:{start_date} until:{end_date}').get_items()):
  if i>level-1:
    break
  twitter.append([tweet.date,tweet.id,tweet.url,tweet.rawContent,tweet.user.username,
                  tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])
df=pd.DataFrame(twitter,columns=['date', 'id', 'url', 'tweet content', 'username','reply count', 'retweet count','language', 'source', 'like count'])  
#df['date'] = pd.to_datetime(df['date']).dt.date


 
 
st.dataframe(df)  #to Create DataFrame

       
csv=df.to_csv().encode('utf-8') #DataFrame to CSV
col1, col2, col3, col4, col5, col6, = st.columns([1,1,1,1,1,1])

with col6:
   
  st.download_button(    
      label="Download CSV",
      data=csv,
      file_name='large_df.csv',
      mime='text/csv',

  )  #csv Download btn

 
with col5:
  json=df.to_json().encode('utf-8')

  st.download_button(
        label="Download JSON",
        data=json,
        file_name='large_df.json',
        mime='text/json',
    ) #json Download btn
st.markdown(""" <style> 

</style> """, unsafe_allow_html=True)

# Upload Btn
with col1:
  if st.button('Upload'):
      data=df.to_dict('records')
      search_term=str(search_term)
      data1={search_term:data}
      records.insert_one(data1)
