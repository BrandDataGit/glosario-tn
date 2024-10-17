import streamlit as st
import pandas as pd
from supabase_config import supabase
from utils import get_capacidad_id, normalize_string, is_valid_name

def import_terms_from_excel():
    st.subheader("Importar términos de negocio desde Excel")

    # Subir archivo Excel
    uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Verificar que las columnas requeridas estén presentes
            required_columns = [
                "Sujeto", "DataSteward", "Capacidad", "Proceso de valor",
                "Término de negocio", "Concepto", "Sinónimo1", "Sinonimo2", "Sinonimo3", "Origen"
            ]
            
            if not all(col in df.columns for col in required_columns):
                st.error("El archivo Excel no contiene todas las columnas requeridas.")
                return

            # Mostrar vista previa de los datos
            st.write("Vista previa de los datos:")
            st.dataframe(df.head())

            if st.button("Importar términos"):
                import_results = import_terms(df)
                st.write(import_results)

        except Exception as e:
            st.error(f"Error al leer el archivo Excel: {str(e)}")

def import_terms(df):
    results = {"éxitos": 0, "errores": []}

    for index, row in df.iterrows():
        try:
            # Normalizar y validar el nombre del término
            nombre_termino = row["Término de negocio"].strip()
            if not is_valid_name(nombre_termino):
                raise ValueError(f"El nombre del término '{nombre_termino}' contiene caracteres no válidos.")

            # Verificar si el término ya existe
            existing_term = supabase.table("termino-negocio").select("Id").eq("nombre-termino", nombre_termino).execute()
            if existing_term.data:
                raise ValueError(f"Ya existe un término de negocio con el nombre '{nombre_termino}'.")

            # Verificar si existe un dato de negocio con el mismo nombre
            existing_data = supabase.table("dato-negocio").select("id").eq("dato", nombre_termino).execute()
            if existing_data.data:
                raise ValueError(f"Ya existe un dato de negocio con el nombre '{nombre_termino}'.")

            # Obtener el ID de la capacidad
            capacidad_id = get_capacidad_id(row["Capacidad"])
            if capacidad_id is None:
                raise ValueError(f"No se encontró la capacidad '{row['Capacidad']}'.")

            # Preparar los sinónimos
            sinonimos = ", ".join(filter(None, [row.get(f"Sinónimo{i}", "").strip() for i in range(1, 4)]))

            # Insertar el nuevo término
            new_term = {
                "nombre-termino": nombre_termino,
                "concepto": row["Concepto"],
                "sujeto": row["Sujeto"],
                "proceso-valor": row["Proceso de valor"],
                "capacidad_id": capacidad_id,
                "master-data-steward": row["DataSteward"],
                "sinonimos": sinonimos,
                "origen": row["Origen"],
                "estatus": "captura"
            }

            response = supabase.table("termino-negocio").insert(new_term).execute()
            if response.data:
                results["éxitos"] += 1
            else:
                raise ValueError("Error al insertar el término en la base de datos.")

        except Exception as e:
            results["errores"].append(f"Fila {index + 2}: {str(e)}")

    return f"Importación completada. {results['éxitos']} términos importados exitosamente. {len(results['errores'])} errores encontrados.\n\nErrores:\n" + "\n".join(results["errores"])

# Agregar esta función a la página principal
def add_import_terms_to_main():
    if st.sidebar.button("Importar términos desde Excel"):
        st.session_state.page = 'import_terms'
        st.rerun()