# app.py
# pip install streamlit openai-agents python-dotenv

import streamlit as st
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("❌ GEMINI_API_KEY is not set. Please define it in your .env file.")
    st.stop()

# --- External Gemini API Client ---
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# --- Therapy Agent ---
therapy_agent = Agent(
    name='Therapy Agent',
    instructions="""You are a Psychologist.

- You are a compassionate, calm, and professional AI therapist assistant. 
  Help users explore their emotions, thoughts, and behaviors with warmth, respect, and understanding.
- Use open-ended questions that promote self-awareness (e.g., “What do you think led to that feeling?”).
  Use evidence-based approaches like CBT, Motivational Interviewing, and Mindfulness — but never diagnose.
- Always validate emotions before suggesting coping tools like reframing thoughts, grounding, journaling, or mindfulness.
- If user expresses self-harm or suicidal intent, respond with empathy and safety guidance — 
  encourage contacting trusted people, helplines, or emergency services. Do NOT attempt crisis counseling.
- Keep replies concise (1–3 short paragraphs), with gentle tone and reflective summaries.
- If user askes for a solution to their problems, make sure to give a solution along with the questions.
"""
)

# --- Streamlit UI ---
st.set_page_config(page_title="Therapy AI Agent 🧠", page_icon="💬", layout="centered")

st.markdown("<h1 style='color:#8B0000;'>🧠 Your AI Therapist</h1>", unsafe_allow_html=True)
st.markdown("<span style='color:#008B8B; font-weight:bold;'>Hi there! I'm your AI Therapist. Let's talk about what's been on your mind lately 💬</span>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Async Runner ---
async def get_ai_response(prompt):
    response = await Runner.run(
        therapy_agent,
        input=prompt,
        run_config=config
    )
    return response.final_output


# --- Chat input handling ---
if prompt := st.chat_input("How are you feeling?"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking with empathy..."):
            reply = asyncio.run(get_ai_response(prompt))
            st.markdown(reply)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
