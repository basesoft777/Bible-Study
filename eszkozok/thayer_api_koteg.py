#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F158 — a Thayer szakaszonkénti fordításának Batch-kötegelője (Anthropic Message Batches API; DT-F27a).

A `bdb_api_koteg.py` Thayer-párja. A `thayer_jelolt/forditas.py` függvényeit hívja (prompt v5.2, adatblokk,
javítóréteg + 14–16. kapu, szakaszsorok, beírás), nem másolja; a REST-hívó, a kulcskezelés (`PARDES_API_KEY`), a
`tsv_olvas` / `tsv_hozzaad` az `eszkozok/karoli_strong/api_koteg.py`-ból, a tiszta segédek (költség, JSON-válasz,
javító üzenet, modellnév) a `bdb_api_koteg.py`-ból jönnek. A kulcs nem íródik ki, fájlba nem kerül.

Egység: Strong; a nagy szócikk csoportjai (`thayer_bemenet.csoportok`) külön kérések. `custom_id` = `<strong>-c<csoport>-p<próba>`.
A forrás a csoport `helyorzo_bont` ⟦n⟧ helyőrzőit kapja (a héber/görög szakaszok; csoportonként 1-től), a visszaállítás betűhű.

  lista     [--ki PATH] [--ts NAP]  a teljes Thayer futási listája (a `szolista.allapot` szabályával); repóba nem ír
  szaraz    --adag N --strongok FÁJL   a kérések összeállítása hálózat nélkül: kérés-, csoport-, karakterszám, becslés, csomagolás
  bszaraz   a B-út (15–25 kicsi/közepes Strong / kérés) száraz futása: kérésszám, szűkített állandó rész, kalibrált becslés
  bbekuld   a B-kérések beküldése (--db: az első DB; plafon: mért futó összeg + becslés; a nagyok a `bekuld`-del, egyenként)
  bekuld    a következő csomag beküldése — csak a megadott plafonnal (--plafon USD; alapérték 0 = tilos)
  allapot   a batch-ek állapota
  begyujt   a kész batch-ek nyers válaszai a valaszok.jsonl-be, költségnapló
  kapuz     válasz → JSON → helyőrző-visszaállítás → `forditas.utofeldolgoz` (javítóréteg + kapuk) → kapu_eredmeny.jsonl
  javit     a kapun bukott Strongok 2. batch-e (a kapu hibaüzenetével)
  rogzit    a kapun átment Strongok szakaszsorai a munkatáblába (`naplok/F132_THAYER_SZAKASZ_munka.tsv`); a kétszer
            bukottak a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be
  beir      STRONG… a munkatábla szakaszsorai az `adat/forditasok.tsv`-be (`forditas.beir`; --regi-elavult, --kezi-marad)
  --onteszt a hálózat nélküli öntesztek

Használat:
    python eszkozok/thayer_api_koteg.py lista --ki <repón kívül>/lista.tsv
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt --munka <repón kívül> szaraz
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt --plafon 20 bekuld
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt allapot|begyujt|kapuz|javit|rogzit
    python eszkozok/thayer_api_koteg.py --adag 1 --strongok strongok.txt beir --regi-elavult --allapot sonnet

