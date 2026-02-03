import streamlit as st
import google.generativeai as genai

# --------------------------------------------------
# PAGE CONFIG & HIDE STREAMLIT BRANDING
# --------------------------------------------------
st.set_page_config(
    page_title="Supplier Evaluation Assistant",
    page_icon="🤖",
    layout="centered"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div style="text-align:center">
<h1>Supplier Evaluation Assistant</h1>
<p style="font-size:16px;color:#6c757d;">
I help you answer questions related to the supplier evaluation form and required documents.
</p>
</div>
""", unsafe_allow_html=True)

st.info(
    "👋 Welcome! Please tell me which question you have about the supplier evaluation form. "
    "I will guide you on what information or document you need to upload."
)

# --------------------------------------------------
# API CONFIG
# --------------------------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ GOOGLE_API_KEY is missing in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash-latest")

# --------------------------------------------------
# SYSTEM PROMPT (VERY IMPORTANT)
# --------------------------------------------------
SYSTEM_PROMPT = """
You are a Supplier Evaluation Assistant.

RULES:
- Use ONLY the information in the knowledge base.
- DO NOT invent or assume information.
- Answer clearly and briefly.
- Respond in the SAME language as the user.
- If the user asks for an example and it exists, explain it briefly.
- If the information is not in the knowledge base, respond exactly with:
  "This information is not available. Please follow the official instructions."
- Keep a professional and helpful tone.
"""

# --------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------
KNOWLEDGE_BASE = """
1. Passport retention:
Question: Does your company retain passports or migrant employee documents?
Required document: Signed declaration of NO document retention policy.
Example: https://vegaguerrero.com/wp-content/uploads/2023/03/BLOG-VGA.png

2. Deposits or fees:
Required document: Hiring policy that prohibits deposits or fees (PDF).

3. Internal fines:
Required document: Internal regulation prohibiting economic penalties (PDF).

4. Free resignation:
Required document: Voluntary resignation procedure (PDF).

5. Access to documents:
Required document: HR policy on free access to personal documents (PDF).

6. Facility exits:
Required document: Access and exit policy during breaks (PDF).

7. Working hours:
Required document: Shift schedule and attendance record example (PDF).

8. Overtime:
Required document: Payroll receipts showing paid overtime and overtime policy (PDF).

9. Non-discrimination:
Required document: Equality and non-discrimination policy (PDF).

10. Written contracts:
Required document: Sample employment contract (PDF).

11. Clear conditions:
Required document: Job offer or offer letter (PDF).

12. Social security:
Required document: Social security registration evidence (PDF).

13. Health & safety:
Required document: Annual occupational health and safety program (PDF).

14. Accidents:
Required document: Accident reporting procedure and log (PDF).

15. Migration costs:
Required document: Migration management policy (PDF).

16. Foreign employees:
Required document: Guide for foreign employees (PDF).

17. Freedom of association:
Required document: Freedom of association policy (PDF).

18. Complaints channel:
Required document: Whistleblowing or complaints procedure (PDF).

19. Supplier standards:
Required document: Supplier code of conduct (PDF).

20. Audits:
Required document: Recent labor audit report (PDF).
"""

# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        final_prompt = f"""
{SYSTEM_PROMPT}

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

User question:
{user_input}
"""
        response = model.generate_content(final_prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

    except Exception as e:
        st.error(f"Error: {e}")

    )

