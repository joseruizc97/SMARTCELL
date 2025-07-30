import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import requests
import json
import os



# Cargar modelo y encoder
modelo = joblib.load("modelo_precio_movil_xgb.pkl")
encoder = joblib.load("encoder_categorias.pkl")





def generar_consejos_venta_ia(marca, modelo, estado, año_lanzamiento, capacidad, color, provincia, precio_predicho):
    """
    Genera consejos de venta específicos usando lógica de IA
    """
    
    # Diccionario de marcas más conocidas
    marcas_amigables = {
        'apple': 'iPhone',
        'samsung': 'Samsung Galaxy',
        'xiaomi': 'Xiaomi',
        'oppo': 'OPPO',
        'oneplus': 'OnePlus',
        'realme': 'Realme',
        'motorola': 'Motorola',
        'alcatel': 'Alcatel',
        'tcl': 'TCL',
        'nothing phone': 'Nothing Phone',
        'sony': 'Sony Xperia',
        'google': 'Google Pixel',
        'honor': 'Honor',
        'huawei': 'Huawei',
        'vivo': 'Vivo',
        'asus': 'Asus',
        'fairphone': 'Fairphone',
        'nokia': 'Nokia',
        'zte': 'ZTE'
    }
    
    marca_amigable = marcas_amigables.get(str(marca), str(marca))
    antigüedad = datetime.now().year - int(año_lanzamiento)
    
    # Análisis de mercado por marca
    consejos_marca = {
        'apple': {
            'fortalezas': ['Alta demanda', 'Buena retención de valor', 'Mercado premium'],
            'consejos': ['Destaca la calidad de construcción', 'Menciona la compatibilidad con iOS', 'Enfócate en la durabilidad'],
            'plataformas_recomendadas': ['Wallapop', 'Milanuncios', 'Facebook Marketplace'],
            'precio_optimo': precio_predicho * 1.05  # 5% más alto
        },
        'samsung': {
            'fortalezas': ['Variedad de modelos', 'Buena relación calidad-precio', 'Tecnología avanzada'],
            'consejos': ['Resalta las características técnicas', 'Menciona la pantalla AMOLED', 'Destaca la versatilidad'],
            'plataformas_recomendadas': ['Wallapop', 'Milanuncios', 'Vibbo'],
            'precio_optimo': precio_predicho * 1.03
        },
        'xiaomi': {
            'fortalezas': ['Excelente relación calidad-precio', 'Tecnología actual', 'Buena batería'],
            'consejos': ['Enfócate en el precio competitivo', 'Destaca la batería', 'Menciona MIUI'],
            'plataformas_recomendadas': ['Wallapop', 'Milanuncios'],
            'precio_optimo': precio_predicho * 0.98
        },
        'oppo': {
            'fortalezas': ['Cámaras de calidad', 'Carga rápida', 'Diseño atractivo'],
            'consejos': ['Destaca la calidad de cámara', 'Menciona la carga rápida', 'Enfócate en el diseño'],
            'plataformas_recomendadas': ['Wallapop', 'Milanuncios'],
            'precio_optimo': precio_predicho * 1.02
        },
        'oneplus': {
            'fortalezas': ['Rendimiento premium', 'OxygenOS', 'Carga rápida'],
            'consejos': ['Destaca el rendimiento', 'Menciona OxygenOS', 'Enfócate en la velocidad'],
            'plataformas_recomendadas': ['Wallapop', 'Milanuncios', 'Facebook Marketplace'],
            'precio_optimo': precio_predicho * 1.04
        }
    }
    
    # Consejos por estado del dispositivo
    consejos_estado = {
        'nuevo': {
            'consejos': ['Destaca que está sin usar', 'Mantén el precio alto', 'Incluye todos los accesorios'],
            'factor_precio': 1.1
        },
        'como nuevo': {
            'consejos': ['Enfócate en el excelente estado', 'Menciona el uso mínimo', 'Destaca la garantía'],
            'factor_precio': 1.05
        },
        'buen estado': {
            'consejos': ['Destaca el buen funcionamiento', 'Menciona el mantenimiento', 'Ofrece garantía'],
            'factor_precio': 1.0
        },
        'aceptable': {
            'consejos': ['Sé honesto sobre el estado', 'Ofrece un precio competitivo', 'Destaca la funcionalidad'],
            'factor_precio': 0.9
        },
        'desgastado': {
            'consejos': ['Enfócate en el precio bajo', 'Sé transparente sobre el estado', 'Ofrece como repuesto'],
            'factor_precio': 0.7
        }
    }
    
    # Consejos por antigüedad
    consejos_antigüedad = {
        0: "Dispositivo del año actual - máximo valor",
        1: "Dispositivo reciente - muy buena retención de valor",
        2: "Dispositivo de 2 años - buen valor",
        3: "Dispositivo de 3 años - precio moderado",
        4: "Dispositivo de 4 años - precio económico",
        5: "Dispositivo de 5+ años - precio muy económico"
    }
    
    # Consejos por capacidad
    consejos_capacidad = {
        32: "Capacidad básica - precio más bajo",
        64: "Capacidad estándar - precio equilibrado",
        128: "Capacidad popular - mejor valor",
        256: "Capacidad premium - precio más alto",
        512: "Capacidad máxima - precio premium"
    }
    
    # Obtener consejos específicos
    info_marca = consejos_marca.get(str(marca), {
        'fortalezas': ['Buena marca', 'Calidad garantizada'],
        'consejos': ['Destaca las características', 'Ofrece garantía'],
        'plataformas_recomendadas': ['Wallapop', 'Milanuncios'],
        'precio_optimo': precio_predicho
    })
    
    info_estado = consejos_estado.get(str(estado), {
        'consejos': ['Destaca el estado general'],
        'factor_precio': 1.0
    })
    
    # Generar análisis completo
    precio_optimo = info_marca['precio_optimo'] * info_estado['factor_precio']
    
    return {
        'precio_optimo': precio_optimo,
        'fortalezas_marca': info_marca['fortalezas'],
        'consejos_marca': info_marca['consejos'],
        'consejos_estado': info_estado['consejos'],
        'plataformas_recomendadas': info_marca['plataformas_recomendadas'],
        'consejo_antigüedad': consejos_antigüedad.get(antigüedad, "Dispositivo con varios años"),
        'consejo_capacidad': consejos_capacidad.get(capacidad, "Capacidad estándar"),
        'factor_competitividad': "Alto" if precio_predicho < 300 else "Medio" if precio_predicho < 600 else "Bajo"
    }

