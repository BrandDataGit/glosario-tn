import streamlit as st
import pandas as pd
from supabase_config import supabase
from itertools import zip_longest

def load_termino_negocio_data():
    try:
        #st.write("Intentando conectar con Supabase...")
        response = supabase.table('termino-negocio').select('*').execute()
        #st.write("Conexión exitosa. Datos recibidos.")
        df = pd.DataFrame(response.data)
        #st.write(f"Columnas encontradas: {df.columns.tolist()}")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos de Supabase: {str(e)}")
        return pd.DataFrame()

def display_status_indicator(status):
    status_map = {
        "captura": "⚪",  # Punto sin rellenar
        "por aprobar": "🟡",  # Punto relleno amarillo
        "aprobado": "🟢",  # Punto relleno verde
    }
    return status_map.get(status.lower(), "⚪")  # Default to empty circle

def get_associated_data(term_id):
    # Obtener los datos asociados al término
    response = supabase.table('termino-dato').select('dato-id').eq('termino-id', term_id).execute()
    data_ids = [item['dato-id'] for item in response.data]
    
    if data_ids:
        response = supabase.table('dato-negocio').select('*').in_('id', data_ids).execute()
        return response.data
    return []

def display_asociable_attributes(term_id):
    # Estilo CSS para los breadcrumbs
    subheader_style = """
        <style>
        .breadcrumbs {
            font-size: 1em;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 1em;
        }
        </style>
    """
    
    # Combinar el estilo y el contenido de los breadcrumbs
    subheader_with_style = f"""
        {subheader_style}
        <div class="breadcrumbs">Datos disponibles:</div>
    """
    
    # Renderizar los breadcrumbs con estilo
    st.markdown(subheader_with_style, unsafe_allow_html=True)

    # Obtener datos ya asociados al término
    associated_response = supabase.table('termino-dato').select('dato-id').eq('termino-id', term_id).execute()
    associated_data_ids = [item['dato-id'] for item in associated_response.data]

    # Obtener todos los datos de negocio disponibles que no estén asociados
    response = supabase.table('dato-negocio').select('*').not_.in_('id', associated_data_ids).execute()
    available_data = response.data

    if not available_data:
        st.write("No hay datos disponibles para asociar.")
        return

    # Ordenar los datos disponibles por 'dato' en orden ascendente
    available_data.sort(key=lambda x: x['dato'])

    # Agregar un filtro de búsqueda
    search_term = st.text_input("Buscar por nombre del dato:")
    filtered_data = [data for data in available_data if search_term.lower() in data['dato'].lower()]

    # Crear dos columnas para mostrar los expanders
    col1, col2 = st.columns(2)

    # Dividir los datos filtrados en dos listas para mantener el orden alfabético en ambas columnas
    mid = len(filtered_data) // 2
    left_column_data = filtered_data[:mid]
    right_column_data = filtered_data[mid:]

    # Mostrar datos disponibles en tarjetas
    for left_data, right_data in zip_longest(left_column_data, right_column_data):
        with col1:
            if left_data:
                with st.expander(f"{left_data['dato']}"):
                    st.write(f"Definición: {left_data['definicion']}")
                    st.write(f"Tipo de dato: {left_data['tipo_dato']}")
                    if st.button("Asociar", key=f"associate_{left_data['id']}"):
                        associate_data(term_id, left_data['id'])
                        st.success(f"Dato '{left_data['dato']}' asociado exitosamente.")
                        st.rerun()
        
        with col2:
            if right_data:
                with st.expander(f"{right_data['dato']}"):
                    st.write(f"Definición: {right_data['definicion']}")
                    st.write(f"Tipo de dato: {right_data['tipo_dato']}")
                    if st.button("Asociar", key=f"associate_{right_data['id']}"):
                        associate_data(term_id, right_data['id'])
                        st.success(f"Dato '{right_data['dato']}' asociado exitosamente.")
                        st.rerun()

    if not filtered_data:
        st.write("No se encontraron datos que coincidan con la búsqueda.")

def associate_data(term_id, data_id):
    # Crear la relación en la tabla termino-dato
    supabase.table('termino-dato').insert({
        'termino-id': term_id,
        'dato-id': data_id,
        'estatus': 'activo',
        #'created_at': 'now()',
        #'user_create': st.session_state.get('user_id', 'unknown')
    }).execute()

def associate_existing_data(term_id):
    st.session_state.page = 'associate_data'
    st.session_state.selected_term = term_id
    st.rerun()

def add_new_data(term_id):
    st.session_state.page = 'add_new_data'
    st.session_state.selected_term = term_id
    st.rerun()

def get_related_terms(data_id):
    # Obtener los términos asociados al dato
    response = supabase.table('termino-dato').select('termino-id').eq('dato-id', data_id).execute()
    term_ids = [item['termino-id'] for item in response.data]
    
    if term_ids:
        response = supabase.table('termino-negocio').select('*').in_('Id', term_ids).execute()
        return response.data
    return []

def display_breadcrumbs(current_page, term_name=None, data_name=None):
    breadcrumbs = []
    
    if current_page in ['term_detail', 'data_detail'] and term_name:
        breadcrumbs.append(f"Nivel: Término de Negocio")#breadcrumbs.append(f"📚 {term_name}")
    
    if current_page == 'data_detail' and data_name:
        breadcrumbs.append(f"Dato de Negocio Asociado")#breadcrumbs.append(f"📑 {data_name}")

    breadcrumb_html = " &gt; ".join(breadcrumbs)
    
    # Estilo CSS para los breadcrumbs
    breadcrumb_style = """
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
    breadcrumbs_with_style = f"""
        {breadcrumb_style}
        <div class="breadcrumbs">{breadcrumb_html}</div>
    """
    
    # Renderizar los breadcrumbs con estilo
    st.markdown(breadcrumbs_with_style, unsafe_allow_html=True)