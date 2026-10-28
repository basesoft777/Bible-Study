#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/glossza_lexikon_forditas.py -- F121 GLOSSZA_FORDITAS (DT-F121b: a #140 eszkozetol kulon fajl):
a lexikonoldalak "(forditasra var)" jelolesu szotari egysegeinek listaja es rogzitese.

  lista --id ISTENTISZT-001 [--kimenet <repon kivuli konyvtar>]
      A generator sajat forditas_ehhez() hivasait naplozza egy repon kivuli lexikon-renderben, igy a
      kulcs es a forrasszoveg pontosan az, amit a lap keres. Kimenet: naplok/F121_GLOSSZA_FORDITAS_lista.tsv
      (kulcs, forrasszoveg, forras_hash, allapot: megvan / hianyzik / elavult).
  A forrasszoveg-feloldo (forras_szoveg) a 13. szabaly (ellenoriz.py) forrasa is: egy feloldo, nem ket masolat.

Olvasas split('\\t')-bel (CLAUDE.md: a csv modul tilos).
"""
import sys
import os
import hashlib
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(GYOKER, 'konkordancia')
LISTA = os.path.join(GYOKER, 'naplok', 'F121_GLOSSZA_FORDITAS_lista.tsv')
DBH_JELENTESEK = os.path.join(KONKORDANCIA, 'UBS_DBH_jelentesek.tsv')
FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forras_hossz',
          'allapot', 'forrasszoveg']
EM_DASH = '—'

# szotar -> melyik forrasoszlopbol szarmazik a mezo forrasszovege (SEMA 2.14)
DBH_MEZOK = {'definicio_hu': 'definicio_rovid', 'glosszak_hu': 'glosszak'}


def sha1(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def tsv_sorok(path):
    """Fejlecsoros TSV, '#'-megjegyzessorok nelkul; split('\\t')."""
    with open(path, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


_dbh_idx = None


def dbh_forras_idx(konkordancia_dir=KONKORDANCIA):
    """{(strong, lexid, mezo): forrasszoveg} az UBS_DBH_jelentesek.tsv-bol (strongonkent az elso sor)."""
    global _dbh_idx
    idx = {}
    for r in tsv_sorok(os.path.join(konkordancia_dir, 'UBS_DBH_jelentesek.tsv')):
        for mezo, oszlop in DBH_MEZOK.items():
            idx.setdefault((r['strong'], r['lexid'], mezo), r.get(oszlop, ''))
    return idx


def forras_szoveg_dbh(sor, idx):
    """Az UBS_DBH forditasok.tsv-sor forrasszovege (entry_id = lexid, jelentes_szam = '—'), kulonben None."""
    if sor.get('szotar') != 'UBS_DBH' or sor.get('jelentes_szam') != EM_DASH:
        return None
    return idx.get((sor['strong'], sor['entry_id'], sor['mezo']))


def lista_keszit(motivum_id, kimenet):
    """A generator forditas_ehhez() hivasait naplozva rendereli a lapot kimenet-be (repon kivuli konyvtar)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
    import lexikon_general as lg
    import general
    hivasok = {}
    eredeti = lg.forditas_ehhez

    def naplozo(szotar, strong, entry_id, jelentes_szam, mezo):
        hu = eredeti(szotar, strong, entry_id, jelentes_szam, mezo)
        hivasok.setdefault((szotar, strong, entry_id, jelentes_szam, mezo), bool(hu))
        return hu

    lg.forditas_ehhez = naplozo
    regi_argv = sys.argv
    sys.argv = ['general.py', '--cel', 'lexikon', '--id', motivum_id, '--kimenet', kimenet]
    try:
        general.main()
    finally:
        sys.argv = regi_argv
        lg.forditas_ehhez = eredeti
    return hivasok


def lista(motivum_id, kimenet=None):
    kimenet = kimenet or tempfile.mkdtemp(prefix='F121_lista_')
    if os.path.abspath(kimenet).startswith(GYOKER):
        raise SystemExit('a --kimenet a repon kivuli konyvtar legyen')
    hivasok = lista_keszit(motivum_id, kimenet)
    dbh = dbh_forras_idx()
    dntg = {(r['strong'], r['lexid'], r['entry_kod']): r for r in tsv_sorok(os.path.join(KONKORDANCIA, 'UBS_DNTG_jelentesek.tsv'))}
    kimeneti = []
    for kulcs, van in sorted(hivasok.items()):
        szotar, strong, entry_id, jsz, mezo = kulcs
        if van:
            continue
        forras = None
        if szotar == 'UBS_DBH':
            forras = dbh.get((strong, entry_id, mezo))
        elif szotar == 'UBS_DNTG':
            r = dntg.get((strong, entry_id, jsz))
            if r:
                forras = r.get({'definicio_hu': 'definicio_rovid', 'glosszak_hu': 'glosszak'}.get(mezo, ''), None)
        kimeneti.append((kulcs, forras))
    with open(LISTA, 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(FEJLEC) + '\n')
        for kulcs, forras in kimeneti:
            if forras is None:
                sor = list(kulcs) + ['', '', 'nincs_forras', '']
            else:
                sor = list(kulcs) + [sha1(forras), str(len(forras)), 'hianyzik', forras.replace('\t', ' ')]
            f.write('\t'.join(sor) + '\n')
    print('hianyzo egyedi egyseg: %d (lista: %s; render: %s)' % (len(kimeneti), LISTA, kimenet))
    for kulcs, forras in kimeneti:
        print(' ', kulcs, '' if forras is not None else '-- nincs forrasszoveg')
    return kimeneti


def main():
    a = sys.argv[1:]
    if not a or a[0] != 'lista' or '--id' not in a:
        raise SystemExit('hasznalat: glossza_lexikon_forditas.py lista --id <ID> [--kimenet <konyvtar>]')
    kim = a[a.index('--kimenet') + 1] if '--kimenet' in a else None
    lista(a[a.index('--id') + 1], kim)


if __name__ == '__main__':
    main()
