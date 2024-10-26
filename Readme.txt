README.txt - Evaluación de Trabajos de Estudiantes
Nombre de la Aplicación: Evaluación de Trabajos de Estudiantes
TAC - Taller D
Versión: 1.0

Descripción:
Esta aplicación permite la evaluación automática de trabajos enviados por estudiantes en formato PDF. La aplicación extrae imágenes de los trabajos, permite seleccionar observaciones para cada estudiante, y genera un informe en PDF con calificación, observaciones y un logo personalizado.

Requisitos del Sistema
Sistema Operativo: Windows 10 o superior (para otras plataformas, consulta al desarrollador).
Instalación
Descargar el Archivo Ejecutable:

Descarga el archivo ejecutable EvaluacionEstudiantes.exe desde la ubicación proporcionada.
Ejecución de la Aplicación:

Haz doble clic en EvaluacionEstudiantes.exe para iniciar la aplicación. La aplicación se abrirá en tu navegador predeterminado en la URL http://localhost:8501.
Uso de la Aplicación
Seleccionar la Carpeta de PDFs:

Introduce la ruta de la carpeta que contiene los trabajos de los estudiantes en formato PDF. La estructura de la carpeta debe estar organizada por niveles y subcarpetas con los nombres de los estudiantes.
Generar Imágenes:

Haz clic en el botón "Generar imágenes desde PDFs" para extraer imágenes de las páginas de los PDFs y guardarlas en la carpeta imagenes_extraidas.
Visualizar Imágenes:

Selecciona el nivel y el estudiante de la lista desplegable. Luego, en el panel expandible "Ver imágenes del trabajo", podrás visualizar las imágenes extraídas.
Añadir Observaciones:

Selecciona las observaciones correspondientes para cada estudiante usando el campo desplegable de observaciones. También puedes añadir observaciones adicionales en el campo de texto provisto.
Calificación:

Introduce la calificación del estudiante en el campo de texto correspondiente.
Generar PDF de Evaluación:

Haz clic en el botón "Generar PDF de evaluación" para crear un informe en PDF con el logo, la calificación y las observaciones seleccionadas, además de las imágenes del trabajo. El PDF se guardará en la carpeta evaluaciones.
Estructura de Carpetas
La estructura de carpetas para la aplicación debe ser la siguiente:

scss
Copiar código
/AplicacionEvaluacion
│   EvaluacionEstudiantes.exe
│   observaciones.xlsx
│   logo.png
│
├───evaluaciones
├───imagenes_extraidas
└───(Carpeta con trabajos de estudiantes)
    ├───CUARTO
    │   ├───Estudiante1
    │   └───Estudiante2
    ├───PRIMERO
    │   ├───Estudiante1
    │   └───Estudiante2
    └───SEGUNDO
Personalización
Modificar el Logo:

Si deseas cambiar el logo que aparece en el PDF, reemplaza el archivo logo.png en la carpeta principal con la imagen que prefieras. El logo debe estar en formato PNG y su tamaño ideal es de 4x4 cm para una visualización óptima.
Actualizar Observaciones:

Para añadir o modificar observaciones predeterminadas, abre y edita el archivo observaciones.xlsx. Asegúrate de que las observaciones estén en la columna llamada "Observaciones".

Solución de Problemas
No se Generan Imágenes desde PDFs:

Verifica que los archivos en la carpeta estén en formato PDF y que las subcarpetas sigan la estructura correcta.
Asegúrate de que el nombre de la carpeta no tenga caracteres especiales que puedan causar problemas al procesar la ruta.
El PDF de Evaluación no se Genera:

Asegúrate de que todos los campos (observaciones, calificación, y selección de estudiante) estén completos antes de presionar el botón "Generar PDF de evaluación".
Verifica que tengas permisos de escritura en la carpeta evaluaciones.
Problemas con el Logo:

Asegúrate de que el archivo logo.png está presente y que tiene el formato correcto (PNG). Revisa que el nombre del archivo sea exactamente logo.png.
Contacto
Para más información o asistencia técnica, contacta a:
Email: rlmoreira1@umsa.bo
Teléfono: 70112175

