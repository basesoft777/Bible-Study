"""A keresés (#76 M3, M0 3.6): a bemenet értelmezése és normalizálása, a találatok összegyűjtése, az illesztés és a lapozás.

Nem függ a Flasktól, és SQL-t nem tartalmaz (az SQL a `lekerdezesek.py`-ban áll, paraméterezve; N-F76c). Négy ág:

- **Strong-szám** (`strong=H0216`, legfeljebb három, szóközzel vagy `+`-szal: a versek, amelyekben mind előfordul): `token_strong`.
- **Magyar szó** (`szo=…`, `mod=`): `pontos` = a szóalak (kis/nagybetű-független, a `szo_kis` szabálya); `szoto` (az alap, DT146/2) =
  a pontos alak ∪ a szótári alakhoz tartozó Károli-alakok (`szotari_kereso`, a kötőjeles alakok darabjaival együtt); `szoto_strong`
  ((c) mód, DT146/2 kapcsoló) = a `szoto` ∪ a találatok nem nyelvtani Strong-számaival párosított minden magyar szó (F95 M0 6. szakasz).
- **Magyar frázis** (`frazis=…`, 2–4 szó): egymást követő szótokenek egy Károli-versen belül (`token_karoli`, DT146/3).
- **Héber frázis** (`heber=…`, 1–4 szó): a `token_karoli` héber oldalának mássalhangzós alakja (`szo_kis`), az előtag-tokenek
  (ו ה ב כ ל מ ש, a TAHOT külön tokenként tartja őket) toleranciájával: a beírt szó egyezhet 1–4 egymást követő token összefűzésével.

A `q=` mező a típust a bemenetből ismeri fel (igehely → ugrás; Strong-szám; héber betű → héber frázis; egy magyar szó → szó;
több → frázis). A magyar szó- és frázis-keresés a Károli–Strong szótokeneken fut: a 9 párosítatlan újszövetségi könyvben nincs
szótoken, ott nem talál (a lap ezt kiírja; F95 M0 5. szakasz).
"""
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

from markupsafe import Markup, escape

import lekerdezesek as q

OLDALMERET = 50
MAX_HOSSZ = 100
TIPUSOK = ('strong', 'szo', 'frazis', 'heber')
TIPUS_NEVEK = {'auto': 'automatikus', 'strong': 'Strong-szám', 'szo': 'magyar szó', 'frazis': 'magyar frázis (2–4 szó)', 'heber': 'héber frázis'}
MODOK = ('pontos', 'szoto', 'szoto_strong')
ALAP_MOD = 'szoto'                       # DT146/2: az alap az alak ∪ szótári alak
MOD_NEVEK = {'pontos': 'csak a pontos alak', 'szoto': 'pontos alak + szótári alak (alap)', 'szoto_strong': 'szótári alak + Strong-ág ((c) mód)'}
HEBER_BETU = re.compile('[א-ת]')
GOROG_BETU = re.compile('[Ͱ-Ͽἀ-῿]')
ELOTAG = set('והבכלמש')                  # a TAHOT külön tokenként tartott előtagjai (mássalhangzós alak)
MAX_ELOTAG = 3
STRONG_LISTA_MAX = 5000                  # a magyar alak párosított Strong-listája e fölött nem készül (a leggyakoribb szavaknál 50+ ms)


class KeresesHiba(Exception):
    """Érvénytelen keresési bemenet; az üzenet a felhasználónak szól."""


def szo_kis(s):
    """A `token_karoli.szo_kis` / `token_par.hu_szo_kis` szabálya (az építő `sqlite_epit.szo_kis`-ával azonos; a teszt összeveti):
    NFC, kisbetű, minden nem betű/számjegy karakter (írásjel, kötőjel, aposztróf, héber pontozás és ékezet) nélkül."""
    s = unicodedata.normalize('NFC', s or '').lower()
    return re.sub(r'[\W_]+', '', s)


def kereso_alak(s):
    """A `szotari_kereso.keresoalak` szabálya (F95, SEMA): NFC + kisbetű; a kötőjelet megtartja (nem `szo_kis`)."""
    return unicodedata.normalize('NFC', (s or '').strip()).lower()


def hu_darabok(s):
    """A magyar bemenet szótokenjei: szóköz és kötőjel mentén bontva (a `token_karoli` a kötőjeles alakot szétvágja), `szo_kis`-sel."""
    return [k for k in (szo_kis(x) for x in re.split(r'[\s\-‐‑–]+', s or '')) if k]


