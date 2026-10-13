"""F94.1 megfigyelés (N-F94d, manual): a hátravetett, külön írt igekötő gyakorisága a Károliban
(„vettettek el”, „ragadja el”, „jelenté … meg”, „hajtott ki”, „rejted el”). Javítás nincs; a tövezés alakonként megy,
ezért az ilyen előfordulás az igekötős szótári alakra keresve nem jön elő, az alapigére igen.

Két szám igekötőnként:
  - **alsó becslés:** a külön álló igekötő után írásjel vagy versvég áll (biztosan hátravetett: „rejted el.”);
  - **felső becslés:** minden külön álló igekötő-token (benne az előre vetett „meg nem”, a *ki* névmás, a *meg* kötőszó is).
Használat: python eszkozok/szoto/hatravetett_igekoto.py"""
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
IGEKOTO = ['meg', 'el', 'ki', 'be', 'le', 'fel', 'föl', 'át', 'vissza', 'össze', 'rá', 'reá', 'oda', 'elő', 'alá',
           'hozzá', 'szét', 'széjjel', 'utána', 'végig']
TOKEN = re.compile(r"[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+|[.,;:!?]")


def main():
    also, felso, pelda = collections.Counter(), collections.Counter(), {}
    versek = 0
    for sor in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' not in sor:
            continue
        versek += 1
        ih, szoveg = sor.split('\t', 1)
        t = TOKEN.findall(szoveg)
        for i, w in enumerate(t):
            if w in IGEKOTO:
                felso[w] += 1
                kov = t[i + 1] if i + 1 < len(t) else ''
                if (kov == '' or kov in '.,;:!?') and i > 0 and t[i - 1] not in '.,;:!?':
                    also[w] += 1
                    pelda.setdefault(w, f'{ih} „{t[i - 1]} {w}”')
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    print('| igekötő | alsó becslés (utána írásjel / versvég) | felső becslés (minden külön álló token) | példa |')
    print('|---|---|---|---|')
    for w in sorted(IGEKOTO, key=lambda x: -also[x]):
        if felso[w]:
            print(f'| {w} | {also[w]} | {felso[w]} | {pelda.get(w, "—")} |')
    print(f'| **összesen** | **{sum(also.values())}** | **{sum(felso.values())}** | |')
    h = hashlib.sha256(open(KAROLI, 'rb').read()).hexdigest()[:12]
    print(f'\nscope=OT+NT-full ({versek} Károli-vers) | forras=konkordancia/Karoli_1908.tsv (sha256:{h}) + '
          f'eszkozok/szoto/hatravetett_igekoto.py (heurisztika, manual megfigyelés) | ts={ts}')


if __name__ == '__main__':
    main()
