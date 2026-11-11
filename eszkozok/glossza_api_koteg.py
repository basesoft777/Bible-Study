#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F161 — a lexikonlapok rövid szótári glosszáinak (UBS DNTG, UBS DBH, TBESG) fordítási lánca.

A `thayer_api_koteg.py` (B-út) és a `bdb_api_koteg.py` mintájára: rögzített prompt (`forditas/prompt_glossza_v1.md`),
egységenkénti mankó (kötelező terminológia, Károli-alakok, elfogadott egyenértékek), hálózat nélküli kérés-összeállítás,
kapuk, legfeljebb egy javító kör, rögzítés és beírás az `adat/forditasok.tsv`-be. A kérés egyszerre megy a Batch API-ra
(`bekuld`) és az előfizetői subagentnek (`prompt` → a subagent válasza → `bevesz`): a kérés bájtra azonos, mert mindkét út
a `szaraz` által írt `keresek.jsonl`-ből olvas, és a `bekuld` a fájlt csak akkor küldi, ha az újraépített kéréssel egyezik.

Bemenet: a #121 `lista` kimenete (`glossza_lexikon_forditas.py lista --id <ID>`, a lap által keresett pontos kulcs és
forrásszöveg). Ebből a `szotar` ∈ {UBS_DNTG, UBS_DBH, TBESG} és `allapot` = hianyzik sorok az egységek; a forrás a
`glossza_lexikon_forditas.forras_szoveg` feloldójából újra kiolvasva, hash-sel összevetve.

  szaraz   --lista F --munka D   egységek (egysegek.tsv) és kérések (keresek.jsonl) hálózat nélkül; kérés-, egység-,
                                 karakterszám, becslés (manual)
  prompt   --munka D --cid C --ki F   egy kérés user-szövege fájlba (a subagent ezt kapja, szó szerint)
  bekuld   --munka D --plafon USD [--kor 1|2]   a kör kéréseinek beküldése (plafon nélkül tilos)
  allapot  --munka D             a batchek állapota
  begyujt  --munka D             a kész batchek válaszai a valaszok.jsonl-be, költségnapló
  bevesz   --munka D --cid C --valasz F --modell M   a subagent válasza a valaszok.jsonl-be (M: a ténylegesen futott modell)
  kapuz    --munka D             válasz → JSON → helyőrző-visszaállítás → javítóréteg → kapuk → kapu_eredmeny.jsonl
  javit    --munka D             a kapun bukott egységek javító kérései (keresek_p2.jsonl; a kapu hibaüzenetével; egyszer)
  rogzit   --munka D [--datum]   az átment egységek sorai (rogzitett.tsv, a forditasok.tsv sémája); a kétszer bukottak a
                                 bukottak.tsv-be
  beir     --munka D [--jelzes-atnezve] [--felulir]   a rogzitett.tsv sorai az adat/forditasok.tsv-be
  --onteszt                      hálózat nélküli önteszt (a teljes teszt: teszt_glossza_api_koteg.py)

A munkakönyvtár a repón kívül van (a `--munka` kötelező, és nem lehet a repóban). Kilépési kódok: 0 rendben; 2 hibás
paraméter vagy előfeltétel; 3 a plafon megállít; 4/5 az `api_koteg.py` szerint. TSV: split('\\t'), '\\t'.join(); csv nincs.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time

ITT = os.path.dirname(os.path.abspath(__file__))
for _u in (os.path.join(ITT, 'karoli_strong'), ITT):
    if _u not in sys.path:
        sys.path.insert(0, _u)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import api_koteg as AK  # noqa: E402  (REST-hívó, kulcs: PARDES_API_KEY, tsv_olvas / tsv_hozzaad, eredmeny_sorok)
import bdb_api_koteg as B  # noqa: E402  (csak a tiszta segédek: koltseg, jsonl, modell_allapot, NAPLO/BATCH_FEJLEC)
import emeles as E  # noqa: E402  (helyőrzők, terminológia, kötelező alakok, a forditasok.tsv fejléce)
import forditas_kapuk as K  # noqa: E402  (a meglévő fordítási kapuk, módosítás nélkül)
import forditas_vedelem as FV  # noqa: E402  (F182, F31: érvényes fordítás nem fordul újra)
import glossza_lexikon_forditas as GLF  # noqa: E402  (a #121 feloldója és mankója)
import olvasoi_kapu as OK  # noqa: E402  (az olvasói kapu tiltásai: BELSO, ANGOL_SZO, ANGOL_FUNKCIO)

ROOT = os.path.dirname(ITT)
PROMPT_UT = os.path.join(ROOT, 'forditas', 'prompt_glossza_v2.md')      # v2: a v1 + a UBS-definíció kiegészítő szabálya
PROMPT_VERZIO = 'glossza v2'
MENETJEL = 'F161'                  # a megjegyzés eleje (a #121 `menet_sorai` / `egyenertek_tabla` kizárója)
SZOTARAK = ('UBS_DNTG', 'UBS_DBH', 'TBESG')
SZOTAR_NEV = {'UBS_DNTG': 'UBS DNTG', 'UBS_DBH': 'UBS DBH', 'TBESG': 'TBESG (rövid jelentés)'}
BELSO_KIVETEL = ('belső szó (gerinc)',)   # a lap prózájának belső szava; a szótári glosszában köznapi magyar szó (gerinc = backbone)
MEZO_NEV = {'glosszak_hu': 'glossza', 'definicio_hu': 'definíció'}
UBS_JEL = re.compile(r'\{L:[^{}]*\}|[=≈◄►]')   # a UBS saját jelei és hivatkozás-jelölése (prompt v2, kiegészítő szabály)
FORRAS_FAJL = {'UBS_DNTG': 'konkordancia/UBS_DNTG_jelentesek.tsv', 'UBS_DBH': 'konkordancia/UBS_DBH_jelentesek.tsv',
               'TBESG': 'konkordancia/TBESG.txt'}
MODELL = AK.MODELL                 # a kérésben kért modell; a rögzítés a válasz tényleges modellnevét írja
EFFORT = 'high'
MAX_TOKENS = 16000
EGYSEG_KERES = 20                  # egység / kérés felső határa (a B-út 15–25-ös sávjában)
KAROLI_DB = 6                      # a mankó Károli-alakjai (a leggyakoribbak)
EGYENERTEK_DB = 3
# Becslés (manual, mérés nélkül): bemenet ~2,4 karakter/token; kimenet egységenként ~350 token gondolkodással.
KAR_TOKEN = 2.4
KI_EGYSEG = 350
EGYSEG_FEJLEC = ['id', 'keres', 'szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forras',
                 'helyorzok']
