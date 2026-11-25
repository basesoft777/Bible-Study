# -*- coding: utf-8 -*-
"""F239 U1 2. pont: a teljesség-mérés eltérései -> `nyitva` jelölt-blokksorok (DT-F123o minta, lexémánként egy sor).
Bemenet: naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv + _teljesseg.tsv (a F239_U1_02_osztaly.py kimenete).
Kimenet: naplok/F239_U1_TEREMT-001_jelolt_sorok.tsv (jeloltek.tsv-séma). `--ir`: a sorok hozzáfűzése az adat/jeloltek.tsv-hez
(kulcs-ütközésnél és bármely régi sor eltérésénél megáll). TSV: split('\\t') / '\\t'.join(), csv modul nélkül."""
import sys, os, re
from collections import OrderedDict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
MID = 'TEREMT-001'
DATUM = '2026.11.23'
IR = '--ir' in sys.argv
BL = os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_teljesseg_blokkok.tsv')
TJ = os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_teljesseg.tsv')
KI = os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_jelolt_sorok.tsv')
JT = os.path.join(GY, 'adat', 'jeloltek.tsv')

def tsv(p):
    return [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')]

blokk = OrderedDict()
for c in tsv(BL)[1:]:
    blokk.setdefault((c[0], c[1]), []).append(c[2])
szavak, prov = {}, {}
for c in tsv(TJ)[1:]:
    if c[2] == 'ELTÉRÉS':
        szavak[(c[0], c[1])] = c[4]
    prov.setdefault(c[0], c[5])
tok = {}
for r in L.load_tahot() + L.load_tagnt():
    tok.setdefault(r['Strong-szám'], r)

def szerep(s):
    t = tok.get(s)
    if not t:
        return 'a %s szó' % s
    return 'a %s (%s, angolul „%s”)' % (t['Szótő'], t['Kiejtés'], t['Rövid jelentés'])

jel = [r for r in tsv(JT)[1:]]
hasznalt = {(r[0], r[1], r[9], r[10]) for r in jel}
sorok, vers_hasznalt = [], set()
for (h, k), vs in blokk.items():
    n = len(vs)
    szabad = next((v for v in vs if (MID, v, 'elofordulas', '') not in hasznalt and v not in vers_hasznalt), None)
    if szabad is None:
        for s in sorok:
            if s[1] in vs:
                s[4] += ' Ugyanez a vers a %s blokkban is áll (halo=%s, blokk=%s): %d vers, a lista a blokkok fájlban.' % ('Károli-szó háló' if h == 'karoli' else 'szótár-háló', h, k, n)
                break
        continue
    vers_hasznalt.add(szabad)
    if h == 'karoli':
        mind = []
        for v in vs:
            for w in re.split(r'[;,]\s*', szavak.get(('karoli', v), '')):
                w = w.strip()
                if w and w not in mind:
                    mind.append(w)
        karoli_szo = '; '.join(mind[:8])
        forras = ('F239 U1 teljesség-mérés, Károli-szó háló, blokk-sor (DT-F123o minta): %d vers, a sor igehelye a blokk egy verse; a lista: '
                  'naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv (halo=karoli, blokk=%s), naplok/F239_U1_TEREMT-001.md 2. pont | %s'
                  % (n, k, prov['karoli']))
        if k.startswith('osztálytalan:'):
            ind = ('Összesítő sor %d versre (a sor igehelye a blokk egy verse): a Károli „%s”-csoport szava áll bennük (Károli-szó háló), de a gépi '
                   'glossza-illesztés nem talált a mélység-szavak jelentéskörébe eső héber vagy görög szót; kézi olvasásra marad. '
                   'A versekben a motívum szavai (a תְּהוֹם és az ἄβυσσος) nem állnak.' % (n, k.split(':')[1]))
        else:
            ind = ('Összesítő sor %d versre (a sor igehelye a blokk egy verse): a Károli-szó háló találata. A versek szavai között %s áll '
                   '(gépi glossza-illesztés, nem ítélet); a vers Károli-fordításában mélység-csoportba tartozó szó áll; a motívum szavai (a תְּהוֹם és az ἄβυσσος) a versekben nem állnak. '
                   'Elbírálás az értelmező menetben, blokkban.' % (n, szerep(k)))
    else:
        karoli_szo = ''
        forras = ('F239 U1 teljesség-mérés, szótár-háló (BDB/Thayer), blokk-sor (DT-F123o minta): %d vers; a lista: '
                  'naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv (halo=szotar, blokk=szotar), naplok/F239_U1_TEREMT-001.md 2. pont | %s'
                  % (n, prov['szotar']))
        ind = ('Összesítő sor %d versre (a sor igehelye a blokk egy verse): a szótár-háló (BDB/Thayer) a motívum szavánál idézi a verset, de a versben '
               'a motívum szavai nem állnak (versszámozás-eltolás vagy más lexéma lehet); kézi ellenőrzés az értelmező menetben.' % n)
    sorok.append([MID, szabad, forras, 'nyitva', ind, karoli_szo, '', '', DATUM, 'elofordulas', '', '', '', ''])
with open(KI, 'w', encoding='utf-8', newline='\n') as f:
    f.write("# GENERÁLT: naplok/F239_U1_02_jelolt_sorok.py — jeloltek.tsv-séma, `nyitva`, lexémánként egy blokk-sor; --ir: hozzáfűzve az adat/jeloltek.tsv-hez\n")
    f.write('id\tigehely\tforras_kereses\tdontes\tindoklas\tkaroli_szo\tazonositas_modja\tmegbizhatosag\tdatum\tjelolt_tipus\tcel_id\tcel_igehely\tcel_alpont\tdontes_ref\n')
    for s in sorok:
        f.write('\t'.join(x.replace('\t', ' ') for x in s) + '\n')
print('blokksor:', len(sorok))
if IR:
    nyers = open(JT, 'rb').read()
    if not nyers.endswith(b'\n'):
        raise SystemExit('a jeloltek.tsv nem \\n-re végződik')
    kulcsok = {(r[0], r[1], r[9], r[10]) for r in jel}
    for s in sorok:
        if (s[0], s[1], s[9], s[10]) in kulcsok:
            raise SystemExit('kulcs-ütközés: %r' % (s[:2],))
    uj = ''.join('\t'.join(x.replace('\t', ' ') for x in s) + '\n' for s in sorok).encode('utf-8')
    ir = nyers + uj
    # ellenőrzés: a régi sorok változatlanok, az új sorok 14 oszlopúak
    regi = nyers.decode('utf-8').split('\n')
    ujj = ir.decode('utf-8').split('\n')
    assert ujj[:len(regi) - 1] == regi[:-1], 'régi sor eltér'
    assert all(len(x.split('\t')) == 14 for x in ujj[len(regi) - 1:-1]), 'oszlopszám'
    open(JT, 'wb').write(ir)
    chk = open(JT, 'rb').read().decode('utf-8').split('\n')
    assert chk[:len(regi) - 1] == regi[:-1] and len(chk) - 1 == len(regi) - 1 + len(sorok), 'írás után eltér'
    print('hozzáfűzve:', len(sorok))
