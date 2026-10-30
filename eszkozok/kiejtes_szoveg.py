"""A kiejtés-szabály a lap szövegén (ISTENTISZT-001 arany lap, 2026-10-29).

Egy héber vagy görög szótári szó kiejtése szakaszonként (a `##`/`###` címek között) az első előfordulásnál kötelező, és
minden címsorban és táblázatfejben; ugyanabban a szakaszban nem ismétlendő; szó szerinti forrásidézetben (BDB, Thayer,
LSJ, TBESG szövege és fordítása) nem kell.

- `elemez(szoveg)`: soronként a hiányzó kiejtések (sor, szakasz, rész: generált/kézi, szó, ok, javasolt kiejtés).
- `potol(szoveg)`: a GENERÁLT részeken (GENERÁLT-KEZDET…VÉGE, GENERÁLT-RÉS … a rés proveniencia-soráig) a hiányzó
  kiejtést a szó után zárójelben pótolja. Görögül gépi magyaros átírás (`kiejtes.py`); héberül a jóváhagyott alak
  (`adat/kiejtes_kivetelek.tsv`), ennek híján (DT-F131y, 2026-10-30) a pontozott szó gépi kiejtése „…, gépi” jelöléssel
  (`heber_kiejtes.py`); pontozatlan, jóváhagyás nélküli szónál nem pótol (jelölt hiány). A kézi részt nem írja: azt a
  forrásban kell javítani.

Egy szó „kiejtéssel áll”, ha utána zárójelben latin betűs szöveg következik (a sorvégi szónál a következő sor elején is),
vagy táblázatsorban a következő cella latin betűs. A szó azonossága: a mellékjelek nélküli betűsor.
"""
import collections
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIVETELEK = os.path.join(GYOKER, 'adat', 'kiejtes_kivetelek.tsv')
TBESH = os.path.join(GYOKER, 'konkordancia', 'TBESH.txt')

HEBER = r'[א-תיִ-ﭏ][֐-׿יִ-ﭏ]*'
GOROG = r'[Ͱ-Ͽἀ-῿]+'
SZO = re.compile(r'%s(?:(?:[ ־]|\.\.\.|…)%s)*|%s(?: %s)*' % (HEBER, HEBER, GOROG, GOROG))
TOLDALEK = re.compile(r'(?:-[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+)?')
SZO_ELVALASZTO = re.compile(r'[ ־]|\.\.\.|…')
# a szó után (magyar raggal, „+” kapcsolattal is: „קָרָא-t (kárá)”, „קָרָא+שֵׁם (kárá + sém)”) zárójelben latin betű,
# vagy zárójelen belül vessző után („(ἐπικαλέομαι, epikaleomai)”)
KIEJTES_UTAN = re.compile(r'(?:-[^\s(]*|\+\S*)?(?:\**\s*\(\s*[*]?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűꞌʼ\'.]'
                          r'|\s*[–—]\s*[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű])|,\s*[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]')
LATIN = re.compile(r'[a-záéíóöőúüű]')
ELOTAG = 'בלוכמהש'


