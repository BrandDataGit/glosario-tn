import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Lector de Glosario", layout="wide")

# Función para verificar las columnas requeridas
def verificar_columnas(df):
    columnas_requeridas = [
        "Sujeto", "Proceso de Valor", "Capacidad", "Master Data Steward",
        "Término de negocio", "Concepto", "Sinónimo 1", "Sinónimo 2", "Sinónimo 3",
        "Origen", "Revisión", "Comentarios", "Estatus Comentarios"
    ]
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    return columnas_faltantes

# Menú de navegación
menu = ["Leer TN"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Leer TN":
    st.title("Leer Términos de Negocio")

    # Verificar si el archivo Excel existe
    if not os.path.exists("glosario.xlsx"):
        st.error("El archivo 'glosario.xlsx' no se encuentra en el directorio actual.")
    else:
        try:
            # Leer el archivo Excel
            df = pd.read_excel("glosario.xlsx")
            
            # Mostrar información de depuración
            st.write("Información de depuración:")
            st.write(f"Número de filas: {df.shape[0]}")
            st.write(f"Número de columnas: {df.shape[1]}")
            st.write("Nombres de las columnas:")
            st.write(df.columns.tolist())

            # Verificar las columnas
            columnas_faltantes = verificar_columnas(df)

            if columnas_faltantes:
                st.error(f"Faltan las siguientes columnas en el archivo Excel: {', '.join(columnas_faltantes)}")
            else:
                st.success("Todas las columnas requeridas están presentes.")
                # Mostrar la tabla
                st.dataframe(df)

        except Exception as e:
            st.error(f"Ocurrió un error al leer el archivo Excel: {str(e)}")