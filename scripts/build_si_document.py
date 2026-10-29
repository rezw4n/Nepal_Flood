"""Supplementary Information for the full-length article (paper/Nepal-Flood-Document-*.docx).

Same content as Supplementary_Information.md, with items renumbered in the order in which the article first cites
them, the workflow figure removed (it is Figure 2 of the article) and US spelling.
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_si import make_md_raw, finalize, ROOT          # noqa: E402
from export_v2 import export                               # noqa: E402

OUT = ROOT/'paper'/'Nepal-Flood-Document-SI-DLC_RA_AB.md'
TMAP = {15: 11, 11: 12, 12: 13, 13: 14, 14: 15}           # old -> new table numbers
FMAP = {6: 1, 5: 2, 2: 3, 3: 4, 4: 5}                      # old -> new figure numbers; old Fig. 1 is Figure 2 of the article
US = [(r'\banalysed\b', 'analyzed'), (r'\banalyse\b', 'analyze'), (r'\bcolour', 'color'), (r'\bColour', 'Color'),
      (r'(?<![_\w])harmonised(?![_\w.])', 'harmonized'), (r'\bharmonisation\b', 'harmonization'),
      (r'\bnormalis', 'normaliz'), (r'\bmodelled\b', 'modeled'), (r'\bmodelling\b', 'modeling'),
      (r'\boptimised\b', 'optimized'), (r'\bmetres\b', 'meters'), (r'\bkilometres\b', 'kilometers'),
      (r'\bcentre\b', 'center'), (r'\blicence\b', 'license'), (r'\bgrey\b', 'gray'), (r'\bbehaviour', 'behavior')]


def renumber(text):
    """Map every 'Supplementary Table/Fig./Note N' (with panel letters and 'N and M' lists); ranges are left alone."""
    out, pos = [], 0
    for m in re.finditer(r'Supplementary (Tables?|Figs?\.|Figures?|Notes?) ', text):
        if m.start() < pos:
            continue
        mp = TMAP if m.group(1).startswith('Table') else FMAP if m.group(1).startswith('Fig') else {}
        out.append(text[pos:m.end()]); pos = m.end()
        while True:
            nm = re.match(r'\d+', text[pos:])
            if not nm or re.match(r'[–-]\d', text[pos + nm.end():]):
                break
            out.append(str(mp.get(int(nm.group(0)), int(nm.group(0))))); pos += nm.end()
            pl = re.match(r'[a-z](?:[,–-][a-z])*', text[pos:])
            if pl:
                out.append(pl.group(0)); pos += pl.end()
            sep = re.match(r'(?: and |, )(?=\d)', text[pos:])
            if not sep:
                break
            out.append(sep.group(0)); pos += sep.end()
    out.append(text[pos:])
    return ''.join(out)


def sort_blocks(section, start):
    """Reorder the blocks of a section that begin with the regex `start` (capturing the item number)."""
    tail = ''
    if section.rstrip().endswith('\\pagebreak'):
        section, tail = section.rstrip()[:-len('\\pagebreak')], '\\pagebreak\n\n'
    parts = re.split('(?m)(?=' + start.replace(r'(\d+)', r'\d+') + ')', section)
    head, blocks = parts[0], parts[1:]
    blocks.sort(key=lambda b: int(re.match(start, b).group(1)))
    return head + ''.join(b.rstrip() + '\n\n' for b in blocks) + tail


def main():
    md = make_md_raw()
    md, n = re.subn(r'!\[Supplementary Figure 1\]\([^)]*\)\n\n\*\*Supplementary Fig\. 1 \|[^\n]*\n\n', '', md)
    assert n == 1, 'workflow figure not found'
    md = md.replace('Supplementary Figs. 1–6', 'Supplementary Figs. 1–5')
    md = md.replace('scripts that accompany the manuscript', 'scripts that accompany the article')
    assert not re.search(r'Supplementary Fig(?:ure|\.) 1\b', md), 'reference to the removed workflow figure'
    md = renumber(md)
    a, b = md.split('## Supplementary Tables', 1)
    b, c = b.split('## Supplementary Figures', 1)
    c, d = c.split('## Supplementary References', 1)
    md = (a + '## Supplementary Tables' + sort_blocks(b, r'\*\*Supplementary Table (\d+) \|')
          + '## Supplementary Figures' + sort_blocks(c, r'!\[Supplementary Figure (\d+)\]') + '## Supplementary References' + d)
    for pat, rep in US:
        md = re.sub(pat, rep, md)
    md, order = finalize(md)
    for kind, n_items in (('Table', 15), ('Fig.', 5)):
        found = [int(x) for x in re.findall(rf'\*\*Supplementary {re.escape(kind)} (\d+) \|', md)]
        assert found == list(range(1, n_items + 1)), (kind, found)
    OUT.write_text(md, encoding='utf-8')
    print(f'wrote {OUT.name}: {len(order)} references')
    export(OUT, OUT.stem, 'Supplementary Information')


if __name__ == '__main__':
    main()
