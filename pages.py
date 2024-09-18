import streamlit as st
import pandas as pd
from utils import (display_status_indicator, get_associated_data, 
associate_existing_data, add_new_data, display_asociable_attributes, 
get_related_terms, display_breadcrumbs)
from supabase_config import supabase
from itertools import zip_longest

def display_terms(df):
    st.header("Explorar")

    # Añadir filtro de búsqueda por nombre del término
    term_filter = st.text_input("Buscar por nombre del término")

    # Aplicar filtro por nombre del término
    if term_filter:
        df = df[df['nombre-termino'].str.contains(term_filter, case=False)]

    # Mostrar número de resultados
    st.write(f"Mostrando {len(df)} términos de negocio")

    # Ordenar el DataFrame por 'nombre-termino' en orden ascendente
    df_sorted = df.sort_values(by='nombre-termino')

    # Dividir los términos en dos listas para mantener el orden alfabético en ambas columnas
    mid = len(df_sorted) // 2
    left_column_data = df_sorted.iloc[:mid]
    right_column_data = df_sorted.iloc[mid:]

    # Crear dos columnas para mostrar los expanders
    col1, col2 = st.columns(2)

    # Iterar sobre los términos y mostrarlos en las columnas
    for (_, left_row), (_, right_row) in zip_longest(left_column_data.iterrows(), right_column_data.iterrows(), fillvalue=(None, pd.Series())):
        with col1:
            if not left_row.empty:
                display_term_expander(left_row)
        
        with col2:
            if not right_row.empty:
                display_term_expander(right_row)

def display_term_expander(row):
    with st.expander(f"{display_status_indicator(row['estatus'])} 📚 **{row['nombre-termino']}**"):
        st.write(f"**Concepto:**  \n" f"{row['concepto']}")
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
        col3, col4, col5 = st.columns([1,2,1])
        with col3:
            st.write("")
        with col4:
            if st.button("🔎 Detalle", key=f"btn_{row['nombre-termino']}"):
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
            colc, cold, colf, colg = st.columns([8,1,1,1])
            with colc:
                display_breadcrumbs('term_detail', term_name=term_details['nombre-termino'])
            with cold:
                if st.button("🚀 Home"):
                    st.session_state.page = 'term_explore'
                    st.rerun()
            with colf:
                if st.button("✏️ Editar"):
                    st.session_state.page = 'term_edit'
                    st.rerun()
            with colg:
                # Agregar botón de estatus clickeable
                status_button = display_status_indicator(term_details['estatus'])
                if st.button(f"{status_button} Estatus"):
                    st.session_state.page = 'edit_status'
                    st.session_state.editing_term = term_details
                    st.rerun()

            st.header(f"📚 {term_details['nombre-termino']}")
            
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

            # Mostrar datos de negocio asociados y botones para asociar datos existentes o agregar nuevos
            col_header, col_associate, col_add = st.columns([9,1,1])
            with col_header:
                st.subheader("Datos de Negocio Asociados")
            with col_associate:
                if st.button("🔗 Asociar"):
                    associate_existing_data(term_id)
            with col_add:
                if st.button("➕ Agregar"):
                    add_new_data(term_id)
            
            associated_data = get_associated_data(term_id)
            if associated_data:
                # Ordenar los datos asociados por el campo 'dato' en orden ascendente
                associated_data.sort(key=lambda x: x['dato'])
                
                # Dividir los datos en dos listas para mantener el orden alfabético en ambas columnas
                mid = len(associated_data) // 2
                left_column_data = associated_data[:mid]
                right_column_data = associated_data[mid:]
                
                # Crear dos columnas para mostrar los expanders
                col1, col2 = st.columns(2)
                
                # Iterar sobre los datos asociados y mostrarlos en las columnas
                for left_data, right_data in zip_longest(left_column_data, right_column_data):
                    with col1:
                        if right_data:
                            with st.expander(f"{display_status_indicator(right_data['estatus'])}📑**{right_data['dato']}**"):
                                st.write(f"Definición: {right_data['definicion']}")
                                st.write(f"Tipo de dato: {right_data['tipo_dato']}")
                                if st.button("🔎 Detalle", key=f"detail_{right_data['id']}"):
                                    st.session_state.selected_data = right_data['id']
                                    st.session_state.page = 'data_detail'
                                    st.rerun()
                    
                    with col2:
                        if left_data:
                            with st.expander(f"{display_status_indicator(left_data['estatus'])}📑**{left_data['dato']}**"):
                                st.write(f"Definición: {left_data['definicion']}")
                                st.write(f"Tipo de dato: {left_data['tipo_dato']}")
                                if st.button("🔎 Detalle", key=f"detail_{left_data['id']}"):
                                    st.session_state.selected_data = left_data['id']
                                    st.session_state.page = 'data_detail'
                                    st.rerun()
                        
            else:
                st.write("No hay datos de negocio asociados.")

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
            st.header(f"Editar: 📚{term_details['nombre-termino']}")

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
                col_space,col_cancel, col_save = st.columns([7,1,1])
                with col_space:
                    st.write("")
                with col_cancel:
                    if st.form_submit_button("❌ Cancelar"):
                        st.session_state.page = 'term_detail'
                        st.rerun()
                with col_save:
                    if st.form_submit_button("💾 Guardar"):
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
                        st.session_state.page = 'term_detail'
                        st.rerun()

        else:
            st.write("No se encontraron detalles para este término.")
    except Exception as e:
        st.error(f"Error al editar los detalles del término: {str(e)}")


