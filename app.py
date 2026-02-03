import streamlit as st
import google.generativeai as genai

# 1. Configuración básica
st.set_page_config(page_title="Asistente de Evaluación", layout="centered")
st.title("🤖 Soporte a Proveedores")

# 2. Configurar la API (Asegúrate de que en Secrets diga GOOGLE_API_KEY)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Configura la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Inicializar el modelo con el nombre correcto
model = genai.GenerativeModel("models/chat-bison-001")


# 4. Tu base de datos (Las 20 preguntas)
BASE_DATOS = """
Actúa como un asistente experto. Usa esta información para responder:
1. Pasaportes: No se retienen documentos. Evidencia: Política de NO retención.
2. Pagos: No se piden depósitos. Evidencia: Política de contratación.
3. Multas: No hay sanciones económicas. Evidencia: Reglamento interno.
4. Renuncia: Sin restricciones. Evidencia: Procedimiento de baja.
5. Acceso docs: Acceso libre siempre. Evidencia: Política de RH.
6. Salidas: Libre en descansos. Evidencia: Reglamento de acceso.
7. Jornada: Legal y con descansos. Evidencia: Rol de turnos.
8. Horas extra: Voluntarias y pagadas. Evidencia: Recibos nómina.
9. No discriminación: Proceso justo. Evidencia: Política de igualdad.
10. Contrato: Escrito y previo. Evidencia: Modelo contrato.
11. Condiciones: Claras antes de contratar. Evidencia: Carta oferta.
12. IMSS: Afiliación obligatoria. Evidencia: Avisos afiliatorios.
13. Seguridad: Programa SST. Evidencia: Programa anual SST.
14. Accidentes: Procedimiento reporte. Evidencia: Bitácora accidentes.
15. Migración: Sin costos al trabajador. Evidencia: Política migratoria.
16. Extranjeros: Info clara derechos. Evidencia: Guía extranjeros.
17. Sindicatos: Libertad asociación. Evidencia: Política libertad.
18. Denuncias: Canal confidencial. Evidencia: Portal anónimo.
19. Proveedores: Cumplir normas. Evidencia: Código conducta.
20. Auditorías: Prácticas auditadas. Evidencia: Informe auditoría.
"""

# 5. Interfaz de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generar respuesta (Formato corregido)
    try:
        # Enviamos la instrucción de forma limpia
        mensaje_final = f"{BASE_DATOS}\n\nPregunta: {prompt}"
        response = model.generate_content(mensaje_final)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Hubo un problema: {e}")
