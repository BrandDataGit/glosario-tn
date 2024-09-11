import streamlit as st
from filters import apply_filters

def display_cards(df):
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    # Dividir los datos en dos partes
    half = len(df) // 2
    df1, df2 = df.iloc[:half], df.iloc[half:]

    # Función para mostrar una tarjeta individual
    def show_card(row):
        with st.expander(row["Término de negocio"]):
            col_info, col_buttons = st.columns([3, 1])
            with col_info:
                st.write(f"**Concepto:** {row['Concepto']}")
                st.write(f"**Master Data Steward:** {row['Master Data Steward']}")
                st.write(f"**Sujeto:** {row['Sujeto']}")
                st.write(f"**Capacidad:** {row['Capacidad']}")
                st.write(f"**Proceso de Valor:** {row['Proceso de Valor']}")
            with col_buttons:
                if st.button("👁️ Ver detalle", key=f"btn_{row['Término de negocio']}"):
                    st.session_state.selected_tn = row['Término de negocio']
                    st.session_state.page = 'detail'
                    st.rerun()
            st.markdown("---")  # Línea divisoria entre tarjetas
    
    # Mostrar tarjetas en la primera columna
    with col1:
        for _, row in df1.iterrows():
            show_card(row)
    
    # Mostrar tarjetas en la segunda columna
    with col2:
        for _, row in df2.iterrows():
            show_card(row)

def display_explore_tn_page(df):
    st.header("Explorar")

    
    # Aplicar filtros
    filtered_df = apply_filters(df)
    df=filtered_df
    
    # Mostrar número de resultados
    st.write(f"Mostrando {len(filtered_df)} términos de negocio")

    col1, col2 = st.columns(2)
    for i, (_, row) in enumerate(df.iterrows()):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(row["Término de negocio"]):
                st.write(f"**Concepto:** {row['Concepto']}")
                st.write(f"**Master Data Steward:** {row['Master Data Steward']}")
                st.write(f"**Sujeto:** {row['Sujeto']}")
                st.write(f"**Capacidad:** {row['Capacidad']}")
                st.write(f"**Proceso de Valor:** {row['Proceso de Valor']}")
                if st.button("👁️ Ver detalle", key=f"btn_{row['Término de negocio']}"):
                    st.session_state.selected_tn = row['Término de negocio']
                    st.session_state.page = 'tn_detail'
                    st.rerun()                
