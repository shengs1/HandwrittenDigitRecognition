"""Đối chiếu số liệu đã lưu bằng phép tính độc lập; không fit hoặc thay mô hình."""
from pathlib import Path
import ast
import hashlib
import json
import unittest

import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]


class ArtifactConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / 'models/registry.json').read_text(encoding='utf-8'))
        cls.artifact_dir = ROOT / 'outputs' / cls.registry['run_id']
        cls.comparison = pd.read_csv(cls.artifact_dir / 'model_comparison.csv').set_index('model')
        cls.predictions = pd.read_csv(cls.artifact_dir / 'test_predictions.csv')
        cls.digits = load_digits()
        cls.train, cls.test = train_test_split(np.arange(len(cls.digits.target)), test_size=0.2,
                                             stratify=cls.digits.target, random_state=42)

    def test_metrics_and_report_csv_match_predictions(self):
        for name in self.registry['models']:
            rows = self.predictions[self.predictions.model == name]
            expected = classification_report(rows.true_label, rows.predicted_label, labels=np.arange(10),
                                             output_dict=True, zero_division=0)
            report = pd.read_csv(self.artifact_dir / f'classification_report_{name}.csv', index_col=0)
            self.assertAlmostEqual(self.comparison.loc[name, 'accuracy'], accuracy_score(rows.true_label, rows.predicted_label))
            for metric, column in [('precision', 'precision_macro'), ('recall', 'recall_macro'), ('f1-score', 'f1_macro')]:
                self.assertAlmostEqual(self.comparison.loc[name, column], expected['macro avg'][metric])
            for label in map(str, range(10)):
                for metric in ['precision', 'recall', 'f1-score', 'support']:
                    self.assertAlmostEqual(report.loc[label, metric], expected[label][metric])
            self.assertEqual(report.loc['accuracy', 'support'], len(rows))
            self.assertAlmostEqual(report.loc['accuracy', 'f1-score'], expected['accuracy'])
            self.assertTrue(report.loc['accuracy', ['precision', 'recall']].isna().all())

    def test_confusion_pairs_and_mistakes_match_predictions(self):
        for name in self.registry['models']:
            rows = self.predictions[self.predictions.model == name]
            matrix = confusion_matrix(rows.true_label, rows.predicted_label, labels=np.arange(10))
            saved_matrix = pd.read_csv(self.artifact_dir / f'confusion_matrix_{name}.csv', index_col=0).to_numpy()
            np.testing.assert_array_equal(saved_matrix, matrix)
            pairs = pd.read_csv(self.artifact_dir / f'confusion_pairs_{name}.csv')
            expected_pairs = {(a, b): int(matrix[a, b]) for a in range(10) for b in range(10)
                              if a != b and matrix[a, b] > 0}
            self.assertEqual({(int(r.true_label), int(r.predicted_label)): int(r.count)
                              for r in pairs.itertuples()}, expected_pairs)
            mistakes = pd.read_csv(self.artifact_dir / f'misclassified_{name}.csv')
            expected = rows.loc[rows.true_label != rows.predicted_label,
                                ['sample_index', 'true_label', 'predicted_label']].reset_index(drop=True)
            pd.testing.assert_frame_equal(mistakes.reset_index(drop=True), expected)

    def test_cv_summary_and_grid_choice_match_saved_folds(self):
        summary = pd.read_csv(self.artifact_dir / 'cv_summary.csv').set_index('model')
        for name in self.registry['models']:
            details = pd.read_csv(self.artifact_dir / f'cv_details_{name}.csv')
            if name == 'logreg_raw':
                values = details.test_f1_macro.to_numpy()
            else:
                best = details.loc[details.mean_test_score.idxmax()]
                values = np.array([best[f'split{i}_test_score'] for i in range(5)])
                pipeline = joblib.load(ROOT / 'models' / self.registry['models'][name]['path'])
                for key, value in ast.literal_eval(best['params']).items():
                    self.assertEqual(pipeline.get_params()[key], value)
            self.assertAlmostEqual(summary.loc[name, 'cv_f1_macro_mean'], values.mean())
            self.assertAlmostEqual(summary.loc[name, 'cv_f1_macro_std'], values.std(ddof=0))
        winner = summary.reset_index().sort_values(['cv_f1_macro_mean', 'model'], ascending=[False, True]).iloc[0]['model']
        self.assertEqual(winner, self.registry['selected_model'])

    def test_registry_scaler_and_test_indices_are_consistent(self):
        for name, entry in self.registry['models'].items():
            path = ROOT / 'models' / entry['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry['sha256'])
            pipeline = joblib.load(path)
            records = self.predictions[self.predictions.model == name]
            np.testing.assert_array_equal(records.sample_index, self.test)
            np.testing.assert_array_equal(records.true_label, self.digits.target[self.test])
            scaler = pipeline.named_steps['scale']
            if name == 'logreg_raw':
                self.assertEqual(scaler, 'passthrough')
            else:
                self.assertEqual(scaler.n_samples_seen_, len(self.train))
                np.testing.assert_allclose(scaler.mean_, self.digits.data[self.train].mean(axis=0), atol=1e-12)
            self.assertEqual(self.comparison.loc[name, 'pipeline_bytes'], path.stat().st_size)

    def test_learning_curve_and_mlp_history_are_consistent(self):
        curve = pd.read_csv(self.artifact_dir / 'learning_curve.csv')
        folds = pd.read_csv(self.artifact_dir / 'learning_curve_folds.csv')
        for row in curve.itertuples():
            group = folds[(folds.model == row.model) & (folds.train_size == row.train_size)]
            self.assertEqual(len(group), 5)
            for prefix in ['train', 'validation']:
                values = group[f'{prefix}_f1_macro']
                self.assertAlmostEqual(getattr(row, f'{prefix}_mean'), values.mean())
                self.assertAlmostEqual(getattr(row, f'{prefix}_std'), values.std(ddof=0))
        pipeline = joblib.load(ROOT / 'models' / self.registry['models']['mlp']['path'])
        history = json.loads((self.artifact_dir / 'mlp_history.json').read_text(encoding='utf-8'))
        clf = pipeline.named_steps['clf']
        np.testing.assert_array_equal(history['loss_curve'], clf.loss_curve_)
        np.testing.assert_array_equal(history['validation_scores'], clf.validation_scores_)
        self.assertEqual(len(history['loss_curve']), history['n_iter'])


if __name__ == '__main__':
    unittest.main()
