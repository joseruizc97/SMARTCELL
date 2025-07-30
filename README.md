# 📱 SMARTCELL - Predicción de Precios de Móviles

## 🎯 Descripción del Proyecto

**SMARTCELL** es una aplicación de Machine Learning que predice precios de móviles usados en el mercado español. Utiliza datos reales de Wallapop para entrenar un modelo XGBoost que proporciona estimaciones precisas de precios basadas en características como marca, modelo, estado, capacidad y ubicación.

## ✨ Características Principales

- 🎯 **Predicción de precios** con alta precisión
- 📊 **Análisis de mercado** por marca y modelo
- 💡 **Consejos inteligentes** de venta personalizados
- 🎨 **Interfaz moderna** con Streamlit
- 📱 **Responsive design** para cualquier dispositivo
- 🔍 **Validación de datos** robusta

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Streamlit** - Interfaz web
- **XGBoost** - Modelo de Machine Learning
- **Pandas** - Manipulación de datos
- **Scikit-learn** - Preprocesamiento y encoding
- **Joblib** - Serialización de modelos

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/smartcell.git
cd smartcell
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run app_3.0.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 🚀 Uso de la Aplicación

### 1. Selección de Características
- **Marca**: Selecciona la marca del móvil
- **Modelo**: Elige el modelo específico
- **Año de lanzamiento**: Se determina automáticamente según el modelo
- **Estado**: Condición del dispositivo (nuevo, como nuevo, buen estado, aceptable)
- **Capacidad**: Almacenamiento en GB
- **Color**: Color del dispositivo
- **Provincia**: Ubicación geográfica

### 2. Predicción
- Haz clic en "🚀 Predecir Precio"
- Recibe el precio estimado
- Obtén consejos personalizados de venta
- Visualiza insights del mercado

## 📁 Estructura del Proyecto

```
smartcell/
├── README.md                    # Documentación principal
├── requirements.txt             # Dependencias del proyecto
├── app_3.0.py                   # Aplicación principal Streamlit
├── modelo_precio_movil_xgb.pkl  # Modelo entrenado
├── encoder_categorias.pkl       # Encoder para variables categóricas
├── notebooks/                   # Jupyter notebooks de análisis
│   ├── LIMPIEZA DATOS.ipynb     # Limpieza y preprocesamiento
│   ├── ANALISIS EDA.ipynb       # Análisis exploratorio de datos
│   └── MODELADO.ipynb           # Entrenamiento del modelo
├── data/                        # Datasets
│   ├── df_final.csv             # Dataset final procesado
│   └── datos_wallapop_limpieza_final.csv  # Datos originales limpios
└── docs/                        # Documentación adicional
    └── informe_eda.html         # Informe de análisis exploratorio
```

## 📊 Dataset

El modelo está entrenado con **7,877 registros** de móviles usados extraídos de Wallapop, incluyendo:

- **19 marcas** principales (Apple, Samsung, Xiaomi, etc.)
- **400+ modelos** con años de lanzamiento específicos
- **52 provincias** españolas
- **Múltiples estados** de conservación
- **Variedad de capacidades** y colores

## 🎯 Métricas del Modelo

- **R² Score**: 0.85+
- **RMSE**: < 50€
- **MAE**: < 35€
- **Validación cruzada**: 5-fold

## 🔧 Desarrollo

### Entrenamiento del modelo
```bash
# Ejecutar el notebook de modelado
jupyter notebook notebooks/MODELADO.ipynb
```

### Análisis de datos
```bash
# Ejecutar el notebook de limpieza
jupyter notebook notebooks/LIMPIEZA DATOS.ipynb

# Ejecutar el análisis exploratorio
jupyter notebook notebooks/ANALISIS EDA.ipynb
```

## 📈 Características del Modelo

### Variables de entrada:
- **Categóricas**: Marca, modelo, provincia, color
- **Numéricas**: Año de lanzamiento, antigüedad, capacidad, estado

### Feature Engineering:
- **Encoding**: One-Hot Encoding para variables categóricas
- **Normalización**: Variables numéricas escaladas
- **Agrupación**: Modelos similares agrupados

## 🤝 Contribuciones

Las contribuciones son bienvenidas. 

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Jose Antonio Ruiz Castillo** - Estudiante de Data Science ID Bootcamp

## 📞 Contacto

- **Email**: ruizcastillojoseantonio1@gmail.com
- **LinkedIn**: [https://www.linkedin.com/in/jose-antonio-ruiz-castillo/]
- **GitHub**: [@joseruizc97](https://github.com/joseruizc97)

---

⭐ **Si te gusta este proyecto, ¡dale una estrella en GitHub!** 