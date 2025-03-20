"""
API client configuration for BPMN Cloud Upload Tool.

This module configures the API client for making requests to the Celonis API,
including headers, base URL, and proxy settings.
"""

import streamlit as st
import requests

def get_api_config():
    """
    Get the current API configuration from session state.
    
    Returns:
        tuple: (base_url, headers, proxies) for making API requests
    """
    base_url = st.session_state.celonis_base_url
    headers = {
        "Authorization": f'Bearer {st.session_state.celonis_app_key}',
        "Content-Type": "application/json"
    }
    proxies = st.session_state.proxies
    
    return base_url, headers, proxies

def test_api_connection(celonis_base_url, celonis_app_key_input):
    """
    Test the API connection using the provided credentials.
    
    Args:
        base_url (str): The base URL for the Celonis API
        headers (dict): The headers to use for the API request
        proxies (dict): The proxy configuration to use
        
    Returns:
        bool: True if connection successful, False otherwise
        str: Error message if connection failed, None otherwise
    """
    # Test the connection before setting credentials_set to true
    try:
        # Make a simple API call to verify credentials
        test_url = f"{celonis_base_url}/categories"
        test_headers = {
            "Authorization": f'Bearer {celonis_app_key_input}',
            "Content-Type": "application/json"
        }
        proxies_to_test = st.session_state.proxies
        
        response = requests.get(test_url, headers=test_headers, proxies=proxies_to_test, timeout=10)
        
        if response.status_code == 200:
            st.session_state.credentials_set = True
            st.success("Credentials verified and saved successfully!")
        else:
            st.error(f"Failed to connect with provided credentials: {response.status_code} - {response.text}")
            st.session_state.credentials_set = False
    except Exception as e:
        st.error(f"Connection test failed: {str(e)}")
        st.session_state.credentials_set = False