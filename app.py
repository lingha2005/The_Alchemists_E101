import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="GroFlow", page_icon="🌱", layout="wide")
# --- HELPER FUNCTION: AI CONNECTION (Debug Version) ---
def ask_gemini(prompt, key):
    # Try Flash first (fastest)
    model = "gemini-2.5-flash"
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, headers=headers, json=payload)
        
        # SUCCESS
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # ERROR HANDLING
        elif response.status_code == 400:
            return f"⚠️ Invalid API Key (Error 400). Please check for spaces."
        elif response.status_code == 429:
            return "⏳ Too Many Requests. Wait 60 seconds."
        else:
            return f"⚠️ Google Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"⚠️ Connection Failed: {str(e)}"

# --- 1. STATE MANAGEMENT (Remembering where we are) ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- 2. ADVANCED CSS (Aesthetic & Animations) ---
st.markdown("""
    <style>
    /* MAIN THEME: Beige & Earthy */
    .stApp {
        background-color: #F9F5EB; /* Light Beige */
        background-image: url("https://www.transparenttextures.com/patterns/concrete-wall.png");
    }
    
    /* SIDEBAR: Darker Beige + Dark Text */
    [data-testid="stSidebar"] {
        background-color: #E6DCC3;
        border-right: 2px solid #6B8E23;
    }
    
    /* TEXT COLORS: Force Dark Brown everywhere */
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown, label {
        color: #4B3621 !important; /* Coffee Brown */
        font-family: 'Helvetica', sans-serif;
    }
    
    /* FIX: Make Metrics (Trust Points) Dark Brown */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #4B3621 !important;
    }
    
    /* NAVIGATION BUTTONS (The "Hover Card" Effect) */
    div.stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 12px;
        background-color: #FDFBF7; /* Cream Card */
        color: #4B3621;
        border: 2px solid #6B8E23; /* Olive Border */
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s ease-in-out;
    }
    
    /* HOVER STATE: Lift up and turn Olive */
    div.stButton > button:hover {
        background-color: #6B8E23; /* Olive Fill */
        color: white !important;
        border-color: #556B2F;
        transform: translateY(-5px) scale(1.02); /* Pop up effect */
        box-shadow: 0px 10px 20px rgba(107, 142, 35, 0.4);
    }
    
    /* HOME BUTTON (Specific Style) */
    [data-testid="stSidebar"] button {
        background-color: #4B3621;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Profile Only - No Menu) ---
with st.sidebar:
    st.title("🌱 GroFlow")
    st.image("https://api.dicebear.com/9.x/micah/svg?seed=Felix", width=100)
    st.write("**Hello, Sarah!**")
    st.caption("Owner: Sarah's Cakes")
    
    if "points" not in st.session_state:
        st.session_state.points = 120
    
    st.write("---")
    st.metric("Trust Points Balance", st.session_state.points, delta="10 pts")
    st.write("---")
    
    # "Home" Button is the only navigation here
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# --- 4. PAGE ROUTING LOGIC ---

# ==========================================
# PAGE: HOME DASHBOARD
# ==========================================
if st.session_state.page == "Home":
    # Hero Section
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.title("🌱 GroFlow")
        st.subheader("Growth. Funding. Freedom.")
        st.markdown("""
        **Welcome to your Command Center.**
        Select a module below to start automating your business.
        """)
    with col2:
        st.image("https://img.freepik.com/free-vector/organic-farming-concept_23-2148425232.jpg?w=740", use_container_width=True)

    st.write("---")
    st.subheader("Select a Module")
    
    # THE NEW NAVIGATION (Clickable Cards)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🤖 **AI Manager**")
        st.caption("Generate instant marketing tasks.")
        if st.button("Launch AI Assistant →"):
            st.session_state.page = "AI Assistant"
            st.rerun()
            
    with c2:
        st.warning("💰 **Fundraising**")
        st.caption("Unlock capital with Trust Points.")
        if st.button("Go to Marketplace →"):
            st.session_state.page = "Fundraising"
            st.rerun()
            
    with c3:
        st.success("📈 **Adaptive Tracker**")
        st.caption("Recalibrate your monthly goals.")
        if st.button("Open Tracker →"):
            st.session_state.page = "Adaptive Tracker"
            st.rerun()

# ==========================================
# PAGE: AI ASSISTANT (Fixed Error Handling & Model)
# ==========================================
elif st.session_state.page == "AI Assistant":
    st.header("🤖 Constraint-Aware AI Assistant")
    st.caption("Your Virtual Business Manager")
    
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

    tab_quick, tab_monthly = st.tabs(["⚡ Quick Micro-Actions", "📅 Monthly Strategic Plan"])

    # --- TAB 1: QUICK ACTIONS ---
    with tab_quick:
        st.markdown("#### Instant Productivity")
        st.write("Got 15 minutes? Let's fill it with high-impact work.")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                energy_level = st.select_slider("🔋 Your Current Energy Level", options=["Low (Tired)", "Medium", "High (Let's go!)"])
                time_now = st.selectbox("⏳ Time You Have RIGHT NOW", ["10 Minutes", "30 Minutes", "1 Hour"])
            with col2:
                platform = st.multiselect("📱 Platforms You Use", ["Instagram", "WhatsApp", "Email", "TikTok", "LinkedIn"], default=["Instagram"])
                task_type = st.selectbox("🎯 Focus Area", ["Sales/Revenue", "Brand Awareness", "Admin/Cleanup"])

            if st.button("⚡ Generate Quick Wins", type="primary"):
                if not api_key:
                    st.error("Please enter your API Key in the sidebar!")
                else:
                    with st.spinner("Finding high-impact tasks..."):
                        try:
                            # FIX 1: Switched to 'gemini-pro' (More reliable)
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                            headers = {'Content-Type': 'application/json'}
                            
                            prompt = f"""
                            Act as a productivity coach. Context: Energy={energy_level}, Time={time_now}, Focus={task_type}, Platforms={platform}.
                            Give me exactly 3 "Micro-Actions" I can do RIGHT NOW. No fluff.
                            """
                            
                            payload = {"contents": [{"parts": [{"text": prompt}]}]}
                            response = requests.post(url, headers=headers, json=payload)
                            
                            if response.status_code == 200:
                                ai_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                                st.success("🚀 Ready to execute:")
                                st.markdown(ai_text)
                            else:
                                # FIX 2: Show the REAL error message
                                st.error(f"⚠️ Error {response.status_code}: {response.text}")
                        except Exception as e:
                            st.error(f"Connection Error: {e}")

    # --- TAB 2: MONTHLY STRATEGY ---
# --- TAB 2: MONTHLY STRATEGY (Interactive) ---
    with tab_monthly:
        st.markdown("#### Strategic Growth Engine")
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                goal_text = st.text_input("🏆 Main Goal", placeholder="e.g. Launch Summer Collection")
                business_desc = st.text_input("🛒 What do you sell?", "Handmade Jewelry")
            with c2:
                duration = st.slider("🗓️ Duration (Weeks)", 4, 12, 4)
                budget_monthly = st.number_input("💰 Total Budget ($)", 0, 10000, 500)
            
            if st.button("📅 Draft Interactive Roadmap"):
                # Check for API Key in Session State
                if "api_key" not in st.session_state or not st.session_state["api_key"]:
                    st.error("Please enter your API Key in the sidebar first!")
                else:
                    with st.spinner("🤖 AI is designing your tracker..."):
                        
                        # We demand JSON format so we can build checkboxes
                        prompt = f"""
                        Act as a Project Manager. 
                        Context: Business={business_desc}, Goal={goal_text}, Duration={duration} weeks, Budget=${budget_monthly}.
                        
                        OUTPUT FORMAT INSTRUCTION:
                        You must output ONLY valid JSON. Do not write intro text.
                        Structure the JSON as a list of phases. Example:
                        [
                            {{"phase": "Week 1: Setup", "tasks": ["Task A", "Task B"]}},
                            {{"phase": "Week 2: Launch", "tasks": ["Task C", "Task D"]}}
                        ]
                        Generate {duration} phases (one per week).
                        """
                        
                        try:
                            # 1. Get the Raw Text from AI
                            ai_response_text = ask_gemini(prompt, st.session_state["api_key"])
                            
                            # 2. Clean the text (sometimes AI adds ```json ... ``` wrappers)
                            clean_json = ai_response_text.replace("```json", "").replace("```", "").strip()
                            
                            # 3. Convert Text to Data
                            import json
                            roadmap_data = json.loads(clean_json)
                            
                            # 4. Save to Session State (So it stays when we click checkboxes)
                            st.session_state["generated_roadmap"] = roadmap_data
                            st.rerun()
                            
                        except Exception as e:
                            st.error("AI generated text instead of data. Please try again.")
                            st.write(ai_response_text) # Show the raw text just in case

        # --- DISPLAY THE INTERACTIVE TRACKER ---
        if "generated_roadmap" in st.session_state:
            st.divider()
            st.subheader(f"🚀 Your {duration}-Week Action Plan")
            st.caption("This is your custom-built tracker. Check off items as you go!")
            
            # Loop through the data and build UI
            for phase in st.session_state["generated_roadmap"]:
                with st.expander(f"📌 {phase['phase']}", expanded=True):
                    for task in phase['tasks']:
                        st.checkbox(task, key=task) # Unique key for every task

            if st.button("🗑️ Clear Plan"):
                del st.session_state["generated_roadmap"]
                st.rerun()
# ==========================================
# PAGE: FUNDRAISING (Pinterest/Instagram Style)
# ==========================================
elif st.session_state.page == "Fundraising":
    
    # --- 1. HEADER & WALLET ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("💰 Community Marketplace")
        st.caption("Discover businesses, Vouch for quality, and help them unlock capital.")
    with col2:
        # High-visibility Wallet
        st.metric("Your Trust Points", st.session_state.points, delta="Available to spend")

    st.divider()

    # --- 2. UPLOAD SECTION (The "Create" Button) ---
    with st.expander("➕ Create a New Campaign"):
        with st.form("new_campaign"):
            c1, c2 = st.columns([1, 2])
            with c1:
                # Simulating an image upload (we'll just use a placeholder if they don't have one)
                uploaded_file = st.file_uploader("Product Image", type=["jpg", "png"])
            with c2:
                new_title = st.text_input("Campaign Title")
                new_desc = st.text_area("Description")
                new_goal = st.number_input("Goal (Points)", value=1000)
            
            if st.form_submit_button("Post Campaign"):
                new_camp = {
                    "name": new_title, 
                    "owner": "You", 
                    "desc": new_desc,
                    "points": 0, 
                    "goal": new_goal,
                    # If no image uploaded, use a random one
                    "image": "https://picsum.photos/400/300?random=99" if not uploaded_file else uploaded_file
                }
                st.session_state.campaigns.append(new_camp)
                st.success("Campaign Posted!")
                st.rerun()

    # --- 3. THE FEED (Pinterest Grid) ---
    
    # Initialize Mock Data if empty
    if "campaigns" not in st.session_state:
        st.session_state.campaigns = [
            {
                "name": "EcoWraps", 
                "owner": "Sarah S.", 
                "desc": "Replacing plastic wrap with organic beeswax sheets.",
                "points": 850, 
                "goal": 1000,
                "image": "ecowraps.jpg"
            },
            {
                "name": "WoodToys", 
                "owner": "ToyCraft", 
                "desc": "Safe, non-toxic toys made from reclaimed wood.",
                "points": 400, 
                "goal": 1000,
                "image": "woodtoys.jpg"
            },
            {
                "name": "KeralaSpices", 
                "owner": "SpiceRoute", 
                "desc": "Authentic homemade spice blends from Kerala.",
                "points": 980, 
                "goal": 1000,
                "image": "spices.jpg"
            },
        ]

    # Grid Layout (3 Columns)
    cols = st.columns(3)
    
    for i, camp in enumerate(st.session_state.campaigns):
        # We cycle through columns 0, 1, 2
        with cols[i % 3]: 
            with st.container(border=True):
                # IMAGE
                if camp.get("image"):
                    st.image(camp["image"], use_container_width=True)
                
                # DETAILS
                st.subheader(camp["name"])
                st.caption(f"by {camp['owner']}")
                st.write(camp.get("desc", ""))
                
                # PROGRESS BAR
                progress = min(camp["points"] / camp["goal"], 1.0)
                st.progress(progress)
                st.caption(f"🏆 {camp['points']} / {camp['goal']} Trust Points")
                
                # INTERACTION BUTTONS
                b1, b2 = st.columns(2)
                
                with b1:
                    if st.button(f"❤️ Like", key=f"like_{i}"):
                        st.toast("You liked this project!")
                
                with b2:
                    # Logic: Vouching costs YOU points, gives THEM points
                    if camp["points"] >= camp["goal"]:
                        st.success("Funded! 🎉")
                    else:
                        if st.button(f"✨ Vouch (10)", key=f"vouch_{i}"):
                            if st.session_state.points >= 10:
                                st.session_state.points -= 10 # Cost to you
                                st.session_state.campaigns[i]["points"] += 10 # Gain for them
                                st.rerun()
                            else:
                                st.error("Not enough points!")
                
                # COMMENTS SECTION (Simulated)
                with st.expander("💬 Comments"):
                    st.text_input("Add a comment...", key=f"com_{i}")
                    st.write("*Very cool project!* - @mike")
# ==========================================
# PAGE: TRACKER
# ==========================================
# ==========================================
# PAGE: ADAPTIVE TRACKER (With AI & Checklists)
# ==========================================
elif st.session_state.page == "Adaptive Tracker":
    st.header("📈 Closed-Loop Adaptive Tracker")
    st.caption("Real-time accountability: If you miss targets, the AI recalibrates your roadmap.")
    
    # API Key is needed here for the "Recalibrate" feature
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

    # --- 1. PERFORMANCE INPUTS ---
    with st.container(border=True):
        st.subheader("📊 Live Performance Data")
        col1, col2, col3 = st.columns(3)
        
        target = col1.number_input("Monthly Revenue Goal ($)", value=1000)
        current = col2.number_input("Current Revenue Achieved ($)", value=400)
        days = col3.slider("Days Remaining in Month", 1, 30, 10)
    
    # --- 2. WEEKLY CHECKLIST (New Feature) ---
    st.write("---")
    st.subheader("✅ Weekly Milestones Checklist")
    st.caption("Tick the tasks you actually completed this week. The AI analyzes your misses.")
    
    # Organized columns for checkboxes
    c1, c2, c3, c4 = st.columns(4)
    check_1 = c1.checkbox("Posted 3x on Socials")
    check_2 = c2.checkbox("Sent Email Newsletter")
    check_3 = c3.checkbox("Inventory Audit Done")
    check_4 = c4.checkbox("Replied to Reviews")
    
    # Calculate "Execution Score" based on ticks
    completed_tasks = sum([check_1, check_2, check_3, check_4])
    total_tasks = 4
    execution_score = int((completed_tasks / total_tasks) * 100)
    
    # Show a progress bar for the checklist
    st.progress(execution_score / 100)
    st.caption(f"Execution Score: {execution_score}%")

    # --- 3. VISUALS & LOGIC ---
    st.write("---")
    gap = target - current
    
    # Burn-Down Chart (Graph)
    st.subheader("📉 Burn-Down Chart")
    # We create a simulated trend line ending at the current revenue
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Revenue Trend": [current*0.1, current*0.2, current*0.4, current*0.6, current*0.8, current*0.9, current]
    })
    st.line_chart(chart_data, x="Day", y="Revenue Trend", color="#6B8E23")

    # --- 4. AI RECALIBRATION LOGIC ---
    if gap > 0:
        # Standard Math Calculation
        daily_needed = gap / days
        st.error(f"⚠️ You are behind by ${gap}. To catch up, you need ${daily_needed:.2f}/day.")
        
        # The AI Recalibration Button
        if st.button("🔄 AI Recalibrate Strategy", type="primary"):
            if not api_key:
                st.error("Please enter your API Key in the sidebar to recalibrate!")
            else:
                with st.spinner("🤖 AI is analyzing your missed tasks and recalculating..."):
                    
                    # Identify exactly what was missed
                    missed_tasks = []
                    if not check_1: missed_tasks.append("Social Media Posts")
                    if not check_2: missed_tasks.append("Email Newsletter")
                    if not check_3: missed_tasks.append("Inventory Audit")
                    if not check_4: missed_tasks.append("Review Replies")
                    missed_text = ", ".join(missed_tasks) if missed_tasks else "None (Execution was perfect, but Revenue is low)"

                    # The Strategy Prompt
                    prompt = f"""
                    Act as a Crisis Management Coach for a small business.
                    
                    CURRENT STATUS: 
                    - Goal: ${target} | Current: ${current} | Gap: ${gap}
                    - Days Left: {days} days
                    - Execution Score: {execution_score}%
                    
                    MISSED TASKS THIS WEEK: 
                    {missed_text}
                    
                    YOUR TASK:
                    1. CALCULATE the new required Daily Revenue to hit the goal.
                    2. ANALYZE why the gap exists based on the specific missed tasks (e.g., if they missed marketing, explain how that hurts sales).
                    3. GENERATE a strict "Recovery Plan" for the next {days} days to catch up.
                    
                    Keep it encouraging but strict. Maximum Efficiency focus.
                    """
                    
                    # Call the Helper Function (Assumes ask_gemini is defined at the top of your file)
                    result = ask_gemini(prompt, api_key)
                    
                    if "Error" in result or "Too Many Requests" in result:
                        st.error(result)
                    else:
                        st.divider()
                        st.subheader("🚀 Your AI Recovery Plan")
                        st.markdown(result)
                    
    else:
        st.success("🎉 You are on track! Keep up the momentum.")
        st.balloons()