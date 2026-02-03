import streamlit as st
import google.generativeai as genai

# 1. Page configuration
st.set_page_config(page_title="Evaluation Assistant", layout="centered")
st.title("🤖 Supplier Support Chatbot")

# 2. API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Please configure 'GOOGLE_API_KEY' in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Model (cheap + fast)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 4. SYSTEM RULES (VERY IMPORTANT)
SYSTEM_PROMPT = """
You are a compliance support chatbot for suppliers.

STRICT RULES:
- ONLY answer using the information in "AVAILABLE INFORMATION".
- DO NOT explain policies.
- DO NOT add context, advice, or assumptions.
- DO NOT invent information.
- Answer in a maximum of 2 short sentences.
- If the answer is not explicitly in the information, reply exactly:
  "This information is not available. Please follow the official instructions."
"""

# 5. AVAILABLE INFORMATION (your real source)
BASE_DATOS = """
AVAILABLE INFORMATION:

Passport:
Documents are NOT retained.
Evidence: No-retention policy.

Payments:
No deposits are required.
Evidence: Hiring policy.

Penalties:
There are no financial penalties.
Evidence: Internal regulations.

Resignation:
No restrictions apply.
Evidence: Termination procedure.

Document access:
Employees always have free access to their documents.
Evidence: HR policy.
"""

# 6. Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        final_prompt = f"""
{SYSTEM_PROMPT}

{BASE_DATOS}

User question:
{prompt}
"""

        response = model.generate_content(final_prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

    except Exception as e:
        st.error(f"Error: {e}")

