import streamlit as st
import requests
from xml.etree import ElementTree as ET
import os
import tempfile

def show_upload_summary(all_tags):
    # Show summary before upload
    st.subheader("Upload Summary")
    st.markdown(f"**Category:** {st.session_state.selected_category['name']}")
    st.markdown(f"**Process Model:** {st.session_state.selected_process_model['name']}")

    # Show selected tags
    if st.session_state.selected_tags:
        st.markdown("**Selected Tags:**")
        for tag_key in st.session_state.selected_tags:
            for tag in all_tags:
                if tag["key"] == tag_key:
                    st.markdown(f"- {tag['name']}")
    else:
        st.markdown("**Selected Tags:** None")