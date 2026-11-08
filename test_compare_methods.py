import csv
import tempfile
import unittest
from pathlib import Path
import compare_methods as app

class ComparisonTests(unittest.TestCase):
    def setUp(self):
        with (app.ROOT/'sources/seed_candidates.csv').open(encoding='utf-8') as f:
            self.rows=list(csv.DictReader(f))
    def test_structural_baseline_keeps_real_study(self):
        self.assertTrue(app.basic_screen(self.rows)['Study'])
    def test_blank_url_rejected(self):
        self.rows[0]['source_url']=''
        self.assertFalse(app.basic_screen(self.rows)[self.rows[0]['candidate_id']])
    def test_duplicate_case_and_space_rejected(self):
        self.rows[1]['candidate']='  '+self.rows[0]['candidate'].upper()+'  '
        self.assertFalse(app.basic_screen(self.rows)[self.rows[1]['candidate_id']])
    def test_invalid_year_rejected(self):
        self.rows[0]['year']='future'
        self.assertFalse(app.basic_screen(self.rows)[self.rows[0]['candidate_id']])
    def test_metric_denominators(self):
        m=app.evaluate(dict(a=True,b=True,c=False),dict(a=True,b=False,c=True))
        self.assertEqual((m['tp'],m['fp'],m['fn'],m['tn']),(1,1,1,0))
        self.assertEqual(m['inclusion_recall'],0.5)
    def test_mismatched_identity_rejected(self):
        with self.assertRaises(ValueError): app.evaluate(dict(a=True),dict(b=True))
    def test_no_positive_predictions(self):
        self.assertIsNone(app.evaluate(dict(a=False),dict(a=True))['inclusion_precision'])
    def test_real_comparison_and_determinism(self):
        with tempfile.TemporaryDirectory(dir=app.ROOT) as tmp:
            out=Path(tmp)
            result=app.run(app.ROOT/'sources/seed_candidates.csv',app.ROOT/'sources/screening_evidence.csv',out)
            self.assertEqual(result['methods']['B1 inventory retention']['agreement_percent'],87.5)
            self.assertEqual(result['methods']['P source reviewed screening']['included'],7)
            saved={p.name:p.read_bytes() for p in out.iterdir()}
            app.run(app.ROOT/'sources/seed_candidates.csv',app.ROOT/'sources/screening_evidence.csv',out)
            self.assertEqual(saved,{p.name:p.read_bytes() for p in out.iterdir()})

if __name__=='__main__': unittest.main(verbosity=2)
