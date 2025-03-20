import streamlit as st

def data_model_selection_section():
    st.subheader("Select Data Model")
    
    # Use a form to group the selectbox and button
    with st.form("data_model_form"):
        model_names = [model[0] for model in st.session_state.model_options]
        selected_model_name = st.selectbox(
            "Data Pool", 
            options=model_names, 
            key="model_selector"
        )
        submit_model = st.form_submit_button("Select Data Model")
    
    if submit_model:
        with st.spinner("Processing data model selection..."):
            # Find the selected model
            selected_model = next((model for name, id, model in st.session_state.model_options if name == selected_model_name), None)
            
            if selected_model:
                # Store the selected model
                st.session_state.selected_model = selected_model
                
                # Get tables for this model using cached function
                try:
                    tables = selected_model.get_tables()
                    
                    # Store tables in session state
                    table_options = [(table.name, table.id, table) for table in tables]
                    st.session_state.table_options = table_options
                    
                    # Set model selected flag
                    st.session_state.model_selected = True
                    
                    st.success(f"Selected data model: {selected_model_name}")
                    st.success(f"Found {len(table_options)} tables.")
                    
                except Exception as e:
                    st.error(f"Error fetching tables: {str(e)}")