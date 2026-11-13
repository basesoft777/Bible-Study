"""F194.4 (K68; DT595, DT684): az ISTENTISZT-001 kiválasztott Nave-témáinak indoka a 2. kiadás határán, versekkel.

A döntések (DT424: „Csak a 8 funkció”) nem változnak, csak az `indok` mező: a 20 előfordulás-versen (DT-F194a után) a
jelöltképzés (`eszkozok/szerep_nave.jeloltek`, küszöb: 2 vers és 1%) öt kiválasztott témát ad; ezek indoka a HAMART-001
mintájára a motívumverseket nevezi. A három kiválasztott, de már nem jelölt téma indoka kimondja, miért nem áll a
blokkban (a jelöltképzés számaival). Írás előtt: csak az `indok` mező, csak ez a 8 sor változik; a számok a
`szerep_nave.jeloltek` mai futásából ellenőrizve. Futtatás: python naplok/F194_nave_indok.py [--ir]
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import szerep_nave as SN  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
UJ = {   # tema_id -> (az új indok, a várt motívumversek a jelöltképzésben, jelölt-e)
    'NAVE-4150': ('funkció-téma: a Kármel-próba (1Kir 18:24–26) és a pünkösdi beszéd (ApCsel 2:21) mint ébredés',
                  ['1Kir 18:24', '1Kir 18:25', '1Kir 18:26', 'ApCsel 2:21'], True),
    'NAVE-3621': ('funkció-téma: a hála és a fogadalom kötelezettsége a 116. zsoltárban (Zsolt 116:13, 116:17)',
                  ['Zsolt 116:13', 'Zsolt 116:17'], True),
    'NAVE-2458': ('funkció-téma: a bálványisten nevének hívása, a kontraszt (1Kir 18:25–26)',
                  ['1Kir 18:25', '1Kir 18:26'], True),
    'NAVE-2034': ('funkció-téma: Isten dicsősége a név kimondásával (2Móz 33:19, 34:5)',
                  ['2Móz 33:19', '2Móz 34:5'], True),
    'NAVE-4301': ('funkció-téma: a megmenekülés ígérete a segítségül hívóknak (ApCsel 2:21, Róm 10:13)',
                  ['ApCsel 2:21', 'Róm 10:13'], True),
    'NAVE-4874': ('funkció-téma (Zsolt 116:4, 116:13); a 2. kiadás 20 versén a téma 261 verséből 2 a motívumé, '
                  'a jelöltküszöb (1%) alatt, ezért a blokkban nem áll', ['Zsolt 116:4', 'Zsolt 116:13'], False),
    'NAVE-3790': ('funkció-téma (Róm 10:13); a 2. kiadás 20 versén egy motívumvers, a jelöltküszöb (2 vers) alatt, '
                  'ezért a blokkban nem áll', ['Róm 10:13'], False),
    'NAVE-3936': ('funkció-téma: a segítségül hívás tagadása; a helyei (Jer 10:25, Zsolt 79:6) névmási raggal állnak, '
                  'a motívumon kívül, ezért a 2. kiadás 20 versén nem jelölt, és a blokkban nem áll', [], False),
}


def main():
    ir = '--ir' in sys.argv
    sorai = [r for r in SN._sorok(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')) if r['id'] == ID]
    mind = {j['tema_id']: j for j in SN.jeloltek(sorai, tiltott=set(), min_vers=1, min_arany=0)}
    jelolt = {j['tema_id'] for j in SN.jeloltek(sorai, tiltott=set())}
    hibak = []
    for tid, (_i, vers, jel) in UJ.items():
        if mind.get(tid, {}).get('motivumversek', []) != vers:
            hibak.append('%s: a motívumversek mások: %s' % (tid, mind.get(tid, {}).get('motivumversek')))
        if (tid in jelolt) != jel:
            hibak.append('%s: a jelölt-állapot más' % tid)
    ut = os.path.join(GYOKER, 'adat', 'tematikus_temak.tsv')
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = next(s for s in sorok if s and not s.startswith('#')).rstrip('\r').split('\t')
    valt = 0
    for i, s in enumerate(sorok):
        m = s.rstrip('\r').split('\t')
        if len(m) != len(fej):
            continue
        d = dict(zip(fej, m))
        if d['id'] == ID and d['tema_id'] in UJ:
            if d['dontes'] != 'kivalasztott':
                hibak.append('%s: nem kiválasztott' % d['tema_id'])
            d['indok'] = UJ[d['tema_id']][0]
            sorok[i] = '\t'.join(d[k] for k in fej) + ('\r' if s.endswith('\r') else '')
            valt += 1
    if valt != len(UJ):
        hibak.append('%d sor helyett %d' % (len(UJ), valt))
    for h in hibak:
        print('HIBA:', h)
    if hibak:
        raise SystemExit(1)
    print('tematikus_temak.tsv: %d indok; a blokk témái: %s' % (valt, ', '.join(sorted(jelolt & set(UJ)))))
    if ir:
        with open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(sorok))
        print('írva.')


if __name__ == '__main__':
    main()
