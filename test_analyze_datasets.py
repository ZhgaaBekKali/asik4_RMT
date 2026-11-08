"""Synthetic mutations are validation fixtures, never research observations."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import analyze_datasets as app

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads((app.ROOT/'sources/source_observations.json').read_text(encoding='utf-8'))

    def reject(self, field, value):
        self.rows[0][field]=value
        with self.assertRaises(ValueError): app.validate(self.rows)

    def test_empty_input(self):
        with self.assertRaises(ValueError): app.validate([])
    def test_missing_field(self):
        del self.rows[0]['resource']
        with self.assertRaisesRegex(ValueError,'resource'): app.validate(self.rows)
    def test_blank_field(self): self.reject('source_url','  ')
    def test_duplicate_name_normalized(self):
        self.rows[1]['resource']='  KAZAKH   SPEECH CORPUS (KSC)  '
        with self.assertRaisesRegex(ValueError,'duplicate name'): app.validate(self.rows)
    def test_duplicate_id(self):
        self.rows[1]['resource_id']=self.rows[0]['resource_id']
        with self.assertRaisesRegex(ValueError,'duplicate id'): app.validate(self.rows)
    def test_bad_year(self): self.reject('year','20xx')
    def test_future_year(self): self.reject('year','9999')
    def test_bad_size(self): self.reject('scale_value','many')
    def test_negative_size(self): self.reject('scale_value','-1')
    def test_zero_size(self): self.reject('scale_value','0')
    def test_nan_size(self): self.reject('scale_value','NaN')
    def test_infinite_size(self): self.reject('scale_value','Infinity')
    def test_bad_precision(self): self.reject('scale_precision','unknown')
    def test_bad_task(self): self.reject('primary_task','Other')
    def test_bad_license(self): self.reject('license_status','free')
    def test_bad_date(self): self.reject('accessed_on','2026-02-30')
    def test_wrong_url(self): self.reject('source_url','https://example.com/')
    def test_bad_subset(self): self.reject('kazakh_only_count','999999')
    def test_outputs_and_reproducibility(self):
        with tempfile.TemporaryDirectory(dir=app.ROOT) as tmp:
            output=Path(tmp);source=app.ROOT/'sources/source_observations.json'
            result=app.run(source,output)
            self.assertEqual(result['record_count'],7)
            self.assertEqual(result['task_counts']['LLM evaluation'],2)
            self.assertEqual(result['unknown_license_count'],4)
            self.assertFalse(result['scale_totals_computed'])
            files=['dataset_inventory.csv','analysis_output.json','task_summary.csv','task_modality_summary.csv']
            saved={p:(output/p).read_bytes() for p in files}
            app.run(source,output)
            self.assertEqual(saved,{p:(output/p).read_bytes() for p in files})
            self.assertNotIn(b'\r\r\n',saved['task_summary.csv'])
    def test_cli_different_working_directory(self):
        with tempfile.TemporaryDirectory(dir=app.ROOT) as tmp:
            r=subprocess.run([sys.executable,str(app.ROOT/'analyze_datasets.py'),'--output-dir',tmp],cwd=app.ROOT.parent,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout)['record_count'],7)
    def test_cli_invalid_input_no_outputs(self):
        with tempfile.TemporaryDirectory(dir=app.ROOT) as tmp:
            root=Path(tmp);source=root/'bad.json';source.write_text('[]',encoding='utf-8')
            r=subprocess.run([sys.executable,'-O',str(app.ROOT/'analyze_datasets.py'),'--source',str(source),'--output-dir',str(root/'out')],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
            self.assertIn('nonempty',r.stderr)
            self.assertFalse((root/'out').exists())

if __name__=='__main__': unittest.main(verbosity=2)