def heber_szavak(s):
    """A héber bemenet szavai (szóköz mentén), a `szo_kis` szabályával: a pontozás és a maqaf kiesik."""
    return [k for k in (szo_kis(x) for x in (s or '').split()) if k]


@dataclass
class Kerdes:
    tipus: str
    szoveg: str
    szavak: list
    mod: str = ALAP_MOD
    tol: int = -1


def _int(v, alap):
    try:
        return int(v)
    except (TypeError, ValueError):
        return alap


def ertelmez(args, kozos=None):
    """`args`: a kérés paraméterei (dict-szerű, `.get`). Visszaad: Kerdes, vagy ('ugras', út), vagy None (üres űrlap).
    Hibás bemenetre KeresesHiba (a felhasználónak szóló üzenettel)."""
    tol = max(-1, _int(args.get('tol'), -1))
    mod = args.get('mod') if args.get('mod') in MODOK else ALAP_MOD
    tipus, szoveg = None, None
    for t in TIPUSOK:                                      # az állandó, típusos alak: ?strong= ?szo= ?frazis= ?heber=
        if args.get(t):
            tipus, szoveg = t, args.get(t)
            break
    if tipus is None:
        szoveg = args.get('q') or ''
        tipus = args.get('tipus') if args.get('tipus') in TIPUSOK else 'auto'
    szoveg = (szoveg or '').strip()
    if not szoveg:
        return None
    if len(szoveg) > MAX_HOSSZ:
        raise KeresesHiba('A keresett kifejezés legfeljebb %d karakter lehet.' % MAX_HOSSZ)
    if re.search(r'[\x00-\x1f\x7f]', szoveg):
        raise KeresesHiba('A keresett kifejezésben vezérlőkarakter áll.')
    if tipus == 'auto':
        if kozos is not None:
            import oldalak                                     # körkörös import elkerülése
            cel = oldalak.ugras_celpont(kozos, szoveg)
            if cel and not cel.startswith('/szo/'):
                return ('ugras', cel)
        tipus = auto_tipus(szoveg)
    return Kerdes(tipus, szoveg, normalizal(tipus, szoveg), mod, tol)


def auto_tipus(szoveg):
    if all(q.hnorm(x) for x in re.split(r'[\s+]+', szoveg.strip()) if x):
        return 'strong'
    if HEBER_BETU.search(szoveg):
        return 'heber'
    if GOROG_BETU.search(szoveg):
        raise KeresesHiba('Görög szövegre ez a kiadás nem keres; adj meg Strong-számot (pl. G3056).')
    return 'szo' if len(szoveg.split()) == 1 else 'frazis'


def normalizal(tipus, szoveg):
    if tipus == 'strong':
        lista = [x for x in re.split(r'[\s+,]+', szoveg) if x]
        ki = [q.hnorm(x) for x in lista]
        if not ki or None in ki:
            raise KeresesHiba('Érvénytelen Strong-szám. Alakja: H0216 vagy G3056 (legfeljebb három, szóközzel elválasztva).')
        ki = list(dict.fromkeys(ki))
        if len(ki) > 3:
            raise KeresesHiba('Legfeljebb három Strong-szám adható meg egyszerre.')
        return ki
    if tipus == 'heber':
        if not HEBER_BETU.search(szoveg):
            raise KeresesHiba('A héber frázis héber betűkkel adható meg (pontozással vagy anélkül).')
        ki = heber_szavak(szoveg)
        if not 1 <= len(ki) <= 4:
            raise KeresesHiba('A héber frázis 1–4 szó.')
        return ki
    ki = hu_darabok(szoveg)
    if not ki:
        raise KeresesHiba('A keresett kifejezésben nincs betű vagy számjegy.')
    if tipus == 'szo':
        if len(szoveg.split()) != 1:
            raise KeresesHiba('Magyar szóra egy szót adj meg; több szóra a frázis-keresés való.')
        if len(ki) > 4:
            raise KeresesHiba('A kötőjeles szó legfeljebb négy tagú lehet.')
        return ki
    if not 2 <= len(ki) <= 4:
        raise KeresesHiba('A magyar frázis 2–4 szó (a kötőjel is szóhatár).')
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# a találatok
# ---------------------------------------------------------------------------------------------------------------------
@dataclass
class Talalatok:
    """A teljes találathalmaz (lapozás előtt)."""
    versek: list                                    # [(sorrend, igehely)] sorrend szerint, ismétlés nélkül
    hu: set = field(default_factory=set)            # {(igehely, hu_sorszam)} a kiemelendő magyar szavak (a lap versein csoportosítva, lap_sorai)
    er: dict = field(default_factory=dict)          # {igehely: [ [er_sorszam, ...] szócsoportonként ]} (héber frázis)
    elofordulas: int = 0
    info: dict = field(default_factory=dict)
    figyelmeztetes: list = field(default_factory=list)


