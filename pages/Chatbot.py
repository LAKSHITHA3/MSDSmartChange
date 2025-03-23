import streamlit as st
import google.generativeai as genai
from io import BytesIO
import fitz
import speech_recognition as sr


# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Chatbot",
    layout="wide",
)
st.sidebar.page_link(page="main.py", label="🏠 Main page")

# Configure Gemini API Key (ideally load this from environment variables)
genai.configure(api_key="AIzaSyCftOsOCU-zMFlbg4Fy7k3VqElIKQZYcRY")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {"preferences": "default"}
if "context" not in st.session_state:
    st.session_state.context = ""

# --------- Advanced Feature Functions ---------

def fetch_knowledge_graph_insights(user_input):
    insights = ""
    if "ADKAR" in user_input.upper():
        insights += "Insight: ADKAR focuses on Awareness, Desire, Knowledge, Ability, and Reinforcement. "
    if "LEWIN" in user_input.upper():
        insights += "Insight: Lewin's model comprises Unfreeze, Change, and Refreeze phases. "
    return insights.strip()

def simulate_scenario(user_input):
    if "what if" in user_input.lower():
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"Based on this query: '{user_input}', generate a detailed scenario analysis comparing the applicable change management models. Provide a tabular comparison very specific to the scenario" 
        )
        return response.text if response else "Error generating scenario comparison."
    return ""

def cross_modal_integration():
    uploaded_file = st.sidebar.file_uploader("Upload a supporting document or voice note", type=["txt", "wav", "mp3", "pdf"])
    content = ""
    if uploaded_file is not None:
        # If the file is a text file
        if uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
        
        # If the file is a PDF
        elif uploaded_file.type == "application/pdf":
            # Convert uploaded file to a file-like object using BytesIO
            file_bytes = uploaded_file.read()  # Read the uploaded file as bytes
            pdf_reader = fitz.open(stream=file_bytes, filetype="pdf")  # Pass the byte data to fitz
            for page in pdf_reader:
                content += page.get_text()
                             # Display the extracted content in Streamlit

        # If the file is an audio file (WAV or MP3)
        elif uploaded_file.type in ["audio/wav", "audio/mp3"]:
            # Use SpeechRecognition to convert speech to text
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(uploaded_file)

            with audio_file as source:
                audio_data = recognizer.record(source)
                try:
                    content = recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    content = "Sorry, I could not understand the audio."
                except sr.RequestError:
                    content = "Sorry, there was an issue with the speech recognition service."
                
    return content

def update_context(user_input, response_text):
    st.session_state.context += f"\nUser: {user_input}\nAI: {response_text}"

def get_company_insights(user_input):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"Provide detailed insights about the company mentioned in this query: '{user_input}'"
    )
    return response.text if response else "Error generating company insights."

def generate_ai_response(user_input, content):
    knowledge_insights = fetch_knowledge_graph_insights(user_input)
    scenario = simulate_scenario(user_input)

    # Check for company-specific context using Gemini AI
    additional_info = ""
    company_names = ["microsoft", "google", "msd", "DBS", "OCBC", "UOB", "Singtel", "CapitaLand", "Singapore Airlines", "Temasek", "Grab", "Shopee", "Wilmar", 
 "Keppel Corporation", "Mapletree", "StarHub", "SATS", "City Developments Limited", "ST Engineering", "ComfortDelGro", 
 "Razer", "BreadTalk", "Singapore Exchange", "SIA Engineering", "Yeo Hiap Seng", "Hong Leong Group", "Ezion Holdings", 
 "Fraser and Neave", "SP Group", "STATS ChipPAC", "Parkway Life REIT", "Tuan Sing Holdings", "Lendlease", "Far East Organization", 
 "Sembcorp Industries", "Dairy Farm International", "UOL Group", "Ascendas", "Singapore Technologies Aerospace", "Olam Group", 
 "SGX", "Singapore Technologies Engineering", "Banyan Tree", "Wilmar International", "SembMarine", "Ascott Residence Trust", 
 "Keppel Land", "Capitaland Mall Trust", "HDB", "Changi Airport Group", "Mapletree Industrial Trust", "Eureka", "Jardine Cycle & Carriage", 
 "Raffles Medical Group", "Healthway Medical", "M1", "Venture Corporation", "Singapore Power"]
    for company in company_names:
       if company in user_input.lower():
          additional_info += get_company_insights(user_input)

    # Add the additional_info to the prompt before generating the response
    prompt_with_context = f"Context: {st.session_state.context}\nUser: {user_input}\nScenario: {scenario}\nAdditional Info: {additional_info}\nAI:\nContent: {content}\n"

    # Generate the response from the model
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt_with_context)
    main_response = response.text if response else "Error generating response."

    # Build the full response by including the insights, sentiment, scenario, and cross-modal info
    full_response = "\n\n".join(
    part for part in [
        knowledge_insights,
        main_response,
        content
    ] if part
    )


    update_context(user_input, main_response)
    return full_response

# --------- Streamlit UI ---------

st.title("💬 Advanced AI Communication Chatbot")
st.markdown(
    "Interact with our AI assistant to generate announcements, updates, invitations, and feedback requests. "
    "This tool leverages advanced capabilities to decompose tasks, personalize responses, offer domain insights, "
    "analyze sentiment, simulate scenarios, and integrate cross-modal inputs.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")
content = cross_modal_integration()

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    bot_response = generate_ai_response(user_input, content)
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})