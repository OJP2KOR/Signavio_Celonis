"""
UI components and styling for BPMN Cloud Upload Tool.

This module contains UI-related functions that help maintain a consistent
look and feel throughout the application.
"""

import streamlit as st

def setup_page_config():
    """
    Configure Streamlit page settings including title, icon, and layout.
    """
    st.set_page_config(
        page_title="BPMN Cloud Upload Tool",
        page_icon="📊",
        layout="wide"
    )

def add_styles():
    """
    Add custom CSS styling to the application.
    
    This includes styles for headers, success and error messages, etc.
    """
    st.markdown("""
    <style>
        .main-header {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 22px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .success-message {
            color: green;
            font-weight: bold;
        }
        .error-message {
            color: red;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """
    Display the main application header and description.
    """
    st.markdown('<div class="main-header">BPMN Cloud Upload Tool</div>', unsafe_allow_html=True)
    st.markdown("""
    This application helps you upload BPMN diagrams to Celonis Process Repository.
    The workflow involves:
    1. Loading a BPMN XML file
    2. Selecting or creating a category
    3. Selecting or creating a process model
    4. Adding tags (optional)
    5. Uploading the BPMN content
    """)

def section_header(section_number, title):
    """
    Display a numbered section header with consistent styling.
    
    Args:
        title (str): The title of the section
        section_number (int): The numerical order of the section
    """
    st.markdown(f'<div class="section-header">{section_number}. {title}</div>', 
                unsafe_allow_html=True)