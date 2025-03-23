import streamlit as st
import google.generativeai as genai
import csv

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCftOsOCU-zMFlbg4Fy7k3VqElIKQZYcRY")

# Function to query Gemini AI for training timeline
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate a dynamic training timeline based on scenario and department
def generate_training_timeline(scenario, department, avg_age, training_duration, frequency, start_date, training_focus):
    # Construct a detailed prompt for Gemini AI
    prompt = f"""
    Given the following parameters, generate a detailed employee training timeline:
    - Scenario: {scenario}
    - Department: {department}
    - Average Age of Employees: {avg_age}
    - Training Duration: {training_duration} months
    - Frequency of Training Sessions: {frequency}
    - Training Focus: {training_focus}
    - Training Start Date: {start_date}
    
    Create a month-by-month breakdown of the training plan, including topics, expected outcomes, and milestones. Ensure that the training is engaging and practical.
    """
    
    # Query Gemini AI for the training timeline
    timeline = ask_gemini(prompt)
    return timeline

# Function to get training focus from Gemini AI based on scenario and department
def get_training_focus_from_ai(scenario, department):
    # Construct the prompt for Gemini AI to generate training focus
    prompt = f"Given the scenario '{scenario}' and department '{department}', suggest the key skills, topics, and areas of focus for employee training. Output the focus as a single string."
    
    # Call to Google Gemini AI to infer the training focus
    response = ask_gemini(prompt)
    
    # Extract the training focus from the response
    training_focus = response.strip()  # Remove leading/trailing spaces
    return training_focus

# Function to append data to CSV
def file_append(data1, data2, data3):    
    with open('training_timeline.csv', 'a+') as file:  # Append & read mode
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Wrap all fields in quotes
        writer.writerow([data1, data2, data3])

# Streamlit UI
st.set_page_config(
    page_title="TrainingTimeline", 
    layout="wide",
)

st.title("📅 Employee Training Timeline Generator")
st.markdown("Design a detailed training timeline for employees to learn new skills and topics.")

# User Inputs
scenario = st.text_input("Describe the Scenario (e.g., Leadership Development, Compliance Training, Soft Skills):")
department = st.text_input("Department (e.g., Marketing, Engineering, HR):")
avg_age = st.number_input("Average Age of Employees:", min_value=18, max_value=100, step=1)
training_duration = st.number_input("Training Duration (in months):", min_value=1, max_value=12, step=1)
frequency = st.selectbox("Frequency of Training Sessions:", ["Weekly", "Bi-Weekly", "Monthly"])
start_date = st.date_input("Training Start Date:")

if "response" not in st.session_state:
    st.session_state["response"] = ""
if "title" not in st.session_state:
    st.session_state["title"] = ""

# Generate Response Button
if st.button("Generate Training Timeline"):
    if scenario and department and training_duration and start_date:
        # Dynamically infer the training focus using Gemini AI
        training_focus = get_training_focus_from_ai(scenario, department)
        
        # Generate the detailed training timeline
        st.session_state["response"] = generate_training_timeline(
            scenario, 
            department, 
            avg_age, 
            training_duration, 
            frequency, 
            start_date, 
            training_focus
        )
        
        st.session_state["title"] = f"Training Timeline for {department}"

        st.subheader("📝 Generated Training Timeline:", divider="blue")
        st.write(st.session_state["response"])
    else:
        st.warning("Please fill in all fields before generating.")

if st.session_state["response"] != "" and st.session_state["title"] != "":
    if st.button("Push Timeline"):
        with open('pages/training_timeline.csv', 'r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader)

        file_append(row_count, st.session_state["title"], st.session_state["response"])
        st.success("Training timeline pushed to CSV ✅")
