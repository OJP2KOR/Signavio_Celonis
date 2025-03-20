import streamlit as st
import requests
from xml.etree import ElementTree as ET
import os
import tempfile

from api.process_models import get_process_models, create_process_model


def check_process_model(process_models):
    if process_models:
        st.subheader("Available Process Models")
        
        # Display process models with select buttons
        for pm in process_models:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{pm['name']}** (ID: {pm['id']})")
            with col2:
                if st.button(f"Select", key=f"select_pm_{pm['id']}"):
                    st.session_state.selected_process_model = pm
    else:
        st.info("No process models found for this category.")
        
def show_process_model_section():
    # Get process models for the selected category
    process_models = get_process_models(st.session_state.selected_category['id'])

    check_process_model(process_models)

    # Option to create a new process model
    st.subheader("Create New Process Model")
    with st.expander("Create a new process model"):
        new_model_name = st.text_input("New Process Model Name")
        
        if st.button("Create Process Model"):
            if new_model_name:
                result = create_process_model(st.session_state.selected_category['id'], new_model_name)
                if result:
                    st.session_state.selected_process_model = result