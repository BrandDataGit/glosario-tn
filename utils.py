import streamlit as st
import pandas as pd
from supabase_config import supabase

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
        "aprobacion": "🟡",  # Punto relleno amarillo
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

    # Mostrar datos disponibles en tarjetas
    for data in available_data:
        with st.expander(f"{data['dato']}"):
            st.write(f"Definición: {data['definicion']}")
            st.write(f"Tipo de dato: {data['tipo_dato']}")
            if st.button("Asociar", key=f"associate_{data['id']}"):
                associate_data(term_id, data['id'])
                st.success(f"Dato '{data['dato']}' asociado exitosamente.")
                st.rerun()

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