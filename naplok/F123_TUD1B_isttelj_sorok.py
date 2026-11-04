"""F123.TUD1B (2) — az ISTENTISZT-001 teljesség-mérésének (#620) blokk-osztályai összesítő jelöltsorként.

Az orkesztrátor döntése a felhasználó felhatalmazásával (2026-11-04), az ALVIL-001 mintájára (DT564): a
`naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv` öt osztálya (a három háló kifejezés nélküli ELTÉRÉS-találatai, a
mérés szerint egyikben sem áll a motívum kifejezése) osztályonként EGY `elutasítva` sort kap a `jeloltek.tsv`-ben:
- `igehely`: az osztály első verse (kanonikus sorrend), a sor ezt mondja („az első itt”);
- `forras_kereses`: „F123 U1 teljesség-mérés, <hálók>, blokk-kizárás (DT564 minta): N vers, az első itt; a lista: …”
  — az N a vers-, nem a sorszám (a blokkfájlban egy vers hálónként külön sor), a napló proveniencia-sorával;
- `indoklas`: olvasói szöveg, „Összesítő sor N versre (az első itt áll): …”;
- `dontes_ref`: a napló és a blokkfájl osztálya.
A versszám a blokkfájlból számolt különböző versek száma; egy vers egyetlen osztályban áll (ellenőrizve).
Írás előtt a meglévő sorok változatlansága ellenőrizve (split('\\t'), `igazolas_migracio.py` minta); eltérésnél, vagy
ha az osztály első verse már jelölt-kulcs, megáll.

    python naplok/F123_TUD1B_isttelj_sorok.py          # szárazon
    python naplok/F123_TUD1B_isttelj_sorok.py --ir
"""
import io
import os
import sys
from collections import OrderedDict, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import general as G  # noqa: E402

MID = 'ISTENTISZT-001'
DATUM = '2026.11.04'
BLOKKFAJL = 'naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv'
NAPLO = 'naplok/F123_teljesseg_ISTENTISZT-001.md'
# a napló 3. szakaszának proveniencia-sora (a kifejezés-mérés és az osztályozás futása)
PROV = ('scope=ISTENTISZT-001 ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (tokensorrend) | '
        'forras=naplok/F123_ISTTELJ_meres.py, naplok/F123_TUD1B_isttelj_sorok.py | ts=2026-11-04T07:34Z')
HALO = OrderedDict([('strong', 'Strong-háló'), ('karoli', 'Károli-szó háló'),
                    ('szotar', 'szótár (BDB H7121, Thayer G1941) háló')])
ZARAS = (' A motívumhoz az a vers tartozik, amelyben a hívás az Úr nevére irányul (a héberben a kárá után a besém és az '
         'Úr neve, a JHVH, a görögben az epikaleó és az ónoma), ezért egyik sem tartozik ide; a teljes lista a lap '
         'készítőinek módszertani naplójában.')
# osztály → (karoli_szo, az indoklás tartalmi mondata); a sorrend a napló 2. szakaszáé
OSZTALY = OrderedDict([
    ('qara_nev_nelkul', ('hív', 'a קָרָא (kárá, hív, kiált) igéje a név, a שֵׁם (sém) nélkül áll a versben: hívás, '
                                'kiáltás vagy meghívás, a név segítségül hívása nélkül.')),
    ('elnevezes_nev', ('nevez', 'a kárá és a sém egy versben áll, de elnevezésként („nevét X-nek nevezte”), nem a név '
                                'segítségül hívásaként.')),
    ('mas_lexema', ('', 'a Károli hív, kiált vagy segítségül szava ezekben a versekben más héber vagy görög szót fordít; '
                        'a motívum szavai nem állnak a versben.')),
    ('kulon_kontextus', ('', 'a kárá és a sém egy versben áll, de nem egy szerkezetben: a hívás nem a névre irányul.')),
    ('besem_JHVH_nelkul', ('', 'a kárá és a besém egy szerkezetben áll, de a név után nem az Úr neve, a JHVH áll, hanem '
                               'névmási rag, más név vagy az elóhím.')),
])


