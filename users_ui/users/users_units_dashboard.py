# Show Overview data like total users, total units..
import streamlit as st
import os


def drawUsersDashboard():
    NODES_NAME=st.session_state.nodesId["identifier"]
    current_dir=os.getcwd()
    user_permissions = st.session_state.user_permissions
    Nodes_pages = []
    for i in range(1, len(st.session_state.nodesId)):
        pod = f"{NODES_NAME}-{i}"
        if pod in user_permissions:
            page = st.Page(f"{current_dir}/nodes/{NODES_NAME}_{i}.py", title=f"{NODES_NAME} {i}", icon="🛜", default=(i == 1))
            Nodes_pages.append(page)

    pages = {
        f"{NODES_NAME}s": Nodes_pages
    }
    st.logo(f"{current_dir}/images/logo.png",size="large")
    st.sidebar.subheader("Energy Monitoring Dashboard")
    st.sidebar.markdown(
        "Anedya energy monitoring dashboard with Elmeasure(lg64xx)."
    )
    if len(st.session_state.user_permissions) > 0:
        pg = st.navigation(pages)
        pg.run()
    else:
        st.error(f"You don't have permission to access any {NODES_NAME}")
    
    
