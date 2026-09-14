#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""f4_0c_korut_ellenoriz.py — a Tétel B (csv-írók kiváltása) elfogadási mérése.

A kérdés, amit megválaszol: az `'\\t'.join()`-os író bájtra ugyanazt írja-e,
amit a kiváltott `csv` modulos író írt volna — és bájtra ugyanazt-e, ami ma a
táblában áll.

**A referencia a `git show HEAD:<fájl>` kimenete, NEM a munkafában lévő fájl.**
A repó `core.autocrlf=true`-val megy, tehát a munkafa sorvége checkoutonként
változhat; a blob viszont stabil, és a commit is oda kerül (F4_BRIEF.md, B20).

Táblánként két mérés, mindkettő a blob sorain:

  UJ   — a sorokat `split('\\t')`-vel szétvágva, az új íróval visszaírva:
         hány sor tér el a blobtól? Elvárt: 0. Ez a bájthűség bizonyítéka.

  REGI — ugyanazok a sorok a kiváltott `csv` modulos íróval visszaírva:
         hány sor tér el a blobtól? Ahol ez > 0, ott a régi író rontott volna
         egy körúttól; ahol 0, ott a csere bizonyítottan bájtra semleges.

A REGI oszlop miatt ez a szkript — a `csv_karmeres.py`-hoz hasonlóan —
szándékosan importálja a `csv` modult: a mérés tárgya maga a modul. Ez a két
fájl az E1-grep két tudatos kivétele; egyik sem ír kanonikus táblát.

Futtatás a repó gyökeréből:
    python eszkozok/f4_0c_korut_ellenoriz.py
