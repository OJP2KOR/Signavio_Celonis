import streamlit as st

def data_pool_selection_section():

    # Use a form to group the selectbox and button
    with st.form("data_pool_form"):
        pool_names = [pool[0] for pool in st.session_state.pool_options]
        selected_pool_name = st.selectbox(
            "Data Pool", 
            options=pool_names, 
            key="pool_selector"
        )
        submit = st.form_submit_button("Select Data Pool")
    
    if submit:
        with st.spinner("Processing data pool selection..."):
            # Find the selected pool
            selected_pool = next((pool for name, id, pool in st.session_state.pool_options if name == selected_pool_name), None)
            
            if selected_pool:
                # Store the selected pool
                st.session_state.selected_pool = selected_pool
                
                # Get data models for this pool using cached function
                try:
                    data_models = selected_pool.get_data_models()
                    
                    # Store data models in session state
                    model_options = [(model.name, model.id, model) for model in data_models]
                    st.session_state.model_options = model_options
                                                
                    st.success(f"Selected data pool: {selected_pool_name}")
                    st.success(f"Found {len(model_options)} data models.")

                    st.session_state.pool_selected = True
                
                except Exception as e:
                    st.error(f"Error fetching data models: {str(e)}")