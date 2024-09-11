import streamlit as st
from filters import apply_filters


def display_explore_tn_page(df):
    st.header("Explorar")

    # Aplicar filtros
    filtered_df = apply_filters(df)
    
    # Mostrar número de resultados
    st.write(f"Mostrando {len(filtered_df)} términos de negocio")

    col1, col2 = st.columns(2)
    for i, (_, row) in enumerate(filtered_df.iterrows()):
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
