import requests

# URL modificada para descarga directa
sharepoint_url = "https://tecmx-my.sharepoint.com/personal/bh_chavez_tec_mx/_layouts/15/download.aspx?share=EbX6dcSIv6BFgZ0AERAE2v0BK2SlRAHLICGFHAsFv3fVNg"

# Descargar el archivo
def descargar_excel(url):
    response = requests.get(url)
    with open("glosario.xlsx", 'wb') as file:
        file.write(response.content)
    print("Archivo descargado y guardado como 'glosario.xlsx'.")

descargar_excel(sharepoint_url)