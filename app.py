import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Supplier Evaluation Assistant")

# Hide Streamlit & GitHub branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Supplier Evaluation Assistant")
st.write("👋 Welcome! I can help you understand what document or evidence you need to upload.")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

SYSTEM_PROMPT = """
You are a Supplier Evaluation Assistant.

Rules:
- Always respond in the SAME language used by the user.
- Use ONLY the information provided in the Knowledge Base.
- You may rephrase or explain the requirement in simple words if the user does not understand.
- Do NOT add new policies, legal context, or assumptions.
- Do NOT invent documents or requirements.
- Focus on explaining what document or evidence must be uploaded.
- If the information is not explicitly available in the Knowledge Base, reply exactly:
  "This information is not available. Please follow the official instructions."
"""

KNOWLEDGE_BASE = """
1. Passport retention:
Question: Do you retain passports or migrant documents of foreign employees?
Evidence: Signed declaration of NO document retention policy (PDF).

2. Recruitment payments:
Question: Do you request deposits or payments to start or keep a job?
Evidence: Recruitment policy prohibiting fees or deposits (PDF).

3. Economic penalties:
Question: Are there internal fines or economic penalties for workers?
Evidence: Internal regulations prohibiting financial sanctions (PDF).

4. Voluntary resignation:
Question: How do you guarantee employees can resign freely?
Evidence: Voluntary resignation procedure and acknowledgement receipt (PDF).

5. Access to documents:
Question: Do employees have free access to their personal documents?
Evidence: HR policy on voluntary custody and free access (PDF).

6. Exit during breaks:
Question: Can employees leave the facilities during breaks or outside working hours?
Evidence: Access and exit policy with schedules and permissions (PDF).

7. Working hours:
Question: Do working hours comply with labor laws and mandatory rest?
Evidence: Shift schedule and attendance records (PDF).

8. Overtime:
Question: Are employees required to work overtime?
Evidence: Payroll receipts showing overtime payment and overtime policy (PDF).

9. Non-discrimination:
Question: Is recruitment free from discrimination?
Evidence: Equality and non-discrimination policy (PDF).

10. Written contracts:
Question: Do employees receive a written contract before starting work?
Evidence: Employment contract template (PDF).

11. Job conditions:
Question: Are salary, schedule, duties and benefits explained before hiring?
Evidence: Job offer letter or employment offer format (PDF).

12. Social security:
Question: Are employees registered with social security?
Evidence: Social security registration notices (PDF).

13. Health and safety:
Question: Do you have a formal occupational health and safety program?
Evidence: Annual OHS program and training plan (PDF).

14. Accidents:
Question: How are work-related incidents handled?
Evidence: Incident reporting procedure and accident log (PDF).

15. Migration costs:
Question: Are migration permits managed without charging workers?
Evidence: Migration management and cost responsibility policy (PDF).

16. Foreign workers information:
Question: Do foreign employees receive clear information on their rights?
Evidence: Guide or manual for foreign employees (PDF).

17. Freedom of association:
Question: Can employees join or form unions?
Evidence: Freedom of association policy (PDF).

18. Complaints channel:
Question: Is there a confidential complaints channel?
Evidence: Complaints procedure and anonymous reporting channel (PDF).

19. Supplier standards:
Question: Are suppliers required to comply with labor standards?
Evidence: Signed supplier code of conduct (PDF).

20. Audits:
Question: Are labor practices audited?
Evidence: Recent labor audit report (PDF).
"""


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

if user_input := st.chat_input("Type your question here"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
{SYSTEM_PROMPT}

Knowledge Base:
{KNOWLEDGE_BASE}

Conversation history:
{st.session_state.messages}

User question:
{user_input}
"""

    response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

