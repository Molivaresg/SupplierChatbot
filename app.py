import streamlit as st
import google.generativeai as genai

# 1. Configuración básica (Sin estilos complejos para evitar errores)
st.set_page_config(page_title="Soporte Proveedores", page_icon="📋")

st.title("🤖 Asistente de Evaluación")
st.write("Hola. Resuelvo tus dudas sobre las 20 preguntas iniciales.")

# 2. El Cerebro
BASE_DATOS = """
Eres un asistente para proveedores. Responde basándote en esto:
1. Retención de documentos: No se retienen pasaportes. Evidencia: Política de NO retención (PDF).
2. Pagos: No se piden depósitos. Evidencia: Política de contratación (PDF).
3. Multas: No hay sanciones económicas. Evidencia: Reglamento interno (PDF).
4. Renuncia: Sin restricciones. Evidencia: Procedimiento de baja (PDF).
5. Acceso docs: Acceso libre siempre. Evidencia: Política de RH (PDF).
6. Salidas: Libre en descansos. Evidencia: Reglamento de acceso (PDF).
7. Jornada: Legal y con descansos. Evidencia: Rol de turnos (PDF).
8. Horas extra: Voluntarias y pagadas. Evidencia: Recibos nómina (PDF).
9. No discriminación: Proceso justo. Evidencia: Política de igualdad (PDF).
10. Contrato: Escrito y previo. Evidencia: Modelo contrato (PDF).
11. Condiciones: Claras antes de contratar. Evidencia: Carta oferta (PDF).
12. IMSS: Afiliación obligatoria. Evidencia: Avisos afiliatorios (PDF).
13. Seguridad: Programa SST. Evidencia: Programa anual SST (PDF).
14. Accidentes: Procedimiento reporte. Evidencia: Bitácora accidentes (PDF).
15. Migración: Sin costos al trabajador. Evidencia: Política migratoria (PDF).
16. Extranjeros: Info clara derechos. Evidencia: Guía extranjeros (PDF).
17. Sindicatos: Libertad asociación. Evidencia: Política libertad (PDF).
18. Denuncias: Canal confidencial. Evidencia: Portal anónimo (PDF).
19. Proveedores: Cumplir normas. Evidencia: Código conducta (PDF).
20. Auditorías: Prácticas auditadas. Evidencia: Informe auditoría (PDF).
"""

# 3. Configurar IA (Usando Secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error("Error con la API Key. Verifica los Secrets en Streamlit.")

# 4. Historial del Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat
if prompt := st.chat_input("¿En qué pregunta tienes duda?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta
    contexto_ia = f"{BASE_DATOS}\n\nResponde a: {prompt}"
    response = model.generate_content(contexto_ia)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
