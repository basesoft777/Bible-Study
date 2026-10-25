#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.2 — a mai magyar múlt idő képzése és a jelen idejű alak elemzése (a .2 igealak-lépcsőjéhez).

Determinisztikus, kézi szabálykészlet (manual: a mai magyar igeragozás általános ismerete); a
kimenetet a hívó (`igealak.py`) a korpusz-támasszal és a felhasználói mintán méri. API, LLM és
Hunspell nélkül. Nem olvas és nem ír fájlt.

  szetbont(lemma)            → (igekötő, alapige): a leghosszabb igekötő, amely után ige marad
  mult(alapige, szem, targy) → a mai múlt idejű alak az igekötő nélkül (szem: E1 E2 E3 T1 T2 T3;
                               targy: True = tárgyas ragozás), vagy None
  jelen_elemez(alak, lemma)  → (igekötő, alapige, szem, targy) a jelen idejű alakra, vagy None

A múlt idő tövének típusai (a mai ragozás szerint; a kivételek kézi listában):
  kozvetlen   -l -r -n -ny -j -ly magánhangzó után, és az áll/száll: felelt, felelte, feleltek
  e3_kotohang az E/3 alanyi kötőhangzós, a többi nem: mondott/mondta, látott/látta, nézett/nézte
  kotohang    mindenütt kötőhangzós: -ít, mássalhangzó + t, egytagú rövid magánhangzó + t,
              mássalhangzó-torlódás: tanított/tanította, tartott/tartotta, ütött/ütötte, nemzett/nemzette
  hosszu      egytagú, hosszú magánhangzóra végződő tő: lő → lőtt/lőtte
