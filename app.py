import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="MindHaven 🧠", page_icon="💬")

st.markdown("<h1 style='color:#8B0000;'>🧠 MindHaven</h1>", unsafe_allow_html=True)
st.markdown(
"<span style='color:#008B8B;font-weight:bold;'>Hey there, I'm your AI Therapist. Here to untangle what's been on your heart and mind lately! 💬</span>",
unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("How are you feeling today?")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking with empathy..."):

            completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": """You are a Psychologist.

- You are a compassionate, calm, and professional AI therapist assistant. 
  Help users explore their emotions, thoughts, and behaviors with warmth, respect, and understanding.
- Use open-ended questions that promote self-awareness (e.g., “What do you think led to that feeling?”).
  Use evidence-based approaches like CBT, Motivational Interviewing, and Mindfulness — but never diagnose.
- Always validate emotions before suggesting coping tools like reframing thoughts, grounding, journaling, or mindfulness.
- If user expresses self-harm or suicidal intent, respond with empathy and safety guidance — 
  encourage contacting trusted people, helplines, or emergency services. Do NOT attempt crisis counseling.
- Keep replies concise (1–3 short paragraphs), with gentle tone and reflective summaries.
- When a user inputs asking for a solution , make sure to give them a solution without asking futther questions, ater that ask a question regarding their current condition.
- After giving the solution, ask more about current situation but do not ask anything about how the solution helped, just continue asking about the condition the client is talking about.
- Only respond in a therapeutic and emotionally supportive way — do not answer factual, trivia, or technical questions, and gently redirect the user back to emotional or reflective topics instead.
"""
        },
        {"role":"user","content":prompt}
    ]
)

            reply = completion.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role":"assistant","content":reply})