Kilépési kód 1, ha bármely tábla UJ-eltérése nem 0.
"""

import io
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RIPORT = os.path.join(ROOT, 'naplok', 'F4_0c_korut_ellenoriz.tsv')

# A Tétel B tíz írási helyének céltáblái, amelyek a HEAD-ben is benne vannak.
# A többi célfájl (args.kimenet, eszkozok/f3_4_munkalap.tsv, phaseA_all.tsv,
# step1_decisions.tsv) nincs verziókövetve, tehát nincs mihez mérni.
IRO_CELTABLAK = {
    'adat/grammatikai_strongok.tsv': 'grammatikai_strongok_general.py:231',
    'konkordancia/Karoli_Strong_kivonat.tsv': 'merge_karoli_szofaj.py:48 (helyben!)',
    'konkordancia/TAHOT_kivonat.tsv': 'tahot_karoli_kulcs_generalas.py:220',
    'konkordancia/TAHOT_kivonat_nyitott_esetek.tsv': 'tahot_karoli_kulcs_generalas.py:227',
    'konkordancia/Betu_utotag_kizarva.tsv': 'lxx_kivonat_fetch_v2.py:106 (hozzáfűz)',
}


def tsv_sor(mezok):
    """Egy TSV-sor a csv modul nélkül — a Tétel B-ben bevezetett író.

    Szó szerint ugyanaz a törzs, ami a nyolc kicserélt szkriptbe került;
    itt a mérés tárgyaként szerepel.
    """
    ki = []
    for m in mezok:
        m = '' if m is None else str(m)
        if '\t' in m or '\n' in m or '\r' in m:
            raise ValueError('elválasztó a mezőben: %r' % (m,))
        ki.append(m)
    return '\t'.join(ki) + '\n'


def regi_tsv_sor(mezok):
    """A kiváltott író: csv.writer(delimiter=TAB, lineterminator=LF)."""
    import csv
    puffer = io.StringIO()
    csv.writer(puffer, delimiter='\t', lineterminator='\n').writerow(list(mezok))
    return puffer.getvalue()


def head_blob_sorok(ut):
    """A HEAD-blob sorai, sorvég nélkül; + zárul-e a blob sorvéggel."""
    nyers = subprocess.check_output(
        ['git', 'show', 'HEAD:' + ut], cwd=ROOT)
    szoveg = nyers.decode('utf-8')
    veg_ujsor = szoveg.endswith('\n')
    sorok = szoveg.split('\n')
    if veg_ujsor:
        sorok = sorok[:-1]
    return sorok, veg_ujsor, szoveg


def merj(ut):
    sorok, veg_ujsor, szoveg = head_blob_sorok(ut)
    uj_elteres = 0
    regi_elteres = 0
    uj_elso = ''
    regi_elso = ''
    cr_sor = 0
    for s in sorok:
        if '\r' in s:
            cr_sor += 1
            continue
        mezok = s.split('\t')
        u = tsv_sor(mezok)
        if u != s + '\n':
            uj_elteres += 1
            if not uj_elso:
                uj_elso = s[:120]
        r = regi_tsv_sor(mezok)
        if r != s + '\n':
            regi_elteres += 1
            if not regi_elso:
                regi_elso = s[:120]
    return {
        'fajl': ut,
        'sorok': len(sorok),
        'veg_ujsor': 'igen' if veg_ujsor else 'NEM',
        'cr_sor': cr_sor,
        'uj_eltero_sor': uj_elteres,
        'regi_eltero_sor': regi_elteres,
        # a mintasorban tab van; a riport maga is TSV, tehát láthatóvá tesszük
        'uj_elso_eltero': mintara(uj_elso),
        'regi_elso_eltero': mintara(regi_elso[:80]),
    }


def mintara(s):
    """Mintasor riport-mezőbe: az elválasztók láthatóvá téve."""
    if not s:
        return '-'
    return s.replace('\t', '\\t').replace('\r', '\\r').replace('\n', '\\n')


def main():
    tablak = subprocess.check_output(
        ['git', 'ls-files', 'adat/', 'konkordancia/'], cwd=ROOT
    ).decode('utf-8').split('\n')
    tablak = sorted(t.strip() for t in tablak if t.strip().endswith('.tsv'))

    print('Táblák (HEAD-blobból): %d' % len(tablak))
    print('Referencia: git show HEAD:<fájl> — NEM a munkafa (core.autocrlf=true).\n')

    eredmenyek = []
    for ut in tablak:
        e = merj(ut)
        e['iro_hivas'] = IRO_CELTABLAK.get(ut, '-')
        eredmenyek.append(e)
        if e['uj_eltero_sor'] or e['regi_eltero_sor'] or e['cr_sor']:
            print('  %-52s UJ=%-6d REGI=%-6d CR=%d'
                  % (ut, e['uj_eltero_sor'], e['regi_eltero_sor'], e['cr_sor']))

    mezok = ['fajl', 'iro_hivas', 'sorok', 'veg_ujsor', 'cr_sor',
             'uj_eltero_sor', 'regi_eltero_sor', 'uj_elso_eltero', 'regi_elso_eltero']
    with io.open(RIPORT, 'w', encoding='utf-8', newline='') as f:
        f.write('# GENERÁLT: eszkozok/f4_0c_korut_ellenoriz.py — kézzel nem szerkesztendő.\n')
        f.write('# Referencia: git show HEAD:<fájl>. UJ = az új író eltérése a blobtól\n')
        f.write('# (elvárt 0); REGI = a kiváltott csv-író eltérése ugyanattól a blobtól.\n')
        f.write(tsv_sor(mezok))
        for e in eredmenyek:
            f.write(tsv_sor([e[k] for k in mezok]))

    uj_hibas = [e for e in eredmenyek if e['uj_eltero_sor']]
    regi_hibas = [e for e in eredmenyek if e['regi_eltero_sor']]
    nincs_veg = [e for e in eredmenyek if e['veg_ujsor'] == 'NEM']
    cr = [e for e in eredmenyek if e['cr_sor']]

    print('\n--- Összegzés ---')
    print('Tábla összesen:                         %d' % len(eredmenyek))
    print('Adatsor összesen:                       %d' % sum(e['sorok'] for e in eredmenyek))
    print('UJ író: bájtra eltérő tábla:            %d' % len(uj_hibas))
    print('REGI (csv) író: bájtra eltérő tábla:    %d' % len(regi_hibas))
    if regi_hibas:
        for e in regi_hibas:
            print('    %-50s %d sor' % (e['fajl'], e['regi_eltero_sor']))
    print('Blob nem zárul sorvéggel:               %d' % len(nincs_veg))
    print('CR-t tartalmazó sor van a blobban:      %d tábla' % len(cr))
    print('\nA tíz írási hely céltáblái közül a HEAD-ben: %d'
          % sum(1 for e in eredmenyek if e['iro_hivas'] != '-'))
    for e in eredmenyek:
        if e['iro_hivas'] != '-':
            print('  %-50s UJ=%d REGI=%d  <- %s'
                  % (e['fajl'], e['uj_eltero_sor'], e['regi_eltero_sor'], e['iro_hivas']))

    print('\nRiport: %s' % os.path.relpath(RIPORT, ROOT))
    if uj_hibas:
        print('\nMEGÁLLÁS: az új író nem bájthű %d táblán.' % len(uj_hibas), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
