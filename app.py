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

# Initialize Investor Pool
if "investor_pool" not in st.session_state:
    st.session_state.investor_pool = 5000  # Starting liquidity pool

if "investor_investments" not in st.session_state:
    st.session_state.investor_investments = []

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

# --- 3. SIDEBAR (Profile & Global Settings) ---
with st.sidebar:
    st.title("🌱 GroFlow")
    st.image("https://api.dicebear.com/9.x/micah/svg?seed=Felix", width=100)
    st.write("**Hello, Sarah!**")
    st.caption("Owner: Sarah's Cakes")
    
    # --- GLOBAL API KEY INPUT (The Fix) ---
    st.write("---")
    # This 'key="api_key"' argument automatically saves the input to st.session_state
    st.text_input("🔑 Enter Gemini API Key", type="password", key="api_key")
    
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
        st.image("smallbusiness.jpg", use_container_width=True)

    st.write("---")
    st.subheader("Select a Module")
    
    # THE NEW NAVIGATION (Clickable Cards)
    c1, c2, c3, c4 = st.columns(4)
    
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
    
    with c4:
        st.error("🏦 **Investor Portal**")
        st.caption("Fund businesses & earn returns.")
        if st.button("Access Investor Hub →"):
            st.session_state.page = "Investor Portal"
            st.rerun()

