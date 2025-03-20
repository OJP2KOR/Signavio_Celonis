import streamlit as st
import requests
from xml.etree import ElementTree as ET
import os
import tempfile

from api.tags import get_tag_groups, create_tag, create_tag_group

def available_tags(tag_groups):
    all_tags = []
    # Display tags from all tag groups
    for tag_group in tag_groups:
        if "tags" in tag_group and tag_group["tags"]:
            with st.expander(f"Tag Group: {tag_group['name']}"):
                for tag in tag_group["tags"]:
                    tag_key = f"{tag_group['id']}_{tag.get('id', '')}"
                    tag_selected = st.checkbox(
                        tag.get("name", "Unnamed Tag"), 
                        key=f"tag_{tag_key}",
                        value=tag_key in st.session_state.selected_tags
                    )
                    
                    if tag_selected and tag_key not in st.session_state.selected_tags:
                        st.session_state.selected_tags.append(tag_key)
                    elif not tag_selected and tag_key in st.session_state.selected_tags:
                        st.session_state.selected_tags.remove(tag_key)
                    
                    all_tags.append({
                        "group_id": tag_group['id'],
                        "tag_id": tag.get('id', ''),
                        "key": tag_key,
                        "name": tag.get("name", "Unnamed Tag")
                    })
    return all_tags

def create_new_tag(tag_groups):
    with st.expander("Create a new tag"):
        new_tag_in_existing_group = st.checkbox("Add to existing tag group")
        
        if new_tag_in_existing_group and tag_groups:
            tag_group_options = [(group["name"], group["id"]) for group in tag_groups]
            tag_group_name, tag_group_id = st.selectbox(
                "Tag Group", 
                options=tag_group_options,
                format_func=lambda x: x[0]
            )
            
            new_tag_name = st.text_input("New Tag Name")
            
            if st.button("Create Tag"):
                if new_tag_name:
                    create_tag(tag_group_id, new_tag_name)
        else:
            new_tag_group_name = st.text_input("New Tag Group Name")
            new_tag_name = st.text_input("New Tag Name")
            
            if st.button("Create Tag Group and Tag"):
                if new_tag_group_name and new_tag_name:
                    # First create the tag group
                    group_result = create_tag_group(new_tag_group_name)
                    if group_result:
                        # Then create the tag in the new group
                        create_tag(group_result["id"], new_tag_name)

def show_tags_section():
    # Get tag groups
    tag_groups = get_tag_groups()
    
    if tag_groups:
        st.subheader("Available Tags")
        all_tags = available_tags(tag_groups)
    else:
        st.info("No tag groups found.")
    
    # Option to create new tags
    st.subheader("Create New Tag")
    create_new_tag(tag_groups)

    return all_tags