def display_associate_data_page(term_id):
    col1,col2 = st.columns([8,1])
    with col1:
        st.header("Asociar Datos Existentes")
    with col2:
        if st.button("↩️ Volver al TN"):
            st.session_state.page = 'term_detail'
            st.rerun()
    
    display_asociable_attributes(term_id)

def display_attribute_detail(data_id):
    try:
        response = supabase.table('dato-negocio').select('*').eq('id', data_id).execute()
        data_details = response.data[0] if response.data else None

        if data_details:
            term_id = st.session_state.get('selected_term')
            term_name = "Término Desconocido"
            if term_id:
                term_data_response = supabase.table('termino-dato').select('*').eq('termino-id', term_id).eq('dato-id', data_id).execute()
                if term_data_response.data:
                    term_details = supabase.table('termino-negocio').select('nombre-termino').eq('Id', term_id).execute().data[0]
                    term_name = term_details['nombre-termino']
                else:
                    term_name = "Término no asociado"

            colc, cold, colf, colg = st.columns([8, 1.5, 1, 1])
            with colc:
                display_breadcrumbs('data_detail', term_name=term_name, data_name=data_details['dato'])
            with cold:
                if st.button("↩️ Volver al TN"):
                    st.session_state.page = 'term_detail'
                    st.rerun()
            with colf:
                if st.button("✏️ Editar"):
                    st.session_state.page = 'data_edit'
                    st.session_state.editing_data = data_details
                    st.rerun()
            with colg:
                # Agregar botón de estatus clickeable
                status_button = display_status_indicator(data_details['estatus'])
                if st.button(f"{status_button} Estatus"):
                    st.session_state.page = 'edit_attribute_status'
                    st.session_state.editing_attribute = data_details
                    st.rerun()
            
            st.header(f"📑 {data_details['dato']}")

            st.text_area("Definición", value=data_details['definicion'], disabled=True)
            st.text_input("Formato de entrada", value=data_details['formato_entrada'], disabled=True)
            st.text_area("Valores permitidos", value=data_details['valores_permitidos'], disabled=True)
            st.text_input("Valor predeterminado", value=data_details['valor_predeterminado'], disabled=True)
            st.checkbox("Dato obligatorio", value=data_details['dato_obligatorio'], disabled=True)
            st.text_area("Regla de negocio", value=data_details['regla_negocio'], disabled=True)
            st.text_input("Tipo de dato", value=data_details['tipo_dato'], disabled=True)
            st.text_input("Uso", value=data_details['uso'], disabled=True)
            st.text_input("Estatus", value=data_details['estatus'], disabled=True)
            st.text_area("Comentario", value=data_details['comentario'], disabled=True)

            # Nueva sección: Términos de Negocio Relacionados
            st.subheader("Términos de Negocio Relacionados")
            related_terms = get_related_terms(data_id)
            if related_terms:
                # Ordenar los términos relacionados alfabéticamente por nombre-termino
                related_terms.sort(key=lambda x: x['nombre-termino'])
                
                # Dividir los términos en dos listas para mantener el orden alfabético en ambas columnas
                mid = len(related_terms) // 2
                left_column_terms = related_terms[:mid]
                right_column_terms = related_terms[mid:]
                
                # Crear dos columnas para mostrar los expanders
                col1, col2 = st.columns(2)
                
                # Función para mostrar un término en un expander
                def display_term(term):
                    with st.expander(f"{display_status_indicator(term['estatus'])}📚{term['nombre-termino']}"):
                        st.write(f"Concepto: {term['concepto']}")
                        st.write(f"Proceso de Valor: {term['proceso-valor']}")
                        if st.button("🔎 Detalle", key=f"view_term_{term['Id']}"):
                            st.session_state.selected_term = term['Id']
                            st.session_state.page = 'term_detail'
                            st.rerun()
                
                # Mostrar términos en las columnas
                with col1:
                    for term in right_column_terms:
                        display_term(term)
                
                with col2:
                    for term in left_column_terms:
                        display_term(term)
            else:
                st.write("No hay términos de negocio relacionados.")

        else:
            st.write("No se encontraron detalles para este dato.")
    except Exception as e:
        st.error(f"Error al cargar los detalles del dato: {str(e)}")

