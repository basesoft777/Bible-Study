"""F213 mérés (bekötési audit, orkesztrátor, 2026-11-12): blokkonként hány Strongnál vagy témánál mutat a blokk magyar fordítást
a bekötés után (a fordítás előtte is a `pardes.db`-ben volt, az olvasó nem olvasta).

Futtatás (WSL): PARDES_DB=~/pardes/pardes.db python3 naplok/F213_bekotes_meres.py
"""
import os
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db = os.environ.get('PARDES_DB') or os.path.expanduser('~/pardes/pardes.db')
con = sqlite3.connect(db)
F = "FROM forditasok WHERE forditas_hu <> '' AND COALESCE(allapot, '') <> 'elavult' AND COALESCE(jelentes_szam, '') NOT LIKE '%~%'"


def egy(sql, *p):
    return con.execute(sql, p).fetchone()[0]


sorok = [
    ('szo.tbesg (glossza)', egy("SELECT COUNT(DISTINCT strong) %s AND szotar='TBESG' AND mezo='glosszak_hu'" % F),
     egy('SELECT COUNT(DISTINCT strong) FROM tbesg')),
    ('szo.tbesg (szócikk)', egy("SELECT COUNT(DISTINCT strong) %s AND szotar='TBESG' AND mezo='forditas_hu'" % F),
     egy('SELECT COUNT(DISTINCT strong) FROM tbesg')),
    ('szo.lsj', egy("SELECT COUNT(DISTINCT strong) %s AND szotar='LSJ'" % F), egy('SELECT COUNT(*) FROM lsj')),
    ('szo.sdbh (domén, Strong)', egy("SELECT COUNT(DISTINCT d.strong) FROM sdbh_domenek d WHERE d.domen_kod IN (SELECT entry_id %s AND szotar='SDBH')" % F),
     egy('SELECT COUNT(DISTINCT strong) FROM sdbh_domenek')),
    ('szo.sdgnt (domén, Strong)', egy("SELECT COUNT(DISTINCT d.strong) FROM sdgnt_domenek d WHERE d.domen_kod IN (SELECT entry_id %s AND szotar='SDGNT')" % F),
     egy('SELECT COUNT(DISTINCT strong) FROM sdgnt_domenek')),
    ('szo.tw_h / tw_g (tW-cikk)', egy("SELECT COUNT(DISTINCT entry_id) %s AND szotar='tW_szocikkek'" % F), egy('SELECT COUNT(*) FROM tw_szocikkek')),
    ('szo.tbesh (glossza, Strong)', egy("SELECT COUNT(DISTINCT t.strong) FROM tbesh t JOIN glosszak_heber_hu g ON g.strong=t.strong AND g.glossza_en=t.gloss "
                                        "WHERE g.glossza_hu <> ''"), egy('SELECT COUNT(DISTINCT strong) FROM tbesh')),
    ('szo.tbesh (szócikk)', egy("SELECT COUNT(DISTINCT strong) %s AND szotar='TBESH'" % F), egy('SELECT COUNT(DISTINCT strong) FROM tbesh')),
    ('vers.nave (téma)', egy("SELECT COUNT(DISTINCT tema_id) FROM nave_tema_hu WHERE magyar <> '' AND COALESCE(cimke_en, '') = ''"),
     egy('SELECT COUNT(DISTINCT tema_id) FROM nave_vers')),
    ('vers.nave (vers)', egy("SELECT COUNT(DISTINCT n.igehely) FROM nave_vers n WHERE n.tema_id IN (SELECT tema_id FROM nave_tema_hu WHERE magyar <> '')"),
     egy('SELECT COUNT(DISTINCT igehely) FROM nave_vers')),
]
print('blokk\tmagyar\tösszes')
for nev, hu, ossz in sorok:
    print('%s\t%d\t%d' % (nev, hu, ossz))
meta = dict(con.execute('SELECT kulcs, ertek FROM meta').fetchall()) if con.execute("SELECT 1 FROM sqlite_master WHERE name='meta'").fetchone() else {}
print('proveniencia: scope=pardes.db forditasok, nave_tema_hu, glosszak_heber_hu | forras=naplok/F213_bekotes_meres.py, pardes.db (%s) | ts=%s'
      % (meta.get('epites_ts', '?'), __import__('datetime').date.today().isoformat()))
