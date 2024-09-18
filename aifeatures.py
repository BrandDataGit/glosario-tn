import PyPDF2
import os
from openai import OpenAI
from supabase_config import supabase
from utils import get_associated_data
from datetime import datetime

def extract_pdf_content(pdf_directory):
    content = ""
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(pdf_directory, filename)
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
    return content

# Ejemplo de uso:
# pdf_content = extract_pdf_content('/ruta/a/tu/directorio/de/pdfs')


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
                    {"role": "system", "content": "Eres un analista de negocio experto en metadatos, gestión de información y gobierno de datos."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Prepara el prompt para ChatGPT
    prompt = f"""
    Proporciona retroalimentación sobre el siguiente término de negocio y sus datos asociados,
    considerando únicamente los lineamientos de gobierno de datos proporcionados y con respecto al contexto de negocio proporcionado:

    Contexto proporcionado:
    Capacidad de Negocio: {term_details['capacidad']}
    Sujeto: {term_details['sujeto']}
    Proceso de Valor: {term_details['proceso-valor']}
    Master Data Steward: {term_details['master-data-steward']}
    
    Nombre del Término de Negocio: {term_details['nombre-termino']}
    Concepto del Término de negocio: {term_details['concepto']}
    

    Datos de negocio asociados:
    """

    for data in associated_data:
        prompt += f"""
        - Nombre del dato: {data['dato']}
          Definición del dato: {data['definicion']}
          Tipo de dato: {data['tipo_dato']}
        """

    prompt += f"""
    Lineamientos de gobierno de datos:
    {pdf_content[:1000]}  # Limitamos a 1000 caracteres para no exceder los límites de tokens

    
    Genera retroalimentación, justifica cada inciso:
    1. Lineamientos a revisar en el nombre del Termino de Negocio que si se cumplen.
    2. Lineamientos a revisar en el nombre del Termino de Negocio que no se cumplen.
    3. Lineamientos a revisar en concepto de Términos de Negocio que si se cumplen.
    4. Lineamientos a revisar en concepto de Términos de Negocio que no se cumplen.
    5. La coherencia entre el término y sus datos asociados.
    
    """
    resultado = chat_con_gpt(prompt)

    # Guardar el resultado y la fecha en Supabase
    current_time = datetime.now().isoformat()
    supabase.table('termino-negocio').update({
        'ai_review': resultado,
        'ai_review_date': current_time
    }).eq('Id', term_id).execute()

    return resultado

