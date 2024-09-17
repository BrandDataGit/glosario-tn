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
    st.header("Datos Disponibles para Asociar")

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

        if st.form_submit_button("Agregar nuevo dato"):
            # Insertar el nuevo dato en la tabla dato-negocio
            response = supabase.table('dato-negocio').insert({
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
                'comentario': new_comentario,
                'created_at': 'now()',
                'user_create': st.session_state.get('user_id', 'unknown')
            }).execute()

            if response.data:
                new_data_id = response.data[0]['id']
                # Crear la relación en la tabla termino-dato
                supabase.table('termino-dato').insert({
                    'termino-id': term_id,
                    'dato-id': new_data_id,
                    'estatus': 'activo',
                    'created_at': 'now()',
                    'user_create': st.session_state.get('user_id', 'unknown')
                }).execute()

                st.success("Nuevo dato agregado y asociado exitosamente.")
                st.rerun()
            else:
                st.error("Error al agregar el nuevo dato.")