"""Chạy notebook đầy đủ qua kernel thật. Đây là lệnh thực nghiệm offline, không thuộc app."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
for key, folder in {"MPLCONFIGDIR": "matplotlib", "IPYTHONDIR": "ipython",
                    "JUPYTER_RUNTIME_DIR": "jupyter_runtime", "JUPYTER_CONFIG_DIR": "jupyter_config"}.items():
    target = ROOT / "tmp" / folder
    target.mkdir(parents=True, exist_ok=True)
    os.environ[key] = str(target)

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

path = ROOT / 'digit_classification.ipynb'
notebook = nbformat.read(path, as_version=4)
manager = KernelManager(kernel_name='python3')
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(notebook, km=manager, timeout=1800,
                        resources={'metadata': {'path': str(ROOT)}})
try:
    client.execute()
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print('Notebook executed successfully; code cells:', sum(c.cell_type == 'code' for c in notebook.cells))
    for cell in notebook.cells:
        for output in cell.get('outputs', []):
            if output.output_type == 'stream' and ('Run:' in output.text or 'Đã xuất' in output.text):
                print(output.text.strip())
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
