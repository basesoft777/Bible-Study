"""F94.3 megfigyelés (N-F94f, manual): a különírt vonatkozó névmás gyakorisága a Károliban („a ki”, „a kit”, „a mely”,
„a melyet”, „a mit”, „a kiknek”). A tövezés alakonként megy, ezért a különírt „a” névelőként kap szótári alakot, holott a
vonatkozó névmás (aki, amely, ami) része; az amely-re (aki-ra, ami-re) keresve az „a” token nem jelenik meg. Javítás nincs.

Számol: az „a” (kis- vagy nagybetűs) után közvetlenül álló ki-, mely-, mi- névmásalakok; összevetésül az egybeírt
(aki-, amely-, ami-) alakok. A „mi” családnál a felső becslés a birtokos „a mi (Istenünk)” szerkezetet is tartalmazza;
az alsó becslés ezt kizárja (ha a következő szó -nk/-ünk/-unk végű vagy nagybetűs).
Használat: python eszkozok/szoto/kulonirt_vonatkozo.py"""
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
SZO = re.compile(r"[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+")
RAG = r'(t|k|ket|nek|knek|é|ben|kben|ből|kből|re|kre|ről|kről|hez|khez|től|ktől|vel|kkel|lyel|lyekkel|ért|kért|n|ken)?'
CSALAD = {'ki': re.compile(r'^ki' + RAG + '$'), 'mely': re.compile(r'^mely(ek)?' + RAG + '$'),
          'mi': re.compile(r'^mi' + RAG + '$')}
EGYBE = {'ki': re.compile(r'^aki' + RAG + '$'), 'mely': re.compile(r'^amely(ek)?' + RAG + '$'), 'mi': re.compile(r'^ami' + RAG + '$')}


def main():
    kulon, kulon_also, egybe, pelda = collections.Counter(), collections.Counter(), collections.Counter(), {}
    for s in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' not in s:
            continue
        ig, sz = s.split('\t', 1)
        t = SZO.findall(sz)
        for i, w in enumerate(t):
            wl = w.lower()
            for cs, rx in EGYBE.items():
                if rx.match(wl):
                    egybe[cs] += 1
            if wl != 'a' or i + 1 >= len(t):
                continue
            k = t[i + 1]
            for cs, rx in CSALAD.items():
                if rx.match(k):  # kisbetűs névmásalak
                    kulon[cs] += 1
                    pelda.setdefault(cs, f'{ig} „a {k}”')
                    kov = t[i + 2] if i + 2 < len(t) else ''
                    if not (cs == 'mi' and (kov[:1].isupper() or re.search(r'(nk|ünk|unk)$', kov))):
                        kulon_also[cs] += 1
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    print('| család | különírt („a” + névmás), felső | alsó (a „mi” birtokos nélkül) | egybeírt (aki-, amely-, ami-) | példa |')
    print('|---|---|---|---|---|')
    for cs in ('ki', 'mely', 'mi'):
        print(f'| {cs}- | {kulon[cs]} | {kulon_also[cs]} | {egybe[cs]} | {pelda.get(cs, "—")} |')
    print(f'| **összesen** | **{sum(kulon.values())}** | **{sum(kulon_also.values())}** | **{sum(egybe.values())}** | |')
    h = hashlib.sha256(open(KAROLI, 'rb').read()).hexdigest()[:12]
    print(f'\nscope=OT+NT-full | forras=konkordancia/Karoli_1908.tsv (sha256:{h}) + eszkozok/szoto/kulonirt_vonatkozo.py '
          f'(heurisztika, manual megfigyelés) | ts={ts}')


if __name__ == '__main__':
    main()
