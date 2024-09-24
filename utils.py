import streamlit as st
import pandas as pd
from supabase_config import supabase
from itertools import zip_longest
import unidecode
import re

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


def get_child_terms(term_id):
    # Obtener los términos hijo asociados al término padre
    response = supabase.table('termino-termino').select('termino-hijo-id').eq('termino-padre-id', term_id).execute()
    child_term_ids = [item['termino-hijo-id'] for item in response.data]
    
    if child_term_ids:
        response = supabase.table('termino-negocio').select('*').in_('Id', child_term_ids).execute()
        return response.data
    return []

def associate_existing_term(parent_term_id):
    st.session_state.page = 'associate_term'
    st.session_state.parent_term_id = parent_term_id
    st.rerun()


def add_new_child_term(parent_term_id):
    st.session_state.page = 'add_new_child_term'
    st.session_state.parent_term_id = parent_term_id
    st.rerun()
    
def associate_term(parent_term_id, child_term_id):
    # Crear la relación en la tabla termino-termino
    supabase.table('termino-termino').insert({
        'termino-padre-id': parent_term_id,
        'termino-hijo-id': child_term_id,
        'estatus': 'captura',
        'created_at': 'now()'
    }).execute()

def display_associable_terms(parent_term_id):
    # Obtener términos ya asociados al término padre
    associated_response = supabase.table('termino-termino').select('termino-hijo-id').eq('termino-padre-id', parent_term_id).execute()
    associated_term_ids = [item['termino-hijo-id'] for item in associated_response.data]

    # Obtener todos los términos de negocio disponibles que no estén asociados
    response = supabase.table('termino-negocio').select('*').not_.in_('Id', associated_term_ids).not_.eq('Id', parent_term_id).execute()
    available_terms = response.data

    if not available_terms:
        st.write("No hay términos disponibles para asociar.")
        return

    # Ordenar los términos disponibles por 'nombre-termino' en orden ascendente
    available_terms.sort(key=lambda x: x['nombre-termino'])

    # Agregar un filtro de búsqueda
    search_term = st.text_input("Buscar por nombre del término:")
    filtered_terms = [term for term in available_terms if search_term.lower() in term['nombre-termino'].lower()]

    # Crear dos columnas para mostrar los expanders
    col1, col2 = st.columns(2)

    # Dividir los términos filtrados en dos listas
    mid = len(filtered_terms) // 2
    left_column_terms = filtered_terms[:mid]
    right_column_terms = filtered_terms[mid:]

    # Mostrar términos disponibles en tarjetas
    for left_term, right_term in zip_longest(left_column_terms, right_column_terms):
        with col1:
            if left_term:
                with st.expander(f"{left_term['nombre-termino']}"):
                    st.write(f"Concepto: {left_term['concepto']}")
                    if st.button("Asociar", key=f"associate_term_{left_term['Id']}"):
                        associate_term(parent_term_id, left_term['Id'])
                        st.success(f"Término '{left_term['nombre-termino']}' asociado exitosamente.")
                        st.rerun()
        
        with col2:
            if right_term:
                with st.expander(f"{right_term['nombre-termino']}"):
                    st.write(f"Concepto: {right_term['concepto']}")
                    if st.button("Asociar", key=f"associate_term_{right_term['Id']}"):
                        associate_term(parent_term_id, right_term['Id'])
                        st.success(f"Término '{right_term['nombre-termino']}' asociado exitosamente.")
                        st.rerun()

    if not filtered_terms:
        st.write("No se encontraron términos que coincidan con la búsqueda.")

def normalize_string(s):
    # Remove accents and convert to lowercase
    return unidecode.unidecode(s).lower()

def is_valid_name(name):
     #Allow letters (including accented ones), numbers, and spaces
    return bool(re.match(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9\s]+$', name))

def get_capacidades():
    try:
        response = supabase.table('capacidad').select('*').execute()
        return [cap['capacidad'] for cap in response.data]
    except Exception as e:
        st.error(f"Error al cargar capacidades: {str(e)}")
        return []

def get_capacidad_id(nombre_capacidad):
    try:
        response = supabase.table('capacidad').select('id').eq('capacidad', nombre_capacidad).execute()
        return response.data[0]['id'] if response.data else None
    except Exception as e:
        st.error(f"Error al obtener id de capacidad: {str(e)}")
        return None

def get_capacidad_nombre(capacidad_id):
    try:
        # Convertir capacidad_id a entero, eliminando cualquier parte decimal
        capacidad_id = int(float(capacidad_id))
        response = supabase.table('capacidad').select('capacidad').eq('id', capacidad_id).execute()
        return response.data[0]['capacidad'] if response.data else None
    except ValueError:
        st.error(f"Error: capacidad_id inválido ({capacidad_id})")
        return None
    except Exception as e:
        st.error(f"Error al obtener nombre de capacidad: {str(e)}")
        return None

def desasociar_termino(parent_term_id, child_term_id):
    try:
        response = supabase.table('termino-termino').delete().eq('termino-padre-id', parent_term_id).eq('termino-hijo-id', child_term_id).execute()
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error al desasociar el término: {str(e)}")
        return False
    
def desasociar_dato(term_id, data_id):
    try:
        response = supabase.table('termino-dato').delete().eq('termino-id', term_id).eq('dato-id', data_id).execute()
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error al desasociar el dato: {str(e)}")
        return False

def delete_data_and_relations(data_id):
    try:
        # Primero, eliminamos todas las relaciones en la tabla termino-dato
        supabase.table('termino-dato').delete().eq('dato-id', data_id).execute()
        
        # Luego, eliminamos el dato de negocio
        response = supabase.table('dato-negocio').delete().eq('id', data_id).execute()
        
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error al eliminar el dato y sus relaciones: {str(e)}")
        return False