#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F170_kodkonyv_angol.py -- a kódkönyv (`adat/nyilt_kodkonyv.tsv`) sorai az angol réteg új oszlopaihoz (F170.3–4).
Egyszeri, idempotens szerkesztő-segéd: a `strong_glossza_en`, a szabad szöveg `<oszlop>_en` párjai és a
`forditas_modja` oszlopsorai; a `jelentes_en` leírásának pontosítása (szótári kivonat, nem a STEPBible-glossza).
A meglévő sorok mezői a `jelentes_en` sor két leírásán kívül nem változnak (írás előtt összevetve).
Használat: python naplok/F170_kodkonyv_angol.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import nyilt_mag_export as E  # noqa: E402

KK = os.path.join(GY, 'adat', 'nyilt_kodkonyv.tsv')
PROV = 'scope=manual | forras=F170 NYILT_MAG_ANGOL: az angol réteg oszlopai (F170.3–4) | ts=2026-11-05'

JEL_HU = ('A szótári jelentés angolul: kivonat a sor `szotar` oszlopában megnevezett szótár (BDB, Thayer: közkincs; '
          'TBESG: CC BY 4.0) szócikkének szövegéből, a jelentés számával (`jelentes_szam`). Szótári kivonat, nem a '
          'STEPBible rövid glosszája; az angol szófogódzót a `strong_glossza_en` adja.')
JEL_EN = ('The dictionary meaning in English: an excerpt from the text of the entry in the dictionary named in the '
          'row’s `szotar` column (BDB, Thayer: public domain; TBESG: CC BY 4.0), for the meaning numbered in '
          '`jelentes_szam`. A dictionary excerpt, not the short STEPBible gloss; the short English word cue is '
          '`strong_glossza_en`.')
GLO_HU = ('Rövid angol szófogódzó: a sor Strong-számának glosszája a STEPBible TBESH (héber) és TBESG (görög) '
          'lexikonjából (a Gloss oszlop; a Meaning oszlop nem). Több Strong-számnál ` + `-szal fűzve, a sorrendjük '
          'szerint; ha a Strong-számnak több fő bejegyzése van (pl. név és köznév), ` / `-rel. A glossza a Strong-szám '
          'egészére szól, nem az adott vers jelentésére (arra a `jelentes_en`). Forrás: Data created by '
          'www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0).')
GLO_EN = ('Short English word cue: the gloss of the row’s Strong number from the STEPBible TBESH (Hebrew) and TBESG '
          '(Greek) lexicons (the Gloss column, not the Meaning column). With several Strong numbers joined by ` + ` in '
          'their order; where a Strong number has several main entries (e.g. a name and a common noun), by ` / `. The '
          'gloss belongs to the Strong number as a whole, not to the meaning in the verse (for that, see `jelentes_en`). '
          'Source: Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0).')
EN_HU = ('Az előző oszlop (%s) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg '
         'a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg '
         'változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg '
         'marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).')
EN_EN = ('English counterpart of the text in the preceding column (%s): a **machine translation**; the row’s '
         '`forditas_modja` column names the model. The translation belongs to the given version of the Hungarian '
         'text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the '
         'gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering '
         'in square brackets (not the text of an English Bible translation).')
FM_HU = ('A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a '
         'ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs '
         'érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt '
         'értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.')
FM_EN = ('How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine '
         'translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid '
         'translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of '
         'closed-vocabulary values are not machine translations but edited codebook labels.')


def main():
    with open(KK, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    I = {k: fej.index(k) for k in fej}
    kulcsok = set()
    for i in range(fej_i + 1, len(sorok)):
        if not sorok[i] or sorok[i].startswith('#'):
            continue
        m = sorok[i].split('\t')
        kulcsok.add((m[0], m[1], m[2]))
        if (m[0], m[1], m[2]) == ('elofordulasok.tsv', 'jelentes_en', ''):
            m[I['leiras_hu']], m[I['leiras_en']] = JEL_HU, JEL_EN
            sorok[i] = '\t'.join(m)

    def sor(t, o, hu, en):
        m = [''] * len(fej)
        m[I['tabla']], m[I['oszlop']], m[I['leiras_hu']], m[I['leiras_en']], m[I['proveniencia']] = t, o, hu, en, PROV
        return '\t'.join(m)

    uj = []
    if ('elofordulasok.tsv', 'strong_glossza_en', '') not in kulcsok:
        uj.append(sor('elofordulasok.tsv', 'strong_glossza_en', GLO_HU, GLO_EN))
    for t, mezok in sorted(E.SZABAD.items()):
        for o in mezok:
            if (t, o + '_en', '') not in kulcsok:
                uj.append(sor(t, o + '_en', EN_HU % o, EN_EN % o))
        if (t, 'forditas_modja', '') not in kulcsok:
            uj.append(sor(t, 'forditas_modja', FM_HU, FM_EN))
    with open(KK, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok + uj) + '\n')
    print('új sor: %d' % len(uj))


if __name__ == '__main__':
    main()
