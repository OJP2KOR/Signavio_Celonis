"""
BPMN Cloud Upload Tool - Main Application

This is the main entry point for the BPMN Cloud Upload Tool application,
which helps users upload BPMN diagrams to Celonis Process Repository.

The application flow follows these steps:
1. Configure credentials (Celonis API key and proxy settings)
2. Upload BPMN file
3. Select or create a category
4. Select or create a process model
5. Add optional tags
6. Upload the BPMN content to Celonis
"""

import streamlit as st
from xml.etree import ElementTree as ET

from utils.ui import setup_page_config, add_styles, display_header, section_header
from utils.session import initialize_session_state, reset_credentials
from utils.file_handler import process_bpmn_upload
from api.process_models import upload_bpmn_file
from components.credentials import show_credentials_section
from components.category_selection import show_category_selection
from components.process_model_selection import show_process_model_section
from components.tag_selection import show_tags_section
from components.upload_summary import show_upload_summary
############################################################## CELONIS CONNECTION #############################################
from components.celonis_connection import celonis_connection_section
from components.data_pool_selection import data_pool_selection_section
from components.data_model_selection import data_model_selection_section
from components.activity_table_selection import activity_table_selection_section
from components.activity_column_selection import activity_column_selection_section
from components.activity_comparison import display_activity_comparison


def extract_task_names_from_bpmn(bpmn_content):
    """Extract task and event names from BPMN XML content, handling namespaces dynamically."""
    try:
        root = ET.fromstring(bpmn_content)

        # Extract namespace dynamically
        namespace = ""
        if root.tag.startswith("{"):
            namespace = root.tag.split("}")[0][1:]  # Extracts namespace URI

        # List of elements to extract names from
        task_types = [
            "task", "userTask", "serviceTask", "businessRuleTask", "manualTask",
            "scriptTask", "sendTask", "receiveTask", "callActivity", "subProcess",
            "startEvent", "intermediateThrowEvent", "endEvent"
        ]

        tasks = set()

        # Extract names from all specified task elements
        for task_type in task_types:
            for task in root.findall(f".//{{{namespace}}}{task_type}"):
                name = task.get("name")
                if name and name.strip():
                    tasks.add(name.strip())

        return list(tasks)

    except Exception as e:
        return [f"Error parsing BPMN XML: {str(e)}"]

def main():
    """Main application function that orchestrates the workflow."""
    # Setup page configuration and styling
    setup_page_config()
    add_styles()
    display_header()
    
    # Initialize session state variables
    initialize_session_state()

    section_header("1", "Configure Credentials")

    # 1. Show credentials section
    show_credentials_section()
    
    # Only proceed if credentials are set
    if not st.session_state.credentials_set:
        reset_credentials()
        st.stop()

    # 2. Show BPMN file upload section
    section_header("2", "BPMN File")
    uploaded_file = st.file_uploader("Choose a BPMN file", type=['bpmn', 'xml'])
    st.session_state.bpmn_loaded = process_bpmn_upload(uploaded_file)
    
    # Only proceed if BPMN file is loaded
    if not st.session_state.bpmn_loaded:
        st.stop()
    else:
        section_header("3", "Category Selection")
        # 3. Show category selection section
        show_category_selection()
    
    # Only proceed if category is selected
    if not st.session_state.selected_category:
        st.stop()
    else:
        st.success(f"Selected Category: {st.session_state.selected_category['name']} (ID: {st.session_state.selected_category['id']})")
        
        section_header("4", "Process Model Selection")

        # 4. Show process model selection section
        show_process_model_section()
    
    # Only proceed if process model is selected
    if not st.session_state.selected_process_model:
        st.stop()
    else:
        st.success(f"Selected Process Model: {st.session_state.selected_process_model['name']} (ID: {st.session_state.selected_process_model['id']})")
        
        # Tags Selection
        section_header("5", "Tags (Optional)")
    
        # 5. Show tags selection section
        all_tags = show_tags_section()
    
    # 6. Show upload summary and upload button
    section_header("6", "Upload BPMN")

    show_upload_summary(all_tags)

    # Upload button
    if st.button("Upload BPMN to Celonis", type="primary"):
        # Extract tag IDs from the composite keys
        tag_ids = []
        if hasattr(st.session_state, 'selected_tags') and 'all_tags' in locals():
            for tag_key in st.session_state.selected_tags:
                for tag in all_tags:
                    if tag["key"] == tag_key and tag["tag_id"]:
                        tag_ids.append(tag["tag_id"])
        
        # Upload the BPMN content
        success = upload_bpmn_file(
            st.session_state.selected_category['id'],
            st.session_state.selected_process_model['id'],
            st.session_state.bpmn_content,
            tag_ids
        )

        st.balloons()
        st.markdown('<div class="success-message">BPMN uploaded successfully!</div>', unsafe_allow_html=True)
        
        # Extract BPMN task names if not already done
        if success and not st.session_state.bpmn_tasks:
            st.session_state.bpmn_tasks = extract_task_names_from_bpmn(st.session_state.bpmn_content)
        
            # Provide a link to view the process model in Celonis
            celonis_domain = st.session_state.get("CELONIS_BASE_URL", "").split('/api/')[0]
            if celonis_domain:
                view_url = f"{celonis_domain}/ui/{st.session_state.selected_category['id']}"
                st.markdown(f"[View in Celonis Process Repository]({view_url})")

            st.session_state.upload_success = True
    
    # Only proceed if process model is selected
    if not st.session_state.upload_success:
        st.stop()
    else:
        section_header("7", "Celonis Activity Comparison")
        
        # Sidebar navigation
        page = st.sidebar.radio(
            "Navigation",
            ["1️⃣ Connect to Celonis", "2️⃣ Select Data Pool"],
            index=0 if not st.session_state.celonis_connected else 1
        )

        # Connect to Celonis Page
        if page == "1️⃣ Connect to Celonis":

            # 4. Use the checkbox with the key matching the session state variable and specify the on_change function
            # Use a form to group related inputs
            compare_activities = st.checkbox(
                "Compare with Celonis activities and add missing ones",
                value=True,
                key="compare_activities"
            )

            if compare_activities:
                celonis_connection_section()
                # Only show "Next" button if connected
                if st.session_state.celonis_connected:
                    if st.button("Next ➡️", key="to_data_pool"):
                        st.session_state.page = "2️⃣ Select Data Pool"
                        st.rerun()

        # Select Data Pool Page
        elif page == "2️⃣ Select Data Pool":
            st.header("Select Data Pool")

            if not st.session_state.celonis_connected:
                st.warning("⚠️ Please connect to Celonis first!")
                st.stop()

            data_pool_selection_section()

            if not st.session_state.pool_selected:
                st.stop()
            else:
                data_model_selection_section()
            
            if not st.session_state.model_selected:
                st.stop()
            else:
                activity_table_selection_section()
            
            if not st.session_state.table_selected:
                st.stop()
            else:
                activity_column_selection_section()

            if not st.session_state.activities_fetched:
                st.stop()
            else:
                display_activity_comparison()

if __name__ == "__main__":
    main()