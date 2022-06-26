import streamlit as st

with open("README.md") as readme:
    st.write(readme.read())

st.button("Reload")
