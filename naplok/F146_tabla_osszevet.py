"""F146.2: a KK4 próbakimenetének sorról sorra összevetése a táblával (a 3.2 halmaz-őr, független újraolvasással).

Elfogadás: (1) a két fájl sorszáma egyezik, és az eltérő sorok pontosan a Jóel 2:28–3:21 26 adatsora és az új
`# F146 javítás` fejléc-jegyzet (a többi sor bájtra azonos, ugyanazon a helyen — kivéve a jegyzet beszúrása miatti eltolást);
(2) a 26 sor értéke: igehely_kjv = Károli-szám, igehely_mt = a mért MT-vers, KEZI, macula_mt_f146.
Csak olvas. Futtatás: python naplok/F146_tabla_osszevet.py <régi tábla> <új tábla>
TSV split('\\t'), a csv modul nélkül.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def olvas(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def main():
    regi, uj = olvas(sys.argv[1]), olvas(sys.argv[2])
    jo = {'Jóel 2:%d' % v: ('2:%d' % v, '3:%d' % (v - 27)) for v in range(28, 33)}
    jo.update({'Jóel 3:%d' % v: ('3:%d' % v, '4:%d' % v) for v in range(1, 22)})
    uj_jegyzet = [s for s in uj if s.startswith('# F146 javítás')]
    assert len(uj_jegyzet) == 1 and not any(s.startswith('# F146 javítás') for s in regi)
    u2 = [s for s in uj if not s.startswith('# F146 javítás')]
    assert len(u2) == len(regi), (len(u2), len(regi))
    valt = []
    for i, (a, b) in enumerate(zip(regi, u2)):
        if a != b:
            ka, kb = a.split('\t')[0], b.split('\t')[0]
            assert ka == kb, 'a sorrend eltér a %d. sorban: %r / %r' % (i + 1, ka, kb)
            valt.append(kb)
            p = b.split('\t')
            assert kb in jo, 'halmazon kívüli változás: %s' % kb
            assert p[1:5] == [jo[kb][0], jo[kb][1], 'KEZI', 'macula_mt_f146'], b
    assert sorted(valt) == sorted(jo), sorted(set(jo) - set(valt))
    print('összevetés: %d / %d sor; eltér: %d adatsor (mind a Jóel 26 sora, a várt értékkel) + 1 új fejléc-jegyzet; minden más sor bájtra azonos'
          % (len(uj), len(regi), len(valt)))


if __name__ == '__main__':
    main()
