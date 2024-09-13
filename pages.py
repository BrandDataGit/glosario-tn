import streamlit as st
import pandas as pd
from utils import display_status_indicator
from supabase_config import supabase

def display_terms(df):
    st.header("Explorar")

    # Mostrar número de resultados
    st.write(f"Mostrando {len(df)} términos de negocio")

    col1, col2 = st.columns(2)
    for i, (_, row) in enumerate(df.iterrows()):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(f"{display_status_indicator(row['estatus'])} **{row['nombre-termino']}**"):
                st.write(f"**Concepto:**  \n" f"{row['concepto']}")
                #st.write(f"Master Data Steward: **{row['Master Data Steward']}**")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Master Data Steward:</div>
                    <div style='margin-left: 40px;'><strong>{row['master-data-steward']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Sujeto:</div>
                    <div style='margin-left: 40px;'><strong>{row['sujeto']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Capacidad:</div>
                    <div style='margin-left: 40px;'><strong>{row['capacidad']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Proceso de Valor:</div>
                    <div style='margin-left: 40px;'><strong>{row['proceso-valor']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"   \n")
                st.write(f"   \n")
                col3,col4,col5 = st.columns([1,2,1])
            with col3:
                st.write("")
            with col4:
                if st.button("🧐 Ver más", key=f"btn_{row['nombre-termino']}"):
                    st.session_state.selected_term = row['Id']
                    st.session_state.page = 'term_detail'
                    st.rerun()   
            with col5:
                st.write("")
    

def display_term_detail(term_id):
    try:
        # Obtener los detalles del término
        response = supabase.table('termino-negocio').select('*').eq('Id', term_id).execute()
        term_details = response.data[0] if response.data else None

        if term_details:
            cola, colb = st.columns([5,1])
            with cola:
                st.header(f"{term_details['nombre-termino']}")
            with colb:
                if st.button("✏️ Editar"):
                    st.session_state.page = 'term_edit'
                    st.rerun()

            # Mostrar información del término de negocio
            st.text_area("Concepto", value=term_details['concepto'], disabled=True)
            
            # Crear dos columnas
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Capacidad", value=term_details['capacidad'], disabled=True)
                st.text_input("Sujeto", value=term_details['sujeto'], disabled=True)
            
            with col2:
                st.text_input("Proceso de Valor", value=term_details['proceso-valor'], disabled=True)
                st.text_input("Master Data Steward", value=term_details['master-data-steward'], disabled=True)

            # Puedes agregar más campos aquí si es necesario
        else:
            st.write("No se encontraron detalles para este término.")
    except Exception as e:
        st.error(f"Error al cargar los detalles del término: {str(e)}")

def edit_term_detail(term_id):
    try:
        # Obtener los detalles del término
        response = supabase.table('termino-negocio').select('*').eq('Id', term_id).execute()
        term_details = response.data[0] if response.data else None
        if term_details:
            st.header(f"Editar: {term_details['nombre-termino']}")

            # Crear formulario para edición
            with st.form(key='edit_term_form'):
                # Campos editables
                new_concept = st.text_area("Concepto", value=term_details['concepto'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_capacity = st.text_input("Capacidad", value=term_details['capacidad'])
                    new_subject = st.text_input("Sujeto", value=term_details['sujeto'])
                
                with col2:
                    new_value_process = st.text_input("Proceso de Valor", value=term_details['proceso-valor'])
                    new_data_steward = st.text_input("Master Data Steward", value=term_details['master-data-steward'])

                # Botones de acción
                col_cancel, col_save = st.columns(2)
                with col_cancel:
                    if st.form_submit_button("Cancelar"):
                        st.session_state.page = 'tn_detail'
                        st.rerun()
                with col_save:
                    if st.form_submit_button("Guardar"):
                        # Actualizar los datos en Supabase
                        updated_data = {
                            'concepto': new_concept,
                            'capacidad': new_capacity,
                            'sujeto': new_subject,
                            'proceso-valor': new_value_process,
                            'master-data-steward': new_data_steward
                        }
                        
                        supabase.table('termino-negocio').update(updated_data).eq('Id', term_id).execute()
                        
                        st.success("Cambios guardados exitosamente.")
                        st.session_state.page = 'tn_detail'
                        st.rerun()

        else:
            st.write("No se encontraron detalles para este término.")
    except Exception as e:
        st.error(f"Error al editar los detalles del término: {str(e)}")