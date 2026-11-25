"""F239 U3 — a TEREMT-001 teljesség-mérésének két fájlja az új generátor rögzített útvonalán (adat/lapgen_bemenetek.tsv
B05: naplok/F123_teljesseg_<ID>.tsv, B06: naplok/F123_teljesseg_<ID>_blokkok.tsv). A mérés egy: a forrás az U1 F239-es
fájlja; a másolat bájtra azonos, egy MÁSOLAT-sorral a fejléc után. Futtatás: python naplok/F239_U3_teljesseg_masolat.py"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PAROK = [('F239_U1_TEREMT-001_teljesseg.tsv', 'F123_teljesseg_TEREMT-001.tsv', 'B05'),
         ('F239_U1_TEREMT-001_teljesseg_blokkok.tsv', 'F123_teljesseg_TEREMT-001_blokkok.tsv', 'B06')]
for forras, cel, b in PAROK:
    t = open(os.path.join(GY, 'naplok', forras), encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    elso, _, tobbi = t.partition(nl)
    jel = ('# MÁSOLAT: naplok/%s (F239 U3, 2026-11-23) — az új generátor %s bemenetének rögzített útvonala '
           '(adat/lapgen_bemenetek.tsv); a mérés egy, kézzel nem szerkesztendő' % (forras, b))
    open(os.path.join(GY, 'naplok', cel), 'w', encoding='utf-8', newline='').write(elso + nl + jel + nl + tobbi)
    print('%s → %s' % (forras, cel))
