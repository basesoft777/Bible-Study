"""Olvasói pilot: a bővítés (F60.5, v2) — a repó meglévő adatainak hozzáadása a szó- és vers-lapokhoz.

Az adat.py hívja (nem önálló program). Csak olvas; új adatot nem állít elő: minden érték egy meglévő
tábla sora, a gépi feldolgozás (kulcs-illesztés, tartomány bontása, morfológiai kód feloldása) szabálya
itt olvasható, és a lapon „gépi feldolgozás” jelleget kap. A TSV-t split('\\t')-bel olvassa (csv modul tilos).

Szó-lapok (kulcs: Strong): SDBH/SDGNT domén, SECE_H/SECE_G, OSHL (TWOT, BDB-azonosító), TBESH, LSJ, MCGED,
UBS_DNTG angol jelentések, tW (translationWords).
Vers-lapok: BSB és KJV angol szó szavanként, Nave témák, TIPNR tulajdonnevek, adatréteg (motívum,
kapcsolat, LXX-döntés), LXX versszintű együttelőfordulás és többlet-szakaszok, versszámozási eltérések.

Versszám-kulcsok (a Károli 1908 számozása a kiinduló):
- MT-kulcs: a Karoli_versmegfeleltetes.tsv igehely_mt oszlopa, ha üres, a Károli-szám (a BSB 'mt' számozású).
- KJV-kulcs: ahol az LXX_OS ad szót a versre, annak KJV-oszlopa (kjv_lxx); ahol nem, a szomszédos vers
  eltolása ugyanabban a fejezetben (Zsolt 22:1 → 22:0, a felirat); végső tartalék a versmegfeleltető tábla.
  Ok: a Zsolt 22-re a versmegfeleltető tábla azonosságot ad (Károli 22:2 = KJV 22:2), de a KJV-szöveg
  szerint Károli 22:2 = KJV 22:1; az LXX_OS KJV-oszlopa ezzel egyezik. A tábla hibája nyitott (jelentés)."""
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def _sorok(gy, ut, fejlec=True):
    with open(gy + ut, encoding='utf-8-sig') as fh:
        elso = True
        for s in fh:
            s = s.rstrip('\r\n')
            if not s or s.startswith('#'):
                continue
            if fejlec and elso:
                elso = False
                continue
            yield s.split('\t')


def _tisztit_html(t):
    t = re.sub(r'<\s*br\s*/?\s*>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', '', t)
    return t.replace('\\n', '\n').strip()


