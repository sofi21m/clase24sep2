import os
import base64
import streamlit as st
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuración de página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Visión IA - Análisis de Imágenes",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# -----------------------------------------------------------------------------
# Barra Lateral - Configuración de credenciales
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Configuración")
    
    ke = st.text_input('Ingresa tu API Key de OpenAI', type="password", help="Formato: sk-...")
    if ke:
        os.environ['OPENAI_API_KEY'] = ke

    st.markdown("---")
    st.markdown("### 📌 Instrucciones")
    st.markdown("1. Ingresa tu API Key de OpenAI.")
    st.markdown("2. Sube una imagen (JPG, JPEG o PNG).")
    st.markdown("3. Escribe una pregunta específica si lo deseas.")
    st.markdown("4. Haz clic en **Analizar Imagen**.")

# -----------------------------------------------------------------------------
# Encabezado Principal
# -----------------------------------------------------------------------------
st.title("👁️ Visión Inteligente IA")
st.write("Sube cualquier imagen y deja que el modelo GPT-4o interprete su contenido en detalle.")

st.markdown("---")

# -----------------------------------------------------------------------------
# Layout en Dos Columnas
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🖼️ Imagen de origen")
    uploaded_file = st.file_uploader("Selecciona o arrastra tu archivo", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption=f"📁 {uploaded_file.name}", use_container_width=True)

with col2:
    st.subheader("💬 Opciones de Análisis")
    
    show_details = st.toggle("🔍 ¿Quieres preguntar algo específico?", value=False)
    
    additional_details = ""
    if show_details:
        additional_details = st.text_area(
            "Escribe tu pregunta o dale contexto a la IA:",
            placeholder="Ejemplo: ¿Qué marca es ese automóvil? o ¿Qué ingredientes ves sobre la mesa?",
            height=120
        )

    st.markdown("
