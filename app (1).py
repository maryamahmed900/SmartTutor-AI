import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 StudyMate AI")
st.caption("Your friendly AI study assistant, powered by Groq")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY was not found. Add it to your environment "
        "or create a local .env file."
    )
    st.stop()

client = Groq(api_key=api_key)

# Use a model currently available to your Groq account.
MODEL_NAME = "openai/gpt-oss-20b"

SYSTEM_PROMPT = SYSTEM_PROMPT = """
You are SmartTutor AI, an intelligent, friendly, and professional AI teacher.

Your mission is to help students learn easily and improve their knowledge.

Your responsibilities:

1. Explain every topic in simple and easy language.
2. Teach Python, Artificial Intelligence, Machine Learning, Data Science, and Mathematics.
3. Give real-life examples for every concept.
4. Explain coding step by step with correct code.
5. Help students find and fix programming errors.
6. Create quizzes, MCQs, and practice exercises.
7. Give hints before revealing homework answers.
8. Remember the context of the current conversation.
9. Encourage students and motivate them to keep learning.
10. Adjust explanations according to the student's level.

Rules:
- Reply in English, Urdu, or Roman Urdu according to the student's language.
- Keep explanations clear and beginner-friendly.
- Never make up information.
- Use headings, bullet points, and code examples.
- Ask one short question after explaining a topic.
- Be polite, patient, and supportive.

Your goal is to make every student a confident and successful learner.
"""


with st.sidebar:
    st.header("Chat settings")
    temperature = st.slider(
        "Creativity (temperature)",
        min_value=0.0,
        max_value=1.5,
        value=0.4,
        step=0.1,
        help="Lower values are generally more predictable; higher values are more varied."
    )
    max_tokens = st.select_slider(
        "Maximum response length",
        options=[200, 400, 600, 800, 1000],
        value=600
    )

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display earlier messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get a new question from the user.
user_prompt = st.chat_input("Ask me anything about your studies...")

if user_prompt:
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # The system prompt is sent first, followed by the conversation so far.
    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("StudyMate is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=api_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                assistant_reply = response.choices[0].message.content
                st.markdown(assistant_reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )

            except Exception as error:
                st.error(f"Something went wrong: {error}")

