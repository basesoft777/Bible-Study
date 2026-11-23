"""Az olvasó kiejtése a projekt saját kiejtés-szolgáltatásából (F230, a felmérés 1. pontja; kiejtés-szabály).

A szó-lap és a versnézet ugyanazt a kiejtést mutatja, mint a lexikonlap: **nem** a `strong_szotar.kiejtes` (ragozott alakból
származó STEP-átírás) és nem a TBESH/TAHOT átírása.

- Héber szótő: a jóváhagyott kivétel (`adat/kiejtes_kivetelek.tsv`, nyelv=heber; kulcs: a lemma NFC alakja, majd a STEP-átírás),
  ennek híján a pontozott lemma gépi kiejtése (`heber_kiejtes.kiejt`, DT-F131y; a lexikonlap `lemma_kiejtes_szabaly`-a).
- Héber szó a versben: az írott szó (előtag + tő + toldalék, `heber_kiejtes.teljes_szo`) gépi kiejtése a tő csempéjén; az előtag- és
  toldalék-morféma (H9001…) csempéjén nincs külön kiejtés (egyedül olvasva hibás lenne: pl. a „-ו” toldalék „vó”).
- Görög: a TBESG/TAGNT SBL-átírásából a `kiejtes.py` magyaros átírása (szabálytábla + kivételek), mint a lexikonlap `gorog_magyaros`-a.
- **Tartalék:** ha nincs kivétel és nincs gépi szabály (pontozatlan alak, hiányzó átírás), a kiejtés üres (''), a lap nem hibázik.
  A TBESH/TAHOT átírása tartalékként sem jelenik meg kiejtésként.
A modulok fájlútról töltődnek (a `sys.path` nem változik), mint a `blokkok._eszkoz_modul`.
"""
import importlib.util
import os
import unicodedata


def _eszkoz_modul(nev):
    """Az `eszkozok/` közös modulja fájlútról (a lexikon-generátorral közös kód)."""
    ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), nev + '.py')
    spec = importlib.util.spec_from_file_location('eszkoz_' + nev, ut)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


KJ = _eszkoz_modul('kiejtes')
HK = _eszkoz_modul('heber_kiejtes')

_tabla = {}


def _betolt():
    if not _tabla:
        _tabla['szabaly'] = KJ.szabalyok_betolt()
        _tabla['gorog'] = KJ.kivetelek_betolt(nyelv='gorog')
        _tabla['heber'] = KJ.kivetelek_betolt(nyelv='heber')
    return _tabla


def heber_szoto(lemma, step_atiras=''):
    """A héber szótő kiejtése: jóváhagyott kivétel, ennek híján gépi; '' ha egyik sincs."""
    if not lemma:
        return ''
    t = _betolt()['heber']
    return (t.get(unicodedata.normalize('NFC', lemma)) or t.get(step_atiras or '')
            or HK.kiejt(lemma.split(',')[0].strip()) or '')


def gorog(sbl_atiras):
    """Görög SBL-átírásból magyaros kiejtés; '' átírás híján."""
    if not sbl_atiras:
        return ''
    t = _betolt()
    return KJ.atir(sbl_atiras, t['szabaly'], t['gorog']) or ''


def vers_szavak(sorok):
    """Egy vers (vagy a sorszám szerint rendezett token-sorok) kiejtései: `sorok` = [(nyelv, strong_nyers, alak, tahot_atiras)] a
    token_eredeti sorrendjében; a visszaadott lista ugyanolyan hosszú. Héber tő-sorra az írott szó kiejtése, előtag- és
    toldalék-sorra '' (l. a modul leírása); görög sorra a magyaros átírás a TAGNT átírásából."""
    het = [{'Strong-szám': (sn or ''), 'Ragozott alak': alak or '', 'Kiejtés': at or ''} for ny, sn, alak, at in sorok]
    ki = []
    for i, (ny, sn, alak, at) in enumerate(sorok):
        if ny == 'H':
            if (sn or '').startswith('H9'):
                ki.append('')
            else:
                a, elotag, makkef = HK.teljes_szo(het, i)
                ki.append(HK.kiejt(a, elotag, makkef))
        else:
            ki.append(gorog(iota_atiras(alak, at)))
    return ki


def iota_atiras(alak, at):
    """F231 (#34): a TAGNT átírása a szóvégi alsó iotás étát (ῇ, ῃ) „ēa”-nak írja („ἀρχῇ” → „archēa”, „τῇ” → „tēa”; a korpuszon
    1471 token): az alsó iota néma, a magyaros kiejtésben nem áll külön hang. Csak ott javít, ahol a görög alak szóvégén valóban
    alsó iotás éta áll."""
    jelek = '.,;:·'
    if not at or not at.rstrip(jelek).endswith('ēa'):
        return at
    d = unicodedata.normalize('NFD', (alak or '').rstrip(jelek + '᾿’\''))
    alap = ''.join(c for c in d if c in 'ηΗ\u0345' or unicodedata.category(c).startswith('L'))
    if not (alap.endswith('η\u0345') or alap.endswith('Η\u0345')):
        return at
    vege = len(at) - len(at.rstrip(jelek))
    return at[:len(at) - vege - 1] + at[len(at) - vege:]
