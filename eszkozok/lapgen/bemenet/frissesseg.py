"""lapgen.bemenet.frissesseg — a pillanatkép-bemenetek frissességi kapui (GK-03, S9c; DT-F218d (a), a lapgen bemeneti
rétegében).

A generált pillanatkép (a B05 mintájára) csak kapuval lehet bemenet: betöltéskor a kapu igazolja, hogy a pillanatkép a
mai bemenetekből készült, különben BemenetHiba, és a lap nem készül el belőle.

- **Fejléc-hash kapu (B18, B19, B21).** A generált tábla `# forras:` fejlécsora a forrásai hash-ét hordozza
  (`útvonal@<sha256 első 12 jegye>`, sorvég-normalizálva). A kapu a `FEJLEC_KAPU` szerint a jegyzékben álló forrásokat
  veti össze a mai fájllal; a forrásnak a fejlécben is állnia kell. Ami a jegyzékben nincs (a kód hash-e, a Macula-
  fájlok, a Thayer nyers lexikona), azt a kapu nem nézi; a B18 `forditasok.tsv@` hash-e a teljes fájlé, minden
  fordításváltozásnál eltér, ezért a kapu ezt sem nézi. Ezek az előállító szkriptek fejléc-bővítésével kapnak kaput
  (N-tétel a 218c-re, #238).
- **Lefedettségi kapu (B36, B38).** A B36-nak és a B38-nak nincs forrás-hash-e. A B36 egy héber szavának versei a mai
  héber szövegben (B08) is a szót hordozzák; a B38 motívumsorainak (héber szó, vers) párja a mai héber szövegben áll,
  kivéve, ha a sor csoportjában betoldás áll (a fordítás a héberben nem álló szót told be). Elavult pillanatkép (pl. a
  TAHOT átkulcsolása után) itt akad meg.

A kapu hash-olvasása nem tartalmi olvasás: nem kerül az olvasási naplóba (a lap forráslistája a tartalmi olvasásokból
jön), a mérce bemenet-hash őre pedig a tartalmi olvasásokat méri.
"""
import os
import re

from lapgen.bemenet.jegyzek import BemenetHiba

# bemenet → a fejlécében ellenőrzött források (jegyzékbeli azonosítók; a forrás minden útvonala, amelynek neve a
# fejlécben áll, összevetődik; legalább egynek állnia kell)
FEJLEC_KAPU = {
    'B18': ('B17',),
    'B19': ('B22', 'B34', 'B07', 'B30', 'B42', 'B08', 'B17'),
    'B21': ('B63', 'B07'),
}
_FORRAS_SOR = '# forras:'
_TAG_RX = re.compile(r'([A-Za-z0-9_./\-]+)@([0-9a-f]{12})\b')
_FEJ_SOROK = 5
_STRONG_UTOTAG_RX = re.compile(r'[a-z]$')


def fejlec_hashek(fejsorok):
    """A `# forras:` sor hash-ei fájlnév szerint ({név: hash12}); None, ha nincs ilyen sor."""
    sor = next((s for s in fejsorok if s.startswith(_FORRAS_SOR)), None)
    if sor is None:
        return None
    return {os.path.basename(utvonal): h for utvonal, h in _TAG_RX.findall(sor)}


def fejlec_ellenoriz(b_id, fejsorok, mai):
    """A fejléc-hash kapu tiszta része. `mai`: [(forrás-azonosító, útvonal, mai hash12)]. BemenetHiba, ha a fejléc
    hiányzik, egy forrás egyik útvonala sem áll benne, vagy egy hash eltér. Visszaadja az összevetett útvonalakat."""
    hashek = fejlec_hashek(fejsorok)
    if hashek is None:
        raise BemenetHiba('%s: a generált tábla fejlécében nincs `# forras:` sor; a pillanatkép frissessége nem '
                          'igazolható' % b_id)
    osszevetett, latott = [], set()
    for forras_id, utvonal, h in mai:
        nev = os.path.basename(utvonal)
        if nev not in hashek:
            continue
        latott.add(forras_id)
        if hashek[nev] != h:
            raise BemenetHiba('%s: elavult pillanatkép: a(z) %s (%s) a fejléc szerint %s, ma %s; futtasd újra az '
                              'előállító szkriptet' % (b_id, utvonal, forras_id, hashek[nev], h))
        osszevetett.append(utvonal)
    hianyzik = sorted({f for f, _u, _h in mai} - latott)
    if hianyzik:
        raise BemenetHiba('%s: a fejléc nem nevezi meg a forrását (%s); a pillanatkép frissessége nem igazolható'
                          % (b_id, ', '.join(hianyzik)))
    return tuple(osszevetett)


def fejlec_kapu(b, b_id):
    """A fejléc-hash kapu a bemenetre (`FEJLEC_KAPU`)."""
    fejsorok = b._fejsorok(b_id, b._egy_utvonal(b_id), _FEJ_SOROK)
    mai = [(f, u, b._hash_kapuhoz(u)[:12]) for f in FEJLEC_KAPU[b_id] for u in b._utvonalak(f)]
    return fejlec_ellenoriz(b_id, fejsorok, mai)


def _alap(strong_kod):
    return _STRONG_UTOTAG_RX.sub('', strong_kod)


def b36_ellenoriz(strong_kod, b36_versek, versben):
    """A B36 lefedettségi kapuja egy héber szóra: a tábla minden verse a mai héber szövegben is hordozza a szót.
    `versben(vers_kod)`: a vers Strong-kódjai a mai héber szövegben."""
    kint = sorted(v for v in b36_versek if _alap(strong_kod) not in {_alap(s) for s in versben(v)})
    if kint:
        raise BemenetHiba('B36: elavult pillanatkép: a(z) %s szó a mai héber szövegben nem áll ezekben a versekben: %s%s; '
                          'futtasd újra az `lxx_versszintu_import.py`-t'
                          % (strong_kod, ', '.join(kint[:5]), ' …' if len(kint) > 5 else ''))


def b38_ellenoriz(motivum_kod, sorok, versben):
    """A B38 lefedettségi kapuja a motívum ókori fordítás-soraira: (héber szó, vers) párja a mai héber szövegben
    áll, vagy a pár csoportjában betoldás-sor van. `sorok`: [(strong kódja, vers kódja, betoldás-e)]."""
    betoldasos = {(s, v) for s, v, bet in sorok if bet}
    kint = sorted({(s, v) for s, v, _bet in sorok if s.startswith('H') and (s, v) not in betoldasos
                   and _alap(s) not in {_alap(x) for x in versben(v)}})
    if kint:
        raise BemenetHiba('B38: elavult pillanatkép: a(z) %s motívum sorainak szava a mai héber szövegben nem áll a '
                          'versben: %s; a visszhang-tábla sorai frissítendők'
                          % (motivum_kod, ', '.join('%s %s' % p for p in kint[:5])))
