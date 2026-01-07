import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="GroFlow", page_icon="🌱", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🌱 GroFlow")
st.sidebar.info("The Closed-Loop AI Growth Ecosystem for MSMEs")

# The menu to choose pages
page = st.sidebar.radio("Go to:", ["Home", "AI Assistant", "Fundraising", "Adaptive Tracker"])

# --- PAGE 1: HOME ---
if page == "Home":
    st.title("Welcome to GroFlow")
    st.markdown("""
    ### Overcoming the Resource Paralysis Paradox
    Small businesses have quality products but lack time and capital. GroFlow solves this with three integrated tools:
    
    * **🤖 Constraint-Aware AI Assistant:** Your virtual manager for realistic micro-actions.
    * **💰 Metric-Driven Fundraising:** Convert community 'Trust Points' into micro-funding.
    * **📈 Closed-Loop Adaptive Tracker:** Auto-recalibrates your strategy when real life happens.
    """)
    st.success("👈 Select 'AI Assistant' from the sidebar to test the AI!")

# --- PAGE 2: AI ASSISTANT (Powered by Gemini) ---
elif page == "AI Assistant":
    st.header("🤖 Constraint-Aware AI Assistant")
    
    # 1. API Key Input
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("Enter your current resources. The AI will generate a custom plan.")
    
    # 2. User Inputs
    with st.form("ai_form"):
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("💰 Available Marketing Budget ($)", min_value=0, value=50)
        with col2:
            time = st.slider("⏳ Time Available (Hours per Week)", 0, 40, 5)
        
        inventory = st.selectbox("📦 Inventory Status", ["Overstocked", "Healthy", "Low Stock"])
        business_type = st.text_input("What do you sell?", "Handmade Soap") 
        
        submitted = st.form_submit_button("Generate AI Plan")

    # 3. AI Logic
    if submitted:
        if not api_key:
            st.error("❌ Please enter your API Key in the sidebar first!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Act as an expert business consultant for a small business selling {business_type}.
                Constraints: Budget=${budget}, Time={time} hours/week, Inventory={inventory}.
                
                Generate a plan:
                1. Three specific "Micro-Actions" to do immediately.
                2. Explain why this fits the budget/time.
                """
                
                with st.spinner("Consulting the AI..."):
                    response = model.generate_content(prompt)
                    st.divider()
                    st.subheader("Your Custom AI Strategy")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Error: {e}")

# --- PAGE 3: FUNDRAISING (Placeholder) ---
elif page == "Fundraising":
    st.header("💰 Metric-Driven Fundraising")
    st.write("Coming soon...")

# --- PAGE 4: TRACKER (Placeholder) ---
elif page == "Adaptive Tracker":
    st.header("📈 Closed-Loop Adaptive Tracker")
    st.write("Coming soon...")