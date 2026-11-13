# -*- coding: utf-8 -*-
"""F194.24 — a H7121 BDB rokon nyelvi sorainak második keze (claude-opus-5-5): soronkénti ítélet a BDB-szócikk fején
(konkordancia/BDB_teljes_unabridged.tsv, H7121: „Late Hebrew id., read aloud, read; Phoenician קרא call; Arabic read
aloud, recite (the Qur'an) …; Aramaic קְלרא, call, etc., so Old Aramaic קרא, Nabatean id., Palmyrene id., קרה”).
Kimenet: naplok/F194_bdb_rokon_atnezes.tsv (a megfelelo_kinyer.py beolvas --atnezes bemenete)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
ITELET = {
    'újhéber': 'A fej szerint „Late Hebrew id., read aloud, read”: az „id.” a héber jelentéssel azonosat jelöl, a felolvasás és olvasás új jelentés; alak a szócikkben nincs, a sor ezt mondja.',
    'föníciai': 'A fejben „Phoenician קרא call” áll: az írás szó szerint egyezik, a jelentés „hív”; pontozás nélküli alak, kiejtés helyesen nincs.',
    'arab': 'A fej az arab jelentést adja (read aloud, recite, a Korán), az arab írás a szövegből kiesett; a gyorsítótárban a szó nem szerepel, a hiány kimondva.',
    'arámi': 'A fejben „Aramaic קְלרא, call, etc.”: a ל az ר előtt nem tartozik a gyökhöz (szövegromlás), ezért helyes, hogy a sor alakot nem rögzít.',
    'óarámi': 'A fejben „so Old Aramaic קרא”: az írás szó szerint egyezik, a „so” az arámival azonos jelentést jelöl; kiejtés helyesen nincs.',
    'nabateus': 'A fejben „Nabatean id.”: az előző (arámi) alakra és jelentésre utal, külön alakot nem közöl; a sor ezt mondja.',
    'palmürai': 'A fejben „Palmyrene id., קרה”: az „id.” után álló קרה nyelvjelölés nélküli, a sor helyesen nem rendeli a palmüraihoz.',
}
sorok = [l.rstrip('\n').split('\t') for l in open('naplok/F194_bdb_rokon_kinyert.tsv', encoding='utf-8') if l.strip()]
fej = sorok[0]
ix = {k: i for i, k in enumerate(fej)}
ki = ['motivum\tstrong\tigehely\tforras\talak\tlemma\tjelentes\tatnezo\titelet\tmegjegyzes']
for r in sorok[1:]:
    ki.append('\t'.join([r[ix['motivum']], r[ix['strong']], r[ix['igehely']], r[ix['forras']], r[ix['alak']],
                         r[ix['lemma']], r[ix['jelentes']], 'claude-opus-5-5', 'jo', ITELET[r[ix['lemma']]]]))
open('naplok/F194_bdb_rokon_atnezes.tsv', 'w', encoding='utf-8', newline='\n').write('\n'.join(ki) + '\n')
print(len(ki) - 1)
