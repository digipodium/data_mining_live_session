import streamlit as st
import scraper as sc
import os
import pandas as pd
# variables

st.sidebar.title("Menu options")
lang = st.sidebar.selectbox("select a language",['python','javascript','c++','java','html','css','c'])
date = st.sidebar.selectbox("date range",['daily','weekly','monthly'])

# step 1
url =  sc.get_dynamic_url(language=lang,date_range=date)
st.title("Data mining - live")
st.text('data will be scraped from')
st.text_input('the url to be scraped',value=url)
st.write('select options ')
view_raw_data = st.checkbox('view raw data (not the best idea)')
view_dictionary_data = st.checkbox('view data dictionary')
save_data = st.checkbox('save data to file')
if st.button('start mining'):
    with st.spinner('collecting data from url'):
        soup = sc.get_data_as_soup(url)
        st.success("webpage loaded")
else:
    soup = None 
# step 2
if soup :
    if view_raw_data:
        with st.spinner('loading raw data'):
            raw_data = sc.view_raw_data(soup)
            st.markdown(raw_data)
    rows = sc.get_rows(soup)
    datadict = sc.extract_data(rows,date)
    if view_dictionary_data:
        with st.spinner('loading data dictionary'):
            st.write(datadict)
    if save_data:
        with st.spinner('saving data as dataset'):
            df = sc.save_data(datadict,lang,date)
            st.success('data saved')
            st.write(df)

files = os.listdir('datasets')
if files:
    selected_files = st.selectbox('created datasets',files)
btnview = st.button('view data')
if btnview:
    content = pd.read_csv('datasets/'+selected_files)
    st.subheader("viewing saved dataset")
    st.write(content)

btngraph = st.button('view graph')
if btngraph:
    fig = sc.generate_graph('datasets/'+selected_files)
    st.plotly_chart(fig)