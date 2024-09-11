import streamlit as st

def apply_filters(df):
    st.sidebar.header("Filtros")
    
    # Filtro por Sujeto
    sujetos = ["Todos"] + list(df["Sujeto"].unique())
    sujeto_selected = st.sidebar.selectbox("Filtrar por Sujeto", sujetos)
    
    # Filtro por Capacidad
    capacidades = ["Todos"] + list(df["Capacidad"].unique())
    capacidad_selected = st.sidebar.selectbox("Filtrar por Capacidad", capacidades)
    
    # Filtro por Proceso de Valor
    procesos = ["Todos"] + list(df["Proceso de Valor"].unique())
    proceso_selected = st.sidebar.selectbox("Filtrar por Proceso de Valor", procesos)

    # Filtro por Master Data Steward
    master_data_steward = ["Todos"] + list(df["Master Data Steward"].unique())
    master_data_steward_selected = st.sidebar.selectbox("Filtrar por Master Data Steward", master_data_steward)
    
    # Aplicar filtros
    if sujeto_selected != "Todos":
        df = df[df["Sujeto"] == sujeto_selected]
    if capacidad_selected != "Todos":
        df = df[df["Capacidad"] == capacidad_selected]
    if proceso_selected != "Todos":
        df = df[df["Proceso de Valor"] == proceso_selected]
    if master_data_steward_selected != "Todos":
        df = df[df["Master Data Steward"] == master_data_steward_selected]
    
    return df