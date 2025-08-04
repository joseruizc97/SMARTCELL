import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="SMARTCELL - Predicción de Precios",
    page_icon="📱",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📱 SMARTCELL</h1>
    <p>Predicción Inteligente de Precios de Móviles</p>
</div>
""", unsafe_allow_html=True)

# Verificar si los archivos del modelo existen
@st.cache_resource
def load_models():
    try:
        # Intentar cargar los modelos
        if os.path.exists("modelo_precio_movil_xgb.pkl"):
            modelo = joblib.load("modelo_precio_movil_xgb.pkl")
            encoder = joblib.load("encoder_categorias.pkl")
            return modelo, encoder, True
        else:
            st.warning("⚠️ Archivos del modelo no encontrados. Usando modo demo.")
            return None, None, False
    except Exception as e:
        st.error(f"❌ Error cargando modelos: {e}")
        return None, None, False

# Cargar modelos
modelo, encoder, modelos_cargados = load_models()

# Datos de ejemplo para demo
marcas = ['apple', 'samsung', 'xiaomi', 'oppo', 'oneplus']
estados = ['nuevo', 'como nuevo', 'buen estado', 'aceptable', 'desgastado']
colores = ['negro', 'azul', 'gris', 'blanco', 'dorado']
provincias = ['madrid', 'barcelona', 'valencia', 'sevilla', 'bilbao']

# Interfaz principal
st.markdown("### 📋 Formulario de Predicción")

col1, col2 = st.columns(2)

with col1:
    marca = st.selectbox("📱 Marca", marcas)
    modelo_telefono = st.text_input("📱 Modelo", "iPhone 13")
    estado = st.selectbox("⭐ Estado", estados)
    capacidad = st.selectbox("💾 Capacidad (GB)", [32, 64, 128, 256, 512])

with col2:
    color = st.selectbox("🎨 Color", colores)
    provincia = st.selectbox("📍 Provincia", provincias)
    año = st.selectbox("📅 Año", list(range(2018, 2025)))

# Botón de predicción
if st.button("🚀 Predecir Precio"):
    if modelos_cargados:
        # Lógica de predicción real
        try:
            # Aquí iría la lógica de predicción real
            precio_estimado = 450.0  # Placeholder
            st.success(f"✅ Precio estimado: {precio_estimado:.2f} €")
        except Exception as e:
            st.error(f"❌ Error en la predicción: {e}")
    else:
        # Modo demo
        import random
        precio_demo = random.uniform(200, 800)
        st.markdown(f"""
        <div class="metric-card">
            <h2>💰 Precio Estimado (Demo)</h2>
            <h1>{precio_demo:.0f} €</h1>
            <p>Modo demostración - Modelos no disponibles</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 Esta es una versión demo. Los modelos reales no están disponibles en este entorno.")

# Información adicional
st.markdown("---")
st.markdown("### 📊 Información del Proyecto")
st.write("""
- **Tecnología:** Machine Learning con XGBoost
- **Datos:** Análisis de precios de móviles de segunda mano
- **Funcionalidades:** Predicción de precios, comparador, generador de posteos
- **Estado:** En desarrollo para despliegue online
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🚀 SMARTCELL - Desarrollado con ❤️ para el mercado de móviles de segunda mano</p>
</div>
""", unsafe_allow_html=True) 