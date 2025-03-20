"""
Session state management for BPMN Cloud Upload Tool.

This module handles session state initialization and management
for maintaining application state across re-runs.
"""

import streamlit as st
from config import DEFAULT_CELONIS_BASE_URL

def initialize_session_state():
    """
    Initialize all required session state variables if they don't exist.
    
    This ensures consistent state management across application reruns.
    """
    # Authentication and connection
    if 'credentials_set' not in st.session_state:
        st.session_state.credentials_set = False
    if 'celonis_app_key' not in st.session_state:
        st.session_state.celonis_app_key = None
    if 'celonis_base_url' not in st.session_state:
        st.session_state.celonis_base_url = DEFAULT_CELONIS_BASE_URL
    if 'proxies' not in st.session_state:
        st.session_state.proxies = None
    if 'proxy_username' not in st.session_state:
        st.session_state.proxy_username = False
    if 'proxy_password' not in st.session_state:
        st.session_state.proxy_password = False
        
    # BPMN file state
    if 'bpmn_loaded' not in st.session_state:
        st.session_state.bpmn_loaded = False
    if 'bpmn_content' not in st.session_state:
        st.session_state.bpmn_content = None
    if "bpmn_tasks" not in st.session_state:
        st.session_state.bpmn_tasks = []
        
    # Selection state
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_process_model' not in st.session_state:
        st.session_state.selected_process_model = None
    if 'selected_tags' not in st.session_state:
        st.session_state.selected_tags = []
    if "upload_success" not in st.session_state:
        st.session_state.upload_success = False

    # Celonis state
    if 'pool_selected' not in st.session_state:
        st.session_state.pool_selected = False
    if 'model_options' not in st.session_state:
        st.session_state.model_options = False
    if 'selected_pool' not in st.session_state:
        st.session_state.selected_pool = False
    if 'celonis_connected' not in st.session_state:
        st.session_state.celonis_connected = False
    if "model_selected" not in st.session_state:
        st.session_state.model_selected = False
    if 'model_names' not in st.session_state:
        st.session_state.model_names = False
    if 'table_selected' not in st.session_state:
        st.session_state.table_selected = False
    if 'column_options' not in st.session_state:
        st.session_state.column_options = False
    if 'activities_fetched' not in st.session_state:
        st.session_state.activities_fetched = False
    # Store checkbox state in session_state
    if "confirm_add" not in st.session_state:
        st.session_state.confirm_add = False
    if "missing_activities" not in st.session_state:
        st.session_state.missing_activities = []

def reset_session_state():
    """
    Reset all session state variables and force a page rerun.
    
    This provides a clean slate for users to start over.
    """
    # Delete all keys in session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Reinitialize session state
    initialize_session_state()
    
    # Force a page rerun
    st.experimental_rerun()

def reset_credentials():
    """
    Reset only the credential-related session state variables.
    
    This allows users to re-enter credentials without losing other state.
    """
    st.warning("Please configure and verify your credentials to proceed.")
    # Add a button to reset credentials if they were previously set but failed
    if st.session_state.celonis_app_key:
        st.session_state.credentials_set = False
        st.session_state.celonis_app_key = None
        st.session_state.proxies = None
        # st.session_state.credential_error = False
        
        # Force a page rerun
        st.experimental_rerun()