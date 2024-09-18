import PyPDF2
import os
from openai import OpenAI
from supabase_config import supabase
from utils import get_associated_data
from datetime import datetime

def extract_pdf_content(pdf_path):
    content = ""
    try:
        # Obtener la ruta absoluta del archivo PDF
        abs_path = os.path.abspath(pdf_path)
        print(f"Intentando abrir el archivo: {abs_path}")
        
        with open(abs_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{pdf_path}'")
    except PyPDF2.errors.PdfReadError:
        print(f"Error: No se pudo leer el archivo PDF '{pdf_path}'")
    except Exception as e:
        print(f"Error inesperado al procesar '{pdf_path}': {str(e)}")
    
    return content

def ai_review(term_id, pdf_content):
    # Configura tu API key de OpenAI
    client = OpenAI(api_key='sk-qN7JYVj6-dkSFR9Qv2d4Sr9YqkUAQOyvzlo5Y_tiUhT3BlbkFJ9f_WcQTtRoou1blxdznIRHe6pQ5ZEaskpDEuWn4g0A')

    # Obtén los detalles del término
    term_response = supabase.table('termino-negocio').select('*').eq('Id', term_id).execute()
    term_details = term_response.data[0] if term_response.data else None

    if not term_details:
        return "No se encontraron detalles para este término."

    # Obtén los datos asociados
    associated_data = get_associated_data(term_id)

    def chat_con_gpt(prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un analista de negocio experto en metadatos, gestión de información y gobierno de datos. Usas lenguaje minimalista y apto para todo publico de la institución."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Prepara el prompt para ChatGPT
    prompt = f"""
    Proporciona retroalimentación sobre el siguiente término de negocio y sus datos asociados (si los hay),
    considerando únicamente los lineamientos de gobierno de datos proporcionados:

    Información de Contexto:
    Capacidad de Negocio: {term_details['capacidad']}
    Sujeto: {term_details['sujeto']}
    Proceso de Valor: {term_details['proceso-valor']}
    Master Data Steward: {term_details['master-data-steward']}
    
    Información del Término de Negocio:
    Nombre: {term_details['nombre-termino']}
    Concepto: {term_details['concepto']}
    

    Datos de negocio asociados:
    """

    if associated_data:
        for data in associated_data:
            prompt += f"""
            - Nombre del dato: {data['dato']}
            Definición del dato: {data['definicion']}
            Tipo de dato: {data['tipo_dato']}
            """
    else:
        prompt += "No hay datos de negocio asociados a este término.\n"

    prompt += f"""
    Lineamientos de gobierno de datos:
    {pdf_content[:1000]}  # Limitamos a 1000 caracteres para no exceder los límites de tokens

    Basándote exclusivamente en los lineamientos de gobierno de datos proporcionados, genera retroalimentación justificada para cada uno de los siguientes puntos:

    1. Lineamientos que SÍ se cumplen en el nombre del Término de Negocio.
    2. Lineamientos que NO se cumplen en el nombre del Término de Negocio.
    3. Lineamientos que SÍ se cumplen en el concepto del Término de Negocio.
    4. Lineamientos que NO se cumplen en el concepto del Término de Negocio.
    5. La coherencia entre el término y sus datos asociados (si los hay).

    Para cada punto, cita el/los lineamientos específicos y explica cómo se cumple o no se cumple.
    """
    print(pdf_content)
    resultado = chat_con_gpt(prompt)

    # Guardar el resultado y la fecha en Supabase
    current_time = datetime.now().isoformat()
    supabase.table('termino-negocio').update({
        'ai_review': resultado,
        'ai_review_date': current_time
    }).eq('Id', term_id).execute()

    return resultado

