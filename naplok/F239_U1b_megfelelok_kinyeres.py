"""F239.U1b (C-vh, SEMA 2.53): a TEREMT-001 visszhang-megfelelőinek modell-kinyerése (első kéz).

A lánc-szó a תְּהוֹם (tehóm, H8415) a motívum 35 ószövetségi versében (a 34 vers + Jób 41:32; a szerkesztő
döntése: a motívum határa az ÓSZ-ben a héber szó), az ἄβυσσος (abüsszosz, G0012) a 9 újszövetségi versben. A
Targum (Targum_PD: csak az Onkelos, a Mózes-könyvek; a Jonatan-sorok a lapon nem renderelnek, ezért nem
kinyertek) és a Vulgata (Clementina) megfelelője: az alak a forrás versszövegéből szó szerint, a kinyerő olvasta
(claude-sonnet-5-5, 2026-11-23). A hiány kimondva: a Zsoltárok, a Jób és a Példabeszédek Targuma nincs a szabad
forrásban; a Péld 8:28 Vulgata-szövege a tehóm szavát nem tartalmazza. A BDB rokon nyelvi háttere: a szócikkben
és a Sefaria-gyorsítótárban rokon nyelvi adat nincs. A második kéz ítélete külön átnézés-bemenet
(`naplok/F239_U1b_megfelelok_atnezes.tsv`), a beolvasás: `eszkozok/visszhang/megfelelo_kinyer.py beolvas`.

Kimenet: `naplok/F239_U1b_megfelelok_kinyert.tsv`. Futtatás: python naplok/F239_U1b_megfelelok_kinyeres.py
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 'TEREMT-001'
MODELL = 'claude-sonnet-5-5'
TS = '2026-11-23'
OSZLOP = ['motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas', 'megjegyzes',
          'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
TEH = 'תְּהוֹמָא'

TARGUM = [   # (igehely, alak, lemma, jelentés, megjegyzés)
    ('1Móz 1:2', 'תְהוֹמָא', TEH, 'mélység', ''),
    ('1Móz 7:11', 'תְּהוֹמָא', TEH, 'mélység', ''),
    ('1Móz 8:2', 'תְהוֹמָא', TEH, 'mélység', ''),
    ('1Móz 49:25', 'מִמַעֲמַקֵי', 'מַעֲמַק', 'mélységek',
     'a héber „lent heverő mélység” helyén a Targum a „föld mélységei alulról” kifejezést írja (מִמַעֲמַקֵי אַרְעָא מִלְרָע): a '
     'tehóm szava nincs a versben'),
    ('2Móz 15:5', 'תְּהוֹמַיָא', TEH, 'mélység', ''),
    ('2Móz 15:8', 'תְהוֹמִין', TEH, 'mélység', ''),
    ('5Móz 8:7', 'וּתְהוֹמִין', TEH, 'mélység', ''),
    ('5Móz 33:13', 'וּתְהוֹמִין', TEH, 'mélység',
     'a mondat a forrásokat és a mélységeket együtt említi; a „mélységek” (תְּהוֹמִין) mellett a „föld mélységei alulról” '
     'kifejezés is áll (מִמַעֲמַקֵי אַרְעָא מִלְרָע)'),
]
# (igehely, alak, megjegyzés); az alap-lemma: abyssus
VULGATA_OSZ = [
    ('1Móz 1:2', 'abyssi', ''), ('1Móz 7:11', 'abyssi', ''), ('1Móz 8:2', 'abyssi', ''),
    ('1Móz 49:25', 'abyssi', ''), ('2Móz 15:5', 'Abyssi', ''), ('2Móz 15:8', 'abyssi', ''),
    ('5Móz 8:7', 'abyssi', ''), ('5Móz 33:13', 'abysso', ''),
    ('Jób 28:14', 'Abyssus', ''), ('Jób 38:16', 'abyssi', ''), ('Jób 38:30', 'abyssi', ''),
    ('Zsolt 33:7', 'abyssos', 'a forrásban a Vulgata számozása szerint (Zsolt 32:7) áll'),
    ('Zsolt 36:7', 'abyssus', 'a forrásban a Vulgata számozása szerint (Zsolt 35:7) áll'),
    ('Zsolt 42:8', 'Abyssus · abyssum', 'a forrásban a Vulgata számozása szerint (Zsolt 41:8) áll; a két tehóm két latin alakban'),
    ('Zsolt 71:20', 'abyssis', 'a forrásban a Vulgata számozása szerint (Zsolt 70:20) áll'),
    ('Zsolt 77:17', 'abyssi', 'a forrásban a Vulgata számozása szerint (Zsolt 76:17) áll'),
    ('Zsolt 78:15', 'abysso', 'a forrásban a Vulgata számozása szerint (Zsolt 77:15) áll'),
    ('Zsolt 104:6', 'Abyssus', 'a forrásban a Vulgata számozása szerint (Zsolt 103:6) áll'),
    ('Zsolt 106:9', 'abyssis', 'a forrásban a Vulgata számozása szerint (Zsolt 105:9) áll'),
    ('Zsolt 107:26', 'abyssos', 'a forrásban a Vulgata számozása szerint (Zsolt 106:26) áll'),
    ('Zsolt 135:6', 'abyssis', 'a forrásban a Vulgata számozása szerint (Zsolt 134:6) áll'),
    ('Zsolt 148:7', 'abyssi', ''),
    ('Péld 3:20', 'abyssi', ''), ('Péld 8:24', 'abyssi', ''), ('Péld 8:27', 'abyssos', ''),
    ('Péld 8:28', '', 'a „mélység forrásai” (עִינוֹת תְּהוֹם) helyén a latin csak „fontes aquarum”-ot (a vizek forrásait) '
                      'ír: a mélység szava nincs a versben'),
    ('Ézs 51:10', 'abyssi', ''), ('Ézs 63:13', 'abyssos', ''), ('Ez 26:19', 'abyssum', ''),
    ('Ez 31:4', 'abyssus', ''), ('Ez 31:15', 'abysso', ''), ('Ámós 7:4', 'abyssum', ''),
    ('Hab 3:10', 'abyssus', ''), ('Jón 2:6', 'abyssus', ''),
    ('Jób 41:32', 'abyssum', 'a forrásban a Vulgata számozása szerint (Jób 41:23) áll'),
]
VULGATA_USZ = [
    ('Luk 8:31', 'abyssum', ''), ('Róm 10:7', 'abyssum', ''), ('Jel 9:1', 'abyssi', ''), ('Jel 9:2', 'abyssi', ''),
    ('Jel 9:11', 'abyssi', ''), ('Jel 11:7', 'abysso', ''), ('Jel 17:8', 'abysso', ''), ('Jel 20:1', 'abyssi', ''),
    ('Jel 20:3', 'abyssum', ''),
]


def sor(strong, ige, forras, alak, lemma, jel, megj, fajl, jelzo):
    return {'motivum': M, 'strong': strong, 'igehely': ige, 'forras': forras, 'alak': alak, 'lemma': lemma,
            'kiejtes': '', 'jelentes': jel, 'betoldas': 'nem', 'megjegyzes': megj, 'kinyeres': 'modell',
            'modell': MODELL, 'ellenorzes': '',
            'proveniencia': 'scope=%s %s %s %s | forras=%s | ts=%s' % (M, jelzo, strong, ige, fajl, TS)}


def main():
    sorok = [sor('H8415', i, 'targum', a, l, j, m, 'Targum_PD.tsv', 'lánc-szó') for i, a, l, j, m in TARGUM]
    sorok += [sor('H8415', i, 'vulgata', a, 'abyssus' if a else '', 'mélység' if a else '', m,
                  'Vulgata_Clementina.tsv', 'lánc-szó') for i, a, m in VULGATA_OSZ]
    sorok += [sor('G0012', i, 'vulgata', a, 'abyssus', 'mélység', m, 'Vulgata_Clementina.tsv', 'lánc-szó')
              for i, a, m in VULGATA_USZ]
    sorok.append({'motivum': M, 'strong': 'H8415', 'igehely': '', 'forras': 'bdb', 'alak': '', 'lemma': '',
                  'kiejtes': '', 'jelentes': '', 'betoldas': 'nem', 'megjegyzes': 'a BDB-szócikkben nincs rokon nyelvi adat',
                  'kinyeres': 'modell', 'modell': MODELL, 'ellenorzes': '',
                  'proveniencia': 'scope=%s BDB rokon nyelv H8415 | forras=BDB_teljes_unabridged.tsv | ts=%s' % (M, TS)})
    ki = os.path.join(GYOKER, 'naplok', 'F239_U1b_megfelelok_kinyert.tsv')
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(OSZLOP) + '\n')
        for r in sorok:
            f.write('\t'.join(r[o] for o in OSZLOP) + '\n')
    print('%s: %d sor' % (os.path.relpath(ki, GYOKER), len(sorok)))


main()