BUKOTT_FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'kapu', 'ok', 'probalkozas',
                 'modell', 'datum']
CID = re.compile(r'^G(?P<n>\d{3})-p(?P<proba>[12])$')
FEJLEC = E.FORDITASOK_FEJLEC
_HG = re.compile('[%s]' % E._HG_KAR)
KIZAR_GATOLO = ('6_hosszarany',)   # JELZES-kapu; a rövid glosszán nem értelmezhető, de az eredményben marad
MUNKA = None
# a subagent-út jelölése a megjegyzésben (orkesztrátor, 2026-11-03): a kérés ugyanaz, a futtató környezet más
SUBAGENT_EREDET = ('Code-session (előfizetői keret), general-purpose subagent %s, a kérés szó szerint (a `prompt` fájljából beolvasva, '
                   'a válasz fájlba írásának utasításával); eltérés az API-tól: Claude Code alap rendszerutasítás, effort/max_tokens '
                   'nem állítható')


def ut(*r):
    return os.path.join(MUNKA, *r)


def sha1(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def custom_id(n, proba):
    return 'G%03d-p%d' % (n, proba)


def munka_beallit(d):
    global MUNKA
    if not d:
        raise SystemExit('a --munka kötelező (repón kívüli könyvtár)')
    d = os.path.abspath(d)
    if os.path.normcase(d + os.sep).startswith(os.path.normcase(ROOT + os.sep)):
        raise SystemExit('a --munka a repón kívüli könyvtár legyen: %s' % d)
    MUNKA = d
    return d


def tsv_ir(utvonal, fejlec, sorok):
    with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(fejlec) + '\n')
        for r in sorok:
            cellak = [str(r.get(m, '')) for m in fejlec]
            if any('\t' in c or '\n' in c for c in cellak):
                raise SystemExit('tab vagy sortörés egy cellában: %s' % cellak[:5])
            f.write('\t'.join(cellak) + '\n')


