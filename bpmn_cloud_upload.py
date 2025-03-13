import streamlit as st
import requests
import json
from xml.etree import ElementTree as ET
import os
from dotenv import load_dotenv
import tempfile

# Set page configuration
st.set_page_config(
    page_title="BPMN Cloud Upload Tool",
    page_icon="📊",
    layout="wide"
)

# Add styling
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
    .info-message {
        color: blue;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Main title and description
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

# # Load environment variables from .env file or use Streamlit secrets
# def load_credentials():
#     # Try to load from .env file first
#     if os.path.exists('credential.env'):
#         load_dotenv('credential.env')
#         celonis_app_key = os.getenv('CELONIS_APP_KEY_P')
#         proxy_username = os.getenv('PROXY_USERNAME')
#         proxy_password = os.getenv('PROXY_PASSWORD')
#     else:
#         # If no .env file, try to use Streamlit secrets
#         try:
#             celonis_app_key = st.secrets["CELONIS_APP_KEY_P"]
#             proxy_username = st.secrets["PROXY_USERNAME"]
#             proxy_password = st.secrets["PROXY_PASSWORD"]
#         except:
#             celonis_app_key = None
#             proxy_username = None
#             proxy_password = None
    
#     return celonis_app_key, proxy_username, proxy_password

# Initialize session state variables if they don't exist
if 'credentials_set' not in st.session_state:
    st.session_state.credentials_set = False
if 'bpmn_loaded' not in st.session_state:
    st.session_state.bpmn_loaded = False
if 'bpmn_content' not in st.session_state:
    st.session_state.bpmn_content = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_process_model' not in st.session_state:
    st.session_state.selected_process_model = None
if 'selected_tags' not in st.session_state:
    st.session_state.selected_tags = []
if 'proxies' not in st.session_state:
    st.session_state.proxies = None
if 'celonis_app_key' not in st.session_state:
    st.session_state.celonis_app_key = None
if 'celonis_base_url' not in st.session_state:
    st.session_state.celonis_base_url = "https://bosch.eu-4.celonis.cloud/process-repository/api/v1"


# Configure Celonis and proxy settings
st.markdown('<div class="section-header">1. Configure Credentials</div>', unsafe_allow_html=True)

# celonis_app_key, proxy_username, proxy_password = load_credentials()

# # Option for manual credential input
# with st.expander("Configure credentials manually", expanded=not st.session_state.credentials_set):
#     col1, col2 = st.columns(2)
#     with col1:
#         celonis_app_key_input = st.text_input("Celonis App Key", value=celonis_app_key if celonis_app_key else "", type="password")
#     with col2:
#         celonis_base_url = st.text_input("Celonis Base URL", value="https://bosch.eu-4.celonis.cloud/process-repository/api/v1")
    
#     st.subheader("Proxy Settings")
#     use_proxy = st.checkbox("Use Proxy", value=True)
    
#     if use_proxy:
#         col1, col2 = st.columns(2)
#         with col1:
#             proxy_username_input = st.text_input("Proxy Username", value=proxy_username if proxy_username else "")
#             proxy_host = st.text_input("Proxy Host", value="rb-proxy-unix-de01.bosch.com")
#         with col2:
#             proxy_password_input = st.text_input("Proxy Password", value=proxy_password if proxy_password else "", type="password")
#             proxy_port = st.text_input("Proxy Port", value="8080")
    
#     if st.button("Save Credentials"):
#         if not celonis_app_key_input:
#             st.error("Celonis App Key is required")
#         else:
#             celonis_app_key = celonis_app_key_input
#             if use_proxy:
#                 proxy_username = proxy_username_input
#                 proxy_password = proxy_password_input
#             else:
#                 proxy_username = None
#                 proxy_password = None
            
#             st.session_state.credentials_set = True
#             st.success("Credentials saved successfully!")

with st.expander("Configure credentials", expanded=not st.session_state.credentials_set):
    col1, col2 = st.columns(2)
    with col1:
        celonis_app_key_input = st.text_input("Celonis App Key", type="password")
    with col2:
        celonis_base_url = st.text_input("Celonis Base URL", value="https://bosch.eu-4.celonis.cloud/process-repository/api/v1")
    
    st.subheader("Proxy Settings")
    use_proxy = st.checkbox("Use Proxy", value=True)
    
    if use_proxy:
        col1, col2 = st.columns(2)
        with col1:
            proxy_username_input = st.text_input("Proxy Username")
            proxy_host = st.text_input("Proxy Host", value="rb-proxy-unix-de01.bosch.com")
        with col2:
            proxy_password_input = st.text_input("Proxy Password", type="password")
            proxy_port = st.text_input("Proxy Port", value="8080")
    
    if st.button("Save Credentials"):
        if not celonis_app_key_input:
            st.error("Celonis App Key is required")
        else:
            st.session_state.celonis_app_key = celonis_app_key_input
            st.session_state.celonis_base_url = celonis_base_url
            
            if use_proxy:
                st.session_state.proxy_username = proxy_username_input
                st.session_state.proxy_password = proxy_password_input
                st.session_state.proxy_host = proxy_host
                st.session_state.proxy_port = proxy_port
                st.session_state.use_proxy = True
                
                # Configure proxies
                proxy_url = f"http://{proxy_username_input}:{proxy_password_input}@{proxy_host}:{proxy_port}"
                st.session_state.proxies = {
                    "http": proxy_url,
                    "https": proxy_url,
                }
            else:
                st.session_state.use_proxy = False
                st.session_state.proxies = None
            
            st.session_state.credentials_set = True
            st.success("Credentials saved successfully!")

# Only proceed if credentials are set
# Only proceed if credentials are set
if not st.session_state.credentials_set and not st.session_state.celonis_app_key:
    st.warning("Please configure your credentials to proceed.")
    st.stop()

# API configuration
CELONIS_BASE_URL = st.session_state.celonis_base_url
CELONIS_AUTH_HEADERS = {
    "Authorization": f'Bearer {st.session_state.celonis_app_key}',
    "Content-Type": "application/json"
}

# Use session state for proxies
proxies = st.session_state.proxies

# API functions
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_categories():
    try:
        url = f"{CELONIS_BASE_URL}/categories"
        response = requests.get(url, headers=CELONIS_AUTH_HEADERS, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get categories: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting categories: {str(e)}")
        return []

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_process_models(category_id):
    try:
        url = f"{CELONIS_BASE_URL}/categories/{category_id}/process-models"
        response = requests.get(url, headers=CELONIS_AUTH_HEADERS, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get process models: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting process models: {str(e)}")
        return []

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_tag_groups():
    try:
        url = f"{CELONIS_BASE_URL}/tag-groups"
        response = requests.get(url, headers=CELONIS_AUTH_HEADERS, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get tag groups: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error getting tag groups: {str(e)}")
        return []

def create_category(category_name, parent_id=None):
    try:
        url = f"{CELONIS_BASE_URL}/categories"
        payload = {"name": category_name}
        if parent_id:
            payload["parentId"] = parent_id
        response = requests.post(url, headers=CELONIS_AUTH_HEADERS, json=payload, proxies=proxies)
        if response.status_code == 200:
            st.success(f"Category '{category_name}' created successfully!")
            # Clear cache to refresh the categories list
            get_categories.clear()
            return response.json()
        else:
            st.error(f"Failed to create category: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating category: {str(e)}")
        return None

def create_process_model(category_id, model_name):
    try:
        url = f"{CELONIS_BASE_URL}/categories/{category_id}/process-models"
        payload = {"name": model_name}
        response = requests.post(url, headers=CELONIS_AUTH_HEADERS, json=payload, proxies=proxies)
        if response.status_code == 200:
            st.success(f"Process model '{model_name}' created successfully!")
            # Clear cache to refresh the process models list
            get_process_models.clear()
            return response.json()
        else:
            st.error(f"Failed to create process model: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating process model: {str(e)}")
        return None

def create_tag_group(tag_group_name):
    try:
        url = f"{CELONIS_BASE_URL}/tag-groups"
        payload = {"name": tag_group_name}
        response = requests.post(url, headers=CELONIS_AUTH_HEADERS, json=payload, proxies=proxies)
        if response.status_code == 200:
            st.success(f"Tag group '{tag_group_name}' created successfully!")
            # Clear cache to refresh the tag groups list
            get_tag_groups.clear()
            return response.json()
        else:
            st.error(f"Failed to create tag group: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating tag group: {str(e)}")
        return None

def create_tag(tag_group_id, tag_name):
    try:
        url = f"{CELONIS_BASE_URL}/tag-groups/{tag_group_id}"
        # First get the current tags
        response = requests.get(url, headers=CELONIS_AUTH_HEADERS, proxies=proxies)
        if response.status_code != 200:
            st.error(f"Failed to get tag group: {response.status_code} - {response.text}")
            return None
        
        tag_group = response.json()
        
        # Append the new tag
        tags = tag_group.get("tags", [])
        tags.append({"name": tag_name})
        
        # Update the tag group with the new tag
        payload = {
            "name": tag_group["name"],
            "tags": tags
        }
        
        response = requests.put(url, headers=CELONIS_AUTH_HEADERS, json=payload, proxies=proxies)
        if response.status_code == 200:
            st.success(f"Tag '{tag_name}' created successfully!")
            # Clear cache to refresh the tag groups list
            get_tag_groups.clear()
            return response.json()
        else:
            st.error(f"Failed to create tag: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating tag: {str(e)}")
        return None

def upload_bpmn_file(category_id, process_model_id, bpmn_content, tag_ids=None):
    try:
        # First upload the BPMN file
        url = f"{CELONIS_BASE_URL}/categories/{category_id}/process-models/{process_model_id}/file"
        headers = CELONIS_AUTH_HEADERS.copy()
        headers["Content-Type"] = "application/octet-stream"
        response = requests.post(url, headers=headers, data=bpmn_content, proxies=proxies)
        
        if response.status_code != 200:
            st.error(f"Failed to upload BPMN file: {response.status_code} - {response.text}")
            return False
        
        # If tags are provided, add them to the process model
        if tag_ids and len(tag_ids) > 0:
            url = f"{CELONIS_BASE_URL}/categories/{category_id}/process-models/{process_model_id}"
            
            # First get the current process model details
            response = requests.get(url, headers=CELONIS_AUTH_HEADERS, proxies=proxies)
            if response.status_code != 200:
                st.error(f"Failed to get process model details: {response.status_code} - {response.text}")
                return False
            
            process_model = response.json()
            
            # Update with tags
            payload = {
                "name": process_model["name"],
                "tagIds": tag_ids
            }
            
            response = requests.put(url, headers=CELONIS_AUTH_HEADERS, json=payload, proxies=proxies)
            if response.status_code != 200:
                st.error(f"Failed to add tags to process model: {response.status_code} - {response.text}")
                return False
        
        return True
    except Exception as e:
        st.error(f"Error uploading BPMN file: {str(e)}")
        return False

# Signavio BPMN Export (placeholder)
st.markdown('<div class="section-header">2. BPMN File</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Upload BPMN File", "Signavio BPMN Export (Coming Soon)"])

with tab1:
    uploaded_file = st.file_uploader("Choose a BPMN file", type=['bpmn', 'xml'])
    
    if uploaded_file is not None:
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
                    st.code(bpmn_content[:2000] + ("..." if len(bpmn_content) > 2000 else ""), language="xml")
            except ET.ParseError as e:
                st.error(f"Invalid XML format: {str(e)}")
        except Exception as e:
            st.error(f"Error loading BPMN file: {str(e)}")

with tab2:
    st.info("Signavio API integration will be available in a future update.")
    
    # Placeholder for Signavio API form
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Signavio API Key", disabled=True)
        st.text_input("Tenant ID", disabled=True)
    with col2:
        st.text_input("Directory ID", disabled=True)
        st.text_input("Diagram ID", disabled=True)
    
    st.button("Import from Signavio", disabled=True)

def extract_task_names_from_bpmn(bpmn_content):
    """Extract task names from BPMN XML content."""
    try:
        root = ET.fromstring(bpmn_content)
        
        # Define namespaces for BPMN XML
        namespaces = {
            'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        }
        
        # Find all task elements
        tasks = []
        
        # Regular tasks
        for task in root.findall('.//bpmn:task', namespaces):
            name = task.get('name')
            if name and name.strip():
                tasks.append(name.strip())
        
        # User tasks
        for task in root.findall('.//bpmn:userTask', namespaces):
            name = task.get('name')
            if name and name.strip():
                tasks.append(name.strip())
        
        # Service tasks
        for task in root.findall('.//bpmn:serviceTask', namespaces):
            name = task.get('name')
            if name and name.strip():
                tasks.append(name.strip())
        
        # Business rule tasks
        for task in root.findall('.//bpmn:businessRuleTask', namespaces):
            name = task.get('name')
            if name and name.strip():
                tasks.append(name.strip())
                
        # Manual tasks
        for task in root.findall('.//bpmn:manualTask', namespaces):
            name = task.get('name')
            if name and name.strip():
                tasks.append(name.strip())
        
        # Remove duplicates and return
        return list(set(tasks))
    except Exception as e:
        st.error(f"Error parsing BPMN XML: {str(e)}")
        return []

# If BPMN file is loaded, proceed with category selection
if st.session_state.bpmn_loaded:
    st.markdown('<div class="section-header">3. Category Selection</div>', unsafe_allow_html=True)
    
    # Get categories
    categories = get_categories()
    
    # Create a hierarchical structure of categories
    category_dict = {}
    root_categories = []
    
    for cat in categories:
        category_dict[cat["id"]] = {
            "name": cat["name"],
            "level": cat["level"],
            "parent_id": cat["parentId"],
            "id": cat["id"],
            "children": []
        }
    
    for cat in categories:
        if cat["parentId"]:
            if cat["parentId"] in category_dict:  # Check if parent exists
                category_dict[cat["parentId"]]["children"].append(category_dict[cat["id"]])
        else:
            root_categories.append(category_dict[cat["id"]])
    
    # Display categories as a tree
    st.subheader("Category Hierarchy")
    
    # Recursive function to display the category tree with select buttons
    def display_category(category, indent=""):
        col1, col2 = st.columns([4, 1])
        with col1:
            parent_info = f"(Parent: {category_dict[category['parent_id']]['name']})" if category["parent_id"] else "(Super Category)"
            st.markdown(f"{indent}📁 **{category['name']}** {parent_info}")
        with col2:
            if st.button(f"Select", key=f"select_cat_{category['id']}"):
                st.session_state.selected_category = category
        
        for child in category["children"]:
            display_category(child, indent + "&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # Display the category tree
    for root in root_categories:
        display_category(root)
    
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
                result = create_category(new_category_name, parent_category_id)
                if result:
                    # Refresh the categories
                    categories = get_categories()
    
    # Show the selected category
    if st.session_state.selected_category:
        st.success(f"Selected Category: {st.session_state.selected_category['name']} (ID: {st.session_state.selected_category['id']})")
        
        # Process Model Selection
        st.markdown('<div class="section-header">4. Process Model Selection</div>', unsafe_allow_html=True)
        
        # Get process models for the selected category
        process_models = get_process_models(st.session_state.selected_category['id'])
        
        if process_models:
            st.subheader("Available Process Models")
            
            # Display process models as a table
            pm_data = []
            for pm in process_models:
                pm_data.append({
                    "Name": pm["name"],
                    "ID": pm["id"],
                    "Created At": pm.get("createdAt", ""),
                    "Updated At": pm.get("updatedAt", "")
                })
            
            # Display process models with select buttons
            for i, pm in enumerate(process_models):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{pm['name']}** (ID: {pm['id']})")
                with col2:
                    if st.button(f"Select", key=f"select_pm_{pm['id']}"):
                        st.session_state.selected_process_model = pm
        else:
            st.info("No process models found for this category.")
        
        # Option to create a new process model
        st.subheader("Create New Process Model")
        with st.expander("Create a new process model"):
            new_model_name = st.text_input("New Process Model Name")
            
            if st.button("Create Process Model"):
                if new_model_name:
                    result = create_process_model(st.session_state.selected_category['id'], new_model_name)
                    if result:
                        st.session_state.selected_process_model = result
        
        # Show the selected process model
        if st.session_state.selected_process_model:
            st.success(f"Selected Process Model: {st.session_state.selected_process_model['name']} (ID: {st.session_state.selected_process_model['id']})")
            
            # Tags Selection
            st.markdown('<div class="section-header">5. Tags (Optional)</div>', unsafe_allow_html=True)
            
            # Get tag groups
            tag_groups = get_tag_groups()
            
            if tag_groups:
                st.subheader("Available Tags")
                
                all_tags = []
                # Display tags from all tag groups
                for tag_group in tag_groups:
                    if "tags" in tag_group and tag_group["tags"]:
                        with st.expander(f"Tag Group: {tag_group['name']}"):
                            for tag in tag_group["tags"]:
                                tag_key = f"{tag_group['id']}_{tag.get('id', '')}"
                                tag_selected = st.checkbox(
                                    tag.get("name", "Unnamed Tag"), 
                                    key=f"tag_{tag_key}",
                                    value=tag_key in st.session_state.selected_tags
                                )
                                
                                if tag_selected and tag_key not in st.session_state.selected_tags:
                                    st.session_state.selected_tags.append(tag_key)
                                elif not tag_selected and tag_key in st.session_state.selected_tags:
                                    st.session_state.selected_tags.remove(tag_key)
                                
                                all_tags.append({
                                    "group_id": tag_group['id'],
                                    "tag_id": tag.get('id', ''),
                                    "key": tag_key,
                                    "name": tag.get("name", "Unnamed Tag")
                                })
            else:
                st.info("No tag groups found.")
            
            # Option to create new tags
            st.subheader("Create New Tag")
            with st.expander("Create a new tag"):
                new_tag_in_existing_group = st.checkbox("Add to existing tag group")
                
                if new_tag_in_existing_group and tag_groups:
                    tag_group_options = [(group["name"], group["id"]) for group in tag_groups]
                    tag_group_name, tag_group_id = st.selectbox(
                        "Tag Group", 
                        options=tag_group_options,
                        format_func=lambda x: x[0]
                    )
                    
                    new_tag_name = st.text_input("New Tag Name")
                    
                    if st.button("Create Tag"):
                        if new_tag_name:
                            result = create_tag(tag_group_id, new_tag_name)
                else:
                    new_tag_group_name = st.text_input("New Tag Group Name")
                    new_tag_name = st.text_input("New Tag Name")
                    
                    if st.button("Create Tag Group and Tag"):
                        if new_tag_group_name and new_tag_name:
                            # First create the tag group
                            group_result = create_tag_group(new_tag_group_name)
                            if group_result:
                                # Then create the tag in the new group
                                tag_result = create_tag(group_result["id"], new_tag_name)
            
            # Final Upload Section
            st.markdown('<div class="section-header">6. Upload BPMN</div>', unsafe_allow_html=True)
            
            # Show summary before upload
            st.subheader("Upload Summary")
            st.markdown(f"**Category:** {st.session_state.selected_category['name']}")
            st.markdown(f"**Process Model:** {st.session_state.selected_process_model['name']}")
            
            # Show selected tags
            if st.session_state.selected_tags:
                st.markdown("**Selected Tags:**")
                for tag_key in st.session_state.selected_tags:
                    for tag in all_tags:
                        if tag["key"] == tag_key:
                            st.markdown(f"- {tag['name']}")
            else:
                st.markdown("**Selected Tags:** None")

            

            # New section for Celonis activity comparison
            st.markdown('<div class="section-header">7. Celonis Activity Comparison</div>', unsafe_allow_html=True)
            
            # Extract BPMN task names
            bpmn_tasks = extract_task_names_from_bpmn(st.session_state.bpmn_content)
            
            if bpmn_tasks:
                st.subheader("BPMN Tasks Detected")
                st.write(f"Found {len(bpmn_tasks)} unique tasks in the BPMN diagram:")
                for task in bpmn_tasks:
                    st.write(f"- {task}")
                
                # Ask if user wants to compare with Celonis activities
                if st.checkbox("Compare with Celonis activities and add missing ones"):
                    with st.expander("Connect to Celonis", expanded=True):
                        # # Get Celonis credentials (reuse the ones from earlier if available)
                        # celonis_url = st.text_input("Celonis URL", value="bosch.eu-4.celonis.cloud")
                        # celonis_api_token = st.text_input("Celonis API Token", type="password", 
                        #                             value=st.session_state.celonis_app_key if st.session_state.celonis_app_key else "")
                        celonis_url = st.text_input("Celonis URL", value="bosch.eu-4.celonis.cloud", key="celonis_url")
                        celonis_api_token = st.text_input("Celonis API Token", type="password", value=st.session_state.celonis_app_key if st.session_state.celonis_app_key else "", key="celonis_api_token")
                        
                        # Proxy settings
                        use_celonis_proxy = st.checkbox("Use Proxy for Celonis", value=st.session_state.use_proxy if "use_proxy" in st.session_state else True)
                        if use_celonis_proxy:
                            celonis_proxy_host = st.text_input("Proxy Host", value=st.session_state.proxy_host if "proxy_host" in st.session_state else "rb-proxy-unix-de01.bosch.com", key="celonis_proxy_host")
                            celonis_proxy_port = st.text_input("Proxy Port", value=st.session_state.proxy_port if "proxy_port" in st.session_state else "8080", key="celonis_proxy_port")
                            celonis_proxy_username = st.text_input("Proxy Username", value=st.session_state.proxy_username if "proxy_username" in st.session_state else "", key="celonis_proxy_username")
                            celonis_proxy_password = st.text_input("Proxy Password", type="password", value=st.session_state.proxy_password if "proxy_password" in st.session_state else "", key="celonis_proxy_password")
                        
                        if st.button("Connect to Celonis"):
                            try:
                                with st.spinner("Connecting to Celonis..."):
                                    # Import required packages
                                    st.info("Importing required packages...")
                                    import platform
                                    
                                    try:
                                        from pycelonis import get_celonis
                                        import httpx
                                    except ImportError:
                                        st.error("The required packages 'pycelonis' and 'httpx' are not installed. Please install them using pip.")
                                        st.code("pip install pycelonis httpx", language="bash")
                                        st.stop()
                                    
                                    # Create the proxy URL if using proxy
                                    proxy_mounts = None
                                    if use_celonis_proxy and celonis_proxy_username and celonis_proxy_password:
                                        proxy_url = f"http://{celonis_proxy_username}:{celonis_proxy_password}@{celonis_proxy_host}:{celonis_proxy_port}"
                                        proxy_mounts = {
                                            "http://": httpx.HTTPTransport(proxy=proxy_url),
                                            "https://": httpx.HTTPTransport(proxy=proxy_url)
                                        }
                                    
                                    # Celonis connection settings
                                    login = {
                                        "base_url": celonis_url,
                                        "api_token": celonis_api_token,
                                        "timeout": 120,
                                        "retries": 1,
                                        "permissions": False,
                                        "connect": True,
                                        "mounts": proxy_mounts,
                                        "key_type": "USER_KEY"
                                    }
                                    
                                    login_ems = { 
                                        "api_token": celonis_api_token,
                                        "key_type": "USER_KEY",
                                        "timeout": 120,
                                        "retries": 1,
                                        "permissions": False
                                    }
                                    
                                    # Connect to Celonis based on platform
                                    st.info(f"Connecting to Celonis on {platform.system()}...")
                                    if platform.system() == 'Windows':
                                        celonis = get_celonis(**login)            
                                    else:
                                        celonis = get_celonis(**login_ems)
                                    
                                    # Store in session state
                                    st.session_state.celonis = celonis
                                    st.success("Connected to Celonis successfully!")
                                    
                                    # Get data pools
                                    st.info("Fetching data pools...")
                                    data_pools = celonis.data_integration.get_data_pools()
                                    st.session_state.data_pools = data_pools
                                    
                                    # Display data pools
                                    pool_options = [(pool.name, pool.id, pool) for pool in data_pools]
                                    st.session_state.pool_options = pool_options
                                    st.success(f"Found {len(pool_options)} data pools.")
                                    
                            except Exception as e:
                                st.error(f"Error connecting to Celonis: {str(e)}")
                    
                    # If connected to Celonis and data pools available
                    if 'celonis' in st.session_state and 'pool_options' in st.session_state:
                        st.subheader("Select Data Pool")
                        
                        pool_names = [pool[0] for pool in st.session_state.pool_options]
                        selected_pool_name = st.selectbox("Data Pool", options=pool_names)
                        
                        if st.button("Select Data Pool"):
                            # Find the selected pool
                            selected_pool_id = None
                            selected_pool = None
                            for name, id, pool in st.session_state.pool_options:
                                if name == selected_pool_name:
                                    selected_pool_id = id
                                    selected_pool = pool
                                    break
                            
                            if selected_pool:
                                st.session_state.selected_pool = selected_pool
                                
                                # Get data models for this pool
                                try:
                                    with st.spinner("Fetching data models..."):
                                        data_models = selected_pool.get_data_models()
                                        st.session_state.data_models = data_models
                                        
                                        # Display data models
                                        model_options = [(model.name, model.id, model) for model in data_models]
                                        st.session_state.model_options = model_options
                                        
                                        st.success(f"Selected data pool: {selected_pool_name}")
                                        st.success(f"Found {len(model_options)} data models.")
                                except Exception as e:
                                    st.error(f"Error fetching data models: {str(e)}")
                    
                    # If data models available
                    if 'model_options' in st.session_state:
                        st.subheader("Select Data Model")
                        
                        model_names = [model[0] for model in st.session_state.model_options]
                        selected_model_name = st.selectbox("Data Model", options=model_names)
                        
                        if st.button("Select Data Model"):
                            # Find the selected model
                            selected_model = None
                            for name, id, model in st.session_state.model_options:
                                if name == selected_model_name:
                                    selected_model = model
                                    break
                            
                            if selected_model:
                                st.session_state.selected_model = selected_model
                                
                                # Get tables for this model
                                try:
                                    with st.spinner("Fetching tables..."):
                                        tables = selected_model.get_tables()
                                        st.session_state.tables = tables
                                        
                                        # Display tables
                                        table_options = [(table.name, table.id, table) for table in tables]
                                        st.session_state.table_options = table_options
                                        
                                        st.success(f"Selected data model: {selected_model_name}")
                                        st.success(f"Found {len(table_options)} tables.")
                                except Exception as e:
                                    st.error(f"Error fetching tables: {str(e)}")
                    
                    # If tables available
                    if 'table_options' in st.session_state:
                        st.subheader("Select Activity Table")
                        
                        table_names = [table[0] for table in st.session_state.table_options]
                        selected_table_name = st.selectbox("Activity Table", options=table_names)
                        
                        if st.button("Select Activity Table"):
                            # Find the selected table
                            selected_table = None
                            for name, id, table in st.session_state.table_options:
                                if name == selected_table_name:
                                    selected_table = table
                                    break
                            
                            if selected_table:
                                st.session_state.selected_table = selected_table
                                
                                # Get columns for this table
                                try:
                                    with st.spinner("Fetching columns..."):
                                        columns = selected_table.get_columns()
                                        st.session_state.columns = columns
                                        
                                        # Display columns
                                        column_options = [column.name for column in columns]
                                        st.session_state.column_options = column_options
                                        
                                        st.success(f"Selected activity table: {selected_table_name}")
                                        st.success(f"Found {len(column_options)} columns.")
                                except Exception as e:
                                    st.error(f"Error fetching columns: {str(e)}")
                    
                    # If columns available
                    if 'column_options' in st.session_state:
                        st.subheader("Select Activity Column")
                        
                        selected_column_name = st.selectbox("Activity Column", options=st.session_state.column_options)
                        
                        if st.button("Select Activity Column"):
                            st.session_state.selected_column = selected_column_name
                            
                            # Get existing activities
                            try:
                                with st.spinner("Fetching and comparing activities..."):
                                    # Check if the table contains activities
                                    activity_table = st.session_state.selected_pool.get_tables().find(st.session_state.selected_table.name)
                                    
                                    # Get all columns to check for CELONISCHANGE_DATE
                                    table_columns = activity_table.get_columns()
                                    column_names = [col.name for col in table_columns]
                                    
                                    # Check if CELONISCHANGE_DATE exists in columns
                                    has_change_date = any('CELONISCHANGE_DATE' in col for col in column_names)
                                    st.session_state.has_change_date = has_change_date
                                    
                                    # Get existing activities using selected column
                                    query = f"SELECT DISTINCT \"{selected_column_name}\" FROM \"{activity_table.name}\""
                                    activities_df = st.session_state.selected_model.get_data_frame(query)
                                    
                                    existing_activities = activities_df[selected_column_name].dropna().tolist()
                                    st.session_state.existing_activities = existing_activities
                                    
                                    # Compare with BPMN tasks
                                    missing_activities = [task for task in bpmn_tasks if task not in existing_activities]
                                    st.session_state.missing_activities = missing_activities
                                    
                                    if missing_activities:
                                        st.warning(f"Found {len(missing_activities)} activities in BPMN that are missing in Celonis.")
                                        st.write("Missing activities:")
                                        for act in missing_activities:
                                            st.write(f"- {act}")
                                    else:
                                        st.success("All BPMN activities are already in Celonis!")
                                        
                            except Exception as e:
                                st.error(f"Error comparing activities: {str(e)}")
                    
                    # If missing activities found
                    if 'missing_activities' in st.session_state and st.session_state.missing_activities:
                        st.subheader("Add Missing Activities")
                        
                        confirm = st.checkbox("I confirm that I want to add the missing activities to Celonis")
                        
                        if confirm:
                            if 'has_change_date' in st.session_state and st.session_state.has_change_date:
                                # Can add silently using append
                                if st.button("Add Missing Activities"):
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
                                    except Exception as e:
                                        st.error(f"Error adding activities: {str(e)}")
                            else:
                                # Cannot add silently, provide SQL statements
                                st.info("The activity table doesn't have '*CELONIS*CHANGE_DATE' column. You need to add activities manually.")
                                
                                # Generate SQL statements
                                sql_statements = []
                                for act in st.session_state.missing_activities:
                                    # Escape single quotes in the activity name
                                    escaped_act = act.replace("'", "''")
                                    sql = f"INSERT INTO \"{st.session_state.selected_table.name}\" (\"{st.session_state.selected_column}\") VALUES ('{escaped_act}')"
                                    sql_statements.append(sql)
                                
                                st.code("\n".join(sql_statements), language="sql")
                                
                                # Provide link to data pool
                                if 'celonis_url' in locals():
                                    pool_id = st.session_state.selected_pool.id
                                    pool_url = f"https://{celonis_url}/integration/ui/pools/{pool_id}"
                                    st.markdown(f"[Open Data Pool in Celonis]({pool_url})")
            
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
                
                if success:
                    st.balloons()
                    st.markdown('<div class="success-message">BPMN uploaded successfully!</div>', unsafe_allow_html=True)

                    # New section for Celonis activity comparison
                    st.markdown('<div class="section-header">7. Celonis Activity Comparison</div>', unsafe_allow_html=True)
                    
                    # Provide a link to view the process model in Celonis
                    celonis_domain = CELONIS_BASE_URL.split('/api/')[0]
                    view_url = f"{celonis_domain}/ui/{st.session_state.selected_category['id']}"
                    
                    st.markdown(f"[View in Celonis Process Repository]({view_url})")

                    # # New section for Celonis activity comparison
                    # st.markdown('<div class="section-header">7. Celonis Activity Comparison</div>', unsafe_allow_html=True)
                    
                    # # Extract BPMN task names
                    # bpmn_tasks = extract_task_names_from_bpmn(st.session_state.bpmn_content)
                    
                    # if bpmn_tasks:
                    #     st.subheader("BPMN Tasks Detected")
                    #     st.write(f"Found {len(bpmn_tasks)} unique tasks in the BPMN diagram:")
                    #     for task in bpmn_tasks:
                    #         st.write(f"- {task}")
                        
                    #     # Ask if user wants to compare with Celonis activities
                    #     if st.checkbox("Compare with Celonis activities and add missing ones"):
                    #         with st.expander("Connect to Celonis", expanded=True):
                    #             # Get Celonis credentials (reuse the ones from earlier if available)
                    #             celonis_url = st.text_input("Celonis URL", value="bosch.eu-4.celonis.cloud")
                    #             celonis_api_token = st.text_input("Celonis API Token", type="password", 
                    #                                         value=celonis_app_key if 'celonis_app_key' in locals() else "")
                                
                    #             # Proxy settings
                    #             use_celonis_proxy = st.checkbox("Use Proxy for Celonis", value=True)
                    #             if use_celonis_proxy:
                    #                 celonis_proxy_host = st.text_input("Proxy Host", value=proxy_host if 'proxy_host' in locals() else "rb-proxy-unix-de01.bosch.com")
                    #                 celonis_proxy_port = st.text_input("Proxy Port", value=proxy_port if 'proxy_port' in locals() else "8080")
                    #                 celonis_proxy_username = st.text_input("Proxy Username", value=proxy_username if 'proxy_username' in locals() else "")
                    #                 celonis_proxy_password = st.text_input("Proxy Password", type="password", 
                    #                                                 value=proxy_password if 'proxy_password' in locals() else "")
                                
                    #             if st.button("Connect to Celonis"):
                    #                 try:
                    #                     with st.spinner("Connecting to Celonis..."):
                    #                         import platform
                    #                         from pycelonis import get_celonis
                    #                         import httpx
                                            
                    #                         # Create the proxy URL if using proxy
                    #                         if use_celonis_proxy:
                    #                             proxy_url = f"http://{celonis_proxy_username}:{celonis_proxy_password}@{celonis_proxy_host}:{celonis_proxy_port}"
                    #                             proxy_mounts = {
                    #                                 "http://": httpx.HTTPTransport(proxy=proxy_url),
                    #                                 "https://": httpx.HTTPTransport(proxy=proxy_url)
                    #                             }
                    #                         else:
                    #                             proxy_mounts = None
                                            
                    #                         # Celonis connection settings
                    #                         login = {
                    #                             "base_url": celonis_url,
                    #                             "api_token": celonis_api_token,
                    #                             "timeout": 120,
                    #                             "retries": 1,
                    #                             "permissions": False,
                    #                             "connect": True,
                    #                             "mounts": proxy_mounts,
                    #                             "key_type": "USER_KEY"
                    #                         }
                                            
                    #                         login_ems = { 
                    #                             "api_token": celonis_api_token,
                    #                             "key_type": "USER_KEY",
                    #                             "timeout": 120,
                    #                             "retries": 1,
                    #                             "permissions": False
                    #                         }
                                            
                    #                         # Connect to Celonis
                    #                         if platform.system() == 'Windows':
                    #                             celonis = get_celonis(**login)            
                    #                         else:
                    #                             celonis = get_celonis(**login_ems)
                                            
                    #                         # Store in session state
                    #                         st.session_state.celonis = celonis
                    #                         st.success("Connected to Celonis successfully!")
                                            
                    #                         # Get data pools
                    #                         data_pools = celonis.data_integration.get_data_pools()
                    #                         st.session_state.data_pools = data_pools
                                            
                    #                         # Display data pools
                    #                         pool_options = [(pool.name, pool.id, pool) for pool in data_pools]
                    #                         st.session_state.pool_options = pool_options
                                            
                    #                 except Exception as e:
                    #                     st.error(f"Error connecting to Celonis: {str(e)}")
                            
                    #         # If connected to Celonis and data pools available
                    #         if 'celonis' in st.session_state and 'pool_options' in st.session_state:
                    #             st.subheader("Select Data Pool")
                                
                    #             pool_names = [pool[0] for pool in st.session_state.pool_options]
                    #             selected_pool_name = st.selectbox("Data Pool", options=pool_names)
                                
                    #             if st.button("Select Data Pool"):
                    #                 # Find the selected pool
                    #                 selected_pool_id = None
                    #                 selected_pool = None
                    #                 for name, id, pool in st.session_state.pool_options:
                    #                     if name == selected_pool_name:
                    #                         selected_pool_id = id
                    #                         selected_pool = pool
                    #                         break
                                    
                    #                 if selected_pool:
                    #                     st.session_state.selected_pool = selected_pool
                                        
                    #                     # Get data models for this pool
                    #                     data_models = selected_pool.get_data_models()
                    #                     st.session_state.data_models = data_models
                                        
                    #                     # Display data models
                    #                     model_options = [(model.name, model.id, model) for model in data_models]
                    #                     st.session_state.model_options = model_options
                                        
                    #                     st.success(f"Selected data pool: {selected_pool_name}")
                            
                    #         # If data models available
                    #         if 'model_options' in st.session_state:
                    #             st.subheader("Select Data Model")
                                
                    #             model_names = [model[0] for model in st.session_state.model_options]
                    #             selected_model_name = st.selectbox("Data Model", options=model_names)
                                
                    #             if st.button("Select Data Model"):
                    #                 # Find the selected model
                    #                 selected_model = None
                    #                 for name, id, model in st.session_state.model_options:
                    #                     if name == selected_model_name:
                    #                         selected_model = model
                    #                         break
                                    
                    #                 if selected_model:
                    #                     st.session_state.selected_model = selected_model
                                        
                    #                     # Get tables for this model
                    #                     tables = selected_model.get_tables()
                    #                     st.session_state.tables = tables
                                        
                    #                     # Display tables
                    #                     table_options = [(table.name, table.id, table) for table in tables]
                    #                     st.session_state.table_options = table_options
                                        
                    #                     st.success(f"Selected data model: {selected_model_name}")
                            
                    #         # If tables available
                    #         if 'table_options' in st.session_state:
                    #             st.subheader("Select Activity Table")
                                
                    #             table_names = [table[0] for table in st.session_state.table_options]
                    #             selected_table_name = st.selectbox("Activity Table", options=table_names)
                                
                    #             if st.button("Select Activity Table"):
                    #                 # Find the selected table
                    #                 selected_table = None
                    #                 for name, id, table in st.session_state.table_options:
                    #                     if name == selected_table_name:
                    #                         selected_table = table
                    #                         break
                                    
                    #                 if selected_table:
                    #                     st.session_state.selected_table = selected_table
                                        
                    #                     # Get columns for this table
                    #                     columns = selected_table.get_columns()
                    #                     st.session_state.columns = columns
                                        
                    #                     # Display columns
                    #                     column_options = [column.name for column in columns]
                    #                     st.session_state.column_options = column_options
                                        
                    #                     st.success(f"Selected activity table: {selected_table_name}")
                            
                    #         # If columns available
                    #         if 'column_options' in st.session_state:
                    #             st.subheader("Select Activity Column")
                                
                    #             selected_column_name = st.selectbox("Activity Column", options=st.session_state.column_options)
                                
                    #             if st.button("Select Activity Column"):
                    #                 st.session_state.selected_column = selected_column_name
                                    
                    #                 # Get existing activities
                    #                 try:
                    #                     # Check if the table contains activities
                    #                     query = f"SELECT DISTINCT \"{selected_column_name}\" FROM \"{st.session_state.selected_table.name}\""
                    #                     activities_df = st.session_state.selected_model.get_data_frame(query)
                                        
                    #                     existing_activities = activities_df[selected_column_name].dropna().tolist()
                    #                     st.session_state.existing_activities = existing_activities
                                        
                    #                     # Compare with BPMN tasks
                    #                     missing_activities = [task for task in bpmn_tasks if task not in existing_activities]
                    #                     st.session_state.missing_activities = missing_activities
                                        
                    #                     if missing_activities:
                    #                         st.warning(f"Found {len(missing_activities)} activities in BPMN that are missing in Celonis.")
                    #                         st.write("Missing activities:")
                    #                         for act in missing_activities:
                    #                             st.write(f"- {act}")
                    #                     else:
                    #                         st.success("All BPMN activities are already in Celonis!")
                                        
                    #                     # Check if the table has *CELONIS*CHANGE_DATE column
                    #                     has_change_date = any("*CELONIS*CHANGE_DATE" in col for col in st.session_state.column_options)
                    #                     st.session_state.has_change_date = has_change_date
                                        
                    #                 except Exception as e:
                    #                     st.error(f"Error comparing activities: {str(e)}")
                            
                    #         # If missing activities found
                    #         if 'missing_activities' in st.session_state and st.session_state.missing_activities:
                    #             st.subheader("Add Missing Activities")
                                
                    #             confirm = st.checkbox("I confirm that I want to add the missing activities to Celonis")
                                
                    #             if confirm:
                    #                 if 'has_change_date' in st.session_state and st.session_state.has_change_date:
                    #                     # Can add silently using append
                    #                     if st.button("Add Missing Activities"):
                    #                         try:
                    #                             with st.spinner("Adding missing activities..."):
                    #                                 # Create DataFrame with missing activities
                    #                                 import pandas as pd
                    #                                 new_entries_df = pd.DataFrame({
                    #                                     st.session_state.selected_column: st.session_state.missing_activities
                    #                                 })
                                                    
                    #                                 # Append to the table
                    #                                 st.session_state.selected_table.append(new_entries_df)
                                                    
                    #                                 st.success("Activities added successfully to Celonis!")
                    #                         except Exception as e:
                    #                             st.error(f"Error adding activities: {str(e)}")
                    #                 else:
                    #                     # Cannot add silently, provide SQL statements
                    #                     st.info("The activity table doesn't have '*CELONIS*CHANGE_DATE' column. You need to add activities manually.")
                                        
                    #                     # Generate SQL statements
                    #                     sql_statements = []
                    #                     for act in st.session_state.missing_activities:
                    #                         sql = f"INSERT INTO \"{st.session_state.selected_table.name}\" (\"{st.session_state.selected_column}\") VALUES ('{act}')"
                    #                         sql_statements.append(sql)
                                        
                    #                     st.code("\n".join(sql_statements), language="sql")
                                        
                    #                     # Provide link to data pool
                    #                     pool_id = st.session_state.selected_pool.id
                    #                     pool_url = f"https://{celonis_url}/integration/ui/pools/{pool_id}"
                    #                     st.markdown(f"[Open Data Pool in Celonis]({pool_url})")


# Footer
st.markdown("---")
st.markdown("BPMN Cloud Upload Tool - Developed for Bosch")