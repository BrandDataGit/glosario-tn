import streamlit as st
from supabase_config import sign_up, sign_in, sign_out, get_user, check_user_exists, insert_user_profile
import pandas as pd
from utils import load_termino_negocio_data, get_capacidades, get_capacidad_id, delete_term_and_relations
from pages import (display_terms, display_term_detail, edit_term_detail, 
                   display_associate_data_page, display_attribute_detail, 
                   edit_attribute_detail, display_add_new_attribute, 
                   edit_term_status, edit_attribute_status, add_new_term,
                   display_associate_existing_term, display_add_new_child_term)

st.set_page_config(page_title="Glosario de Términos de Negocio", layout="wide")

# Agregar estilos CSS personalizados
st.markdown("""
<style>
    body {
        font-size: 0.9rem !important;
    }
    .stButton button {
        font-size: 0.9rem !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        font-size: 0.9rem !important;
    }
    .stTextInput input, .stTextArea textarea {
        font-size: 0.9rem !important;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

def login():
    st.title("Iniciar Sesión")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")
    if st.button("Iniciar Sesión", key="login_button"):
        # Primero, verificar si el usuario existe
        if not check_user_exists(email):
            st.error("Usuario no registrado.")
            return
        
        # Si el usuario existe, intentar iniciar sesión
        try:
            response = sign_in(email, password)
            if response.user:
                st.session_state.user = response.user
                st.success("Inicio de sesión exitoso!")
                st.rerun()
        except Exception as e:
            error_message = str(e)
            if "Invalid login credentials" in error_message:
                st.error("Usuario o contraseña incorrectos.")
            else:
                st.error(f"Error en el inicio de sesión: {error_message}")


def signup():
    st.title("Registrarse")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Contraseña", type="password", key="signup_password")
    if st.button("Registrarse", key="signup_button"):
        if check_user_exists(email):
            st.error("Este email ya está registrado. Por favor, usa otro email o inicia sesión.")
        else:
            response = sign_up(email, password)
            if "error" in response:
                st.error(response["error"])
            elif response.user:
                # El registro fue exitoso, ahora insertamos el email en user-profile
                insert_result = insert_user_profile(email)
                if insert_result:
                    st.success("Registro exitoso! Por favor, inicia sesión.")
                else:
                    st.warning("Registro exitoso, pero hubo un problema al crear el perfil de usuario. Por favor, contacta al soporte.")
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

        if st.session_state.get('term_deleted'):
            # Eliminar el término de la base de datos
            delete_term_and_relations(st.session_state.term_to_delete)
            # Limpiar las variables de sesión
            st.session_state.term_deleted = False
            st.session_state.term_to_delete = None
            st.session_state.selected_term = None
            st.session_state.selected_attribute = None
            st.session_state.parent_term_id = None
            # Forzar una recarga completa
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
        filter_columns = ['master-data-steward', 'proceso-valor', 'origen', 'estatus', 'sujeto']
        filters = {}
        
        for column in filter_columns:
            if column in tn_df.columns:
                options = ['Todos'] + list(tn_df[column].unique())
                filters[column] = st.sidebar.selectbox(f"Filtrar por {column}", options)
            else:
                st.warning(f"Columna '{column}' no encontrada en el DataFrame")

         # Filtro especial para capacidad
        capacidades = get_capacidades()
        selected_capacidad = st.sidebar.selectbox("Filtrar por capacidad", ['Todos'] + capacidades)
        filters['capacidad'] = selected_capacidad

        # Aplicar filtros
        for column, value in filters.items():
            if value != 'Todos':
                if column == 'capacidad':
                    capacidad_id = get_capacidad_id(value)
                    tn_df = tn_df[tn_df['capacidad_id'] == capacidad_id]
                else:
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