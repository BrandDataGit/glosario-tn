import streamlit as st
from supabase_config import sign_up, sign_in, sign_out, get_user
import pandas as pd
from utils import load_termino_negocio_data
from pages import (display_terms, display_term_detail, edit_term_detail, 
                   display_associate_data_page, display_attribute_detail, 
                   edit_attribute_detail, display_add_new_attribute, 
                   edit_term_status, edit_attribute_status, add_new_term,
                   display_associate_existing_term, display_add_new_child_term)

st.set_page_config(page_title="Glosario de Términos de Negocio", layout="wide")

def login():
    st.title("Iniciar Sesión")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")
    if st.button("Iniciar Sesión"):
        response = sign_in(email, password)
        if response.user:
            st.session_state.user = response.user
            st.success("Inicio de sesión exitoso!")
            st.rerun()
        else:
            st.error("Error en el inicio de sesión. Por favor, verifica tus credenciales.")

def signup():
    st.title("Registrarse")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Contraseña", type="password", key="signup_password")
    if st.button("Registrarse"):
        response = sign_up(email, password)
        if response.user:
            st.success("Registro exitoso! Por favor, inicia sesión.")
            st.rerun()
        else:
            st.error("Error en el registro. Por favor, intenta de nuevo.")

def main():
    if "user" not in st.session_state:
        tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
        with tab1:
            login()
        with tab2:
            signup()
    else:
        st.title("Glosario de Términos de Negocio")

        # Agregar botón de cierre de sesión en la barra lateral
        st.sidebar.title(f"Bienvenido, {st.session_state.user.email}")
        if st.sidebar.button("Cerrar Sesión"):
            sign_out()
            st.session_state.pop("user", None)
            st.rerun()

        # Inicializar variables de sesión si no existen
        if 'page' not in st.session_state:
            st.session_state.page = 'term_explore'
        if 'selected_term' not in st.session_state:
            st.session_state.selected_term = None
        if 'selected_attribute' not in st.session_state:
            st.session_state.selected_attribute = None
        if 'parent_term_id' not in st.session_state:
            st.session_state.parent_term_id = None

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
            elif st.session_state.page == 'add_new_term':
                add_new_term()
            elif st.session_state.page == 'associate_term':
                display_associate_existing_term(st.session_state.parent_term_id)
            elif st.session_state.page == 'add_new_child_term':
                display_add_new_child_term(st.session_state.parent_term_id)

if __name__ == "__main__":
    main()