# Configuración de la página
st.set_page_config(
    page_title="SMARTCELL - Predicción Inteligente de Precios",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-style: italic;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 2rem 0 1rem 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .form-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #333;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <div class="main-title">📱 SMARTCELL</div>
    <div class="subtitle">Predicción Inteligente de Precios de Móviles</div>
</div>
""", unsafe_allow_html=True)



# Sección de características destacadas
st.markdown("""
<div class="feature-grid">
    <div class="feature-item">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">IA Inteligente</div>
        <div class="feature-desc">Consejos personalizados por marca y modelo</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">💰</div>
        <div class="feature-title">Precio Óptimo</div>
        <div class="feature-desc">Análisis de mercado en tiempo real</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Comparador</div>
        <div class="feature-desc">Simula diferentes configuraciones</div>
    </div>
    <div class="feature-item">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Posteos</div>
        <div class="feature-desc">Genera anuncios optimizados</div>
    </div>
</div>
""", unsafe_allow_html=True)



# Listas de opciones (rellenadas desde el modelo o manualmente)
estado_dict = {
    'nuevo': 4,
    'como nuevo': 3,
    'buen estado': 2,
    'aceptable': 1,
    'desgastado': 0
}

# Lista de estados para el selectbox
todos_estados = ['Selecciona una opción...'] + list(estado_dict.keys())

# Diccionario de marcas y sus modelos correspondientes
marcas_modelos = {
    'apple': ['iphone 7', 'iphone 8', 'iphone se 2020', 'iphone x', 'iphone xr', 'iphone 11', 'iphone 11 pro', 'iphone 11 pro max', 'iphone 12', 'iphone 12 mini', 'iphone 12 pro', 'iphone 12 pro max', 'iphone 13', 'iphone 13 mini', 'iphone 13 pro', 'iphone 13 pro max', 'iphone 14', 'iphone 14 plus', 'iphone 14 pro', 'iphone 14 pro max', 'iphone 15', 'iphone 15 plus', 'iphone 15 pro', 'iphone 15 pro max', 'iphone 16', 'iphone 16 plus', 'iphone 16 pro', 'iphone 16 pro max', 'iphone 16e'],
    'samsung': ['galaxy a05s', 'galaxy a06', 'galaxy a10', 'galaxy a12', 'galaxy a13', 'galaxy a13 5g', 'galaxy a14', 'galaxy a14 5g', 'galaxy a15', 'galaxy a15 5g', 'galaxy a16', 'galaxy a16 5g', 'galaxy a20e', 'galaxy a21s', 'galaxy a22', 'galaxy a23 5g', 'galaxy a25', 'galaxy a26', 'galaxy a32', 'galaxy a32 5g', 'galaxy a33 5g', 'galaxy a34', 'galaxy a35', 'galaxy a36', 'galaxy a40', 'galaxy a50', 'galaxy a51', 'galaxy a52', 'galaxy a52 5g', 'galaxy a52s 5g', 'galaxy a53 5g', 'galaxy a54', 'galaxy a55', 'galaxy a56', 'galaxy a6', 'galaxy a70', 'galaxy a71', 'galaxy j4 plus', 'galaxy j5', 'galaxy j7', 'galaxy note10', 'galaxy note10 plus', 'galaxy note20 ultra 5g', 'galaxy s10', 'galaxy s10 plus', 'galaxy s10e', 'galaxy s20', 'galaxy s20 fe', 'galaxy s20 fe 5g', 'galaxy s20 plus', 'galaxy s21', 'galaxy s21 5g', 'galaxy s21 fe 5g', 'galaxy s21 plus 5g', 'galaxy s21 ultra 5g', 'galaxy s22 5g', 'galaxy s22 plus 5g', 'galaxy s22 ultra 5g', 'galaxy s23', 'galaxy s23 fe', 'galaxy s23 plus', 'galaxy s23 ultra', 'galaxy s24', 'galaxy s24 fe', 'galaxy s24 plus', 'galaxy s24 ultra', 'galaxy s25', 'galaxy s25 plus', 'galaxy s25 ultra', 'galaxy s6', 'galaxy s7', 'galaxy s7 edge', 'galaxy s8', 'galaxy s9', 'galaxy s9 plus', 'galaxy z flip 3 5g', 'galaxy z flip 4', 'galaxy z flip 5', 'galaxy z flip 6', 'galaxy z fold 3 5g', 'galaxy z fold 4', 'galaxy z fold 6'],
    'xiaomi': ['redmi 10', 'redmi 12', 'redmi 12c', 'redmi 13', 'redmi 13c', 'redmi 9', 'redmi 9a', 'redmi 9c', 'redmi a2', 'redmi a3', 'redmi a5 4g', 'redmi note 10 pro', 'redmi note 10s', 'redmi note 11', 'redmi note 11 pro 5g', 'redmi note 11s', 'redmi note 12', 'redmi note 12 pro', 'redmi note 13', 'redmi note 13 pro', 'redmi note 13 pro plus', 'redmi note 14 4g', 'redmi note 14 5g', 'redmi note 14 pro 4g', 'redmi note 14 pro plus 5g', 'redmi note 14c 4g', 'redmi note 7', 'redmi note 8', 'redmi note 8 pro', 'redmi note 8t', 'redmi note 9', 'redmi note 9 pro'],
    'oppo': ['oppo a15', 'oppo a16s', 'oppo a17', 'oppo a18', 'oppo a38', 'oppo a40', 'oppo a5 pro', 'oppo a5 pro 5g', 'oppo a53s', 'oppo a54', 'oppo a54 5g', 'oppo a54s', 'oppo a57', 'oppo a57s', 'oppo a60', 'oppo a60 5g', 'oppo a72', 'oppo a74', 'oppo a74 5g', 'oppo a78', 'oppo a78 5g', 'oppo a79', 'oppo a79 5g', 'oppo a80', 'oppo a80 5g', 'oppo a9 (2020)', 'oppo a91', 'oppo a94 5g', 'oppo find n2 flip', 'oppo find x3 lite', 'oppo find x3 pro', 'oppo find x5', 'oppo find x5 lite', 'oppo find x5 pro', 'oppo find x8 pro', 'oppo reno 10 5g', 'oppo reno 12', 'oppo reno 12f', 'oppo reno 13f 5g', 'oppo reno 4z 5g'],
    'oneplus': ['nord', 'nord 2 5g', 'nord 2t', 'nord 3'],
    'realme': ['gt 6', 'gt 7 pro', 'gt master', 'gt neo2', 'gt2', 'gt2 pro'],
    'motorola': ['moto g15', 'moto g35', 'moto g55'],
    'alcatel': ['alcatel 1', 'alcatel 1 (2021)', 'alcatel 1se (2020)', 'blade a35', 'blade a55', 'c11', 'c21', 'c53', 'c55', 'c61'],
    'tcl': ['tcl 10 se', 'tcl 20 5g', 'tcl 20 se', 'tcl 30 se', 'tcl 306', 'tcl 40 nxtpaper 5g', 'tcl 40 se', 'tcl 50 5g', 'tcl 50 nxtpaper', 'tcl 50 pro nxtpaper'],
    'nothing phone': ['nothing phone (1)', 'nothing phone (2)', 'nothing phone (2a)'],
    'sony': ['sony xperia'],
    'google': ['10', '10 pro', '11', '11 lite 5g ne', '12', '12 pro', '12 pro plus', '12x', '13', '14 pro plus', '14t', '14x'],
    'honor': ['5', '6', '7', '8', '8 pro', '8i', '8t', '9', '9 pro'],
    'huawei': ['note 50', 'note 60'],
    'vivo': ['otros'],
    'asus': ['otros'],
    'fairphone': ['otros'],
    'nokia': ['otros'],
    'zte': ['otros']
}

# Diccionario con los años de lanzamiento específicos por modelo
modelo_año_lanzamiento = {
    # Samsung
    "galaxy s23 fe": 2023, "galaxy note10 plus": 2019, "galaxy a52 5g": 2021, "galaxy a16": 2024,
    "galaxy a15": 2023, "galaxy a36": 2024, "galaxy a15 5g": 2023, "galaxy a22": 2021,
    "galaxy s23 ultra": 2023, "galaxy s20 fe": 2020, "galaxy s24": 2024, "galaxy a05": 2023,
    "galaxy a6": 2018, "galaxy a51": 2020, "galaxy a54": 2023, "galaxy j7": 2015,
    "galaxy s22 5g": 2022, "galaxy a34": 2023, "galaxy a8": 2018, "galaxy a13": 2022,
    "galaxy a70": 2019, "galaxy s25": 2025, "galaxy a56": 2025, "galaxy z fold 4": 2022,
    "galaxy z flip 6": 2025, "galaxy a50": 2019, "galaxy s22 ultra 5g": 2022, "galaxy a53 5g": 2022,
    "galaxy s20 plus 5g": 2020, "galaxy s20 plus": 2020, "galaxy a25": 2023, "galaxy a40": 2019,
    "galaxy note20": 2020, "galaxy s21 ultra 5g": 2021, "galaxy a52s 5g": 2021, "galaxy s21 5g": 2021,
    "galaxy a10": 2019, "galaxy a35": 2024, "galaxy s25 ultra": 2025, "galaxy a14": 2023,
    "galaxy s21 fe 5g": 2022, "galaxy a05s": 2023, "galaxy s23": 2023, "galaxy s4": 2013,
    "galaxy a55": 2025, "galaxy a20e": 2019, "galaxy core prime": 2014, "galaxy s24 fe": 2024,
    "galaxy a26": 2024, "galaxy a12": 2020, "galaxy s25 plus": 2025, "galaxy note20 ultra 5g": 2020,
    "galaxy s20 ultra": 2020, "galaxy s22 plus 5g": 2022, "galaxy a32 5g": 2021, "galaxy a03 core": 2021,
    "galaxy note10 lite": 2020, "galaxy s20": 2020, "galaxy s6": 2015, "galaxy s24 plus": 2024,
    "galaxy s20 5g": 2020, "galaxy a72": 2021, "galaxy a16 5g": 2024, "galaxy s21": 2021,
    "galaxy z fold 5": 2023, "galaxy note10": 2019, "galaxy a23": 2022, "galaxy a20": 2019,
    "galaxy j6 plus": 2018, "galaxy z flip 4": 2022, "galaxy s24 ultra": 2024, "galaxy s9": 2018,
    "galaxy m30s": 2019, "galaxy a33 5g": 2022, "galaxy a04e": 2023, "galaxy z fold 2 5g": 2020,
    "galaxy note9": 2018, "galaxy s20 fe 5g": 2020, "galaxy s10": 2019, "galaxy z fold 3 5g": 2021,
    "galaxy a21s": 2020, "galaxy z flip 3 5g": 2021, "galaxy a3": 2014, "galaxy a71 5g": 2020,
    "galaxy s20 ultra 5g": 2020, "galaxy note20 ultra": 2020, "galaxy a23 5g": 2022, "galaxy a04s": 2023,
    "galaxy a06": 2023, "galaxy a6 plus": 2018, "galaxy s10 plus": 2019, "galaxy grand prime": 2014,
    "galaxy s21 plus 5g": 2021, "galaxy a31": 2020, "galaxy a5": 2014, "galaxy s7": 2016,
    "galaxy j5 2016": 2016, "galaxy a71": 2020, "galaxy a22 5g": 2021, "galaxy s23 plus": 2023,
    "galaxy a52": 2021, "galaxy a02s": 2021, "galaxy note8": 2017, "galaxy j4 plus": 2018,
    "galaxy j7 2016": 2016, "galaxy z flip 5": 2023, "galaxy a13 5g": 2022, "galaxy s8": 2017,
    "galaxy s9 plus": 2018, "galaxy s8 plus": 2017, "galaxy a10s": 2019, "galaxy a5 2016": 2016,
    "galaxy z flip": 2020, "galaxy j3 2016": 2016, "galaxy z fold 6": 2025, "galaxy s10e": 2019,
    "galaxy a32": 2021, "galaxy j3 2017": 2017, "galaxy a3 2016": 2016, "galaxy a7 2018": 2018,
    "galaxy xcover 3": 2015, "galaxy s4 zoom": 2013, "galaxy a14 5g": 2023, "galaxy note20 5g": 2020,
    "galaxy s25 edge": 2025, "galaxy j5": 2015, "galaxy j5 2017": 2017, "galaxy s7 edge": 2016,
    "galaxy j7 2017": 2017, "galaxy m52 5g": 2021, "galaxy a02": 2021, "galaxy m13": 2022,
    "galaxy a41": 2020, "galaxy m10": 2019, "galaxy s iii cdma": 2012, "galaxy a30s": 2019,
    "galaxy a03": 2022, "galaxy a90 5g": 2019, "galaxy a03s": 2021, "galaxy m55": 2024,
    "galaxy a24 4g": 2023, "galaxy a51 5g": 2020, "galaxy m02": 2021, "galaxy s5": 2014,
    "galaxy a04": 2023, "galaxy j7 duo": 2018, "galaxy a20s": 2019, "galaxy a42 5g": 2020,
    "galaxy m33": 2022, "galaxy a7": 2014, "galaxy j6": 2018,

    # iPhone
    "iphone 14": 2022, "iphone 11": 2019, "iphone 12": 2020, "iphone 16 plus": 2024,
    "iphone 13": 2021, "iphone 12 mini": 2020, "iphone 16e": 2024, "iphone 7": 2016,
    "iphone se 2020": 2020, "iphone 15": 2023, "iphone xr": 2018, "iphone 16 pro max": 2024,
    "iphone 11 pro": 2019, "iphone 12 pro": 2020, "iphone 16": 2024, "iphone x": 2017,
    "iphone 16 pro": 2024, "iphone 13 pro": 2021, "iphone 8": 2017, "iphone 13 mini": 2021,
    "iphone se 2022": 2022, "iphone 12 pro max": 2020, "iphone 11 pro max": 2019, "iphone 15 plus": 2023,
    "iphone 6": 2014, "iphone 15 pro max": 2023, "iphone 15 pro": 2023, "iphone 13 pro max": 2021,
    "iphone 14 pro": 2022, "iphone xs": 2018, "iphone 5s": 2013, "iphone 14 plus": 2022,
    "iphone xs max": 2018, "iphone 8 plus": 2017, "iphone 4": 2010, "iphone 6s": 2015,
    "iphone 14 pro max": 2022, "iphone 7 plus": 2016, "iphone 5": 2012, "iphone 6 plus": 2014,

    # OPPO
    "oppo a76": 2022, "oppo a40": 2021, "oppo a16s": 2021, "oppo find x8 pro": 2024,
    "oppo reno 6 pro 5g": 2021, "oppo a16": 2021, "oppo a17": 2022, "oppo a54s": 2021,
    "oppo a78 5g": 2023, "oppo a54 5g": 2021, "oppo reno 10 5g": 2023, "oppo a5 pro": 2025,
    "oppo a80": 2024, "oppo find x3 lite": 2021, "oppo reno 13f 5g": 2025, "oppo find x3 pro": 2021,
    "oppo reno 8 pro 5g": 2022, "oppo a60 5g": 2024, "oppo a96": 2022, "oppo ax7": 2018,
    "oppo a60": 2024, "oppo reno 12f": 2024, "oppo a72": 2020, "oppo a38": 2023,
    "oppo a18": 2023, "oppo a57s": 2022, "oppo a98 5g": 2023, "oppo find x5 lite": 2022,
    "oppo a15": 2020, "oppo reno 4z": 2020, "oppo a9 (2020)": 2019, "oppo a78": 2023,
    "oppo a54": 2021, "oppo a94 5g": 2021, "oppo a74 5g": 2021, "oppo a79 5g": 2023,
    "oppo a74": 2021, "oppo reno 12f 5g": 2024, "oppo reno 6": 2021, "oppo a57": 2022,
    "oppo a5 pro 5g": 2025, "oppo find x5": 2022, "oppo reno 8 lite 5g": 2022, "oppo reno 12": 2024,
    "oppo reno 12 pro 5g": 2024, "oppo a9": 2019, "oppo a98": 2023, "oppo reno 2z": 2019,
    "oppo x3 neo": 2021, "oppo find x3 neo": 2021, "oppo a53s": 2021, "oppo find n2 flip": 2023,
    "oppo a5 (2020)": 2020, "oppo find x2 lite": 2020, "oppo reno 4z 5g": 2020, "oppo reno 8 pro": 2022,
    "oppo reno 10 pro": 2023, "oppo find x3 lite 5g": 2021, "oppo reno 6 5g": 2021, "oppo reno 8 lite": 2022,
    "oppo a80 5g": 2024, "oppo reno 11f 5g": 2024, "oppo a73 5g": 2020, "oppo a79": 2023,
    "oppo find x2 pro": 2020, "oppo reno 13 5g": 2024, "oppo find n": 2021, "oppo reno 13": 2024,
    "oppo find x5 pro": 2022, "oppo a58": 2022, "oppo a52": 2020, "oppo reno 13 pro": 2024,
    "oppo a59": 2020, "oppo reno 4": 2020, "oppo reno 12 5g": 2024, "oppo a72 5g": 2020,
    "oppo a53": 2020, "oppo reno 10": 2023, "oppo a91": 2020, "oppo reno 8": 2022,
    "oppo reno 12 pro": 2024, "oppo reno 10x zoom": 2019, "oppo reno z": 2019, "oppo find x8s": 2025,
    "oppo reno 4 pro": 2020, "oppo a15s": 2020, "oppo a94": 2021, "oppo reno 13f": 2025,
    "oppo find x7 ultra": 2024, "oppo reno 11f": 2024, "oppo reno 4 pro 5g": 2020,

    # Huawei
    "p30 lite": 2019, "p10 plus": 2017, "p30": 2019, "p smart 2019": 2019,
    "p20 lite": 2018, "p smart plus 2019": 2019, "mate 20 x": 2018,

    # Realme
    "note 60": 2024, "5 pro": 2019, "13 pro plus": 2024, "10": 2021, "c3": 2020,
    "c33": 2023, "gt master": 2021, "7": 2020, "5": 2021, "14x": 2024, "9": 2021,
    "8": 2021, "12": 2021, "c21y": 2021, "c61": 2024, "12 pro plus": 2024, "12 pro": 2021,
    "6": 2020, "gt 7t": 2025, "c21": 2021, "11": 2021, "gt 7": 2025, "14t": 2024,
    "c31": 2021, "c65": 2024, "11 pro": 2021, "c75": 2025, "note 50": 2024, "gt 6": 2024,
    "14 pro plus": 2025, "gt 7 pro": 2025, "11 pro plus": 2021, "8i": 2021, "c11": 2020,
    "12x": 2021, "13 pro": 2023, "7i": 2020, "12 plus": 2022, "gt2": 2022, "c25y": 2021,
    "c11 2021": 2021, "gt neo2": 2021, "c35": 2022, "gt2 pro": 2022, "gt neo 3t": 2022,
    "c55": 2023, "gt 6t": 2024, "6i": 2021, "c67": 2023, "c53": 2023, "8 pro": 2021,
    "10 pro": 2021, "x2 pro": 2023, "6 pro plus": 2020, "14 pro": 2024, "c51": 2023,
    "6 pro": 2020, "gt 5g": 2021, "14": 2024, "c30": 2023, "c3 3 camaras": 2020,
    "narzo 50 5g": 2021, "x50 5g": 2020, "7 pro": 2020, "x50 pro 5g": 2020, "9i": 2020,
    "3": 2020, "gt neo 3": 2022, "narzo 50i prime": 2021, "narzo 50a prime": 2021,

    # OnePlus
    "nord ce 2 5g": 2021, "x": 2015, "9 pro": 2021, "8t": 2020, "7t pro": 2020,
    "nord 2t": 2022, "12": 2023, "9": 2021, "8": 2020, "7": 2019, "10 pro": 2022,
    "13t": 2024, "nord 2 5g": 2021, "nord ce 3 lite": 2022, "nord 3": 2022, "5t": 2017,
    "10t": 2023, "11": 2023, "nord": 2020, "nord ce 2 lite 5g": 2022, "5": 2020,
    "8 5g (t-mobile)": 2021, "6": 2018, "one": 2014, "13": 2023, "9rt 5g": 2021,
    "nord ce 5g": 2021, "12r": 2022, "nord ce4 lite": 2023, "7t": 2019, "6t": 2019,
    "2": 2015, "3": 2016, "nord 4": 2024, "nord n20 se": 2022, "8 pro": 2023,
    "open": 2023, "7 pro": 2017, "8t plus 5g": 2022, "nord n10 5g": 2020,
    "7t pro 5g mclaren": 2020, "3t": 2016,

    # Google
    "pixel 9a": 2025, "pixel 9 pro xl": 2024, "pixel 8": 2023, "pixel 7 pro": 2022,
    "pixel 8a": 2023, "pixel 6a": 2022, "pixel 9a 8gb 128gb": 2025, "pixel 6": 2021,
    "pixel 2 xl": 2017, "pixel 7": 2022, "pixel 8 pro": 2023, "pixel 9": 2024,
    "pixel 9 pro fold": 2024, "pixel 8 8gb 256gb": 2023, "pixel 8 8gb 128gb": 2023,
    "pixel 5": 2020, "pixel 3": 2018, "pixel 4": 2019, "pixel 4a": 2020, "pixel fold": 2023,
    "pixel 9 xl pro": 2024, "pixel 9 12gb 128gb": 2024, "pixel 9pro xl": 2024,
    "pixel 9 pro fold": 2024, "pixel 3 xl": 2018,

    # Vivo
    "y28": 2024, "iqoo neo 10 pro": 2024, "x fold 3": 2024, "y01": 2021, "y19s": 2021,
    "y16": 2021, "y28s": 2022, "x fold 3": 2024, "y12": 2021, "x90 pro+": 2022,
    "y76 5g": 2022,

    # Motorola
    "razr 50 ultra": 2024, "razr 40 ultra": 2023, "razr 50": 2024, "razr 40": 2023,
    "edge 50 fusion": 2024, "edge 50 pro": 2024, "edge 50": 2024, "edge 50 neo": 2024,
    "edge 50 ultra": 2024, "edge 60 fusion": 2025, "edge 60": 2025, "edge 60 pro": 2025,
    "moto g15": 2024, "moto g35": 2024, "moto g55": 2024, "moto g04s": 2024,
    "moto g54": 2023, "moto g85": 2024, "moto g24": 2024, "edge 40 neo": 2023,
    "moto g14": 2023, "edge 30": 2022, "edge 40": 2023, "moto g34": 2024, "moto g": 2013,
    "edge 30 fusion": 2022, "moto e5": 2018,

    # Nokia
    "8": 2017, "3.1": 2018, "7230": 2009, "c20": 2021, "1.3": 2021, "2660 flip": 2022,
    "210": 2019, "lumia 520": 2013, "n95": 2007, "5": 2020, "2": 2020, "7": 2019,
    "150": 2016, "n70": 2005, "7 plus": 2018, "1": 2021,

    # Sony
    "sony xperia l1": 2016, "sony xperia 1": 2019, "sony xperia l2": 2018, "sony xperia xz2": 2018,
    "sony xperia x": 2016, "sony xperia": 2020, "sony xperia xa1": 2016, "sony xperia 10": 2019,
    "sony xperia z5": 2015, "sony xperia z3": 2014, "sony xperia z1": 2013, "sony xperia 5 ii": 2020,
    "sony xperia xa2": 2018, "sony xperia sp": 2013, "sony xperia c4": 2015, "sony xperia 1 iii": 2021,
    "sony xperia l3": 2019, "sony xperia z2": 2013, "sony xperia 1 ii": 2020, "sony xperia vi": 2022,
    "sony xperia 10v": 2022, "sony xperia xa ultra": 2016, "sony xperia 5 iii": 2021,

    # Asus
    "rog phone 6": 2022, "zenfone 4": 2017, "zenfone 10": 2024, "rog phone 9": 2024,
    "rog phone 6d": 2022, "zenfone 8": 2021, "zenfone go": 2015, "zenfone 3 max": 2016,
    "zenfone 9": 2022,

    # Honor
    "400": 2025, "magic4 lite": 2022, "magic v3": 2024, "50 lite": 2022, "10": 2018,

    # ZTE
    "a7": 2019, "blade a51": 2020, "v8 lite": 2016, "blade a35": 2019, "blade a55": 2021,
    "blade a506": 2019, "blade a31": 2018, "blade": 2019, "blade a75": 2024, "blade a35e": 2024,
    "blade a53 pro": 2023, "redmagic 7": 2022, "blade a72": 2020, "blade v60 vita": 2023,

    # TCL
    "tcl 30": 2022, "tcl 40 se": 2023, "tcl 30 se": 2023, "tcl 50 5g": 2022, "tcl 10 se": 2020,
    "tcl 50": 2021, "tcl 40 nxtpaper": 2023, "tcl 20r 5g": 2021, "tcl 20 5g": 2021,
    "tcl 20 pro 5g": 2022, "tcl 10 5g": 2021, "tcl 50 nxtpaper": 2022, "tcl 30e": 2021,
    "tcl 50 pro nxtpaper": 2022, "tcl 40r 5g": 2021, "tcl 30 5g": 2021, "tcl 20 se": 2020,
    "tcl 505": 2022, "tcl 306": 2022, "tcl 40 nxtpaper 5g": 2023, "tcl 408": 2023,
    "tcl 205": 2021, "tcl 50 se": 2022, "tcl 10l": 2020, "tcl 10 plus": 2020, "tcl 403": 2023,
    "tcl 60r 5g": 2022, "tcl none": 2023, "tcl 305": 2023, "tcl 20y": 2021, "tcl 40 xl": 2023,

    # Alcatel
    "alcatel 5v": 2018, "alcatel 1": 2021, "alcatel u5": 2020, "alcatel 1s (2021)": 2021,
    "alcatel 1se (2020)": 2020, "alcatel 1c (2019)": 2019, "alcatel 3": 2021, "alcatel 1x": 2021,
    "alcatel 1s": 2021, "alcatel 1 (2021)": 2021, "alcatel 1se": 2021, "alcatel 1b (2022)": 2022,
    "alcatel 3x (2020)": 2020, "alcatel 2001": 2001, "alcatel pixi 4 (6) 3g": 2016,
    "alcatel pop 7": 2014, "alcatel pixi 4": 2016, "alcatel 3088": 2019, "alcatel 2012": 2012,
    "alcatel pop 4": 2016, "alcatel 3x": 2020, "alcatel 1s (2020)": 2020, "alcatel pixi 4 (4)": 2016,
    "alcatel 1x (2019)": 2019, "alcatel 2052": 2014, "alcatel 1b (2020)": 2020,
    "alcatel one touch star": 2014, "alcatel 1l (2021)": 2021,

    # Fairphone
    "1": 2013, "5": 2022, "6": 2023, "3+": 2019,

    # Nothing Phone
    "nothing phone (2)": 2023, "nothing phone (3a) pro": 2024, "nothing phone (3a)": 2024,
    "nothing phone (1)": 2022, "nothing phone (2a)": 2024, "nothing phone (2a) plus": 2025,

    # Xiaomi/Redmi
    "redmi note 10s": 2021, "redmi note 10 pro": 2021, "redmi note 13 pro": 2024, "redmi 10a": 2022,
    "redmi 13": 2024, "redmi 9c": 2020, "redmi note 12 pro": 2022, "poco x6 pro": 2024,
    "redmi a3": 2023, "redmi note 14 pro": 2024, "redmi 12c": 2022, "redmi 12c 3gb 32gb": 2022,
    "redmi note 14": 2023, "redmi note 14 5g": 2024, "redmi 13c": 2023, "redmi a5": 2025,
    "redmi 12": 2022, "redmi note 12": 2022, "poco x4 pro 5g": 2022, "redmi 14c": 2025,
    "redmi note 14 pro 4g": 2024, "redmi note 14 4g": 2024, "redmi a5 4g": 2025,
    "redmi note 14c 4g": 2025, "redmi note 7": 2019, "redmi 10c": 2022, "11 lite 5g ne": 2021,
    "redmi note 11": 2022, "redmi note 13": 2023, "redmi 9t": 2021, "mi a3": 2019,
    "poco x3 pro": 2021, "redmi 9": 2020, "redmi note 9 pro": 2020, "redmi note 11 pro 5g": 2022,
    "mi 11 ultra": 2021, "mi 10 lite 5g": 2020, "14 ultra": 2024, "mi 11": 2021,
    "redmi 6": 2018, "poco x7 pro": 2024, "mi 11 lite": 2021, "redmi note 11s": 2022,
    "redmi a2": 2023, "mi a2": 2018, "redmi note 11 pro": 2022, "redmi 10 5g": 2022,
    "poco c65": 2023, "redmi 9a": 2020, "redmi note 4": 2017, "redmi note 12 pro plus": 2022,
    "mi 9": 2019, "12t": 2022, "mix flip": 2024, "poco x7": 2024, "mi 9t": 2019,
    "redmi note 8 pro": 2019, "poco f3": 2021, "redmi note 12s": 2023, "redmi 10": 2021,
    "poco f5": 2023, "redmi note 9": 2020, "mi 8 lite": 2018, "poco c75": 2024,
    "redmi note 13 pro plus": 2023, "poco f2 pro": 2020, "15 ultra": 2025, "mi 10t lite 5g": 2020,
    "redmi note 10": 2021, "redmi note 8t": 2019, "11i": 2022, "redmi 2": 2015,
    "redmi note 9s": 2020, "poco x3": 2020, "mi a1": 2017, "redmi 13c 5g": 2024,
    "redmi note 14 pro plus 5g": 2024, "redmi note 8": 2019, "poco x5 pro": 2023,
    "redmi 8": 2019, "mi a2 lite": 2018, "redmi 8a": 2019, "14t pro": 2024, "mi 10t 5g": 2020,
    "redmi 7": 2019, "redmi 7a": 2019, "poco m4 pro": 2021, "redmi note 11t 5g": 2021,
    "redmi note 11 pro plus 5g": 2021, "mi 6": 2017, "redmi note 10 5g": 2021,
    "poco m6": 2023, "redmi s2": 2018, "redmi note 10t 5g": 2021, "moto g15": 2024,
    "moto g35": 2024, "moto g55": 2024, "moto g04s": 2024, "moto g54": 2023, "moto g85": 2024,
    "moto g24": 2024, "edge 40 neo": 2023, "moto g14": 2023, "edge 30": 2022, "edge 40": 2023,
    "moto g34": 2024, "moto g": 2013, "edge 30 fusion": 2022, "moto e5": 2018,
    "mi note 10 pro": 2019, "redmi a1": 2022, "poco f7": 2025, "mi 10t pro 5g": 2020,
    "redmi note 6 pro": 2018, "redmi 5 plus": 2017, "13 lite": 2023, "poco m7 pro 5g": 2023,
    "12 lite": 2022, "mi 11 lite 5g": 2021, "poco m5s": 2022, "mi 8": 2018, "poco f6": 2023,
    "mi 10 5g": 2020, "galaxy j3": 2016
}

marcas = ['Selecciona una opción...'] + list(marcas_modelos.keys())
provincias = ['Selecciona una opción...', 'alava', 'albacete', 'alicante', 'almeria', 'asturias', 'avila', 'badajoz', 'barcelona', 'burgos', 'caceres', 'cadiz', 'cantabria', 'castellon', 'ceuta', 'ciudad real', 'cordoba', 'cuenca', 'girona', 'granada', 'guadalajara', 'guipuzcoa', 'huelva', 'huesca', 'islas baleares', 'jaen', 'la coruña', 'la rioja', 'las palmas', 'leon', 'lleida', 'lugo', 'madrid', 'malaga', 'melilla', 'murcia', 'navarra', 'ourense', 'palencia', 'pontevedra', 'salamanca', 'santa cruz de tenerife', 'segovia', 'sevilla', 'soria', 'tarragona', 'teruel', 'toledo', 'valencia', 'valladolid', 'vizcaya', 'zamora', 'zaragoza']
colores = ['Selecciona una opción...', 'negro', 'azul', 'gris', 'blanco', 'dorado', 'morado', 'plateado', 'verde', 'rosa', 'naranja', 'beige', 'amarillo', 'rojo', 'marrón', 'coral', 'multicolor']
capacidades = ['Selecciona una opción...', 1.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0]

# Sección de características principales
st.markdown("""
<div class="section-header">
    📋 Formulario de Predicción
</div>
""", unsafe_allow_html=True)

# Contenedor del formulario con diseño mejorado
with st.container():
    st.markdown("""
    <div class="form-container">
    """, unsafe_allow_html=True)
    
    # Inicializar session_state si no existe
    if 'marca_seleccionada' not in st.session_state:
        st.session_state.marca_seleccionada = 'Selecciona una opción...'
    
    # Sección de selección de marca y modelo (fuera del formulario)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏷️ **Información del Dispositivo**")
        marca = st.selectbox("📱 Marca", marcas, key="marca_select")
        
        # Filtrar modelos según la marca seleccionada
        if marca != 'Selecciona una opción...':
            modelos_disponibles = ['Selecciona una opción...'] + marcas_modelos.get(str(marca), [])
            modelo_agrupado = st.selectbox("📱 Modelo", modelos_disponibles, key="modelo_select")
            
            # Filtrar años según el modelo específico seleccionado
            if modelo_agrupado != 'Selecciona una opción...':
                # Buscar el año específico del modelo
                año_modelo = modelo_año_lanzamiento.get(str(modelo_agrupado))
                if año_modelo:
                    # Si el modelo tiene un año específico, solo mostrar ese año
                    año_lanzamiento = st.selectbox("📅 Año de lanzamiento", [año_modelo], key="año_select", disabled=True)
                    st.info(f"✅ Año automático: {año_modelo} (específico para este modelo)")
                else:
                    # Si no se encuentra el año específico, mostrar años generales de la marca
                    años_generales = list(range(2015, 2026))
                    año_lanzamiento = st.selectbox("📅 Año de lanzamiento", ['Selecciona una opción...'] + años_generales, key="año_select")
                    st.warning("⚠️ Año no encontrado en la base de datos. Selecciona manualmente.")
            else:
                año_lanzamiento = st.selectbox("📅 Año de lanzamiento", ['Selecciona un modelo primero...'], key="año_select_disabled", disabled=True)
        else:
            modelo_agrupado = st.selectbox("📱 Modelo", ['Selecciona una marca primero...'], key="modelo_select_disabled", disabled=True)
            año_lanzamiento = st.selectbox("📅 Año de lanzamiento", ['Selecciona una marca primero...'], key="año_select_disabled", disabled=True)
    
    with col2:
        st.markdown("#### 🎨 **Características Físicas**")
        provincia = st.selectbox("📍 Provincia", provincias, key="provincia_select")
        color = st.selectbox("🎨 Color", colores, key="color_select")
        capacidad = st.selectbox("💾 Capacidad (GB)", capacidades, key="capacidad_select")
        estado = st.selectbox("⭐ Estado del dispositivo", todos_estados, key="estado_select")

    # Formulario principal (solo con el botón)
    with st.form("form_prediccion"):
        submitted = st.form_submit_button("🚀 Predecir Precio")
    
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    # Validar que todos los campos estén completados
    campos_requeridos = [marca, provincia, modelo_agrupado, color, capacidad, estado, año_lanzamiento]
    campos_vacios = [campo for campo in campos_requeridos if campo == 'Selecciona una opción...' or campo == 'Selecciona una marca primero...']
    
    if campos_vacios:
        st.error("❌ Por favor, completa todos los campos antes de hacer la predicción.")
    else:
        # Calcular antigüedad
        año_actual = datetime.now().year
        if isinstance(año_lanzamiento, (int, str)) and str(año_lanzamiento).isdigit():
            antigüedad = año_actual - int(año_lanzamiento)
        else:
            antigüedad = 0  # Valor por defecto si no es válido
        
        # Construir el DataFrame de entrada (igual que en el entrenamiento)
        datos_usuario = {
            "marca": marca,
            "provincia": provincia,
            "modelo_agrupado": modelo_agrupado,
            "color": color,
            "estado_codificada": estado_dict[str(estado)],
            "año de lanzamiento": año_lanzamiento,
            "antigüedad": antigüedad,
            "capacidad_num": capacidad
        }

        df_usuario = pd.DataFrame([datos_usuario])

        # Codificar variables categóricas (igual que en el entrenamiento)
        cols_cat = ["marca", "provincia", "modelo_agrupado", "color"]
        encoded_user = encoder.transform(df_usuario[cols_cat])
        df_encoded = pd.DataFrame(encoded_user, columns=encoder.get_feature_names_out(cols_cat))

        # Unir con variables numéricas (igual que en el entrenamiento)
        df_numericas = df_usuario[['estado_codificada', 'año de lanzamiento', 'antigüedad', 'capacidad_num']]
        df_final = pd.concat([df_numericas, df_encoded], axis=1)

        # Alinear columnas con las del modelo (importante para que no falle)
        try:
            columnas_modelo = modelo.get_booster().feature_names
            df_final = df_final.reindex(columns=columnas_modelo, fill_value=0)
        except Exception as e:
            st.error(f"❌ Error al procesar los datos: {str(e)}")
            st.stop()

        # Predecir
        try:
            pred = modelo.predict(df_final)[0]
            
            # Resultado principal con diseño mejorado
            st.markdown("""
            <div class="metric-card">
                <h2 style="margin: 0; font-size: 2rem;">💰 Precio Estimado</h2>
                <h1 style="margin: 0.5rem 0; font-size: 3.5rem; font-weight: bold;">{:.0f} €</h1>
                <p style="margin: 0; opacity: 0.8;">Precio optimizado para el mercado actual</p>
            </div>
            """.format(pred), unsafe_allow_html=True)
            
            # Generar consejos de venta
            consejos = generar_consejos_venta_ia(
                marca=marca,
                modelo=modelo_agrupado,
                estado=estado,
                año_lanzamiento=año_lanzamiento,
                capacidad=capacidad,
                color=color,
                provincia=provincia,
                precio_predicho=pred
            )
            
            # Resumen de la predicción con diseño mejorado
            st.markdown("""
            <div class="info-card">
                <h3 style="margin: 0 0 1rem 0; text-align: center;">📱 Resumen de la Predicción</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div><strong>🏷️ Marca:</strong> {}</div>
                    <div><strong>📱 Modelo:</strong> {}</div>
                    <div><strong>⭐ Estado:</strong> {}</div>
                    <div><strong>📅 Año:</strong> {}</div>
                    <div><strong>💾 Capacidad:</strong> {} GB</div>
                    <div><strong>🎨 Color:</strong> {}</div>
                    <div><strong>📍 Provincia:</strong> {}</div>
                    <div><strong>📊 Antigüedad:</strong> {} años</div>
                </div>
            </div>
            """.format(marca, modelo_agrupado, estado, año_lanzamiento, capacidad, color, provincia, antigüedad), unsafe_allow_html=True)

            # Sección de consejos de venta mejorada
            st.markdown("""
            <div class="section-header">
                🤖 Consejos de Venta Inteligentes
            </div>
            """, unsafe_allow_html=True)
            

            
            # Generar consejos
            with st.spinner("🤖 Generando consejos inteligentes..."):
                consejos = generar_consejos_venta_ia(
                    marca=marca,
                    modelo=modelo_agrupado,
                    estado=estado,
                    año_lanzamiento=año_lanzamiento,
                    capacidad=capacidad,
                    color=color,
                    provincia=provincia,
                    precio_predicho=pred
                )
            
            # Crear columnas para mejor organización
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💰 **Análisis de Precio**")
                st.metric("Precio Estimado", f"{pred:.2f} €")
                st.metric("Precio Óptimo", f"{consejos['precio_optimo']:.2f} €")
                
                diferencia = consejos['precio_optimo'] - pred
                if diferencia > 0:
                    st.success(f"📈 Puedes subir el precio hasta {diferencia:.2f} € más")
                elif diferencia < 0:
                    st.warning(f"📉 Considera bajar el precio {abs(diferencia):.2f} €")
                else:
                    st.info("✅ El precio está bien posicionado")
                
                st.markdown("#### 🎯 **Competitividad**")
                if consejos['factor_competitividad'] == "Alto":
                    st.success("🟢 Alta competitividad - Buen momento para vender")
                elif consejos['factor_competitividad'] == "Medio":
                    st.warning("🟡 Competitividad media - Revisa la competencia")
                else:
                    st.info("🔴 Baja competitividad - Considera ajustar el precio")
            
            with col2:
                st.markdown("#### 📱 **Fortalezas de la Marca**")
                for fortaleza in consejos['fortalezas_marca']:
                    st.write(f"✅ {fortaleza}")
                
                st.markdown("#### 🏆 **Plataformas Recomendadas**")
                for plataforma in consejos['plataformas_recomendadas']:
                    st.write(f"📱 {plataforma}")
            
            # Sección de consejos específicos
            st.markdown("---")
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### 💡 **Consejos para la Marca**")
                for consejo in consejos['consejos_marca']:
                    st.write(f"💡 {consejo}")
                
                st.markdown("#### 📊 **Análisis Técnico**")
                st.write(f"📅 **Antigüedad:** {consejos['consejo_antigüedad']}")
                st.write(f"💾 **Capacidad:** {consejos['consejo_capacidad']}")
            
            with col4:
                st.markdown("#### 🎯 **Consejos por Estado**")
                for consejo in consejos['consejos_estado']:
                    st.write(f"🎯 {consejo}")
                
                st.markdown("#### ⏰ **Momento Óptimo**")
                if antigüedad <= 2:
                    st.success("🟢 Excelente momento para vender")
                elif antigüedad <= 4:
                    st.warning("🟡 Buen momento, pero considera el precio")
                else:
                    st.info("🔴 Vender rápido antes de que pierda más valor")
            
            # Guardar datos en session_state para simulaciones
            st.session_state.datos_para_simulacion = {
                'datos_usuario': datos_usuario,
                'cols_cat': cols_cat,
                'columnas_modelo': columnas_modelo,
                'pred_original': pred
            }
            
            # Historial de predicciones
            st.markdown("---")
            st.subheader("📋 **Historial de Predicciones**")
            
            # Inicializar historial si no existe
            if 'historial_predicciones' not in st.session_state:
                st.session_state.historial_predicciones = []
            
            # Añadir predicción actual al historial
            prediccion_actual = {
                'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'marca': marca,
                'modelo': modelo_agrupado,
                'estado': estado,
                'capacidad': capacidad,
                'precio': pred,
                'precio_optimo': consejos['precio_optimo']
            }
            
            # Evitar duplicados
            if prediccion_actual not in st.session_state.historial_predicciones:
                st.session_state.historial_predicciones.append(prediccion_actual)
            
            # Mostrar historial
            if len(st.session_state.historial_predicciones) > 1:
                st.write("**Predicciones anteriores:**")
                for i, pred_hist in enumerate(st.session_state.historial_predicciones[-5:], 1):  # Últimas 5
                    st.write(f"{i}. {pred_hist['marca']} {pred_hist['modelo']} - {pred_hist['precio']:.2f}€ ({pred_hist['fecha']})")
                
                if st.button("🗑️ Limpiar Historial"):
                    st.session_state.historial_predicciones = []
                    st.rerun()
            else:
                st.info("Esta es tu primera predicción. El historial se irá guardando automáticamente.")

            # Guardar datos en session_state para el generador de posteo
            st.session_state.prediccion_realizada = True
            st.session_state.datos_prediccion = {
                'marca': marca,
                'modelo': modelo_agrupado,
                'estado': estado,
                'año_lanzamiento': año_lanzamiento,
                'capacidad': capacidad,
                'color': color,
                'provincia': provincia,
                'precio': pred
            }
            
        except Exception as e:
            st.error(f"❌ Error al hacer la predicción: {str(e)}")
            st.write("Esto puede deberse a que las columnas no coinciden con las del modelo entrenado.")

# Sección de comparador de precios (fuera del bloque if submitted)
if 'datos_para_simulacion' in st.session_state:
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        📊 Comparador de Precios Avanzado
    </div>
    """, unsafe_allow_html=True)
    st.write("Simula diferentes configuraciones para ver cómo cambia el precio:")
    
    # Obtener datos originales
    datos_originales = st.session_state.datos_para_simulacion['datos_usuario']
    
    # Crear formulario de simulación
    with st.form("form_simulacion"):
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.markdown("#### 🔄 **Variables a Simular**")
            
            # Estado
            estado_sim = st.selectbox(
                "⭐ Estado del dispositivo",
                list(estado_dict.keys()),
                index=list(estado_dict.keys()).index(datos_originales.get('estado', 'buen estado')),
                key="estado_sim"
            )
            
            # Capacidad
            capacidad_sim = st.selectbox(
                "💾 Capacidad (GB)",
                [1.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0],
                index=[1.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0].index(datos_originales.get('capacidad_num', 64.0)),
                key="capacidad_sim"
            )
            
            # Color
            color_sim = st.selectbox(
                "🎨 Color",
                ['negro', 'azul', 'gris', 'blanco', 'dorado', 'morado', 'plateado', 'verde', 'rosa', 'naranja', 'beige', 'amarillo', 'rojo', 'marrón', 'coral', 'multicolor'],
                index=['negro', 'azul', 'gris', 'blanco', 'dorado', 'morado', 'plateado', 'verde', 'rosa', 'naranja', 'beige', 'amarillo', 'rojo', 'marrón', 'coral', 'multicolor'].index(datos_originales.get('color', 'negro')),
                key="color_sim"
            )
        
        with col_sim2:
            st.markdown("#### 📍 **Ubicación y Año**")
            
            # Provincia
            provincia_sim = st.selectbox(
                "📍 Provincia",
                provincias[1:],  # Excluir "Selecciona una opción..."
                index=provincias[1:].index(datos_originales.get('provincia', 'madrid')),
                key="provincia_sim"
            )
            
            # Año de lanzamiento
            año_original = datos_originales.get('año de lanzamiento', 2020)
            año_sim = st.selectbox(
                "📅 Año de lanzamiento",
                list(range(2015, 2025)),
                index=list(range(2015, 2025)).index(año_original) if año_original in range(2015, 2025) else 5,
                key="año_sim"
            )
            
            # Marca y Modelo (solo lectura para mostrar)
            st.markdown("#### 📱 **Dispositivo (No modificable)**")
            st.write(f"**Marca:** {datos_originales.get('marca', 'N/A')}")
            st.write(f"**Modelo:** {datos_originales.get('modelo_agrupado', 'N/A')}")
        
        # Botón de simulación
        submitted_sim = st.form_submit_button("🚀 Simular Precio")
    
    # Procesar simulación
    if submitted_sim:
        # Calcular antigüedad
        año_actual = datetime.now().year
        if año_sim is not None:
            antigüedad_sim = año_actual - int(año_sim)
        else:
            antigüedad_sim = 0
        
        # Crear datos de simulación
        datos_sim = {
            "marca": datos_originales['marca'],
            "provincia": provincia_sim,
            "modelo_agrupado": datos_originales['modelo_agrupado'],
            "color": color_sim,
            "estado_codificada": estado_dict[str(estado_sim)] if estado_sim else estado_dict['buen estado'],
            "año de lanzamiento": año_sim if año_sim is not None else 2020,
            "antigüedad": antigüedad_sim,
            "capacidad_num": capacidad_sim
        }
        
        # Procesar predicción
        try:
            df_sim = pd.DataFrame([datos_sim])
            cols_cat = ["marca", "provincia", "modelo_agrupado", "color"]
            encoded_sim = encoder.transform(df_sim[cols_cat])
            df_encoded_sim = pd.DataFrame(encoded_sim, columns=encoder.get_feature_names_out(cols_cat))
            df_numericas_sim = df_sim[['estado_codificada', 'año de lanzamiento', 'antigüedad', 'capacidad_num']]
            df_final_sim = pd.concat([df_numericas_sim, df_encoded_sim], axis=1)
            df_final_sim = df_final_sim.reindex(columns=st.session_state.datos_para_simulacion['columnas_modelo'], fill_value=0)
            
            pred_sim = modelo.predict(df_final_sim)[0]
            pred_original = st.session_state.datos_para_simulacion['pred_original']
            diferencia_sim = pred_sim - pred_original
            
            # Mostrar resultados con diseño mejorado
            st.markdown("""
            <div class="metric-card">
                <h2 style="margin: 0; font-size: 2rem;">💰 Resultado de la Simulación</h2>
                <h1 style="margin: 0.5rem 0; font-size: 3.5rem; font-weight: bold;">{:.0f} €</h1>
                <p style="margin: 0; opacity: 0.8;">Precio simulado con la nueva configuración</p>
            </div>
            """.format(pred_sim), unsafe_allow_html=True)
            
            # Comparación con precio original
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                st.markdown("#### 📊 **Comparación**")
                st.metric("Precio Original", f"{pred_original:.2f} €")
                st.metric("Precio Simulado", f"{pred_sim:.2f} €")
                
                if diferencia_sim > 0:
                    st.success(f"📈 **Incremento:** +{diferencia_sim:.2f} €")
                elif diferencia_sim < 0:
                    st.warning(f"📉 **Decremento:** {diferencia_sim:.2f} €")
                else:
                    st.info("✅ **Sin cambios**")
            
            with col_comp2:
                st.markdown("#### 🔍 **Análisis de Cambios**")
                
                # Mostrar qué cambió
                cambios = []
                if estado_sim != datos_originales.get('estado', 'buen estado'):
                    cambios.append(f"Estado: {datos_originales.get('estado', 'buen estado')} → {estado_sim}")
                
                if capacidad_sim != datos_originales.get('capacidad_num', 64.0):
                    cambios.append(f"Capacidad: {datos_originales.get('capacidad_num', 64.0)}GB → {capacidad_sim}GB")
                
                if color_sim != datos_originales.get('color', 'negro'):
                    cambios.append(f"Color: {datos_originales.get('color', 'negro')} → {color_sim}")
                
                if provincia_sim != datos_originales.get('provincia', 'madrid'):
                    cambios.append(f"Provincia: {datos_originales.get('provincia', 'madrid')} → {provincia_sim}")
                
                if año_sim != datos_originales.get('año de lanzamiento', 2020):
                    cambios.append(f"Año: {datos_originales.get('año de lanzamiento', 2020)} → {año_sim}")
                
                if cambios:
                    st.write("**Cambios realizados:**")
                    for cambio in cambios:
                        st.write(f"• {cambio}")
                else:
                    st.info("No se realizaron cambios")
                
                # Porcentaje de cambio
                if pred_original > 0:
                    porcentaje_cambio = (diferencia_sim / pred_original) * 100
                    st.metric("Cambio %", f"{porcentaje_cambio:+.1f}%")
            
            # Consejos basados en la simulación
            st.markdown("---")
            st.markdown("#### 💡 **Consejos de la Simulación**")
            
            if diferencia_sim > 50:
                st.success("🎯 **Excelente oportunidad:** Esta configuración puede aumentar significativamente el valor de tu dispositivo.")
            elif diferencia_sim > 20:
                st.info("📈 **Buena mejora:** Considera esta configuración para maximizar el precio de venta.")
            elif diferencia_sim < -50:
                st.warning("⚠️ **Atención:** Esta configuración reduce significativamente el valor. Considera otras opciones.")
            elif diferencia_sim < -20:
                st.info("📉 **Precio menor:** Esta configuración reduce el valor, pero puede ser más fácil de vender.")
            else:
                st.info("⚖️ **Precio equilibrado:** Esta configuración mantiene un precio similar al original.")
                
        except Exception as e:
            st.error(f"❌ Error en la simulación: {str(e)}")
    
    # Botones de simulación rápida
    st.markdown("---")
    st.markdown("#### ⚡ **Simulaciones Rápidas**")
    st.write("Prueba configuraciones comunes:")
    
    col_rap1, col_rap2, col_rap3 = st.columns(3)
    
    with col_rap1:
        if st.button("🏆 Simular 'Como Nuevo'", key="rap_estado"):
            datos_sim = datos_originales.copy()
            datos_sim['estado_codificada'] = estado_dict['como nuevo']
            
            df_sim = pd.DataFrame([datos_sim])
            encoded_sim = encoder.transform(df_sim[st.session_state.datos_para_simulacion['cols_cat']])
            df_encoded_sim = pd.DataFrame(encoded_sim, columns=encoder.get_feature_names_out(st.session_state.datos_para_simulacion['cols_cat']))
            df_numericas_sim = df_sim[['estado_codificada', 'año de lanzamiento', 'antigüedad', 'capacidad_num']]
            df_final_sim = pd.concat([df_numericas_sim, df_encoded_sim], axis=1)
            df_final_sim = df_final_sim.reindex(columns=st.session_state.datos_para_simulacion['columnas_modelo'], fill_value=0)
            
            pred_sim = modelo.predict(df_final_sim)[0]
            diferencia_sim = pred_sim - st.session_state.datos_para_simulacion['pred_original']
            st.metric("Precio 'Como Nuevo'", f"{pred_sim:.2f} €", f"{diferencia_sim:+.2f} €")
    
    with col_rap2:
        if st.button("💾 Simular 256GB", key="rap_capacidad"):
            datos_sim = datos_originales.copy()
            datos_sim['capacidad_num'] = 256.0
            
            df_sim = pd.DataFrame([datos_sim])
            encoded_sim = encoder.transform(df_sim[st.session_state.datos_para_simulacion['cols_cat']])
            df_encoded_sim = pd.DataFrame(encoded_sim, columns=encoder.get_feature_names_out(st.session_state.datos_para_simulacion['cols_cat']))
            df_numericas_sim = df_sim[['estado_codificada', 'año de lanzamiento', 'antigüedad', 'capacidad_num']]
            df_final_sim = pd.concat([df_numericas_sim, df_encoded_sim], axis=1)
            df_final_sim = df_final_sim.reindex(columns=st.session_state.datos_para_simulacion['columnas_modelo'], fill_value=0)
            
            pred_sim = modelo.predict(df_final_sim)[0]
            diferencia_sim = pred_sim - st.session_state.datos_para_simulacion['pred_original']
            st.metric("Precio 256GB", f"{pred_sim:.2f} €", f"{diferencia_sim:+.2f} €")
    
    with col_rap3:
        if st.button("📍 Simular Madrid", key="rap_provincia"):
            datos_sim = datos_originales.copy()
            datos_sim['provincia'] = 'madrid'
            
            df_sim = pd.DataFrame([datos_sim])
            encoded_sim = encoder.transform(df_sim[st.session_state.datos_para_simulacion['cols_cat']])
            df_encoded_sim = pd.DataFrame(encoded_sim, columns=encoder.get_feature_names_out(st.session_state.datos_para_simulacion['cols_cat']))
            df_numericas_sim = df_sim[['estado_codificada', 'año de lanzamiento', 'antigüedad', 'capacidad_num']]
            df_final_sim = pd.concat([df_numericas_sim, df_encoded_sim], axis=1)
            df_final_sim = df_final_sim.reindex(columns=st.session_state.datos_para_simulacion['columnas_modelo'], fill_value=0)
            
            pred_sim = modelo.predict(df_final_sim)[0]
            diferencia_sim = pred_sim - st.session_state.datos_para_simulacion['pred_original']
            st.metric("Precio en Madrid", f"{pred_sim:.2f} €", f"{diferencia_sim:+.2f} €")

