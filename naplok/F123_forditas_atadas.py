"""F123 (ALVIL-001, DT-F123h): a hiányzó fordítások átadó listája a külön Sonnet-menetnek (a #121 eszközével; nem a #123
munkája). Bemenet: `naplok/F123_adat_ALVIL-001_forditas_hiany.tsv` (a hiánylista) és `naplok/F123_adat_ALVIL-001_szotar.tsv`
(a forrásszöveg hossza és SHA-1 előtagja); kimenet: `naplok/F123_forditas_atadas_ALVIL-001.tsv`, a `forditasok.tsv` kulcsával
(szotar, strong, entry_id, jelentes_szam, mezo). A teljes `forras_hash`-t a fordító eszköz a SEMA 2.14 szabálya szerint
maga számolja; a lista az előtagot adja összevetésre. A renderben látható hatás oszlopa a 2026-10-29-i gerinces próbarender
mérése (`naplok/F123_M1_ALVIL-001.md` 5.).

    python naplok/F123_forditas_atadas.py
"""
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIANY = os.path.join(GY, 'naplok', 'F123_adat_ALVIL-001_forditas_hiany.tsv')
SZOTAR = os.path.join(GY, 'naplok', 'F123_adat_ALVIL-001_szotar.tsv')
KI = os.path.join(GY, 'naplok', 'F123_forditas_atadas_ALVIL-001.tsv')
HATAS = {
    ('UBS_DBH', 'H7585', 'glosszak_hu'): 'a lexikonoldal 1. szakaszának UBS-cellája, 63 sor („world of the dead *(fordításra vár)*”)',
    ('UBS_DNTG', 'G0086', 'glosszak_hu'): 'a G0086 UBS-domén sora (12.50 „death *(fordításra vár)*”)',
}


def tsv(ut):
    L = [l.rstrip('\n').rstrip('\r').split('\t') for l in open(ut, encoding='utf-8') if not l.startswith('#')]
    return [dict(zip(L[0], r)) for r in L[1:] if r and r[0]]


def main():
    sz = tsv(SZOTAR)
    ki = []
    for h in tsv(HIANY):
        kulcs = '|'.join([h['szotar'], h['strong'], h['entry_id'], h['jelentes_szam'], h['mezo']])
        s = next((x for x in sz if x.get('forditas_kulcs', '').startswith(kulcs[:len(kulcs) - len(h['mezo']) - 1])
                  and x['strong'] == h['strong']), None)
        s = next((x for x in sz if x['strong'] == h['strong'] and x['forras'] == h['forras'] and
                  (x['kulcs'] == h['entry_id'] or h['entry_id'] in x['kulcs'] or x['kulcs'] in h['entry_id'] or
                   h['jelentes_szam'] in x['kulcs'])), s)
        # F123 (2026-10-29, a fordító session jelzése): a kulcs és a hash a generátor keresése szerint
        strong, hossz, sha = h['strong'], (s or {}).get('hossz', '—'), (s or {}).get('sha1_10', '—')
        forras_szoveg = None
        if h['szotar'] in ('UBS_DBH', 'UBS_DNTG'):
            # lexikon_general.ubs_glossza_cella / forditas_ehhez: (szótár, Strong, lexid, jelentésszám, mező); a forrásszöveg
            # a `glosszak` (glosszak_hu) vagy a `definicio_rovid` (definicio_hu) oszlop (SEMA 2.14)
            oszlop = 'glosszak' if h['mezo'] == 'glosszak_hu' else 'definicio_rovid'
            fajl = os.path.join(GY, 'konkordancia', 'UBS_DBH_jelentesek.tsv' if h['szotar'] == 'UBS_DBH' else 'UBS_DNTG_jelentesek.tsv')
            sor = next(x for x in tsv(fajl) if x['lexid'] == h['entry_id'])
            forras_szoveg = sor[oszlop]
        elif h['szotar'] == 'tW_szocikkek':
            # lexikon_general._tw_cikk_blokk: a kulcs a cikk ELSŐ Strongja (r['strongok'][0]), a forrás a cikk szövege
            sor = next(x for x in tsv(os.path.join(GY, 'konkordancia', 'tW_szocikkek.tsv')) if x['tw_id'] == h['entry_id'])
            strong = [t for t in re.split(r'[+,; ]+', sor['strong']) if t][0]
            forras_szoveg = sor['szoveg']
        if forras_szoveg is not None:
            hossz, sha = str(len(forras_szoveg)), hashlib.sha1(forras_szoveg.encode('utf-8')).hexdigest()
        ki.append([h['szotar'], strong, h['entry_id'], h['jelentes_szam'], h['mezo'], h['forras'], hossz, sha,
                   HATAS.get((h['szotar'], h['strong'], h['mezo']), 'a szerepmátrix blokkja (2. szakasz)')])
    fej = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras', 'forras_hossz', 'forras_sha1', 'hatas_a_lapon']
    with open(KI, 'w', encoding='utf-8', newline='') as f:
        f.write('# F123 ALVIL-001: a fordítási átadó lista (DT-F123h: külön Sonnet-menet, a #121 eszközével) | készítő: '
                'naplok/F123_forditas_atadas.py | proveniencia: scope=ALVIL-001 H7585+G0086 | forras=naplok/F123_adat_ALVIL-001_'
                'forditas_hiany.tsv + naplok/F123_adat_ALVIL-001_szotar.tsv (split) | ts=2026-10-29\n')
        f.write('\t'.join(fej) + '\n')
        for r in ki:
            f.write('\t'.join(r) + '\n')
    print('sor\t%d' % len(ki))
    for r in ki:
        print('\t'.join(r[:5] + r[7:8]))


if __name__ == '__main__':
    main()
