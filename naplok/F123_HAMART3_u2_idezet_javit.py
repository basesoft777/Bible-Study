# -*- coding: utf-8 -*-
"""F123 HAMART-001 U2 utójavítás: a beépített jelölt-sorok indoklásának idézetei a Károli-vers szó szerinti részei
legyenek (`9_` v1, 5. szabály; E34). Csere a jeloltek.tsv HAMART-001 soraiban és a u2-szkript forrásában."""
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CSERE = [
    ('„tövis és bogáncs nő fel oltáraikon”, és a vers megnevezi Izrael bűnét is.',
     '„Tövis és bogácskóró növi be oltáraikat”, és a vers megnevezi „az Izráel vétkét” is.'),
    ('a föld (adamá) „pusztává lesz teljességéből, a benne lakók erőszaka miatt”. A vers együtt hozza az erőszak '
     '(chámász), a föld és a teljesség (a „megtelt” igének tövéből) szavát,',
     'Izrael földje „pusztaságra vetkőzzék … bőségéből minden lakói álnoksága miatt”. A héber vers együtt hozza az '
     'erőszak (chámász, a Károliban „álnokság”), a föld (adamá) és a teljesség (melóá, a „megtelt” igének tövéből; a '
     'Károliban „bőség”) szavát,'),
    ('a pusztító „nem rontja meg (sáchat) a föld (adamá) gyümölcsét”.',
     'a kártevő „nem veszti el földetek gyümölcsét”; a héberben a romlás igéje (sáchat) és a föld (adamá) áll.'),
    ('„kiirtok mindent a földnek színéről … embert és barmot, az ég madarait”.',
     '„mindent elvesztek e föld színéről”, „Elvesztek embert és barmot; elvesztem az ég madarait”.'),
    ('„semmi átok nem lesz többé” (κατανάθεμα, a kritérium szava nélkül).',
     '„semmi elátkozott nem lesz többé” (a görögben κατάθεμα, átok; a kritérium szava nélkül).'),
]


def csere(ut):
    s = io.open(ut, encoding='utf-8', newline='').read()
    for a, b in CSERE:
        n = s.count(a)
        assert n == 1, (ut, a[:40], n)
        s = s.replace(a, b)
    io.open(ut, 'w', encoding='utf-8', newline='').write(s)
    print(ut, 'OK')


csere('adat/jeloltek.tsv')
# a u2-szkript forrásában a sorok több sorra tördelve állnak: a szkript ezzel a javítással együtt érvényes
