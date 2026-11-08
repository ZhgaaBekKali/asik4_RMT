"""Retrospective screening ablation on eight real seed candidates, not an efficacy benchmark."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = ('candidate_id', 'candidate', 'year', 'primary_task', 'source_url')

def basic_screen(rows):
    """Baseline 2 checks shape and duplicates, without source interpretation."""
    seen = set()
    result = {}
    for row in rows:
        key = row['candidate_id']
        name = ' '.join(row['candidate'].casefold().split())
        valid = all(str(row.get(k, '')).strip() for k in REQUIRED)
        valid = valid and row['year'].isdigit() and 1900 <= int(row['year']) <= 2026
        valid = valid and row['source_url'].startswith('https://aclanthology.org/')
        valid = bool(valid and name not in seen)
        seen.add(name)
        result[key] = valid
    return result

def evaluate(predictions, reference):
    if predictions.keys() != reference.keys():
        raise ValueError('Candidate identities do not match the reference')
    tp = sum(predictions[k] and reference[k] for k in reference)
    fp = sum(predictions[k] and not reference[k] for k in reference)
    fn = sum(not predictions[k] and reference[k] for k in reference)
    tn = sum(not predictions[k] and not reference[k] for k in reference)
    return dict(n=len(reference), included=tp+fp, tp=tp, fp=fp, fn=fn, tn=tn,
                agreement_percent=100*(tp+tn)/len(reference),
                inclusion_precision=tp/(tp+fp) if tp+fp else None,
                inclusion_recall=tp/(tp+fn) if tp+fn else None)

def run(source, evidence, output):
    with source.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    with evidence.open(encoding='utf-8-sig', newline='') as f:
        decisions = list(csv.DictReader(f))
    ids = [r['candidate_id'] for r in rows]
    if not rows or len(ids) != len(set(ids)):
        raise ValueError('Candidates must be nonempty with unique IDs')
    if len(decisions) != len(ids) or {r['candidate_id'] for r in decisions} != set(ids):
        raise ValueError('Exactly one evidence decision per candidate is required')
    if any(r['decision'] not in {'include', 'exclude'} or not r['reason'].strip() for r in decisions):
        raise ValueError('Evidence decisions need valid labels and reasons')
    reference = {r['candidate_id']:r['decision']=='include' for r in decisions}
    methods = {'B1 inventory retention':dict.fromkeys(ids, True),
               'B2 structural validation':basic_screen(rows),
               'P source reviewed screening':reference.copy()}
    metrics = {name:evaluate(pred, reference) for name,pred in methods.items()}
    predictions = [dict(candidate_id=r['candidate_id'], candidate=r['candidate'], method=name,
                        included=int(pred[r['candidate_id']]), reference_included=int(reference[r['candidate_id']]))
                   for r in rows for name,pred in methods.items()]
    output.mkdir(parents=True, exist_ok=True)
    with (output/'baseline_predictions.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(predictions[0]),lineterminator='\n'); w.writeheader(); w.writerows(predictions)
    with (output/'baseline_metrics.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['method',*next(iter(metrics.values())).keys()],lineterminator='\n')
        w.writeheader();w.writerows(dict(method=k,**v) for k,v in metrics.items())
    sensitive = {k:v for k,v in reference.items() if v}
    result = dict(methods=metrics, sensitivity_retained_candidates={
        name:evaluate({k:pred[k] for k in sensitive},sensitive) for name,pred in methods.items()},
        candidates_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        evidence_sha256=hashlib.sha256(evidence.read_bytes()).hexdigest(),
        interpretation='Retrospective descriptive ablation. Proposed decisions equal the source-reviewed reference by construction. No held-out labels, independent coder, statistical efficacy or generalisation claim.')
    (output/'comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'sources/seed_candidates.csv')
    p.add_argument('--evidence',type=Path,default=ROOT/'sources/screening_evidence.csv')
    p.add_argument('--output-dir',type=Path,default=ROOT/'results')
    a=p.parse_args(); print(json.dumps(run(a.source,a.evidence,a.output_dir),indent=2))
