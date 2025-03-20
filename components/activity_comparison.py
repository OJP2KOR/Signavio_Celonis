import streamlit as st

def missing_activities_section():
    st.subheader("Add Missing Activities")
                    
    st.info("Adding these missing activities to Celonis is necessary for proper conformance checking.")

    # # Function to update confirmation state
    # def update_confirm_add():
    #     st.session_state.confirm_add = True

    # Checkbox to confirm adding missing activities
    confirm_add = st.checkbox(
                "I confirm that I want to add the missing activities to Celonis",
                key="confirm_add"
            )
    
    if confirm_add:
        if st.session_state.has_change_date:
            # Can add silently using append
            if st.button("Add Missing Activities", key="add_activities_btn"):
                try:
                    with st.spinner("Adding missing activities..."):
                        # Create DataFrame with missing activities
                        import pandas as pd
                        new_entries_df = pd.DataFrame({
                            st.session_state.selected_column: st.session_state.missing_activities
                        })
                        
                        # Append to the table
                        st.session_state.selected_table.append(new_entries_df)
                        
                        st.success("Activities added successfully to Celonis!")
                        
                        # Refresh the activity list
                        st.info("Refreshing activity list...")
                        
                        # Get updated data
                        activity_table_dm = st.session_state.activity_table_dm
                        activity_columns = activity_table_dm.get_columns()
                        
                        import pycelonis.pql as pql
                        column_dict = {
                            st.session_state.selected_column: activity_columns.find(st.session_state.selected_column)
                        }
                        
                        df = pql.DataFrame(column_dict)
                        new_existing_activities = df[st.session_state.selected_column].unique().tolist()
                        
                        # Update session state
                        st.session_state.existing_activities = new_existing_activities
                        
                        # Check if all activities are now present
                        still_missing = [task for task in st.session_state.bpmn_tasks 
                                    if task not in new_existing_activities]
                        
                        if still_missing:
                            st.warning(f"There are still {len(still_missing)} missing activities.")
                            for act in sorted(still_missing):
                                st.write(f"- {act}")
                        else:
                            st.success("All activities are now in Celonis!")
                except Exception as e:
                    st.error(f"Error adding activities: {str(e)}")
        else:
            # Cannot add silently, provide SQL statements
            st.info("The activity table doesn't have a _CELONIS_CHANGE_DATE column. You need to add activities manually.")
            
            # Generate SQL statements
            sql_statements = []
            for act in sorted(st.session_state.missing_activities):
                # Escape single quotes in the activity name
                escaped_act = act.replace("'", "''")
                sql = f"INSERT INTO \"{st.session_state.selected_table_name}\" (\"{st.session_state.selected_column}\") VALUES ('{escaped_act}')"
                sql_statements.append(sql)
            
            st.code("\n".join(sql_statements), language="sql")
            
            # Provide link to data pool
            pool_id = st.session_state.selected_pool.id
            pool_url = f"https://{st.session_state.celonis_url_value}/integration/ui/pools/{pool_id}"
            st.markdown(f"[Open Data Pool in Celonis]({pool_url})")

def display_activity_comparison():
    # Display the comparison

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("BPMN Activities")
        st.info(f"Found {len(st.session_state.bpmn_tasks)} activities in BPMN")
        for task in sorted(st.session_state.bpmn_tasks):
            st.write(f"- {task}")
    
    with col2:
        st.subheader("Celonis Activities")
        st.info(f"Found {len(st.session_state.existing_activities)} activities in Celonis")
        if len(st.session_state.existing_activities) <= 20:
            for act in sorted(st.session_state.existing_activities):
                st.write(f"- {act}")
        else:
            st.write(f"Too many activities to display ({len(st.session_state.existing_activities)})")
    
    if st.session_state.missing_activities:
        st.subheader("Missing Activities")
        st.warning(f"Found {len(st.session_state.missing_activities)} activities in BPMN that are missing in Celonis.")
        for act in st.session_state.missing_activities:
            st.write(f"- {act}")
        missing_activities_section()
    else:
        st.success("All BPMN activities are already in Celonis!")