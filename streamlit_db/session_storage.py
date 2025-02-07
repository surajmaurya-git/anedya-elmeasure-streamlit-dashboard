import streamlit as st


def initialize_session_state():

    if "view_role" not in st.session_state:
        st.session_state.view_role = "admin"

    if "user_permissions" not in st.session_state:
        st.session_state.user_permissions = []

    if "user_variables_access" not in st.session_state:
        st.session_state.user_variables_access = []

    # ========= Project Controller ================
    if "create_pages" not in st.session_state:  
        st.session_state.create_pages = False
    
    # ======== Anedya ====================
    if "anedya_client" not in st.session_state:
        st.session_state.anedya_client = None

    if "nodeIds" not in st.session_state:
        st.session_state.nodesId = {}
        
    if "variables" not in st.session_state:
        st.session_state.variables= {}
    
    # ======== Firestore =================
    if "firestore_client" not in st.session_state:
        st.session_state.firestore_client = None

    # ======== HTTP ======================
    if "http_client" not in st.session_state:
        st.session_state.http_client = None


    # =========== Controllers ============
    if "door" not in st.session_state:
         st.session_state.door= "Open Door"

    if "light" not in st.session_state:
         st.session_state.light= "Turn Light On"

    if "fan" not in st.session_state:
         st.session_state.fan= "Turn Fan On"

    if "massage" not in st.session_state:
         st.session_state.massage= "Turn Massager On"


