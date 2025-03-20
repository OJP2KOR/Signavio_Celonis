"""
Tag-related API calls for BPMN Cloud Upload Tool.

This module contains functions for retrieving tag groups from the Celonis API
and creating new tag groups and tags.
"""

import streamlit as st
import requests
from api.client import get_api_config
from config import API_CACHE_TTL

@st.cache_data(ttl=API_CACHE_TTL)
def get_tag_groups():
    """
    Fetch all tag groups from the Celonis API.
    
    Returns:
        list: List of tag group objects, or empty list if request fails
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/tag-groups"
        response = requests.get(url, headers=headers, proxies=proxies)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get tag groups: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting tag groups: {str(e)}")
        return []

def create_tag_group(tag_group_name):
    """
    Create a new tag group in Celonis.
    
    Args:
        tag_group_name (str): Name of the new tag group
        
    Returns:
        dict: The created tag group object, or None if creation failed
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/tag-groups"
        payload = {"name": tag_group_name}
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        
        if response.status_code == 200:
            st.success(f"Tag group '{tag_group_name}' created successfully!")
            # Clear cache to refresh the tag groups list
            get_tag_groups.clear()
            return response.json()
        else:
            st.error(f"Failed to create tag group: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating tag group: {str(e)}")
        return None

def create_tag(tag_group_id, tag_name):
    """
    Create a new tag in an existing tag group.
    
    Args:
        tag_group_id (str): ID of the tag group to add the tag to
        tag_name (str): Name of the new tag
        
    Returns:
        dict: The updated tag group object, or None if creation failed
    """
    base_url, headers, proxies = get_api_config()
    
    try:
        url = f"{base_url}/tag-groups/{tag_group_id}"
        
        # First get the current tags
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code != 200:
            st.error(f"Failed to get tag group: {response.status_code} - {response.text}")
            return None
        
        tag_group = response.json()
        
        # Append the new tag
        tags = tag_group.get("tags", [])
        tags.append({"name": tag_name})
        
        # Update the tag group with the new tag
        payload = {
            "name": tag_group["name"],
            "tags": tags
        }
        
        response = requests.put(url, headers=headers, json=payload, proxies=proxies)
        if response.status_code == 200:
            st.success(f"Tag '{tag_name}' created successfully!")
            # Clear cache to refresh the tag groups list
            get_tag_groups.clear()
            return response.json()
        else:
            st.error(f"Failed to create tag: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating tag: {str(e)}")
        return None