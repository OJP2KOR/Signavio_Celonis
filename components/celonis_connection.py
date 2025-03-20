import streamlit as st

def celonis_connection_section():
    with st.expander("Connect to Celonis", expanded=not st.session_state.celonis_connected):
        celonis_url = st.text_input("Celonis URL", value="bosch.eu-4.celonis.cloud", key="celonis_url")
        celonis_api_token = st.text_input("Celonis API Token", type="password", 
                                    value=st.session_state.get('celonis_app_key', ''), key="celonis_api_token")
        
        # Proxy settings
        use_celonis_proxy = st.checkbox("Use Proxy for Celonis", 
                                    value=st.session_state.get('use_proxy', True), 
                                    key="use_celonis_proxy")
        
        if use_celonis_proxy:
            celonis_proxy_host = st.text_input("Proxy Host", 
                                        value=st.session_state.get('proxy_host', "rb-proxy-unix-de01.bosch.com"), 
                                        key="celonis_proxy_host")
            celonis_proxy_port = st.text_input("Proxy Port", 
                                        value=st.session_state.get('proxy_port', "8080"), 
                                        key="celonis_proxy_port")
            celonis_proxy_username = st.text_input("Proxy Username", 
                                            value=st.session_state.get('proxy_username', ""), 
                                            key="celonis_proxy_username")
            celonis_proxy_password = st.text_input("Proxy Password", type="password", 
                                            value=st.session_state.get('proxy_password', ""), 
                                            key="celonis_proxy_password")
        
        if st.button("Connect to Celonis", key="connect_celonis_btn"):
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
                    
                    # Save credentials to session state
                    st.session_state['celonis_url_value'] = celonis_url
                    st.session_state['celonis_api_token_value'] = celonis_api_token
                    st.session_state['use_proxy_value'] = use_celonis_proxy
                    
                    if use_celonis_proxy:
                        st.session_state.proxy_host = celonis_proxy_host
                        st.session_state.proxy_port = celonis_proxy_port
                        st.session_state.proxy_username = celonis_proxy_username
                        st.session_state.proxy_password = celonis_proxy_password
                    
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
                    
                    # Store celonis object in session state
                    st.session_state.celonis = celonis
                    
                    st.session_state.celonis_connected = True
                    st.success("Connected to Celonis successfully!")
                    
                    # Get data pools
                    st.info("Fetching data pools...")
                    data_pools = celonis.data_integration.get_data_pools()
                    
                    # Display data pools
                    pool_options = [(pool.name, pool.id, pool) for pool in data_pools]
                    st.session_state.pool_options = pool_options
                    st.success(f"Found {len(pool_options)} data pools.")

                    st.session_state.celonis_connected = True
                    
            except Exception as e:
                st.error(f"Error connecting to Celonis: {str(e)}")
