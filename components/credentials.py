import streamlit as st
import requests
from xml.etree import ElementTree as ET
import os
import tempfile

from utils.session import reset_credentials
from api.client import test_api_connection

def show_credentials_section():
    
    with st.expander("Configure credentials", expanded=not st.session_state.credentials_set):
        col1, col2 = st.columns(2)
        with col1:
            celonis_app_key_input = st.text_input("Celonis App Key", type="password")
        with col2:
            celonis_base_url = st.text_input("Celonis Base URL", value="https://bosch.eu-4.celonis.cloud/process-repository/api/v1")
        
        st.subheader("Proxy Settings")
        use_proxy = st.checkbox("Use Proxy", value=True)
        
        if use_proxy:
            col1, col2 = st.columns(2)
            with col1:
                proxy_username_input = st.text_input("Proxy Username")
                proxy_host = st.text_input("Proxy Host", value="rb-proxy-unix-de01.bosch.com")
            with col2:
                proxy_password_input = st.text_input("Proxy Password", type="password")
                proxy_port = st.text_input("Proxy Port", value="8080")
        
        if st.button("Save Credentials"):
            if not celonis_app_key_input:
                st.error("Celonis App Key is required")
            else:
                st.session_state.celonis_app_key = celonis_app_key_input
                st.session_state.celonis_base_url = celonis_base_url
                st.session_state.proxy_username = proxy_username_input
                st.session_state.proxy_password = proxy_password_input
                
                if use_proxy:
                    proxy_url = f"http://{proxy_username_input}:{proxy_password_input}@{proxy_host}:{proxy_port}"
                    st.session_state.proxies = {
                        "http": proxy_url,
                        "https": proxy_url,
                    }
                else:
                    st.session_state.proxies = None
                
                test_api_connection(celonis_base_url, celonis_app_key_input)