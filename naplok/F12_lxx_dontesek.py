"""F12.4 (DT-F12c (1)): a TEREMT-002 három előfordulás-versének LXX-döntései és friss lxx-hid audit-sorai.

Két tábla, csak hozzáfűzés, írás előtti és utáni sorösszevetéssel:
  - adat/lxx_dontesek.tsv: 6 sor (LD091–LD096), versenként a H8414 (első, ezt mutatja a lap) és a H0922;
    a `bizonyossag` a SEMA 2.11 / DT23 szerint: `biztos`, ha a Macula szó-szintű illesztése és az LXX_OS
    ugyanazt a lemmát adja; `valoszinu`, ha csak az LXX_OS ad szót (a Macula nem illeszt: hiányzó forrás);
  - adat/auditok.tsv: 3 sor (TEREMT-002, B4) a 2026-11-02-i friss `lekerdez.py lxx-hid` futás proveniencia-sorával.
A régi 60 B4-sor (kivezetett LXX_kivonat_*.tsv) nem változik.

A szóadatok forrása (2026-11-02, lekérdezve):
  - konkordancia/LXX_OS/{genesis,jeremiah-lxx,isaiah}.tsv (pozicio, lemma, strong);
  - konkordancia/Macula_heber_{Genezis,Jeremias,Ezsaias}.tsv (a héber token görög illesztése).

    python naplok/F12_lxx_dontesek.py        # száraz futás
    python naplok/F12_lxx_dontesek.py --ir
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LXX = os.path.join(GYOKER, 'adat', 'lxx_dontesek.tsv')
AUD = os.path.join(GYOKER, 'adat', 'auditok.tsv')
TS = '2026-11-02'
FEJ = ['id', 'igehely', 'lxx_igehely', 'heber_strong', 'gorog_lemma', 'gorog_strong', 'lxx_pozicio', 'tipus',
       'megjegyzes', 'bizonyossag', 'proveniencia']
FORRAS_KETTO = ('forras=Macula_heber (macula-hebrew@47db250b, szó-szintű illesztés) + LXX_OS (lxx-morph@c91f6b1e, '
                'KK-kötés) + lekerdez.py lxx-hid (ts=2026-11-02T11:33Z)')
FORRAS_LXX = 'forras=LXX_OS (lxx-morph@c91f6b1e, KK-kötés) + lekerdez.py lxx-hid (ts=2026-11-02T11:33Z)'
PROV = 'scope=F12 LXX-döntés, TEREMT-002 %s | %s | dontes=DT-F12c(1) | ts=' + TS

SOROK = [
    ['LD091', '1Móz 1:2', 'Genesis 1:2', 'H8414', 'ἀόρατος', 'G0517', '5', 'eltero_forditas',
     'A תֹהוּ-t a fordító ἀόρατος-szal („láthatatlan”) adja, a pár: ἀόρατος καὶ ἀκατασκεύαστος. Macula és LXX_OS egyezik.',
     'biztos', PROV % ('1Móz 1:2 H8414', FORRAS_KETTO)],
    ['LD092', '1Móz 1:2', 'Genesis 1:2', 'H0922', 'ἀκατασκεύαστος', '', '7', 'eltero_forditas',
     'A בֹהוּ-t a fordító ἀκατασκεύαστος-szal („berendezetlen”) adja. Macula és LXX_OS egyezik. A szónak az LXX_OS-ben '
     'nincs Strong-száma (strong_ok = nincs_uszbeli_megfelelo): a görög Strong hiánya explicit, nem pótolt.',
     'biztos', PROV % ('1Móz 1:2 H0922', FORRAS_KETTO)],
    ['LD093', 'Jer 4:23', 'Jeremiah (LXX) 4:23', 'H8414', 'οὐθέν', 'G3762', '7', 'eltero_forditas',
     'A pár (תֹהוּ וָבֹהוּ) helyén az LXX egyetlen szót ír: ἰδοὺ οὐθέν („íme, semmi”). A Macula a két héber szót nem '
     'illeszti (hiányzó forrás, nem ellenkező állítás), ezért egyforrású.',
     'valoszinu', PROV % ('Jer 4:23 H8414', FORRAS_LXX)],
    ['LD094', 'Jer 4:23', 'Jeremiah (LXX) 4:23', 'H0922', '', '', '', 'lxx_minusz',
     'A וָבֹהוּ-nak nincs külön görög szava: az LXX a párt az egy οὐθέν-nel adja (l. LD093). A Macula nem illeszt.',
     'valoszinu', PROV % ('Jer 4:23 H0922', FORRAS_LXX)],
    ['LD095', 'Ézs 34:11', 'Isaiah 34:11', 'H8414', 'ἔρημος', 'G2048', '18', 'eltero_forditas',
     'A קַו־תֹהוּ („a kietlenség mérőzsinórja”) helyén: σπαρτίον γεωμετρίας ἐρήμου; a תֹהוּ megfelelője az ἐρήμου '
     '(ἔρημος). Macula és LXX_OS egyezik.',
     'biztos', PROV % ('Ézs 34:11 H8414', FORRAS_KETTO)],
    ['LD096', 'Ézs 34:11', 'Isaiah 34:11', 'H0922', '', '', '', 'lxx_minusz',
     'Az אַבְנֵי־בֹהוּ („az üresség kövei”) tagnak nincs görög megfelelője a versben (az LXX helyén ὀνοκένταυροι áll); '
     'a Macula sem illeszt görög szót. A hiány explicit, nem pótolt.',
     'valoszinu', PROV % ('Ézs 34:11 H0922', FORRAS_LXX)],
]
AUDIT = [
    ['TEREMT-002', 'B4', 'scope=range:1Móz 1:2 | forras=LXX_OS/genesis.tsv+TAGNT_kivonat.tsv | n=19 | ts=2026-11-02T11:33Z',
     '2026.11.02'],
    ['TEREMT-002', 'B4', 'scope=range:Jer 4:23 | forras=LXX_OS/jeremiah-lxx.tsv+TAGNT_kivonat.tsv | n=17 | ts=2026-11-02T11:33Z',
     '2026.11.02'],
    ['TEREMT-002', 'B4', 'scope=range:Ézs 34:11 | forras=LXX_OS/isaiah.tsv+TAGNT_kivonat.tsv | n=23 | ts=2026-11-02T11:33Z',
     '2026.11.02'],
]


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok) + '\n')
    if olvas(ut) != sorok:
        raise SystemExit('megállás: a visszaolvasott %s eltér' % ut)


def main():
    lsorok = olvas(LXX)
    if next(s for s in lsorok if not s.startswith('#')).split('\t') != FEJ:
        raise SystemExit('megállás: az lxx_dontesek.tsv fejléce eltér')
    idk = {s.split('\t')[0] for s in lsorok}
    kulcs = {tuple(s.split('\t')[1:4:2]) for s in lsorok}
    for r in SOROK:
        if len(r) != len(FEJ) or r[0] in idk or (r[1], r[3]) in kulcs or any('\t' in m for m in r):
            raise SystemExit('megállás: hibás vagy meglévő sor: %s' % r[0])
    asorok = olvas(AUD)
    meglevo = set(asorok)
    for r in AUDIT:
        if '\t'.join(r) in meglevo:
            raise SystemExit('megállás: az audit-sor már létezik: %s' % r[2])
    l_uj = lsorok + ['\t'.join(r) for r in SOROK]
    a_uj = asorok + ['\t'.join(r) for r in AUDIT]
    print('lxx_dontesek.tsv: +%d sor; auditok.tsv: +%d sor' % (len(SOROK), len(AUDIT)))
    if '--ir' not in sys.argv:
        print('száraz futás: nincs írás (--ir)')
        return
    ir(LXX, l_uj)
    ir(AUD, a_uj)
    print('írva')


if __name__ == '__main__':
    main()
