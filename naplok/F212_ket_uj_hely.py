"""F212: a felhasználó tartalmi döntései a gyászoló föld helyeiről (2026-11-12), egy körben.

- BE (a felhasználó: „a Jer 23:10 kerüljön be”; „Igen, így” — Jer 12:4 be, Jóel 1:10 és a többi ki): Jer 23:10 és
  Jer 12:4 a HAMART-001 tematikus előfordulása (a Hós 4:1-3 mintájára: a lánc szavai nélkül, a föld gyászol a lakók
  bűne, illetve az átok miatt). `adat/elofordulasok.tsv` sor (a 2.1 kerek mondata és a funkció is itt), és a
  `adat/jeloltek.tsv` beépített sora.
- KI, egyenként, indoklással: Jóel 1:10, Jer 12:11, Jer 14:2, Ámós 1:2, Hós 10:5, Sir 2:8.
- A kivett versek elhagyják a csoportos blokkjukat (`naplok/F123_teljesseg_HAMART-001_blokkok.tsv`: a vers nem lehet
  egyszerre előfordulás vagy egyedi döntés és csoport-tag, ellenoriz.py 36.), és a blokk összesítő sorának versszáma
  (forras_kereses, indoklás) ennyivel csökken.
Írás előtt összevetés: a többi sor bájtra változatlan, a blokkok versszáma = az összesítő sorok versszáma.
Futtatás: python naplok/F212_ket_uj_hely.py [--ir]
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELOF = os.path.join(GY, 'adat', 'elofordulasok.tsv')
JEL = os.path.join(GY, 'adat', 'jeloltek.tsv')
BLOKK = os.path.join(GY, 'naplok', 'F123_teljesseg_HAMART-001_blokkok.tsv')
MID = 'HAMART-001'
DATUM = '2026.11.12'
DONTES_BE = 'a felhasználó döntése (2026-11-12): „a Jer 23:10 kerüljön be”; „Igen, így” (Jer 12:4 be, Jóel 1:10 és a többi ki)'
PROV = 'scope=manual | forras=%s; az orkesztrátor továbbította; F212 | ts=2026-11-12' % DONTES_BE

UJ_ELOF = [
    {'igehely': 'Jer 12:4', 'strong': 'H0056', 'karoli_szo': 'gyászoljon',
     'kapcsolodas': ('Jeremiás panaszában a föld gyászol, és a lakók miatt pusztul az állat: „Meddig gyászoljon a föld, '
                     'és meddig száradjon el minden fű a mezőn? A benne lakók gonoszsága miatt pusztul el barom és '
                     'madár”. A lakók bűne a földre és a teremtményekre száll, ahogy a Hós 4:3-ban és az 1Móz 6:7-ben; '
                     'a lánc szavai nem állnak benne, a hely ezért tematikus, nem lexikai kapcsolatként tartozik ide.'),
     'funkcio': '🔍 tematikus, nem lexikai — a lakók gonoszsága miatt gyászol a föld és pusztul az állat'},
    {'igehely': 'Jer 23:10', 'strong': 'H0423', 'karoli_szo': 'esküvés',
     'kapcsolodas': ('Jeremiás a próféták és a nép bűnéről mondja: „a hamis esküvés miatt gyászol a föld, a pusztának '
                     'legelője kiszáradt”. A héberben itt az átok szava áll (álá), ugyanaz, amely az Ézs 24:6-ban '
                     'megemészti a földet; a Károli esküvésnek fordítja. A bűn következménye a földre száll, de a lánc '
                     'saját szavai nélkül; a hely ezért tematikus, nem lexikai kapcsolatként tartozik ide.'),
     'funkcio': '🔍 tematikus, nem lexikai — az átok miatt gyászol a föld'},
]
KI = {  # igehely: (blokk-kulcs (halo, blokk), indoklás)
    'Jóel 1:10': (('strong', 'H0127'), 'Határeset: a föld (adámá) gyászol, de a vers nem nevez meg bűnt okként; a gyász '
                  'oka a sáska és az aszály (Jóel 1:4-12), nem az elkövető tette, ezért a terjedés szerkezete hiányzik.'),
    'Jer 12:11': (('f212', 'H0056'), 'Általános pusztulás: „Elpusztíttatik az egész föld”; a föld szava itt az erec, a lánc '
                  'szava nem áll a versben, és a vers nem a Genezis láncát hozza vissza.'),
    'Jer 14:2': (('f212', 'H0056'), 'Aszály miatti gyász: Júda és kapui gyászolnak a szárazság miatt (Jer 14:1-6); a vers '
                 'nem nevez meg bűnt okként, a lánc szava nem áll benne.'),
    'Ámós 1:2': (('f212', 'H0056'), 'A pásztorok legelői hervadnak az Úr szavára; a lánc szava nem áll a versben, és a '
                 'következmény nem az elkövető tettéből terjed tovább.'),
    'Hós 10:5': (('f212', 'H0056'), 'Bálvány miatti gyász: Samaria lakói Bét-Aven borjúját siratják; nem a föld gyászol, '
                 'és a lánc szava nem áll a versben.'),
    'Sir 2:8': (('strong', 'H7843'), 'Fizikai pusztítás: az Úr Sion kőfalát rontja le; a romlás igéje háborús pusztításra '
                'áll, nem erkölcsi megromlásra.'),
}
BE_KI_BLOKK = {'Jer 12:4': ('nf63e', 'H7451'), 'Jer 23:10': ('nf63e', 'H7451')}


def olvas(ut):
    with io.open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def ir(ut, sorok):
    with io.open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok))


def main():
    iras = '--ir' in sys.argv
    # 1. előfordulások: a HAMART-001 utolsó sora után
    elof = olvas(ELOF)
    fej = next(s for s in elof if s and not s.startswith('#')).split('\t')
    hamart = [i for i, s in enumerate(elof) if s.startswith(MID + '\t')]
    if any(s.split('\t')[1] in ('Jer 12:4', 'Jer 23:10') for s in (elof[i] for i in hamart)):
        print('az előfordulás-sorok már bent vannak; nincs írás')
        return
    uj_e = []
    for u in UJ_ELOF:
        d = dict.fromkeys(fej, '')
        d.update({'id': MID, 'igehely': u['igehely'], 'kapcsolodas': u['kapcsolodas'], 'pardes_szint': 'Drash',
                  'funkcio': u['funkcio'], 'gerinc_elem': 'tematikus:1Móz 3:17', 'strong': u['strong'],
                  'lexikon_szotar': 'BDB', 'lexikon_entry_id': u['strong'], 'jelentes_szam': 'Qal',
                  'karoli_szo': u['karoli_szo'], 'azonositas_modja': 'tartalom-alapú', 'megbizhatosag': 'közepes',
                  'proveniencia': PROV, 'igazolas': 'nincs', 'felmerult_tanulmany': 'teljesség-mérés'})
        uj_e.append('\t'.join(d[k] for k in fej))
    elof_uj = elof[:hamart[-1] + 1] + uj_e + elof[hamart[-1] + 1:]
    # 2. jelöltek: két beépített, hat egyenként elutasított sor; az összesítő sorok versszáma
    jel = olvas(JEL)
    jfej = next(s for s in jel if s and not s.startswith('#')).split('\t')
    uj_j = []
    for u in UJ_ELOF:
        d = dict.fromkeys(jfej, '')
        d.update({'id': MID, 'igehely': u['igehely'], 'dontes': 'beépítve', 'datum': DATUM, 'jelolt_tipus': 'elofordulas',
                  'forras_kereses': 'F212 teljesség-mérés (a gyászoló föld helyei) | ' + PROV,
                  'indoklas': u['funkcio'].split(' — ', 1)[1].capitalize() + '; a lánc szavai nélkül, tematikus hely (a Hós 4:1-3 mintájára).',
                  'dontes_ref': 'F212 · ' + DONTES_BE})
        uj_j.append('\t'.join(d[k] for k in jfej))
    for v, (_b, ind) in KI.items():
        d = dict.fromkeys(jfej, '')
        d.update({'id': MID, 'igehely': v, 'dontes': 'elutasítva', 'datum': DATUM, 'jelolt_tipus': 'elofordulas',
                  'forras_kereses': 'F212 teljesség-mérés (a gyászoló föld helyei), egyenként | ' + PROV,
                  'indoklas': ind, 'dontes_ref': 'F212 · ' + DONTES_BE})
        uj_j.append('\t'.join(d[k] for k in jfej))
    kivesz = dict(BE_KI_BLOKK, **{v: b for v, (b, _i) in KI.items()})
    csokken = {}
    for v, b in kivesz.items():
        csokken[b] = csokken.get(b, 0) + 1
    jel_uj = []
    for s in jel:
        c = s.split('\t')
        if s and not s.startswith('#') and c[0] == MID and len(c) > 4:
            m = re.search(r'\(halo=(\w+), blokk=(\w+)\)', c[2])
            if m and (m.group(1), m.group(2)) in csokken:
                n_regi = int(re.search(r'blokk-sor[^:]*:\s*(\d+) vers', c[2]).group(1))
                n_uj = n_regi - csokken[(m.group(1), m.group(2))]
                c[2] = re.sub(r'(blokk-sor[^:]*:\s*)%d vers' % n_regi, r'\g<1>%d vers' % n_uj, c[2], 1)
                c[4] = c[4].replace('Összesítő sor %d versre' % n_regi, 'Összesítő sor %d versre' % n_uj, 1)
                print('összesítő: %s %s %d → %d' % (m.group(1), m.group(2), n_regi, n_uj))
                s = '\t'.join(c)
        jel_uj.append(s)
    veg = jel_uj[-1] == ''
    jel_uj = (jel_uj[:-1] if veg else jel_uj) + uj_j + ([''] if veg else [])
    # 3. blokkok
    blokk = olvas(BLOKK)
    blokk_uj, kivett = [], []
    for s in blokk:
        c = s.split('\t')
        if len(c) >= 3 and c[2] in kivesz and (c[0], c[1]) == kivesz[c[2]]:
            kivett.append(c[2])
            continue
        blokk_uj.append(s)
    if sorted(kivett) != sorted(kivesz):
        raise SystemExit('MEGÁLLÁS: a blokkokból kivett versek: %s, várt: %s' % (sorted(kivett), sorted(kivesz)))
    for (h, b), _n in csokken.items():
        db = sum(1 for s in blokk_uj if s.startswith('%s\t%s\t' % (h, b)))
        sor = next(s for s in jel_uj if '(halo=%s, blokk=%s)' % (h, b) in s)
        n = int(re.search(r'blokk-sor[^:]*:\s*(\d+) vers', sor.split('\t')[2]).group(1))
        if db != n:
            raise SystemExit('MEGÁLLÁS: %s %s blokk %d vers, az összesítő %d' % (h, b, db, n))
    print('előfordulás +2; jelölt +8 (2 beépítve, 6 elutasítva); blokkokból kivéve %d vers' % len(kivett))
    if not iras:
        print('(próba: --ir nélkül nincs írás)')
        return
    ir(ELOF, elof_uj)
    ir(JEL, jel_uj)
    ir(BLOKK, blokk_uj)
    print('írva')


if __name__ == '__main__':
    main()
