import json
import uuid
import os
from tkinter import filedialog, Tk

DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads") 
OUTPUT_FOLDER = r'c:\Users\leitmotiv\Downloads'

def clean_n8n_workflow(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)

        keys_to_remove = ['active', 'id', 'tags', 'pinData', 'versionId', 'settings', 'meta']
        for key in keys_to_remove:
            workflow.pop(key, None)

        if 'nodes' in workflow:
            for node in workflow['nodes']:
                node['id'] = str(uuid.uuid4())
                node.pop('credentials', None)
                node.pop('webhookId', None)
                if node.get('disabled') is False:
                    del node['disabled']

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"Procesado con éxito: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

def seleccionar_archivo():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    print("Seleccionando archivo...")
    archivo = filedialog.askopenfilename(
        initialdir=DOWNLOADS_PATH,
        title="Selecciona el workflow de n8n",
        filetypes=(("JSON files", "*.json"), ("all files", "*.*"))
    )
    return archivo

if __name__ == "__main__":
    archivo_entrada = seleccionar_archivo()

    if archivo_entrada:
        nombre_base = os.path.basename(archivo_entrada)
        nombre_salida = f"CLEANED_{nombre_base}"
        ruta_salida = os.path.join(OUTPUT_FOLDER, nombre_salida)
        
        clean_n8n_workflow(archivo_entrada, ruta_salida)
    else:
        print("No se seleccionó ningún archivo.")