def _rendez(igehelyek, sorrend):
    """{igehely} -> [(sorrend, igehely)] a Biblia sorrendjében (a `vers` táblában nem szereplő igehely kimarad)."""
    return sorted((sorrend[ig], ig) for ig in igehelyek if ig in sorrend)


def strong_kereses(con, k, sorrend, par_lathato=True):
    halmaz, db = None, 0
    alakok, ismeretlen = {}, []
    for s in k.szavak:
        if not q.strong_van(con, s):
            ismeretlen.append(s)
        ig_set = q.kereses_strong_versek(con, s)
        db += q.kereses_strong_db(con, s)
        halmaz = ig_set if halmaz is None else (halmaz & ig_set)
        alakok[s] = q.kereses_strong_alakok(con, s) if par_lathato else []          # a párosítás adata csak látható `vers.par` mellett
    t = Talalatok(_rendez(halmaz or set(), sorrend), elofordulas=db if len(k.szavak) == 1 else 0)
    t.info['strong_alakok'] = alakok
    if ismeretlen:
        t.figyelmeztetes.append('Ismeretlen Strong-szám: %s.' % ', '.join(ismeretlen))
    return t


def szo_kereses(con, k, sorrend, strong_ag=True):
    """A magyar szó három módja. `strong_ag`: a (c) mód engedélyezett-e (a `vers.par` láthatósága).
    A pontos ág csak (igehely, sorszám) párt olvas (fedő index, `ix_token_karoli_2`); a talált alakokat a szótári ág adja."""
    darabok = k.szavak
    if len(darabok) == 1:
        pontos = set(q.kereses_hu_szo_kis(con, darabok[0]))
    else:                                                  # kötőjeles bemenet: a darabok egymást követő tokenként (pontos alak)
        pontos = {(ig, elso + i) for ig, elso in q.kereses_frazis(con, darabok, 'hu') for i in range(len(darabok))}
    tokenek = set(pontos)
    t = Talalatok([])
    t.info['mod'] = k.mod
    t.info['pontos_db'] = len(pontos) // len(darabok)
    alakok, db = [], Counter()
    if k.mod in ('szoto', 'szoto_strong'):
        ka = kereso_alak(k.szoveg)
        par = q.szotari_kereso(con, ka)
        alakok = [a for a, _ in par]
        t.info['kereso_alak'] = ka
        t.info['kereso_mezok'] = sorted({m for _, mz in par for m in (mz or '').split(',') if m})
        if alakok:
            for ig, sz, szo in q.kereses_hu_alakok(con, alakok):
                tokenek.add((ig, sz))
                db[szo] += 1
            kotojeles = [a for a in alakok if '-' in a]
            if kotojeles:
                for ig, sz, alak in q.kereses_kotojeles(con, kotojeles):
                    if (ig, sz) not in tokenek:
                        tokenek.add((ig, sz))
                        db[alak] += 1
        # javaslat: a beírt alak szótári alakja (ha más), hogy a tőre is lehessen keresni
        for probalt in dict.fromkeys((k.szoveg, k.szoveg.lower(), k.szoveg[:1].upper() + k.szoveg[1:].lower())):
            sa = q.szotari_alak_alakra(con, probalt)
            if sa and kereso_alak(sa[0]) != ka:
                t.info['javaslat'] = sa[0]
                break
    # mit talált és hogyan (DT146/2): a szótári ág alakjai; a pontos alak külön szám
    t.info['alakok'] = sorted(db.items(), key=lambda x: (-x[1], x[0]))
    t.info['szotari_alakok_szama'] = len(alakok)
    t.info['szoto_db'] = len(tokenek) - len(pontos)
    if k.mod == 'szoto_strong':
        if not strong_ag:
            t.figyelmeztetes.append('A Strong-ággal bővített mód ezen a hozzáférési szinten nem érhető el (a párosítás blokkja zárt); a szótári alakos keresés eredménye látszik.')
        else:
            strongok = q.kereses_tokenek_strongjai(con, list(tokenek))
            t.info['strong_ag'] = strongok.most_common()
            elotte = len(tokenek)
            if strongok:
                tokenek.update(q.kereses_par_strong_tokenek(con, list(strongok)))
            t.info['strong_ag_db'] = len(tokenek) - elotte
    t.hu = tokenek
    t.versek = _rendez({ig for ig, _ in tokenek}, sorrend)
    t.elofordulas = len(tokenek) // (len(darabok) if (len(darabok) > 1 and k.mod == 'pontos') else 1)
    if len(darabok) == 1 and strong_ag:
        if len(pontos) <= STRONG_LISTA_MAX:
            t.info['strongok'] = q.kereses_szo_strongjai(con, darabok[0])
        else:
            t.figyelmeztetes.append('A párosított Strong-számok listája %d előfordulás fölött nem készül (itt %d); a szó-lapokon és a Strong-keresésben látszik.' % (
                STRONG_LISTA_MAX, len(pontos)))
    return t


