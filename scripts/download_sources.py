"""Archive explicitly listed public sources; validate status, retain request metadata."""
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import requests
import argparse

ROOT = Path(__file__).resolve().parents[1]

def retrieve(item):
    key, url = item
    record = {'id': key, 'url': url, 'retrieved_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        r = requests.get(url, timeout=45, headers={'User-Agent': 'NepalFloodResearch/1.0'})
        ct = r.headers.get('Content-Type', '')
        ext = '.zip' if r.content.startswith(b'PK\x03\x04') else '.pdf' if r.content.startswith(b'%PDF') else '.json' if r.content.lstrip().startswith((b'{', b'[')) else '.html'
        p = ROOT / 'sources' / (key + ext)
        p.write_bytes(r.content)
        record.update(final_url=r.url, status=r.status_code, content_type=ct, bytes=len(r.content),
                      sha256=hashlib.sha256(r.content).hexdigest(), file=str(p.relative_to(ROOT)))
    except requests.RequestException as e:
        record['error'] = str(e)
    return record

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--all',action='store_true',help='Repeat all original URLs in the archived retrieval log')
    args=parser.parse_args()
    log = ROOT / 'sources' / 'retrieval_log.json'
    records = json.loads(log.read_text(encoding='utf-8')) if log.exists() else []
    urls = {r['id']:r['url'] for r in records} if args.all else json.loads((ROOT / 'sources' / 'next_urls.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for r in pool.map(retrieve, urls.items()):
            records.append(r)
            print(json.dumps(r), flush=True)
    log.write_text(json.dumps(records, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
