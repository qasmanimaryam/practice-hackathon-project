
import os
import time
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Study Buddy")

st.title("AI Study Buddy 📚")
st.write("Ask AI to explain any topic in simple language!")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=api_key)

topic = st.text_input("Enter your study topic")

if st.button("Explain Topic"):
    if topic.strip():
        with st.spinner("AI is preparing your answer..."):
            response = None

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=(
                            "Explain this topic in simple language "
                            "with one clear example: " + topic
                        )
                    )
                    break

                except Exception as error:
                    if "503" in str(error) and attempt < 2:
                        time.sleep(2 ** (attempt + 1))
                    else:
                        st.error(
                            "AI request failed. Check model access, "
                            "API key, or try again later."
                        )
                        st.caption(str(error))
                        break

            if response is not None:
                st.subheader("Your Explanation")
                st.write(response.text)

    else:
        st.warning("Please enter a topic first.")
