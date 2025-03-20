"""
Category-related API calls for BPMN Cloud Upload Tool.

This module contains functions for retrieving categories from the Celonis API
and creating new categories.
"""

import streamlit as st
import requests
from api.client import get_api_config
from config import API_CACHE_TTL

@st.cache_data(ttl=API_CACHE_TTL)
def get_categories():
    """
    Fetch all categories from the Celonis API.
    
    Returns:
        list: List of category objects, or empty list if request fails
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/categories"
        response = requests.get(url, headers=headers, proxies=proxies)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get categories: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting categories: {str(e)}")
        return []

def create_category(category_name, parent_id=None):
    """
    Create a new category in Celonis.
    
    Args:
        category_name (str): Name of the new category
        parent_id (str, optional): ID of the parent category if creating a subcategory
        
    Returns:
        dict: The created category object, or None if creation failed
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/categories"
        payload = {"name": category_name}
        
        if parent_id:
            payload["parentId"] = parent_id
            
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        
        if response.status_code == 200:
            new_category = response.json()  # Store new category details
            st.success(f"Category '{category_name}' created successfully!")

            # Refresh categories list
            categories = get_categories()

            # Set newly created category as the selected category
            st.session_state.selected_category = new_category

            # Force rerun to refresh UI
            st.rerun()
            
            return new_category
        else:
            st.error(f"Failed to create category: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating category: {str(e)}")
        return None