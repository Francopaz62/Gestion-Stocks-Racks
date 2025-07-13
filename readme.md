# Sistema de Gestión de Stock en Racks

Aplicación desarrollada en Python con **Streamlit** para gestionar la ubicación de pallets en racks, permitiendo registrar y visualizar información como producto, lote, fechas y cantidad de manera simple y visual.

## Funcionalidades

- Visualización tipo grilla de racks y ubicaciones (slots)
- Registro y edición de productos por slot
- Almacenamiento de datos en un archivo CSV (`pallets.csv`)
- Interfaz intuitiva y fácil de usar

## Requisitos

- Python 3.10 o superior

### 📦 Instalación de dependencias

Asegurate de tener un entorno virtual activado. Luego instalá los paquetes necesarios con:

pip install -r requirements.txt


### Cómo ejecutar la app: 

Asegurate de estar en la carpeta del proyecto.
Ejecutá el siguiente comando:
streamlit run app.py


Se abrirá la aplicación automáticamente en tu navegador en la dirección:
http://localhost:8501/


Estructura de archivos
  FINAL PROGRAMACION STOCK
├── .venv/              # Entorno virtual (no se sube a repositorios)
├── app.py              # App principal de Streamlit
├── pallets.csv         # Archivo con los datos de stock
├── readme.md           # Documentación del proyecto
├── requirements.txt    # Lista de dependencias
├── utils.py            # Funciones auxiliares (si lo necesitás después)


Desarrollado por Franco Paz Maturano