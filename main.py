"""
python streamlit basic
"""
import streamlit as st
st.title("wel come to streamlit app")

# page handle
input_handler = st.Page(page="inputHandler.py", title="Input Handler",)
dataframe = st.Page(page="dataframe.py", title="Dataframe", )

pages = st.navigation([input_handler, dataframe])
pages.run()