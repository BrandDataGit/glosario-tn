import streamlit as st
from utils import delete_data_and_relations, get_dato_nombre, delete_term_and_relations, get_term_nombre

@st.dialog("Confirmar eliminación de dato de negocio")
def eliminar_dato_negocio(data_id):
    item_name = get_dato_nombre(data_id)
    st.write(f"¿Está seguro de que desea eliminar: {item_name}?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sí, eliminar"):
                success, message = delete_data_and_relations(data_id)
                if success:
                    st.success(message)
                    st.session_state.page = 'term_detail'
                    st.rerun()
                else:
                    st.error(message)
    with col2:
        if st.button("No, cancelar"):
            st.session_state.delete_confirmation = False
            st.rerun()

@st.dialog("No se puede borrar el dato de negocio")
def warning_1(data_id):
    item_name = get_dato_nombre(data_id)
    st.write(f"{item_name} está asociado a múltiples términos de negocio y no puede ser eliminado.")
    col1,col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        if st.button("Cancelar"):
            st.session_state.delete_confirmation = False
            st.rerun()
    with col3:
        st.write("")

@st.dialog("Confirmar eliminación de Término de negocio")
def eliminar_termino_negocio(term_id):
    item_name = get_term_nombre(term_id)
    st.write(f"¿Está seguro de que desea eliminar: {item_name}?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sí, eliminar"):
                success, message = delete_term_and_relations(term_id)
                if success:
                    st.success(message)
                    st.session_state.page = 'term_explore'
                    st.rerun()
                else:
                    st.error(message)
    with col2:
        if st.button("No, cancelar"):
            st.session_state.delete_confirmation = False
            st.rerun()

@st.dialog("No se puede borrar el termino de negocio")
def warning_2(term_id):
    item_name = get_term_nombre(term_id)
    st.write(f"{item_name} tiene asociados múltiples términos y/o datos de negocio y no puede ser eliminado.")
    col1,col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        if st.button("Cancelar"):
            st.session_state.delete_confirmation = False
            st.rerun()
    with col3:
        st.write("")