def frazis_kereses(con, k, sorrend):
    t = Talalatok([])
    sorok = q.kereses_frazis(con, k.szavak, 'hu')
    t.hu = {(ig, elso + i) for ig, elso in sorok for i in range(len(k.szavak))}
    t.versek = _rendez({ig for ig, _ in sorok}, sorrend)
    t.elofordulas = len(sorok)
    return t


def heber_magok(szo):
    """A beírt héber szó lehetséges „magjai”: a szó maga, és az elöl leválasztható előtag-betűk (legfeljebb három) utáni rész.
    A TAHOT az előtagot külön tokenként tartja, így a szó utolsó tokenje a mag."""
    ki = [szo]
    for i in range(1, min(MAX_ELOTAG, len(szo) - 1) + 1):
        if all(c in ELOTAG for c in szo[:i]):
            ki.append(szo[i:])
    return list(dict.fromkeys(ki))


def heber_illeszt(tokenek, szavak):
    """`tokenek`: [(sorszam, szo_kis, szo)] egy vers héber tokenjei sorszám szerint; `szavak`: a beírt szavak (`szo_kis`).
    Minden beírt szó 1–4 egymást követő token összefűzésével egyezik (az előtagok külön tokenek). Visszaad: a találatok listája,
    mindegyik a szócsoportok sorszám-listája ([[sorszam, ...], ...]). A vers határán nem lép át (versenként hívják)."""
    ki = []
    n = len(tokenek)
    for i in range(n):
        if not tokenek[i][1]:
            continue
        pos, csoportok = i, []
        for w in szavak:
            acc, talalt = '', False
            for j in range(pos, min(pos + 4, n)):
                acc += tokenek[j][1]
                if acc == w and tokenek[j][1]:
                    csoportok.append([tokenek[x][0] for x in range(pos, j + 1)])
                    pos, talalt = j + 1, True
                    break
                if not w.startswith(acc):
                    break
            if not talalt:
                break
        else:
            ki.append(csoportok)
    return ki


def heber_kereses(con, k, sorrend):
    """A jelölt versek a beírt szavak versének metszete (a szavak magjai szerint, a legritkábbtól); bennük a `heber_illeszt` dönt.
    Egyetlen, előtaggal nem bontható szónál a találat maga a token (közvetlen, indexes út)."""
    t = Talalatok([])
    magok = [heber_magok(w) for w in k.szavak]
    if len(k.szavak) == 1 and len(magok[0]) == 1:
        for ig, sz in q.kereses_er_tokenek(con, k.szavak[0]):
            t.er.setdefault(ig, []).append([[sz]])
            t.elofordulas += 1
        t.versek = _rendez(t.er, sorrend)
        t.info['jelolt_versek'] = len(t.er)
        return t
    szamok = sorted((q.kereses_er_db(con, m), i) for i, m in enumerate(magok))
    jeloltek = None
    for db, i in szamok:
        if not db:
            jeloltek = set()
            break
        v = q.kereses_er_versek(con, magok[i])
        jeloltek = v if jeloltek is None else (jeloltek & v)
        if not jeloltek:
            break
    jeloltek = sorted(jeloltek or ())
    t.info['jelolt_versek'] = len(jeloltek)
    tokenek = q.er_tokenek_versekre(con, jeloltek)
    for ig, lista in tokenek.items():
        m = heber_illeszt(lista, k.szavak)
        if m:
            t.er[ig] = m
            t.elofordulas += len(m)
    t.versek = _rendez(t.er, sorrend)
    return t


