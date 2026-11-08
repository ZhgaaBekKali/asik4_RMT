"""Validate and analyse a source-linked metadata pilot. Standard library only."""
import argparse
import collections
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parent
FIELDS = ['resource_id','resource','anthology_id','year','primary_task','modality',
          'scale_value','scale_precision','scale_unit','license_status','source_url',
          'accessed_on','evidence_level','scope_note','kazakh_only_count','dataset_version','provenance']
TASKS = {'Speech recognition','Named entity recognition','Text-to-speech',
         'Machine translation','Question answering','LLM evaluation'}
LICENSES = {'unknown','CC BY 4.0','CC BY-SA version unspecified'}

def validate(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError('Input must be a nonempty list of source observations')
    seen = set()
    for number, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f'Row {number}: expected an object')
        for key in FIELDS:
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f'Row {number}: missing or empty {key}')
            row[key] = row[key].strip()
        name = ' '.join(row['resource'].casefold().split())
        for kind, value in [('name', name), ('id', row['resource_id'].casefold()), ('publication',row['anthology_id'])]:
            if (kind,value) in seen:
                raise ValueError(f'Row {number}: duplicate {kind}: {value}')
            seen.add((kind,value))
        if not row['year'].isdigit() or not 1900 <= int(row['year']) <= date.today().year:
            raise ValueError(f'Row {number}: invalid year')
        try:
            size = Decimal(row['scale_value'])
            if not size.is_finite() or size <= 0:
                raise ValueError(f'Row {number}: size must be finite and positive')
        except InvalidOperation as exc:
            raise ValueError(f'Row {number}: invalid numerical size') from exc
        if row['scale_precision'] not in {'exact','approximate','reported','less_than'}:
            raise ValueError(f'Row {number}: invalid scale precision')
        if row['primary_task'] not in TASKS or row['modality'] not in {'text','speech','multimodal'}:
            raise ValueError(f'Row {number}: invalid task or modality')
        if row['license_status'] not in LICENSES:
            raise ValueError(f'Row {number}: invalid license status')
        if row['source_url'] != f"https://aclanthology.org/{row['anthology_id']}/":
            raise ValueError(f'Row {number}: source URL does not match identifier')
        try:
            accessed = date.fromisoformat(row['accessed_on'])
        except ValueError as exc:
            raise ValueError(f'Row {number}: invalid access date') from exc
        if int(row['year']) > accessed.year:
            raise ValueError(f'Row {number}: publication year after access year')
        if row['evidence_level'] != 'publication_metadata_checked':
            raise ValueError(f'Row {number}: unsupported evidence level')
        subset = row['kazakh_only_count']
        if subset != 'unknown' and (not subset.isdigit() or not 0 < int(subset) <= size):
            raise ValueError(f'Row {number}: invalid Kazakh subset count')
    return rows

def write_csv(path, fields, rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

def run(source, output):
    source_bytes=source.read_bytes()
    rows=validate(json.loads(source_bytes.decode('utf-8-sig')))
    tasks=dict(sorted(collections.Counter(r['primary_task'] for r in rows).items()))
    licenses=dict(sorted(collections.Counter(r['license_status'] for r in rows).items()))
    matrix=collections.Counter((r['primary_task'],r['modality']) for r in rows)
    report={
        'record_count':len(rows),'task_counts':tasks,'license_status_counts':licenses,
        'unknown_license_count':licenses.get('unknown',0),
        'scale_totals_computed':False,
        'source_sha256':hashlib.sha256(source_bytes).hexdigest(),
        'warning':'Seven resource metadata records, not corpus samples or an exhaustive census. Study-level candidates are excluded. Publication-reported sizes are not independently recounted. Unknown licence is not proof of no licence. No cross-unit totals or linguistic-quality scores are computed.'}
    output.mkdir(parents=True,exist_ok=True)
    write_csv(output/'dataset_inventory.csv',FIELDS,rows)
    write_csv(output/'task_summary.csv',['primary_task','resource_count'],[dict(primary_task=k,resource_count=v) for k,v in tasks.items()])
    write_csv(output/'task_modality_summary.csv',['primary_task','modality','resource_count'],[dict(primary_task=t,modality=m,resource_count=n) for (t,m),n in sorted(matrix.items())])
    (output/'analysis_output.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    environment={'python':sys.version,'platform':platform.platform(),'dependencies':'Python standard library only','source_sha256':report['source_sha256']}
    (output/'environment.json').write_text(json.dumps(environment,indent=2)+'\n',encoding='utf-8')
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'sources'/'source_observations.json')
    parser.add_argument('--output-dir',type=Path,default=ROOT)
    args=parser.parse_args()
    try:
        print(json.dumps(run(args.source,args.output_dir),indent=2,ensure_ascii=False))
    except (ValueError,OSError) as exc:
        parser.exit(2,f'Error: {exc}\n')

if __name__=='__main__':
    main()
