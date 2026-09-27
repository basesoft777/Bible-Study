"""S0b.3: LXX korpuszszint ujramerese grammatikai szuressel (H7121 x G1941, x G2564).
Csak olvas; a naplok/SZOTAR_S0b_lxx_versszint.tsv-t generalta. Futtatas: a repo
gyokerebol, python naplok/SZOTAR_S0b_lxx_versszint_szkript.py."""
import sys, os, glob
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_tsv(path):
    with open(path, encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f if not l.startswith('#')]
    header = lines[0].split('\t')
    rows = []
    for l in lines[1:]:
        if not l:
            continue
        parts = l.split('\t')
        parts += [''] * (len(header) - len(parts))
        rows.append(dict(zip(header, parts)))
    return rows


gram_rows = read_tsv(os.path.join(ROOT, 'adat', 'grammatikai_strongok.tsv'))
gram_g = set(str(int(r['strong'][1:])) for r in gram_rows if r['strong'].startswith('G'))
print("grammatikai G-strong szam:", len(gram_g))

tahot_rows = read_tsv(os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv'))
h7121_set = set(r['Igehely'] for r in tahot_rows if r['Strong-szám'] == 'H7121')
print("H7121 Karoli-igehely (TAHOT_kivonat):", len(h7121_set))

lxx_files = glob.glob(os.path.join(ROOT, 'konkordancia', 'LXX_OS', '*.tsv'))
verse_strongs = {}
covered_verses = set()
for fp in lxx_files:
    for r in read_tsv(fp):
        kv = r.get('igehely_karoli', '')
        if kv in h7121_set:
            covered_verses.add(kv)
            s = r.get('strong', '')
            if s:
                verse_strongs.setdefault(kv, []).append(s)

print("LXX_OS-ben megtalalhato H7121-vers:", len(covered_verses))
print("Nem talalhato:", len(h7121_set) - len(covered_verses))

verse_unique = {v: set(verse_strongs.get(v, [])) for v in covered_verses}


def talalati_arany(codes_map, target_strong):
    return sum(1 for v in covered_verses if target_strong in codes_map[v])


raw_1941 = talalati_arany(verse_unique, '1941')
raw_2564 = talalati_arany(verse_unique, '2564')
total_unique_codes = sum(len(s) for s in verse_unique.values())
all_counter = Counter()
for v in covered_verses:
    all_counter.update(verse_unique[v])

print()
print("NYERS (szuretlen), verzenkent egyedi kod:")
print("  G1941:", raw_1941, "/", len(covered_verses), "=%.1f%%" % (100 * raw_1941 / len(covered_verses)))
print("  G2564:", raw_2564, "/", len(covered_verses), "=%.1f%%" % (100 * raw_2564 / len(covered_verses)))
print("  atlagos egyedi Strong/vers:", round(total_unique_codes / len(covered_verses), 2))
print("  top 10:", all_counter.most_common(10))

verse_unique_filt = {v: (verse_unique[v] - gram_g) for v in covered_verses}
filt_1941 = talalati_arany(verse_unique_filt, '1941')
filt_2564 = talalati_arany(verse_unique_filt, '2564')
total_filt_unique = sum(len(s) for s in verse_unique_filt.values())
filt_counter = Counter()
for v in covered_verses:
    filt_counter.update(verse_unique_filt[v])

print()
print("SZURT (grammatikai G-strong nelkul):")
print("  G1941:", filt_1941, "/", len(covered_verses), "=%.1f%%" % (100 * filt_1941 / len(covered_verses)))
print("  G2564:", filt_2564, "/", len(covered_verses), "=%.1f%%" % (100 * filt_2564 / len(covered_verses)))
print("  atlagos egyedi Strong/vers:", round(total_filt_unique / len(covered_verses), 2))
print("  top 10:", filt_counter.most_common(10))

zaj_db = total_unique_codes - total_filt_unique
print()
print("Zaj arany: %d/%d = %.1f%%" % (zaj_db, total_unique_codes, 100 * zaj_db / total_unique_codes))
