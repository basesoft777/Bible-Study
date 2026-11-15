"""F194.2 (CLAUDE.md 6. lépés, LXX-híd; 2. szabály: nincs közvetlen út): az ISTENTISZT-001 LXX-híd mérésének
(`naplok/F194_lxx_hid_scan.py` → `naplok/F194_lxx_hid_ISTENTISZT-001.tsv`) döntés nélküli versei a `jeloltek.tsv`-be.

A mérés 40 olyan ószövetségi verset adott, amelyben a LXX-ben ἐπικαλέω + ὄνomα áll, és nincs előfordulás- vagy
jelöltsoruk; ebből 23-at az F123-as teljesség-mérés összesítő sorai már lefednek (`naplok/F123_teljesseg_ISTENTISZT-
001_blokkok.tsv`). A maradék 17 versben a héber szövegben a קָרָא (kárá, H7121) nem áll (TAHOT), a formula csak a görög
fordítás olvasata. Döntés (értelmező ítélet, a határ nem változik; a negatív kritérium szerint):
- 14 vers szenvedő (passzív) szerkezet: a hely viseli az Úr nevét — egy összesítő sor (DT564 minta), a tagok a
  blokkfájl `lxx_szenvedo_hely` blokkjában (halo=lxx);
- 2Sám 20:1, 2Krón 28:15: megnevezés — egy-egy sor;
- Zsolt 75:2: a héberben „neved közel van”, a segítségül hívás csak a görög olvasat — egy sor.
Mind `elutasítva`, `elofordulas` típusú jelölt. Ellenőrzés írás előtt: a jelölés forrása (`jeloles_oka`) és az
elutasítás oka (`elutasitas_oka`) besorolható és a várt; az olvasói kapu indoklás-szabályai (csak Strong-szám
engedett); a Károli-idézetek; a blokk tagjainak száma = 14; az új sorok előtt a fájl többi sora változatlan.
Futtatás: python naplok/F194_lxx_jeloltek.py [--ir]
"""
import os
import re
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
sys.path.insert(0, os.path.join(GYOKER, 'naplok'))
import szerep_kizart as SZK  # noqa: E402
import F194_indoklas_meres as IM  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
DATUM = '2026.11.12'
SCAN = 'naplok/F194_lxx_hid_ISTENTISZT-001.tsv'
BLOKKFAJL = os.path.join(GYOKER, 'naplok', 'F123_teljesseg_ISTENTISZT-001_blokkok.tsv')
UTANA = ('2Móz 31:2', 'Összesítő sor 12 versre')   # az új sorok e sor után kerülnek
SZENVEDO = ['5Móz 12:5', '5Móz 12:11', '5Móz 12:21', '5Móz 12:26', '5Móz 14:23', '5Móz 14:24', '5Móz 16:2',
            '5Móz 16:6', '5Móz 16:11', '5Móz 17:8', '5Móz 17:10', '5Móz 26:2', '2Krón 6:20', 'Ézs 18:7']


def scan_prov():
    for s in open(os.path.join(GYOKER, SCAN), encoding='utf-8'):
        m = s.rstrip('\n').split('\t')
        if len(m) > 5 and m[0] != 'igehely':
            return m[5]
    raise SystemExit('nincs LXX-híd mérés')


def sorok_uj(prov):
    fk = 'F194 LXX-híd teljesség-mérés, Septuaginta-híd: a LXX-ben ἐπικαλέω + ὄνομα, a héberben a kárá nélkül | %s' % prov
    fk_blokk = ('F194 LXX-híd teljesség-mérés, Septuaginta-híd, blokk-kizárás (DT564 minta): %d vers, az első itt; a '
                'lista: naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv (halo=lxx, blokk=lxx_szenvedo_hely) | %s'
                % (len(SZENVEDO), prov))
    ref = SCAN
    return [
        ('5Móz 12:5', fk_blokk, 'Összesítő sor %d versre (az első itt áll): a héber szövegben a קָרָא (kárá) ige nem '
         'áll; a hely, „a melyet kiválaszt az Úr”, az ő nevét viseli („hogy az ő nevét oda helyezze és ott lakozzék”). '
         'A görög fordítás ezt szenvedő (passzív) igével adja vissza: ἐπικληθῆναι τὸ ὄνομα αὐτοῦ (epikléthénai to '
         'onoma autú). Ez hovatartozás, nem a név segítségül hívása; a negatív kritérium kizárja.' % len(SZENVEDO),
         ref + ' (blokk=lxx_szenvedo_hely)', 'passzív szerkezet vagy megnevezés (negatív kritérium)'),
        ('2Sám 20:1', fk, 'Megnevezés jellegű használat: „kinek neve Séba vala”; a görög fordítás ezt az '
         'ἐπικαλούμενος … ὄνομα αὐτῷ Σαβεε (epikalúmenosz … onoma autó Szabee) alakkal adja vissza, a héber szövegben '
         'a קָרָא (kárá) nem áll.', ref, 'passzív szerkezet vagy megnevezés (negatív kritérium)'),
        ('2Krón 28:15', fk, 'Megnevezés jellegű használat: „a névszerint megnevezett férfiak”; a görög fordítás ezt az '
         'οἳ ἐπεκλήθησαν ἐν ὀνόματι (hoi epekléthészan en onomati) alakkal adja vissza, a héber szövegben a קָרָא '
         '(kárá) nem áll.', ref, 'passzív szerkezet vagy megnevezés (negatív kritérium)'),
        ('Zsolt 75:2', fk, 'Nincs meg a formula a versben: a héber szöveg szerint „neved közel van” (קָרוֹב שְׁמֶךָ, '
         'káróv semechá); a görög fordítás ezt ἐπικαλεσόμεθα τὸ ὄνομά σου (epikaleszometha to onoma szú, „segítségül '
         'hívjuk a nevedet”) alakban olvassa. A segítségül hívás csak a görög fordításé.', ref,
         'a formula nincs a versben'),
    ]


