"""
Process model-related API calls for BPMN Cloud Upload Tool.

This module contains functions for retrieving, creating, and updating process models
in the Celonis API.
"""

import streamlit as st
import requests
from api.client import get_api_config
from config import API_CACHE_TTL

@st.cache_data(ttl=API_CACHE_TTL)
def get_process_models(category_id):
    """
    Fetch process models for a specific category from the Celonis API.
    
    Args:
        category_id (str): ID of the category to fetch process models for
        
    Returns:
        list: List of process model objects, or empty list if request fails
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/categories/{category_id}/process-models"
        response = requests.get(url, headers=headers, proxies=proxies)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get process models: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting process models: {str(e)}")
        return []

def create_process_model(category_id, model_name):
    """
    Create a new process model in a category.
    
    Args:
        category_id (str): ID of the category to create the process model in
        model_name (str): Name of the new process model
        
    Returns:
        dict: The created process model object, or None if creation failed
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/categories/{category_id}/process-models"
        payload = {"name": model_name}
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        
        if response.status_code == 200:
            st.success(f"Process model '{model_name}' created successfully!")
            # Clear cache to refresh the process models list
            get_process_models.clear()
            return response.json()
        else:
            st.error(f"Failed to create process model: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating process model: {str(e)}")
        return None

def upload_bpmn_file(category_id, process_model_id, bpmn_content, tag_ids=None):
    """
    Upload a BPMN file to a process model and optionally add tags.
    
    Args:
        category_id (str): ID of the category containing the process model
        process_model_id (str): ID of the process model to upload to
        bpmn_content (str): The BPMN XML content as a string
        tag_ids (list, optional): List of tag IDs to add to the process model
        
    Returns:
        bool: True if upload successful, False otherwise
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        # First upload the BPMN file
        url = f"{base_url}/categories/{category_id}/process-models/{process_model_id}/file"
        upload_headers = headers.copy()
        upload_headers["Content-Type"] = "application/octet-stream"
        
        response = requests.post(
            url, 
            headers=upload_headers, 
            data=bpmn_content, 
            proxies=proxies
        )
        
        if response.status_code != 200:
            st.error(f"Failed to upload BPMN file: {response.status_code} - {response.text}")
            return False
        
        # If tags are provided, add them to the process model
        if tag_ids and len(tag_ids) > 0:
            url = f"{base_url}/categories/{category_id}/process-models/{process_model_id}"
            
            # First get the current process model details
            response = requests.get(url, headers=headers, proxies=proxies)
            if response.status_code != 200:
                st.error(f"Failed to get process model details: {response.status_code} - {response.text}")
                return False
            
            process_model = response.json()
            
            # Update with tags
            payload = {
                "name": process_model["name"],
                "tagIds": tag_ids
            }
            
            response = requests.put(url, headers=headers, json=payload, proxies=proxies)
            if response.status_code != 200:
                st.error(f"Failed to add tags to process model: {response.status_code} - {response.text}")
                return False
        
        return True
    except Exception as e:
        st.error(f"Error uploading BPMN file: {str(e)}")
        return False