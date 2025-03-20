import streamlit as st

def activity_table_selection_section():
    st.subheader("Select Activity Table")
    
    with st.form("data_act_table_form"):
        table_names = [table[0] for table in st.session_state.table_options]
        selected_table_name = st.selectbox(
            "Activity Table", 
            options=table_names, 
            key="table_selector"
        )
        st.session_state.selected_table_name = selected_table_name
        
        submit_act_table = st.form_submit_button("Select Activity Table")
    
    if submit_act_table:
        with st.spinner("Processing table selection..."):
            # Find the selected table
            selected_table = next((table for name, id, table in st.session_state.table_options if name == selected_table_name), None)
            
            if selected_table:
                # Store the selected table
                st.session_state.selected_table = selected_table
                
                # Get the activity table from data model
                activity_table_dm = st.session_state.selected_model.get_tables().find(selected_table_name)
                st.session_state.activity_table_dm = activity_table_dm
                
                # Get columns for activity table using cached function
                try:
                    activity_columns = activity_table_dm.get_columns()
                    
                    # Store columns in session state
                    column_options = [column.name for column in activity_columns]
                    st.session_state.column_options = column_options
                    
                    # Check if _CELONIS_CHANGE_DATE exists in columns
                    has_change_date = any('_CELONIS_CHANGE_DATE' in col for col in column_options)
                    st.session_state.has_change_date = has_change_date
                    
                    # Set table selected flag
                    st.session_state.table_selected = True
                    
                    st.success(f"Selected activity table: {selected_table_name}")
                    st.success(f"Found {len(column_options)} columns.")
                    
                except Exception as e:
                    st.error(f"Error fetching columns: {str(e)}")