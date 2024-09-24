import PyInstaller.__main__
import os
import sys

# Obtén la ruta al directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define las rutas a los archivos principales y recursos
main_file = os.path.join(current_dir, 'main.py')
pdf_dir = os.path.join(current_dir, 'conocimiento')
env_file = os.path.join(current_dir, '.env')

# Crea un archivo temporal que iniciará Streamlit
bootstrap_file = os.path.join(current_dir, 'bootstrap.py')
with open(bootstrap_file, 'w') as f:
    f.write('''
import streamlit.web.bootstrap
import sys
import os

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "main.py"]
    sys.path.insert(0, os.path.dirname(__file__))
    streamlit.web.bootstrap.run(sys.argv, 'streamlit run', 'main.py', '')
''')

# Configura los argumentos para PyInstaller
pyinstaller_args = [
    '--name=GlosarioTNApp',
    '--onefile',
    '--noconsole',
    '--add-data', f'{pdf_dir}:conocimiento',
    '--add-data', f'{env_file}:.', 
    '--add-data', f'{main_file}:.',
    '--hidden-import=streamlit',
    '--hidden-import=pandas',
    '--hidden-import=supabase',
    '--hidden-import=dotenv',
    '--hidden-import=streamlit.web.bootstrap',
    '--collect-all=streamlit',
    '--collect-all=altair',
    '--collect-all=pandas',
    '--collect-all=numpy',
    bootstrap_file
]

# Ejecuta PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

# Limpia el archivo temporal
os.remove(bootstrap_file)

print("Compilación completada. El ejecutable se encuentra en el directorio 'dist'.")