def edit_attribute_detail(data_details):
    st.header(f"Editar: 📑{data_details['dato']}")

    with st.form("edit_data_form"):
        new_definicion = st.text_area("Definición", value=data_details['definicion'])
        new_formato_entrada = st.text_input("Formato de entrada", value=data_details['formato_entrada'])
        new_valores_permitidos = st.text_area("Valores permitidos", value=data_details['valores_permitidos'])
        new_valor_predeterminado = st.text_input("Valor predeterminado", value=data_details['valor_predeterminado'])
        new_dato_obligatorio = st.checkbox("Dato obligatorio", value=data_details['dato_obligatorio'])
        new_regla_negocio = st.text_area("Regla de negocio", value=data_details['regla_negocio'])
        new_tipo_dato = st.text_input("Tipo de dato", value=data_details['tipo_dato'])
        new_uso = st.text_input("Uso", value=data_details['uso'])
        new_estatus = st.selectbox("Estatus", ["captura", "aprobacion", "aprobado"], index=["captura", "aprobacion", "aprobado"].index(data_details['estatus']))
        new_comentario = st.text_area("Comentario", value=data_details['comentario'])

        col_space,col1, col2 = st.columns([7,1,1])
        with col_space:
            st.write("")
        with col1:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state.page = 'data_detail'
                st.rerun()
        with col2:
            if st.form_submit_button("💾 Guardar"):
                try:
                    updated_data = {
                        'definicion': new_definicion,
                        'formato_entrada': new_formato_entrada,
                        'valores_permitidos': new_valores_permitidos,
                        'valor_predeterminado': new_valor_predeterminado,
                        'dato_obligatorio': new_dato_obligatorio,
                        'regla_negocio': new_regla_negocio,
                        'tipo_dato': new_tipo_dato,
                        'uso': new_uso,
                        'estatus': new_estatus,
                        'comentario': new_comentario
                    }
                    
                    supabase.table('dato-negocio').update(updated_data).eq('id', data_details['id']).execute()
                    
                    st.success("Cambios guardados exitosamente.")
                    st.session_state.page = 'data_detail'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {str(e)}")

