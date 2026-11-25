"""F239 U3 — a TEREMT-001 négy kiválasztott Nave-témájának és hat altételének magyar neve az adat/nave_tema_hu.tsv-be.
Bemenet: naplok/F239_U3_nave_tervezet.tsv (a kapuk és mankók kimenete: naplok/F239_U3_nave_manko.tsv; egy kézi
ítélet: a „The bottomless pit” a Jelenések ἄβυσσος-a, Károli „mélység”, ezért nem „verem”). Írás előtt összeveti a
régi sorokat: csak hozzáfűz, meglévő kulcsot nem ír felül."""
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UT = os.path.join(GY, 'adat', 'nave_tema_hu.tsv')
nyers = open(UT, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
regi = nyers.split(nl)
kulcsok = {tuple(s.split('\t')[:2]) for s in regi if s and not s.startswith('#')}
PROV = ('scope=manual | forras=a végrehajtó tervezete (glossza_lexikon_forditas.py nave: kapuk és mankók, '
        'naplok/F239_U3_nave_manko.tsv), F239 U3 | ts=2026-11-23')
uj = []
fej = None
for s in open(os.path.join(GY, 'naplok', 'F239_U3_nave_tervezet.tsv'), encoding='utf-8'):
    m = s.rstrip('\r\n').split('\t')
    if fej is None:
        fej = m; continue
    r = dict(zip(fej, m))
    if (r['tema_id'], r['cimke_en']) in kulcsok:
        sys.exit('HIBA: már van sor: %s %s' % (r['tema_id'], r['cimke_en']))
    h = hashlib.sha1(r['angol'].encode('utf-8')).hexdigest()
    uj.append('\t'.join([r['tema_id'], r['cimke_en'], r['angol'], r['magyar'], h, 'kezi', 'claude-opus-5-5',
                         '2026-11-23', PROV]))
if not nyers.endswith(nl):
    nyers += nl
uj_szoveg = nyers + nl.join(uj) + nl
assert uj_szoveg.startswith(nyers)
open(UT, 'w', encoding='utf-8', newline='').write(uj_szoveg)
print('hozzáfűzve: %d sor' % len(uj))
