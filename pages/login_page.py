import streamlit as st
import streamlit_authenticator as stauth
from utils.auth import get_authenticator

st.set_page_config(page_title="Login / Signup", page_icon="🔒", layout="wide")

# Load authenticator
authenticator = get_authenticator()

# Login form
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    st.button("Go to Export Page", on_click=lambda: st.experimental_set_query_params(page="export_page"))
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")