def display_add_new_attribute(term_id):
    # Estilo CSS para los breadcrumbs
    subheader_style = """
        <style>
        .breadcrumbs {
            font-size: 1.2em;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1em;
        }
        </style>
    """
    
    # Combinar el estilo y el contenido de los breadcrumbs
    subheader_with_style = f"""
        {subheader_style}
        <div class="breadcrumbs">Agregar nuevo dato de negocio</div>
    """
    
    # Renderizar los breadcrumbs con estilo
    st.markdown(subheader_with_style, unsafe_allow_html=True)


    with st.form("add_new_data_form"):
        new_dato = st.text_input("Dato")
        new_definicion = st.text_area("Definición")
        new_formato_entrada = st.text_input("Formato de entrada")
        new_valores_permitidos = st.text_area("Valores permitidos (JSON)")
        new_valor_predeterminado = st.text_input("Valor predeterminado")
        new_dato_obligatorio = st.checkbox("Dato obligatorio")
        new_regla_negocio = st.text_area("Regla de negocio")
        new_tipo_dato = st.text_input("Tipo de dato")
        new_uso = st.text_input("Uso")
        new_estatus = st.selectbox("Estatus", ["captura", "aprobacion", "aprobado"])
        new_comentario = st.text_area("Comentario")

        col0, col1, col2 = st.columns([7,1,1])
        with col0:
            st.write("")
        with col1:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state.page = 'term_detail'
                st.rerun()
        with col2:
            if st.form_submit_button("💾 Guardar"):
                try:
                    # Insertar nuevo dato en la tabla dato-negocio
                    data_response = supabase.table('dato-negocio').insert({
                        'dato': new_dato,
                        'definicion': new_definicion,
                        'formato_entrada': new_formato_entrada,
                        'valores_permitidos': new_valores_permitidos,
                        'valor_predeterminado': new_valor_predeterminado,
                        'dato_obligatorio': new_dato_obligatorio,
                        'regla_negocio': new_regla_negocio,
                        'tipo_dato': new_tipo_dato,
                        'uso': new_uso,
                        'estatus': new_estatus,
                        'comentario': new_comentario
                    }).execute()

                    if data_response.data:
                        new_data_id = data_response.data[0]['id']
                        
                        # Crear relación en la tabla termino-dato
                        relation_response = supabase.table('termino-dato').insert({
                            'termino-id': term_id,
                            'dato-id': new_data_id,
                            'estatus': 'activo'
                        }).execute()

                        if relation_response.data:
                            st.success("Nuevo dato agregado y asociado exitosamente.")
                            st.session_state.page = 'term_detail'
                            st.rerun()
                        else:
                            st.error("Error al crear la relación entre el término y el dato.")
                    else:
                        st.error("Error al agregar el nuevo dato.")
                except Exception as e:
                    st.error(f"Error al procesar la solicitud: {str(e)}")

def edit_term_status(term_details):
    st.header(f"Estatus: 📚{term_details['nombre-termino']}")

    with st.form("edit_status_form"):
        new_status = st.selectbox("Estatus", ["captura", "por aprobar", "aprobado"], index=["captura", "por aprobar", "aprobado"].index(term_details['estatus']))
        new_comments = st.text_area("Comentarios", value=term_details.get('comentarios', ''))

        col_space, col1, col2 = st.columns([7,1,1])
        with col_space:
            st.write("")
        with col1:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state.page = 'term_detail'
                st.rerun()
        with col2:
            if st.form_submit_button("💾 Guardar"):
                try:
                    updated_data = {
                        'estatus': new_status,
                        'comentarios': new_comments
                    }
                    
                    supabase.table('termino-negocio').update(updated_data).eq('Id', term_details['Id']).execute()
                    
                    st.success("Cambios guardados exitosamente.")
                    st.session_state.page = 'term_detail'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {str(e)}")

def edit_attribute_status(data_details):
    st.header(f"Editar Estatus: 📑{data_details['dato']}")

    with st.form("edit_attribute_status_form"):
        new_status = st.selectbox("Estatus", ["captura", "por aprobar", "aprobado"], index=["captura", "por aprobar", "aprobado"].index(data_details['estatus']))
        new_comments = st.text_area("Comentarios", value=data_details.get('comentario', ''))

        col_space, col1, col2 = st.columns([7,1,1])
        with col_space:
            st.write("")
        with col1:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state.page = 'data_detail'
                st.rerun()
        with col2:
            if st.form_submit_button("💾 Guardar"):
                try:
                    updated_data = {
                        'estatus': new_status,
                        'comentario': new_comments
                    }
                    
                    supabase.table('dato-negocio').update(updated_data).eq('id', data_details['id']).execute()
                    
                    st.success("Cambios guardados exitosamente.")
                    st.session_state.page = 'data_detail'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar los cambios: {str(e)}")