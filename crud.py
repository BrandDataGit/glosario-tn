import streamlit as st
from ui_components import display_explore_tn_page
from attributes import display_tn_details, add_new_attribute, edit_tn_details, edit_attribute_details
from attribute_explorer import display_explore_attributes_page, display_attribute_detail_page

st.set_page_config(page_title="Glosario de Términos de Negocio", layout="wide")

def main():
    st.title("Glosario de Términos de Negocio")

    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = 'explore'
    if 'selected_tn' not in st.session_state:
        st.session_state.selected_tn = None
    if 'selected_attribute' not in st.session_state:
        st.session_state.selected_attribute = None

    # Load data from Supabase
    df_tn = load_termino_negocio_data()
    df_dato = load_dato_negocio_data()
    df_relation = load_termino_dato_relations()
    if df_tn is None or df_dato is None or df_relation is None:
        return

    # Navigation menu
    menu = ["Explorar Términos", "Explorar Datos"]
    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Explorar Términos":
        if st.session_state.page in ['explore_attributes']:
            st.session_state.page = 'explore'
        if st.session_state.page != 'explore':
            if st.button("🚀 Regresar a TN"):
                st.session_state.page = 'explore'
                st.rerun()

        if st.session_state.page == 'explore':
            display_explore_tn_page(df_tn)
        elif st.session_state.page == 'tn_detail':
            display_tn_details(df_tn, df_dato, df_relation, st.session_state.selected_tn)
        elif st.session_state.page == 'tn_edit':
            edit_tn_details(df_tn, df_dato, df_relation, st.session_state.selected_tn)
        elif st.session_state.page == 'attribute_detail':
            display_attribute_detail_page(df_dato, df_relation, df_tn, st.session_state.selected_attribute)
        elif st.session_state.page == 'add_attribute':
            add_new_attribute(df_dato, df_relation, st.session_state.selected_tn)
        elif st.session_state.page == 'edit_attribute':
            edit_attribute_details(df_dato, st.session_state.selected_attribute, st.session_state.selected_tn)
            
    elif choice == "Explorar Datos":
        if st.session_state.page in ['explore']:
            st.session_state.page = 'explore_attributes'
        if st.session_state.page != 'explore_attributes':
            if st.button("🚀 Regresar a Datos"):
                st.session_state.page = 'explore_attributes'
                st.rerun()

        if st.session_state.page == 'explore_attributes':
            display_explore_attributes_page(df_dato, df_relation)
        elif st.session_state.page == 'attribute_detail_page':
            display_attribute_detail_page(df_dato, df_relation, df_tn, st.session_state.selected_attribute)

if __name__ == "__main__":
    main()