def nyit(ut):
    with io.open(ut, encoding='utf-8', newline='') as f:
        t = f.read()
    nl = '\r\n' if '\r\n' in t else '\n'
    return t.split(nl), nl


def blokkok():
    sorok, _ = nyit(os.path.join(GY, BLOKKFAJL))
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    versek, halok, osztaly_e = defaultdict(set), defaultdict(set), {}
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        assert osztaly_e.setdefault(r['igehely'], r['blokk']) == r['blokk'], r   # egy vers egy osztályban
        versek[r['blokk']].add(r['igehely'])
        halok[r['blokk']].add(r['halo'])
    assert set(versek) == set(OSZTALY), sorted(versek)
    return versek, halok


def main():
    ir = '--ir' in sys.argv
    versek, halok = blokkok()
    sorrend, hiany = G.konyv_sorrend_betolt(), set()
    ut = os.path.join(GY, 'adat', 'jeloltek.tsv')
    sorok, nl = nyit(ut)
    fi = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    fej = sorok[fi].split('\t')
    ix = {n: j for j, n in enumerate(fej)}
    kulcsok = {s.split('\t')[1] for s in sorok[fi + 1:] if s.startswith(MID + '\t')}
    if any(s.startswith(MID + '\t') and 'blokk-kizárás' in s for s in sorok):
        sys.exit('MÁR BEÍRVA: van ISTENTISZT-001 blokk-sor a táblában — nem írok')
    hozza = []
    for osz, (karoli, mondat) in OSZTALY.items():
        lst = sorted(versek[osz], key=lambda v: G.igehely_rendezo_kulcs(v, sorrend, hiany))
        elso, n = lst[0], len(lst)
        assert elso not in kulcsok, (osz, elso)
        assert not (set(lst) & kulcsok), (osz, sorted(set(lst) & kulcsok)[:5])   # a blokk versei nem jelöltek
        r = [''] * len(fej)
        r[ix['id']] = MID
        r[ix['igehely']] = elso
        r[ix['forras_kereses']] = (
            'F123 U1 teljesség-mérés, %s, blokk-kizárás (DT564 minta): %d vers, az első itt; a lista: %s (blokk=%s), '
            '%s | %s' % (', '.join(v for k, v in HALO.items() if k in halok[osz]), n, BLOKKFAJL, osz, NAPLO, PROV))
        r[ix['dontes']] = 'elutasítva'
        r[ix['indoklas']] = 'Összesítő sor %d versre (az első itt áll): %s%s' % (n, mondat, ZARAS)
        r[ix['karoli_szo']] = karoli
        r[ix['datum']] = DATUM
        r[ix['jelolt_tipus']] = 'elofordulas'
        r[ix['dontes_ref']] = '%s 2. szakasz · %s (blokk=%s)' % (NAPLO, BLOKKFAJL, osz)
        hozza.append('\t'.join(r))
        print('%-18s %4d vers, az első: %s' % (osz, n, elso))
    if hiany:   # a blokkfájl nem normalizált könyvneve (pl. „Sir”) a sor végére kerül; az első verset nem érinti
        print('figyelmeztetés: a normalizáló táblában nincs: %s' % ', '.join(sorted(hiany)))
    utolso = max(i for i, s in enumerate(sorok) if s.startswith(MID + '\t'))
    uj = sorok[:utolso + 1] + hozza + sorok[utolso + 1:]
    # a meglévő sorok változatlanok: az új tábla a beszúrt sorok nélkül bájtra az eredeti
    if [s for s in uj if s not in hozza] != sorok or len(uj) != len(sorok) + len(hozza):
        sys.exit('ELTÉRÉS a meglévő sorokban — nem írok')
    if any(len(s.split('\t')) != len(fej) for s in hozza):
        sys.exit('mezőszám-hiba — nem írok')
    print('összesen: %d vers, %d sor' % (sum(len(v) for v in versek.values()), len(hozza)))
    if ir:
        with io.open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write(nl.join(uj))
        print('megírva: adat/jeloltek.tsv (+%d sor)' % len(hozza))


if __name__ == '__main__':
    main()
