import os
import base64
import streamlit as st
from openai import OpenAI

# -----------------------------------------------------------------------------
# Configuración general y estilos personalizados
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Visión IA - Análisis de Imágenes",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados para darle vida y color a la interfaz
st.markdown("""
    
""", unsafe_allow_html=True)


def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


# -----------------------------------------------------------------------------
# Barra Lateral - Configuración de credenciales
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8637/8637101.png", width=100)
    st.title("⚙️ Configuración")
    
    ke = st.text_input('Ingresa tu API Key de OpenAI', type="password", help="Formato: sk-...")
    if ke:
        os.environ['OPENAI_API_KEY'] = ke

    st.markdown("---")
    st.markdown("""
        ### 📌 Instrucciones:
        1. Ingresa tu API Key de OpenAI.
        2. Sube una imagen en formato JPG, JPEG o PNG.
        3. Opcionalmente, escribe una pregunta o indicación específica.
        4. Haz clic en **Analizar Imagen**.
    """)


# -----------------------------------------------------------------------------
# Encabezado Principal
# -----------------------------------------------------------------------------
st.markdown('
