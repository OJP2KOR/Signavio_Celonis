"""
File handling utilities for BPMN Cloud Upload Tool.

This module handles file upload, validation, and processing for BPMN XML files.
"""

import os
import tempfile
import streamlit as st
from xml.etree import ElementTree as ET
from config import MAX_PREVIEW_CHARS

def process_bpmn_upload(uploaded_file):
    """
    Process an uploaded BPMN file, validate it, and store in session state.
    
    Args:
        uploaded_file: The Streamlit UploadedFile object
        
    Returns:
        bool: True if file was successfully processed, False otherwise
    """
    if uploaded_file is None:
        return False
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bpmn') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
        
        # Read the file
        with open(temp_file_path, 'r', encoding='utf-8') as file:
            bpmn_content = file.read()
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Check if it's valid XML
        try:
            ET.fromstring(bpmn_content)
            st.session_state.bpmn_content = bpmn_content
            st.session_state.bpmn_loaded = True
            st.success(f"BPMN file '{uploaded_file.name}' loaded successfully!")
            
            # Show a preview of the XML content
            with st.expander("Preview BPMN XML"):
                preview_content = bpmn_content[:MAX_PREVIEW_CHARS]
                if len(bpmn_content) > MAX_PREVIEW_CHARS:
                    preview_content += "..."
                st.code(preview_content, language="xml")
            
            return st.session_state.bpmn_loaded
            
        except ET.ParseError as e:
            st.error(f"Invalid XML format: {str(e)}")
            return False
            
    except Exception as e:
        st.error(f"Error loading BPMN file: {str(e)}")
        return False