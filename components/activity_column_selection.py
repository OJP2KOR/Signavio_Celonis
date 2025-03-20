import streamlit as st

def activity_column_selection_section():
    st.subheader("Select Activity Column")
    with st.form("data_act_col_form"):
        selected_column_name = st.selectbox(
            "Activity Column", 
            options=st.session_state.column_options, 
            key="column_selector"
        )
        
        submit_exist_act = st.form_submit_button("Get Existing Activities")
    
    if submit_exist_act:
        with st.spinner("Analyzing activities..."):
            try:
                # Store the selected column name
                st.session_state.selected_column = selected_column_name
                
                # Get the activity table columns
                activity_table_dm = st.session_state.activity_table_dm
                activity_columns = activity_table_dm.get_columns()
                
                # Import PQL for DataFrame creation
                import pycelonis.pql as pql
                from pycelonis.config import Config
                Config.DEFAULT_DATA_MODEL = st.session_state.selected_model

                # Create a dictionary for PQL DataFrame with all columns
                column_dict = {}
                for column in activity_columns:
                    column_dict[column.name] = activity_columns.find(column.name)
                
                # Create PQL DataFrame
                df = pql.DataFrame(column_dict)
                
                # Get unique activity values using cached function
                existing_activities = df[selected_column_name].unique().tolist()
                st.session_state.existing_activities = existing_activities
                
                # Compare with BPMN tasks
                missing_activities = [task for task in st.session_state.bpmn_tasks if task not in existing_activities]
                missing_activities.sort()  # Sort alphabetically
                st.session_state.missing_activities = missing_activities
                
                # Set activities fetched flag
                st.session_state.activities_fetched = True
                
            except Exception as e:
                st.error(f"Error comparing activities: {str(e)}")