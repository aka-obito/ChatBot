import streamlit as st
import google.generativeai as genai

# Configure the Google Gemini API
API_KEY = "AIzaSyBpVMSkWj2iBHtpyQHzsC9gsRYYRA8RuhE"
genai.configure(api_key=API_KEY)

# Function to generate schema using Google Gemini API
def generate_schema(prompt, context=""):
    try:
        # Combine the context with the current prompt
        combined_prompt = f"{context}\n{prompt}" if context else prompt
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(combined_prompt)
        return response.text  # Extract the generated text from the response
    except Exception as e:
        return f"Error: {str(e)}"

# App Title and Styling
st.markdown("""
    <style>
        .chat-container {
            background-color: #f7f7f7;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .chat-prompt {
            font-weight: bold;
            color: #007BFF;
        }
        .chat-response {
            color: #333;
            margin-top: 5px;
        }
        .submit-button {
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
        }
        .clear-button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("The AI CHATBOT 🤖")

# Initialize session state for managing the chat and buttons
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "context" not in st.session_state:
    st.session_state.context = ""

# Input Section
st.markdown("### Enter your query below:")
prompt = st.text_area("Ask me something:", placeholder="Type your question here...")

col1, col2 = st.columns([1, 1])

with col1:
    submit_clicked = st.button("Submit", help="Click to submit your query.", key="submit", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear Chat", help="Click to clear the chat history.", key="clear", use_container_width=True)

# Handle Clear Chat Button
if clear_clicked:
    st.session_state.conversation_history = []
    st.session_state.context = ""
    st.success("Chat history cleared!")

# Handle Submit Button
if submit_clicked and prompt.strip():
    with st.spinner("Generating your answer..."):
        # Generate schema using the accumulated context
        schema = generate_schema(prompt, st.session_state.context)

    # Add to chat history
    st.session_state.conversation_history.append({
        "prompt": prompt,
        "schema": schema
    })

    # Update context for future queries
    st.session_state.context += f"\nQ: {prompt}\nA: {schema}"

# Chat History Display
if st.session_state.conversation_history:
    st.markdown("### Chat History:")
    for i, entry in enumerate(st.session_state.conversation_history):
        st.markdown(f"""
            <div class="chat-container">
                <div class="chat-prompt">Q{i+1}: {entry['prompt']}</div>
                <div class="chat-response">A{i+1}: {entry['schema']}</div>
            </div>
        """, unsafe_allow_html=True)
