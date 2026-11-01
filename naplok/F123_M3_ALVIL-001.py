"""F123 X.M3 (ALVIL-001): az új kézi forrás (`motivumok/ALVIL-001.md`) összeállítása a jóváhagyott leképezési tábla
(`naplok/F123_szetvalasztas_ALVIL-001.tsv`, DT-F123g (a)) `forras` egységeiből, bájtra, a sablon 9 (v0.3) szakaszrendjében.

A régi tanulmány a `--regi` útvonalon (alapérték: az archív példány, ha már ott van, különben a `tematikus_lezart/` alatt);
a sorokat a tábla sorszámai szerint veszi. Új szöveg csak a tábla szerint: a szerkezeti jelölők (FORRÁSRÉTEG, ADAT-NÉZET,
INAKTÍV, RÉS), a fejléc-proveniencia 【NAPLO】-ja, a 3.U és a ↳ alpont alcíme, az alpont értelmező prózája (DT-F123d (2),
2e. 5.; az értelmező menet írja), a 7.N tétel címkéje és a Proveniencia-sorok (a ténylegesen lefutott lekérdezések sorai,
`adat/auditok.tsv`, F123.ALVIL.M2). A vágott egységek (Á8 dátumrész, 37.2/37.4, 20.2) a táblában megnevezett részszövegek.

Ellenőrzés (a végén): minden `forras` egység (a vágottaknál a részszöveg) pontosan egyszer áll az új fájlban; a tábla
`archivum`/`generalt` egységeinek egyetlen, 40 karakternél hosszabb sora sem áll benne.

    python naplok/F123_M3_ALVIL-001.py [--regi <út>] [--proba]
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEL = os.path.join(GY, 'motivumok', 'ALVIL-001.md')
TABLA = os.path.join(GY, 'naplok', 'F123_szetvalasztas_ALVIL-001.tsv')
ALAP = 'tematikus_lezart/Hadesz_Seol_tematikus.md'
ARCH = 'archivum/ALVIL-001/Hadesz_Seol_tematikus.md'

ALPONT = (
    '**A motívum határa a halál szorításában kiáltónál.** A Seól nemcsak a halottak helye, hanem a még élőt is szorongató '
    'hatalom: „a Seól kötelei körülvettek” (2Sám 22:6 = Zsolt 18:6), „a Seól szorongatásai megragadtak” (Zsolt 116:3), „a '
    'Seól gyomrából kiáltottam” (Jón 2:3). Ezeken a helyeken a hívó a Seól fenyegetéséből az Úrhoz kiált, és meghallgatást '
    'nyer.\n\n'
    '- **Minimális jegy:** a Seól a hívót szorongatja, és ő az Úrhoz kiált (meghallgatás). Mindkét elem nélkül a hely nem '
    'tartozik ide.\n'
    '- **Kizárva:** a Seól mint az ellenségek sorsa (Zsolt 55:16; Zsolt 31:18) — ott nem a hívót szorongatja, hanem a hívó '
    'kéri, hogy az ellenség jusson oda.\n'
    '- **A hígulás iránya:** az „ima bajban”. A halálveszélyből Istenhez kiáltó, de a Seólt nem nevező hely (például Zsolt '
    '107:18–19: „a halál kapujához közelgetének … az Úrhoz kiáltának”) ezen a fölérendelt fogalmon keresztül tartozna ide, '
    'ezért az alpontból kimarad.\n'
    '- **Viszony a név segítségül hívásához (ISTENTISZT-001):** a két motívum egyetlen közös helye a Zsolt 116:3–4 (a Seól '
    'szorongatása, majd „az Úr nevét hívtam segítségül”); a név nélküli kiáltás nem ISTENTISZT-001-előfordulás.'
)


def tabla():
    L = [l.rstrip('\n').rstrip('\r').split('\t') for l in open(TABLA, encoding='utf-8') if not l.startswith('#')]
    return [dict(zip(L[0], r)) for r in L[1:]]


def main():
    proba = '--proba' in sys.argv
    regi = sys.argv[sys.argv.index('--regi') + 1] if '--regi' in sys.argv else (ARCH if os.path.exists(os.path.join(GY, ARCH)) else ALAP)
    T = open(os.path.join(GY, regi), encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
    if T[0].startswith('<!-- ARCHÍV:'):
        T = T[1:]  # az archív fejléc nélkül: a sorszámok a régi fájléi

    def s(n):
        return T[n - 1]

    def resz(n, kezd, veg=None):
        x = s(n)
        a = x.index(kezd)
        b = x.index(veg, a) + len(veg) if veg else len(x)
        return x[a:b]

    l145 = s(145).replace(' *(felvéve 2026.08.25)*', '', 1)
    assert l145 != s(145)
    hos_lelet = resz(131, '"Megváltom őket', 'adja vissza.')
    tr_mondat = resz(131, 'A TR/Byzantinus hagyomány', 'származik')
    mt16 = resz(46, 'külön motívumként kezelendő', 'sorra kerül.')

    D = []
    a = D.append
    a('# Hádész (Seól) — a halottak birodalma')
    a('')
    a('<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->')
    a('')
    a('【NAPLO: F123 M3, 2026-10-29 — a forrás a régi tematikus tanulmány (`archivum/ALVIL-001/Hadesz_Seol_tematikus.md`), '
      'a kereszthivatkozás-napló és a régi forrásréteg szétválasztásával készült, a `naplok/F123_szetvalasztas_ALVIL-001.tsv` '
      'jóváhagyott leképezési táblája szerint (DT-F123g (a)); sablon: 9_ v0.3 (tervezet, az első 2. lépcsős motívum mint '
      'sablon-próba, DT-F123a).】')
    a('')
    a('## Kivonat')
    a('')
    a(s(5)); a(''); a(s(7)); a(''); a(s(9))
    a('')
    a('<!-- ADAT-NÉZET: 0. Forrás-összegyűjtés a meglévő anyagból (örökölt motívum) | forrás: adat/jeloltek.tsv (forras_kereses), '
      'adat/auditok.tsv | cél: general.py --cel lexikon#ALVIL-001#kizart | SZINT: belso -->')
    a('')
    a('## 1. Előfordulások összegyűjtése')
    a('')
    a('<!-- ADAT-NÉZET: 1. pont, 7 oszlopos előfordulás-tábla | forrás: adat/elofordulasok.tsv | cél: general.py --cel study | SZINT: apparatus -->')
    a('')
    a(s(63))
    a('')
    a(s(133))
    a('')
    a('<!-- INAKTÍV: Logikai kötőszó szerinti bontás — nincs adat: az egyetlen igehely-tartományú sor (Jel 20:13-14) '
      'bontását a régi tanulmány nem tárgyalta; a hiány nincs kitöltve -->')
    a('')
    a('### Friss, teljes körű keresés (P1–P7)')
    a('')
    a('【NAPLO: F123 M2, 2026-10-29 — a P-lépések nyoma az `adat/auditok.tsv` ALVIL-001-sorai (9 B4-lekérdezés, '
      '`naplok/F123_audit_ALVIL-001.py`); a régi tanulmány 2026.09.10-i scanjének leírása az archív példány Q2-jében.】')
    a('')
    a('## 2. Eredeti nyelvi összevetés')
    a('')
    a('<!-- ADAT-NÉZET: 2.S Szótári háttér — szerepmátrix | forrás: adat/lexikon_hivatkozasok.tsv, adat/szotar_szerepek.tsv | '
      'cél: general.py --cel lexikon#ALVIL-001#szocikkek | SZINT: apparatus -->')
    a('')
    a('<!-- ADAT-NÉZET: 2/b Kiegészítő szótári adatok | forrás: adat/lexikon_hivatkozasok.tsv | cél: general.py --cel lexikon '
      '(2b rés, res_forras forras=adat) | SZINT: apparatus -->')
    a('')
    a(s(52)); a(s(53)); a(s(54))
    a('')
    a('## 3. A PaRDeS keretrendszer — a motívum egészére alkalmazva')
    a('')
    a(s(140))
    a(s(141)); a(''); a(s(143)); a(''); a(l145); a(''); a(s(147)); a(''); a(s(149))
    a('')
    a('### Új felismerés — Hós 13:14 → 1Kor 15:55')
    a('')
    a(hos_lelet)
    a('')
    a('### ↳ Alpont: kiáltás a Seól szorításából')
    a('')
    a('【NAPLO: DT-F123d (2), felhasználó, 2026-10-19 (határdöntés, A4): a „kiáltás a Seól szorításából” az ALVIL-001 ↳ '
      'alpontja, nem új ID; a Seól nélküli scan küszöbe a DT-F123e szerint nem teljesült (1 minősített hely < 3, '
      '`naplok/F123_adat_ALVIL-001.md` 5c).】')
    a('')
    a(ALPONT)
    a(s(150))
    a('')
    a('<!-- INAKTÍV: 4. Kapcsolódás a kutatási sablonhoz — nincs adat: dedikált, kifejezetten erre a lexikai komplexumra '
      '(seól/hádész) vonatkozó pünkösdi/karizmatikus szakirodalmi feldolgozás nem áll rendelkezésre elegendő mennyiségben '
      'ahhoz, hogy nevesített szerzőkkel idézhető legyen -->')
    a('')
    a('## 5. Alkalmazás és tanítványság')
    a('')
    a('<!-- INAKTÍV: 5.T Nevesített tanítói egyezés — a 7. lépés (B9) az ALVIL-001-re nem futott; a jóváhagyott listáról '
      'dedikáltan erre a témára szánt, ellenőrizhető forrás nem állt rendelkezésre; a hiány nincs kitöltve -->')
    a('')
    a('<!-- RÉS-KEZDET: alkalmazas -->')
    a('')
    a(s(162))
    a('')
    a('<!-- RÉS-VÉGE: alkalmazas -->')
    a('')
    a('## 6. Napló-frissítés')
    a('')
    a('<!-- ADAT-NÉZET: 6. Napló-frissítés (státusz) | forrás: adat/motivumok.tsv (statusz, statusz_verzio, statusz_datum) | '
      'cél: general.py --cel naplo | SZINT: belso -->')
    a('')
    a('## 7. Módszertan és nyitott kérdések')
    a('')
    a('<!-- ADAT-NÉZET: 7.K Kereszthivatkozások + Minősítés | forrás: adat/jeloltek.tsv (dontes, indoklas, forras_kereses), '
      'TSK/Károli-KH ∩ előfordulások | cél: general.py --cel lexikon (minosites rés, res_forras forras=adat) | SZINT: apparatus -->')
    a('')
    a('<!-- ADAT-NÉZET: 7.A Kapcsolatok + Alátámasztás | forrás: adat/kapcsolatok.tsv (indoklas) | cél: general.py --cel lexikon '
      '(alatamasztas rés, res_forras forras=adat) | SZINT: apparatus -->')
    a('')
    a('<!-- RÉS-KEZDET: modszertan -->')
    a('')
    a('<!-- ADAT-NÉZET: 7.M Módszertan — ellenőrzési rétegek | forrás: adat/auditok.tsv | cél: general.py --cel lexikon | SZINT: belso -->')
    a('')
    a('**Szövegkritikai megjegyzés a Hós 13:14 → 1Kor 15:55 lelethez:** ' + tr_mondat + '; az 1Kor 15:55 ezért nem '
      'G0086-előfordulás (a kritikai szöveg mindkét tagmondatban θάνατος-t hoz).')
    a('')
    a('### Nyitott kérdések és séma-korlátok')
    a('')
    a('1. **Mt 16:18** (ᾍδης, „a pokol kapui”, ekkleziológiai kontextus): ' + mt16)
    a('')
    a('<!-- RÉS-VÉGE: modszertan -->')
    a('')
    a('<!-- ADAT-NÉZET: 7.Q Minőségi kapu, verzió-címke | forrás: adat/motivumok.tsv (sablon_verzio), adat/auditok.tsv | cél: '
      'general.py --cel lexikon | SZINT: belso -->')
    a('')
    a('## Proveniencia-sorok')
    a('')
    a('【NAPLO: a Kivonat és az 1. szakasz számai (64 ÓSZ-vers, 66 szóelőfordulás, tíz ᾍδης-előfordulás) a ténylegesen '
      'lefutott lekérdezésekből, `adat/auditok.tsv` (F123.ALVIL.M2): scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | '
      'strong=H7585 | n=64 | ts=2026-10-29T10:48Z | csatorna=cli · scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | '
      'strong=H7585 | n=66 (igealak) | ts=2026-10-29T10:48Z | csatorna=cli · scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | '
      'strong=G0086 | n=10 | ts=2026-10-29T10:48Z | csatorna=cli】')
    a('')
    szoveg = '\n'.join(D)

    # ellenőrzés
    hiba = []
    for r in tabla():
        if r['kategoria'] != 'forras' or r['fajl'] != ALAP:
            continue
        for n in range(int(r['sor_tol']), int(r['sor_ig']) + 1):
            x = s(n)
            if n == 145:
                x = l145
            elif n == 131:
                x = hos_lelet if r['resz'] == '2' else tr_mondat
            elif n == 46:
                x = mt16
            elif n == 156:
                continue  # az INAKTÍV indoka (részszöveg-átvétel, nem bájtra: a jelölőben)
            elif n == 164:
                continue
            if szoveg.count(x) != 1:
                hiba.append('forras egység nem pontosan egyszer: %d (%d×) %s' % (n, szoveg.count(x), x[:60]))
    for r in tabla():
        if r['kategoria'] in ('archivum', 'generalt') and r['fajl'] == ALAP and r['resz'] == '':
            for n in range(int(r['sor_tol']), int(r['sor_ig']) + 1):
                x = s(n).strip()
                if len(x) > 40 and x in szoveg and not x.startswith('<!--') and x != '---':
                    hiba.append('nem-forras egység a forrásban: %d %s' % (n, x[:60]))
    if hiba:
        print('\n'.join(hiba))
        sys.exit(1)
    if not proba:
        with open(CEL, 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)
    print('%s: %d sor, %d bájt; forrás: %s; ellenőrzés rendben' % ('próba' if proba else 'írva', szoveg.count('\n'),
                                                                  len(szoveg.encode('utf-8')), regi))


if __name__ == '__main__':
    main()
