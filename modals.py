import streamlit as st
from utils import delete_data_and_relations, get_dato_nombre, check_data_associations

@st.dialog("Confirmar eliminación")
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