# Taller 3 - Extracción de Datos desde API REST, Almacenamiento en MongoDB Atlas y Análisis Exploratorio (EDA)

**Curso:** Bases de Datos — Pregrado en Estadística  
**Institución:** Universidad de Antioquia (UdeA)  
**Estudiante:** Juan Pablo Ortiz Jaramillo  

## Descripción del Proyecto
Este proyecto implementa un flujo completo de adquisición, almacenamiento NoSQL y análisis estadístico descriptivo en Python:
1. **Extracción:** Consumo paginado de **1.000 registros reales** desde la API pública [Open Brewery DB](https://www.openbrewerydb.org/) mediante `requests`.
2. **Almacenamiento NoSQL:** Carga e indexación de los documentos JSON en una base de datos documental en la nube (**MongoDB Atlas**, base `cervecerias_db`, colección `cervecerias`) usando `pymongo`.
3. **Análisis Exploratorio de Datos (EDA):** Limpieza, validación de calidad de datos, consultas de agregación y visualización estadística con `pandas`, `matplotlib` y `seaborn` en Jupyter Notebook.

## Estructura del Repositorio
```text
├── ingesta.py              # Script de extracción desde Open Brewery DB y carga en MongoDB Atlas
├── eda_cervecerias.ipynb   # Cuaderno Jupyter con limpieza, agregaciones y visualizaciones estadísticas
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Exclusión de archivos temporales y variables de entorno
└── README.md               # Documentación del proyecto