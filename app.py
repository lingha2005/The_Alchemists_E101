import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="GroFlow", page_icon="🌱", layout="wide")

# 2. Sidebar Navigation
st.sidebar.title("🌱 GroFlow")
st.sidebar.info("The Closed-Loop AI Growth Ecosystem for MSMEs")
page = st.sidebar.radio("Go to:", ["Home", "AI Assistant", "Fundraising", "Adaptive Tracker"])

# 3. Main Page Logic
if page == "Home":
    st.title("Welcome to GroFlow")
    st.markdown("""
    ### Overcoming the Resource Paralysis Paradox
    Small businesses have quality products but lack time and capital. GroFlow solves this with three integrated tools:
    
    * **🤖 Constraint-Aware AI Assistant:** Your virtual manager for realistic micro-actions.
    * **💰 Metric-Driven Fundraising:** Convert community 'Trust Points' into micro-funding.
    * **📈 Closed-Loop Adaptive Tracker:** Auto-recalibrates your strategy when real life happens.
    """)
    st.success("👈 Select a module from the sidebar to begin.")

elif page == "AI Assistant":
    st.header("🤖 Constraint-Aware AI Assistant")
    st.write("This module will generate micro-actions based on your time and budget.")
    # We will build the logic here in the next step

elif page == "Fundraising":
    st.header("💰 Metric-Driven Fundraising")
    st.write("Showcase products and earn 'Trust Points' to unlock capital.")
    # We will build the logic here later

elif page == "Adaptive Tracker":
    st.header("📈 Closed-Loop Adaptive Tracker")
    st.write("Real-time strategy recalibration based on performance.")
    # We will build the logic here later