"""F182 (3. menet; A11, A12 — `sablonok/KESZ_LAP_KOVETELMENY.md` K60, K11): a HAMART-001 lapján álló tW-szócikkcímek és
szemantikai doménnevek magyar sora a fordítási gyorsítótárba (`adat/forditasok.tsv`, SEMA 2.14).

Kulcsok (a feloldó: `eszkozok/glossza_lexikon_forditas.tovabbi_forras`):
  tW_szocikkek | <a cikk első Strongja> | <tw_id> | cim   | glosszak_hu — forrás: a `tW_szocikkek.tsv` `cim` oszlopa;
  SDBH / SDGNT | —                       | <domen_kod> | domen | glosszak_hu — forrás: a `*_domenek.tsv` `domen` oszlopa.
A fordítás Sonnet-subagent munkája (claude-sonnet-5-5, saját kiírt modellnév; a kérés szövege a
`naplok/F182_jelentes.md` 3. menetében), mérés nélkül; ami már le van fordítva, nem fordul újra (a lista csak a hiányzó kulcsokat adta).

Használat: python naplok/F182_cim_forditas_betolt.py <cimek.json> <cimek_hu.json> --modell <név> [--ir]
TSV: split('\\t') / '\\t'.join(); írás előtt: a meglévő sorok változatlanok, csak új sor kerül a végére.
"""
import hashlib
import io
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import glossza_lexikon_forditas as GLF  # noqa: E402

UT = os.path.join(GYOKER, 'adat', 'forditasok.tsv')


def main():
    be, hu, ir = sys.argv[1], sys.argv[2], '--ir' in sys.argv
    modell = sys.argv[sys.argv.index('--modell') + 1]
    kerdes = json.load(io.open(be, encoding='utf-8'))
    valasz = {x['id']: x['hu'].strip() for x in json.load(io.open(hu, encoding='utf-8'))}
    if set(valasz) != {x['id'] for x in kerdes}:
        sys.exit('HIBA: a válasz kulcsai nem egyeznek a kérésével')
    szoveg = io.open(UT, encoding='utf-8', newline='').read()
    sorok = szoveg.split('\n')
    fej = next(s for s in sorok if s and not s.startswith('#')).rstrip('\r').split('\t')
    crlf = sorok[1].endswith('\r') if len(sorok) > 1 else False
    meglevo = {tuple(s.rstrip('\r').split('\t')[:5]) for s in sorok if s and not s.startswith('#')}
    uj = []
    cache = {}
    for x in kerdes:
        kulcs = x['id'].split('|')
        if tuple(kulcs) in meglevo:
            continue
        sor = dict(zip(('szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo'), kulcs))
        forras = GLF.forras_szoveg(sor, cache=cache)
        if forras != x['en']:
            sys.exit('HIBA: a feloldó forrásszövege eltér: %s (%r ≠ %r)' % (x['id'], forras, x['en']))
        h = hashlib.sha1(forras.encode('utf-8')).hexdigest()
        r = dict(sor, forras_hash=h, forditas_hu=valasz[x['id']], allapot='sonnet', modell=modell, datum='2026.11.11',
                 terminologia_verzio='v5',
                 megjegyzes='F182 3. menet (A11/A12: a tW-szócikk címe, illetve a szemantikai domén neve; general-purpose '
                            'subagent %s, köteg: naplok/F182_cim_forditas_betolt.py)' % modell)
        uj.append('\t'.join(r.get(k, '') for k in fej))
    vege = szoveg if szoveg.endswith('\n') else szoveg + ('\r\n' if crlf else '\n')
    ki = vege + ('\r\n' if crlf else '\n').join(uj) + ('\r\n' if crlf else '\n')
    # összevetés: a meglévő tartalom változatlan előtag
    assert ki.startswith(szoveg.rstrip('\r\n'))
    print('új sor: %d' % len(uj))
    if ir:
        io.open(UT, 'w', encoding='utf-8', newline='').write(ki)
        print('kiírva')


if __name__ == '__main__':
    main()
