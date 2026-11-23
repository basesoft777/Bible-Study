"""F239 U3 — két adatjavítás a TEREMT-001 előfordulás-soraiban (adat/elofordulasok.tsv), a próza előtt.

1. Hab 3:10 `karoli_szo`: „a víz-ár” → „a hullám”. A versben a „víz-ár” a zerem majim fordítása; a tehómot a Károli
   „a hullám”-mal adja: „gátat tör a víz-ár, harsog a hullám” (natan tehóm qóló; konkordancia/Karoli_1908.tsv,
   TAHOT_kivonat.tsv). Lelet: az U3 versenkénti kivonata, érvnapló D2.6.
2. Zsolt 106:9 kutatói jelentés-hozzárendelés: `lexikon_szotar`=BDB, `lexikon_entry_id`=H8415, `jelentes_szam`=2. A BDB
   a verset a 2. jelentésben idézi („in plural = abysses of sea, Exod 15:5, 8 (of Red Sea, so) Isa 63:13 || Psa
   106:9”); a példatábla a formai bevezetőből („only here with article”) egy második útvonalat is ad, és az új
   generátor a kettő közül kézi hozzárendelést kér (B19). A hozzárendelés a szótár saját szövegét követi.

Az `elofordulasok.tsv` sor-változása a határ ujjlenyomatát (39. szabály) is változtatja: a határdöntés-jelet a próza
menete a végén frissíti, kimondva, hogy a változás nem határ-változás (csak karoli_szo, jelentés-hozzárendelés,
kapcsolodas, funkcio, proveniencia).
Írás előtt csak a megnevezett mezők változhatnak (összevetés); a `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F239_U3_elofordulas_javit.py [--ir]"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/elofordulasok.tsv'
MOT = 'TEREMT-001'
JAVIT = {
    'Hab 3:10': {'karoli_szo': ('a víz-ár', 'a hullám')},
    'Zsolt 106:9': {'lexikon_szotar': ('', 'BDB'), 'lexikon_entry_id': ('', 'H8415'), 'jelentes_szam': ('', '2')},
}


def main(ir):
    nyers = open(UT, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(nl)
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    ix = {k: i for i, k in enumerate(sorok[fej_i].split('\t'))}
    kesz = set()
    for i in range(fej_i + 1, len(sorok)):
        m = sorok[i].split('\t')
        if len(m) < 2 or m[0] != MOT or m[1] not in JAVIT:
            continue
        for mezo, (regi, uj) in JAVIT[m[1]].items():
            if m[ix[mezo]] == uj:
                continue
            if m[ix[mezo]] != regi:
                sys.exit('HIBA: %s %s: várt %r, talált %r' % (m[1], mezo, regi, m[ix[mezo]]))
            m[ix[mezo]] = uj
            print('  %s · %s: %r → %r' % (m[1], mezo, regi, uj))
        sorok[i] = '\t'.join(m)
        kesz.add(m[1])
    if kesz != set(JAVIT):
        sys.exit('HIBA: nem található sor: %s' % (set(JAVIT) - kesz))
    if ir:
        open(UT, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
    print('ÍRVA' if ir else '(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