def keres(con, k, sorrend, par_lathato=True):
    """A teljes találathalmaz. `sorrend`: {igehely: sorrend} (`lekerdezesek.vers_sorrendek`, egyszer betöltve); `par_lathato`: a `vers.par`
    blokk (a Károli–Strong párosítás) látszik-e a kérés szintjén."""
    if k.tipus == 'strong':
        return strong_kereses(con, k, sorrend, par_lathato)
    if k.tipus == 'szo':
        return szo_kereses(con, k, sorrend, strong_ag=par_lathato)
    if k.tipus == 'frazis':
        return frazis_kereses(con, k, sorrend)
    if k.tipus == 'heber':
        return heber_kereses(con, k, sorrend)
    raise ValueError(k.tipus)


# ---------------------------------------------------------------------------------------------------------------------
# lapozás és megjelenítés
# ---------------------------------------------------------------------------------------------------------------------
def lap(t, tol, meret=OLDALMERET):
    """A kulcsos lapozás (M0 3.6): a `tol` sorrend UTÁNI első `meret` vers; (lap, következő tol vagy None)."""
    resz = [v for v in t.versek if v[0] > tol]
    oldal = resz[:meret]
    return oldal, (oldal[-1][0] if len(resz) > meret else None)


def kiemelt_vers(szoveg, tokenek, jelolt):
    """A Károli-vers HTML-je, a `jelolt` sorszámú szavak `<mark>`-kal; minden szövegrész escape-elt. Szótoken híján a szöveg maga."""
    if not tokenek:
        return escape(szoveg or '')
    igazit = q.szovegbe_igazit(szoveg, [szo for _, szo in tokenek])
    ki = []
    for (sz, szo), (kiir, szokoz) in zip(tokenek, igazit):
        if sz in jelolt and szo and szo in kiir:
            i = kiir.index(szo)
            x = escape(kiir[:i]) + Markup('<mark>%s</mark>') % szo + escape(kiir[i + len(szo):])
        else:
            x = escape(kiir)
        ki.append(x + (Markup(' ') if szokoz else Markup('')))
    return Markup('').join(ki).rstrip()


def lap_sorai(con, kozos, t, oldal, k, par_lathato=True):
    """A lap találati sorai: [{ig, url, html, heb}]."""
    igek = [ig for _, ig in oldal]
    vadat = q.vers_adatok(con, igek)
    hu_tok = q.hu_tokenek_versekre(con, igek)
    jelolt = {ig: set() for ig in igek}
    for ig, sz in t.hu:
        if ig in jelolt:
            jelolt[ig].add(sz)
    er_szo = {}
    if k.tipus in ('strong', 'heber') and par_lathato:
        er_poz = {ig: {sz for cs in t.er.get(ig, []) for g in cs for sz in g} for ig in igek} if k.tipus == 'heber' else {}
        for ig, hs, ers, st in q.par_versekre(con, igek):
            if (k.tipus == 'strong' and st in k.szavak) or (k.tipus == 'heber' and ers in er_poz.get(ig, ())):
                jelolt[ig].add(hs)
    if k.tipus == 'heber':
        er_tok = q.er_tokenek_versekre(con, igek)
        for ig in igek:
            szo_map = {sz: szo for sz, _, szo in er_tok.get(ig, [])}
            er_szo[ig] = [' '.join(''.join(szo_map.get(sz, '') for sz in g) for g in cs) for cs in t.er.get(ig, [])]
    ki = []
    for so, ig in oldal:
        kk, _, fv = ig.rpartition(' ')
        fej, vers = fv.split(':')
        szoveg = vadat.get(ig, (None, ''))[1]
        ki.append({'ig': ig, 'url': '/%s/%s/%s' % (kozos.slug.get(kk, ''), fej, vers),
                   'html': kiemelt_vers(szoveg, hu_tok.get(ig, []), jelolt.get(ig, set())),
                   'heb': er_szo.get(ig, []), 'token_nelkul': not hu_tok.get(ig)})
    return ki


def kereses_url(k, tol=None):
    """A találatlista állandó címe (a típusos paraméterrel); `tol`: a lapozás kulcsa."""
    from urllib.parse import urlencode
    p = [(k.tipus, k.szoveg)]
    if k.tipus == 'szo' and k.mod != ALAP_MOD:
        p.append(('mod', k.mod))
    if tol is not None:
        p.append(('tol', str(tol)))
    return '/kereses?' + urlencode(p)
