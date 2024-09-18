import streamlit as st
import pandas as pd
from supabase_config import supabase
from utils import load_termino_negocio_data
from pages import (display_terms, display_term_detail, edit_term_detail, 
display_associate_data_page, display_attribute_detail, 
edit_attribute_detail, display_add_new_attribute, edit_term_status, edit_attribute_status)

st.set_page_config(page_title="Glosario de Términos de Negocio", layout="wide")

def main():
    st.title("Glosario de Términos de Negocio")

    # Inicializar variables de sesión si no existen
    if 'page' not in st.session_state:
        st.session_state.page = 'term_explore'
    if 'selected_term' not in st.session_state:
        st.session_state.selected_term = None
    if 'selected_attribute' not in st.session_state:
        st.session_state.selected_attribute = None

    # Cargar datos
    tn_df = load_termino_negocio_data()

    if tn_df.empty:
        st.warning("No se pudieron cargar los datos. Por favor, verifica tu conexión a Supabase.")
        return
    
    # Menú de navegación
    menu = ["Explorar Términos"]
    choice = st.sidebar.selectbox("Menú", menu)

    # Filtros
    st.sidebar.header("Filtros")
    
    # Crear filtros dinámicamente
    filter_columns = ['master-data-steward', 'proceso-valor', 'origen', 'estatus', 'sujeto', 'capacidad']
    filters = {}
    
    for column in filter_columns:
        if column in tn_df.columns:
            options = ['Todos'] + list(tn_df[column].unique())
            filters[column] = st.sidebar.selectbox(f"Filtrar por {column}", options)
        else:
            st.warning(f"Columna '{column}' no encontrada en el DataFrame")

    # Aplicar filtros
    for column, value in filters.items():
        if value != 'Todos':
            tn_df = tn_df[tn_df[column] == value]
    
    if choice == "Explorar Términos":
        if st.session_state.page == 'term_explore':
            display_terms(tn_df)
        elif st.session_state.page == 'term_detail':
            display_term_detail(st.session_state.selected_term)
        elif st.session_state.page == 'term_edit':
            edit_term_detail(st.session_state.selected_term)
        elif st.session_state.page == 'associate_data':
            display_associate_data_page(st.session_state.selected_term)
        elif st.session_state.page == 'data_detail':
            display_attribute_detail(st.session_state.selected_data)
        elif st.session_state.page == 'data_edit':
            edit_attribute_detail(st.session_state.editing_data)
        elif st.session_state.page == 'add_new_data':
            display_add_new_attribute(st.session_state.selected_term)
        elif st.session_state.page == 'edit_status':
            edit_term_status(st.session_state.editing_term)
        elif st.session_state.page == 'edit_attribute_status':
            edit_attribute_status(st.session_state.editing_attribute)

if __name__ == "__main__":
    main()