"""Kiểm tra hợp đồng notebook và phòng tránh rò rỉ dữ liệu."""
import ast
import re
import unittest
from pathlib import Path

import nbformat
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import StratifiedKFold, train_test_split

ROOT = Path(__file__).resolve().parents[1]


class NotebookContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb = nbformat.read(ROOT / "digit_classification.ipynb", as_version=4)
        cls.code = [cell for cell in cls.nb.cells if cell.cell_type == "code"]

    def test_notebook_schema_and_python_syntax(self):
        nbformat.validate(self.nb)
        for cell in self.code:
            compile(cell.source, f"cell:{cell.id}", "exec")

    def test_sixteen_sections_in_required_order(self):
        headings = [int(match.group(1)) for cell in self.nb.cells if cell.cell_type == "markdown"
                    for match in re.finditer(r"^## (\d+)\.", cell.source, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 17)))

    def test_experiment_switch_and_core_functions_are_defined(self):
        assignments = {}
        for cell in self.code:
            for node in ast.parse(cell.source).body:
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assignments[target.id] = node.value.value
        self.assertIsInstance(assignments["RUN_EXPERIMENTS"], bool)
        self.assertFalse(any('raise NotImplementedError' in cell.source for cell in self.code))
        self.assertTrue(any("experiment" in cell.metadata.get("tags", []) for cell in self.code))

    def test_no_top_level_model_fit_before_lock_section(self):
        section = 0
        for cell in self.nb.cells:
            if cell.cell_type == "markdown":
                match = re.search(r"^## (\d+)\.", cell.source, re.MULTILINE)
                if match:
                    section = int(match.group(1))
                continue
            if section >= 15:
                break
            tree = ast.parse(cell.source)
            # Definitions are deferred; calls in support cells must not fit models/test.
            tree.body = [node for node in tree.body if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    method = node.func.attr
                    if method in {"fit", "fit_transform", "predict", "fit_predict"}:
                        self.assertEqual(ast.unparse(node.func), "pca_eda.fit_transform")
                        self.assertEqual(ast.unparse(node.args[0]), "X_train")

    def test_core_selection_signature_has_no_test_input(self):
        functions = {node.name: node for cell in self.code for node in ast.parse(cell.source).body
                     if isinstance(node, ast.FunctionDef)}
        self.assertEqual([arg.arg for arg in functions["choose_model_by_cv"].args.args], ["cv_summary"])
        self.assertIn("measure_final_pipeline", functions)

    def test_saved_notebook_has_no_execution_errors(self):
        for cell in self.code:
            self.assertFalse(any(output.output_type == "error" for output in cell.get("outputs", [])))

    def test_saved_notebook_output_does_not_embed_machine_paths(self):
        for cell in self.code:
            for output in cell.get("outputs", []):
                text = output.get("text", "")
                self.assertIsNone(re.search(r"(?<![\w])[A-Za-z]:[\\/]", text))


class DatasetContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = load_digits()
        cls.X, cls.y = data.data, data.target
        cls.train, cls.test = train_test_split(np.arange(len(cls.y)), test_size=0.2,
                                             stratify=cls.y, random_state=42)

    def test_official_shape_pixel_and_label_domain(self):
        self.assertEqual(self.X.shape, (1797, 64))
        self.assertTrue(np.isfinite(self.X).all())
        self.assertTrue(((0 <= self.X) & (self.X <= 16)).all())
        self.assertTrue((self.X == np.floor(self.X)).all())
        self.assertEqual(set(self.y), set(range(10)))

    def test_no_identical_image_crosses_train_test_or_cv(self):
        keys = [tuple(row) for row in self.X]
        self.assertFalse({keys[i] for i in self.train} & {keys[i] for i in self.test})
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        for train, val in cv.split(self.X[self.train], self.y[self.train]):
            self.assertFalse({keys[self.train[i]] for i in train} & {keys[self.train[i]] for i in val})
            self.assertEqual(set(self.y[self.train[val]]), set(range(10)))


if __name__ == "__main__":
    unittest.main()
