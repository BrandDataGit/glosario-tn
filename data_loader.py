import pandas as pd
import streamlit as st

def load_excel_data(file_path):
    try:
        df = pd.read_excel(file_path)
        required_columns = ["Sujeto", "Capacidad", "Proceso de Valor", "Término de negocio", "Concepto", "Master Data Steward"]
        
        if all(col in df.columns for col in required_columns):
            return df
        else:
            st.error("El archivo Excel no contiene todas las columnas requeridas.")
            return None
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {str(e)}")
        return None

def save_excel_data(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar el archivo Excel: {str(e)}")
        return False

def load_attributes_data(file_path):
    try:
        df = pd.read_excel(file_path)
        required_columns = ["Atributo", "Definición", "Regla de Negocio", "Sinónimos"]
        
        if all(col in df.columns for col in required_columns):
            return df
        else:
            st.error("El archivo Excel de atributos no contiene todas las columnas requeridas.")
            return None
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo con las columnas requeridas
        df = pd.DataFrame(columns=["Atributo", "Definición", "Regla de Negocio", "Sinónimos"])
        df.to_excel(file_path, index=False)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel de atributos: {str(e)}")
        return None

def save_attributes_data(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        st.success(f"Atributos guardados exitosamente en {file_path}")
    except Exception as e:
        st.error(f"Error al guardar el archivo Excel de atributos: {str(e)}")

def load_tn_attribute_relations(file_path):
    try:
        df = pd.read_excel(file_path)
        required_columns = ["Término de Negocio", "Atributo"]
        
        if all(col in df.columns for col in required_columns):
            return df
        else:
            st.error("El archivo Excel de relaciones no contiene todas las columnas requeridas.")
            return None
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo con las columnas requeridas
        df = pd.DataFrame(columns=["Término de Negocio", "Atributo"])
        df.to_excel(file_path, index=False)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel de relaciones: {str(e)}")
        return None

def save_tn_attribute_relations(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        st.success(f"Relaciones guardadas exitosamente en {file_path}")
    except Exception as e:
        st.error(f"Error al guardar el archivo Excel de relaciones: {str(e)}")