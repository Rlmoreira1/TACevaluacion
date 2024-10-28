import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF para extraer imágenes de PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import textwrap
import os
import streamlit as st

web: streamlit run app.py --server.port $PORT
# Función para cargar observaciones desde Excel
def cargar_observaciones(ruta_archivo):
    df = pd.read_excel(ruta_archivo, engine='openpyxl')
    return df['Observaciones'].tolist()

# Función para extraer nombres de estudiantes y niveles desde los PDFs
def obtener_estudiantes_y_niveles(carpeta_pdfs):
    estudiantes_por_nivel = {}
    for nivel in os.listdir(carpeta_pdfs):
        ruta_nivel = os.path.join(carpeta_pdfs, nivel)
        if os.path.isdir(ruta_nivel):
            estudiantes = []
            for estudiante_carpeta in os.listdir(ruta_nivel):
                ruta_estudiante = os.path.join(ruta_nivel, estudiante_carpeta)
                if os.path.isdir(ruta_estudiante):
                    archivos = os.listdir(ruta_estudiante)
                    for archivo in archivos:
                        ruta_archivo = os.path.join(ruta_estudiante, archivo)
                        if archivo.endswith('.pdf'):
                            nombre_estudiante = estudiante_carpeta
                            estudiantes.append(nombre_estudiante)
                            break
            if estudiantes:
                estudiantes_por_nivel[nivel] = estudiantes
    return estudiantes_por_nivel

# Función para generar imágenes desde PDFs
def extraer_imagenes_de_pdfs(carpeta_pdfs, carpeta_imagenes):
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
    
    for nivel in os.listdir(carpeta_pdfs):
        ruta_nivel = os.path.join(carpeta_pdfs, nivel)
        if os.path.isdir(ruta_nivel):
            for estudiante_carpeta in os.listdir(ruta_nivel):
                ruta_estudiante = os.path.join(ruta_nivel, estudiante_carpeta)
                if os.path.isdir(ruta_estudiante):
                    archivos = os.listdir(ruta_estudiante)
                    for archivo in archivos:
                        ruta_pdf = os.path.join(ruta_estudiante, archivo)
                        if archivo.endswith('.pdf'):
                            try:
                                documento = fitz.open(ruta_pdf)
                                for pagina_num, pagina in enumerate(documento, start=1):
                                    imagen = pagina.get_pixmap()
                                    nombre_imagen = f"{nivel}_{estudiante_carpeta}_pagina_{pagina_num}.jpg"
                                    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
                                    imagen.save(ruta_imagen)
                                documento.close()
                                break
                            except Exception as e:
                                st.error(f"Error al procesar {archivo} en {ruta_estudiante}")

# Función para generar el PDF final con las observaciones, calificación y logo
def generar_pdf_completo(estudiante, nivel, observaciones, calificacion, imagenes, logo_path):
    # Crear la carpeta 'evaluaciones' en la misma ubicación del script si no existe
    carpeta_evaluaciones = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evaluaciones')
    if not os.path.exists(carpeta_evaluaciones):
        os.makedirs(carpeta_evaluaciones)

    # Definir la ruta del PDF
    nombre_pdf = os.path.join(carpeta_evaluaciones, f"{nivel}_{estudiante}_evaluacion.pdf")
    c = canvas.Canvas(nombre_pdf, pagesize=letter)
    c.setTitle(f"Evaluación para {estudiante}")

    # Establecer márgenes de 2.5 cm
    margen_izquierdo = 2.5 * cm
    margen_derecho = 2.5 * cm
    ancho_pagina, alto_pagina = letter

    # Ancho útil de la página después de aplicar los márgenes
    ancho_util = ancho_pagina - margen_izquierdo - margen_derecho

    # Añadir el logo en la parte superior si se proporciona
    if logo_path and os.path.exists(logo_path):
        logo_ancho = 3 * cm
        logo_alto = 3 * cm
        c.drawImage(logo_path, margen_izquierdo, alto_pagina - logo_alto - 1 * cm, width=logo_ancho, height=logo_alto)

    # Ajustar el texto para que se respete el ancho útil
    texto_evaluacion = f"Evaluación para {estudiante} en el nivel {nivel}."
    lineas_texto = textwrap.wrap(texto_evaluacion, width=70)

    # Añadir el texto ajustado
    c.setFont("Helvetica", 12)
    y_position = alto_pagina - 7 * cm
    for linea in lineas_texto:
        c.drawString(margen_izquierdo, y_position, linea)
        y_position -= 15

    # Añadir la calificación y las observaciones
    c.drawString(margen_izquierdo, y_position, f"Calificación: {calificacion}")
    y_position -= 20
    c.drawString(margen_izquierdo, y_position, "Observaciones:")
    y_position -= 15

    # Añadir las observaciones con márgenes
    for obs in observaciones:
        c.drawString(margen_izquierdo, y_position, f"- {obs}")
        y_position -= 20
        if y_position < 50:
            c.showPage()
            y_position = alto_pagina - 2.5 * cm

    # Añadir las imágenes de los trabajos con márgenes
    for imagen in imagenes:
        c.showPage()
        c.drawImage(
            imagen,
            margen_izquierdo,
            100,
            width=ancho_util,
            height=alto_pagina - 200,
            preserveAspectRatio=True,
            anchor='c'
        )

    c.save()
    st.success(f"PDF generado para {estudiante} en {nombre_pdf}")

