import streamlit as st
import google.generativeai as genai

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Evaluation Assistant", layout="centered")
st.title("🤖 Supplier Evaluation Assistant")

st.markdown("""
👋 **Welcome!**

I can help you answer questions related to the supplier evaluation form  
and required documents. Please type your question below.
""")

# -----------------------------
# API KEY
# -----------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Please configure 'GOOGLE_API_KEY' in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# -----------------------------
# MODEL (cheap & fast)
# -----------------------------
model = genai.GenerativeModel("models/gemini-1.5-flash")

# -----------------------------
# SYSTEM PROMPT (STRICT)
# -----------------------------
SYSTEM_PROMPT = """
You are a supplier support chatbot.

RULES:
- Be polite and professional.
- ONLY use the information provided.
- DO NOT invent information.
- DO NOT add explanations or assumptions.
- Answer in a maximum of 2 short sentences.
- If the information is not available, reply exactly:
  "This information is not available. Please follow the official instructions."
"""

# -----------------------------
# KNOWLEDGE BASE (EDIT THIS)
# -----------------------------
FAQ = {
    "passport": "Upload a clear copy of the main passport page. Documents are not retained.",
    "payment": "No deposits are required.",
    "penalty": "There are no financial penalties.",
    "resignation": "There are no restrictions for resignation.",
    "document access": "Employees always have free access to their documents.",
    "working hours": "Working hours comply with the law and include breaks.",
    "overtime": "Overtime is voluntary and paid.",
    "discrimination": "There is a non-discrimination policy in place."
}

# -----------------------------
# SIMPLE INTENT DETECTION
# -----------------------------
def detect_topic(user_input):
    user_input = user_input.lower()
    for key in FAQ.keys():
        if key in user_input:
            return key
    return None

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    topic = detect_topic(prompt)

    # -----------------------------
    # RESPONSE LOGIC
    # -----------------------------
    if topic:
        context = FAQ[topic]

        final_prompt = f"""
{SYSTEM_PROMPT}

AVAILABLE INFORMATION:
{context}

User question:
{prompt}
"""

        try:
            response = model.generate_content(final_prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = "An error occurred. Please try again later."

    else:
        answer = "This information is not available. Please follow the official instructions."

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------------
# HELP FOOTER
# -----------------------------
st.caption(
    "Example topics: Passport, Payment, Penalty, Overtime, Document access"
)
