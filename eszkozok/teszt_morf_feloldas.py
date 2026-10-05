"""F58 M2: az eszkozok/morf_feloldas.py tesztje (python eszkozok/teszt_morf_feloldas.py).

Az elvárt szövegek a jelkulcs-táblából (adat/morf_kulcs_heber.tsv) következnek;
a teszt a feloldó viselkedését ellenőrzi (állapot, jelzés, hiány-jelölés).
"""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import morf_feloldas as mf  # noqa: E402

HIBA = []


def ellenoriz(nev, feltetel, reszlet=''):
    if not feltetel:
        HIBA.append(nev + (' :: ' + str(reszlet) if reszlet else ''))


def main():
    # 1. ismert kódok (héber)
    VART = {
        'Vqp3ms': 'ige; törzs: qal; típus: perfectum (qatal); személy: harmadik; nem: hímnem; szám: egyes szám',
        'Vqw3ms': 'ige; törzs: qal; típus: szekvenciális imperfectum (wayyiqtol); személy: harmadik; nem: hímnem; szám: egyes szám',
        'Ncfsa': 'főnév; típus: köznév; nem: nőnem; szám: egyes szám; állapot: abszolút',
        'Ncmsc': 'főnév; típus: köznév; nem: hímnem; szám: egyes szám; állapot: constructus',
        'Sp3ms': 'toldalék; típus: névmási; személy: harmadik; nem: hímnem; szám: egyes szám',
        'Td': 'partikula; típus: határozott névelő',
        'R': 'elöljáró',
        'C': 'kötőszó',
        'Np': 'főnév; típus: tulajdonnév',
        'Rd': 'elöljáró; típus: határozott névelő',
        'Vqc': 'ige; törzs: qal; típus: infinitivus constructus',
        'Vqrmsa': 'ige; törzs: qal; típus: participium, cselekvő; nem: hímnem; szám: egyes szám; állapot: abszolút',
        'Vhp3ms': 'ige; törzs: hifil; típus: perfectum (qatal); személy: harmadik; nem: hímnem; szám: egyes szám',
    }
    for kod, vart in VART.items():
        f = mf.felold(kod, 'H')
        ellenoriz('héber ' + kod, f['szoveg'] == vart and f['allapot'] == 'teljes', f['szoveg'])

    # 2. a nyelv számít: ugyanaz a törzsjel arámiban más
    ellenoriz('arámi Vqp3ms = peal', 'törzs: peal' in mf.felold('Vqp3ms', 'A')['szoveg'])
    f = mf.felold('Vqp3ms', None)
    ellenoriz('nyelv nélkül kétértelmű', f['ketertelmu'] and '[nyelv ismeretlen]' in f['szoveg'], f['szoveg'])

    # 3. arámi törzsjel: arámiként teljes, héberként részleges, nyelv nélkül jelzett
    ellenoriz('Vec arámi teljes', mf.felold('Vec', 'A')['allapot'] == 'teljes')
    fh = mf.felold('Vec', 'H')
    ellenoriz('Vec héber részleges, a hiány jelölt', fh['allapot'] == 'reszleges' and '[?e]' in fh['szoveg'], fh['szoveg'])
    ellenoriz('Vec nyelv nélkül jelzett', '[csak arámi olvasat]' in mf.felold('Vec', None)['szoveg'])

    # 4. x-helykitöltő: külön állapot, nem „teljes”
    f = mf.felold('Nxxxa', 'A')
    ellenoriz('Nxxxa helykitöltős', f['allapot'] == 'helykitoltovel' and f['helykitoltos'], f['allapot'])

    # 5. ismeretlen jel: a nyers jel marad, hiányként jelölve, nincs csendes kitöltés
    f = mf.felold('Zzz', 'H')
    ellenoriz('ismeretlen szófaj', f['allapot'] == 'ismeretlen' and '[?Zzz]' in f['szoveg'] and f['hianyzo'], f)
    f = mf.felold('Vqp3mQ', 'H')
    ellenoriz('ismeretlen utolsó jel', f['allapot'] == 'reszleges' and '[?Q]' in f['szoveg'], f['szoveg'])
    f = mf.felold('', 'H')
    ellenoriz('üres kód', f['allapot'] == 'ismeretlen' and f['hianyzo'])
    f = mf.felold('Vap3ms', 'H')
    ellenoriz('kötelező pozíció hibája után nincs találgatás',
              f['allapot'] == 'reszleges' and 'infinitivus' not in f['szoveg'], f['szoveg'])

    # 6. adat-szintű: a Macula-tábla minden (kód, nyelv) párja a tényleges nyelvvel feloldódik
    par, allapot, reszleges, ketertelmu = mf.lefedettseg(None, kiir=False)
    ellenoriz('nincs részlegesen feloldott pár a szó nyelvével',
              allapot['reszleges'][0] == 0 and allapot['ismeretlen'][0] == 0, allapot)

    if HIBA:
        print('HIBA:')
        for h in HIBA:
            print(' -', h)
        sys.exit(1)
    print('Minden teszt zöld.')


if __name__ == '__main__':
    main()