# ============================ morfológiai kód feloldása ============================
class MorfKulcs:
    """A Macula (OSHB-stílusú) morfológiai kód magyar feloldása az adat/morf_kulcs_heber.tsv alapján.
    A kód szerkezete szófajonként (a kulcs 'szerkezet' sorai):
      ige: törzs, típus, [személy,] nem, szám, állapot (a participiumnál nincs személy; a főnévi igenévnél
      csak a típus); főnév/melléknév: típus, nem, szám, állapot; névmás/toldalék: típus, személy, nem, szám;
      elöljáró/partikula: típus; kötőszó/határozószó: nincs. Az 'x' helykitöltő kimarad.
    A nyelv (héber/arámi) az adat/morf_nyelv_aramai.tsv-ből jön (xml_id szerint); a hiányzó sor héber."""

    def __init__(self, gy):
        self.t = defaultdict(dict)
        for r in _sorok(gy, 'adat/morf_kulcs_heber.tsv'):
            if len(r) > 4:
                self.t[r[0]][(r[1], r[2])] = r[4]
        self.aramai = {}
        self.ismeretlen = Counter()

    def betolt_nyelv(self, gy, xml_idk):
        for r in _sorok(gy, 'adat/morf_nyelv_aramai.tsv'):
            if len(r) > 3 and r[0] in xml_idk:
                self.aramai[r[0]] = r[3]

    def nyelv(self, xml_id):
        return self.aramai.get(xml_id, 'H')

    def _k(self, poz, kod, nyelv):
        d = self.t[poz]
        return d.get((nyelv, kod)) or d.get(('*', kod))

    def dekodol(self, kod, nyelv='H'):
        if not kod:
            return ''
        sz = kod[0]
        rest = kod[1:]
        elso = self._k('szofaj', sz, nyelv)
        if elso is None:
            self.ismeretlen[kod] += 1
            return ''
        ki = [elso]
        if sz == 'V':
            mezok = ['igetorzs', 'igetipus']
            tip = rest[1:2]
            if tip in ('r', 's'):
                mezok += ['nem', 'szam', 'allapot']
            elif tip in ('a', 'c'):
                mezok += ['allapot']
            else:
                mezok += ['szemely', 'nem', 'szam', 'allapot']
        elif sz in ('N', 'A'):
            mezok = ['tipus_' + sz, 'nem', 'szam', 'allapot']
        elif sz in ('P', 'S'):
            mezok = ['tipus_' + sz, 'szemely', 'nem', 'szam']
        elif sz in ('R', 'T'):
            mezok = ['tipus_' + sz]
        else:
            mezok = []
        for poz, c in zip(mezok, rest):
            if c == 'x':
                continue
            hu = self._k(poz, c, nyelv)
            if hu is None:
                self.ismeretlen[kod] += 1
                ki.append('[%s?]' % c)
                continue
            ki.append(hu + ' személy' if poz == 'szemely' else hu)
        if len(rest) > len(mezok):
            self.ismeretlen[kod] += 1
        return ', '.join(ki)


