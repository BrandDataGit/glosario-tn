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
            with st.expander(f"**{row["Término de negocio"]}**"):
                st.write(f"**Concepto:**  \n" f"{row['Concepto']}")
                #st.write(f"Master Data Steward: **{row['Master Data Steward']}**")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Master Data Steward:</div>
                    <div style='margin-left: 40px;'><strong>{row['Master Data Steward']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Sujeto:</div>
                    <div style='margin-left: 40px;'><strong>{row['Sujeto']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Capacidad:</div>
                    <div style='margin-left: 40px;'><strong>{row['Capacidad']}</strong></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
                st.write(f"  \n")
                st.markdown(
                f"""
                <div style='display: flex;'>
                    <div style='width: 150px;'>Proceso de Valor:</div>
                    <div style='margin-left: 40px;'><strong>{row['Proceso de Valor']}</strong></div>
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
                if st.button("👁️ Ver detalle", key=f"btn_{row['Término de negocio']}**"):
                    st.session_state.selected_tn = row['Término de negocio']
                    st.session_state.page = 'tn_detail'
                    st.rerun()   
            with col5:
                st.write("")
                
            
                
                             