# Interfaz de la aplicación en Streamlit
st.title("Evaluación de Estudiantes - Proceso Completo")

# Ruta fija para el logo
logo_path = "D:/TALLER D 2024/APLICACION WEB TAC/logo.png"

# Cargar las observaciones desde el archivo
ruta_archivo = 'observaciones.xlsx'
observaciones_iniciales = cargar_observaciones(ruta_archivo)

# Selección de la carpeta de PDFs
carpeta_pdfs = st.text_input("Introduce la ruta de la carpeta que contiene los PDFs:", key="carpeta_pdfs")
carpeta_imagenes = 'imagenes_extraidas'

# Almacenamiento del estado de los datos seleccionados
if 'estado' not in st.session_state:
    st.session_state.estado = {
        'nivel': None,
        'estudiante': None,
        'observaciones': [],
        'calificacion': '',
    }

# Obtener estudiantes y niveles si se proporciona la carpeta
if carpeta_pdfs:
    if os.path.exists(carpeta_pdfs):
        estudiantes_por_nivel = obtener_estudiantes_y_niveles(carpeta_pdfs)
        if estudiantes_por_nivel:
            st.session_state.estado['nivel'] = st.selectbox("Selecciona el nivel:", list(estudiantes_por_nivel.keys()))

            if st.session_state.estado['nivel']:
                estudiantes = estudiantes_por_nivel[st.session_state.estado['nivel']]
                st.session_state.estado['estudiante'] = st.selectbox("Selecciona el estudiante:", estudiantes)

# Generar imágenes desde PDFs
if st.button("Generar imágenes desde PDFs"):
    if carpeta_pdfs:
        extraer_imagenes_de_pdfs(carpeta_pdfs, carpeta_imagenes)
        st.success("Imágenes generadas correctamente desde los PDFs.")
    else:
        st.error("Por favor, introduce una ruta válida para la carpeta de PDFs.")

# Mostrar imágenes en un panel expandible si se selecciona un estudiante
if st.session_state.estado['estudiante']:
    imagenes_disponibles = [img for img in os.listdir(carpeta_imagenes) if st.session_state.estado['estudiante'] in img and st.session_state.estado['nivel'] in img]
    if imagenes_disponibles:
        with st.expander("Ver imágenes del trabajo"):
            for imagen in imagenes_disponibles:
                st.image(os.path.join(carpeta_imagenes, imagen), caption=imagen)

# Selección de observaciones
st.session_state.estado['observaciones'] = st.multiselect(
    "Selecciona las observaciones que correspondan:",
    observaciones_iniciales,
    key="observaciones"
)

# Añadir una observación adicional
nueva_observacion = st.text_input("Añadir una observación adicional:")
if nueva_observacion:
    st.session_state.estado['observaciones'].append(nueva_observacion)

# Selección de la calificación
st.session_state.estado['calificacion'] = st.text_input("Introduce la calificación del estudiante:")

# Botón para generar el PDF final
# Botón para generar el PDF final
if st.button("Generar PDF de evaluación"):
    if (st.session_state.estado['observaciones'] and 
        imagenes_disponibles and 
        st.session_state.estado['calificacion'] and 
        st.session_state.estado['estudiante'] and 
        st.session_state.estado['nivel']):
        
        imagenes_caminos = [os.path.join(carpeta_imagenes, img) for img in imagenes_disponibles]
        generar_pdf_completo(
            st.session_state.estado['estudiante'],
            st.session_state.estado['nivel'],
            st.session_state.estado['observaciones'],
            st.session_state.estado['calificacion'],
            imagenes_caminos,
            logo_path
        )

