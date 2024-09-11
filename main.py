import streamlit as st
from data_loader import load_excel_data, save_excel_data, load_attributes_data, save_attributes_data, load_tn_attribute_relations, save_tn_attribute_relations
from ui_components import display_explore_tn_page
from attributes import display_tn_details, display_attribute_details, add_new_attribute

st.set_page_config(page_title="Glosario de Términos de Negocio", layout="wide")

def main():
    st.title("Glosario de Términos de Negocio")

    # Inicializar variables de sesión si no existen
    if 'page' not in st.session_state:
        st.session_state.page = 'explore'
    if 'selected_tn' not in st.session_state:
        st.session_state.selected_tn = None
    if 'selected_attribute' not in st.session_state:
        st.session_state.selected_attribute = None

    # Cargar datos
    df = load_excel_data("glosario.xlsx")
    attr_df = load_attributes_data("atributos.xlsx")
    relation_df = load_tn_attribute_relations("relaciones_tn_atributos.xlsx")
    if df is None or attr_df is None or relation_df is None:
        return

    # Menú de navegación
    menu = ["Explorar Términos"]
    choice = st.sidebar.selectbox("Menú", menu)



# 

    if choice == "Explorar Términos":
        if st.session_state.page != 'explore':
            if st.button("⬅️ Regresar"):
                st.session_state.page = 'explore'
                st.rerun()

        if st.session_state.page == 'explore':
            display_explore_tn_page(df)
        elif st.session_state.page == 'tn_detail':
            display_tn_details(df, attr_df, relation_df, st.session_state.selected_tn)
        elif st.session_state.page == 'attribute_detail':
            display_attribute_details(attr_df, st.session_state.selected_attribute, st.session_state.selected_tn)
        elif st.session_state.page == 'add_attribute':
            add_new_attribute(attr_df, relation_df, st.session_state.selected_tn)

        

if __name__ == "__main__":
    main()