def alap(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn' and not c.isspace() and c not in '־־')


_jovahagyott = None


def jovahagyott_heber():
    """{mellékjel nélküli héber alak: kiejtés} a `kiejtes_kivetelek.tsv` héber soraiból; a STEP-átírás kulcsú sorok
    (`qa.ra`, `shem`) a TBESH lemmáján át."""
    global _jovahagyott
    if _jovahagyott is None:
        sorok = []
        with open(KIVETELEK, encoding='utf-8', newline='') as f:
            s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
        fej = s[0].split('\t')
        sorok = [dict(zip(fej, x.split('\t'))) for x in s[1:]]
        step = {r['alak']: r['kiejtes'] for r in sorok if r['nyelv'] == 'heber' and not re.search(HEBER, r['alak'])}
        d = {heber_kulcs(r['alak']): r['kiejtes'] for r in sorok if r['nyelv'] == 'heber' and re.search(HEBER, r['alak'])}
        if step and os.path.exists(TBESH):
            with open(TBESH, encoding='utf-8') as f:
                for sor in f:
                    c = sor.rstrip('\r\n').split('\t')
                    if len(c) > 4 and c[4] in step:
                        d.setdefault(heber_kulcs(c[3]), step[c[4]])
        _jovahagyott = d
    return _jovahagyott


def heber_kulcs(w):
    """A héber szó kulcsa: a kantillációs jelek és a meteg nélkül, a magánhangzójelekkel (a mássalhangzó-váz egyedül
    nem elég: שֻׁם ≠ שֵׁם)."""
    w = unicodedata.normalize('NFC', w)
    return ''.join(c for c in w if not ('֑' <= c <= '֯' or c in 'ֽ׀'))


def _massalhangzo(w):
    return ''.join(c for c in w if 'א' <= c <= 'ת')


ELOTAG_RE = re.compile('^([%s])[ְ-ׇּׁׂ]*' % ELOTAG)
ELOTAG_KIEJTES = {'ב': 'be', 'ל': 'le', 'ו': 've', 'כ': 'ke', 'מ': 'mi', 'ה': 'ha', 'ש': 'se'}


def heber_kiejtes(szo):
    """A jóváhagyott kiejtés (szókapcsolatnál szavanként, egyjegyű előtaggal is); ennek híján a pontozott szó gépi
    kiejtése (DT-F131y), ilyenkor az egész „…, gépi” jelölést kap; vagy None. Pontozatlan szónál a mássalhangzó-váz,
    ha az egyértelmű."""
    import heber_kiejtes as HK
    gepi = False
    jo = jovahagyott_heber()
    vaz = collections.defaultdict(set)
    for k, v in jo.items():
        vaz[_massalhangzo(k)].add(v)
    ki = []
    elo = ''
    szavak = SZO_ELVALASZTO.split(szo)
    for wi, w in enumerate(szavak):
        k = heber_kulcs(w)
        m0 = ELOTAG_RE.match(k)
        if m0 and m0.end() == len(k) and wi < len(szavak) - 1:  # önálló előtag (a בְּ előtag): gépi kiejtés
            elo = ELOTAG_KIEJTES[m0.group(1)]  # külön írt előtag (בְּ שֵׁם): a következő szóhoz tartozik
            continue
        if k in jo:
            ki.append(elo + jo[k])
            elo = ''
            continue
        m = ELOTAG_RE.match(k)
        if m and k[m.end():] in jo:
            ki.append(ELOTAG_KIEJTES[m.group(1)] + jo[k[m.end():]])
            continue
        if _massalhangzo(k) == k and len(vaz.get(k, ())) == 1:
            ki.append(next(iter(vaz[k])))
            continue
        g = HK.kiejt(w)
        if g:
            ki.append(elo + g)
            elo = ''
            gepi = True
            continue
        return None
    return ' '.join(ki)  # DT430 kiegészítés: jelölés nélkül


_gorog_tabla = None


def gorog_kiejtes(szo):
    """Szavanként: ha a szó TBESG-lemma (vagy SECE-címszó), a lemma kiejtése; különben a gépi magyaros átírás."""
    global _gorog_tabla
    import kiejtes as KJ
    import lexikon_general as LG  # hívásidőben: a generátor maga is ezt a modult hívja
    if _gorog_tabla is None:
        _gorog_tabla = (KJ.szabalyok_betolt(), KJ.kivetelek_betolt(nyelv='gorog'))
    idx = LG.lemma_strong_index()
    ki = []
    for w in szo.split():
        st = [x for x in idx.get(unicodedata.normalize('NFC', w), []) if x.startswith('G')]
        lk = LG.lemma_kiejtes(st[0]) if len(st) == 1 else None
        if lk and unicodedata.normalize('NFC', lk[0]) != unicodedata.normalize('NFC', w):
            lk = None  # a kiírt alak nem a lemma (ἐπικαλέομαι ↔ ἐπικαλέω): a kiírt alak gépi kiejtése
        ki.append(lk[1] if lk and lk[1] else KJ.atir(LG.gepi_atiras(w), *_gorog_tabla))
    return ' '.join(ki)


def kiejtes(szo):
    return heber_kiejtes(szo) if re.match(HEBER, szo) else gorog_kiejtes(szo)


def forras_idezet(sor):
    t = sor.lstrip()
    return (t.startswith('>') or t.startswith('**🇭🇺**') or t.startswith('- `') or t.startswith('**A szócikk feje')
            or t.startswith('<!--') or t.startswith('<summary'))


def _sor_reszek(sorok):
    """[(generált-e, forrásidézet-e, szakasz)] soronként."""
    ki = []
    blokk = res = False
    details = 0
    szakasz = '(eleje)'
    for sor in sorok:
        if sor.startswith('## ') or sor.startswith('### '):
            szakasz = sor.lstrip('# ').strip()
            res = False
        if 'GENERÁLT-KEZDET' in sor:
            blokk = True
        if 'GENERÁLT-RÉS' in sor:
            res = True
        details += sor.count('<details>') - sor.count('</details>')
        ki.append((blokk or res, details > 0 or forras_idezet(sor), szakasz))
        if 'GENERÁLT-VÉGE' in sor:
            blokk = False
        if res and sor.startswith('*Proveniencia: `scope=id:'):
            res = False
    return ki


def _van_kiejtes(sorok, i, m):
    sor = sorok[i]
    utana = sor[m.end():]
    if not utana.strip() and i + 1 < len(sorok):
        utana = sorok[i + 1]
    if KIEJTES_UTAN.match(utana):
        return True
    if sor.startswith('|'):
        cellak = sor.split('|')
        poz = sor[:m.start()].count('|')
        fej = next((sorok[k] for k in range(i, -1, -1) if sorok[k].startswith('|')
                    and k + 1 < len(sorok) and sorok[k + 1].startswith('|---')), '')
        fejcellak = fej.split('|')
        if poz + 1 >= len(fejcellak) or fejcellak[poz + 1].strip() != 'Kiejtés':
            return False
        kov = cellak[poz + 1].strip() if poz + 1 < len(cellak) else ''
        return bool(LATIN.search(kov)) and not SZO.search(kov) and kov not in ('—', '-')
    return False


def _bejar(sorok, potolni):
    reszek = _sor_reszek(sorok)
    latott = collections.defaultdict(set)
    hiany = []
    for i, sor in enumerate(sorok):
        gen, idezet, szakasz = reszek[i]
        if idezet:
            continue
        cim = sor.startswith('#')
        tablafej = sor.startswith('|') and i + 1 < len(sorok) and sorok[i + 1].startswith('|---')
        uj, poz = [], 0
        for m in SZO.finditer(sor):
            szo = m.group(0)
            kulcs = heber_kulcs(szo) if re.match(HEBER, szo) else alap(szo)
            kell = cim or tablafej or kulcs not in latott[szakasz]
            latott[szakasz].add(kulcs)
            if re.match(HEBER, szo):
                # a szókapcsolat kiejtése a benne álló szavakét is jelenti (a szakaszban nem ismétlendő)
                latott[szakasz].update(heber_kulcs(w) for w in SZO_ELVALASZTO.split(szo))
            if not kell or _van_kiejtes(sorok, i, m):
                continue
            jav = kiejtes(szo)
            if potolni and gen and jav:
                vege = m.end() + len(TOLDALEK.match(sor, m.end()).group(0))
                uj.append(sor[poz:vege] + ' (%s)' % jav)
                poz = vege
                continue
            hiany.append((i + 1, szakasz, 'generált' if gen else 'kézi', szo,
                          'cím' if cim else 'táblafej' if tablafej else 'első előfordulás', jav))
        if uj:
            sorok[i] = ''.join(uj) + sor[poz:]
    return hiany


def elemez(szoveg):
    return _bejar(szoveg.split('\n'), False)


def potol(szoveg):
    """(pótolt szöveg, a megmaradt hiányok listája)."""
    sorok = szoveg.split('\n')
    hiany = _bejar(sorok, True)
    return '\n'.join(sorok), hiany
