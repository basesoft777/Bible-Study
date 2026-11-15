"""F194.6 (K65, K66, K67a; SEMA 2.53): az ISTENTISZT-001 visszhang-megfelelőinek modell-kinyerése (első kéz).

A formula igéje, a קָרָא (kárá, H7121) a 16 ószövetségi előfordulás-versben: a Targum (Targum_PD: Onkelos, Jonatan) és
a Vulgata (Clementina) megfelelője; az ἐπικαλέω (epikaleó, G1941) a 4 újszövetségi versben: a Vulgata megfelelője. Az
alak a forrás versszövegéből szó szerint (a kinyerő olvasta: claude-opus-5-5, 2026-11-12). A hiány kimondva: a
Zsoltárok Targuma nincs a szabad forrásban, a sor alak nélkül áll. A második kéz ítélete külön átnézés-bemenet
(`naplok/F194_megfelelok_atnezes.tsv`), a beolvasás: `eszkozok/visszhang/megfelelo_kinyer.py beolvas`.

A kimenet: `naplok/F194_megfelelok_kinyert.tsv`. Futtatás: python naplok/F194_megfelelok_kinyeres.py
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 'ISTENTISZT-001'
MODELL = 'claude-opus-5-5'
TS = '2026-11-12'
OSZLOP = ['motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas', 'megjegyzes',
          'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
ZSOLT_HIANY = 'a Zsoltárok Targuma nincs a szabad forrásban (Targum_PD: Onkelos és Jonatan), a megfelelő nem azonosítható'

TARGUM = [   # (igehely, alak, lemma, kiejtés, jelentés, megjegyzés)
    ('1Móz 4:26', 'מִלְּצַלָּאָה', 'צְלָא', 'millecalláá', 'imádkozik',
     'a Targum a hívást az imádkozás szavával adja vissza, de a mondatot megfordítja: Énós napjaiban az emberek '
     'felhagytak az imádkozással (חָלוּ … מִלְּצַלָּאָה, chálú … millecalláá)'),
    ('1Móz 12:8', 'וְצַלִּי', 'צְלָא', 'vecallí', 'imádkozik', 'a hívás helyén az imádkozás igéje áll'),
    ('1Móz 13:4', 'וְצַלֵּי', 'צְלָא', 'vecallé', 'imádkozik', ''),
    ('1Móz 21:33', 'וְצַלִּי', 'צְלָא', 'vecallí', 'imádkozik', ''),
    ('1Móz 26:25', 'וְצַלִּי', 'צְלָא', 'vecallí', 'imádkozik', ''),
    ('2Móz 33:19', 'וְאֶקְרֵי', 'קְרָא', 'veekré', 'hív, kiált',
     'itt a Targum megtartja a hívás igéjét, nem az imádkozásét'),
    ('2Móz 34:5', 'וּקְרָא', 'קְרָא', 'úkerá', 'hív, kiált', 'itt a Targum megtartja a hívás igéjét, nem az imádkozásét'),
    ('1Kir 18:24', 'וְתִקְרוּן · אֲצַלֵי', 'קְרָא · צְלָא', 'vetikrún · acalé', 'hív · imádkozik',
     'a Baál prófétáinak hívását a hívás igéje, Illését az imádkozásé adja vissza'),
    ('1Kir 18:25', 'וּקְרוֹ', 'קְרָא', 'úkeró', 'hív, kiált',
     'a Baál prófétáinak hívása: a Targum a hívás igéjét és a nevet tartja, de a héber „isteneitek” helyén „a ti '
     'bálványaitok” áll (בְּשׁוּם טַעֲוַתְכוֹן, besúm taavatchón, „a ti bálványaitok nevében”)'),
    ('1Kir 18:26', 'וּקְרוֹ', 'קְרָא', 'úkeró', 'hív, kiált', 'a Baál prófétáinak hívása: a hívás igéje marad'),
    ('2Kir 5:11', 'וִיצַלֵי', 'צְלָא', 'vícalé', 'imádkozik', ''),
    ('Sof 3:9', 'לְצַלָאָה', 'צְלָא', 'lecaláá', 'imádkozik', ''),
    ('Jóel 2:32', 'דְצַלֵי', 'צְלָא', 'decalé', 'imádkozik',
     'a forrásban a héber számozás szerinti kulcson (Jóel 3:5) áll'),
    ('Zsolt 116:4', '', '', '', '', ZSOLT_HIANY),
    ('Zsolt 116:13', '', '', '', '', ZSOLT_HIANY),
    ('Zsolt 116:17', '', '', '', '', ZSOLT_HIANY),
]
VULGATA_OSZ = [
    ('1Móz 4:26', 'invocare', ''), ('1Móz 12:8', 'invocavit', ''), ('1Móz 13:4', 'invocavit', ''),
    ('1Móz 21:33', 'invocavit', ''), ('1Móz 26:25', 'invocato', ''),
    ('2Móz 33:19', 'vocabo', 'a latin itt előtag nélküli igét (voco) ír, nem az invoco-t'),
    ('2Móz 34:5', 'invocans', 'a Vulgata a segítségül hívást Mózesnek tulajdonítja: „stetit Moyses cum eo, invocans”'),
    ('1Kir 18:24', 'Invocate · invocabo', ''), ('1Kir 18:25', 'invocate', ''), ('1Kir 18:26', 'invocabant', ''),
    ('2Kir 5:11', 'invocaret', ''), ('Jóel 2:32', 'invocaverit', ''), ('Sof 3:9', 'invocent', ''),
    ('Zsolt 116:4', 'invocavi', 'a forrásban a Vulgata számozása szerint (Zsolt 114:4) áll'),
    ('Zsolt 116:13', 'invocabo', 'a forrásban a Vulgata számozása szerint (Zsolt 115:4) áll'),
    ('Zsolt 116:17', 'invocabo', 'a forrásban a Vulgata számozása szerint (Zsolt 115:8) áll'),
]
VULGATA_USZ = [
    ('ApCsel 2:21', 'invocaverit', ''), ('Róm 10:13', 'invocaverit', ''), ('1Kor 1:2', 'invocant', ''),
    ('ApCsel 22:16', 'invocato', 'a Vulgata a „nomine ipsius” alakot követi, mint a kritikai görög szöveg (αὐτοῦ)'),
]


def sor(strong, ige, forras, alak, lemma, kiej, jel, megj, fajl):
    return {'motivum': M, 'strong': strong, 'igehely': ige, 'forras': forras, 'alak': alak, 'lemma': lemma,
            'kiejtes': kiej, 'jelentes': jel, 'betoldas': 'nem', 'megjegyzes': megj, 'kinyeres': 'modell',
            'modell': MODELL, 'ellenorzes': '',
            'proveniencia': 'scope=%s formula-ige %s %s | forras=%s | ts=%s' % (M, strong, ige, fajl, TS)}


def main():
    sorok = [sor('H7121', i, 'targum', a, l, k, j, m, 'Targum_PD.tsv') for i, a, l, k, j, m in TARGUM]
    sorok += [sor('H7121', i, 'vulgata', a, 'voco' if a == 'vocabo' else 'invoco', '', 'hív, kiált' if a == 'vocabo'
                  else 'segítségül hív', m, 'Vulgata_Clementina.tsv') for i, a, m in VULGATA_OSZ]
    sorok += [sor('G1941', i, 'vulgata', a, 'invoco', '', 'segítségül hív', m, 'Vulgata_Clementina.tsv')
              for i, a, m in VULGATA_USZ]
    ki = os.path.join(GYOKER, 'naplok', 'F194_megfelelok_kinyert.tsv')
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(OSZLOP) + '\n')
        for r in sorok:
            f.write('\t'.join(r[o] for o in OSZLOP) + '\n')
    print('%s: %d sor' % (os.path.relpath(ki, GYOKER), len(sorok)))


if __name__ == '__main__':
    main()