# ==========================================
# PAGE: AI ASSISTANT (Fixed)
# ==========================================
elif st.session_state.page == "AI Assistant":
    st.header("🤖 Constraint-Aware AI Assistant")
    st.caption("Your Virtual Business Manager")
    
    # WE REMOVED THE EXTRA INPUT HERE because it's now in the global sidebar

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
                # Check if the Global Key is missing
                if "api_key" not in st.session_state or not st.session_state.api_key:
                    st.error("Please enter your API Key in the sidebar first!")
                else:
                    with st.spinner("Finding high-impact tasks..."):
                        try:
                            # Use the Global Key
                            key_to_use = st.session_state.api_key
                            
                            # Using 1.5 Flash (Most reliable model)
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key_to_use}"
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
                                st.error(f"⚠️ Error {response.status_code}: {response.text}")
                        except Exception as e:
                            st.error(f"Connection Error: {e}")

    # --- TAB 2: MONTHLY STRATEGY ---
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
                # Check Global Key
                if "api_key" not in st.session_state or not st.session_state.api_key:
                    st.error("Please enter your API Key in the sidebar first!")
                else:
                    with st.spinner("🤖 AI is designing your tracker..."):
                        
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
                            # Use Global Key
                            key_to_use = st.session_state.api_key
                            ai_response_text = ask_gemini(prompt, key_to_use)
                            
                            # Clean and Parse
                            clean_json = ai_response_text.replace("```json", "").replace("```", "").strip()
                            import json
                            roadmap_data = json.loads(clean_json)
                            
                            # Save Plan
                            st.session_state["generated_roadmap"] = roadmap_data
                            st.rerun()
                            
                        except Exception as e:
                            st.error("AI generated text instead of data. Please try again.")
                            st.write(ai_response_text) # Debugging

        # Display Plan
        if "generated_roadmap" in st.session_state:
            st.divider()
            st.subheader(f"🚀 Your {duration}-Week Action Plan")
            st.caption("This is your custom-built tracker. Check off items as you go!")
            
            for phase in st.session_state["generated_roadmap"]:
                with st.expander(f"📌 {phase['phase']}", expanded=True):
                    for task in phase['tasks']:
                        st.checkbox(task, key=task)

            if st.button("🗑️ Clear Plan"):
                del st.session_state["generated_roadmap"]
                st.rerun()# ==========================================
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
                    "image": "https://picsum.photos/400/300?random=99" if not uploaded_file else uploaded_file,
                    "funded_by_investors": False,
                    "investor_funding": 0
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
                "image": "ecowraps.jpg",
                "funded_by_investors": False,
                "investor_funding": 0,
                "community_vouches": 42,
                "monthly_revenue": 2500,
                "months_in_business": 8
            },
            {
                "name": "WoodToys", 
                "owner": "ToyCraft", 
                "desc": "Safe, non-toxic toys made from reclaimed wood.",
                "points": 400, 
                "goal": 1000,
                "image": "woodtoys.jpg",
                "funded_by_investors": False,
                "investor_funding": 0,
                "community_vouches": 18,
                "monthly_revenue": 1800,
                "months_in_business": 5
            },
            {
                "name": "KeralaSpices", 
                "owner": "SpiceRoute", 
                "desc": "Authentic homemade spice blends from Kerala.",
                "points": 1200, 
                "goal": 1000,
                "image": "spices.jpg",
                "funded_by_investors": False,
                "investor_funding": 0,
                "community_vouches": 65,
                "monthly_revenue": 3200,
                "months_in_business": 12
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
                
                # Show if investor-funded
                if camp.get("funded_by_investors"):
                    st.success(f"💼 Investor Funded: ${camp.get('investor_funding', 0)}")
                
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
                                # Track community vouches
                                if "community_vouches" not in st.session_state.campaigns[i]:
                                    st.session_state.campaigns[i]["community_vouches"] = 0
                                st.session_state.campaigns[i]["community_vouches"] += 1
                                st.rerun()
                            else:
                                st.error("Not enough points!")
                
                # COMMENTS SECTION (Simulated)
                with st.expander("💬 Comments"):
                    st.text_input("Add a comment...", key=f"com_{i}")
                    st.write("*Very cool project!* - @mike")

# ==========================================
# PAGE: INVESTOR PORTAL (NEW!)
# ==========================================
elif st.session_state.page == "Investor Portal":
    
    # --- HEADER ---
    st.header("🏦 Investor Dashboard")
    st.caption("Deploy capital to vetted small businesses and earn returns while building community impact.")
    
    st.divider()
    
    # --- PORTFOLIO OVERVIEW ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Liquidity Pool", f"${st.session_state.investor_pool:,.0f}", delta="Available")
    
    with col2:
        total_invested = sum([inv['amount'] for inv in st.session_state.investor_investments])
        st.metric("📊 Total Deployed", f"${total_invested:,.0f}")
    
    with col3:
        active_investments = len(st.session_state.investor_investments)
        st.metric("🎯 Active Investments", active_investments)
    
    with col4:
        # Simulated returns (5% monthly return on deployed capital)
        expected_returns = total_invested * 0.05
        st.metric("💵 Expected Monthly Returns", f"${expected_returns:,.0f}", delta="5% ROI")
    
    st.divider()
    
    # --- LIQUIDITY POOL MANAGEMENT ---
    with st.expander("💳 Manage Liquidity Pool"):
        st.subheader("Add or Withdraw Capital")
        
        col_add, col_withdraw = st.columns(2)
        
        with col_add:
            st.markdown("#### Add Funds")
            add_amount = st.number_input("Amount to Add ($)", min_value=0, value=1000, step=100, key="add_funds")
            if st.button("➕ Add to Pool"):
                st.session_state.investor_pool += add_amount
                st.success(f"Added ${add_amount:,.0f} to your liquidity pool!")
                st.rerun()
        
        with col_withdraw:
            st.markdown("#### Withdraw Funds")
            withdraw_amount = st.number_input("Amount to Withdraw ($)", min_value=0, value=500, step=100, key="withdraw_funds")
            if st.button("➖ Withdraw from Pool"):
                if withdraw_amount <= st.session_state.investor_pool:
                    st.session_state.investor_pool -= withdraw_amount
                    st.success(f"Withdrew ${withdraw_amount:,.0f} from your pool!")
                    st.rerun()
                else:
                    st.error("Insufficient funds in liquidity pool!")
    
    st.divider()
    
    # --- INVESTMENT OPPORTUNITIES ---
    st.subheader("🔍 Investment-Ready Businesses")
    st.caption("Businesses that have reached 1000+ Trust Points and meet funding criteria")
    
    # Filter campaigns that are eligible for investor funding
    if "campaigns" not in st.session_state:
        st.info("No businesses available yet. Check the Community Marketplace!")
    else:
        eligible_businesses = [
            camp for camp in st.session_state.campaigns 
            if camp["points"] >= 1000  # Must have reached trust point goal
        ]
        
        if not eligible_businesses:
            st.info("No businesses have reached the 1000 Trust Point threshold yet.")
        else:
            # Display as cards
            for idx, business in enumerate(eligible_businesses):
                with st.container(border=True):
                    col_left, col_right = st.columns([2, 1])
                    
                    with col_left:
                        # Business Details
                        st.subheader(f"🌟 {business['name']}")
                        st.caption(f"Owner: {business['owner']}")
                        st.write(business['desc'])
                        
                        # Key Metrics
                        met1, met2, met3 = st.columns(3)
                        met1.metric("Trust Points", business['points'])
                        met2.metric("Community Vouches", business.get('community_vouches', 0))
                        met3.metric("Monthly Revenue", f"${business.get('monthly_revenue', 0):,.0f}")
                        
                        # Additional Info
                        st.caption(f"⏰ In Business: {business.get('months_in_business', 0)} months")
                        
                        # Funding Status
                        if business.get('funded_by_investors'):
                            st.success(f"✅ Already Funded: ${business.get('investor_funding', 0):,.0f}")
                        else:
                            st.info("⏳ Awaiting investor funding")
                    
                    with col_right:
                        # Investment Image
                        if business.get("image"):
                            st.image(business["image"], use_container_width=True)
                        
                        # Investment Action
                        if not business.get('funded_by_investors'):
                            st.markdown("#### Fund This Business")
                            
                            # Investment amount slider
                            invest_amount = st.number_input(
                                "Investment Amount ($)", 
                                min_value=500, 
                                max_value=10000, 
                                value=2000, 
                                step=500,
                                key=f"invest_amount_{idx}"
                            )
                            
                            # Expected ROI calculator
                            expected_roi = invest_amount * 0.05
                            st.caption(f"💡 Expected Monthly ROI: ${expected_roi:,.0f} (5%)")
                            
                            # Investment button
                            if st.button(f"💼 Invest ${invest_amount:,.0f}", key=f"invest_btn_{idx}", type="primary"):
                                if invest_amount <= st.session_state.investor_pool:
                                    # Deduct from pool
                                    st.session_state.investor_pool -= invest_amount
                                    
                                    # Mark business as funded
                                    business_idx = st.session_state.campaigns.index(business)
                                    st.session_state.campaigns[business_idx]['funded_by_investors'] = True
                                    st.session_state.campaigns[business_idx]['investor_funding'] = invest_amount
                                    
                                    # Add to investment portfolio
                                    st.session_state.investor_investments.append({
                                        'business': business['name'],
                                        'amount': invest_amount,
                                        'date': pd.Timestamp.now().strftime("%Y-%m-%d"),
                                        'status': 'Active'
                                    })
                                    
                                    st.success(f"🎉 Successfully invested ${invest_amount:,.0f} in {business['name']}!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("Insufficient liquidity! Add more funds to your pool.")
                        else:
                            st.success("✅ Funded")
                            st.caption("This business has received funding")
    
    st.divider()
    
    # --- MY INVESTMENTS ---
    st.subheader("📋 My Investment Portfolio")
    
    if not st.session_state.investor_investments:
        st.info("You haven't made any investments yet. Browse opportunities above!")
    else:
        # Create DataFrame
        inv_df = pd.DataFrame(st.session_state.investor_investments)
        
        # Display as table
        st.dataframe(
            inv_df,
            use_container_width=True,
            column_config={
                "business": "Business Name",
                "amount": st.column_config.NumberColumn("Investment", format="$%d"),
                "date": "Investment Date",
                "status": "Status"
            }
        )
        
        # Summary metrics
        col1, col2 = st.columns(2)
        with col1:
            total_inv = inv_df['amount'].sum()
            st.metric("Total Invested", f"${total_inv:,.0f}")
        with col2:
            monthly_return = total_inv * 0.05
            st.metric("Expected Monthly Return", f"${monthly_return:,.0f}")

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