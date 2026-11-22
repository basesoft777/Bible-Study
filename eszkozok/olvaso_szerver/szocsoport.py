"""szocsoport.py — a héber elemek írott szó szerinti csoportja (F231, a #233 2. pontja; a JOHD-validáció szabálya).

A TAHOT a héber szót morfémákra bontja (előtag, szótő, rag külön sor, külön Strong-számmal); az olvasó a szavanként álló
csempéket ezért írott szavanként keretbe foglalja, a keret tetején az egész írott szóval. A szabály a JOHD-validáció
ellenőrző oldaláé (`eszkozok/karoli_strong_validacio_minta.py`, a `johd-validacio` ág, PR #762: `heber_tartalek_csoport`,
`macula_csoport`, `heber_csoport`, `szocsoport_ellenoriz`); az a modul nem importálható (a validáció saját bemeneteit tölti
be), ezért a négy függvény itt áll, a validáció adatformájához (`tok` elem: {'s': Strong, 'a': alak, 'w': Macula-szó})
igazítva; a csoportosítás szabálya változatlan, csak a `szocsoport_ellenoriz` adja vissza az eltérő verseket a megállás
helyett (a kiejtést a hívó adja át, a validáció a saját kivonatából töltötte). A teszt (`teszt_szocsoport.py`) a tartalék szabályt a Macula-csoportosítással
veti össze a teljes ószövetségi korpuszon.

Csak standard könyvtár; SQL és HTML nincs benne.
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def _h_szam(strong):
    m = re.fullmatch(r'H(\d{4})[A-Za-z]?', strong or '')
    return int(m.group(1)) if m else None


def macula_szo(xml_id):
    """A Macula-azonosító szó-része: az utolsó jegy a morféma sorszáma a szón belül (`o010010010012` → `o01001001001`)."""
    return (xml_id or '')[:-1] or None


def heber_tartalek_csoport(tok, kiejtes):
    """A héber elemek csoportja (írott szavanként) Macula-azonosító nélkül: az előtag (H9001–H9009) a következő
    elemhez, a rag (H9010–H9013, H9020–H9049) az előzőhöz, a H9014 mindkét oldalhoz tartozik; maqqef (a TAHOT-kiejtés
    végén kötőjel) után új írott szó kezdődik, kivéve, ha rag következik. Visszaad: csoportsorszám elemenként."""
    g = []
    cur = 0
    elo_elotag = elo_link = elo_maqqef = False
    for i, k in enumerate(tok):
        n = _h_szam(k['s'])
        elotag = n is not None and 9001 <= n <= 9009
        rag = n is not None and (9010 <= n <= 9013 or 9020 <= n <= 9049)
        link = n == 9014
        if i > 0 and not (rag or link or elo_link) and (elo_maqqef or not elo_elotag):
            cur += 1
        g.append(cur)
        elo_elotag, elo_link, elo_maqqef = elotag, link, (kiejtes[i] or '').endswith('-')
    return g


def macula_csoport(tok):
    """Csoportsorszám elemenként a Macula szóazonosítója szerint; None, ha nem minden elemnek van azonosítója."""
    if not tok or not all(k.get('w') for k in tok):
        return None
    g, cur, elozo = [], -1, None
    for k in tok:
        if k['w'] != elozo:
            cur += 1
        g.append(cur)
        elozo = k['w']
    return g


def heber_csoport(tok, kiejtes):
    """Az írott szó szerinti csoportok: a Macula szerint, ha minden elemnek van azonosítója, különben a tartalék
    szabállyal (a TAHOT-kiejtésből)."""
    m = macula_csoport(tok)
    if m is not None:
        return m
    return heber_tartalek_csoport(tok, kiejtes)


def szocsoport_ellenoriz(versek):
    """A tartalék csoportosítás a Macula-azonosítós verseken pontosan a Macula csoportosítását adja.
    `versek`: [(vers, tok, kiejtes)]. Visszaad: (összevetett versek száma, [eltérő versek])."""
    db, elter = 0, []
    for vers, tok, kiejtes in versek:
        m = macula_csoport(tok)
        if m is None:
            continue
        t = heber_tartalek_csoport(tok, kiejtes)
        if any((t[i] == t[i + 1]) != (m[i] == m[i + 1]) for i in range(len(tok) - 1)):
            elter.append(vers)
        db += 1
    return db, elter
