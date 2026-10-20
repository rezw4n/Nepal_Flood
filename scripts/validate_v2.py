"""Checks on the built manuscript, Supplementary Information and exports; writes validation_report.json and checksums.csv."""
from pathlib import Path
import hashlib
import json
import re
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DER = ROOT/'data'/'derived'
PAPER = ROOT/'paper'
MS, SI = PAPER/'Nepal_Flood_Damage_Assessment.md', PAPER/'Supplementary_Information.md'


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def section(md, start, end):
    return md.split(start, 1)[1].split(end, 1)[0]


def main():
    ms, si = MS.read_text(encoding='utf-8'), SI.read_text(encoding='utf-8')
    checks = {}

    def check(name, ok, detail=''):
        checks[name] = dict(ok=bool(ok), detail=detail)

    for nm, md in [('manuscript', ms), ('supplement', si)]:
        check(f'{nm}: no unresolved placeholders', not re.search(r'\{\{\w+\}\}', md), re.findall(r'\{\{\w+\}\}', md)[:5])
        check(f'{nm}: no unresolved citations', '[@' not in md)
        bad = re.findall(r'(?<![\w.])(nan|None|NaN)(?![\w.])', md)
        check(f'{nm}: no missing-value tokens', not bad, bad[:5])
        imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', md)
        missing = [i for i in imgs if not (ROOT/i).exists()]
        check(f'{nm}: all images exist', not missing, missing)

    # supplementary items: exist and are first cited in order in the main text
    main_text = ms.split('## References')[0] + ms.split('## Figures')[1]
    for kind, pat in [('Table', r'Supplementary Table (\d+)'), ('Fig.', r'Supplementary Fig\. (\d+)'), ('Note', r'Supplementary Note (\d+)')]:
        seq = []
        for m in re.finditer(pat, main_text):
            k = int(m.group(1))
            if k not in seq:
                seq.append(k)
        check(f'Supplementary {kind}: first citations sequential', seq == sorted(seq) and seq == list(range(1, len(seq) + 1)), seq)
        if kind == 'Note':
            have = sorted(int(x) for x in re.findall(r'### Supplementary Note (\d+)', si))
        else:
            have = sorted(int(x) for x in re.findall(rf'\*\*Supplementary {re.escape(kind)} (\d+) \|', si))
        check(f'Supplementary {kind}: every cited item exists', set(seq) <= set(have) and set(have) <= set(seq), dict(cited=seq, present=have))

    # main figures cited in order
    seqf = []
    for m in re.finditer(r'Fig(?:s)?\. (\d)', ms.split('## Methods')[0].split('## Introduction')[1]):
        k = int(m.group(1))
        if k not in seqf:
            seqf.append(k)
    check('Main figures first cited in order', seqf == sorted(seqf), seqf)
    for stem in [f'figure_{i}_' for i in range(1, 7)] + [f'figure_s{i}_' for i in range(1, 7)]:
        f = list((ROOT/'figures').glob(stem + '*.png'))
        ok = len(f) == 1 and all(f[0].with_suffix(e).exists() for e in ('.pdf', '.svg'))
        check(f'{stem}: png, pdf and svg present', ok, [x.name for x in f])

    # length guidelines (Nature Communications articles)
    abstract = section(ms, '## Abstract', '## Introduction')
    nab = len(abstract.split())
    body = ms.split('## Introduction')[1].split('## Methods')[0]
    nbody = len(re.sub(r'\^[\d,–]+\^', '', body).split())
    nref = len(re.findall(r'^\d+\. ', section(ms, '## References', '## Acknowledgements'), flags=re.M))
    ndisp = len(re.findall(r'^\*\*(Fig\.|Table) \d+ \|', ms, flags=re.M))
    check('Abstract <= 150 words', nab <= 150, nab)
    check('Main text <= 5,000 words', nbody <= 5000, nbody)
    check('Display items <= 10', ndisp <= 10, ndisp)
    check('References <= 90 (project soft limit; check the target journal)', nref <= 90, nref)

    # key numbers against their sources
    inv = pd.read_parquet(DER/'harmonised_inventory.parquet')
    nd, nx = int((inv.max_level >= 1).sum()), int((inv.max_level == 3).sum())
    check('Harmonized totals match inventory', f'{nd:,} damaged buildings' in ms and f'{nx:,} of them destroyed' in ms, (nd, nx))
    s2log = json.loads((ROOT/'sources_ext'/'s2'/'s2_log.json').read_text())
    check('Sentinel-2 scene counts match log', f"{len(s2log['pre'])} scenes" in ms and f"{len(s2log['post'])} scenes" in ms,
          (len(s2log['pre']), len(s2log['post'])))
    auc = pd.read_csv(ROOT/'tables'/'s2_separability_auc.csv')
    a = auc[(auc['index'] == 'ndvi') & auc.target.str.startswith('destroyed vs not')].auc.iloc[0]
    check('Sentinel-2 NDVI AUC matches table', f'{a:.2f}' in ms, round(a, 3))
    env = json.loads((DER/'impacts_results.json').read_text())
    check('Danger-zone counts match results', f"{env['danger_zone_buildings']:,}" in ms, env['danger_zone_buildings'])

    # exports
    outputs = []
    for stem in ('Nepal_Flood_Damage_Assessment', 'Supplementary_Information'):
        for ext in ('md', 'docx', 'pdf', 'html'):
            p = PAPER/f'{stem}.{ext}'
            fresh = p.exists() and p.stat().st_size > 0 and p.stat().st_mtime >= (PAPER/f'{stem}.md').stat().st_mtime
            check(f'{p.name} exists and is newer than its source', fresh)
            outputs.append(p)
    nd = PAPER/'Nepal Flood Document.docx'
    check('Nepal Flood Document.docx exists and is newer than its template',
          nd.exists() and nd.stat().st_mtime >= (PAPER/'templates'/'document_template.md').stat().st_mtime)
    outputs += [nd, PAPER/'Nepal Flood Document.md']
    try:
        from pypdf import PdfReader
        pages = {s: len(PdfReader(str(PAPER/f'{s}.pdf')).pages) for s in ('Nepal_Flood_Damage_Assessment', 'Supplementary_Information')}
    except Exception as e:                                      # pragma: no cover
        pages = {'error': str(e)}
    report = dict(passed=all(c['ok'] for c in checks.values()), checks=checks, pdf_pages=pages,
                  abstract_words=nab, main_text_words=nbody, references=nref, display_items=ndisp)
    (ROOT/'validation_report.json').write_text(json.dumps(report, indent=1, default=str), encoding='utf-8')

    files = outputs + sorted((ROOT/'figures').glob('figure_*')) + sorted((ROOT/'tables').glob('*.csv')) \
        + sorted(DER.glob('*.json')) + sorted((ROOT/'scripts').glob('*.py')) \
        + sorted((PAPER/'templates').glob('*.md')) + [PAPER/'references.json', ROOT/'requirements.txt', ROOT/'rebuild.ps1']
    rows = [dict(file=str(p.relative_to(ROOT)).replace('\\', '/'), bytes=p.stat().st_size, sha256=sha256(p)) for p in files if p.exists()]
    pd.DataFrame(rows).to_csv(ROOT/'checksums.csv', index=False)
    for k, c in checks.items():
        print(('PASS ' if c['ok'] else 'FAIL ') + k + ('' if c['ok'] else f"  -> {c['detail']}"))
    print(f"abstract {nab} words; main text {nbody} words; {nref} references; {ndisp} display items; PDF pages {pages}")
    if not report['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
