import streamlit as st
import google.generativeai as genai

# Set page configuration
st.set_page_config(
    page_title="Change Management AI Assistant", 
    layout="wide"
)

# Sidebar link to the main page
st.sidebar.page_link(page="main.py", label="📍 Main page")


# Configure Gemini API Key
genai.configure(api_key="AIzaSyCftOsOCU-zMFlbg4Fy7k3VqElIKQZYcRY")

# Function to query Gemini AI
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI

st.title("📈 Change Management AI Assistant")
st.markdown("### Powered by Google Gemini AI")

# **Radio Button for Navigation**
section = st.radio("Select a Section", [
    "Industry Trends", 
    "'What If' Scenario Analysis", 
    "Technology & Market Trends", 
    "Industry Benchmarks", 
    "Case Studies"
])

# **Industry Trends Section**
if section == "Industry Trends":
    st.header("🌍 Industry Trends in Change Management")
    if st.button("Get Latest Trends"):
        prompt = "What are the latest industry trends in change management?"
        trends = ask_gemini(prompt)
        st.write(trends)

# 'What If' Scenario Analysis Section
elif section == "'What If' Scenario Analysis":
    st.header("🔄 'What If' Scenario Analysis")
    col1, col2 = st.columns(2)
    with col1:
        model_1 = st.selectbox("Select First Change Model", [
            "ADKAR Model",
            "Kotter’s 8-Step Change Model",
            "Lewin’s Change Management Model",
            "McKinsey 7-S Framework",
            "Bridges’ Transition Model",
            "Nudge Theory",
            "Kübler-Ross Change Curve",
            "Satir Change Model",
            "Deming’s PDCA Cycle",
            "Burke-Litwin Model of Organizational Change"
        ], key="model1")
    with col2:
        model_2 = st.selectbox("Select Second Change Model", [
            "ADKAR Model",
            "Kotter’s 8-Step Change Model",
            "Lewin’s Change Management Model",
            "McKinsey 7-S Framework",
            "Bridges’ Transition Model",
            "Nudge Theory",
            "Kübler-Ross Change Curve",
            "Satir Change Model",
            "Deming’s PDCA Cycle",
            "Burke-Litwin Model of Organizational Change"
        ], key="model2")

    if st.button("Compare Models"):
        prompt = f"Compare {model_1} with {model_2} in change management. Highlight advantages, disadvantages, and best use cases."
        comparison = ask_gemini(prompt)
        st.write(comparison)

# **Technology & Market Conditions Section**
elif section == "Technology & Market Trends":
    st.header("🚀 Technology & Market Trends Affecting Change")
    if st.button("Get Tech & Market Insights"):
        prompt = "How do current technology trends and market conditions impact change management?"
        tech_trends = ask_gemini(prompt)
        st.write(tech_trends)

# Industry Benchmarks Section
elif section == "Industry Benchmarks":
    st.header("📊 Industry Benchmarks for Change Adoption")
    if st.button("Show Benchmarks"):
        prompt = "What are key industry benchmarks and metrics for measuring change adoption?"
        benchmarks = ask_gemini(prompt)
        st.write(benchmarks)

# Case Studies Section
elif section == "Case Studies":
    st.header("📖 Change Management Case Studies")
    industry = st.selectbox("Select Industry", ["Healthcare", "Finance", "Technology", "Retail", "Education"])

    if st.button("Generate Case Studies"):
        prompt = f"Provide real-world case studies of change management in {industry}, considering cultural and geographic factors."
        case_studies = ask_gemini(prompt)
        st.write(case_studies)

st.markdown("📌 **Use this AI-powered assistant to explore change management insights!**")