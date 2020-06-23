import streamlit as st
import scraper as sc

# variables

st.sidebar.title("Menu options")
language = st.sidebar.selectbox("select a language",['python','javascript'])
date_range = st.sidebar.selectbox("date range",['daily','weekly','monthly'])

url =  sc.get_dynamic_url(language,date_range)
st.title("Data mining - live")
st.text('data will be scraped from')
st.text_input('the url to be scraped',value=url)
view_raw_data = st.checkbox('view raw data')
if st.button('start mining'):
    with st.spinner('collecting data from url'):
        soup = sc.get_data_as_soup(url)
        st.success("webpage loaded")
else:
    soup = None 
if soup :
    if view_raw_data:
        raw_data = sc.view_raw_data(soup)
        st.markdown(raw_data)