# Generador de posteo para segunda mano (fuera del formulario)
if 'prediccion_realizada' in st.session_state and st.session_state.prediccion_realizada:
    st.markdown("---")
    st.subheader("📝 **Generador de Posteo para Segunda Mano**")
    
    datos = st.session_state.datos_prediccion
    
    # Seleccionar plataforma
    plataforma = st.selectbox(
        "Selecciona la plataforma:",
        ["Wallapop", "Milanuncios", "Vibbo", "Facebook Marketplace", "Instagram", "General"]
    )
    
    if st.button("🔄 Generar Posteo"):
        # Generar consejos de venta para el posteo
        consejos_posteo = generar_consejos_venta_ia(
            marca=datos['marca'],
            modelo=datos['modelo'],
            estado=datos['estado'],
            año_lanzamiento=datos['año_lanzamiento'],
            capacidad=datos['capacidad'],
            color=datos['color'],
            provincia=datos['provincia'],
            precio_predicho=datos['precio']
        )

        # Formatear precio
        precio_formateado = f"{datos['precio']:.0f}"
        
        # Obtener valores seguros
        marcas_amigables = {
            'apple': 'iPhone',
            'samsung': 'Samsung Galaxy',
            'xiaomi': 'Xiaomi',
            'oppo': 'OPPO',
            'oneplus': 'OnePlus',
            'realme': 'Realme',
            'motorola': 'Motorola',
            'alcatel': 'Alcatel',
            'tcl': 'TCL',
            'nothing phone': 'Nothing Phone',
            'sony': 'Sony Xperia',
            'google': 'Google Pixel',
            'honor': 'Honor',
            'huawei': 'Huawei',
            'vivo': 'Vivo',
            'asus': 'Asus',
            'fairphone': 'Fairphone',
            'nokia': 'Nokia',
            'zte': 'ZTE'
        }
        marca_amigable = marcas_amigables.get(str(datos['marca']), str(datos['marca']))
        modelo_str = str(datos['modelo']) if datos['modelo'] else "Modelo"
        estado_amigable = consejos_posteo['consejos_estado'][0] # Tomar el primer consejo de estado
        color_str = str(datos['color']) if datos['color'] else "Color"
        provincia_str = str(datos['provincia']) if datos['provincia'] else "Ubicación"
        
        # Generar contenido según plataforma
        if plataforma == "Wallapop":
            titulo = f"📱 {marca_amigable} {modelo_str} - {estado_amigable}"
            descripcion = f"""
¡Hola! Vendo mi {marca_amigable} {modelo_str} en {estado_amigable.lower()}.

📱 **Detalles:**
• Año: {datos['año_lanzamiento']}
• Capacidad: {datos['capacidad']} GB
• Color: {color_str}
• Ubicación: {provincia_str}

💰 **Precio:** {precio_formateado}€

✅ Perfecto funcionamiento
✅ Envío disponible a toda España
✅ Negociable

📞 Contacto por WhatsApp
📍 {provincia_str}

#wallapop #movil #smartphone #venta
"""
        
        elif plataforma == "Milanuncios":
            titulo = f"iPhone {modelo_str}" if datos['marca'] == 'apple' else f"{marca_amigable} {modelo_str}"
            descripcion = f"""
Vendo {marca_amigable} {modelo_str} en {estado_amigable.lower()}.

**Características técnicas:**
• Año de lanzamiento: {datos['año_lanzamiento']}
• Almacenamiento: {datos['capacidad']} GB
• Color: {color_str}
• Estado: {estado_amigable}

**Precio:** {precio_formateado}€

**Garantías:**
• Funcionamiento perfecto
• Sin averías
• Cargador original incluido

**Ubicación:** {provincia_str}
**Contacto:** Llama o WhatsApp

¡Seriedad garantizada!
"""
        
        elif plataforma == "Facebook Marketplace":
            titulo = f"📱 {marca_amigable} {modelo_str} - {precio_formateado}€"
            descripcion = f"""
¡Hola! Vendo mi {marca_amigable} {modelo_str} en {estado_amigable.lower()}.

📱 **Especificaciones:**
• Año: {datos['año_lanzamiento']}
• Capacidad: {datos['capacidad']} GB
• Color: {color_str}
• Ubicación: {provincia_str}

💰 **Precio:** {precio_formateado}€

✅ Funciona perfectamente
✅ Envío disponible
✅ Precio negociable

📞 Contacto por mensaje privado
📍 {provincia_str}

¡Gracias por tu interés!
"""
        
        elif plataforma == "Instagram":
            titulo = f"📱 {marca_amigable} {modelo_str}"
            descripcion = f"""
📱 {marca_amigable} {modelo_str}

📋 **Info:**
• Estado: {estado_amigable}
• Año: {datos['año_lanzamiento']}
• Capacidad: {datos['capacidad']} GB
• Color: {color_str}
• Ubicación: {provincia_str}

💰 **Precio:** {precio_formateado}€

✅ Perfecto estado
✅ Envío disponible
✅ Negociable

📸 Más fotos en mi perfil
📞 DM para info

#segundamano #movil #smartphone #venta #tecnologia
"""
        
        elif plataforma == "Vibbo":
            titulo = f"📱 {marca_amigable} {modelo_str}"
            descripcion = f"""
Vendo {marca_amigable} {modelo_str} en {estado_amigable.lower()}.

**Características:**
• Año: {datos['año_lanzamiento']}
• Capacidad: {datos['capacidad']} GB
• Color: {color_str}
• Ubicación: {provincia_str}

**Precio:** {precio_formateado}€

**Garantías:**
• Funcionamiento perfecto
• Sin problemas
• Envío disponible

**Contacto:** Mensaje privado
**Ubicación:** {provincia_str}

¡Seriedad garantizada!
"""
        
        else:  # General
            titulo = f"📱 {marca_amigable} {modelo_str}"
            descripcion = f"""
Vendo {marca_amigable} {modelo_str} en {estado_amigable.lower()}.

📋 **Características:**
• Estado: {estado_amigable}
• Año: {datos['año_lanzamiento']}
• Capacidad: {datos['capacidad']} GB
• Color: {color_str}
• Ubicación: {provincia_str}

💰 **Precio:** {precio_formateado}€

✅ **Garantía de funcionamiento**
✅ **Envío disponible**
✅ **Negociable**

📞 **Contacto:** [Tu número de teléfono]
📍 **Ubicación:** {provincia_str}

#segundamano #movil #smartphone #tecnologia #venta
"""
        
        posteo = f"{titulo}\n\n{descripcion}"
        
        st.markdown("### 📋 **Posteo Generado:**")
        st.text_area("Copia y pega este texto:", posteo, height=300)
        
        # Botones para copiar
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copiar al Portapapeles"):
                st.write("✅ Posteo copiado al portapapeles")
        with col2:
            if st.button("📱 Generar Nuevo Posteo"):
                st.rerun()