def karoli():
    d = {}
    for s in open(os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8'):
        m = s.rstrip('\n').split('\t')
        if len(m) > 1:
            d[m[0]] = m[1]
    return d


def main():
    ir = '--ir' in sys.argv
    prov = scan_prov()
    kar = karoli()
    minta = SZK.okok(ID)
    hibak = []
    with open(os.path.join(GYOKER, 'adat', 'jeloltek.tsv'), encoding='utf-8', newline='') as f:
        jsor = f.read().split('\n')
    fej = next(s for s in jsor if s and not s.startswith('#')).rstrip('\r').split('\t')
    cr = '\r' if jsor[0].endswith('\r') else ''
    meglevo = {(s.split('\t')[0], s.split('\t')[1]) for s in jsor if s.count('\t') > 3}
    hova = None
    for i, s in enumerate(jsor):
        m = s.split('\t')
        if len(m) > 4 and m[0] == ID and m[1] == UTANA[0] and m[4].startswith(UTANA[1]):
            hova = i
    if hova is None:
        raise SystemExit('nem találom a beszúrás helyét')
    uj = []
    for igehely, fk, ind, ref, vart in sorok_uj(prov):
        if (ID, igehely) in meglevo:
            hibak.append('már van sora: %s' % igehely)
        r = {k: '' for k in fej}
        r.update(id=ID, igehely=igehely, forras_kereses=fk, dontes='elutasítva', indoklas=ind, datum=DATUM,
                 jelolt_tipus='elofordulas', dontes_ref=ref)
        try:
            SZK.jeloles_oka(fk)
            c = SZK.elutasitas_oka(ind, minta)
            if c != vart:
                hibak.append('besorolás: %s: %s (várt: %s)' % (igehely, c, vart))
        except SZK.BeNemSorolhato as e:
            hibak.append('%s: %s' % (igehely, e))
        for nev, mi in IM.merj(ind):
            if nev != 'Strong-szám':
                hibak.append('kapu: %s: %s: %s' % (igehely, nev, mi))
        for q in re.findall(r'„([^”]*)”', ind):
            if q not in kar.get(igehely, '') and q != 'segítségül hívjuk a nevedet':
                hibak.append('idézet: %s: „%s”' % (igehely, q))
        uj.append('\t'.join(r[k] for k in fej) + cr)
    # blokkfájl
    with open(BLOKKFAJL, encoding='utf-8', newline='') as f:
        bsor = f.read().split('\n')
    lxx = {}
    for s in open(os.path.join(GYOKER, SCAN), encoding='utf-8'):
        m = s.rstrip('\n').split('\t')
        if len(m) > 5:
            lxx[m[0]] = m[4]
    if any('\tlxx_szenvedo_hely\t' in s or s.startswith('lxx_szenvedo_hely\t') for s in bsor):
        hibak.append('a blokk már a blokkfájlban van')
    b_uj = ['lxx_szenvedo_hely\t%s\tlxx\t%s [F194.2 LXX-híd; %s]' % (v, lxx.get(v, ''), prov.split(' | ')[-1])
            for v in SZENVEDO]
    if len(b_uj) != len(SZENVEDO) or any(v not in lxx for v in SZENVEDO):
        hibak.append('a blokk tagjai nincsenek mind a LXX-mérésben')
    for h in hibak:
        print('HIBA:', h)
    if hibak:
        raise SystemExit('%d hiba, nem írok' % len(hibak))
    print('jeloltek.tsv: +%d sor a %d. sor után; blokkfájl: +%d sor' % (len(uj), hova + 1, len(b_uj)))
    if not ir:
        print('próba: rendben (írás: --ir)')
        return
    jsor[hova + 1:hova + 1] = uj
    with open(os.path.join(GYOKER, 'adat', 'jeloltek.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(jsor))
    while bsor and bsor[-1] == '':
        bsor.pop()
    with open(BLOKKFAJL, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(bsor + b_uj) + '\n')
    print('írva.')


if __name__ == '__main__':
    main()
