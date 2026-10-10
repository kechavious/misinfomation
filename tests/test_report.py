"""The paper must refuse stale or mismatched reference artifacts."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.generate_paper import ROOT, generate, load_reference


class ReportTests(unittest.TestCase):
    def test_published_markdown_matches_verified_reference(self):
        self.assertEqual((ROOT/'docs/paper.md').read_text(), generate())

    def test_corrupt_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT/'results', root/'results', ignore=shutil.ignore_patterns('plots'))
            path = root/'results/csv/summary.csv'
            path.write_bytes(path.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError, 'integrity'):
                load_reference(root)

    def test_changed_design_requires_new_interpretation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'results').mkdir()
            meta = json.loads((ROOT/'results/metadata.json').read_text())
            meta['parameters']['rounds'] = 20
            (root/'results/metadata.json').write_text(json.dumps(meta))
            with self.assertRaisesRegex(ValueError, 'revise the template'):
                load_reference(root)
            meta['parameters']['rounds'] = 10
            meta['model'] = 'one-shot independent cascade'
            (root/'results/metadata.json').write_text(json.dumps(meta))
            with self.assertRaisesRegex(ValueError, 'changed model'):
                load_reference(root)


if __name__ == '__main__':
    unittest.main()
