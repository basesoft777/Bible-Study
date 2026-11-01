"""F150 M0 mérés — a gépi előszűrő (a gerinc-szókapcsolat hiánya -> `valoszinu_ki`) próbája a meglévő döntéseken.

Mit mér: a `jeloltek.tsv` minden eldöntött (`beépítve` / `elutasítva`), `elofordulas` típusú sorára megnézi, hogy a
jelölt versében (versszakasz-tartománynál az összes versben, `lexikon_general.igehely_lista`) megvan-e a motívum legalább
egy gerinc-szókapcsolata (az `elofordulasok.tsv` `strong` mezőinek kombinációi, a nyelvtani Strongok — a
`grammatikai_strongok.tsv` és a H9xxx — kiszűrve). A vers Strong-halmaza: `szerep_karoli.vers_strongok` (TAHOT+TAGNT,
a kulcs a Károli-vers, F85); ezért a STEPBible-alakú datasetek normalizálása (`Konyv_normalizalo_tabla.tsv`) itt nem kell.

HORDOZÓ-SZŰRÉS: `valoszinu_ki` csak a `motivumok.tsv` `azonossag_tipusa` = lexikai / formulaikus motívumon; máshol
`vizsgalando`. A szkript MINDKÉT változatot kiszámolja (hordozó-szűrés nélkül és vele), és a próba négy változatát is
(egyezés: teljes kombináció / bármely tagja; keresés: egy versben / a tartomány összesített halmazában).

Csak olvas: az `adat/*.tsv`-t és a `konkordancia/`-t nem írja. TSV: split('\\t'), a csv modul nélkül.
Futtatás: python naplok/JELOLT_ELOSZURES_meres.py [--reszletes]
"""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import szerep_karoli as SZK  # noqa: E402
import lexikon_general as LG  # noqa: E402  (csak importálva, nem módosítva)

ADAT = os.path.join(GYOKER, 'adat')
LEXIKAI_HORDOZO = frozenset({'lexikai', 'formulaikus'})

# A 12 ismert hamis kizárás a brief 2. szakaszából. A brief az ANTROP-001 négy sorát két tartományként (Luk 1:46-47,
# 1Kor 2:14-15) nevezi meg, de a jeloltek.tsv-ben versenként külön sor áll: 3 + 4 + 5 = 12.
ISMERT_12 = [
    ('MENNY-001', 'Júd 1:6'), ('MENNY-001', 'Júd 1:14-15'), ('MENNY-001', '2Pét 2:4-5'),
    ('ANTROP-001', 'Luk 1:46'), ('ANTROP-001', 'Luk 1:47'), ('ANTROP-001', '1Kor 2:14'), ('ANTROP-001', '1Kor 2:15'),
    ('HAMART-001', 'Ézs 24:5-6'), ('HAMART-001', 'Hós 4:1-3'), ('HAMART-001', 'Mt 15:19'),
    ('HAMART-001', 'Mk 7:21-23'), ('HAMART-001', '2Pét 3:6-7'),
]


def beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x.strip() and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def ujra_kotojel(h):
    return h.replace('–', '-')


def nyelvtani(st):
    return SZK.nyelvtani(st)


def kombinaciok(sorok):
    """Motívum -> [frozenset(nem nyelvtani Strongok)] (üres kombináció nem számít)."""
    ki = collections.defaultdict(set)
    for s in sorok:
        if not s.get('strong'):
            continue
        k = frozenset(x for x in s['strong'].split('+') if x and not nyelvtani(x))
        if k:
            ki[s['id']].add(k)
    return {m: sorted(v, key=lambda k: sorted(k)) for m, v in ki.items()}


def vizsgal(igehely, kombok, vers_st):
    """Igaz-értékek négy változatra + a versben talált kombináció-tagok.
    Visszatér: dict(szoveg=bool, teljes_vers, teljes_union, lax_vers, lax_union, ok_szoveg)."""
    versek = LG.igehely_lista(ujra_kotojel(igehely))
    halmazok = [(v, vers_st.get(v)) for v in versek]
    van_szoveg = any(h for _v, h in halmazok)
    if not van_szoveg:
        return {'szoveg': False}
    uni = set()
    for _v, h in halmazok:
        if h:
            uni |= h
    teljes_vers = any(k <= h for k in kombok for _v, h in halmazok if h)
    teljes_union = any(k <= uni for k in kombok)
    lax_vers = any(k & h for k in kombok for _v, h in halmazok if h)
    lax_union = any(k & uni for k in kombok)
    # ok-szöveg: melyik kombináció hiányzik, mi van a versben a gerincből
    gerinc_tagok = sorted(set().union(*kombok))
    a_versben = sorted(set(gerinc_tagok) & uni)
    hianyzo = ['+'.join(sorted(k)) for k in kombok if not k <= uni]
    return {'szoveg': True, 'teljes_vers': teljes_vers, 'teljes_union': teljes_union,
            'lax_vers': lax_vers, 'lax_union': lax_union,
            'ok': 'a gerinc-szókapcsolat hiányzik: %s; a versben a gerincből: %s' % (
                ', '.join(hianyzo), ', '.join(a_versben) or 'semmi')}