# ============================ a bővítés fő függvénye ============================
def bovit(C):
    """C: névtér az adat.py-ból (GY, TS, SZAKASZ, KONYV, VERSEK, versek, lapok, gor_lapok, hnorm, STEP_HU, nyelvtani).
    Hozzáadja az új mezőket a versek/lapok/gor_lapok elemeihez; visszaadja (prov_kiegeszites, top, stat)."""
    GY, TS, SZ, KONYV, VERSEK = C.GY, C.TS, C.SZAKASZ, C.KONYV, C.VERSEK
    hnorm = C.hnorm
    stat = {}
    prov = {}

    def sorok(ut, fejlec=True):
        return _sorok(GY, ut, fejlec)

    heber = set(C.lapok)
    gorog = set(C.gor_lapok)
    mind = heber | gorog

    # ------------------------------------------------------------ szó-lapok (kulcs: Strong)
    def tobb(strong):
        return C.lapok[strong] if strong[0] == 'H' else C.gor_lapok[strong]

    # SDBH / SDGNT: szemantikai domén (jelentésenként egy sor)
    fa = {}
    for r in sorok('konkordancia/SDBH_SDGNT_domenfa.tsv'):
        if len(r) > 4:
            fa[(r[0], r[1])] = r[4]
    for fajl, kulcs in (('konkordancia/SDBH_domenek.tsv', 'sdbh'), ('konkordancia/SDGNT_domenek.tsv', 'sdgnt')):
        d = defaultdict(dict)
        szotar = 'SDBH' if kulcs == 'sdbh' else 'SDGNT'
        for r in sorok(fajl):
            if len(r) > 12 and r[0] in mind:
                # a domén-fa szülő-szintjei (a kód 3 jegyes szakaszai: 001, 001002, ...), a levél a 'domen'
                ut = [fa.get((szotar, r[9][:i]), '') for i in range(3, len(r[9]), 3)]
                d[r[0]].setdefault(r[7], {'lexid': r[7], 'domen': r[10], 'domen_kod': r[9], 'glossza': r[11],
                                          'db': int(r[12]) if r[12].isdigit() else 0, 'ut': [x for x in ut if x]})
        for s in mind:
            if s in d:
                tobb(s)['domen'] = sorted(d[s].values(), key=lambda x: (-x['db'], x['lexid']))
        stat[kulcs] = sum(1 for s in mind if s in d and s[0] == ('H' if kulcs == 'sdbh' else 'G'))

    # SECE_H / SECE_G: angol szócikk (TWOT/GK/OSHL-hivatkozásokkal együtt, változatlan szöveg)
    for fajl, kulcs, nyelv in (('konkordancia/SECE_H_teljes.tsv', 'sece_h', 'H'), ('konkordancia/SECE_G_teljes.tsv', 'sece_g', 'G')):
        n = 0
        for r in sorok(fajl):
            if len(r) > 2 and r[0] in mind and r[0][0] == nyelv:
                tobb(r[0])['sece'] = r[2]
                n += 1
        stat[kulcs] = n

    # OSHL lexikális index: TWOT-szám, BDB-azonosító, átírás
    oshl = defaultdict(list)
    for r in sorok('konkordancia/OSHL_lexikalis_index.tsv'):
        if len(r) > 9 and r[0] in heber:
            oshl[r[0]].append({'twot': r[2], 'bdb_id': r[3], 'nyelv': r[4], 'atiras': r[7], 'szofaj': r[8], 'def_en': r[9]})
    for s, lst in oshl.items():
        C.lapok[s]['oshl'] = lst[:6]
        C.lapok[s]['oshl_db'] = len(lst)
    stat['oshl'] = len(oshl)

    # TBESH: bővített Strong-szótár (az eStrong-sorok: dStrong, gloss, jelentés-lista)
    tbesh = defaultdict(list)
    with open(GY + 'konkordancia/TBESH.txt', encoding='utf-8-sig') as fh:
        for s in fh:
            r = s.rstrip('\r\n').split('\t')
            m = re.match(r'^(H\d{4})[a-z]?$', r[0]) if len(r) > 7 else None   # eStrong, pl. H1254a / H1254b
            if m and m.group(1) in heber:
                tbesh[m.group(1)].append({'estrong': r[0], 'dstrong': r[1].strip(), 'rokon': r[2].strip(), 'gloss': r[6],
                                          'jelentes': _tisztit_html(r[7])[:2500]})
    for s, lst in tbesh.items():
        C.lapok[s]['tbesh'] = lst[:8]
        C.lapok[s]['tbesh_db'] = len(lst)
    stat['tbesh'] = len(tbesh)

    # LSJ (görög)
    n = 0
    for r in sorok('konkordancia/LSJ_teljes.tsv'):
        if len(r) > 2 and r[0] in gorog:
            C.gor_lapok[r[0]]['lsj'] = r[2]
            n += 1
    stat['lsj'] = n

    # MCGED (Mounce, görög)
    n = 0
    for r in sorok('konkordancia/MCGED_teljes.tsv'):
        if len(r) > 5 and r[0] in gorog:
            C.gor_lapok[r[0]]['mcged'] = {'gk': r[1], 'gyakorisag': r[4], 'glossza': r[5]}
            n += 1
    stat['mcged'] = n

    # UBS DNTG angol jelentések (görög)
    dntg = defaultdict(list)
    for r in sorok('konkordancia/UBS_DNTG_jelentesek.tsv'):
        if len(r) > 11 and r[0] in gorog:
            dntg[r[0]].append({'lexid': r[4], 'domen': r[7], 'rovid': r[8], 'hosszu': '' if r[9] == '—' else r[9],
                               'glosszak': r[10], 'megjegyzes': '' if r[11] == '—' else r[11]})
    for s, lst in dntg.items():
        C.gor_lapok[s]['ubs_en'] = lst[:12]
        C.gor_lapok[s]['ubs_en_db'] = len(lst)
    stat['ubs_dntg'] = len(dntg)
    # az ÚSZ-helyek (a lapon listázott első öt vers) jelentés-besorolása: UBS_DNTG_referenciak (strong + igehely -> lexid)
    kell_ref = {(g, x['ig']) for g, l in C.gor_lapok.items() for x in l['usz_versek']}
    lex_jel = {x['lexid']: x for lst in dntg.values() for x in lst}
    ref_lex = defaultdict(set)
    for r in sorok('konkordancia/UBS_DNTG_referenciak.tsv'):
        if len(r) > 2 and (r[1], r[2]) in kell_ref:
            ref_lex[(r[1], r[2])].add(r[0])
    n_usz = n_usz_van = 0
    for g, l in C.gor_lapok.items():
        for x in l['usz_versek']:
            n_usz += 1
            x['ubs'] = [{'domen': lex_jel[k]['domen'], 'rovid': lex_jel[k]['rovid']} for k in sorted(ref_lex.get((g, x['ig']), ())) if k in lex_jel][:3]
            n_usz_van += bool(x['ubs'])
    stat['usz_hely'] = n_usz
    stat['usz_hely_ubs'] = n_usz_van

    # tW (translationWords): a strong oszlop '+'-szal elválasztott lista
    tw = defaultdict(list)
    for r in sorok('konkordancia/tW_szocikkek.tsv'):
        if len(r) > 4:
            for s in r[3].split('+'):
                if s in mind:
                    tw[s].append({'tw_id': r[0], 'kategoria': r[1], 'cim': r[2], 'szoveg': r[4].replace('\\n', '\n')})
    tw_cikkek = {}
    for s, lst in tw.items():
        tobb(s)['tw'] = [x['tw_id'] for x in lst[:4]]
        tobb(s)['tw_db'] = len(lst)
        for x in lst[:4]:
            tw_cikkek[x['tw_id']] = x
    stat['tw_h'] = sum(1 for s in tw if s[0] == 'H')
    stat['tw_g'] = sum(1 for s in tw if s[0] == 'G')

    # ------------------------------------------------------------ vers-kulcsok
    inv = defaultdict(list)
    for step, hu in C.STEP_HU.items():
        inv[hu].append(step)
    step_konyv = inv.get(KONYV, [])

    def szam(igehely):
        m = re.match(r'^(\S+) (\d+):(\d+)$', igehely)
        return (int(m.group(2)), int(m.group(3))) if m else None

    def cv(s):
        m = re.match(r'^(\d+):(\d+)$', s or '')
        return (int(m.group(1)), int(m.group(2))) if m else None

    # KJV-kulcs: a kjv_lxx, ennek hiányában a szomszéd vers eltolása
    kjv_cv = {}
    kjv_mod = {}
    eltolas = {}
    for v in C.versek:
        ig = v['igehely']
        k = cv(v['versszam'].get('kjv_lxx'))
        a = szam(ig)
        if k and a:
            kjv_cv[ig] = k
            kjv_mod[ig] = 'LXX_OS KJV-oszlop'
            eltolas[a[0]] = k[1] - a[1]
    for v in C.versek:
        ig = v['igehely']
        if ig in kjv_cv:
            continue
        a = szam(ig)
        if a and a[0] in eltolas:
            kjv_cv[ig] = (a[0], a[1] + eltolas[a[0]])
            kjv_mod[ig] = 'a fejezet eltolása (nincs LXX-szó a versre)'
        else:
            k = cv(v['versszam'].get('kjv'))
            kjv_cv[ig] = k or a
            kjv_mod[ig] = 'versmegfeleltető tábla' if k else 'Károli-szám'
    mt_cv = {}
    for v in C.versek:
        ig = v['igehely']
        mt_cv[ig] = cv(v['versszam'].get('mt')) or szam(ig)

    def kulcs(step, c):
        return '%s.%d.%d' % (step, c[0], c[1])

    # ------------------------------------------------------------ BSB és KJV angol szavak
    mt_kulcsok = {}
    kjv_kulcsok = {}
    for v in C.versek:
        ig = v['igehely']
        mt_kulcsok[ig] = {kulcs(s, mt_cv[ig]) for s in step_konyv}
        kjv_kulcsok[ig] = {kulcs(s, kjv_cv[ig]) for s in step_konyv}
    kell_bsb = set().union(*mt_kulcsok.values()) | set().union(*kjv_kulcsok.values())
    bsb = defaultdict(list)
    for r in sorok('konkordancia/BSB_Strongs.tsv'):
        if len(r) > 6 and r[0] in kell_bsb:
            bsb[r[0]].append({'sz': int(r[1]) if r[1].isdigit() else 0, 'strong': hnorm(r[2]) or r[2], 'szo': r[3],
                              'morf': r[4], 'allapot': r[5], 'szamozas': r[6]})
    kjv = defaultdict(list)
    for r in sorok('konkordancia/KJV_Strongs_teljes.tsv'):
        if len(r) > 4 and r[0] in kell_bsb:
            kjv[r[0]].append({'sz': int(r[1]) if r[1].isdigit() else 0, 'strong': hnorm(r[2]) or r[2], 'szo': r[3], 'morf': r[4]})
    stat['bsb_vers'] = stat['kjv_vers'] = 0
    for v in C.versek:
        ig = v['igehely']
        bk = next((k for k in sorted(mt_kulcsok[ig]) if k in bsb), None)
        kk = next((k for k in sorted(kjv_kulcsok[ig]) if k in kjv), None)
        szavak_b = sorted(bsb[bk], key=lambda x: x['sz']) if bk else []
        szavak_k = sorted(kjv[kk], key=lambda x: x['sz']) if kk else []
        v['angol'] = {
            'bsb': {'kulcs': bk or sorted(mt_kulcsok[ig])[0], 'szamozas': sorted({x['szamozas'] for x in szavak_b}),
                    'szavak': szavak_b},
            'kjv': {'kulcs': kk or sorted(kjv_kulcsok[ig])[0], 'mod': kjv_mod[ig], 'szavak': szavak_k},
        }
        stat['bsb_vers'] += bool(szavak_b)
        stat['kjv_vers'] += bool(szavak_k)

    # ------------------------------------------------------------ Nave (KJV-számozású hivatkozások)
    nave_vers = defaultdict(list)
    nave_fej = defaultdict(list)
    nave_db = 0
    kjv_fejezetek = {c for c, _ in kjv_cv.values()}
    nave_pat = re.compile(r'^(\S+) (\d+)(?::(\d+))?(?:-(?:(\d+):)?(\d+))?$')
    for r in sorok('konkordancia/Nave_basokant.tsv'):
        if len(r) < 11 or not r[7].startswith(KONYV + ' '):
            continue
        m = nave_pat.match(r[7])
        if not m or m.group(1) != KONYV:
            continue
        c1 = int(m.group(2))
        if m.group(3) is None:
            if c1 in kjv_fejezetek:
                nave_fej[c1].append({'tema': r[1], 'cimke': r[5], 'hely': r[7], 'id': r[0]})
            continue
        v1 = int(m.group(3))
        c2 = int(m.group(4)) if m.group(4) else c1
        v2 = int(m.group(5)) if m.group(5) else v1
        tart = (c1, v1) != (c2, v2)
        nave_db += 1
        for v in C.versek:
            if (c1, v1) <= kjv_cv[v['igehely']] <= (c2, v2):
                nave_vers[v['igehely']].append({'tema': r[1], 'cimke': r[5], 'hely': r[7], 'tart': tart, 'id': r[0]})
    stat['nave_vers'] = 0
    for v in C.versek:
        lst = []
        lat = set()
        for x in nave_vers[v['igehely']]:
            k = (x['tema'], x['cimke'], x['hely'])
            if k not in lat:
                lat.add(k)
                lst.append(x)
        v['nave'] = lst
        stat['nave_vers'] += bool(lst)
    nave_fej_ki = {}
    for c, lst in nave_fej.items():
        lat = set()
        ki = []
        for x in lst:
            k = (x['tema'], x['cimke'], x['hely'])
            if k not in lat:
                lat.add(k)
                ki.append(x)
        nave_fej_ki[str(c)] = ki

    # ------------------------------------------------------------ TIPNR (a számozást a vers Strong-számai igazolják)
    szavak_strong = {v['igehely']: {w['strong'] for w in v['heber']} for v in C.versek}
    tip_osszes = tip_illesztett = 0
    for v in C.versek:
        v['tipnr'] = []
    by_kjv = defaultdict(list)
    by_mt = defaultdict(list)
    for v in C.versek:
        by_kjv[kjv_cv[v['igehely']]].append(v)
        by_mt[mt_cv[v['igehely']]].append(v)
    nem_illeszkedo = []
    for r in sorok('konkordancia/TIPNR_kivonat.tsv'):
        if len(r) < 5:
            continue
        m = re.match(r'^(\w+)\.(\d+)\.(\d+)$', r[4])
        if not m or m.group(1) not in step_konyv:
            continue
        c = (int(m.group(2)), int(m.group(3)))
        if c not in by_kjv and c not in by_mt:
            continue
        tip_osszes += 1
        s = hnorm(r[2])
        talalt = None
        for modszer, tabla in (('KJV-szám', by_kjv), ('MT-szám', by_mt)):
            for v in tabla.get(c, []):
                if s and s in szavak_strong[v['igehely']]:
                    talalt = (v, modszer)
                    break
            if talalt:
                break
        if talalt:
            v, modszer = talalt
            if not any(x['nev'] == r[0] and x['strong'] == r[2] for x in v['tipnr']):
                v['tipnr'].append({'nev': r[0], 'valtozat': r[1], 'strong': r[2], 'igehely': r[4], 'illesztes': modszer})
            tip_illesztett += 1
        else:
            nem_illeszkedo.append(r[0] + ' ' + r[4])
    stat['tipnr_osszes'] = tip_osszes
    stat['tipnr_illesztett'] = tip_illesztett
    stat['tipnr_nem_illeszkedo'] = nem_illeszkedo

    # ------------------------------------------------------------ adatréteg: motívum, kapcsolat, LXX-döntés
    pat = re.compile(r'^(\S+) (\d+)(?::(\d+))?(?:-(?:(\d+):)?(\d+))?$')

    def tart(ig):
        m = pat.match(ig or '')
        if not m or m.group(1) != KONYV:
            return None
        c1 = int(m.group(2))
        if m.group(3) is None:
            return (c1, 0), (c1, 9999)
        v1 = int(m.group(3))
        c2 = int(m.group(4)) if m.group(4) else c1
        v2 = int(m.group(5)) if m.group(5) else v1
        return (c1, v1), (c2, v2)

    def metsz(ig, v):
        t = tart(ig)
        a = szam(v['igehely'])
        return bool(t and a and t[0] <= a <= t[1])

    motivum = {}
    for r in sorok('adat/motivumok.tsv'):
        if len(r) > 7:
            motivum[r[0]] = {'cim': r[1], 'ui_cimke': r[2], 'statusz': r[5], 'azonossag': r[8]}
    for v in C.versek:
        v['motivum'] = []
        v['kapcsolat'] = []
        v['lxx_dontes'] = []
    for r in sorok('adat/elofordulasok.tsv'):
        if len(r) > 16:
            for v in C.versek:
                if metsz(r[1], v):
                    v['motivum'].append({'id': r[0], 'igehely': r[1], 'kapcsolodas': r[2], 'pardes_szint': r[3], 'funkcio': r[4],
                                         'gerinc_elem': r[5], 'strong': r[6], 'jelentes_hu': r[11], 'karoli_szo': r[12],
                                         'azonositas': r[13], 'megbizhatosag': r[14], 'proveniencia': r[15], 'igazolas': r[16],
                                         'motivum': motivum.get(r[0], {})})
    for r in sorok('adat/kapcsolatok.tsv'):
        if len(r) > 6:
            for v in C.versek:
                for oszlop, irany in ((0, 'forrás'), (1, 'cél')):
                    if metsz(r[oszlop], v):
                        v['kapcsolat'].append({'forras': r[0], 'cel': r[1], 'id': r[2], 'tipus': r[3], 'funkcio': r[4],
                                               'bizonyossag': r[5], 'pardes_szint': r[6], 'irany': irany,
                                               'motivum': motivum.get(r[2], {})})
    for r in sorok('adat/lxx_dontesek.tsv'):
        if len(r) > 10:
            for v in C.versek:
                if metsz(r[1], v):
                    v['lxx_dontes'].append({'id': r[0], 'lxx_igehely': r[2], 'heber_strong': r[3], 'gorog_lemma': r[4],
                                            'gorog_strong': r[5], 'tipus': r[7], 'megjegyzes': r[8], 'bizonyossag': r[9],
                                            'proveniencia': r[10]})
    stat['motivum_sor'] = sum(len(v['motivum']) for v in C.versek)
    stat['kapcsolat_sor'] = sum(len(v['kapcsolat']) for v in C.versek)
    stat['lxx_dontes_sor'] = sum(len(v['lxx_dontes']) for v in C.versek)

    # ------------------------------------------------------------ LXX versszintű együttelőfordulás, többlet, eltérés
    par = defaultdict(lambda: defaultdict(set))
    for r in sorok('konkordancia/LXX_versszintu_parok.tsv'):
        if len(r) > 3 and r[1] in VERSEK:
            par[r[1]][r[0]].add(r[3])
    stat['lxx_par_vers'] = 0
    for v in C.versek:
        d = par.get(v['igehely'], {})
        v['lxx_par'] = {h: sorted(g) for h, g in sorted(d.items())}
        stat['lxx_par_vers'] += bool(d)
    stat['lxx_par_sor'] = sum(len(g) for v in C.versek for g in v['lxx_par'].values())
    for v in C.versek:
        v['lxx_tobblet'] = []
        v['verzif'] = []
    for r in sorok('konkordancia/LXX_tobblet_szakaszok.tsv'):
        if len(r) > 8:
            for v in C.versek:
                if metsz(r[6], v):
                    v['lxx_tobblet'].append({'szakasz': r[0], 'tipus': r[1], 'kjv': r[2], 'heber': r[3], 'gorog': r[5],
                                             'karoli': r[6], 'karoli_allapot': r[7], 'statusz': r[8]})
    for r in sorok('konkordancia/Verzifikacios_elteres_tabla.tsv'):
        if len(r) > 5:
            for v in C.versek:
                if r[2] == v['igehely']:
                    v['verzif'].append({'step1': r[0], 'step2': r[1], 'karoli': r[2], 'allapot': r[4], 'megjegyzes': r[5]})
    stat['lxx_tobblet_sor'] = sum(len(v['lxx_tobblet']) for v in C.versek)
    stat['verzif_sor'] = sum(len(v['verzif']) for v in C.versek)

    # KJV-kulcs és eltérés a versmegfeleltető táblától: a lapra is kerül
    for v in C.versek:
        ig = v['igehely']
        tab = cv(v['versszam'].get('kjv'))
        v['versszam']['kjv_kulcs'] = '%d:%d' % kjv_cv[ig]
        v['versszam']['kjv_kulcs_forras'] = kjv_mod[ig]
        v['versszam']['tabla_ellentmond'] = bool(tab and tab != kjv_cv[ig])
    stat['kjv_tabla_ellentmondas'] = sum(1 for v in C.versek if v['versszam']['tabla_ellentmond'])

    # ------------------------------------------------------------ proveniencia-sorok
    def p(forras):
        return 'scope=%s | forras=%s | ts=%s' % (SZ, forras, TS)
    prov.update({
        'ubs_usz': 'scope=NT-helyek (a lapon listázott első 5 vers) | forras=konkordancia/UBS_DNTG_referenciak.tsv + UBS_DNTG_jelentesek.tsv (CC BY-SA 4.0) | ts=%s' % TS,
        'sdbh': 'scope=strong | forras=konkordancia/SDBH_domenek.tsv + SDBH_SDGNT_domenfa.tsv (CC BY-SA 4.0) | ts=%s' % TS,
        'sdgnt': 'scope=strong | forras=konkordancia/SDGNT_domenek.tsv + SDBH_SDGNT_domenfa.tsv (CC BY-SA 4.0) | ts=%s' % TS,
        'sece_h': 'scope=strong | forras=konkordancia/SECE_H_teljes.tsv | ts=%s' % TS,
        'sece_g': 'scope=strong | forras=konkordancia/SECE_G_teljes.tsv | ts=%s' % TS,
        'oshl': 'scope=strong | forras=konkordancia/OSHL_lexikalis_index.tsv | ts=%s' % TS,
        'tbesh': 'scope=strong | forras=konkordancia/TBESH.txt | ts=%s' % TS,
        'lsj': 'scope=strong | forras=konkordancia/LSJ_teljes.tsv (CC BY-SA 4.0, Perseus) | ts=%s' % TS,
        'mcged': 'scope=strong | forras=konkordancia/MCGED_teljes.tsv | ts=%s' % TS,
        'ubs_dntg': 'scope=strong | forras=konkordancia/UBS_DNTG_jelentesek.tsv (CC BY-SA 4.0) | ts=%s' % TS,
        'tw': 'scope=strong | forras=konkordancia/tW_szocikkek.tsv (CC BY-SA 4.0) | ts=%s' % TS,
        'bsb': p('konkordancia/BSB_Strongs.tsv; vers-kulcs: MT-szám (gépi illesztés, eszkozok/olvaso_pilot/bovites.py)'),
        'kjv': p('konkordancia/KJV_Strongs_teljes.tsv; vers-kulcs: KJV-szám (LXX_OS KJV-oszlop, eszkozok/olvaso_pilot/bovites.py)'),
        'nave': p('konkordancia/Nave_basokant.tsv; tartomány bontása versekre és KJV-kulcs: eszkozok/olvaso_pilot/bovites.py'),
        'tipnr': p('konkordancia/TIPNR_kivonat.tsv; illesztés: a név Strong-száma a versben (eszkozok/olvaso_pilot/bovites.py)'),
        'morf': p('adat/morf_kulcs_heber.tsv (CC BY 4.0) + adat/morf_nyelv_aramai.tsv; feloldás: eszkozok/olvaso_pilot/bovites.py (gépi feldolgozás)'),
        'motivum': p('adat/elofordulasok.tsv + adat/motivumok.tsv (soronként: a sor saját proveniencia-mezője)'),
        'kapcsolat': p('adat/kapcsolatok.tsv (nincs sor-szintű proveniencia-mező; a tábla fejléke szerint kézi/betolt.py)'),
        'lxx_dontes': p('adat/lxx_dontesek.tsv (soronként: a sor saját proveniencia-mezője)'),
        'lxx_par': p('konkordancia/LXX_versszintu_parok.tsv (versszintű együttelőfordulás, NEM szóillesztés)'),
        'lxx_tobblet': p('konkordancia/LXX_tobblet_szakaszok.tsv'),
        'verzif': p('konkordancia/Verzifikacios_elteres_tabla.tsv'),
    })
    top = {'nave_fejezet': nave_fej_ki, 'tw_cikkek': tw_cikkek}
    return prov, top, stat
