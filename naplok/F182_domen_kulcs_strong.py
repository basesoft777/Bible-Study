"""F182 (A12): a szemantikai doménnév fordítási sorainak kulcsa a szó saját Strongjával (`strong` = a szó Strongja, nem
„—”), mert az `adat/forditasok.tsv` `strong` oszlopa STRONG alakú (`teszt_strong_util`). A fordítás szövege nem változik:
a „—” kulcsú sor helyére a lapon álló minden (Strong, doménkód) párra egy sor kerül ugyanazzal a fordítással.

Futtatás: python naplok/F182_domen_kulcs_strong.py [--ir]
TSV: split('\\t') / '\\t'.join(); írás előtt: a nem érintett sorok változatlanok.
"""
import hashlib
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

UT = os.path.join(GYOKER, 'adat', 'forditasok.tsv')


def main(ir):
    szoveg = io.open(UT, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in szoveg else '\n'
    sorok = szoveg.split(nl)
    fej = next(s for s in sorok if s and not s.startswith('#')).split('\t')
    i = {k: fej.index(k) for k in ('szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash')}
    regi = {}
    marad = []
    for s in sorok:
        c = s.split('\t')
        if len(c) > i['mezo'] and c[i['szotar']] in ('SDBH', 'SDGNT') and c[i['strong']] == '—' \
                and c[i['jelentes_szam']] == 'domen':
            regi[(c[i['szotar']], c[i['entry_id']])] = c
            continue
        marad.append(s)
    _, elo = G.tsv_beolvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv'))
    tokenek = LG.motivum_strong_tokenek([r for r in elo if r['id'] == 'HAMART-001'])
    uj, hasznalt = [], set()
    for t in tokenek:
        sz = 'SDBH' if t.startswith('H') else 'SDGNT'
        for kod, label in LG.domen_talalatok(t):
            c = regi.get((sz, kod))
            if c is None:
                continue
            hasznalt.add((sz, kod))
            d = list(c)
            d[i['strong']] = t
            assert d[i['forras_hash']] == hashlib.sha1(label.encode('utf-8')).hexdigest()
            uj.append('\t'.join(d))
    if set(regi) != hasznalt:
        sys.exit('HIBA: fel nem használt régi sor: %r' % sorted(set(regi) - hasznalt))
    vege = marad
    while vege and vege[-1] == '':
        vege = vege[:-1]
    ki = nl.join(vege + uj) + nl
    print('régi „—” kulcsú sor: %d, új Strong-kulcsú sor: %d' % (len(regi), len(uj)))
    if ir:
        io.open(UT, 'w', encoding='utf-8', newline='').write(ki)
        print('kiírva')


if __name__ == '__main__':
    main('--ir' in sys.argv)
