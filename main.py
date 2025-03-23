import streamlit as st
import streamlit_authenticator as stauth
from yaml import load, SafeLoader, dump

# Load configuration
with open('account.yaml') as file:
    config = load(file, Loader=SafeLoader)

st.set_page_config(
    page_title="MSDSmartChange", 
    page_icon=None,  
    layout="wide",  
    initial_sidebar_state="collapsed", 
    menu_items = None
)

# Set up authentication
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    )

# Centered layout
left_col, center_col, right_col = st.columns([1, 2, 1])
with center_col:
    
    try:
        authenticator.login(location='main', max_concurrent_users=20)
    except Exception as e:
        st.error(f"Login error: {e}")
    if st.session_state.get('authentication_status') != True:
        with st.expander("New User? Register"):
            try:
                user_details = authenticator.register_user(location='main')
                if user_details[1] is not None:
                    config['credentials']['usernames'][user_details[1]]['role'] = "Employee"
                    with open('account.yaml', 'w') as file:
                        dump(config, file)
                    st.success('User registered successfully')
                    st.rerun()
            except Exception as e:
                st.error(f"Registration failed: {e}")
         
        # Login Form
    
    
if st.session_state['authentication_status']:
    user_info = config['credentials']['usernames'][st.session_state['username']]
    st.header(f"Welcome, {st.session_state['name']}",divider="blue")

        # Sidebar Navigation
    st.sidebar.subheader("Tools & Features")
    st.sidebar.page_link(page="pages/AI Assistant.py", label="➤➤➤ AI Assistant")
    st.sidebar.page_link(page="pages/Chatbot.py", label="➤➤➤ Chatbot")
    st.sidebar.page_link(page="pages/PromptPulse.py", label="➤➤➤ PromptPulse")
    st.sidebar.page_link(page="pages/Training Timeline.py", label="➤➤➤ 📅 Training Timeline Generator")
    st.image('cool_change.jpg', width=800)
    st.markdown("""
    Change is hard—let’s face it. Studies show that 70% of change initiatives fail, and the reasons are clear: poor communication, lack of employee engagement, and outdated strategies. Employees feel disconnected, managers struggle with limited insights, and organizations waste time and resources.

    But what if there was a way to make change management smarter, faster, and more effective? That’s exactly what we’ve built.

    ## Why We Built This Portal
    - **Empower Change Management:** Streamline and optimize your change management efforts using AI-powered insights.
    - **Enhance Communication:** Ensure clear, effective messaging tailored to every employee.
    - **Drive Engagement:** Gather real-time feedback and continuously refine strategies.
    - **Support Data-Driven Decisions:** Leverage industry-specific insights and benchmarks.

    ## How It Works

    ### 1. **Research & Strategy Development**
    - Access 10+ change management frameworks like ADKAR, Kotter’s 8-Step Model, and McKinsey 7S.
    - Generate industry-specific case studies and tailored recommendations.
    - Stay ahead of the curve with the latest market trends and news using Google Gemini AI APIs.

    ### 2. **Real-Time Feedback & Sentiment Analysis**
    - Collect employee feedback on change initiatives using AI-powered sentiment analysis.
    - Track employee sentiment over time and identify trends based on demographics like age, department, and role.
    - Continuously refine communication strategies based on feedback insights.

    ### 3. **Dynamic Communication Tools**
    - Create and automate tailored announcements, progress updates, and training invitations using Prompt Pulse.
    - Use NLU (Natural Language Understanding) for human-like interactions.
    - Support multimodal inputs, including PDFs, text, and audio.

    ### 4. **Employee Training & Timeline Generator**
    - Generate customized training timelines based on manager inputs.
    - Ensure employees are prepared for upcoming changes with personalized learning paths.

    ### 5. **Context-Aware Insights**
    - Track conversation history for better understanding and continuity.
    - Access real-time news and trends to provide relevant responses.
    - In the future, store conversation data for deeper analysis and enhanced predictions.

    ## What You Gain
    - **Improved Communication:** Ensure alignment across all teams with tailored messaging.
    - **Higher Engagement:** Create a feedback loop that values employee input.
    - **Informed Decisions:** Leverage data-driven insights to make strategic choices.
    - **Continuous Improvement:** Adapt and optimize strategies based on ongoing analysis.
    - **Scalable Solution:** Easily expand to new departments and regions with AI-driven insights.

    ### 📍 Navigation Guide  
    Please refer to the **sidebar on the left** to access different pages.  

    - ##### **➤➤➤ AI Assistant**                     
    - ##### **➤➤➤ Chatbot**
    - ##### **➤➤➤ PromptPulse** 
    - ##### **➤➤➤ 📅 Training Timeline Generator**
    """)

    authenticator.logout('Logout', 'sidebar')
    
    
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')