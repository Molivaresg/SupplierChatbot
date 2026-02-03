import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página y Estética
st.set_page_config(page_title="Soporte Evaluación Proveedores", page_icon="📋")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_headers=True)

st.title("🤖 Asistente de Evaluación")
st.info("Hola. Soy tu guía para completar la evaluación. Pregúntame sobre cualquier punto de las 20 secciones iniciales.")

# 2. El Cerebro (Tus 20 preguntas inyectadas)
BASE_DATOS = """
Eres un asistente legal y de cumplimiento para proveedores. Tu objetivo es explicar las preguntas de la evaluación y qué evidencia deben presentar.
INFORMACIÓN DE REFERENCIA:
1. Retención de documentos: No se deben retener pasaportes o IDs. Evidencia: Política de NO retención (PDF).
2. Pagos por empleo: No se piden depósitos para trabajar. Evidencia: Política de contratación que prohíbe cuotas (PDF).
3. Multas internas: No hay penalizaciones económicas. Evidencia: Reglamento interno (PDF).
4. Renuncia libre: Personal puede renunciar sin restricciones. Evidencia: Procedimiento de baja voluntaria (PDF).
5. Acceso a documentos: Acceso libre a documentos personales. Evidencia: Política de RH sobre custodia voluntaria (PDF).
6. Libertad de movimiento: Salida libre en descansos y fuera de horario. Evidencia: Reglamento de acceso/salida (PDF).
7. Jornada legal: Se respetan descansos y leyes. Evidencia: Rol de turnos y control de asistencia (PDF).
8. Horas extra: Son voluntarias y pagadas. Evidencia: Recibos de nómina y política de overtime (PDF).
9. No discriminación: Procesos de contratación justos. Evidencia: Política de igualdad y no discriminación (PDF).
10. Contrato escrito: Se entrega antes de iniciar. Evidencia: Modelo de contrato laboral (PDF).
11. Claridad de condiciones: Se explican salarios y beneficios. Evidencia: Formato de oferta laboral (PDF).
12. Seguridad Social: Afiliación obligatoria al IMSS. Evidencia: Avisos afiliatorios (PDF).
13. Salud y Seguridad: Programa formal de SST. Evidencia: Programa anual de SST (PDF).
14. Accidentes: Gestión de incidentes. Evidencia: Procedimiento de reporte y bitácora (PDF).
15. Gestión migratoria: Sin costos para el trabajador. Evidencia: Política de gestión migratoria (PDF).
16. Info Extranjeros: Información clara de derechos. Evidencia: Guía para personal extranjero (PDF).
17. Sindicatos: Libertad de asociación. Evidencia: Política de libertad de asociación (PDF).
18. Canal de denuncias: Canal confidencial de abusos. Evidencia: Procedimiento de denuncias y portal anónimo (PDF).
19. Proveedores: Deben cumplir normas laborales. Evidencia: Código de conducta firmado (PDF).
20. Auditorías: Prácticas laborales auditadas. Evidencia: Informe de auditoría laboral reciente (PDF).

REGLAS DE RESPUESTA:
- Si el usuario pregunta algo que no está en esta lista, dile amablemente: "Esa pregunta no se encuentra en mi base de datos actual, por favor contacta al equipo de Compras."
- Siempre menciona qué "Ejemplo de evidencia" deben preparar.
"""

# 3. Inicializar Gemini
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los Secrets de Streamlit.")

model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Historial del Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interacción
if prompt := st.chat_input("Ej: ¿Qué debo subir para la pregunta de sindicatos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamada a la IA
    instruccion_total = f"{BASE_DATOS}\n\nPregunta del proveedor: {prompt}"
    try:
        response = model.generate_content(instruccion_total)
        respuesta_texto = response.text
    except Exception as e:
        respuesta_texto = "Lo siento, hubo un error al conectar con el cerebro del bot. Revisa tu API Key."

    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
