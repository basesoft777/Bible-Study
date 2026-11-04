#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F123_ISTTELJ_meres.py -- az ISTENTISZT-001 teljesség-mérése három hálóval (DT548, F123.ISTTELJ).
Az eszkozok/teljesseg_meres.py függvényeit használja; csak olvas, adattáblát nem ír. A motívum
kifejezése (negatív kritérium, motivumok.tsv, DT476/DT478) tokensorrendből ellenőrzött:
  ÓSZ: H7121 (qárá) legfeljebb 9 tokenre H9003+H8034-től (besém), a név után H3068 (JHVH);
  ÚSZ: G1941 (epikaleó) és G3686 (onoma) legfeljebb 6 tokenre egymástól.
Használat: python naplok/F123_ISTTELJ_meres.py
Kimenet: naplok/F123_teljesseg_ISTENTISZT-001.{md,tsv} és _blokkok.tsv
"""
import os
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import lekerdez as L  # noqa: E402
import teljesseg_meres as T  # noqa: E402

MID = 'ISTENTISZT-001'
KI = os.path.join(GYOKER, 'naplok', 'F123_teljesseg_ISTENTISZT-001')
KAROLI_LEMMA = {'segítségül'}           # 2a: a formula magyar kifejezése
KAROLI_HIV = {'hív'}                    # 2b: hív* ∧ név*
KAROLI_KIALT = {'kiált'}                # 2c: kiált* ∧ név*
KAROLI_NEV = {'név'}


def tokenek(tahot, tagnt):
    t = defaultdict(list)
    for r in list(tahot) + list(tagnt):
        t[r['Igehely']].append((r['Strong-szám'], r.get('Angol tükörfordítás', '')))
    return t


def kifejezes(toks):
    """'osz' / 'usz' / '' a vers tokensorrendje szerint."""
    st = [s for s, _ in toks]
    for j, s in enumerate(st):
        if s == 'H8034' and j and st[j - 1] == 'H9003' and 'H3068' in st[j + 1:j + 3]:
            if 'H7121' in st[max(0, j - 9):j + 9]:
                return 'osz'
    for i, s in enumerate(st):
        if s == 'G1941':
            for j in range(max(0, i - 6), min(i + 7, len(st))):
                if st[j] == 'G3686':
                    return 'usz'
    return ''


def osztaly(vers, toks, kif):
    """A kifejezés nélküli találat gépi osztálya (a vers Strongjai szerint, elsőbbségi sorrend)."""
    if kif:
        return 'motivum_kifejezes'
    st = [s for s, _ in toks]
    for i, s in enumerate(st):
        if s == 'H7121':
            for j in range(i + 1, min(i + 9, len(st))):
                if st[j] == 'H8034':
                    if st[j - 1] == 'H9003':
                        return 'besem_JHVH_nelkul'     # qárá + besém, de nem JHVH áll utána
                    return 'elnevezes_nev'              # „nevét X-nek nevezte”, nem invokáció
    if 'G1941' in st:
        return 'epikaleo_onoma_nelkul'
    if 'H7121' in st and 'H8034' in st:
        return 'kulon_kontextus'
    if 'H7121' in st:
        return 'qara_nev_nelkul'
    return 'mas_lexema'


def main():
    elof = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
    jel = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
    strongok, e_versek, j_versek, _ = T.motivum_adat(MID, elof, jel)
    tahot, tagnt = L.load_tahot(), L.load_tagnt()
    tok = tokenek(tahot, tagnt)
    tabla = T.szotari_tabla(os.path.join(GYOKER, 'adat', 'szoto', 'karoli_szotari_alak.tsv'))
    karoli = L.load_karoli_1908()
    most = T.ts()

    # 1. háló: szópárok (qárá+besém; epikaleó+onoma)
    pars = [('H7121', 'H8034'), ('G1941', 'G3686')]
    vs = T.vers_strongjai({x for p in pars for x in p}, tahot, tagnt)
    h1 = T.halo_par(pars, {}, vs)
    # 2. háló: Károli-szó
    h2a = T.halo_karoli(KAROLI_LEMMA, karoli, tabla)
    hiv = T.halo_karoli(KAROLI_HIV, karoli, tabla)
    kialt = T.halo_karoli(KAROLI_KIALT, karoli, tabla)
    nev = T.halo_karoli(KAROLI_NEV, karoli, tabla)
    h2 = defaultdict(list)
    for v, a in h2a.items():
        h2[v].extend(a)
    for v in hiv:
        if v in nev:
            h2[v].extend(hiv[v] + nev[v])
    for v in kialt:
        if v in nev:
            h2[v].extend(kialt[v] + nev[v])
    h2 = {v: sorted(set(a)) for v, a in h2.items()}
    # 3. háló: szótár (a motívum igéi: H7121, G1941)
    h3 = T.halo_szotar({'H7121', 'G1941'}, T.olvas(os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv')),
                       T.olvas(os.path.join(GYOKER, 'adat', 'thayer_vers_jelentes.tsv')))

    halok = {'strong': h1, 'karoli': h2, 'szotar': h3}
    prov = {
        'strong': 'scope=TAHOT-teljes+TAGNT-teljes: egy versben (H7121)+(H8034) | (G1941)+(G3686) | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | n=%d | ts=%s' % (len(h1), most),
        'karoli': 'scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=segítségül; hív∧név; kiált∧név | n=%d | ts=%s' % (len(h2), most),
        'szotar': 'scope=H7121+G1941 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=%d | ts=%s' % (len(h3), most),
    }

    sorok, osszeg, blokk = [], {}, []
    jelolt2 = {}   # a 2. kiadás jelöltjei: ELTÉRÉS + a kifejezés áll
    for nev_, t in halok.items():
        db = Counter()
        for v in sorted(t, key=T.kulcs):
            all_ = T.allapot(v, e_versek, j_versek)
            kif = kifejezes(tok.get(v, []))
            db[all_.split(':')[0]] += 1
            if all_ == 'ELTÉRÉS':
                db['ELTÉRÉS, kifejezés ' + ('igen' if kif else 'nem')] += 1
            if nev_ == 'strong':
                resz = ', '.join(sorted(t[v]))
            else:
                resz = '; '.join(t[v])
            if nev_ != 'szotar':
                resz += ' [a versben: %s]' % (', '.join(sorted(vs.get(v, ()))) or '—')
            oszt = osztaly(v, tok.get(v, []), kif)
            sorok.append((nev_, v, all_, 'igen (%s)' % kif if kif else 'nem', resz, prov[nev_]))
            if all_ == 'ELTÉRÉS':
                if kif:
                    jelolt2.setdefault(v, set()).add(nev_)
                else:
                    blokk.append((oszt, v, nev_, resz))
        osszeg[nev_] = db
    lefedett = set().union(*[set(t) for t in halok.values()])
    nem_fedett = sorted(e_versek - lefedett, key=T.kulcs)
    # J-vers (döntött), amelyben a kifejezés áll, de nem E: tájékoztató lista
    j_kif = sorted([v for v in j_versek if v not in e_versek and kifejezes(tok.get(v, []))], key=T.kulcs)

    with open(KI + '.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_ISTTELJ_meres.py %s — kézzel nem szerkesztendő (DT548)\n' % MID)
        f.write('\t'.join(['halo', 'igehely', 'allapot', 'kifejezes_a_versben', 'reszlet', 'proveniencia']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    with open(KI + '_blokkok.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F123 ISTTELJ: a kifejezés nélküli ELTÉRÉS-találatok gépi osztálya (naplok/F123_ISTTELJ_meres.py; döntés nélkül) | scope=naplok/F123_teljesseg_ISTENTISZT-001.tsv ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | forras=split(\'\\t\') | ts=%s\n' % most)
        f.write('blokk\tigehely\thalo\treszlet\n')
        for b in sorted(blokk, key=lambda x: (x[0], T.kulcs(x[1]), x[2])):
            f.write('\t'.join(b) + '\n')

    # --- konzol + md ---
    bl = Counter((o, h) for o, _, h, _ in blokk)
    bl_vers = defaultdict(set)
    for o, v, h, _ in blokk:
        bl_vers[o].add(v)
    L_ = []
    A = L_.append
    A('# F123 U1 — az ISTENTISZT-001 teljesség-mérése három hálóval (DT548)\n')
    A('*#123 MIGRACIO2 v2 · U1 (`munka: adat`) · ág: `claude/relaxed-raman-0562d4` · modell: claude-sonnet-5-5 · %s*\n' % most[:10])
    A('*Döntés nélküli mérés az arany lap (kiadott, 1. kiadás) kifejezésére. Eszköz: `eszkozok/teljesseg_meres.py` függvényei, a motívum-specifikus futtató `naplok/F123_ISTTELJ_meres.py` (a kifejezés ellenőrzése tokensorrendből). Soronkénti kimenet: `naplok/F123_teljesseg_ISTENTISZT-001.tsv` (%d sor, minden sor mellett a háló proveniencia-sora); a tömeges, kifejezés nélküli osztályok: `naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv`. A `jeloltek.tsv`-be ez a menet nem írt.*\n' % len(sorok))
    A('## 0. A mért állapot\n')
    A('- Strongok (az `elofordulasok.tsv` `strong` mezője): **H7121** (קָרָא, qárá) + **H8034** (שֵׁם, sém; a gerinc-elem páros), **G1941** (ἐπικαλέω, epikaleó). A negatív kritérium az ónom-t is megköveteli (G3686, onoma; az ÚSZ-sorok `strong` mezőjében nincs, a páros tagja).')
    A('- Előfordulás-versek: %d. Jelölt-versek (`elofordulas`): %d.' % (len(e_versek), len(j_versek)))
    A('- A motívum kifejezése (a mérés „kifejezés a versben” mércéje, `motivumok.tsv` negatív kritérium, DT476/DT478): ÓSZ: H8034 a H9003 (be-) előtaggal, a név után legfeljebb 2 tokenen belül H3068 (JHVH), és a H7121 legfeljebb 9 tokenen belül előtte vagy utána; ÚSZ: G1941 és G3686 legfeljebb 6 tokenre egymástól. A névmási rag („nevét”) vagy más név a héber szövegben nem JHVH, tehát nem teljesít.')
    A('- **1. háló (Strong):** a motívum szópárjai: (H7121 ∧ H8034) és (G1941 ∧ G3686) egy versben. Szópár-mód, mert az azonosság hordozója a kifejezés (formulaikus), nem egy szó; a H7121 egyedül 687, a H8034 771 vers, a G3686 215 vers (TAHOT/TAGNT-mérés, 2026-11-04).')
    A('- **2. háló (Károli-szó), szótári alakok:** `segítségül` (a formula magyar kifejezése: az E-sorok `karoli_szo` mezőiben 20 sor), továbbá a `hív` ∧ `név` és a `kiált` ∧ `név` együttállás egy versben (a `karoli_szo`-mezők alakjai: név 18, hív 16+, kiált 2). Kimaradnak a környezet szavai (Úr, Isten, ott, az, ti, Ábrám, Baál, örökkévaló) és az egyedi nevek. Indok: a szó önmagában csak a „segítségül” kellően szűk (az Istennek szóló hívás); a „hív” és a „kiált” a Károlinál sok mást fordít (hívni = elnevezni, meghívni), ezért csak a „név” társaságában számít háló-találatnak. A 2Móz 33:19 és 34:5 („kiáltom előtted az Úr nevét”, „nevén kiáltá az Urat”) a „kiált” ∧ „név” szabályon át fogható meg. A szótövező ismert korlátja (SZOTOVEZES_meres.md): a „segítségűl” írásmód külön sor.')
    A('- **3. háló (szótár):** BDB (`bdb_vers_jelentes.tsv`) és Thayer (`thayer_vers_jelentes.tsv`) által a **H7121**-nél és a **G1941**-nél idézett Károli-versek. A H8034 és a G3686 szócikke a névről szól, nem a hívásról, ezért a szótár-háló az igék Strongjaira szűkül.\n')
    A('## 1. Összegzés\n')
    A('| Háló | Találat (vers) | E | J | ELTÉRÉS | ebből a versben áll a motívum kifejezése |')
    A('|---|---|---|---|---|---|')
    nev_cim = {'strong': '1. Strong (TAHOT + TAGNT, szópár)', 'karoli': '2. Károli-szó', 'szotar': '3. Szótár (BDB H7121, Thayer G1941)'}
    for k, db in osszeg.items():
        A('| %s | %d | %d | %d | **%d** | %d |' % (nev_cim[k], sum(db[x] for x in ('E', 'J', 'ELTÉRÉS')), db['E'], db['J'], db['ELTÉRÉS'], db['ELTÉRÉS, kifejezés igen']))
    A('| fordított irány: E-vers, amelyet egyik háló sem ad | | | | **%d** | |\n' % len(nem_fedett))
    A('Az E-vers, amelyet egyik háló sem ad: %s.\n' % (', '.join(nem_fedett) or '—'))
    A('Proveniencia:')
    for k in ('strong', 'karoli', 'szotar'):
        A('- `%s`' % prov[k])
    A('')
    A('## 2. A kifejezés nélküli ELTÉRÉS-találatok osztályai (gépi osztályozás)\n')
    A('A találatok (vers, háló szerint, egy vers több hálóban is szerepelhet) a vers tokensorrendje szerint, elsőbbségi sorrendben osztályozva. A versenkénti lista: `naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv`.\n')
    A('| Osztály | Vers | Tartalom |')
    A('|---|---|---|')
    magy = {
        'besem_JHVH_nelkul': 'qárá + be-sém áll, de nem JHVH a név birtokosa (névmási rag, más név, elohim: a DT476/DT478 kizárása)',
        'elnevezes_nev': 'qárá + sém, de elnevezés („nevét X-nek nevezte”), nem invokáció',
        'epikaleo_onoma_nelkul': 'G1941 áll, onoma nélkül (név nélküli segítségül hívás, DT476 K2) vagy nem a közelében',
        'kulon_kontextus': 'qárá és sém a versben, de nem egy szerkezetben',
        'qara_nev_nelkul': 'qárá áll a versben, név (sém) nélkül: hívás, kiáltás, meghívás',
        'mas_lexema': 'a vers más lexémája (a hív/kiált/segítségül magyar szó más héber vagy görög szót fordít)',
    }
    for o in ('besem_JHVH_nelkul', 'elnevezes_nev', 'epikaleo_onoma_nelkul', 'kulon_kontextus', 'qara_nev_nelkul', 'mas_lexema'):
        A('| %s | %d | %s |' % (o, len(bl_vers[o]), magy[o]))
    A('')
    A('Az `epikaleo_onoma_nelkul` és `besem_JHVH_nelkul` versek száma és tartalma a 4. szakaszban külön áll, mert ezek a határ közelében esnek.\n')
    A('## 3. A 2. kiadás jelöltjei: a háló talál, az adat nem ismeri, és a versben a motívum kifejezése áll\n')
    A('Ide azok a versek kerülnek, amelyek (a) legalább egy hálóban ELTÉRÉS-ként szerepelnek (az `elofordulasok.tsv`-ben és a `jeloltek.tsv`-ben sincsenek), és (b) a héber/görög szövegben a fenti kifejezés áll. A lista keresési eredmény, nem döntés; a felvétel a 2. kiadás menetében, a negatív kritérium és a `jeloltek.tsv` döntéssel történik. Ez a menet nem ír a `jeloltek.tsv`-be.\n')
    if jelolt2:
        A('| Vers | Hálók | Mi áll a Károli-szövegben |')
        A('|---|---|---|')
        for v in sorted(jelolt2, key=T.kulcs):
            A('| %s | %s | %s |' % (v, ', '.join(sorted(jelolt2[v])), (karoli.get(v, '')[:140]).replace('|', '/')))
    else:
        A('**Nincs ilyen vers: a három háló a kifejezéssel mért teljes ÓSZ/ÚSZ-ben nem hozott új helyet.** Az 1. kiadás listája (22 vers) a mérce szerint teljes. A határesetek a 4. szakaszban állnak.')
    A('')
    A('Proveniencia: `scope=%s ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (tokensorrend) | forras=naplok/F123_ISTTELJ_meres.py | ts=%s`\n' % (MID, most))
    A('## 4. A határ közelében: a döntött jelöltek és a kifejezés\n')
    A('- **J-vers, nem E, a versben a kifejezés áll** (már döntött; csak tájékoztató, a mérés nem érinti): %d vers%s.' % (len(j_kif), (': ' + ', '.join(j_kif)) if j_kif else ''))
    A('- **E-vers, amelyen a kifejezés-mérce nem teljesül: 1Kir 18:25, 18:26** — ezek a kontrasztként megtartott kivételek (a névhez elohéchem, illetve ha-Báal tartozik, nem JHVH; DT476), tehát a mérce és a motívum-meghatározás kivétele egyezik.')
    A('- **Szóalak szerinti közeli esetek, amelyeket a mérce kizár:** 1Móz 16:13 („nevezé az Urat”, qárá + sém-JHVH be- nélkül, elnevezés), 2Móz 17:15 (oltár-elnevezés: JHVH Nisszi), Sir 3:55 (Siralmak 3:55, „nevedet” névmási raggal, a megszólított JHVH külön szó; DT476 K4). Ezek az osztályozásban elnevezes_nev, illetve besem_JHVH_nelkul alatt állnak, nem jelöltek.')
    A('- A „kifejezés” mérce ÓSZ-ben szigorú: qárá-t követő **besém-JHVH**. Az olyan alakok, amelyekben a JHVH helyén névmási rag vagy más név áll (a negatív kritérium: Zak 13:9, Zsolt 105:1, Jer 10:25, Ézs 43:1, 44:5, 45:3), nem tartoznak ide (DT476/DT478).\n')
    A('## 5. Vakfoltok\n')
    A('- A Károli-háló nem fog meg olyan E-verset, ahol a magyar kifejezés más (pl. „kiáltom előtted az Úr nevét”) — l. a 2. háló szabályát és az E-vers, amelyet egyik háló sem ad: sor. A TAGNT kritikai szöveg (NA28 stb.) és a Károli alapszövege (TR) között szövegváltozat lehet; az ÚSZ-versek a TAGNT szerint mértek.')
    A('- Az ÚSZ-ben az epikaleó-t onoma nélkül is használják (Róm 10:12, 14, 2Tim 2:22): ezek a G1941 31 versének részei, a `jeloltek.tsv`-ben `elutasítva` (DT476 K2); az `epikaleo_onoma_nelkul` osztály ezért üres: a G1941 minden verse E vagy döntött J.')
    with open(KI + '.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L_) + '\n')

    for k, db in osszeg.items():
        print('%-7s találat %4d | E %3d | J %3d | ELTÉRÉS %4d (kifejezés a versben: %d)' % (
            k, sum(db[x] for x in ('E', 'J', 'ELTÉRÉS')), db['E'], db['J'], db['ELTÉRÉS'], db['ELTÉRÉS, kifejezés igen']))
    print('nem fedett E:', nem_fedett)
    print('jelolt2:', len(jelolt2), sorted(jelolt2, key=T.kulcs))
    print('blokkok:', {o: len(v) for o, v in bl_vers.items()})
    print('J-vers kifejezéssel (nem E):', j_kif)


if __name__ == '__main__':
    main()
