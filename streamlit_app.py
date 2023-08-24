import snowflake.connector
import streamlit
import pandas
import requests
from urllib.error import URLError

streamlit.title('My parents new healthy dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Bluberry oatmeal')
streamlit.text(' 🥗  Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page
streamlit.dataframe(fruits_to_show)

# create a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_repsonse = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)
  # take the json version and normalize it
  fruityvice_repsonse_normalized = pandas.json_normalize(fruityvice_repsonse.json())
  return fruityvice_repsonse_normalized
 

# New section to display Fruityvice Fruit API response
streamlit.header("Fruityvice Fruit Advice")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select some fruit to get info")
  else:
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

#don't run anything past here till we troubleshoot
#streamlit.stop()

#Let's connect to snowflake and get a list of fruits from the table in snowflake 

streamlit.header("View our Fruit list - Add your Favorite")
# Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)


# allow the user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding"+ new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to your list?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

