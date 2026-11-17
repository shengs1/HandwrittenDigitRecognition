"""Execute the support notebook with a real isolated kernel; never run student experiments."""
import ast
import json
import os
from pathlib import Path
import sys
from textwrap import dedent

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

path = ROOT / "digit_classification.ipynb"
notebook = nbformat.read(path, as_version=4)
flags = [node.value.value for cell in notebook.cells if cell.cell_type == "code"
         for node in ast.parse(cell.source).body if isinstance(node, ast.Assign)
         and any(isinstance(target, ast.Name) and target.id == "RUN_STUDENT_EXPERIMENTS" for target in node.targets)
         and isinstance(node.value, ast.Constant)]
if flags != [False]:
    raise RuntimeError("Support runner requires exactly one RUN_STUDENT_EXPERIMENTS=False assignment")

verification = nbformat.v4.new_code_cell(dedent('''
    assert not RUN_STUDENT_EXPERIMENTS and not experiment_complete
    assert status["student_experiments_completed"] is False
    assert len(status["pending_student_tasks"]) == 9
    assert schema.shape[0] == 65 and not schema["missing_count"].any()
    assert quality["invalid_pixel_cells"] == quality["invalid_labels"] == 0
    assert quality["conflicting_image_groups"] == 0
    assert len(X_train) == 1437 and len(X_test) == 360
    assert len(cv_splits) == 5 and not overlap
    assert all(row["overlap_images"] == 0 for row in fold_rows)
    assert set(class_counts.index) == set(range(10))
    figures = sorted(FIGURES.glob("eda_*.png"))
    assert len(figures) == 6 and all(p.stat().st_size > 1000 for p in figures)
    assert not MODEL_OUT.exists()
    assert not (OUT / "model_comparison.csv").exists()
    assert not (OUT / "selection_lock.json").exists()
    verification_report = {
        "run_id": RUN_ID, "status": "passed_support_only", "data_summary": data_summary,
        "data_quality": quality, "split": split_info, "figures": [p.name for p in figures],
        "cv_fold_audit": fold_rows, "models_trained": 0,
        "model_metrics_available": False, "student_core_tested": False,
        "pca_explained_variance_ratio": ratios.tolist(),
    }
    (OUT / "support_verification.json").write_text(json.dumps(verification_report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SUPPORT_VERIFIED", OUT)
'''))
notebook.cells.append(verification)
manager = KernelManager(kernel_name="python3")
# Không cần đăng ký kernel vào cấu hình người dùng; luôn dùng đúng .venv đang chạy script.
manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
client = NotebookClient(notebook, km=manager, timeout=180,
                        resources={"metadata": {"path": str(ROOT)}})
try:
    client.execute()
    errors = [out for cell in notebook.cells if cell.cell_type == "code"
              for out in cell.outputs if out.output_type == "error"]
    if errors:
        raise RuntimeError(errors)
    for out in verification.outputs:
        if out.output_type == "stream":
            print(out.text.strip())
    notebook.cells.pop()  # Không đưa ô kiểm tra nội bộ vào tài liệu thực nghiệm.
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    images = sum(out.output_type == "display_data" and "image/png" in out.get("data", {})
                 for cell in code_cells for out in cell.outputs)
    print(f"Executed {len(code_cells)} code cells; embedded figures={images}; errors=0; student models=0")
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
