# n8n Workflow Cleaner

Script en Python para limpiar y sanitizar workflows exportados de **n8n** antes de subirlos a GitHub o compartirlos públicamente.

Elimina metadatos innecesarios, credenciales y genera nuevos IDs para los nodos.

## ¿Qué hace?

- Elimina campos del workflow:
  - `active`
  - `id`
  - `tags`
  - `pinData`
  - `versionId`
  - `settings`
  - `meta`
- Regenera el `id` de cada nodo (UUID nuevo)
- Elimina:
  - `credentials`
  - `webhookId`
  - `disabled` (cuando es `false`)
- Guarda un nuevo archivo JSON limpio y formateado

## Requisitos

- Python 3.8 o superior  
- No requiere dependencias externas


## Uso

1. Edita las rutas en el script:

```python
input_file = r'path\to\workflow.json'
output_file = r'path\to\workflow_cleaned.json'
