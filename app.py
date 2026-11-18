
import time
import streamlit as st
from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# Page Settings
st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖")

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Prepare Conversation History
    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages
    )

    # Generate AI Response
    with st.chat_message("assistant"):

        with st.spinner("Gemini is thinking..."):

            answer = None

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=history
                    )

                    answer = response.text
                    break

                except errors.ServerError:
                    if attempt < 2:
                        time.sleep(2 ** (attempt + 1))

                except Exception as e:
                    st.error(f"Error: {e}")
                    break

            if answer:
                st.write(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            else:
                st.error(
                    "Gemini is currently busy. Please try again later."
                )

