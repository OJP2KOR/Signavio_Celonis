import streamlit as st

from api.categories import get_categories, create_category

def build_category_hierarchy(categories):
    """
    Build a hierarchical structure of categories for display.
    
    Args:
        categories (list): List of category objects from the API
        
    Returns:
        tuple: (category_dict, root_categories) containing the category hierarchy
    """
    category_dict = {}
    root_categories = []
    
    # First pass: create category dictionary
    for cat in categories:
        category_dict[cat["id"]] = {
            "name": cat["name"],
            "level": cat["level"],
            "parent_id": cat["parentId"],
            "id": cat["id"],
            "children": []
        }
    
    # Second pass: build hierarchy
    for cat in categories:
        if cat["parentId"]:
            if cat["parentId"] in category_dict:  # Check if parent exists
                category_dict[cat["parentId"]]["children"].append(category_dict[cat["id"]])
        else:
            root_categories.append(category_dict[cat["id"]])
    
    return category_dict, root_categories

# Recursive function to display the category tree with select buttons
def display_category(category_dict, category, indent=""):
    col1, col2 = st.columns([4, 1])
    with col1:
        parent_info = f"(Parent: {category_dict[category['parent_id']]['name']})" if category["parent_id"] else "(Super Category)"
        st.markdown(f"{indent}📁 **{category['name']}** {parent_info}")
    with col2:
        if st.button(f"Select", key=f"select_cat_{category['id']}"):
            st.session_state.selected_category = category
            st.rerun()
    
    for child in category["children"]:
        display_category(category_dict, child, indent + "&nbsp;&nbsp;&nbsp;&nbsp;")

def show_category_selection():
    categories = get_categories()

    # Build hierarchy
    category_dict, root_categories = build_category_hierarchy(categories)

    st.subheader("Category Hierarchy")

    # Display category tree
    for root in root_categories:
        display_category(category_dict, root)
    
    # Option to create a new category
    st.subheader("Create New Category")
    with st.expander("Create a new category"):
        new_category_name = st.text_input("New Category Name")
        create_as_subcategory = st.checkbox("Create as subcategory")
        
        parent_category_id = None
        if create_as_subcategory:
            parent_options = [("None", None)] + [(cat["name"], cat["id"]) for cat in categories]
            parent_name, parent_category_id = st.selectbox(
                "Parent Category", 
                options=parent_options,
                format_func=lambda x: x[0],
                index=0
            )
        
        if st.button("Create Category"):
            if new_category_name:
                created_category = create_category(new_category_name, parent_category_id)
                
                if created_category:
                    # Refresh categories after creation
                    categories = get_categories()
                    category_dict, root_categories = build_category_hierarchy(categories)

                    # Set newly created category as selected
                    st.session_state.selected_category = created_category

                    # Rerun to reflect updates
                    st.rerun()