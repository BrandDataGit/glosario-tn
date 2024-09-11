import streamlit as st
import pandas as pd
from data_loader import save_attributes_data, save_tn_attribute_relations

def display_tn_details(df, attr_df, relation_df, tn):
    st.header(f"{tn}")
    
    # Mostrar información del término de negocio
    tn_info = df[df["Término de negocio"] == tn].iloc[0]
    st.text_input("Concepto", value=tn_info['Concepto'], disabled=True)
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Capacidad", value=tn_info['Capacidad'], disabled=True)
        st.text_input("Sujeto", value=tn_info['Sujeto'], disabled=True)
    
    with col2:
        st.text_input("Proceso de Valor", value=tn_info['Proceso de Valor'], disabled=True)
        st.text_input("Master Data Steward", value=tn_info['Master Data Steward'], disabled=True)
    
    # Mostrar atributos asociados en tarjetas
    st.markdown("---")
    st.subheader("Atributos Asociados")
    tn_attributes = relation_df[relation_df["Término de Negocio"] == tn]
    
    col1, col2 = st.columns(2)
    for i, (_, rel) in enumerate(tn_attributes.iterrows()):
        attr = attr_df[attr_df["Atributo"] == rel["Atributo"]].iloc[0]
        with (col1 if i % 2 == 0 else col2):
            with st.expander(attr["Atributo"]):
                st.write(f"**Definición:** {attr['Definición'][:100]}...")
                if st.button(f"Ver detalle de {attr['Atributo']}"):
                    st.session_state.selected_attribute = attr['Atributo']
                    st.session_state.page = 'attribute_detail'
                    st.rerun()
    
    if st.button("Agregar Nuevo Atributo"):
        st.session_state.page = 'add_attribute'
        st.rerun()

def display_attribute_details(attr_df, attribute, tn):
    st.header(f"Detalles del Atributo: {attribute}")
    
    attr_info = attr_df[attr_df["Atributo"] == attribute].iloc[0]
    st.write(f"**Definición:** {attr_info['Definición']}")
    st.write(f"**Regla de Negocio:** {attr_info['Regla de Negocio']}")
    st.write(f"**Sinónimos:** {attr_info['Sinónimos']}")
    
    if st.button("Volver al Término de Negocio"):
        st.session_state.page = 'tn_detail'
        st.session_state.selected_tn = tn
        st.rerun()

def add_new_attribute(attr_df, relation_df, tn):
    st.header(f"Agregar Nuevo Atributo para {tn}")
    
    new_attr = st.text_input("Nombre del Atributo")
    new_def = st.text_area("Definición")
    new_rule = st.text_area("Regla de Negocio")
    new_syn = st.text_input("Sinónimos")
    
    if st.button("Guardar Atributo"):
        new_attr_df = pd.DataFrame({
            "Atributo": [new_attr],
            "Definición": [new_def],
            "Regla de Negocio": [new_rule],
            "Sinónimos": [new_syn]
        })
        attr_df = pd.concat([attr_df, new_attr_df], ignore_index=True)
        
        new_relation = pd.DataFrame({
            "Término de Negocio": [tn],
            "Atributo": [new_attr]
        })
        relation_df = pd.concat([relation_df, new_relation], ignore_index=True)
        
        save_attributes_data(attr_df, "atributos.xlsx")
        save_tn_attribute_relations(relation_df, "relaciones_tn_atributos.xlsx")
        
        st.success(f"Atributo '{new_attr}' agregado exitosamente a '{tn}'.")
        st.session_state.page = 'tn_detail'
        st.session_state.selected_tn = tn
        st.rerun()