A `--strongok` fájl soronként egy Strong (G1941; üres és `#` sorok kimaradnak; egy sor első tabig számít).
Kilépési kódok: 0 rendben; 2 hibás paraméter/előfeltétel; 3 a plafon megállít; 4/5 az api_koteg.py szerint.
TSV: split('\\t'), '\\t'.join(); csv modul nincs.
"""

import argparse
import datetime
import json
import os
import re
import sys
import time

ITT = os.path.dirname(os.path.abspath(__file__))
THAYER_MAPPA = os.path.join(ITT, 'thayer_jelolt')
for _u in (os.path.join(ITT, 'karoli_strong'), ITT, THAYER_MAPPA):     # a THAYER_MAPPA elöl: kulcs, adatblokk, thayer_bemenet
    if _u not in sys.path:
        sys.path.insert(0, _u)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import api_koteg as AK  # noqa: E402
import emeles as E  # noqa: E402
import forditas as F  # noqa: E402
import forditas_kapuk as K  # noqa: E402  (csak a terminológia-kulcs illesztése: `_angol_minta`, ugyanaz, mint az 5. kapué)
import kulcs  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402
import bdb_api_koteg as B  # noqa: E402  (csak a tiszta segédei: költség, JSON-válasz, javító üzenet, modellnév)

ROOT = AK.tokenek.ROOT
MODELL = AK.MODELL                 # claude-sonnet-5-5 (a kérésben kért; a rögzítés a válasz tényleges modellnevét írja)
PLAFON_USD = 0.0                   # beküldés tilos, amíg a plafon nincs megadva (--plafon)
EREDET = ''                        # --eredet: a rogzit megjegyzésébe kerülő eredet-szöveg (F07 M0 (f))
ELOZO_KIADAS_USD = 0.0             # egy közös plafon alatt futó másik adag(ok) mért költsége (--elozo-kiadas)
MUNKA_GYOKER = os.path.join(ROOT, 'forditas', 'thayer_api')
MUNKA_TABLA = F.MUNKA_UT
BUKOTT_UT = os.path.join(ROOT, 'naplok', 'F132_THAYER_SZAKASZ_bukottak.tsv')
BUKOTT_FEJLEC = ['strong', 'kapu', 'ok', 'probalkozas', 'modell', 'datum', 'proveniencia']
CSOMAG = 450                       # kérés / batch (a plafon csomagonként ellenőrződik)
EFFORT = 'high'                    # --effort high|medium (a kérés `output_config.effort`-ja és a futásnapló oszlopa)
EFFORTOK = ('high', 'medium')
# A becslő kalibrálása az F27 M1 mért illesztéséből (naplok/FP3_naplo.md, naplok/FP3_koltseg.py; 51 első körös kérés,
# legkisebb négyzetek; N-F27a). Mind becslés (manual) a mérő batch újraillesztéséig.
BE_KERES = 17136                   # bemeneti token / kérés (a prompt állandó része, szűkítés ELŐTT)
BE_KAR = 3.721                     # bemeneti token / forráskarakter (az adatblokk és a forrás)
KI_KERES = 1134                    # kimeneti (gondolkodással) token / kérés
KI_KAR = 1.654                     # kimeneti (gondolkodással) token / forráskarakter
ALLANDO_REF_KAR = 36257            # a G25 kérés állandó részének karaktere (nem Strongonkénti rész), szűkítés ELŐTT
ALLANDO_KAR_TOKEN = ALLANDO_REF_KAR / BE_KERES     # karakter / token az állandó részre (~2,12; manual)
# F07 M0 (a) (N68 lezárása): az újraillesztés a #27 M1 (51 egy Strongos 1. körös kérés) és a #159 mérő batch (4 B-kérés mindkét
# effortra, 15 javító kérés) mért adataiból: `python naplok/THAYER_ELES_M0.py illeszt`, a részletek a naplok/THAYER_ELES_naplo.md-ben.
# A fenti egy Strongos (A) konstansok az 51 pontra változatlanul érvényesek (R² 0,93 / 0,95); a B-kérés saját együtthatót kap.
B_BE_ALLANDO = 0.684               # bemeneti token / állandó karakter a szűkített B-kérésben (14 426 token / ~21 100 karakter; 4 pont)
B_BE_KAR = 3.178                   # bemeneti token / forráskarakter a B-kérésben (4 pont, átl. |hiba| 7,5%)
B_KI_KAR = {'high': 1.959, 'medium': 1.5207}     # kimeneti (gondolkodással) token / forráskarakter a B-kérésben, effortonként (4-4 pont)
A_KI_EFFORT = {'high': 1.0, 'medium': 0.51}  # az egy Strongos kimenet effort-szorzója (F07 M0 (e): medium/high kimenet 33 660 / 66 300 token az 5 nagy kérésen)
JAVITO_ARANY = {'A': 0.73, 'B': 0.15}           # javító kör költsége / 1. kör költsége. A = nagy: pooled 10,11 / 11,37 USD = 0,890 azokban a futásokban, ahol a javító kör az összes bukott
#                                                  Strongra lefutott (adag1 0,867, adag99 0,883, adag7902 0,84, adag7903 0,95, adag701 0,899 [6,5247 / 7,2575]); az adag7901 részleges javító köre kimarad.
#                                                  B = kicsi/közepes B-javító: az adag701 mért J001 kérése 0,0174 USD / a B-kérés 0,0471 USD = 0,37 (3 Strong, mind kapun bukott az 1. körben:
#                                                  8_idezojel, 16_sigla; az M0 J001: 0,0233 USD, 2 Strong); kis minta, manual — a B-rész az adag költségének ~0,6%-a (F07 A1)
#                                                  F07 A2 újraillesztés (adag702, 85 Strong, első körös bukás 47/85): nagy 4,722 / 8,970 = 0,526; B-javító 0,0877 / 0,6333 = 0,138.
#                                                  Pooled (A1 + A2 + a korábbi futások): A (10,11 + 4,722) / (11,37 + 8,970) = 0,729; B (0,0174 + 0,0877) / (0,0471 + 0,6333) = 0,154. Az arány a bukási aránytól függ
#                                                  (A1 89%, A2 55%); a kapujavítások után a későbbi adagokban kevesebb a bukás, a becslés így konzervatív (manual).
# B-út (csoportos): a kicsi (< KICSI_HATAR) és a közepes (< NAGY_HATAR) Strongok n Strongonként egy kérésben, a nagyok egyenként
KICSI_HATAR, NAGY_HATAR = 500, 3000
B_DB = 20                          # Strong / B-kérés (15–25; a mérés tárgya, --b-db)
B_KAR = 16000                      # forráskarakter / B-kérés felső határa (a kimenet ne lépje át a max_tokens-t)
SZUKIT = True                      # a terminológia- és a Károli-tábla szűkítése a kérés forrására (--nincs-szukites: ki)
AR_BE, AR_KI = B.AR_BE, B.AR_KI
NAPLO_FEJLEC = B.NAPLO_FEJLEC
BATCH_FEJLEC = B.BATCH_FEJLEC
CID = re.compile(r'^(?P<strong>G\d{4}[a-z]?)-c(?P<csoport>\d+)-p(?P<proba>\d)$')      # csak görög (Thayer)
CID_B = re.compile(r'^B(?P<n>\d{3})-p(?P<proba>\d)$')
CID_BJ = re.compile(r'^J(?P<n>\d{3})-p(?P<proba>\d)$')      # F07 M0 (b): B-stílusú javító kérés (kicsi/közepes Strongok csoportosan)
FORRAS_JEL = 'Forrás (Thayer, angol):'
KIMENET_JEL = '## Kimenet'

MUNKA = MUNKA_GYOKER               # adagonként: MUNKA/adag<N>/ (a main() állítja; --munka felülírja)


# ---------- segédek ----------

def ut(*r):
    return os.path.join(MUNKA, *r)


custom_id = B.custom_id


def custom_id_bont(cid):
    m = CID.match(cid)
    return (m.group('strong'), int(m.group('csoport')), int(m.group('proba'))) if m else None


koltseg = B.koltseg
jsonl_olvas = B.jsonl_olvas
jsonl_hozzaad = B.jsonl_hozzaad
json_valasz = B.json_valasz
javito_uzenet = B.javito_uzenet
modell_allapot = B.modell_allapot


def max_tokens_kerelemre(forras_kar):
    """Egy Strongos kérés max_tokens-e: a kalibrált kimenet-becslés háromszorosa (felső korlát, nem költség)."""
    return int(min(64000, max(16000, 3 * (forras_kar * KI_KAR + KI_KERES) + 4000)))


def kerelem_params(uzenetek, forras_kar, max_tokens=None):
    return {'model': MODELL, 'max_tokens': max_tokens or max_tokens_kerelemre(forras_kar),
            'thinking': {'type': 'adaptive'}, 'output_config': {'effort': EFFORT}, 'messages': uzenetek}


def futo_osszeg():
    """Az eddig begyűjtött batchek MÉRT költsége (USD, a válaszok usage-éből; `futasnaplo.tsv`)."""
    return sum(float(s['koltseg_usd'] or 0) for s in AK.tsv_olvas(ut('futasnaplo.tsv')))


def fuggo_becsles(cimke=None):
    """A beküldött, de még be nem gyűjtött batchek beküldéskori becslése (USD, manual) — a mért összeg még nem tartalmazza."""
    ossz = 0.0
    for b in AK.tsv_olvas(ut('batchek.tsv')):
        if cimke is not None and b['cimke'] != cimke:
            continue
        if not os.path.exists(ut('begyujtve_%s.txt' % b['batch_id'])) and os.path.exists(ut('becsles_%s.txt' % b['batch_id'])):
            with open(ut('becsles_%s.txt' % b['batch_id']), encoding='utf-8') as f:
                ossz += float(f.read() or 0)
    return ossz


def plafon_ellenorzes(plafon, becs):
    """(rendben, szöveg): ELOZO_KIADAS_USD (a közös plafon alatti, másik adag mért költsége) + a mért futó összeg + a még
    be nem gyűjtött batchek beküldéskori becslése + a most beküldendő kérések kalibrált becslése <= plafon (F159, N-F27b)."""
    mert, fuggo = futo_osszeg(), fuggo_becsles()
    ossz = ELOZO_KIADAS_USD + mert + fuggo + becs
    return ossz <= plafon, ('becslés %.2f USD (manual); eddig mért %.4f USD + másik adag %.4f + függő %.2f; összesen %.2f / plafon %.2f USD'
                            % (becs, mert, ELOZO_KIADAS_USD, fuggo, ossz, plafon))


def strongok_olvas(fajl):
    """A futási lista Strongjai (Strong_padded), sorrendben, ismétlés nélkül; a thayer_szakaszok.tsv-ben szereplők."""
    ki, lattam = [], set()
    with open(fajl, encoding='utf-8') as f:
        for sor in f:
            s = sor.rstrip('\n').rstrip('\r').split('\t')[0].strip()
            if not s or s.startswith('#'):
                continue
            sp = kulcs.strong_pad(s)
            if not sp:
                raise SystemExit('hibás Strong a listában: %r' % s)
            if sp not in lattam:
                lattam.add(sp)
                ki.append(sp)
    return ki


# ---------- a futási lista ----------

def teljes_lista(ts):
    """Minden thayer_szakaszok.tsv-beli Strong a `szolista.allapot` szabályával (nem csak a motívumok gerincszavai)."""
    fs = szolista.thayer_sorok()
    ki = []
    for sp in sorted(TB.tabla_olvas()):
        szak = TB.szakaszok(sp)
        st, ok, megj = szolista.allapot(sp, szak, fs.get(sp, []))
        ki.append({'strong': sp, 'statusz': st, 'ok': ok, 'szakasz': str(len(szak)), 'karakter': str(len(TB.nezet(szak))),
                   'csoport': str(len(TB.csoportok(szak))), 'illesztes': szak[0]['illesztes'], 'motivumhely': '',
                   'megjegyzes': megj,
                   'proveniencia': 'scope=%s | forras=thayer_api_koteg.py lista (szolista.allapot) | ts=%s' % (sp, ts)})
    return ki


def lista_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_api_koteg.py lista --ts %s — a teljes Thayer futási listája (F158); kézzel nem szerkesztendő.' % ts,
           '# forras: adat/forditasok.tsv@%s + adat/thayer_szakaszok.tsv@%s' % (szolista.sha12(szolista.FORDITASOK_UT), szolista.sha12(TB.TABLA)),
           '\t'.join(szolista.FEJLEC)]
    return '\n'.join(fej + ['\t'.join(r[m] for m in szolista.FEJLEC) for r in sorok]) + '\n'


def lista_osszesito(sorok):
    import collections
    c = collections.Counter((r['statusz'], r['ok']) for r in sorok)
    return 'Strong %d; %s' % (len(sorok), ', '.join('%s/%s %d' % (s, o, n) for (s, o), n in sorted(c.items())))


def lista(ki=None, ts=None):
    ts = ts or datetime.date.today().isoformat()
    sorok = teljes_lista(ts)
    szoveg = lista_szoveg(sorok, ts)
    if ki:
        with open(ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s' % ki)
    else:
        sys.stdout.write(szoveg)
    print('# összesítő: %s' % lista_osszesito(sorok), file=sys.stderr)
    return 0


# ---------- a kérések ----------

def helyorzos_prompt(sp, csoport, darab_info):
    """A `forditas.prompt_epit` kimenete, a forrás-részben a `helyorzo_bont` ⟦n⟧ helyőrzőivel -> (prompt, hely, forras_kar)."""
    prompt = F.prompt_epit(sp, csoport, darab_info)
    tok = TB.tokenes(csoport)
    bont, hely = E.helyorzo_bont(tok)
    i = prompt.rfind(FORRAS_JEL)
    j = prompt.find(KIMENET_JEL, i)
    if i < 0 or j < 0 or prompt[i + len(FORRAS_JEL):j].strip('\n') != tok.strip('\n'):
        raise SystemExit('%s: a prompt forrás-része nem a várt helyen áll' % sp)
    return prompt[:i + len(FORRAS_JEL)] + '\n\n' + bont + '\n\n' + prompt[j:], hely, len(tok)


def kerelmek_strongra(strong):
    """[{strong, csoport, db, prompt, hely, forras_kar, kot}] csoportonként."""
    sp, szak = F.forras(strong)
    cs = TB.csoportok(szak)
    ki = []
    for i, c in enumerate(cs):
        prompt, hely, kar = helyorzos_prompt(sp, c, E.darab_info_szoveg(i, len(cs)))
        ki.append({'strong': sp, 'csoport': i + 1, 'db': len(cs), 'prompt': prompt, 'hely': hely, 'forras_kar': kar,
                   'kot': E.kotelezo_alakok_szoveg(TB.nezet(c)), 'nezet': TB.nezet(c)})
    return ki


def konnyu_strongra(strong):
    """A tervezéshez (adatblokk és prompt nélkül, gyors): [{strong, csoport, db, forras_kar, nezet}] csoportonként."""
    sp, szak = F.forras(strong)
    cs = TB.csoportok(szak)
    return [{'strong': sp, 'csoport': i + 1, 'db': len(cs), 'forras_kar': len(TB.tokenes(c)), 'nezet': TB.nezet(c)}
            for i, c in enumerate(cs)]


def terv(strongok):
    """Az 1. próbás kérések, Strong-szám szerint (a lista sorrendje)."""
    return [k for s in strongok for k in kerelmek_strongra(s)]


def ker_index(strongok):
    ki = {}
    for k in terv(strongok):
        ki.setdefault(k['strong'], []).append(k)
    return ki


def becsles_adat(allando_kar, forras_kar_osszeg, strongok_db, ut='A', effort=None):
    """(bemenet_token, kimenet_token, USD) — Batch-ár, cache nélkül; a kalibrált F27 M1 illesztés (BE_KERES, BE_KAR, KI_KERES,
    KI_KAR; manual). A kérésenkénti állandó a (szűkített) prompt állandó része karakterből; a kimenet Strongonként egy
    kérésnyi állandóval (a B-útra konzervatív felső érték)."""
    effort = effort or EFFORT
    if ut == 'B':      # csoportos kérés: a B-mérés együtthatói (F07 M0 (a)), effortonként külön kimenettel
        be = allando_kar * B_BE_ALLANDO + B_BE_KAR * forras_kar_osszeg
        ki = B_KI_KAR[effort] * forras_kar_osszeg
    else:
        be = allando_kar / ALLANDO_KAR_TOKEN + BE_KAR * forras_kar_osszeg
        ki = (KI_KERES * strongok_db + KI_KAR * forras_kar_osszeg) * A_KI_EFFORT[effort]
    return be, ki, (be * AR_BE + ki * AR_KI) / 1e6


def javito_kor_becsles(elso_kor_usd, ut):
    """A javító kör becsült költsége (USD, manual): a mért javító/1. kör költségarány × az 1. kör becslése."""
    return elso_kor_usd * JAVITO_ARANY[ut]


def allando_kar(prompt):
    """A prompt nem Strongonkénti része (szabályok, terminológia, Károli-tábla, kimenet-séma, példa) karakterben."""
    i = prompt.rfind(BEMENET_JEL)
    j = prompt.find(KIMENET_JEL, i)
    return len(prompt) - (j - i)


def becsles(ker):
    """Egy Strongos (A-stílusú) kérések becslése -> (bemenet_token, kimenet_token, USD) — manual."""
    be = ki = 0.0
    for k in ker:
        b, o, _ = becsles_adat(allando_kar(kuldendo_prompt(k)), k['forras_kar'], 1)
        be, ki = be + b, ki + o
    return be, ki, (be * AR_BE + ki * AR_KI) / 1e6


def csomagok(ker, meret=CSOMAG):
    return [ker[i:i + meret] for i in range(0, len(ker), meret)]


def uzenet(prompt):
    return [{'type': 'text', 'text': prompt}]


# ---------- a terminológia- és a Károli-tábla szűkítése (F159, követelmény 2) ----------

TERM_FEJ = '## Ideiglenes terminológia'
KAROLI_FEJ = '## Károli-rövidítéslista'
BEMENET_JEL = '## Bemenet'
KOT_JEL = 'Az e forrásban előforduló kulcsok gépi kigyűjtése:\n\n'
_TABLA = {}


def term_sorok():
    """[(angol, sor-szöveg)] — a sor-szöveg betűre azonos az `emeles.terminologia_szoveg` soraival."""
    if 'term' not in _TABLA:
        ki = []
        for r in E.tsv_dict_sorok(E.TERMINOLOGIA_UT):
            if r.get('megjegyzes'):
                ki.append((r['angol'], '- `%s` = %s (%s)' % (r['angol'], r['magyar'], r['megjegyzes'])))
            else:
                ki.append((r['angol'], '- `%s` = %s' % (r['angol'], r['magyar'])))
        _TABLA['term'] = ki
    return _TABLA['term']


def karoli_sorok():
    """[(keresett_alakok, sor-szöveg)] — a sor-szöveg betűre azonos az `emeles.karoli_szoveg` soraival; az alakok: a
    STEPBible-rövidítés, a Forrás-alakok és az angol teljes könyvnév (konkordancia/Angol_konyvnev_STEPBible_tabla.tsv)."""
    if 'karoli' not in _TABLA:
        angol = {}
        with open(os.path.join(ROOT, 'konkordancia', 'Angol_konyvnev_STEPBible_tabla.tsv'), encoding='utf-8') as f:
            next(f)
            for sor in f:
                m = sor.rstrip('\n').rstrip('\r').split('\t')
                if len(m) >= 2:
                    angol.setdefault(m[1], []).append(m[0])
        ki = []
        for r in E.tsv_dict_sorok(E.KAROLI_UT):
            rov = r['STEPBible-rövidítés']
            alakok = [rov] + [x.strip() for x in (r.get('Forrás-alakok') or '').split(',') if x.strip()] + angol.get(rov, [])
            ki.append((alakok, '- `%s` → `%s`' % (rov, r['Magyar rövidítés'])))
        _TABLA['karoli'] = ki
    return _TABLA['karoli']


def _alak_minta(alak):
    vege = r'(?![A-Za-z])' if alak[-1:].isalpha() else ''
    return re.compile(r'(?<![A-Za-z0-9])' + re.escape(alak) + vege)


def szukitett_tablak(forrasok):
    """(terminológia-szöveg, Károli-szöveg) a megadott források uniójára: csak azok a sorok, amelyek angol kulcsa
    (terminológia: `forditas_kapuk._angol_minta`, az 5. kapu illesztése; kapu=nem sorok is), illetve rövidítése / forrás-alakja /
    angol könyvneve a forrásban előfordul."""
    egy = '\n'.join(forrasok)
    term = [sor for angol, sor in term_sorok() if K._angol_minta(angol).search(egy)]
    karoli = [sor for alakok, sor in karoli_sorok() if any(_alak_minta(a).search(egy) for a in alakok)]
    return ('\n'.join(term) or '(a forrásban nincs terminológiai sor)',
            '\n'.join(karoli) or '(a forrásban nincs bibliai könyvnév)')


def szukit(prompt, forrasok):
    """A prompt terminológia- és Károli-táblája a források uniójára szűkítve; minden más bájtra azonos."""
    ti = prompt.index(TERM_FEJ)
    t0 = prompt.index('\n\n', ti) + 2
    k0 = prompt.index('\n\n' + KAROLI_FEJ, t0)
    ki = prompt.index('\n\n', k0 + 2) + 2
    ke = prompt.index('\n\n' + BEMENET_JEL, ki)
    term, karoli = szukitett_tablak(forrasok)
    return prompt[:t0] + term + prompt[k0:ki] + karoli + prompt[ke:]


def kuldendo_prompt(k):
    """Az A-stílusú (egy Strongos) kérés szövege: a prompt, szűkítve (SZUKIT), a kérés saját forrására."""
    return szukit(k['prompt'], [k['nezet']]) if SZUKIT else k['prompt']


# ---------- szaraz ----------

def szaraz(strongok):
    t0 = time.time()
    ker = terv(strongok)
    kar = sum(k['forras_kar'] for k in ker)
    be, ki, usd = becsles(ker)
    csom = csomagok(ker)
    print('%d Strong, %d kérés (%d többcsoportos Strong), forrás %d karakter (tokenes bemenet)' % (
        len(strongok), len(ker), len({k['strong'] for k in ker if k['db'] > 1}), kar))
    print('promptok: összesen %d karakter, átlag %d' % (sum(len(kuldendo_prompt(k)) for k in ker),
                                                     sum(len(kuldendo_prompt(k)) for k in ker) // max(1, len(ker))))
    print('becslés (manual; F27 M1 illesztés: bemenet %d token/kérés + %.3f token/forráskarakter, kimenet %d token/kérés + %.3f '
          'token/forráskarakter): bemenet %.0f token, kimenet %.0f token' % (BE_KERES, BE_KAR, KI_KERES, KI_KAR, be, ki))
    jav = javito_kor_becsles(usd, 'A')
    print('költség Batch-áron, cache nélkül (egy Strongos út, effort %s): első kör %.2f + javító kör %.2f (mért arány %.2f) = %.2f USD '
          '(becslés, manual); plafon %.2f USD' % (EFFORT, usd, jav, JAVITO_ARANY['A'], usd + jav, PLAFON_USD))
    print('csomagok: %d × ~%d kérés' % (len(csom), CSOMAG))
    if ker:
        print('max_tokens: %d–%d; modell %s, effort %s; (%.1f mp)' % (
            min(max_tokens_kerelemre(k['forras_kar']) for k in ker), max(max_tokens_kerelemre(k['forras_kar']) for k in ker),
            MODELL, EFFORT, time.time() - t0))
    return 0


# ---------- beküldés ----------

def batchek(cimke=None, kor=None):
    return [b for b in AK.tsv_olvas(ut('batchek.tsv'))
            if (cimke is None or b['cimke'] == cimke) and (kor is None or int(b['kor']) == kor)]


def bekuldott_cidek():
    ki = set()
    for f in os.listdir(ut()) if os.path.isdir(ut()) else []:
        if f.startswith('csomag_') and f.endswith('.txt'):
            with open(ut(f), encoding='utf-8') as h:
                ki.update(x.strip() for x in h if x.strip())
    return ki


def ujra_naplo(batch_id, cimke, kor, csomag, db):
    AK.tsv_hozzaad(ut('batchek.tsv'), BATCH_FEJLEC, {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'batch_id': batch_id, 'cimke': cimke, 'kor': kor,
        'csomag': csomag, 'kerelmek_db': db})


def bekuld(strongok, cimke, plafon=None, hivo=None):
    plafon = PLAFON_USD if plafon is None else plafon
    if plafon <= 0:
        print('MEGÁLLÁS: a plafon %.2f USD — beküldés csak a felhasználó által megadott plafonnal (--plafon) lehetséges' % plafon,
              file=sys.stderr)
        return 3
    hivo = hivo or AK.http
    kesz = bekuldott_cidek() | {r['custom_id'] for r in jsonl_olvas(ut('valaszok.jsonl'))}
    # a már beküldött vagy megválaszolt kérések (pl. a `bbekuld` B-csoportjai) kimaradnak: nincs kettős költség
    ker = [k for k in terv(strongok) if custom_id(k['strong'], k['csoport'], 1) not in kesz]
    csom = csomagok(ker)
    if not csom:
        print('minden csomag beküldve')
        return 0
    index = 0
    cs = csom[index]
    becs = becsles(cs)[2]
    rendben, szoveg = plafon_ellenorzes(plafon, becs)
    print('csomag %d/%d: %d kérés; %s' % (index + 1, len(csom), len(cs), szoveg))
    if not rendben:
        print('MEGÁLLÁS: a mért futó összeg + a becsült költség a plafon (%.2f USD) fölött lenne' % plafon, file=sys.stderr)
        return 3
    kerelmek = [{'custom_id': custom_id(k['strong'], k['csoport'], 1),
                 'params': kerelem_params([{'role': 'user', 'content': uzenet(kuldendo_prompt(k))}], k['forras_kar'])} for k in cs]
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    os.makedirs(ut(), exist_ok=True)
    sorszam = 1 + len([f for f in os.listdir(ut()) if f.startswith('csomag_') and f[7:9].isdigit()])
    with open(ut('csomag_%02d.txt' % sorszam), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek))
    with open(ut('becsles_%s.txt' % b['id']), 'w', encoding='utf-8', newline='\n') as f:
        f.write('%.4f' % becs)
    ujra_naplo(b['id'], cimke, 1, sorszam, len(kerelmek))
    print('batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


def allapot(cimke, hivo=None):
    hivo = hivo or AK.http
    ki = []
    for b in batchek(cimke):
        r = hivo('GET', '/v1/messages/batches/%s' % b['batch_id'])
        print('%s kör=%s csomag=%s: %s %s' % (b['batch_id'], b['kor'], b['csomag'], r.get('processing_status'),
                                             json.dumps(r.get('request_counts'))))
        ki.append(r.get('processing_status'))
    return ki


# ---------- begyűjtés ----------

def begyujt(cimke, hivo=None):
    hivo = hivo or AK.http
    kesz = {s['custom_id'] for s in jsonl_olvas(ut('valaszok.jsonl'))}
    uj = 0
    for b in batchek(cimke):
        sorok = AK.eredmeny_sorok(b['batch_id'], hivo)
        if sorok is None:
            print('%s: még nem ért véget' % b['batch_id'])
            continue
        rekordok, napl = [], []
        for s in sorok:      # custom_id szerint, soha nem pozíció szerint
            cid = s['custom_id']
            if cid in kesz or not (custom_id_bont(cid) or CID_B.match(cid) or CID_BJ.match(cid)):
                continue
            res = s.get('result', {})
            msg = res.get('message') or {}
            usage = msg.get('usage', {})
            rekordok.append({'custom_id': cid, 'tipus': res.get('type'), 'modell': msg.get('model', ''),
                             'stop': msg.get('stop_reason'), 'usage': usage, 'szoveg': AK.uzenet_szoveg(msg),
                             'hiba': json.dumps(res.get('error'), ensure_ascii=False) if res.get('error') else '',
                             'batch_id': b['batch_id']})
            napl.append((cid, msg.get('model', ''), usage, msg.get('stop_reason') or res.get('type'), koltseg(usage)))
            kesz.add(cid)
            if CID_B.match(cid) or CID_BJ.match(cid):      # a B-kérés (és a B-javító kérés) válasza Strongonkénti szintetikus rekordokra bomlik
                rekordok.extend(b_szetbont(rekordok[-1]))
        jsonl_hozzaad(ut('valaszok.jsonl'), rekordok)
        futo = futo_osszeg()
        for cid, mod, u, stop, c in napl:
            futo += c
            AK.tsv_hozzaad(ut('futasnaplo.tsv'), NAPLO_FEJLEC, {
                'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'custom_id': cid, 'modell': mod,
                'effort': EFFORT, 'bemenet_token': u.get('input_tokens', 0), 'cache_olvasas': u.get('cache_read_input_tokens', 0),
                'cache_iras': u.get('cache_creation_input_tokens', 0), 'kimenet_token': u.get('output_tokens', 0),
                'stop_reason': stop, 'koltseg_usd': '%.6f' % c, 'futo_osszeg_usd': '%.6f' % futo})
        uj += len(rekordok)
        if not os.path.exists(ut('begyujtve_%s.txt' % b['batch_id'])):      # az újrafutás nem írja felül a darabszámot
            with open(ut('begyujtve_%s.txt' % b['batch_id']), 'w', encoding='utf-8', newline='\n') as f:
                f.write('%d\n' % len(rekordok))
        print('%s: %d új válasz' % (b['batch_id'], len(rekordok)))
    print('új válasz összesen: %d; futó összeg %.4f USD' % (uj, futo_osszeg()))
    return 0


# ---------- kapuzás ----------

def strong_allapot(sp, kerelmek, valaszok):
    """Egy Strong utolsó próbájának feldolgozása -> dict {strong, proba, allapot, ...} (a bdb_api_koteg szerint)."""
    proba = 1
    cidek = {k['csoport']: custom_id(sp, k['csoport'], 1) for k in kerelmek}
    if all(custom_id(sp, k['csoport'], 2) in valaszok for k in kerelmek):
        proba = 2
        cidek = {k['csoport']: custom_id(sp, k['csoport'], 2) for k in kerelmek}
    if not all(c in valaszok for c in cidek.values()):
        return {'strong': sp, 'proba': proba, 'allapot': 'varakozik'}
    reszek, kivetel, nyers, hibak, modellek, stop_hibas = [], [], [], [], set(), False
    for k in kerelmek:
        v = valaszok[cidek[k['csoport']]]
        modellek.add(v['modell'])
        nyers.append(v['szoveg'])
        if v['tipus'] != 'succeeded' or v['stop'] in ('refusal', 'max_tokens'):
            hibak.append('a kérés nem adott használható választ (%s%s)' % (v['tipus'] if v['tipus'] != 'succeeded' else v['stop'],
                                                                           ': ' + v['hiba'][:120] if v['hiba'] else ''))
            stop_hibas = stop_hibas or v['stop'] == 'refusal'      # csak a refusal végleges; az errored/expired újrapróbálható
            continue
        fh, biz = json_valasz(v['szoveg'])
        if fh is None:
            hibak.append(biz)
            continue
        ismeretlen = sorted({int(n) for n in E.HELYORZO.findall(fh) if not 1 <= int(n) <= len(k['hely'])})
        if ismeretlen:
            hibak.append('ismeretlen helyőrző: %s (a csoportban 1–%d van)' % (ismeretlen, len(k['hely'])))
            continue
        vissza, hiany, tobb = E.helyorzo_visszaallit(fh, k['hely'])
        if hiany or tobb:
            hibak.append('helyőrző-hiba: hiányzó %s, többször használt %s' % (hiany, tobb))
        reszek.append(vissza)
        kivetel.extend(x for x in biz if x not in kivetel)
    base = {'strong': sp, 'proba': proba, 'modellek': sorted(modellek), 'nyers': nyers, 'kivetel': kivetel}
    if hibak:
        return dict(base, allapot='kapuhiba' if stop_hibas else 'javitando', hibak=hibak, vegleges='', valtozasok=[])
    szoveg = ' '.join(reszek)
    if '\t' in szoveg or '\n' in szoveg:
        szoveg = re.sub(r'\s*[\t\n]+\s*', ' ', szoveg)
    szak = TB.szakaszok(sp)
    try:
        vegleges, valt, eredm, ok = F.utofeldolgoz(sp, szak, szoveg, kivetel)
    except Exception as e:      # pl. a szakasztokenek hibája: javítandó, nem leállás
        return dict(base, allapot='javitando', hibak=['feldolgozási hiba: %s' % str(e)[:200]], vegleges='', valtozasok=[])
    bukott = [(n, r) for n, e, r in eredm if e == 'SERTES']
    return dict(base, allapot='kesz' if ok else 'javitando', hibak=['%s: %s' % b for b in bukott], vegleges=vegleges,
                valtozasok=[list(v) for v in valt], kapu_bukott=[n for n, _ in bukott])


def kapuz(strongok):
    ker = ker_index(strongok)
    valaszok = {r['custom_id']: r for r in jsonl_olvas(ut('valaszok.jsonl'))}
    ki, szaml = [], {}
    for sp, ks in ker.items():
        r = strong_allapot(sp, ks, valaszok)
        szaml[r['allapot']] = szaml.get(r['allapot'], 0) + 1
        ki.append(r)
    os.makedirs(ut(), exist_ok=True)
    with open(ut('kapu_eredmeny.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for r in ki:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    p1 = [r for r in ki if r['proba'] == 1 and r['allapot'] != 'varakozik']
    print('Strong: %d; %s' % (len(ki), ', '.join('%s %d' % kv for kv in sorted(szaml.items()))))
    print('1. próbán kapuhibás/javítandó: %d / %d feldolgozott' % (sum(1 for r in p1 if r['allapot'] != 'kesz'), len(p1)))
    return 0


# ---------- javító batch ----------

def javito_kerelmek(elozo, strongok):
    """(kerelmek, meta, bj) a kapun bukott / hiányzó Strongok javító kéréseiből (F07 M0 (b)). A kicsi és közepes Strongok
    csoportosan (B-javító kérés, `J001-p2` …: a közös szabály-rész egyszer, Strongonként a forrás, az előző nyers válasz és a
    kapu hibaüzenete; a hiányzó válaszú Strongnál friss fordítás), a nagyok és a többcsoportosak egyenként (A-stílus: az előző
    válasz assistant-fordulóként). A már beküldött javító kérés nem megy újra. -> (kerelmek, [becslés-tételek], új bj csoportok)."""
    kesz = bekuldott_cidek()
    index = ker_index([r['strong'] for r in elozo])
    kerelmek, tetelek, uj_bj = [], [], {}
    konnyu = {r['strong']: kategoria(konnyu_strongra(r['strong'])) for r in elozo}
    kicsik = [r for r in elozo if konnyu[r['strong']] != 'nagy' and custom_id(r['strong'], 1, 2) not in kesz]
    for r in elozo:
        if konnyu[r['strong']] != 'nagy':
            continue
        for k in index[r['strong']]:
            cid = custom_id(k['strong'], k['csoport'], 2)
            if cid in kesz:
                continue
            nyers = r['nyers'][k['csoport'] - 1] if k['csoport'] - 1 < len(r['nyers']) else ''
            msgs = [{'role': 'user', 'content': uzenet(kuldendo_prompt(k))}]
            if nyers.strip():
                msgs += [{'role': 'assistant', 'content': nyers},
                         {'role': 'user', 'content': javito_uzenet(r['hibak'])}]
            kerelmek.append({'custom_id': cid, 'params': kerelem_params(msgs, k['forras_kar'])})
            tetelek.append(('A', [k], nyers))
    if kicsik:
        lista = [r['strong'] for r in kicsik]
        hibak = {r['strong']: r['hibak'] for r in kicsik}
        nyers = {r['strong']: (r['nyers'][0] if r['nyers'] else '') for r in kicsik}
        cs, _ = b_csoportok_epit(lista, {s: konnyu_strongra(s) for s in lista})
        regi = bj_csoportok_olvas()
        for i, (_, tagok) in enumerate(cs.items()):
            nev = 'J%03d' % (len(regi) + i + 1)
            uj_bj[nev] = tagok
            ks = [kerelmek_strongra(s)[0] for s in tagok]
            prompt = b_prompt(ks, [(nyers[s], hibak[s]) for s in tagok])
            kerelmek.append({'custom_id': '%s-p2' % nev, 'params': kerelem_params(
                [{'role': 'user', 'content': uzenet(prompt)}], 0, b_max_tokens(ks))})
            tetelek.append(('B', ks, [nyers[s] for s in tagok], prompt))
    return kerelmek, tetelek, uj_bj


def javito_becsles(tetelek):
    """A javító kérések becslése (USD, manual): A-tétel: az egy Strongos kérés becslése + a bemenetben az előző válasz;
    B-tétel: a B-kérés becslése + a bemenetben az előző válaszok és a hibaüzenetek. A javító kimenet a teljes Strongot adja vissza."""
    usd = 0.0
    for t in tetelek:
        if t[0] == 'A':
            k, nyers = t[1][0], t[2]
            be, ki, _ = becsles_adat(allando_kar(kuldendo_prompt(k)), k['forras_kar'], 1)
            be += len(nyers) / ALLANDO_KAR_TOKEN
        else:
            ks, nyers, prompt = t[1], t[2], t[3]
            be, ki, _ = becsles_adat(allando_kar(prompt), sum(k['forras_kar'] for k in ks), len(ks), 'B')
            be += (sum(len(x) for x in nyers) + 200 * len(ks)) / ALLANDO_KAR_TOKEN
        usd += (be * AR_BE + ki * AR_KI) / 1e6
    return usd


def javit(strongok, cimke, plafon=None, hivo=None):
    plafon = PLAFON_USD if plafon is None else plafon
    hivo = hivo or AK.http
    lista = set(strongok)      # csak a megadott listából javít (egy részlistával a javító kör szűkíthető)
    elozo = [r for r in jsonl_olvas(ut('kapu_eredmeny.jsonl')) if r['allapot'] == 'javitando' and r['proba'] == 1 and r['strong'] in lista]
    if not elozo:
        print('nincs javítandó Strong')
        return 0
    kerelmek, tetelek, uj_bj = javito_kerelmek(elozo, strongok)
    if not kerelmek:
        print('a javító kérések már be vannak küldve')
        return 0
    becs = javito_becsles(tetelek) * 1.3
    rendben, szoveg = plafon_ellenorzes(plafon, becs)
    print('javító batch: %d kérés (%d B-javító, %d egyenkénti); %s' % (
        len(kerelmek), len(uj_bj), len(kerelmek) - len(uj_bj), szoveg))
    if plafon <= 0 or not rendben:
        print('MEGÁLLÁS: a plafon fölött lenne (vagy nincs megadva)', file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    os.makedirs(ut(), exist_ok=True)
    if uj_bj:
        osszes = dict(bj_csoportok_olvas(), **uj_bj)      # előbb olvas, aztán nyit írásra
        with open(ut('bj_csoportok.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(osszes, f, ensure_ascii=False, indent=0)
    with open(ut('csomag_javito.txt'), 'a', encoding='utf-8', newline='\n') as f:
        f.write(''.join(custom_id(s, 1, 2) + '\n' for tagok in uj_bj.values() for s in tagok))
        f.write(''.join(k['custom_id'] + '\n' for k in kerelmek if CID.match(k['custom_id'])))
    with open(ut('becsles_%s.txt' % b['id']), 'w', encoding='utf-8', newline='\n') as f:
        f.write('%.4f' % becs)
    ujra_naplo(b['id'], cimke, 2, 'javito', len(kerelmek))
    print('javító batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


# ---------- rögzítés ----------

def bukott_sor(sp, r, modell, datum):
    kapu = ','.join(r.get('kapu_bukott') or []) or 'api'
    ok = ' | '.join(r['hibak'])[:600].replace('\t', ' ').replace('\n', ' ')
    return '\t'.join([sp, kapu, ok, 'API Batch, %d. próba' % r['proba'], modell, datum,
                      'scope=%s | forras=thayer_api_koteg.py rogzit | ts=%s' % (sp, datum)])


def munka_ir(munka_ut, strongok, uj_sorok):
    """A munkatábla frissítése: a megnevezett Thayer-Strongok régi sorai kiesnek, az újak a végére kerülnek; minden más sor
    (a `#` megjegyzések, a fejléc, a többi Strong) bájtra azonos, ezt írás előtt ellenőrzi."""
    if os.path.exists(munka_ut):
        with open(munka_ut, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        if not sorok or sorok.pop() != '':
            raise SystemExit('a munkatábla nem sortöréssel végződik')
    else:
        sorok = ['# F132 munkatábla (adat/forditasok.tsv sémája) — beírás előtt; írja: python eszkozok/thayer_api_koteg.py rogzit',
                 '\t'.join(F.FEJLEC)]

    def torlendo(s):
        m = s.split('\t')
        return len(m) > 1 and m[0] == F.SZOTAR and m[1] in strongok
    marad = [s for s in sorok if not torlendo(s)]
    uj = marad + ['\t'.join(str(r.get(m, '')) for m in F.FEJLEC) for r in uj_sorok]
    if uj[:len(marad)] != marad or [s for s in uj[len(marad):] if torlendo(s) is False]:
        raise SystemExit('a munkatábla többi sora eltér — megállok')
    with open(munka_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(uj) + '\n')


def rogzit(strongok, datum=None, szaraz_futas=False, munka_ut=None, bukott_ut=None):
    """A kapun átment Strongok szakaszsorai a munkatáblába (a többi sor bájtra azonos); a kétszer bukottak (és a refusal) a bukottak.tsv-be."""
    munka_ut, bukott_ut = munka_ut or MUNKA_TABLA, bukott_ut or BUKOTT_UT
    eredm = jsonl_olvas(ut('kapu_eredmeny.jsonl'))
    datum = datum or datetime.date.today().strftime('%Y.%m.%d')
    _, term_verzio = E.terminologia_szoveg()
    rogzitett, uj_sorok, bukottak = [], [], []
    for r in eredm:
        sp = r['strong']
        if r['allapot'] == 'kesz':
            allapot, mod = modell_allapot(r['modellek'])        # a válasz ténylegesen futott modellnevéből
            eredet = ''
            if EREDET:      # F07 M0 (f): a #159 mérő batchéből származó, újrakapuzott sor: az adag és a batch-azonosító(k)
                batchek_ = []
                for rek in jsonl_olvas(ut('valaszok.jsonl')):
                    if rek['custom_id'] in (custom_id(sp, 1, p_) for p_ in range(1, r['proba'] + 1)) and rek.get('batch_id') not in batchek_:
                        batchek_.append(rek.get('batch_id'))
                eredet = '%s; batch: %s' % (EREDET, ', '.join(str(b_) for b_ in batchek_))
            megj = '; '.join(x for x in ('API Batch (effort=%s, %d. próba)' % (EFFORT, r['proba']), eredet,
                                         ('terminológia-kivétel (bizonytalan_feloldasok): ' + ', '.join(r['kivetel'])) if r['kivetel'] else '') if x)
            uj_sorok += F.szakasz_sorok(sp, TB.szakaszok(sp), r['vegleges'], allapot, mod, datum, term_verzio, megj)
            E.kisnagybetu_naplo(sp, [tuple(v) for v in r['valtozasok'] if v[0].startswith('5_kisnagybetu')])
            rogzitett.append(sp)
        elif r['allapot'] == 'kapuhiba' or (r['allapot'] == 'javitando' and r['proba'] == 2):
            bukottak.append((sp, r))
    print('rögzítendő: %d Strong; bukott-listára: %d' % (len(rogzitett), len(bukottak)))
    if szaraz_futas:
        return 0
    if rogzitett:
        munka_ir(munka_ut, set(rogzitett), uj_sorok)
    if bukottak:
        letezo = set()
        if os.path.exists(bukott_ut):
            letezo = {tuple(x.rstrip('\n').rstrip('\r').split('\t')[:4]) for x in open(bukott_ut, encoding='utf-8')}
        uj_fajl = not os.path.exists(bukott_ut)
        irt = []
        with open(bukott_ut, 'a', encoding='utf-8', newline='\n') as f:
            if uj_fajl:
                f.write('\t'.join(BUKOTT_FEJLEC) + '\n')
            for sp, r in bukottak:
                sor = bukott_sor(sp, r, ','.join(r.get('modellek') or []), datum)
                if tuple(sor.split('\t')[:4]) in letezo:      # az újrafuttatott rogzit nem duplikál
                    continue
                f.write(sor + '\n')
                irt.append(sp)
        print('bukott-listára: %s' % (', '.join(irt) or '(már rajta volt)'))
    return 0


def beir(strongok, allapot, datum=None, megjegyzes=None, regi_elavult=False, kezi_felulir=False, kezi_marad=False, **kw):
    return F.beir(strongok, allapot, datum, megjegyzes, regi_elavult, kezi_felulir, kezi_marad, **kw)


# ---------- B-út: kérésenként több Strong (F159; a bdb_api_koteg.py B-útja szerint) ----------

def kategoria(konnyu):
    """'kicsi' (< KICSI_HATAR forráskarakter), 'kozepes' (< NAGY_HATAR) vagy 'nagy' (>= NAGY_HATAR vagy több csoportos)."""
    if len(konnyu) > 1 or konnyu[0]['forras_kar'] >= NAGY_HATAR:
        return 'nagy'
    return 'kicsi' if konnyu[0]['forras_kar'] < KICSI_HATAR else 'kozepes'


def b_csoportok_epit(strongok, konnyu_index, b_db=None, b_kar=None):
    """A Strongok sorrendben, legfeljebb b_db Strong és b_kar forráskarakter kérésenként; -> ({nev: [strong]}, [egyedi Strongok]).
    A nagy és a többcsoportos Strongok egyedi (A-stílusú) kérések."""
    b_db, b_kar = b_db or B_DB, b_kar or B_KAR
    csoportok, egyedi, cur, kar = {}, [], [], 0
    for s in strongok:
        ks = konnyu_index[s]
        if kategoria(ks) == 'nagy':
            egyedi.append(s)
            continue
        if cur and (len(cur) >= b_db or kar + ks[0]['forras_kar'] > b_kar):
            csoportok['B%03d' % (len(csoportok) + 1)] = cur
            cur, kar = [], 0
        cur.append(s)
        kar += ks[0]['forras_kar']
    if cur:
        csoportok['B%03d' % (len(csoportok) + 1)] = cur
    return csoportok, egyedi


def kot_unio(kotok):
    sorok = []
    for k in kotok:
        for l in k.split('\n'):
            if l.startswith('- ') and l not in sorok:
                sorok.append(l)
    return '\n'.join(sorok) if sorok else kotok[0]


def b_strong_blokk(k, i, n):
    """Egy Strong B-kérésbeli része: az egy Strongos prompt bemeneti részének (adatblokk + forrás) betűhű szövege."""
    p = k['prompt']
    c = p.rfind(BEMENET_JEL)
    return '### %d/%d. szócikk\n%s' % (i + 1, n, p[c + len(BEMENET_JEL):p.index(KIMENET_JEL, c)].strip('\n'))


def javito_resz(hibak):
    """Egy Strong javító blokkja a B-javító kérésben: a kapu hibái + a javítási utasítás (a `bdb_api_koteg.javito_uzenet` szövege
    a JSON-formára vonatkozó záró mondat nélkül: az a kérés végén, a Kimenet szakaszban egyszer áll)."""
    return B.javito_uzenet(hibak).rsplit(' Add vissza', 1)[0]


def b_prompt(ks, javito=None):
    """Több Strong egy kérésben (`javito`: Strongonként (előző nyers válasz, kapu-hibák) — a B-stílusú javító kör, F07 M0 (b)). A prompt v5.1 szabálytartalma változatlan (ugyanabból a `forditas.prompt_epit`-ből): a közös
    szabály-rész egyszer áll, a kötelező-alak lista a Strongok uniója, a terminológia- és a Károli-tábla a Strongok forrásának
    uniójára szűkítve (SZUKIT); utána Strongonként az adatblokk és a forrás; a válasz Strongonként egy objektumot
    tartalmazó JSON-tömb."""
    p0 = ks[0]['prompt']
    j = p0.find(KOT_JEL) + len(KOT_JEL)
    cut = p0.rfind(BEMENET_JEL)
    kimenet = p0.index(KIMENET_JEL, cut)
    if p0[j:j + len(ks[0]['kot'])] != ks[0]['kot']:
        raise SystemExit('a kötelező-alak lista nem a várt helyen áll: %s' % ks[0]['strong'])
    farok = p0[j + len(ks[0]['kot']):cut]
    json0 = p0.index('```json', kimenet)
    json1 = p0.index('```\n', json0 + 7) + 4
    blokk = [b_strong_blokk(k, i, len(ks)) for i, k in enumerate(ks)]
    if javito:      # Strongonként az előző nyers válasz és a kapu hibaüzenete; a hiányzó válaszú Strongnál friss fordítás
        for i, (nyers, hibak) in enumerate(javito):
            if (nyers or '').strip():
                blokk[i] += ('\n\n#### Az előző kísérlet kimenete erre a szócikkre\n\n```json\n%s\n```\n\n#### Javítandó\n\n%s'
                             % (nyers.strip(), javito_resz(hibak)))
            else:
                blokk[i] += ('\n\n#### Javítandó\n\nErre a szócikkre az előző kísérletben nem érkezett használható válasz: '
                             'fordítsd le a fenti szabályok szerint.')
    bemenet = (('## Bemenet\n\nEgyetlen kérésben %d Thayer-szócikk érkezik' % len(ks))
               + (', mindegyik az előző kísérlet kapuellenőrzésén elbukott vagy hiányzott; a javítandó szócikkeknél a hibák '
                  'felsorolása áll' if javito else '') + '. Mindegyiket külön, önmagában álló szövegként fordítsd a '
               'fenti szabályok szerint: a `⟪n⟫` határtokenek és a `⟦n⟧` helyőrzők az adott szócikken belül számozottak, szócikkek '
               'között nem keverheted, nem vonhatod össze és nem viheted át őket. A kötelező terminológiai alakok listája az összes '
               'szócikk forrására vonatkozik.\n\n') + '\n\n'.join(blokk) + '\n\n'
    kim = ('## Kimenet\n\nKIZÁRÓLAG a következő JSON-sémájú választ add, semmi mást (sem Markdown code fence,\n'
           'sem magyarázat a JSON előtt/után): egyetlen JSON-tömb, szócikkenként pontosan egy objektum, a fenti sorrendben '
           '(a `strong` a szócikk Strong-száma):\n\n```json\n[{"strong": "<a szócikk Strong-száma>", "forditas_hu": '
           '"<a hű magyar fordítás>", "bizonytalan_feloldasok": ["<rövidítés, ha van bizonytalan feloldás>"]}, ...]\n```\n')
    ki = p0[:j] + kot_unio([k['kot'] for k in ks]) + farok + bemenet + kim + p0[json1:]
    return szukit(ki, [k['nezet'] for k in ks]) if SZUKIT else ki


def b_max_tokens(ks):
    return int(min(64000, max(16000, 3 * sum(k['forras_kar'] * KI_KAR + KI_KERES for k in ks) + 4000)))


def b_becsles_konnyu(strongok, konnyu_ix, allando):
    """(bemenet_token, kimenet_token, USD) egy B-kérésre prompt-építés nélkül: az állandó rész karaktere `allando` (manual)."""
    kar = sum(konnyu_ix[s][0]['forras_kar'] for s in strongok)
    return becsles_adat(allando, kar, len(strongok), 'B')


def b_csoportok_olvas():
    with open(ut('b_csoportok.json'), encoding='utf-8') as f:
        return json.load(f)


def bj_csoportok_olvas():
    f = ut('bj_csoportok.json')
    if not os.path.exists(f):
        return {}
    with open(f, encoding='utf-8') as h:
        return json.load(h)


def konnyu_index(strongok):
    return {s: konnyu_strongra(s) for s in strongok}


def b_lista(strongok):
    valasz = {r['custom_id'] for r in jsonl_olvas(ut('valaszok.jsonl'))}
    kuldott = bekuldott_cidek()
    return [x for x in strongok if custom_id(x, 1, 1) not in valasz and custom_id(x, 1, 1) not in kuldott]


def b_csoportok_betolt(strongok):
    f = ut('b_csoportok.json')
    if os.path.exists(f):
        return b_csoportok_olvas()
    lista = b_lista(strongok)
    cs, egyedi = b_csoportok_epit(lista, konnyu_index(lista))
    if egyedi:
        print('%d Strong nem B-úti (nagy vagy többcsoportos): egyenként kerül sorra' % len(egyedi), file=sys.stderr)
    os.makedirs(ut(), exist_ok=True)
    with open(f, 'w', encoding='utf-8', newline='\n') as h:
        json.dump(dict(cs, egyedi=egyedi), h, ensure_ascii=False, indent=0)
    return dict(cs, egyedi=egyedi)


def json_tomb(szoveg):
    t = re.sub(r'^```(?:json)?\s*|\s*```$', '', (szoveg or '').strip())
    i = t.find('[')
    if i < 0:
        return []
    try:
        d, _ = json.JSONDecoder().raw_decode(t[i:])
    except ValueError:
        return []
    return [x for x in d if isinstance(x, dict)] if isinstance(d, list) else []


def b_szetbont(rek):
    """A B-kérés nyers válasza -> Strongonkénti szintetikus válaszrekordok (`<strong>-c1-p1`), hogy a kapuz/javit/rogzit
    ugyanúgy dolgozzon, mint az egy Strongos kéréseknél. Hiányzó objektum -> üres szöveg (javítandó)."""
    m = CID_B.match(rek['custom_id']) or CID_BJ.match(rek['custom_id'])
    javito = bool(CID_BJ.match(rek['custom_id']))
    nev = ('J' if javito else 'B') + m.group('n')
    proba = int(m.group('proba'))
    strongok = (bj_csoportok_olvas() if javito else b_csoportok_olvas())[nev]
    mapa = {}
    if rek['tipus'] == 'succeeded' and rek['stop'] not in ('refusal', 'max_tokens'):
        for x in json_tomb(rek['szoveg']):
            mapa[kulcs.strong_pad(str(x.get('strong', '')))] = x
    return [{'custom_id': custom_id(sp, 1, proba), 'tipus': rek['tipus'], 'modell': rek['modell'], 'stop': rek['stop'], 'usage': {},
             'szoveg': json.dumps(mapa[sp], ensure_ascii=False) if sp in mapa else '', 'hiba': rek['hiba'],
             'batch_id': rek['batch_id'], 'forras': nev} for sp in strongok]


def b_szaraz(strongok):
    t0 = time.time()
    lista = b_lista(strongok)
    ix = konnyu_index(lista)
    cs, egyedi = b_csoportok_epit(lista, ix)
    # az állandó rész karaktere: néhány minta-kérés tényleges (szűkített) B-promptjából; a többire az átlaguk
    allandok = []
    for nev, csop in list(cs.items())[:3]:
        allandok.append(allando_kar(b_prompt([kerelmek_strongra(s)[0] for s in csop])))
    allando = sum(allandok) / len(allandok) if allandok else 0
    be = ki = usd = 0.0
    kat = {'kicsi': 0, 'kozepes': 0, 'nagy': 0}
    for s in lista:
        kat[kategoria(ix[s])] += 1
    for nev, csop in cs.items():
        b, k, u = b_becsles_konnyu(csop, ix, allando)
        be, ki, usd = be + b, ki + k, usd + u
    # az egyedi (nagy) Strongok A-stílusú kérései
    egyedi_kar = sum(k['forras_kar'] for s in egyedi for k in ix[s])
    egyedi_ker = sum(len(ix[s]) for s in egyedi)
    egy_allando = allando_kar(kuldendo_prompt(kerelmek_strongra(egyedi[0])[0])) if egyedi else 0
    eb, ek, eu = becsles_adat(egy_allando * egyedi_ker, egyedi_kar, egyedi_ker)
    jb, je = javito_kor_becsles(usd, 'B'), javito_kor_becsles(eu, 'A')
    kar = sum(ix[s][0]['forras_kar'] for g in cs.values() for s in g)
    print('B-út: %d Strong (kicsi %d, közepes %d), %d B-kérés (átlag %.1f Strong, %.0f forráskarakter); nagy/többcsoportos '
          '(egyenként): %d Strong, %d kérés' % (len(lista) - len(egyedi), kat['kicsi'], kat['kozepes'], len(cs),
                                              (len(lista) - len(egyedi)) / max(1, len(cs)), kar / max(1, len(cs)),
                                              len(egyedi), egyedi_ker))
    print('szűkített állandó rész: ~%.0f karakter (~%.0f token) / B-kérés; a szűkítés előtti: %d karakter (%d token, F27 M1 mért)' % (
        allando, allando / ALLANDO_KAR_TOKEN, ALLANDO_REF_KAR, BE_KERES))
    print('B-kérések becslése (manual): bemenet %.2f M token, kimenet %.2f M token, %.2f USD' % (be / 1e6, ki / 1e6, usd))
    if egyedi:
        print('egyedi kérések becslése (manual): bemenet %.2f M token, kimenet %.2f M token, %.2f USD' % (eb / 1e6, ek / 1e6, eu))
    print('első kör: %.2f USD (B %.2f + egyedi %.2f); javító kör: %.2f USD (B-javító %.2f + egyenkénti %.2f; mért arányok %.2f / %.2f)' % (
        usd + eu, usd, eu, jb + je, jb, je, JAVITO_ARANY['B'], JAVITO_ARANY['A']))
    print('összesen: %.2f USD (becslés, manual; effort %s, Batch-ár, cache nélkül); mért eddig %.4f USD; plafon %.2f USD; (%.1f mp)' % (
        usd + eu + jb + je, EFFORT, futo_osszeg(), PLAFON_USD, time.time() - t0))
    return 0


def b_bekuld(strongok, cimke, db, plafon=None, hivo=None):
    plafon = PLAFON_USD if plafon is None else plafon
    if plafon <= 0:
        print('MEGÁLLÁS: a plafon %.2f USD — beküldés csak megadott plafonnal (--plafon) lehetséges' % plafon, file=sys.stderr)
        return 3
    hivo = hivo or AK.http
    cs = b_csoportok_betolt(strongok)
    kuldott = bekuldott_cidek()
    nevek = [n for n in cs if n != 'egyedi' and custom_id(cs[n][0], 1, 1) not in kuldott]
    if db:
        nevek = nevek[:db]
    if not nevek:
        print('nincs beküldendő B-csoport')
        return 0
    kerelmek, becs = [], 0.0
    for n in nevek:
        ks = [kerelmek_strongra(s)[0] for s in cs[n]]
        prompt = b_prompt(ks)
        becs += becsles_adat(allando_kar(prompt), sum(k['forras_kar'] for k in ks), len(ks), 'B')[2]
        kerelmek.append({'custom_id': '%s-p1' % n, 'params': kerelem_params(
            [{'role': 'user', 'content': uzenet(prompt)}], 0, b_max_tokens(ks))})
    rendben, szoveg = plafon_ellenorzes(plafon, becs)
    print('B-csomag: %d kérés (%d Strong); %s' % (len(kerelmek), sum(len(cs[n]) for n in nevek), szoveg))
    if not rendben:
        print('MEGÁLLÁS: a mért futó összeg + a becsült költség a plafon (%.2f USD) fölött lenne' % plafon, file=sys.stderr)
        return 3
    b = hivo('POST', '/v1/messages/batches', {'requests': kerelmek})
    for n in nevek:
        with open(ut('csomag_%s.txt' % n), 'w', encoding='utf-8', newline='\n') as f:
            f.write(''.join(custom_id(s, 1, 1) + '\n' for s in cs[n]))
    with open(ut('becsles_%s.txt' % b['id']), 'w', encoding='utf-8', newline='\n') as f:
        f.write('%.4f' % becs)
    ujra_naplo(b['id'], cimke, 1, 'B:' + nevek[0] + '-' + nevek[-1], len(kerelmek))
    print('B-batch beküldve: %s (%d kérés)' % (b['id'], len(kerelmek)))
    return 0


# ---------- main ----------

def main(argv=None):
    global MUNKA, PLAFON_USD, ELOZO_KIADAS_USD, EREDET, EFFORT, B_DB, B_KAR, SZUKIT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('parancs', nargs='?', choices=['lista', 'szaraz', 'bszaraz', 'bbekuld', 'bekuld', 'allapot', 'begyujt', 'kapuz', 'javit', 'rogzit', 'beir'])
    ap.add_argument('--adag', type=int, default=None)
    ap.add_argument('--strongok', default=None, help='a futási lista fájlja (soronként egy Strong)')
    ap.add_argument('--cimke', default=None)
    ap.add_argument('--munka', default=None, help='munkamappa (felülírja a forditas/thayer_api/adag<N>/-t; száraz futáshoz a repón kívül)')
    ap.add_argument('--plafon', type=float, default=0.0, help='USD; alapérték 0: a beküldés tilos')
    ap.add_argument('--effort', default='high', choices=EFFORTOK, help='a kérések effortja (a futásnapló oszlopa is)')
    ap.add_argument('--b-db', type=int, default=B_DB, help='B-út: Strong / kérés (15–25)')
    ap.add_argument('--b-kar', type=int, default=B_KAR, help='B-út: forráskarakter / kérés felső határa')
    ap.add_argument('--db', type=int, default=0, help='bbekuld: az első DB beküldetlen B-kérés (0: mind)')
    ap.add_argument('--elozo-kiadas', type=float, default=0.0, help='a közös plafon alatt futó másik adag mért költsége (USD)')
    ap.add_argument('--nincs-szukites', action='store_true', help='a terminológia- és a Károli-tábla szűkítése nélkül')
    ap.add_argument('--ki', default=None)
    ap.add_argument('--ts', default=None)
    ap.add_argument('--allapot', default=None, choices=E.ALLAPOTOK)
    ap.add_argument('--datum', default=None)
    ap.add_argument('--megjegyzes', default=None)
    ap.add_argument('--regi-elavult', action='store_true')
    ap.add_argument('--kezi-felulir', action='store_true')
    ap.add_argument('--kezi-marad', action='store_true')
    ap.add_argument('--eredet', default='', help='rogzit: az eredet szövege a megjegyzésben (pl. a #159 mérő batchéből, újrakapuzva, adag1591)')
    ap.add_argument('--commit', action='store_true', help='bekuld/begyujt/javit/rogzit után a munkamappa commitja és pusholása (api_koteg.git_mentes)')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        import teszt_thayer_api_koteg
        return teszt_thayer_api_koteg.futtat()
    if not a.parancs:
        print('HIBA: parancs kell', file=sys.stderr)
        return 2
    if a.parancs == 'lista':
        return lista(a.ki, a.ts)
    if not a.adag or not a.strongok:
        print('HIBA: --adag és --strongok kell', file=sys.stderr)
        return 2
    MUNKA = a.munka or os.path.join(MUNKA_GYOKER, 'adag%d' % a.adag)
    PLAFON_USD = a.plafon
    EREDET = a.eredet
    ELOZO_KIADAS_USD, EFFORT, B_DB, B_KAR, SZUKIT = a.elozo_kiadas, a.effort, a.b_db, a.b_kar, not a.nincs_szukites
    cimke = a.cimke or 'adag%d' % a.adag
    strongok = strongok_olvas(a.strongok)
    if a.parancs == 'szaraz':
        return szaraz(strongok)
    if a.parancs == 'bszaraz':
        return b_szaraz(strongok)
    kod = futtat_parancs(a, strongok, cimke)
    if a.commit and kod == 0 and a.parancs in ('bekuld', 'bbekuld', 'begyujt', 'kapuz', 'javit', 'rogzit', 'beir'):
        git_mentes('F159: Thayer API-köteg — %s (%s)' % (a.parancs, cimke), a.parancs)
    return kod


def git_mentes(uzenet, parancs):
    """A parancs kimenetének commitja és pusholása (`api_koteg.git_mentes`; csak a megnevezett utak)."""
    if os.path.splitdrive(os.path.abspath(MUNKA))[0] != os.path.splitdrive(ROOT)[0] or not os.path.abspath(MUNKA).startswith(os.path.abspath(ROOT)):
        print('GIT-FIGYELMEZTETÉS: a munkamappa a repón kívül van, nincs mit commitolni', file=sys.stderr)
        return 'nincs_valtozas'
    utak = [os.path.relpath(MUNKA, ROOT).replace(os.sep, '/')]
    if parancs in ('rogzit', 'beir'):
        utak += [os.path.relpath(x, ROOT).replace(os.sep, '/') for x in (MUNKA_TABLA, BUKOTT_UT, E.KISNAGYBETU_UT, E.FORDITASOK_UT)
                 if os.path.exists(x)]
    return AK.git_mentes(uzenet, utak)


def futtat_parancs(a, strongok, cimke):
    if a.parancs == 'bekuld':
        return bekuld(strongok, cimke, a.plafon)
    if a.parancs == 'bbekuld':
        return b_bekuld(strongok, cimke, a.db, a.plafon)
    if a.parancs == 'allapot':
        allapot(cimke)
        return 0
    if a.parancs == 'begyujt':
        return begyujt(cimke)
    if a.parancs == 'kapuz':
        return kapuz(strongok)
    if a.parancs == 'javit':
        return javit(strongok, cimke, a.plafon)
    if a.parancs == 'rogzit':
        return rogzit(strongok, a.datum)
    if not a.allapot:
        print('HIBA: beir --allapot kell', file=sys.stderr)
        return 2
    n = beir(strongok, a.allapot, a.datum, a.megjegyzes, a.regi_elavult, a.kezi_felulir, a.kezi_marad)
    print('adat/forditasok.tsv: %d sor változott/új (%d Strong)' % (n, len(strongok)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
