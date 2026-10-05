"""F58 M1: a Macula-szavak nyelvjelölője (lang="H"/"A") a Macula lowfat XML-ből.

A Macula_heber_*.tsv nem hordozza a nyelvet, az OSHB-kód pedig nyelvfüggő
(l. naplok/MORF_KULCS_M0.md). Az XML-fájlokat egyenként tölti le (streaming,
lemezre nem ír), és csak az arámi (lang="A") szavakat menti:
adat/morf_nyelv_aramai.tsv. Ami nincs benne, az a Macula szerint héber.
Futtatás: python eszkozok/morf_nyelv_kivonat.py
"""
import sys
import re
import json
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REV = '47db250bd55d0d8577f2a94fba114ef16c35b23c'
REPO = 'Clear-Bible/macula-hebrew'
KIMENET = 'adat/morf_nyelv_aramai.tsv'
TS = '2026-10-05'
W_RE = re.compile(r'<w\s[^>]*?>', re.S)


def olvas(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def attr(tag, nev):
    m = re.search(r'\s' + re.escape(nev) + r'="([^"]*)"', tag)
    return m.group(1) if m else ''


def main():
    lista = json.loads(olvas(f'https://api.github.com/repos/{REPO}/contents/WLC/lowfat?ref={REV}'))
    fajlok = sorted(x['name'] for x in lista if x['name'].endswith('-lowfat.xml'))
    sor = []
    nyelvek = {}
    osszes = 0
    for nev in fajlok:
        t = olvas(f'https://raw.githubusercontent.com/{REPO}/{REV}/WLC/lowfat/{nev}').decode('utf-8')
        for tag in W_RE.findall(t):
            osszes += 1
            lang = attr(tag, 'lang')
            nyelvek[lang] = nyelvek.get(lang, 0) + 1
            if lang == 'A':
                sor.append((attr(tag, 'xml:id'), attr(tag, 'ref'), attr(tag, 'morph')))
    sor.sort()
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/morf_nyelv_kivonat.py — kézzel nem szerkesztendő.\n')
        f.write(f'# proveniencia: scope=WLC/lowfat/*.xml `w@lang="A"` szavai ({len(fajlok)} fájl, {osszes} w-elem) | forras=https://github.com/{REPO}@commit {REV} | licenc=CC BY 4.0 (Biblica, Inc) | ts={TS}\n')
        f.write('# nyelvek (w@lang értékei, darab): ' + ', '.join(f'{k or "(üres)"}={v}' for k, v in sorted(nyelvek.items())) + '\n')
        f.write('xml_id\tref\tmorf\tnyelv\n')
        for x in sor:
            f.write('\t'.join(x) + '\tA\n')
    print(len(fajlok), osszes, nyelvek, len(sor))


if __name__ == '__main__':
    main()
