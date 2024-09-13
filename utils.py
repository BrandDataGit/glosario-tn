import streamlit as st
import pandas as pd
from supabase_config import supabase

def load_termino_negocio_data():
    try:
        #st.write("Intentando conectar con Supabase...")
        response = supabase.table('termino-negocio').select('*').execute()
        #st.write("Conexión exitosa. Datos recibidos.")
        df = pd.DataFrame(response.data)
        #st.write(f"Columnas encontradas: {df.columns.tolist()}")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos de Supabase: {str(e)}")
        return pd.DataFrame()

def display_status_indicator(status):
    status_map = {
        "captura": "⚪",  # Punto sin rellenar
        "aprobacion": "🟡",  # Punto relleno amarillo
        "aprobado": "🟢",  # Punto relleno verde
    }
    return status_map.get(status.lower(), "⚪")  # Default to empty circle