"""

import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

MGH = 'aáeéiíoóöőuúüű'
MELY = 'aáoóuú'
KEREK = 'öőüű'
SZEMELYEK = ('E1', 'E2', 'E3', 'T1', 'T2', 'T3')

IGEKOTOK = sorted([
    'meg', 'el', 'ki', 'be', 'bé', 'fel', 'föl', 'le', 'rá', 'reá', 'át', 'által', 'ide', 'oda', 'vissza',
    'össze', 'egybe', 'hozzá', 'szét', 'széjjel', 'elő', 'utána', 'alá', 'fölé', 'felé', 'haza', 'végig',
    'közbe', 'bele', 'belé', 'keresztül', 'körül', 'félre', 'tovább', 'ellen', 'előre', 'hátra', 'újjá',
    'szembe', 'mellé', 'neki', 'néki', 'fenn', 'benn', 'kinn', 'alább', 'végbe', 'elé', 'helyre', 'abba',
    'ellene', 'után', 'hátra', 'fölül', 'felül', 'ki', 'jóvá', 'rendbe', 'tönkre', 'számba', 'kézbe',
], key=len, reverse=True)

# Rendhagyó múlt (alapige → (E/3 alanyi, a többi személy töve)). Kézi lista (manual).
RENDHAGYO = {
    'van': ('volt', 'volt'), 'lesz': ('lett', 'lett'), 'megy': ('ment', 'ment'), 'men': ('ment', 'ment'),
    'jön': ('jött', 'jött'), 'jő': ('jött', 'jött'), 'vesz': ('vett', 'vett'), 'tesz': ('tett', 'tett'),
    'visz': ('vitt', 'vitt'), 'hisz': ('hitt', 'hitt'), 'eszik': ('evett', 'ett'), 'iszik': ('ivott', 'itt'),
    'alszik': ('aludt', 'aludt'), 'aluszik': ('aludt', 'aludt'), 'fekszik': ('feküdt', 'feküdt'),
    'nyugszik': ('nyugodott', 'nyugodt'), 'haragszik': ('haragudott', 'haragudt'),
    'esküszik': ('esküdött', 'esküdt'), 'cselekszik': ('cselekedett', 'cselekedt'),
    'cselekedik': ('cselekedett', 'cselekedt'), 'dicsekszik': ('dicsekedett', 'dicsekedt'),
    'emlékszik': ('emlékezett', 'emlékezt'), 'törekszik': ('törekedett', 'törekedt'),
    'öregszik': ('öregedett', 'öregedt'), 'telik': ('telt', 'telt'), 'hal': ('halt', 'halt'),
    'lát': ('látott', 'látt'), 'hall': ('hallott', 'hallott'), 'kell': ('kellett', 'kellett'),
    'vall': ('vallott', 'vallott'), 'áll': ('állt', 'állt'), 'száll': ('szállt', 'szállt'),
    'bocsát': ('bocsátott', 'bocsátott'), 'mond': ('mondott', 'mondt'), 'küld': ('küldött', 'küldt'),
    'hord': ('hordott', 'hordt'), 'kezd': ('kezdett', 'kezdt'), 'ad': ('adott', 'adt'),
    'áld': ('áldott', 'áldott'), 'old': ('oldott', 'oldott'), 'told': ('toldott', 'toldott'),
    'érez': ('érzett', 'érezt'), 'érzik': ('érzett', 'érezt'), 'nyugodik': ('nyugodott', 'nyugodt'),
    'fő': ('főtt', 'főtt'), 'fú': ('fújt', 'fújt'), 'fúj': ('fújt', 'fújt'),
    # hangkivető tő: az E/3 alanyi rövidült tövön (könyörgött), a többi a teljesen (könyörögtek)
    'könyörög': ('könyörgött', 'könyörögt'), 'forog': ('forgott', 'forogt'), 'mozog': ('mozgott', 'mozogt'),
    'zörög': ('zörgött', 'zörögt'), 'dörög': ('dörgött', 'dörögt'), 'morog': ('morgott', 'morogt'),
    'őriz': ('őrzött', 'őrizt'), 'terem': ('termett', 'termett'), 'melegszik': ('melegedett', 'melegedt'),
    'cselekeszik': ('cselekedett', 'cselekedt'),
}
# Az -ad/-ed végű, kötőhangzó nélküli E/3 (marad → maradt; a fogad, tagad, enged, szenved szabályos).
for _v in ('marad', 'szakad', 'olvad', 'terjed', 'gerjed', 'halad', 'támad', 'szalad', 'akad', 'fakad', 'apad',
           'dagad', 'hasad', 'reped', 'ébred', 'éled', 'lohad', 'fárad', 'csügged', 'ragad', 'buzdul'):
    RENDHAGYO.setdefault(_v, (_v + 't', _v + 't'))
# Csak i/í hangú, mély hangrendű igék (hív → hívott, hívta); a többi i-s ige magas (int → intett, intette).
I_MELY = {'hív', 'nyit', 'szív', 'vív', 'ír', 'sír', 'bír', 'iszik', 'indít', 'nyír', 'irt', 'szít', 'híz', 'ivott', 'itt',
          'bíz', 'bízik', 'tilt', 'szid', 'nyí', 'víj'}
# Rendhagyó jelen (alak → (alapige, személy, tárgyas)); a szabályos elemzés nem fedi.
JELEN_RENDHAGYO = {
    'megy': ('megy', 'E3', False), 'megyen': ('megy', 'E3', False), 'mennek': ('megy', 'T3', False),
    'megyek': ('megy', 'E1', False), 'mégy': ('megy', 'E2', False), 'mész': ('megy', 'E2', False),
    'megyünk': ('megy', 'T1', False),
    'jő': ('jön', 'E3', False), 'jön': ('jön', 'E3', False), 'jőnek': ('jön', 'T3', False),
    'jönnek': ('jön', 'T3', False), 'jövök': ('jön', 'E1', False), 'jövünk': ('jön', 'T1', False),
    'ád': ('ad', 'E3', False), 'ádnak': ('ad', 'T3', False),
    'cselekszik': ('cselekedik', 'E3', False), 'cselekesznek': ('cselekedik', 'T3', False),
    'cselekszi': ('cselekedik', 'E3', True), 'cselekszik_t': ('cselekedik', 'T3', True),
    'issza': ('iszik', 'E3', True), 'isszák': ('iszik', 'T3', True), 'eszi': ('eszik', 'E3', True),
    'eszik': ('eszik', 'E3', False), 'esznek': ('eszik', 'T3', False), 'iszik': ('iszik', 'E3', False),
    'isznak': ('iszik', 'T3', False), 'alszik': ('alszik', 'E3', False), 'aluszik': ('alszik', 'E3', False),
    'alszanak': ('alszik', 'T3', False), 'fekszik': ('fekszik', 'E3', False), 'feküsznek': ('fekszik', 'T3', False),
    'fekszenek': ('fekszik', 'T3', False), 'nyugszik': ('nyugszik', 'E3', False),
    'cselekeszik': ('cselekedik', 'E3', False), 'melegszik': ('melegszik', 'E3', False),
    'veszik': ('vesz', 'T3', True), 'teszik': ('tesz', 'T3', True), 'viszik': ('visz', 'T3', True),
    'hiszik': ('hisz', 'T3', True), 'veszi': ('vesz', 'E3', True), 'teszi': ('tesz', 'E3', True),
    'viszi': ('visz', 'E3', True), 'hiszi': ('hisz', 'E3', True),
    'van': ('van', 'E3', False), 'vannak': ('van', 'T3', False), 'vagyon': ('van', 'E3', False),
    'lesz': ('lesz', 'E3', False), 'lesznek': ('lesz', 'T3', False),
    'emlékezik': ('emlékezik', 'E3', False), 'emlékeznek': ('emlékezik', 'T3', False),
}
# Az *-ik* nélküli alapige *-ik*-es lemmához (lakik → lak).
DIGRAF = ('dzs', 'dz', 'cs', 'gy', 'ly', 'ny', 'sz', 'ty', 'zs')


def hang(szo):
    """o (mély), ö (magas, ajakkerekítéses utolsó magánhangzó), e (magas); csak i/í: mély (hív → hívott)."""
    m = [c for c in szo if c in MGH]
    if not m:
        return 'e'
    if any(c in MELY for c in m):
        return 'o'
    if all(c in 'ií' for c in m):
        return 'o' if szo in I_MELY or any(szo.endswith(x) for x in I_MELY) or szo.endswith('ít') else 'e'
    return 'ö' if m[-1] in KEREK else 'e'


def fonemak(szo):
    """A szó hangjai (a kétjegyű mássalhangzók egy hangként), a végéről nézve elég."""
    ki = []
    i = 0
    while i < len(szo):
        for d in DIGRAF:
            if szo.startswith(d, i):
                ki.append(d)
                i += len(d)
                break
        else:
            ki.append(szo[i])
            i += 1
    return ki


def szotagszam(szo):
    return sum(1 for c in szo if c in MGH)


def to_tipus(v):
    """A múlt idő tövének típusa (l. a modul leírását)."""
    f = fonemak(v)
    if not f:
        return None
    utolso = f[-1]
    if utolso[0] in MGH:
        return 'hosszu' if szotagszam(v) == 1 and utolso in 'áéíóőúű' else None
    elozo = f[-2] if len(f) > 1 else ''
    torlodas = bool(elozo) and elozo[0] not in MGH
    if v.endswith('ít'):
        return 'kotohang'
    if utolso == 't':
        if torlodas:
            return 'kotohang'
        if szotagszam(v) == 1 and elozo in 'aeiouöü':
            return 'kotohang'  # üt, vet, köt, fut, jut, nyit
        return 'e3_kotohang'  # mutat → mutatott / mutatta
    if torlodas:
        if utolso == 'd':
            return 'e3_kotohang'  # kérd-típus: a mond, küld, hord, kezd a RENDHAGYO-ban
        if utolso in ('l', 'r', 'n', 'ny', 'j', 'ly') and elozo == utolso:
            return 'kotohang'  # hall, kell, forr
        return 'kotohang'  # nemz, áld, ért, teremt
    if utolso in ('l', 'r', 'n', 'ny', 'j', 'ly'):
        return 'kozvetlen'
    return 'e3_kotohang'


def kotohang(v):
    return {'o': 'ott', 'e': 'ett', 'ö': 'ött'}[hang(v)]


def mult_tovek(alapige):
    """(E/3 alanyi alak, a többi személy töve) vagy None."""
    if alapige in RENDHAGYO:
        return RENDHAGYO[alapige]
    v = alapige[:-2] if alapige.endswith('ik') and len(alapige) > 3 else alapige
    t = to_tipus(v)
    if t is None:
        return None
    if t == 'kozvetlen':
        return v + 't', v + 't'
    if t == 'hosszu':
        return v + 'tt', v + 'tt'
    if t == 'kotohang':
        return v + kotohang(v), v + kotohang(v)
    return v + kotohang(v), v + 't'


ALANYI = {'o': {'E1': 'am', 'E2': 'ál', 'T1': 'unk', 'T2': 'atok', 'T3': 'ak'},
          'e': {'E1': 'em', 'E2': 'él', 'T1': 'ünk', 'T2': 'etek', 'T3': 'ek'}}
TARGYAS = {'o': {'E1': 'am', 'E2': 'ad', 'E3': 'a', 'T1': 'uk', 'T2': 'átok', 'T3': 'ák'},
           'e': {'E1': 'em', 'E2': 'ed', 'E3': 'e', 'T1': 'ük', 'T2': 'étek', 'T3': 'ék'}}


def mult(alapige, szem, targy):
    tv = mult_tovek(alapige)
    if tv is None or szem not in SZEMELYEK:
        return None
    e3, to = tv
    h = 'o' if hang(alapige[:-2] if alapige.endswith('ik') and alapige not in I_MELY else alapige) == 'o' else 'e'
    if not targy and szem == 'E3':
        return e3
    if targy:
        return to + TARGYAS[h][szem]
    return to + ALANYI[h][szem]


MULT_MINTA = re.compile(r'(tt(am|em|ál|él|unk|ünk|atok|etek|ak|ek|a|e|ák|ék|uk|ük|ad|ed|átok|étek)?|'
                        r'[^aáeéiíoóöőuúüű]t(ak|ek|am|em|a|e|ák|ék|atok|etek|unk|ünk|uk|ük|ál|él|ad|ed))$')


def mult_alak_e(alak, lemma, szavak=()):
    """A mai múlt idő alakja (-tt, mássalhangzó + t + személyrag; a -lt/-rt/-nt/-jt, ha nem a lemma, vagy
    ha a t nélküli tő főnévi igeneve a korpuszban áll: írt → írni)."""
    a = alak.lower()
    if a == lemma.lower():
        return bool(re.search(r'(l|r|n|j|y)t$', a)) and (a[:-1] + 'ni') in szavak
    return bool(MULT_MINTA.search(a)) or bool(re.search(r'(l|r|n|j|y)t$', a))


SZEM_VEG = {'': ('E3', False), 'a': ('E3', True), 'e': ('E3', True), 'ak': ('T3', False), 'ek': ('T3', False),
            'ák': ('T3', True), 'ék': ('T3', True), 'am': ('E1', False), 'em': ('E1', False), 'ál': ('E2', False),
            'él': ('E2', False), 'ad': ('E2', True), 'ed': ('E2', True), 'unk': ('T1', False), 'ünk': ('T1', False),
            'uk': ('T1', True), 'ük': ('T1', True), 'atok': ('T2', False), 'etek': ('T2', False),
            'átok': ('T2', True), 'étek': ('T2', True), 'alak': ('E1', True), 'elek': ('E1', True),
            'lak': ('E1', True), 'lek': ('E1', True)}


# Az E/3 és T/3 alanyi kötőhangzós múlt csak ezeken az igéken cserél (a korpusz gyakori, igei használatú alakjai).
KOTOHANG_IGE = {'szól', 'áll', 'száll', 'mond', 'támad', 'gerjed', 'küld', 'marad', 'szalad', 'ragad', 'kezd', 'múl',
                'fárad', 'olvad', 'szakad', 'származ', 'mondot'}


def kotohang_mult(alak, lemma, szavak):
    """A régies, kötőhangzós múlt mai alakja (mondotta → mondta, szólott → szólt, állottak → álltak), ha
    a mai ragozás kötőhangzó nélküli; None, ha az alak nem ilyen, vagy a mai alakja ugyanaz."""
    a = alak.lower()
    kot, alap = szetbont(lemma.lower(), szavak)
    v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
    if not v or not a.startswith(kot + v):
        return None
    if a.startswith(('halott', 'körülött')) or (alap in RENDHAGYO and not RENDHAGYO[alap][0].startswith(v)):
        return None  # halott (melléknév); elveszett, veszett: az elvész, nem az elvesz (vett) alakja
    for kh in ('ott', 'ett', 'ött'):
        alap_t = v + kh[0] + 't'
        if any((k + alap_t + x) in szavak for k in ('', kot) for x in ('ik', 'ni', 'ett', 'ott', 'ött', 'etik', 'atik')):
            continue  # születtél (születik), küldettem (küldetett), verettek (veretik): saját igető
        if a.startswith(kot + v + kh):
            veg = a[len(kot + v + kh):]
            if veg not in SZEM_VEG:
                return None
            szem, targy = SZEM_VEG[veg]
            if szem in ('E3', 'T3') and not targy and v not in KOTOHANG_IGE:
                return None  # a puszta -ott / -ottak melléknévi igenév is lehet (törött, elbizakodottak, megölöttek)
            m = mult(alap, szem, targy)
            if m and kot + m != a:
                return kot + m
    return None


def ige_e(alapige, szavak):
    """Igei-e az alapige: rendhagyó, vagy a főnévi igenév (tő + -ni/-ani/-eni) a korpuszban áll."""
    if alapige in RENDHAGYO or alapige in ('megy', 'jön', 'van', 'lesz'):
        return True
    v = alapige[:-2] if alapige.endswith('ik') and len(alapige) > 3 else alapige
    if len(v) < 2:
        return False
    if any((v + s) in szavak for s in IGEI_VEG):
        return True
    return any((k + v + s) in szavak for k in IGEKOTOK for s in IGEI_VEG[:3])  # összegyűlni → gyűl


# Az igeiség próbája: főnévi igenév, ható ige, felszólító mód (a múlt -tt nem: helyett, között, alatt).
IGEI_VEG = ('ni', 'ani', 'eni', 'hat', 'het', 'hatnak', 'hetnek', 'jon', 'jen', 'jön', 'jenek', 'janak')


def mult_lemma_nelkul(alak, szavak):
    """Mai múlt idejű igealak-e, a #94 lemmája nélkül: (igekötő +) rendhagyó múlt tő (jött-, ment-, vett-),
    vagy tő + -t/-tt/-ott/-ett/-ött + személyrag, ahol a tő főnévi igeneve a korpuszban áll (hallotta →
    hallani, ástak → ásni). A határozószó (előtt, mellett, között) így kiesik: a tövének nincs igeneve."""
    a = alak.lower()
    kotok = [''] + [k for k in IGEKOTOK if a.startswith(k) and len(a) > len(k) + 2]
    rendhagyo = set()
    for e3, to in RENDHAGYO.values():
        rendhagyo.update((e3, to))
    for k in kotok:
        r = a[len(k):]
        if r in ('itt', 'ott'):
            continue
        for st in rendhagyo:
            if len(st) >= 3 and r != st[:3] and r.startswith(st) and r[len(st):] in SZEM_VEG and r not in ('ett', 'itt'):
                return True
        for kh in ('ott', 'ett', 'ött', 'tt', 't'):
            i = r.rfind(kh)
            while i > 0:
                x, veg = r[:i], r[i + len(kh):]
                if veg in SZEM_VEG and len(x) >= 2 and ige_e(x, szavak):
                    return True
                i = r.rfind(kh, 0, i)
    return False


def lemma_jeloltek(alak, szavak):
    """A #94 által elemezetlen igealak (szótári alak = alak) lehetséges szótári alakjai, a leghosszabbtól:
    a végződés levágásával kapott tő (és -ik-es párja), ha igei (ige_e)."""
    a = alak.lower()
    ki = []
    for n in range(0, min(6, len(a) - 1)):
        t = a[:len(a) - n] if n else a
        for l in (t, t + 'ik'):
            if l not in ki and len(l) >= 2:
                k, ap = szetbont(l, szavak)
                if ige_e(ap, szavak):
                    ki.append(l)
    return ki


def szetbont(lemma, szavak):
    """(igekötő, alapige): a leghosszabb igekötő, amely után igei alapige marad; különben ('', lemma)."""
    for k in IGEKOTOK:
        if lemma.startswith(k) and len(lemma) > len(k) + 1 and ige_e(lemma[len(k):], szavak):
            return k, lemma[len(k):]
    return '', lemma


def jelen_elemez(alak, lemma, szavak):
    """A jelen idejű alak elemzése a lemma (szótári alak) tövéhez mérve: (igekötő, alapige, szem, tárgyas)."""
    a = alak.lower()
    l = lemma.lower()
    kot, alap = szetbont(l, szavak)
    if not a.startswith(kot):
        return None
    resz = a[len(kot):]
    if resz in JELEN_RENDHAGYO:
        ap, szem, t = JELEN_RENDHAGYO[resz]
        return kot, ap, szem, t
    ik = alap.endswith('ik') and len(alap) > 3
    v = alap[:-2] if ik else alap
    if not resz.startswith(v):
        return None
    veg = resz[len(v):]
    # sziszegő tövön a -j- hasonul (hozza, olvassa, hozzák)
    if v[-1:] in ('s', 'z') and veg[:1] == v[-1:] and len(veg) > 1:
        veg = 'j' + veg[1:]
    if veg == 'ik':
        # -ik: E/3 alanyi (ik-ige), vagy magas hangrendű tárgyas T/3 (kérik, nézik, temetik); a #94 lemmája
        # itt nem dönt (temetik: -ik lemma), hanem a tárgyas E/3 (temeti) vagy múlt (temették) a korpuszban
        targyas_t3 = hang(v) != 'o' and any((kot + v + x) in szavak or (v + x) in szavak for x in ('i', 'ték', 'te'))
        return kot, alap, ('T3' if targyas_t3 else 'E3'), targyas_t3
    if veg == '':
        return kot, alap, 'E3', False
    if veg in ('nak', 'nek', 'anak', 'enek'):
        return kot, alap, 'T3', False
    if veg in ('ja', 'i'):
        return kot, alap, 'E3', True
    if veg == 'ják':
        return kot, alap, 'T3', True
    if veg in ('ok', 'ek', 'ök', 'om', 'em', 'öm'):
        return kot, alap, 'E1', veg in ('om', 'em', 'öm') and not ik
    if veg in ('unk', 'ünk'):
        return kot, alap, 'T1', False
    if veg in ('juk', 'jük'):
        return kot, alap, 'T1', True
    if veg in ('tok', 'tek', 'tök', 'otok', 'etek', 'ötök'):
        return kot, alap, 'T2', False
    if veg in ('játok', 'itek'):
        return kot, alap, 'T2', True
    if veg in ('sz', 'asz', 'esz', 'ol', 'el', 'öl'):
        return kot, alap, 'E2', False
    if veg in ('od', 'ed', 'öd'):
        return kot, alap, 'E2', True
    return None
