"""Run analyses three times, tests, and check deterministic analytical output."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
import analyze_datasets
import compare_methods

ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    runs=[]
    for i in range(3):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            dest=Path(tmp)
            analyze_datasets.run(ROOT/'sources/source_observations.json',dest)
            compare_methods.run(ROOT/'sources/seed_candidates.csv',ROOT/'sources/screening_evidence.csv',dest)
            hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.iterdir()) if p.name!='environment.json'}
            runs.append(hashes)
    same=all(r==runs[0] for r in runs)
    analyze_datasets.run(ROOT/'sources/source_observations.json',out)
    compare_methods.run(ROOT/'sources/seed_candidates.csv',ROOT/'sources/screening_evidence.csv',out)
    test=subprocess.run([sys.executable,'-m','unittest','-v','test_analyze_datasets','test_compare_methods'],cwd=ROOT,capture_output=True,text=True)
    (out/'TEST_RESULTS.txt').write_text(test.stdout+test.stderr,encoding='utf-8')
    log=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),runs=3,
             analytical_files_identical=same,excluded_from_byte_comparison=['environment.json'],run_hashes=runs,test_exit_code=test.returncode,
             verification_type='Automated execution by AI assistant on the preparation machine; not independent human reproduction')
    (out/'reproduction_log.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(runs=3,analytical_files_identical=same,test_exit_code=test.returncode),indent=2))
    print(test.stderr)
    return 0 if same and test.returncode==0 else 1

if __name__=='__main__': sys.exit(main())
