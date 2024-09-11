import streamlit as st
import pandas as pd
from data_loader import save_attributes_data, save_tn_attribute_relations, save_excel_data

def display_tn_details(df, attr_df, relation_df, tn):
    
    cola, colb = st.columns([5,1])
    with cola:
        st.header(f"{tn}")
    with colb:
        if st.button("✏️ Editar"):
            st.session_state.page = 'tn_edit'
            st.rerun()

    # Mostrar información del término de negocio
    tn_info = df[df["Término de negocio"] == tn].iloc[0]
    st.text_area("Concepto", value=tn_info['Concepto'], disabled=True)
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

    colc, cold = st.columns([5,1])
    with colc:
        st.subheader("Atributos Asociados")
    with cold:
        if st.button("➕ Agregar"):
            st.session_state.page = 'add_attribute'
            st.rerun()

    
    tn_attributes = relation_df[relation_df["Término de Negocio"] == tn]
    
    col1, col2 = st.columns(2)
    for i, (_, rel) in enumerate(tn_attributes.iterrows()):
        attr = attr_df[attr_df["Atributo"] == rel["Atributo"]].iloc[0]
        with (col1 if i % 2 == 0 else col2):
            with st.expander(f"**{attr["Atributo"]}**"):
                st.write(f"Definición:  \n" f"**{attr['Definición']}**")
                st.write(f"Regla de Negocio:  \n" f"**{attr['Regla de Negocio']}**")
                st.write(f"   \n")
                col3,col4,col5 = st.columns([1,2,1])
            with col3:
                st.write("")
            with col4:
                if st.button("🧐 Ver más", key=f"btn_{attr['Atributo']}"):
                    st.session_state.selected_attribute = attr['Atributo']
                    st.session_state.page = 'attribute_detail'
                    st.rerun()   
            with col5:
                st.write("")
    
    

def display_attribute_details(attr_df, attribute, tn):

    cola, colb = st.columns([5,1])
    with cola:
        st.header(f"{attribute}")
    with colb:
        if st.button("✏️ Editar"):
            st.session_state.page = 'edit_attribute'
            st.rerun()

    # Mostrar información del atributo
    attr_info = attr_df[attr_df["Atributo"] == attribute].iloc[0]

    st.text_area("Definición", value=attr_info['Definición'], disabled=True)
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Regla de Negocio", value=attr_info['Regla de Negocio'], disabled=True)
        
    
    with col2:
        st.text_input("Sinónimos", value=attr_info['Sinónimos'], disabled=True)
    
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
    
    col3, col4, col5 = st.columns([4,1,1])
    with col3:
        st.write(" ")

    with col4:
        if st.button("❌ Cancelar"):
            st.session_state.page = 'tn_detail'
            st.rerun()
    
    with col5:
        if st.button("💾 Guardar"):
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


    


def edit_tn_details(df, attr_df, relation_df, tn):
    st.header(f"Editar: {tn}")
    
    # Obtener información del término de negocio
    tn_info = df[df["Término de negocio"] == tn].iloc[0]
    
    # Crear campos editables
    new_concept = st.text_area("Concepto", value=tn_info['Concepto'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_capacity = st.text_input("Capacidad", value=tn_info['Capacidad'])
        new_subject = st.text_input("Sujeto", value=tn_info['Sujeto'])
    
    with col2:
        new_value_process = st.text_input("Proceso de Valor", value=tn_info['Proceso de Valor'])
        new_data_steward = st.text_input("Master Data Steward", value=tn_info['Master Data Steward'])
    
    
    col3, col4, col5 = st.columns([4,1,1])
    with col3:
        st.write(" ")

    with col4:
        if st.button("❌ Cancelar"):
            st.session_state.page = 'tn_detail'
            st.rerun()
    
    with col5:
        if st.button("💾 Guardar"):
            # Actualizar el DataFrame
            df.loc[df["Término de negocio"] == tn, "Concepto"] = new_concept
            df.loc[df["Término de negocio"] == tn, "Capacidad"] = new_capacity
            df.loc[df["Término de negocio"] == tn, "Sujeto"] = new_subject
            df.loc[df["Término de negocio"] == tn, "Proceso de Valor"] = new_value_process
            df.loc[df["Término de negocio"] == tn, "Master Data Steward"] = new_data_steward
            
            # Guardar cambios en el archivo Excel
            if save_excel_data(df, "glosario.xlsx"):
                st.success("Cambios guardados exitosamente")
                # Cambiar el estado a 'tn_detail' para mostrar la versión actualizada
                st.session_state.page = 'tn_detail'
                st.rerun()
            else:
                st.error("Error al guardar los cambios")


        
    
    # Mostrar atributos asociados (sin edición en esta vista)
    st.markdown("---")
    st.subheader("Atributos Asociados")
    tn_attributes = relation_df[relation_df["Término de Negocio"] == tn]
    
    col1, col2 = st.columns(2)
    for i, (_, rel) in enumerate(tn_attributes.iterrows()):
        attr = attr_df[attr_df["Atributo"] == rel["Atributo"]].iloc[0]
        with (col1 if i % 2 == 0 else col2):
            with st.expander(attr["Atributo"]):
                st.write(f"Definición:  \n" f"**{attr['Definición']}**")
                st.write(f"Regla de Negocio:  \n" f"**{attr['Regla de Negocio']}**")

    
def edit_attribute_details(attr_df, attribute, tn):
    st.header(f"Detalles del Atributo: {attribute}")
    
    attr_info = attr_df[attr_df["Atributo"] == attribute].iloc[0]
    # Crear campos editables
    new_definition = st.text_area("Definición", value=attr_info['Definición'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_business_rule = st.text_input("Regla de Negocio", value=attr_info['Regla de Negocio'])
        
    
    with col2:
        new_sinonims = st.text_input("Sinónimos", value=attr_info['Sinónimos'])
        
    
    col3, col4, col5 = st.columns([4,1,1])
    with col3:
        st.write(" ")

    with col4:
        if st.button("❌ Cancelar"):
            st.session_state.page = 'tn_detail'
            st.session_state.selected_tn = tn
            st.rerun()
    
    with col5:
        if st.button("💾 Guardar"):
            # Actualizar el DataFrame
            attr_df.loc[attr_df["Atributo"] == attribute, "Definición"] = new_definition
            attr_df.loc[attr_df["Atributo"] == attribute, "Regla de Negocio"] = new_business_rule
            attr_df.loc[attr_df["Atributo"] == attribute, "Sinónimos"] = new_sinonims
    
            
            # Guardar cambios en el archivo Excel
            if save_excel_data(attr_df, "atributos.xlsx"):
                st.success("Cambios guardados exitosamente")
                # Cambiar el estado a 'tn_detail' para mostrar la versión actualizada
                st.session_state.page = 'tn_detail'
                st.rerun()
            else:
                st.error("Error al guardar los cambios")