def tsv_be(utvonal):
    if not os.path.exists(utvonal):
        return []
    with open(utvonal, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


# ---------- egységek ----------

def egysegek_listabol(lista_ut, cache=None):
    """A #121 lista sorai közül a lánc egységei, a forrás a mai feloldóból (hash-sel összevetve)."""
    cache = cache if cache is not None else {}
    ki, hibak = [], []
    for r in tsv_be(lista_ut):
        if r.get('szotar') not in SZOTARAK or r.get('allapot') != 'hianyzik' or r.get('mezo') not in MEZO_NEV:
            continue
        if r['szotar'] == 'TBESG' and r.get('jelentes_szam') != 'rovid':
            continue            # a TBESG teljes szócikke nem glossza (a lánc csak a rövid jelentést veszi fel)
        forras = GLF.forras_szoveg(r, cache=cache)
        if forras is None:
            hibak.append('%s: a forrás nem oldható fel' % '|'.join(r[k] for k in E.FORDITASOK_FEJLEC[:5]))
            continue
        if r.get('forras_hash') and r['forras_hash'] != sha1(forras):
            hibak.append('%s: a lista forras_hash-e nem a mai forrásé (a lista elavult)' % '|'.join(
                r[k] for k in E.FORDITASOK_FEJLEC[:5]))
            continue
        ki.append({k: r[k] for k in E.FORDITASOK_FEJLEC[:5]} | {'forras': forras, 'forras_hash': sha1(forras)})
    if hibak:
        raise SystemExit('a lista nem használható:\n  ' + '\n  '.join(hibak))
    ki.sort(key=lambda e: (SZOTARAK.index(e['szotar']), e['strong'], e['entry_id'], e['jelentes_szam'], e['mezo']))
    for i, e in enumerate(ki, 1):
        e['id'] = 'e%03d' % i
        bont, hely = E.helyorzo_bont(e['forras'])
        e['forras_hely'], e['helyorzok'] = bont, hely
    return ki


def keresekre(egysegek, db=EGYSEG_KERES):
    """Mohó csoportosítás: azonos (szótár, Strong) egységei egy kérésbe kerülnek, kérésenként legfeljebb `db` egység."""
    csoportok, akt = [], []
    for kulcs in dict.fromkeys((e['szotar'], e['strong']) for e in egysegek):
        cs = [e for e in egysegek if (e['szotar'], e['strong']) == kulcs]
        if akt and len(akt) + len(cs) > db:
            csoportok.append(akt)
            akt = []
        while len(cs) > db:        # a `db`-nél nagyobb Strong több kérésre bomlik
            csoportok.append(cs[:db])
            cs = cs[db:]
        akt.extend(cs)
    if akt:
        csoportok.append(akt)
    for n, cs in enumerate(csoportok, 1):
        for e in cs:
            e['keres'] = n
    return csoportok


# ---------- kontextus és mankó ----------

_CTX = {}


def _konkordancia(fajl):
    if fajl not in _CTX:
        _CTX[fajl] = GLF.tsv_sorok(os.path.join(GLF.KONKORDANCIA, fajl))
    return _CTX[fajl]


def _tbesg_lemma():
    if 'TBESG_lemma' not in _CTX:
        idx = {}
        with open(os.path.join(GLF.KONKORDANCIA, 'TBESG.txt'), encoding='utf-8', errors='replace') as f:
            for l in f:
                c = l.rstrip('\n').split('\t')
                if len(c) >= 7 and re.match(r'^G\d{4}', c[0]):
                    idx.setdefault(c[0][:5], c[3].strip())
        _CTX['TBESG_lemma'] = idx
    return _CTX['TBESG_lemma']


def _forditasok():
    if 'forditasok' not in _CTX:
        _CTX['forditasok'] = {tuple(r[k] for k in FEJLEC[:5]): r for r in GLF.tsv_sorok(GLF.FORDITASOK)
                              if r.get('allapot') != 'elavult'}
    return _CTX['forditasok']


def kontextus(e):
    """[(címke, szöveg)] — a fordítást segítő, nem fordítandó adatok."""
    sz, st = e['szotar'], e['strong']
    ki = []
    if sz in ('UBS_DNTG', 'UBS_DBH'):
        fajl = 'UBS_DNTG_jelentesek.tsv' if sz == 'UBS_DNTG' else 'UBS_DBH_jelentesek.tsv'
        r = next((x for x in _konkordancia(fajl) if x['strong'] == st and x['lexid'] == e['entry_id']
                  and (sz == 'UBS_DBH' or x['entry_kod'] == e['jelentes_szam'])), None)
        if r:
            ki.append(('Címszó', '%s (%s)' % (r['lemma'], st)))
            if sz == 'UBS_DNTG':
                ki.append(('Louw–Nida-domén', '%s (%s)' % (r['entry_kod'], r['domen'])))
            elif r.get('domen'):
                ki.append(('Domén', r['domen']))
            masik = {'glosszak_hu': ('definicio_hu', 'definicio_rovid', 'Definíció'),
                     'definicio_hu': ('glosszak_hu', 'glosszak', 'Glosszák')}.get(e['mezo'])
            if masik and r.get(masik[1]) and r[masik[1]] != GLF.EM_DASH:
                ki.append(('%s (angol)' % masik[2], r[masik[1]]))
                hu = _forditasok().get((sz, st, e['entry_id'], e['jelentes_szam'], masik[0]))
                if hu:
                    ki.append(('%s (magyar, %s)' % (masik[2], 'jóváhagyott' if hu['allapot'] == 'kezi' else 'gépi, nem lektorált'),
                               hu['forditas_hu']))
    elif sz == 'TBESG':
        lemma = _tbesg_lemma().get(st)
        if lemma:
            ki.append(('Címszó', '%s (%s)' % (lemma, st)))
    return ki


def manko(e, tabla, karoli_cache):
    """[(címke, szöveg)]: a kötelező terminológia, a Károli-alakok és az elfogadott egyenértékek (a #121 mankójából)."""
    ki = []
    kot = E.kotelezo_alakok(e['forras'])
    if kot:
        ki.append(('kötelező terminológia', ', '.join('`%s` → `%s`' % x for x in kot)))
    st = e['strong']
    if st not in karoli_cache:
        karoli_cache[st] = GLF.karoli_alakok_strongra(st)
    if karoli_cache[st]:
        ki.append(('Károli-alakok', ', '.join('%s×%d' % x for x in karoli_cache[st].most_common(KAROLI_DB))))
    ee = []
    for elem in GLF.elemek(e['forras']):
        t = tabla.get(elem.lower())
        if t:
            ee.append('%s → %s' % (elem, ', '.join('%s×%d' % x for x in t.most_common(EGYENERTEK_DB))))
    if ee:
        ki.append(('elfogadott egyenértékek', '; '.join(ee)))
    return ki


def egyseg_blokk(e, tabla, karoli_cache):
    sorok = ['### %s' % e['id'], 'Szótár: %s' % SZOTAR_NEV[e['szotar']], 'Mező: %s' % MEZO_NEV[e['mezo']]]
    sorok += ['%s: %s' % x for x in kontextus(e)]
    m = manko(e, tabla, karoli_cache)
    sorok += ['Mankó — %s: %s' % x for x in m] if m else ['Mankó: (nincs)']
    sorok.append('Fordítandó (angol): %s' % e['forras_hely'])
    return '\n'.join(sorok)


def _sablon():
    with open(PROMPT_UT, encoding='utf-8') as f:
        return f.read().split(E.PROMPT_JELOLO, 1)[1].lstrip('\n')


def terminologia_blokk(egysegek):
    """A terminológia azon sorai, amelyeknek az angol kulcsa a kérés valamelyik forrásában áll (az 5. kapu illesztésével)."""
    term = list(E.tsv_dict_sorok(E.TERMINOLOGIA_UT))
    forras = '\n'.join(e['forras'] for e in egysegek)
    ki = []
    for r in term:
        if K._sajat_talalatok(r['angol'], forras, term):
            s = ('- `%s` = %s (%s)' % (r['angol'], r['magyar'], r['megjegyzes'])) if r.get('megjegyzes') else (
                '- `%s` = %s' % (r['angol'], r['magyar']))
            if s not in ki:
                ki.append(s)
    return '\n'.join(ki) or '(a kérés forrásaiban nincs terminológiai kulcs)'


def prompt_epit(egysegek, tabla, karoli_cache):
    return (_sablon().replace('{{TERMINOLOGIA}}', terminologia_blokk(egysegek))
            .replace('{{EGYSEGEK}}', '\n\n'.join(egyseg_blokk(e, tabla, karoli_cache) for e in egysegek)))


def kerelem_params(uzenetek):
    return {'model': MODELL, 'max_tokens': MAX_TOKENS, 'thinking': {'type': 'adaptive'},
            'output_config': {'effort': EFFORT}, 'messages': uzenetek}


def user(szoveg):
    return {'role': 'user', 'content': [{'type': 'text', 'text': szoveg}]}


def kerelmek_epit(egysegek):
    tabla = GLF.egyenertek_tabla(kizar=(MENETJEL,))
    karoli_cache = {}
    ki = []
    for n, cs in enumerate(keresekre(egysegek), 1):
        ki.append({'custom_id': custom_id(n, 1), 'params': kerelem_params([user(prompt_epit(cs, tabla, karoli_cache))])})
    return ki


def jsonl_szoveg(kerelmek):
    return ''.join(json.dumps(k, ensure_ascii=False, sort_keys=True) + '\n' for k in kerelmek)


def egysegek_ir(egysegek):
    tsv_ir(ut('egysegek.tsv'), EGYSEG_FEJLEC, [dict(e, helyorzok=json.dumps(e['helyorzok'], ensure_ascii=False))
                                               for e in egysegek])


def egysegek_be():
    ki = []
    for r in tsv_be(ut('egysegek.tsv')):
        r['helyorzok'] = json.loads(r['helyorzok'])
        r['keres'] = int(r['keres'])
        r['forras_hely'] = E.helyorzo_bont(r['forras'])[0]
        ki.append(r)
    return ki


def becsles(kerelmek, egyseg_db):
    be = sum(len(json.dumps(k['params']['messages'], ensure_ascii=False)) for k in kerelmek) / KAR_TOKEN
    ki = egyseg_db * KI_EGYSEG
    return be, ki, (be * B.AR_BE + ki * B.AR_KI) / 1e6


def szaraz(lista_ut):
    t0 = time.time()
    egys = egysegek_listabol(lista_ut)
    if not egys:
        print('nincs fordítandó egység (UBS_DNTG / UBS_DBH / TBESG, allapot=hianyzik)')
        return 0
    ker = kerelmek_epit(egys)
    os.makedirs(ut(), exist_ok=True)
    egysegek_ir(egys)
    with open(ut('keresek.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(jsonl_szoveg(ker))
    be, ki, usd = becsles(ker, len(egys))
    db = {}
    for e in egys:
        db[e['szotar']] = db.get(e['szotar'], 0) + 1
    print('%d egység (%s), %d kérés; forrás %d karakter; prompt %d karakter' % (
        len(egys), ', '.join('%s %d' % x for x in db.items()), len(ker), sum(len(e['forras']) for e in egys),
        sum(len(k['params']['messages'][0]['content'][0]['text']) for k in ker)))
    print('becslés (manual, mérés nélkül): bemenet %.0f token, kimenet %.0f token; %.3f USD Batch-áron, cache nélkül' % (be, ki, usd))
    print('kérések: %s (prompt %s; modell %s, effort %s; %.1f mp)' % (ut('keresek.jsonl'), PROMPT_VERZIO, MODELL, EFFORT,
                                                                  time.time() - t0))
    return 0


def kerelmek_be(kor):
    fajl = ut('keresek.jsonl' if kor == 1 else 'keresek_p2.jsonl')
    return B.jsonl_olvas(fajl), fajl


def prompt_ki(cid, ki_ut):
    """A kérés user-szövege (kör 2-nél: a teljes üzenetlánc szövegesen) fájlba, a subagentnek."""
    kor = 2 if cid.endswith('-p2') else 1
    k = next((k for k in kerelmek_be(kor)[0] if k['custom_id'] == cid), None)
    if k is None:
        raise SystemExit('nincs ilyen kérés: %s' % cid)
    uz = k['params']['messages']
    if len(uz) != 1 or uz[0]['role'] != 'user' or len(uz[0]['content']) != 1:
        raise SystemExit('%s: nem egyetlen user-üzenet — a subagent nem kaphatja szó szerint' % cid)
    szoveg = uz[0]['content'][0]['text']
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('%s: %d karakter -> %s' % (cid, len(szoveg), ki_ut))
    return 0


# ---------- beküldés, begyűjtés, bevétel ----------

def futo_osszeg():
    return sum(float(s['koltseg_usd'] or 0) for s in AK.tsv_olvas(ut('futasnaplo.tsv')))


def valaszok():
    return {r['custom_id']: r for r in B.jsonl_olvas(ut('valaszok.jsonl'))}


def bekuldott():
    return {c for b in AK.tsv_olvas(ut('batchek.tsv')) for c in (b.get('cidek') or '').split(',') if c}


def bekuld(kor, plafon, hivo=None):
    if not plafon or plafon <= 0:
        print('MEGÁLLÁS: beküldés csak a felhasználó által megadott plafonnal (--plafon USD)', file=sys.stderr)
        return 3
    ker, fajl = kerelmek_be(kor)
    friss = jsonl_szoveg(kerelmek_epit(egysegek_be()) if kor == 1 else javito_kerelmek()[0])
    with open(fajl, encoding='utf-8') as f:
        if f.read() != friss:
            print('MEGÁLLÁS: a %s nem a mai adatokból épülő kérés (futtasd újra: %s)' % (
                os.path.basename(fajl), 'szaraz' if kor == 1 else 'javit'), file=sys.stderr)
            return 2
    kesz = bekuldott() | set(valaszok())
    ker = [k for k in ker if k['custom_id'] not in kesz]
    if not ker:
        print('nincs beküldendő kérés')
        return 0
    becs = becsles(ker, sum(1 for e in egysegek_be() if any(('### %s\n' % e['id']) in k['params']['messages'][0]['content'][0]['text']
                                                             for k in ker)))[2]
    ossz = futo_osszeg() + becs
    print('%d kérés; becslés %.3f USD (manual) + eddig mért %.4f = %.3f / plafon %.2f USD' % (len(ker), becs, futo_osszeg(), ossz, plafon))
    if ossz > plafon:
        print('MEGÁLLÁS: a plafon fölött', file=sys.stderr)
        return 3
    hivo = hivo or AK.http
    b = hivo('POST', '/v1/messages/batches', {'requests': ker})
    AK.tsv_hozzaad(ut('batchek.tsv'), ['ts', 'batch_id', 'kor', 'kerelmek_db', 'cidek'], {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'batch_id': b['id'], 'kor': kor,
        'kerelmek_db': len(ker), 'cidek': ','.join(k['custom_id'] for k in ker)})
    print('batch beküldve: %s (%d kérés)' % (b['id'], len(ker)))
    return 0


def allapot(hivo=None):
    hivo = hivo or AK.http
    for b in AK.tsv_olvas(ut('batchek.tsv')):
        r = hivo('GET', '/v1/messages/batches/%s' % b['batch_id'])
        print('%s kör=%s: %s %s' % (b['batch_id'], b['kor'], r.get('processing_status'), json.dumps(r.get('request_counts'))))
    return 0


def _naplo(cid, modell, usage, stop, eredet):
    c = B.koltseg(usage)
    AK.tsv_hozzaad(ut('futasnaplo.tsv'), B.NAPLO_FEJLEC + ['eredet'], {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()), 'custom_id': cid, 'modell': modell,
        'effort': EFFORT, 'bemenet_token': usage.get('input_tokens', 0), 'cache_olvasas': usage.get('cache_read_input_tokens', 0),
        'cache_iras': usage.get('cache_creation_input_tokens', 0), 'kimenet_token': usage.get('output_tokens', 0),
        'stop_reason': stop, 'koltseg_usd': '%.6f' % c, 'futo_osszeg_usd': '%.6f' % (futo_osszeg() + c), 'eredet': eredet})


def begyujt(hivo=None):
    hivo = hivo or AK.http
    kesz = set(valaszok())
    uj = 0
    for b in AK.tsv_olvas(ut('batchek.tsv')):
        sorok = AK.eredmeny_sorok(b['batch_id'], hivo)
        if sorok is None:
            print('%s: még nem ért véget' % b['batch_id'])
            continue
        for s in sorok:      # custom_id szerint, soha nem pozíció szerint
            cid = s['custom_id']
            if cid in kesz or not CID.match(cid):
                continue
            res = s.get('result', {})
            msg = res.get('message') or {}
            B.jsonl_hozzaad(ut('valaszok.jsonl'), [{
                'custom_id': cid, 'tipus': res.get('type'), 'modell': msg.get('model', ''), 'stop': msg.get('stop_reason'),
                'usage': msg.get('usage', {}), 'szoveg': AK.uzenet_szoveg(msg), 'eredet': 'api:' + b['batch_id'],
                'hiba': json.dumps(res.get('error'), ensure_ascii=False) if res.get('error') else ''}])
            _naplo(cid, msg.get('model', ''), msg.get('usage', {}), msg.get('stop_reason') or res.get('type'), 'api')
            kesz.add(cid)
            uj += 1
    print('új válasz: %d; futó összeg %.4f USD' % (uj, futo_osszeg()))
    return 0


def bevesz(cid, valasz_ut, modell):
    """A subagent (előfizetői keret) válasza. A modell a ténylegesen futott modell neve (a subagent saját környezetéből)."""
    if not CID.match(cid):
        raise SystemExit('hibás custom_id: %s' % cid)
    if not modell or not re.match(r'^claude-[a-z0-9.-]+$', modell):
        raise SystemExit('a --modell a ténylegesen futott modell teljes neve legyen (pl. claude-sonnet-5-5)')
    kor = 2 if cid.endswith('-p2') else 1
    if cid not in {k['custom_id'] for k in kerelmek_be(kor)[0]}:
        raise SystemExit('nincs ilyen kérés: %s' % cid)
    if cid in valaszok():
        raise SystemExit('%s: már van válasz' % cid)
    with open(valasz_ut, encoding='utf-8') as f:
        szoveg = f.read()
    B.jsonl_hozzaad(ut('valaszok.jsonl'), [{'custom_id': cid, 'tipus': 'succeeded', 'modell': modell, 'stop': 'end_turn',
                                            'usage': {}, 'szoveg': szoveg, 'eredet': 'subagent', 'hiba': ''}])
    _naplo(cid, modell, {}, 'end_turn', 'subagent')
    print('%s: bevéve (%s, subagent, %d karakter)' % (cid, modell, len(szoveg)))
    return 0


# ---------- kapuzás ----------

def valasz_bont(szoveg):
    """-> ({id: (forditas_hu, [bizonytalan])}, hiba) — a modell JSON-válasza."""
    t = re.sub(r'^```(?:json)?\s*|\s*```$', '', (szoveg or '').strip())
    i = t.find('{')
    if i < 0:
        return {}, 'a válasz nem JSON-objektum'
    try:
        d, _ = json.JSONDecoder().raw_decode(t[i:])
    except ValueError as ex:
        return {}, 'a válasz JSON-ja hibás (%s)' % str(ex)[:80]
    if not isinstance(d.get('egysegek'), list):
        return {}, 'a válaszban nincs `egysegek` lista'
    ki, hibak = {}, []
    for x in d['egysegek']:
        if not isinstance(x, dict) or not isinstance(x.get('id'), str):
            hibak.append('azonosító nélküli elem')
            continue
        if x['id'] in ki:
            hibak.append('%s kétszer szerepel' % x['id'])
            continue
        fh = x.get('forditas_hu')
        biz = [str(b) for b in (x.get('bizonytalan_feloldasok') or []) if isinstance(b, str)]
        ki[x['id']] = (fh if isinstance(fh, str) else None, biz)
    return ki, '; '.join(hibak)


def _angol_maradek(forras, hu):
    """A forrás latin betűs (≥ 4 betűs) szava szó szerint a fordításban — angol maradék."""
    hu_szavak = {w.lower() for w in re.findall(r'[A-Za-zÀ-ɏ]+', hu)}
    return sorted({w for w in re.findall(r'[A-Za-z]{4,}', forras) if w.lower() in hu_szavak and not w[0].isupper()})


def egyseg_kapuk(e, hu, bizonytalan):
    """-> (végleges, változások, [(kapu, eredmény, részlet)], átment). A javítóréteg a #132-é (kis/nagybetű-csere)."""
    eredm = []
    if not isinstance(hu, str) or not hu.strip():
        return None, [], [('0_json', 'SERTES', 'a `forditas_hu` hiányzik vagy üres')], False
    hu = hu.strip()
    if '\t' in hu or '\n' in hu:
        return None, [], [('0_json', 'SERTES', 'tab vagy sortörés a fordításban')], False
    vissza, hiany, tobb = E.helyorzo_visszaallit(hu, e['helyorzok'])
    hely = 'RENDBEN'
    if hiany or tobb or '⟦' in vissza:
        hely = 'SERTES'
        eredm.append(('0_helyorzo', 'SERTES', 'hiányzó helyőrző: %s; többször: %s' % (hiany, tobb)))
    else:
        eredm.append(('0_helyorzo', 'RENDBEN', ''))
    vegleges, csere = K.terminologia_kisnagybetu_csere(e['forras'], vissza, bizonytalan_lista=list(bizonytalan))
    valt = [('5_kisnagybetu %s -> %s (%s)' % (alak, kot, angol), db) for angol, alak, kot, db in csere]
    for nev, er, resz in K.kapuk_futtat(e['szotar'], e['forras'], vegleges, bizonytalan=bizonytalan, strong=e['strong']):
        eredm.append((nev, er, resz))
    if e['mezo'] == 'glosszak_hu':
        n_f = len([x for x in e['forras'].split(';') if x.strip()])
        n_h = len([x for x in vegleges.split(';') if x.strip()])
        eredm.append(('G1_elemszam', 'RENDBEN' if n_f == n_h else 'SERTES',
                      '' if n_f == n_h else 'a forrás %d elemű, a fordítás %d elemű' % (n_f, n_h)))
    if e['szotar'] in ('UBS_DNTG', 'UBS_DBH'):
        jf, jh = sorted(UBS_JEL.findall(e['forras'])), sorted(UBS_JEL.findall(vegleges))
        eredm.append(('G5_ubs_jelek', 'RENDBEN' if jf == jh else 'SERTES', '' if jf == jh else
                      'a UBS-jelek / {L:…} jelölések nem a forráséi: forrás %s, fordítás %s' % (jf, jh)))
    jelolo = re.compile(r'\{L:[^{}]*\}')         # a jelölésben álló név nem angol maradék (prompt v2)
    t = _HG.sub(' ', jelolo.sub(' ', vegleges))
    am = [m.group(0) for m in OK.ANGOL_SZO.finditer(t)] + OK.ANGOL_FUNKCIO.findall(t) + _angol_maradek(jelolo.sub(' ', e['forras']), t)
    eredm.append(('G2_angol', 'SERTES' if am else 'RENDBEN', ('angol maradék: ' + ', '.join(am)) if am else ''))
    bj = [nev + ': ' + rx.search(vegleges).group(0) for rx, nev in OK.BELSO if nev not in BELSO_KIVETEL and rx.search(vegleges)]
    eredm.append(('G3_belso', 'SERTES' if bj else 'RENDBEN', '; '.join(bj)))
    eredm.append(('G4_egyenes_idezojel', 'SERTES' if '"' in vegleges else 'RENDBEN', 'egyenes " a fordításban' if '"' in vegleges else ''))
    ok = hely == 'RENDBEN' and K.atment([x for x in eredm if x[0] not in KIZAR_GATOLO]) and all(
        er != 'SERTES' for n, er, _ in eredm if n.startswith('G') or n.startswith('0_'))
    return vegleges, valt, eredm, ok


def manko_jelzes(e, vegleges, tabla, karoli_cache):
    """A #121 mankója a kész sorra (javasol és jelez, nem gátol): szójegyzék (elfogadott egyenérték) és Károli."""
    sor = {k: e[k] for k in FEJLEC[:5]} | {'forditas_hu': vegleges}
    sz = GLF.szojegyzek_ellenorzes(sor, e['forras'], tabla)
    if e['strong'] not in karoli_cache:
        karoli_cache[e['strong']] = GLF.karoli_alakok_strongra(e['strong'])
    ka = GLF.karoli_ellenorzes(sor, karoli_cache[e['strong']])
    tn = tulajdonnev_jelzes(e['strong'], vegleges)
    return {'szojegyzek': list(sz), 'karoli': list(ka), 'tulajdonnev': tn, 'jelzes': sz[0] == 'utkozik' or bool(tn)}


_TIPNR = {}


def tipnr_strongok(ut=None):
    """A TIPNR tulajdonnév-index Strong-számai (`konkordancia/TIPNR_kivonat.tsv` `Strong-szám` oszlopa), Strong_padded alakban."""
    ut = ut or os.path.join(os.path.dirname(ITT), 'konkordancia', 'TIPNR_kivonat.tsv')
    if ut not in _TIPNR:
        ki = set()
        if os.path.exists(ut):
            with open(ut, encoding='utf-8') as f:
                fej = f.readline().rstrip('\n').split('\t')
                i = fej.index('Strong-szám') if 'Strong-szám' in fej else 2
                for l in f:
                    c = l.rstrip('\n').split('\t')
                    if len(c) > i and re.match(r'^[GH]\d{4}', c[i]):
                        ki.add(c[i][:5])
        _TIPNR[ut] = ki
    return _TIPNR[ut]


def tulajdonnev_jelzes(strong, vegleges, tipnr=None):
    """F203 (N88 (2), második előfordulás: F161.11 után a G0076 „ádám”): a TIPNR tulajdonnév-indexében álló Strong kisbetűs
    fordítása jelzés (a beíráshoz `--jelzes-atnezve` kell). Nem gátol és nem javít: a népnév/törzsnév a magyarban kisbetűs
    (G3019 „lévita”), ezt a jelzés átnézője dönti el. -> a jelzés szövege, vagy ''."""
    t = tipnr if tipnr is not None else tipnr_strongok()
    elso = (vegleges or '').lstrip()[:1]
    if strong[:5] in t and elso.isalpha() and elso.islower():
        return 'tulajdonnév-index (TIPNR) Strongja kisbetűvel: %s' % vegleges
    return ''


def kapuz():
    egys = {e['id']: e for e in egysegek_be()}
    val = valaszok()
    tabla = GLF.egyenertek_tabla(kizar=(MENETJEL,))
    karoli_cache = {}
    ki = []
    for proba in (1, 2):
        kerek = kerelmek_be(proba)[0]
        for k in kerek:
            cid = k['custom_id']
            n = int(CID.match(cid).group('n'))
            v = val.get(cid)
            if v is None:
                continue
            ids = [e['id'] for e in egys.values() if e['keres'] == n and ('### %s\n' % e['id']) in
                   k['params']['messages'][0]['content'][0]['text']]
            bont, hiba = valasz_bont(v['szoveg']) if v.get('tipus') == 'succeeded' else ({}, 'a kérés nem sikerült: %s' % v.get('hiba'))
            for i in ids:
                e = egys[i]
                hu, biz = bont.get(i, (None, []))
                if i not in bont:
                    r = (None, [], [('0_json', 'SERTES', hiba or '%s hiányzik a válaszból' % i)], False)
                else:
                    r = egyseg_kapuk(e, hu, biz)
                rek = {'id': i, 'custom_id': cid, 'proba': proba, 'modell': v.get('modell', ''), 'eredet': v.get('eredet', ''),
                       'nyers': hu, 'forditas_hu': r[0], 'valtozasok': r[1], 'eredmenyek': r[2], 'atment': r[3],
                       'bizonytalan': biz}
                if r[3]:
                    rek['manko'] = manko_jelzes(e, r[0], tabla, karoli_cache)
                ki.append(rek)
    with open(ut('kapu_eredmeny.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for r in ki:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    vegso = vegso_allapot(ki)
    at = sum(1 for r in vegso.values() if r['atment'])
    print('kapuzva: %d egység válasszal / %d; átment %d, bukott %d; mankó-jelzés %d' % (
        len(vegso), len(egys), at, len(vegso) - at, sum(1 for r in vegso.values() if r.get('manko', {}).get('jelzes'))))
    for i, r in sorted(vegso.items()):
        if not r['atment']:
            print('  %s (p%d): %s' % (i, r['proba'], '; '.join('%s: %s' % (n, d) for n, er, d in r['eredmenyek'] if er == 'SERTES')))
    return 0


def vegso_allapot(rekordok=None):
    """{id: az egység utolsó próbájának kapu-rekordja}."""
    if rekordok is None:
        rekordok = B.jsonl_olvas(ut('kapu_eredmeny.jsonl'))
    ki = {}
    for r in sorted(rekordok, key=lambda r: r['proba']):
        ki[r['id']] = r
    return ki


# ---------- javító kör ----------

def javito_kerelmek():
    """A kapun bukott egységek javító kérései (p2), determinisztikusan: kérésenként egyetlen user-üzenet — a prompt a bukott
    egységek blokkjaival, utána a korábbi válasz (egységenként) és a kapu hibaüzenete. Így API-n és subagenttel ugyanaz. Csak az
    1. kör kapu-rekordjaiból épül, ezért a 2. kör válaszai után is ugyanazt adja (a `bekuld` ezzel veti össze)."""
    vegso = vegso_allapot([r for r in B.jsonl_olvas(ut('kapu_eredmeny.jsonl')) if r['proba'] == 1])
    egys = {e['id']: e for e in egysegek_be()}
    bukott = {}
    for i, r in vegso.items():
        if not r['atment']:
            bukott.setdefault(r['custom_id'], []).append(r)
    tabla = GLF.egyenertek_tabla(kizar=(MENETJEL,))
    karoli_cache = {}
    ki = []
    for cid, rek in sorted(bukott.items()):
        rek = sorted(rek, key=lambda r: r['id'])
        alap = prompt_epit([egys[r['id']] for r in rek], tabla, karoli_cache)
        sorok = []
        for r in rek:
            hibak = '; '.join('%s — %s' % (n, d or er) for n, er, d in r['eredmenyek'] if er == 'SERTES')
            elozo = r['nyers'] if isinstance(r.get('nyers'), str) and r['nyers'].strip() else '(nincs korábbi válasz)'
            sorok.append('- %s: korábbi fordításod: %s\n  a kapu hibája: %s' % (r['id'], elozo, hibak))
        szoveg = (alap + '\n\n## Javító kör\n\nEzeknek az egységeknek a korábbi fordítása a kapuellenőrzésen elbukott:\n\n'
                  + '\n'.join(sorok) + '\n\nJavítsd ki őket a forrás és a fenti szabályok szerint (a ⟦n⟧ helyőrzők '
                  'változatlanul, pontosan egyszer). A fenti JSON-formában add vissza mindegyiket; KIZÁRÓLAG a JSON-t.')
        ki.append({'custom_id': cid.replace('-p1', '-p2'), 'params': kerelem_params([user(szoveg)])})
    return ki, sum(len(v) for v in bukott.values())


def javit():
    """A javító kör (legfeljebb egyszer, p2)."""
    if any(r['proba'] == 2 for r in vegso_allapot().values()):
        raise SystemExit('a javító kör már lefutott (legfeljebb egy javító kör)')
    ki, db = javito_kerelmek()
    with open(ut('keresek_p2.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(jsonl_szoveg(ki))
    print('javító kérések: %d (%d egység) -> %s' % (len(ki), db, ut('keresek_p2.jsonl')))
    return 0


# ---------- rögzítés, beírás ----------

def allapot_modellbol(modell):
    a, m = B.modell_allapot({modell})
    return a, m


def rogzit(datum=None):
    datum = datum or datetime.date.today().strftime('%Y.%m.%d')
    egys = {e['id']: e for e in egysegek_be()}
    vegso = vegso_allapot()
    _, term_verzio = E.terminologia_szoveg()
    sorok, bukott = [], []
    for i, r in sorted(vegso.items()):
        e = egys[i]
        if r['atment']:
            all_, mod = allapot_modellbol(r['modell'])
            megj = ('%s (glossza-lánc, prompt %s, %s, %s): kapuk átmentek%s%s; terminológia %s | scope=%s %s %s %s %s | '
                    'forras=%s | ts=%s' % (
                        MENETJEL, PROMPT_VERZIO, r['custom_id'], (SUBAGENT_EREDET % r['modell']) if r['eredet'] == 'subagent'
                        else 'Batch API',
                        '; javítóréteg: ' + ', '.join(x[0] for x in r['valtozasok']) if r['valtozasok'] else '',
                        '; bizonytalan: ' + ', '.join(r['bizonytalan']) if r['bizonytalan'] else '',
                        term_verzio, e['szotar'], e['strong'], e['entry_id'], e['jelentes_szam'], e['mezo'],
                        FORRAS_FAJL[e['szotar']], datetime.date.today().isoformat()))
            sorok.append({k: e[k] for k in FEJLEC[:5]} | {
                'forras_hash': e['forras_hash'], 'forditas_hu': r['forditas_hu'], 'allapot': all_, 'modell': mod,
                'datum': datum, 'terminologia_verzio': term_verzio, 'megjegyzes': megj,
                '_manko': 'jelzes' if r.get('manko', {}).get('jelzes') else ''})
        elif r['proba'] == 2:
            for n, er, d in r['eredmenyek']:
                if er == 'SERTES':
                    bukott.append({k: e[k] for k in FEJLEC[:5]} | {'forras_hash': e['forras_hash'], 'kapu': n, 'ok': d,
                                                                   'probalkozas': 2, 'modell': r['modell'], 'datum': datum})
    tsv_ir(ut('rogzitett.tsv'), FEJLEC + ['_manko'], sorok)
    tsv_ir(ut('bukottak.tsv'), BUKOTT_FEJLEC, bukott)
    nyitott = sum(1 for r in vegso.values() if not r['atment'] and r['proba'] == 1)
    print('rögzítve: %d sor (mankó-jelzés %d); kétszer bukott %d egység; javításra vár %d' % (
        len(sorok), sum(1 for s in sorok if s['_manko']), len({(b['strong'], b['entry_id'], b['jelentes_szam']) for b in bukott}), nyitott))
    return 0


def beir(jelzes_atnezve=False, felulir=False, forditasok_ut=None):
    """A rogzitett.tsv sorai az adat/forditasok.tsv-be. Védett: `kezi` sor soha; meglévő nem `kezi` sor csak --felulir-ral;
    mankó-jelzéses sor csak --jelzes-atnezve-vel; a forrás mai hash-e a rögzítettel egyezik; a többi sor bájtra változatlan."""
    forditasok_ut = forditasok_ut or GLF.FORDITASOK
    uj = tsv_be(ut('rogzitett.tsv'))
    if not uj:
        raise SystemExit('a rogzitett.tsv üres (rogzit előbb)')
    if any(r.get('_manko') for r in uj) and not jelzes_atnezve:
        raise SystemExit('mankó-jelzéses sor van (%d) — kézi átnézés után --jelzes-atnezve' % sum(1 for r in uj if r.get('_manko')))
    cache = {}
    for r in uj:
        f = GLF.forras_szoveg(r, cache=cache)
        if f is None or sha1(f) != r['forras_hash']:
            raise SystemExit('%s: a forrás mai hash-e nem a rögzítetté — újra kapuzandó' % '|'.join(r[k] for k in FEJLEC[:5]))
    with open(forditasok_ut, encoding='utf-8', newline='') as fh:
        eredeti = fh.read()
    sorok = eredeti.split('\n')
    if sorok[-1] != '':
        raise SystemExit('a forditasok.tsv nem sortöréssel végződik')
    sorok = sorok[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    if sorok[fej_i].split('\t') != FEJLEC:
        raise SystemExit('a forditasok.tsv fejléce nem a várt: %s' % sorok[fej_i])
    i_all = FEJLEC.index('allapot')
    idx = {tuple(s.split('\t')[:5]): i for i, s in enumerate(sorok) if i > fej_i and s and not s.startswith('#')}
    csere, beszur = {}, {}          # régi index -> új sor; horgony-index -> [új sorok]
    adat = [(i, s.split('\t')) for i, s in enumerate(sorok) if i > fej_i and s and not s.startswith('#')]
    for r in uj:
        sor = '\t'.join(r[m] for m in FEJLEC)
        k = tuple(sor.split('\t')[:5])
        if k in idx:
            regi = sorok[idx[k]].split('\t')
            if regi[i_all] == 'kezi':
                raise SystemExit('védett kezi sor: %s' % (k,))
            FV.ellenoriz(regi, sor.split('\t'), FEJLEC, k)      # F182 (F31): érvényes fordítás nem fordul újra
            if not felulir:
                raise SystemExit('már van sor ehhez a kulcshoz (%s): csak --felulir-ral' % (k,))
            csere[idx[k]] = sor
        else:
            beszur.setdefault(horgony(adat, k), []).append(sor)
    ki = []
    for i, s in enumerate(sorok):
        ki.append(csere.get(i, s))
        ki.extend(beszur.get(i, []))
    ki.extend(beszur.get(None, []))
    # ellenőrzés: a beszúrt sorok nélkül és a cserék visszaállításával a tábla bájtra az eredeti
    vissza = []
    beszurtak = {s for v in beszur.values() for s in v}
    for s in ki:
        if s in beszurtak:
            continue
        vissza.append(s)
    if [sorok[i] if i not in csere else csere[i] for i in range(len(sorok))] != vissza:
        raise SystemExit('váratlan eltérés a táblában — megállok')
    for s in ki:
        if not s.startswith('#') and len(s.split('\t')) != len(FEJLEC):
            raise SystemExit('hibás oszlopszám: %s' % s[:80])
    with open(forditasok_ut, 'w', encoding='utf-8', newline='') as fh:
        fh.write('\n'.join(ki) + '\n')
    n = len(csere) + len(beszurtak)
    print('beírva: %d sor (%d új, a tábla rendje szerinti helyre; %d csere) -> %s' % (n, len(beszurtak), len(csere), forditasok_ut))
    return n


def horgony(adat, k):
    """Az új sor helye (a tábla nem teljesen rendezett, és a vége más PR-ok hozzáfűzési helye): az azonos (szótár, Strong,
    mező) blokk kulcs szerint előző sora mögé; ennek híján az azonos (szótár, mező[, rovid]) sorok kulcs szerinti helyére;
    ennek híján az azonos szótár utolsó sora mögé; csak ha az sincs, a tábla végére (None)."""
    szotar, strong, _, jsz, mezo = k
    for szuro in (lambda c: c[0] == szotar and c[1] == strong and c[4] == mezo,
                  lambda c: c[0] == szotar and c[4] == mezo and (szotar != 'TBESG' or c[3] == jsz),
                  lambda c: c[0] == szotar):
        jelolt = [(i, c) for i, c in adat if szuro(c)]
        if jelolt:
            elotte = [i for i, c in jelolt if tuple(c[:5]) < k]
            return elotte[-1] if elotte else jelolt[0][0] - 1
    return None


# ---------- parancssor ----------

def onteszt():
    hu = 'démon; gonosz szellem'
    e = {'szotar': 'UBS_DNTG', 'strong': 'G4151', 'entry_id': 'x', 'jelentes_szam': '12.37', 'mezo': 'glosszak_hu',
         'forras': 'demon; evil spirit', 'helyorzok': []}
    assert egyseg_kapuk(e, hu, [])[3], egyseg_kapuk(e, hu, [])
    assert not egyseg_kapuk(e, 'démon; evil spirit', [])[3]
    assert not egyseg_kapuk(e, 'démon', [])[3]
    print('önteszt rendben')
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description='F161 glossza-lánc')
    p.add_argument('parancs', nargs='?', choices=['szaraz', 'prompt', 'bekuld', 'allapot', 'begyujt', 'bevesz', 'kapuz',
                                                  'javit', 'rogzit', 'beir'])
    p.add_argument('--munka')
    p.add_argument('--lista')
    p.add_argument('--cid')
    p.add_argument('--ki')
    p.add_argument('--valasz')
    p.add_argument('--modell')
    p.add_argument('--plafon', type=float, default=0.0)
    p.add_argument('--kor', type=int, choices=[1, 2], default=1)
    p.add_argument('--datum')
    p.add_argument('--jelzes-atnezve', action='store_true')
    p.add_argument('--felulir', action='store_true')
    p.add_argument('--onteszt', action='store_true')
    a = p.parse_args(argv)
    if a.onteszt:
        return onteszt()
    if not a.parancs:
        p.error('parancs kell')
    munka_beallit(a.munka)
    if a.parancs == 'szaraz':
        if not a.lista:
            p.error('a szaraz-hoz --lista kell (a #121 lista kimenete)')
        return szaraz(a.lista)
    if a.parancs == 'prompt':
        return prompt_ki(a.cid, a.ki)
    if a.parancs == 'bekuld':
        return bekuld(a.kor, a.plafon)
    if a.parancs == 'allapot':
        return allapot()
    if a.parancs == 'begyujt':
        return begyujt()
    if a.parancs == 'bevesz':
        return bevesz(a.cid, a.valasz, a.modell)
    if a.parancs == 'kapuz':
        return kapuz()
    if a.parancs == 'javit':
        return javit()
    if a.parancs == 'rogzit':
        return rogzit(a.datum)
    if a.parancs == 'beir':
        beir(a.jelzes_atnezve, a.felulir)
        return 0


if __name__ == '__main__':
    sys.exit(main())
