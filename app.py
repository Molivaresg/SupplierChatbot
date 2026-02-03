import streamlit as st
import google.generativeai as genai

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Supplier Evaluation Assistant",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# HIDE STREAMLIT & GITHUB BRANDING
# --------------------------------------------------
hide_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("Supplier Evaluation Assistant")
st.caption(
    "👋 Welcome! I can help you understand what document or evidence you need to upload "
    "for the supplier evaluation form."
)

st.divider()

# --------------------------------------------------
# API CONFIG
# --------------------------------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY is missing. Please contact the administrator.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ✅ CORRECT MODEL NAME
model = genai.GenerativeModel("gemini-flash-latest")

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = """
You are a Supplier Evaluation Assistant.

STRICT RULES:
- Always respond in the SAME language used by the user.
- Use ONLY the information provided in the Knowledge Base.
- Explain the required document in simple and clear terms if needed.
- Do NOT add legal context, policies, or assumptions.
- Do NOT invent documents, requirements, or explanations.
- If the answer is not explicitly in the Knowledge Base, reply exactly:
"This information is not available. Please follow the official instructions."
"""

# --------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------
KNOWLEDGE_BASE = """
1. Passport retention:
Question: Do you retain passports or migrant documents of foreign employees?
Evidence: Signed declaration of NO document retention policy (PDF).
Example link: https://vegaguerrero.com/migratorio/as-a-foreigner-in-mexico-should-i-always-carry-my-passport-or-identification-document-with-me/?lang=en

2. Recruitment payments:
Evidence: Recruitment policy prohibiting fees or deposits (PDF).

3. Economic penalties:
Evidence: Internal regulations prohibiting financial sanctions (PDF).

4. Voluntary resignation:
Evidence: Voluntary resignation procedure and acknowledgement receipt (PDF).

5. Access to documents:
Evidence: HR policy on voluntary custody and free access (PDF).

6. Exit during breaks:
Evidence: Access and exit policy with schedules and permissions (PDF).

7. Working hours:
Evidence: Shift schedule and attendance records (PDF).

8. Overtime:
Evidence: Payroll receipts showing overtime payment and overtime policy (PDF).

9. Non-discrimination:
Evidence: Equality and non-discrimination policy (PDF).

10. Written contracts:
Evidence: Employment contract template (PDF).

11. Job conditions:
Evidence: Job offer letter or employment offer format (PDF).

12. Social security:
Evidence: Social security registration notices (PDF).

13. Health and safety:
Evidence: Annual occupational health and safety program (PDF).

14. Accidents:
Evidence: Incident reporting procedure and accident log (PDF).

15. Migration costs:
Evidence: Migration management and cost responsibility policy (PDF).

16. Foreign workers information:
Evidence: Guide or manual for foreign employees (PDF).

17. Freedom of association:
Evidence: Freedom of association policy (PDF).

18. Complaints channel:
Evidence: Complaints procedure and anonymous reporting channel (PDF).

19. Supplier standards:
Evidence: Signed supplier code of conduct (PDF).

20. Audits:
Evidence: Recent labor audit report (PDF).
"""

# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 👋 How can I help you with the supplier evaluation form?"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Format conversation history as text
    history_text = ""
    for m in st.session_state.messages[-6:]:
        history_text += f"{m['role'].upper()}: {m['content']}\n"

    final_prompt = f"""
{SYSTEM_PROMPT}

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

CONVERSATION:
{history_text}

USER QUESTION:
{user_input}
"""

    try:
        response = model.generate_content(final_prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

    except Exception:
        st.error("An unexpected error occurred. Please try again later.")