def ok_cimke(motivum, indoklas, szotar):
    for r in szotar:
        if r['id'] not in ('*', motivum):
            continue
        try:
            if re.search(r['minta'], indoklas, re.IGNORECASE):
                return r['cimke']
        except re.error:
            continue
    return 'egyéb'


# Bővített heurisztika (a mintaszótár mellett, csak a mérés kedvéért): az indoklás a szókapcsolat/szó hiányáról szól.
HIANY_JELLEGU = re.compile(
    r'nincs\b.{0,60}\b(pár|a versben|szókapcsolat|kapcsolat|H\d{4}|G\d{4})|nem tartalmaz|hiányzik|nem szerepel|'
    r'nincs meg|nem találhat', re.IGNORECASE)


def main():
    reszletes = '--reszletes' in sys.argv
    jel = [r for r in beolvas(os.path.join(ADAT, 'jeloltek.tsv')) if r.get('jelolt_tipus') == 'elofordulas']
    eloford = beolvas(os.path.join(ADAT, 'elofordulasok.tsv'))
    mot = {r['id']: r for r in beolvas(os.path.join(ADAT, 'motivumok.tsv'))}
    szotar = sorted(beolvas(os.path.join(ADAT, 'elutasitasi_okok.tsv')), key=lambda r: int(r['sorrend']))
    komb = kombinaciok(eloford)
    vers_st = SZK.vers_strongok()

    eredmeny = []  # (id, igehely, dontes, indoklas, dict)
    for r in jel:
        if r['dontes'] not in ('beépítve', 'elutasítva'):
            continue
        m = r['id']
        if m not in komb:
            eredmeny.append((m, r['igehely'], r['dontes'], r['indoklas'], {'szoveg': None}))
            continue
        eredmeny.append((m, r['igehely'], r['dontes'], r['indoklas'], vizsgal(r['igehely'], komb[m], vers_st)))

    def hordozo(m):
        return mot.get(m, {}).get('azonossag_tipusa', '?')

    print('# F150 M0 mérés — nyers kimenet')
    print('jeloltek elofordulas, eldöntött: %d' % len(eredmeny))
    print('motívumok kombinációi (nyelvtani Strong nélkül):')
    for m in sorted(komb):
        print('  %s [%s]: %s' % (m, hordozo(m), ' | '.join('+'.join(sorted(k)) for k in komb[m])))
    nincs_komb = sorted({e[0] for e in eredmeny if e[4].get('szoveg') is None})
    print('gerinc-kombináció nélküli motívum (nem mérhető): %s' % (nincs_komb or '-'))

    valtozatok = [('teljes_vers', 'teljes kombináció, egy versben'), ('teljes_union', 'teljes kombináció, a tartomány összes versében'),
                  ('lax_vers', 'bármely tag, egy versben'), ('lax_union', 'bármely tag, a tartomány összes versében')]

    for vk, vnev in valtozatok:
        print('\n## Változat: %s (%s)' % (vk, vnev))
        for szuro in ('NINCS hordozó-szűrés', 'hordozó-szűréssel'):
            ossz = collections.Counter()
            for m, ih, d, ind, e in eredmeny:
                if e.get('szoveg') is None:
                    ossz[(d, 'nem_merheto')] += 1
                    continue
                if not e['szoveg']:
                    ossz[(d, 'nincs_szoveg')] += 1
                    continue
                ki = not e[vk]
                if ki and szuro != 'NINCS hordozó-szűrés' and hordozo(m) not in LEXIKAI_HORDOZO:
                    ki = False
                ossz[(d, 'ki' if ki else 'be')] += 1
            el_ossz = sum(v for (d, _), v in ossz.items() if d == 'elutasítva')
            el_szoveg = el_ossz - ossz[('elutasítva', 'nincs_szoveg')] - ossz[('elutasítva', 'nem_merheto')]
            be_szoveg = sum(v for (d, k), v in ossz.items() if d == 'beépítve' and k in ('ki', 'be'))
            print('  %-22s elutasítva %d (szöveggel %d): valoszinu_ki %d (%.1f%%), vizsgalando %d, szöveg nélkül %d | '
                  'beépítve szöveggel %d: hamis kizárás %d (%.1f%%)' % (
                      szuro, el_ossz, el_szoveg, ossz[('elutasítva', 'ki')],
                      100.0 * ossz[('elutasítva', 'ki')] / el_szoveg if el_szoveg else 0,
                      ossz[('elutasítva', 'be')], ossz[('elutasítva', 'nincs_szoveg')],
                      be_szoveg, ossz[('beépítve', 'ki')],
                      100.0 * ossz[('beépítve', 'ki')] / be_szoveg if be_szoveg else 0))

    # --- Fő változat: teljes kombináció, egy versben ---
    VK = 'teljes_vers'
    print('\n## FŐ VÁLTOZAT (%s): motívumonként' % VK)
    print('motivum\thordozo\tbeepitve\tszoveg_nelkul_be\telutasitva\tszoveg_nelkul_el\t'
          'hamis_kizaras_szuro_nelkul\thamis_kizaras_szuressel\tfelismert_szuro_nelkul\tfelismert_szuressel\t'
          'felismert_arany_szuressel\tok_egyezes_mintaszotar\tok_egyezes_bovitett')
    ossz_sor = collections.Counter()
    cimke_tabla = collections.defaultdict(collections.Counter)
    hamis_sorok = []
    for m in sorted({e[0] for e in eredmeny}):
        be = [e for e in eredmeny if e[0] == m and e[2] == 'beépítve']
        el = [e for e in eredmeny if e[0] == m and e[2] == 'elutasítva']
        be_sz = [e for e in be if e[4].get('szoveg')]
        el_sz = [e for e in el if e[4].get('szoveg')]
        lex = hordozo(m) in LEXIKAI_HORDOZO
        hk_nelkul = [e for e in be_sz if not e[4][VK]]
        hk_vel = hk_nelkul if lex else []
        f_nelkul = [e for e in el_sz if not e[4][VK]]
        f_vel = f_nelkul if lex else []
        okm = okb = 0
        for e in f_vel:
            c = ok_cimke(m, e[3], szotar)
            cimke_tabla[m][c] += 1
            if c in ('a formula nincs a versben', 'név nélküli forma'):
                okm += 1
            if c in ('a formula nincs a versben', 'név nélküli forma') or HIANY_JELLEGU.search(e[3]):
                okb += 1
        for e in hk_nelkul:
            hamis_sorok.append((m, e[1], lex, e[4]['ok'], e[3]))
        ar = '%.0f%%' % (100.0 * len(f_vel) / len(el_sz)) if el_sz else '-'
        print('\t'.join(str(x) for x in [m, hordozo(m), len(be), len(be) - len(be_sz), len(el), len(el) - len(el_sz),
                                         len(hk_nelkul), len(hk_vel), len(f_nelkul), len(f_vel), ar,
                                         '%d/%d' % (okm, len(f_vel)), '%d/%d' % (okb, len(f_vel))]))
        for k, v in [('be', len(be)), ('be_sz', len(be_sz)), ('el', len(el)), ('el_sz', len(el_sz)),
                     ('hk_nelkul', len(hk_nelkul)), ('hk_vel', len(hk_vel)), ('f_nelkul', len(f_nelkul)),
                     ('f_vel', len(f_vel)), ('okm', okm), ('okb', okb)]:
            ossz_sor[k] += v
    print('ÖSSZESEN\t\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t\t%d/%d\t%d/%d' % (
        ossz_sor['be'], ossz_sor['be'] - ossz_sor['be_sz'], ossz_sor['el'], ossz_sor['el'] - ossz_sor['el_sz'],
        ossz_sor['hk_nelkul'], ossz_sor['hk_vel'], ossz_sor['f_nelkul'], ossz_sor['f_vel'],
        ossz_sor['okm'], ossz_sor['f_vel'], ossz_sor['okb'], ossz_sor['f_vel']))

    print('\n## Elutasítási ok-címkék a felismert (valoszinu_ki, lexikai hordozón) elutasításoknál')
    for m in sorted(cimke_tabla):
        print('  %s: %s' % (m, dict(cimke_tabla[m])))

    print('\n## Hamis kizárások soronként (beépítve, de a gerinc-szókapcsolat nincs a versben) — hordozó-szűrés nélkül')
    for m, ih, lex, ok, ind in hamis_sorok:
        print('  %s\t%s\thordozo=%s\t%s\t(indoklás: %s)' % (m, ih, hordozo(m), ok, ind[:140]))

    print('\n## A 12 ismert hamis kizárás (név szerint, fő változat)')
    index = {(e[0], e[1]): e for e in eredmeny}
    for m, ih in ISMERT_12:
        e = index.get((m, ih))
        if not e:
            print('  %s\t%s\tNINCS ilyen sor a jeloltek.tsv-ben' % (m, ih))
            continue
        d = e[4]
        if not d.get('szoveg'):
            print('  %s\t%s\tdöntés=%s\tszöveg nélkül' % (m, ih, e[2]))
            continue
        gep = 'valoszinu_ki' if not d[VK] else 'megvan'
        szuressel = gep if (gep == 'megvan' or hordozo(m) in LEXIKAI_HORDOZO) else 'vizsgalando'
        print('  %s\t%s\tdöntés=%s\thordozo=%s\tgép_szűrés_nélkül=%s\tgép_szűréssel=%s\t%s' % (
            m, ih, e[2], hordozo(m), gep, szuressel, d['ok']))

    if reszletes:
        print('\n## Részletes: elutasítva, valoszinu_ki (lexikai hordozón)')
        for m, ih, d, ind, e in eredmeny:
            if d == 'elutasítva' and e.get('szoveg') and not e[VK] and hordozo(m) in LEXIKAI_HORDOZO:
                print('  %s\t%s\t%s\t%s' % (m, ih, ok_cimke(m, ind, szotar), ind[:120]))


if __name__ == '__main__':
    main()
