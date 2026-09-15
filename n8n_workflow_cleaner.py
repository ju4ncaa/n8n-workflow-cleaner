from __future__ import annotations

import argparse
import json
import logging
import sys
import uuid
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

WORKFLOW_KEYS_TO_REMOVE = [
    "active",
    "id",
    "tags",
    "pinData",
    "versionId",
    "settings",
    "meta",
    "staticData",
    "shared",
    "triggerCount",
]

NODE_KEYS_TO_REMOVE = ["credentials", "webhookId"]


def clean_workflow_dict(workflow: dict) -> dict:
    """Limpia un dict de workflow de n8n in-place y lo retorna."""
    if not isinstance(workflow, dict):
        raise ValueError("El JSON no tiene la estructura esperada de un workflow (no es un objeto).")

    for key in WORKFLOW_KEYS_TO_REMOVE:
        workflow.pop(key, None)

    nodes = workflow.get("nodes")
    if nodes is not None:
        if not isinstance(nodes, list):
            raise ValueError("El campo 'nodes' no es una lista; el archivo podría estar corrupto.")
        for node in nodes:
            node["id"] = str(uuid.uuid4())
            for key in NODE_KEYS_TO_REMOVE:
                node.pop(key, None)
            if node.get("disabled") is False:
                del node["disabled"]

    return workflow


def unique_output_path(path: Path) -> Path:
    """Si 'path' ya existe, agrega _1, _2, etc. para no sobreescribir."""
    if not path.exists():
        return path
    stem, suffix, parent = path.stem, path.suffix, path.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def clean_n8n_workflow_file(input_path: Path, output_dir: Path | None = None) -> Path | None:
    """Limpia un archivo de workflow y guarda el resultado. Retorna la ruta de salida o None si falló."""
    try:
        with input_path.open("r", encoding="utf-8") as f:
            workflow = json.load(f)

        workflow = clean_workflow_dict(workflow)

        out_dir = output_dir or input_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = unique_output_path(out_dir / f"CLEANED_{input_path.name}")

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)

        log.info("Procesado con éxito: %s -> %s", input_path.name, output_path.name)
        return output_path

    except json.JSONDecodeError as e:
        log.error("%s no es un JSON válido: %s", input_path.name, e)
    except Exception as e:
        log.error("Error procesando %s: %s", input_path.name, e)
    return None


def seleccionar_archivos_gui() -> list[Path]:
    """Abre un diálogo para elegir uno o varios archivos JSON."""
    from tkinter import Tk, filedialog

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    downloads = Path.home() / "Downloads"
    log.info("Seleccionando archivo(s)...")
    archivos = filedialog.askopenfilenames(
        initialdir=str(downloads) if downloads.exists() else None,
        title="Selecciona uno o más workflows de n8n",
        filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
    )
    return [Path(a) for a in archivos]


def main() -> None:
    parser = argparse.ArgumentParser(description="Limpia workflows exportados de n8n.")
    parser.add_argument("archivos", nargs="*", help="Archivos JSON a limpiar (si no se pasan, se abre un diálogo).")
    parser.add_argument("--outdir", help="Carpeta de salida (por defecto: misma carpeta que cada archivo).")
    args = parser.parse_args()

    output_dir = Path(args.outdir) if args.outdir else None

    if args.archivos:
        archivos = [Path(a) for a in args.archivos]
    else:
        archivos = seleccionar_archivos_gui()

    if not archivos:
        log.info("No se seleccionó ningún archivo.")
        sys.exit(0)

    resultados = [clean_n8n_workflow_file(a, output_dir) for a in archivos]
    ok = sum(1 for r in resultados if r is not None)
    log.info("\nListo: %d/%d archivo(s) procesado(s) correctamente.", ok, len(archivos))


if __name__ == "__main__":
    main()