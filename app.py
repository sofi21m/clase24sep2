import os
import base64
import streamlit as st
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuración inicial de la app
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Análisis de Imagen con IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# -----------------------------------------------------------------------------
# Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Configuración")
    
    ke = st.text_input('Ingresa tu API Key de OpenAI:', type="password", help="Formato: sk-...")
    if ke:
        os.environ['OPENAI_API_KEY'] = ke

    st.divider()
    st.subheader("📌 Instrucciones")
    st.write("1. Ingresa tu Clave de OpenAI arriba.")
    st.write("2. Sube una imagen (JPG, PNG o JPEG).")
    st.write("3. (Opcional) Activa la casilla para hacer una pregunta específica.")
    st.write("4. Presiona el botón para analizar.")

# -----------------------------------------------------------------------------
# Panel Principal - Encabezado
# -----------------------------------------------------------------------------
st.title("🤖 Análisis Inteligente de Imágenes")
st.caption("Sube una imagen y deja que el modelo GPT-4o describa o responda preguntas sobre ella.")
st.divider()

# -----------------------------------------------------------------------------
# Layout en Dos Columnas
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🖼️ Imagen de Origen")
    uploaded_file = st.file_uploader("Carga tu archivo de imagen aquí:", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

with col2:
    st.subheader("💬 Opciones de Consulta")
    
    show_details = st.toggle("🔍 ¿Quieres preguntar algo específico?", value=False)
    
    additional_details = ""
    if show_details:
        additional_details = st.text_area(
            "Escribe tu pregunta o contexto aquí:",
            placeholder="Ejemplo: ¿Qué objetos hay sobre la mesa?",
            height=120
        )

    st.write("") # Espaciador
    analyze_button = st.button("🚀 Analizar Imagen", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# Lógica de Ejecución y Proceso RAG / Visión
# -----------------------------------------------------------------------------
if analyze_button:
    api_key = os.environ.get('OPENAI_API_KEY', '')

    if not api_key:
        st.error("⚠️ Falta la API Key: Por favor ingresa tu clave de OpenAI en la barra lateral izquierda.")
    elif not uploaded_file:
        st.warning("⚠️ Falta la imagen: Por favor sube una imagen antes de hacer clic en analizar.")
    else:
        client = OpenAI(api_key=api_key)

        st.divider()
        st.subheader("📊 Resultado del Análisis")

        with st.spinner("🧠 Analizando la imagen con GPT-4o..."):
            try:
                base64_image = encode_image(uploaded_file)

                prompt_text = "Describe lo que ves en la imagen en español con buen detalle."
                if show_details and additional_details.strip():
                    prompt_text = f"Responde a la siguiente consulta sobre la imagen en español: {additional_details.strip()}"

                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                        ],
                    }
                ]

                # Mostramos la respuesta en tiempo real dentro de una caja de texto bonita (st.chat_message)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    for completion in client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        max_tokens=1200,
                        stream=True
                    ):
                        if completion.choices[0].delta.content is not None:
                            full_response += completion.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"❌ Ocurrió un error al procesar la imagen: {e}")