# Insights del mercado (solo se muestra después de una predicción)
if 'prediccion_realizada' in st.session_state and st.session_state.prediccion_realizada:
    st.markdown("""
    <div class="info-card">
        <h3 style="margin: 0 0 1rem 0; text-align: center;">💡 Insights del Mercado</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div>
                <h4>🏆 Mejores Oportunidades</h4>
                <ul>
                    <li>Apple: Alta demanda, precios premium</li>
                    <li>Samsung: Tendencia al alza</li>
                    <li>Google: Estable, buena calidad</li>
                </ul>
            </div>
            <div>
                <h4>📈 Tendencias Actuales</h4>
                <ul>
                    <li>Precios en aumento general</li>
                    <li>Demanda alta en marcas premium</li>
                    <li>Madrid y Barcelona: precios más altos</li>
                </ul>
            </div>
            <div>
                <h4>🎯 Estrategias Recomendadas</h4>
                <ul>
                    <li>Enfócate en marcas con alta demanda</li>
                    <li>Considera ubicaciones premium</li>
                    <li>Monitorea tendencias mensuales</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer elegante
st.markdown("""
<div style="
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-top: 3rem;
    text-align: center;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
">
    <h3 style="margin: 0 0 1rem 0;">🚀 SMARTCELL - Tu Asistente de Precios</h3>
    <p style="margin: 0; opacity: 0.9;">
        Desarrollado con ❤️ para el mercado de móviles de segunda mano en España
    </p>
    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
        🤖 IA Inteligente • 💰 Precios Óptimos • 📊 Análisis Avanzado • 📝 Posteos Profesionales
    </div>
</div>
""", unsafe_allow_html=True)
