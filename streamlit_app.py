import streamlit
import snowflake.connector
import pandas
import yfinance as yt
from urllib.error import URLError
import requests


 
#Create the repeatable code block (called a function)
def get_stock_data(stock):
    yfinance_response = yt.Ticker(stock)
   
    return yfinance_response
 
  
# New Section to display yfinance api response
streamlit.header("Yahoo Finance Data")
try:
  stock_text = streamlit.text_input('What stock would you like information about?')
  if not stock_text:
      streamlit.error("Please select a stock to get information.")
  else:
    back_from_function = get_stock_data(stock_text)
    stremlit.header(back_from_function.info)
    
    
    
except URLError as e:
    streamlit.error()


# GetFacebookInformation = yahooFinance.Ticker("FB")
# streamlit.header(GetFacebookInformation.info)


streamlit.title('Zena\'s Amazing Athleisure Catalog')
# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()
# put the dafta into a dataframe
df = pandas.DataFrame(my_catalog)
# temp write the dataframe to the page so I Can see what I am working with
# streamlit.write(df)
# put the first column into a list
color_list = df[0].values.tolist()
# print(color_list)
# Let's put a pick list here so they can pick the color
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))
# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'
# use the option selected to go back and get all the info from the database
my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
df2 = my_cur.fetchone()
streamlit.image(
  df2[0],
width=400,
caption= product_caption
)
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ',df2[2])
streamlit.write(df2[3])
