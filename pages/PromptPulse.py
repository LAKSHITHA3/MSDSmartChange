import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from collections import Counter
import csv

st.set_page_config(
    page_title = "PromptPulse", 
    layout = "wide",
)

st.sidebar.page_link(page = "main.py", label = "📍 Main page")

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCftOsOCU-zMFlbg4Fy7k3VqElIKQZYcRY")

# Function to generate communication using Gemini AI
def generate_custom_communication(template_type, change_type, audience, tone, scope):
    prompts = {
        "Announcement": f"Draft an official announcement about {change_type}. "
                        f"Scope: {scope}. Audience: {audience}. Maintain a {tone} tone. "
                        "Ensure clarity on reasons, goals, and impact. "
                        "Use a structured approach referencing change management frameworks (e.g., Kotter’s 8-Step Model, ADKAR, or Lewin’s Change Model).",
        
        "Progress Update": f"Provide a structured progress update on {change_type}. "
                           f"Scope: {scope}. Audience: {audience}. Maintain a {tone} tone. "
                           "Ensure the update includes key milestones, impact, and next steps. "
                           "Follow a change management framework where applicable.",

        "Training Invitation": f"Draft a training invitation for {change_type}. "
                               f"Scope: {scope}. Audience: {audience}. Maintain a {tone} tone. "
                               "Explain why this training is necessary, the goals of the training, and the expected benefits.",

        "Feedback Request": f"Create a feedback request regarding {change_type}. "
                            f"Scope: {scope}. Audience: {audience}. Maintain a {tone} tone. "
                            "Ensure the message clearly communicates the reason for seeking feedback, "
                            "how the feedback will be used, and its impact on change implementation."
    }

    prompt = prompts.get(template_type, "Invalid template type!")
    if prompt == "Invalid template type!":
        return prompt

    # Call Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")  # Use "gemini-1.5-pro" if available
    response = model.generate_content(prompt)

    return response.text if response else "Error generating response."

def file_append(data1, data2, data3):    
    with open('prompts.csv', 'a+') as file:  # Append & read mode
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Wrap all fields in quotes
        writer.writerow([data1, data2, data3])

# Streamlit UI
st.title("💬 PromptPulse")
st.markdown("Generate custom announcements, progress updates, training invitations, and feedback requests using industry-standard frameworks.")

# User Inputs
template_type = st.selectbox("Select Template Type:", ["Announcement", "Progress Update", "Training Invitation", "Feedback Request"])
change_type = st.text_input("Describe the Change (e.g., Cloud Migration, New Policy):")
scope = st.text_input("Scope of Change (e.g., Organizational, Project-Based, People-Focused):")
audience = st.text_input("Which Department is involved? (e.g., Cybersecurity & Rish Management, AI & ML, Data & Analysis):")
tone = st.selectbox("Select Tone:", ["Formal", "Casual", "Motivational", "Informative"])

if "response" not in st.session_state:
    st.session_state["response"] = ""
if "title" not in st.session_state:
    st.session_state["title"] = ""

# Generate Response Button
if st.button("Generate"):
    if change_type and audience:
        st.session_state["response"] = generate_custom_communication(template_type, change_type, audience, tone, scope)
        st.session_state["title"] = st.session_state["response"].partition('\n')[0]

        st.subheader("📝 Generated Communication:", divider="blue")
        st.write(st.session_state["response"])
    else:
        st.warning("Please fill in all fields before generating.")

if st.session_state["response"] != "" and st.session_state["title"] != "":
    if st.button("Push Prompt"):
        with open('pages/prompts.csv', 'r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader)

        file_append(row_count, st.session_state["title"], st.session_state["response"])
        st.success("Prompt pushed to CSV ✅")



