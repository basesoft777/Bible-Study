#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.3 (3. ellenőri kör, N-F96d/e) — szisztematikus keresés a modern szövegben maradt régies igealakokra.

A #94 jegyétől és a fedettségi osztálytól függetlenül fut a kiadott `adat/karoli_modern/karoli_modern.tsv`
állapotán (a 3. ellenőri kör előtti réteg). Két jelöltkör:

  alak   a változatlan, nem kieső token régies végződéssel: minden -á/-é (a névutók és a mondatbelseji
         nagybetűs nevek nélkül), és a -ának/-ének, -ánk/-énk, -átok/-étek, -aték/-eték, -ád/-éd, -ám/-ém,
         -ál/-él, -ák/-ék, -ván/-vén végű alak, ha a végződés nélküli tő igei (igei alakja a korpuszban áll
         -ni, -hat/-het, -ott/-ett, -ta/-te, -va/-ve, -jon/-jen … végződéssel, igekötővel is; vagy régi tő:
         tev-, vev-, viv-, hiv-, lev-, ev-, iv-, jöv-); a már egyszer LLM-kérdezett alak kimarad
  vala   a létigeinek vett vala előtti szó, ha ő maga vagy a jelen/múlt végződés nélküli töve igei

A szabály-jelölt a végződés szerinti mai alak (igeragozas.mult), ahol képezhető. Az eredmény a felhasználói
döntés (DT-F96q) szerint LLM-kérdés (opus, vak); a kérdések a repón kívülre kerülnek (--llm-kerdes).

A szabály-jelölt az -ék végen szövegkörnyezetfüggő (E1=…|T3=…; az -ik-es igén E/3 alanyi), az -ának/-ének végen
alanyi=…|targyas=…, ha a tárgyas alak a korpuszban áll; a választást az igealak.py tokenenként végzi.

A 4. kör (--kor 4, DT-F96r, 2. opció) a 3. kör után mért kihagyás-osztályok: v-tő (megnyugovék), igekötő + régi tő
(körülvevék), ható ige (késhetének), igeképzős tő (felzúdíták), -a/-e E/3 alanyi múlt névszószűrővel (megfullada), a
csak a .1 által változtatott token (a modern alakján), a vala_nem_elemezheto vala, és a jelölt opus-szavazat nélkül
(`jelolt` típus; az igealak_alakok.tsv-ből). Bemenete a 3. kör utáni réteg pillanatképe (karoli_modern.tsv,
igealak_alakok.tsv); a kérdések S-azonosítósak.

Ír (generált): adat/karoli_modern/regies_szken.tsv (a 3. ellenőri kör előtti réteg pillanatképe; az újrafuttatás a
               --kimenet kapcsolóval a maradékot méri: a már kérdezett alak, a kor3-tábláé is, kimarad)
               adat/karoli_modern/igealak_llm_kor3.tsv + _hivasok.jsonl (--llm-valasz)
               adat/karoli_modern/regies_szken_kor4.tsv, igealak_llm_kor4.tsv + _hivasok.jsonl (--kor 4)
Használat:
    python eszkozok/karoli_modern/regies_szken.py
    python eszkozok/karoli_modern/regies_szken.py --llm-kerdes <könyvtár a repón kívül> [--koteg N]
    python eszkozok/karoli_modern/regies_szken.py --llm-valasz <könyvtár> --modell <név>
    python eszkozok/karoli_modern/regies_szken.py --kimenet <könyvtár a repón kívül>   (maradék-mérés)
    python eszkozok/karoli_modern/regies_szken.py --kor 4 [--llm-kerdes … | --llm-valasz … --modell … | --kimenet …]
    python eszkozok/karoli_modern/regies_szken.py --kor 5 [ugyanezek] (tokenszintű kérdés a teljes verssel, DT-F96u;
        bemenet: igealak_tokenek.tsv, karoli_modern_versek.tsv; ír: regies_szken_kor5.tsv, igealak_llm_kor5.tsv)
"""

import argparse
import collections
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_modern'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import igeragozas as ir  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KM = os.path.join('adat', 'karoli_modern', 'karoli_modern.tsv')
LLM_TABLAK = [os.path.join('adat', 'karoli_modern', f) for f in ('igealak_llm.tsv', 'igealak_llm_opus.tsv')]
KI = os.path.join('adat', 'karoli_modern', 'regies_szken.tsv')
# A DT-F96q szerinti opus-futás eredménye (a kérdés, a szabály-jelölt és az opus válasza); az igealak.py olvassa
KOR3_TABLA = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor3.tsv')
KOR3_NAPLO = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor3_hivasok.jsonl')
# A 4. kör (DT-F96r, 2. opció): a 3. kör után mért kihagyás-osztályok (--kor 4)
KI4 = os.path.join('adat', 'karoli_modern', 'regies_szken_kor4.tsv')
KOR4_TABLA = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor4.tsv')
KOR4_NAPLO = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor4_hivasok.jsonl')
ALAKOK = os.path.join('adat', 'karoli_modern', 'igealak_alakok.tsv')
# Az 5. kör (DT-F96u, 1. opció): tokenszintű kérdés a teljes verssel a változatlanul maradt, eltérő szavazatú jelöltekre
KI5 = os.path.join('adat', 'karoli_modern', 'regies_szken_kor5.tsv')
KOR5_TABLA = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor5.tsv')
KOR5_NAPLO = os.path.join('adat', 'karoli_modern', 'igealak_llm_kor5_hivasok.jsonl')
I_TOKENEK = os.path.join('adat', 'karoli_modern', 'igealak_tokenek.tsv')
VERSEK = os.path.join('adat', 'karoli_modern', 'karoli_modern_versek.tsv')
SZAVAZAT = re.compile(r'(?:llm|opus|kor3_opus|kor4_opus):([^(;]+)\(')
SZABALY = re.compile(r'(?:szabaly|kor3_szabaly|kor4_szabaly):([^;]+)')
# A .2 szabálycímkéinek eleje: az ilyen címkéjű token igealak-döntést kapott (a 4. kör a csak a .1 által változtatott
# tokent is nézi, a modern alakján)
K2_ELO = ('igealak', 'gyanu', 'kotohang', 'mult_E1', 'ok_birtokos', 'token_kivetel', 'tobbseg', 'kor3', 'vala',
          'jelen_mult', 'lon', 'vagyon', 'felszolito', 'jegyhiba', 'igenev')
KEPZO = ('ít', 'ul', 'ül', 'oz', 'ez', 'öz', 'gat', 'get', 'tat', 'tet', 'kod', 'ked', 'köd', 'dos', 'des', 'dös', 'lad',
         'led', 'ad', 'ed')  # az -ad/-ed (megfullad) névszóval is egybeesik: a csere csak a szabály és az opus egyezésével
NEVSZO_RAG = ('ában', 'ében', 'ához', 'éhez', 'ából', 'éből', 'ára', 'ére', 'ával', 'ével', 'áról', 'éről', 'ától',
              'étől')
SZKRIPT = 'eszkozok/karoli_modern/regies_szken.py'
VALA = ('vala', 'valának', 'valék', 'valál', 'valánk', 'valátok')

IGEI = ('ni', 'ani', 'eni', 'hat', 'het', 'ván', 'vén', 'ott', 'ett', 'ött', 'tta', 'tte', 'tták', 'tték', 'ttak', 'ttek',
        'tak', 'tek', 'ta', 'te', 'va', 've', 'jon', 'jen', 'jön', 'tál', 'tél', 'tam', 'tem')
REGI_TO = {'tev': 'tesz', 'vev': 'vesz', 'viv': 'visz', 'hiv': 'hisz', 'lev': 'lesz', 'ev': 'eszik', 'iv': 'iszik',
           'jöv': 'jön', 'tév': 'tesz', 'vév': 'vesz'}
NEM_IGE = {'felé', 'fölé', 'mellé', 'közé', 'mögé', 'elé', 'alá', 'felfelé', 'fölfelé', 'befelé', 'lefelé', 'kifelé',
           'kié', 'miénk', 'közénk', 'elénk', 'közétek', 'elétek', 'elém', 'mellém', 'felém', 'melléd', 'feléd', 'alád',
           'eléd', 'mögéd', 'szám', 'szád', 'család', 'szél', 'fedél', 'szál', 'szék', 'kerék', 'táplálék', 'maradék',
           'fakadék', 'hajlék', 'szívén', 'nevén', 'révén', 'füvén', 'lévén', 'szaván', 'árván', 'magván', 'javán',
           'kíván', 'magának', 'hálának', 'kezének', 'hegyének', 'istenének', 'nemzetének', 'szövetségének',
           'dicsőségének', 'örökségének', 'erősségének', 'szánk'}
# végződés → (személy, tárgyas); None: nincs szabály-jelölt (a szövegkörnyezet dönt, csak LLM)
VEG = [('ának', ('T3', False)), ('ének', ('T3', False)), ('ánk', ('T1', False)), ('énk', ('T1', False)),
       ('átok', ('T2', False)), ('étek', ('T2', False)), ('aték', 'pass'), ('eték', 'pass'),
       ('ád', ('E2', True)), ('éd', ('E2', True)), ('ám', ('E1', True)), ('ém', ('E1', True)),
       ('ál', ('E2', False)), ('él', ('E2', False)), ('ék', 'ek'), ('ák', ('T3', True)),
       ('vén', 'igenev'), ('ván', 'igenev'), ('á', ('E3', True)), ('é', ('E3', True))]
VEG4 = VEG + [('a', ('E3', False)), ('e', ('E3', False))]
VALA_VEG = ('', 'nak', 'nek', 'anak', 'enek', 'ják', 'ja', 'i', 'ik', 'unk', 'ünk', 'juk', 'jük', 'sz', 'tok', 'tek',
            'tök', 'ok', 'ek', 'ök', 'om', 'em', 'öm', 'tt', 'ott', 'ett', 'ött', 't', 'ta', 'te', 'tak', 'ták', 'ték',
            'hat', 'het')


def most():
    """A proveniencia ts-mezője (UTC, percre)."""
    return __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def beolvas():
    tok = []
    with open(os.path.join(ROOT, KM), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#') or l.startswith('igehely\t'):
                continue
            tok.append(l.rstrip('\n').split('\t'))
    return tok


class Szken:
    def __init__(self, tok, kor=3):
        self.kor = kor
        self.tok = tok
        self.sz = collections.Counter()
        for m in tok:
            self.sz[m[2].lower()] += 1
            if m[3]:
                self.sz[m[3].lower()] += 1
        self.volt = set()
        for t in LLM_TABLAK + [KOR3_TABLA, KOR4_TABLA]:
            if not os.path.exists(os.path.join(ROOT, t)):
                continue
            with open(os.path.join(ROOT, t), encoding='utf-8') as f:
                for l in f:
                    if not l.startswith('#'):
                        m = l.rstrip('\n').split('\t')
                        self.volt.add(m[2] if t in (KOR3_TABLA, KOR4_TABLA) and len(m) > 2 else m[0])
        self.kot = [''] + ir.IGEKOTOK

    def igei(self, t):
        if len(t) < 2:
            return False
        k, ap = ir.szetbont(t, self.sz)
        for to in {t, ap}:
            if len(to) < 2:
                continue
            if to.endswith(tuple(REGI_TO)) and len(to) <= len(k) + 6:
                return True
            for kk in self.kot:
                for s in IGEI:
                    if (kk + to + s) in self.sz and (kk + to + s) != t:
                        return True
        return False

    def igei4(self, t):
        """A 4. kör tágabb igei próbája: igekötő + régi tő (körülvev), v-tő (megnyugov → megnyugod), ható ige
        (késhet, tűrhet), igeképzős tő (felzúdít)."""
        if self.igei(t):
            return True
        for k in self.kot:
            if k and t.startswith(k) and t[len(k):] in REGI_TO:
                return True
        if t.endswith('v') and len(t) >= 4 and (self.igei(t[:-1] + 'd') or self.igei(t[:-1] + 'sz')):
            return True
        if t.endswith(('hat', 'het')) and len(t) > 5 and self.igei(t[:-3]):
            return True
        return t.endswith(KEPZO) and len(t) >= 5

    def szabaly_jelolt(self, w, veg, tip):
        """A végződés szerinti mai alak; None, ha nem képezhető."""
        t = w[:-len(veg)]
        if tip == 'igenev':
            return t + ('va' if veg == 'ván' else 've')
        kot, alap = ir.szetbont(t, self.sz)
        regi_to = False
        for regi, uj in REGI_TO.items():
            if alap.endswith(regi) and len(alap) == len(regi):
                alap = uj
        if self.kor == 4 and not ir.ige_e(alap, self.sz) and alap not in ir.RENDHAGYO:
            for k in self.kot:
                if k and t.startswith(k) and t[len(k):] in REGI_TO:
                    kot, alap = k, REGI_TO[t[len(k):]]  # körülvev → körül + vesz
                    regi_to = True
                    break
            else:
                if alap.endswith('v') and self.igei(alap[:-1] + 'd'):
                    alap = alap[:-1] + 'dik'  # megnyugov → megnyugodik (megnyugovék → megnyugodott)
        if tip == 'pass':
            return t + 'at' + ir.kotohang(t + 'at') if veg == 'aték' else t + 'et' + ir.kotohang(t + 'et')
        if not ir.ige_e(alap, self.sz) and alap not in ir.RENDHAGYO:
            alap2 = alap + 'ik'
            if ir.ige_e(alap2, self.sz):
                alap = alap2
        elif tip == 'ek' and not regi_to and (kot + alap + 'ik') in self.sz:
            alap = alap + 'ik'  # bosszankodék → bosszankodik
        if tip == 'ek':
            # -ék: E/1 vagy T/3 tárgyas (a versbeli E/1 dönt, igealak.py); az -ik-es igén E/3 alanyi; ha a T/3
            # tárgyas alak a korpuszban nem áll, E/1
            if alap.endswith('ik'):
                m = ir.mult(alap, 'E3', False)
                return kot + m if m else None
            e1, t3 = ir.mult(alap, 'E1', False), ir.mult(alap, 'T3', True)
            if not e1:
                return None
            if not t3 or (kot + t3) not in self.sz:
                return kot + e1  # tárgyatlan (a T/3 tárgyas alak a korpuszban nem áll): E/1
            return 'E1=%s|T3=%s' % (kot + e1, kot + t3)
        m = ir.mult(alap, *tip)
        if m and tip == ('T3', False):
            # -ának/-ének: alanyi vagy tárgyas (a tagmondat dönt, igealak.py), ha a tárgyas alak a korpuszban áll
            t = ir.mult(alap, 'T3', True)
            if t and t != m and (kot + t) in self.sz:
                return 'alanyi=%s|targyas=%s' % (kot + m, kot + t)
        return kot + m if m else None

    def futtat(self):
        alak = collections.Counter()
        elso = {}
        jel = {}
        kor4 = self.kor == 4
        for i, m in enumerate(self.tok):
            if m[4]:
                continue
            if m[3] and m[3].lower() != m[2].lower():
                # a 4. kör a csak a .1 által változtatott tokent is nézi (dícsérvén → dicsérvén)
                if not kor4 or any(c.startswith(K2_ELO) for c in m[6].split('+')):
                    continue
            w0 = m[3] or m[2]
            if w0[:1].isupper() and m[1] != '1':
                continue
            w = w0.lower()
            if len(w) < 4 or w in self.volt or w in NEM_IGE:
                continue
            for veg, tip in (VEG4 if kor4 else VEG):
                if w.endswith(veg):
                    t = w[:-len(veg)]
                    if veg in ('a', 'e') and (len(t) < 3 or any((t + x) in self.sz for x in NEVSZO_RAG)):
                        break  # névszó (keze → kezében)
                    igei = self.igei4 if kor4 else self.igei
                    if (veg in ('á', 'é') or igei(t)
                            or (veg in ('ák', 'ék', 'ám', 'ém', 'ád', 'éd') and igei(t + 'ik'))):
                        alak[w] += 1
                        elso.setdefault(w, i)
                        jel[w] = self.szabaly_jelolt(w, veg, tip) or ''
                    break
        idx = {(m[0], int(m[1])): i for i, m in enumerate(self.tok)}
        vala = collections.Counter()
        velso = {}
        for i, m in enumerate(self.tok):
            if m[2].lower() in VALA and (m[6].startswith('vala_letige') or (kor4 and m[6] == 'vala_nem_elemezheto')):
                j = idx.get((m[0], int(m[1]) - 1))
                if j is None or self.tok[j][4]:
                    continue
                e = self.tok[j]
                w = (e[3] or e[2]).lower()
                if w in NEM_IGE or len(w) < 3:
                    continue
                for veg in VALA_VEG:
                    if veg and not w.endswith(veg):
                        continue
                    t = w[:len(w) - len(veg)] if veg else w
                    if len(t) >= 3 and (self.igei4(t) if kor4 else self.igei(t)):
                        k = w + ' ' + m[2].lower()
                        if k in self.volt:
                            break
                        vala[k] += 1
                        velso.setdefault(k, j)
                        break
        return alak, elso, jel, vala, velso


def versreszlet(tok, i, n=6):
    ih = tok[i][0]
    j0 = i
    while j0 > 0 and tok[j0 - 1][0] == ih and i - j0 < n:
        j0 -= 1
    j1 = i
    while j1 + 1 < len(tok) and tok[j1 + 1][0] == ih and j1 - i < n:
        j1 += 1
    return ih, ' '.join(('[%s]' % (tok[j][3] or tok[j][2])) if j == i else (tok[j][3] or tok[j][2] or '·')
                        for j in range(j0, j1 + 1))


def ts_mezo(futas_ts=None):
    """A ts-mező; a meglévő válaszokból való újraírásnál (--futas-ts) az LLM-futás eredeti ideje is."""
    return most() + (' | futas_ts=%s (az LLM-futás ideje; a tábla a meglévő válaszfájlokból újraírva)' % futas_ts
                     if futas_ts else '')


def llm_valasz(ki, modell, kor=3, futas_ts=None):
    """A válaszfájlok (valasz_NN.tsv: id<TAB>válasz) és a hívásnapló (hivasok.jsonl) beolvasása a
    regies_szken.tsv kérdéseihez; ír: igealak_llm_kor3.tsv (+ hívásnapló)."""
    if not modell:
        raise SystemExit('--modell kötelező (a ténylegesen futott modell neve)')
    KI_, TABLA, NAPLO = (KI4, KOR4_TABLA, KOR4_NAPLO) if kor == 4 else (KI, KOR3_TABLA, KOR3_NAPLO)
    kerdes = []
    with open(os.path.join(ROOT, KI_), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#') or l.startswith('id\t'):
                continue
            kerdes.append(l.rstrip('\n').split('\t'))
    valasz = {}
    for fn in sorted(os.listdir(ki)):
        if re.match(r'valasz_\d+\.tsv$', fn):
            with open(os.path.join(ki, fn), encoding='utf-8') as f:
                for l in f:
                    m = l.rstrip('\n').split('\t')
                    if len(m) == 2:
                        valasz[m[0]] = m[1].strip()
    hiany = [r[0] for r in kerdes if r[0] not in valasz]
    if hiany or len(valasz) != len(kerdes):
        raise SystemExit('a válasz nem teljes: %d hiányzik %s, %d válasz / %d kérdés'
                         % (len(hiany), hiany[:5], len(valasz), len(kerdes)))
    import json
    with open(os.path.join(ki, 'hivasok.jsonl'), encoding='utf-8') as f:
        hivasok = [json.loads(l) for l in f if l.strip()]
    tok = sum(h.get('total_tokens', 0) for h in hivasok)
    with open(os.path.join(ROOT, TABLA), 'w', encoding='utf-8', newline='\n') as f:
        f.write(('# GENERÁLT: %s --llm-valasz (F96.3, ' + ('--kor 4, 4. kör: DT-F96r' if kor == 4 else '3. kör: DT-F96q') + ') — modell-kimenet (modell_ellenorizetlen), kézzel nem '
                'szerkeszthető | modell=%s (Claude Code subagent, előfizetés, API nélkül; vak, versrészlettel) | '
                'forras=%s (sha256:%s) | scope=a régies-szken minden kérdése (%d: %d alak, %d vala-pár, %d jelölt) | '
                'opus_alak: az alak mai alakja; a vala-páron a vala előtti ige mai múlt idejű alakja, ha a vala '
                'segédige, különben - | token: %d (%d hívás) | ts=%s\n')
                % (SZKRIPT, modell, KI_, sha(KI_), len(kerdes), sum(1 for r in kerdes if r[1] == 'alak'),
                   sum(1 for r in kerdes if r[1] == 'vala'), sum(1 for r in kerdes if r[1] == 'jelolt'), tok, sum(h.get('hivasok', 0) for h in hivasok), ts_mezo(futas_ts)))
        f.write('\t'.join(['id', 'tipus', 'kerdes', 'szabaly_jelolt', 'opus_alak']) + '\n')
        for r in kerdes:
            f.write('\t'.join([r[0], r[1], r[2], r[4], valasz[r[0]]]) + '\n')
    with open(os.path.join(ROOT, NAPLO), 'w', encoding='utf-8', newline='\n') as f:
        for h in hivasok:
            f.write(json.dumps(h, ensure_ascii=False) + '\n')
    print('kor%d: %d válasz; token: %d; kiírva: %s' % (kor, len(valasz), tok, TABLA))


def jelolt_opus_nelkul(tok):
    """A 4. kör (H): a változatlanul maradt jelölt alak, amelyre opus-szavazat még nincs (a DT-F96l többségéhez
    a harmadik szavazat); a felszólító (DT-F96k a) és a -nd- jövő kimarad. {alak: szabály-jelölt}."""
    ki = {}
    fej = None
    with open(os.path.join(ROOT, ALAKOK), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            if (d['alkalmazas'] == 'jelolt' and not d['opus_alak'] and not d['szabaly'].startswith('felszolito')
                    and d['szabaly'] != 'gyanu:nd_jovo'):
                ki[d['alak'].lower()] = d['szabaly_jelolt']
    valtozatlan = set()
    for m in tok:
        # változatlan, vagy csak a .1 változtatta (a régies végződés megmaradt: dícsérvén → dicsérvén)
        if not m[4] and m[2].lower() in ki and (not m[3] or m[3].lower()[-3:] == m[2].lower()[-3:]):
            valtozatlan.add(m[2].lower())
    return {k: v for k, v in ki.items() if k in valtozatlan}


def szavazatok(jelolt):
    """A `jelolt` oszlop meglévő jelöltjei: (szabály-értékek, LLM-értékek)."""
    szab = [v.split('=')[-1].strip() for x in SZABALY.findall(jelolt) for v in x.split('|')]
    return szab, [v.strip() for v in SZAVAZAT.findall(jelolt)]


def kor5_kerdesek():
    """Az 5. kör kérdései: a modern szövegben változatlan, kieső nélküli, `jelolt` oszlopos token, ahol legalább egy
    LLM-szavazat változtatna, vagy LLM-szavazat nélkül a szabály-jelölt változtatna; a felszólító (DT-F96k a) és a -nd- jövő kimarad. A vers a modern
    szöveg, a token [szögletes zárójelben] (a nem kieső tokenek sorrendje a K2 szerint a modern szöveg szavaié)."""
    kieso = collections.defaultdict(set)
    for m in beolvas():
        if m[4]:
            kieso[m[0]].add(int(m[1]))
    vers = {}
    with open(os.path.join(ROOT, VERSEK), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#') or l.startswith('igehely\t'):
                continue
            m = l.rstrip('\n').split('\t')
            vers[m[0]] = m[1]
    betu = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
    sorok = []
    with open(os.path.join(ROOT, I_TOKENEK), encoding='utf-8') as f:
        fej = None
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            if not d['jelolt'] or d['kieso'] or d['alak_modern'].lower() != d['alak_helyesiras'].lower():
                continue
            if d['szabaly'].startswith('felszolito') or 'nd_jovo' in d['szabaly']:
                continue
            szab, llm = szavazatok(d['jelolt'])
            w = d['alak_helyesiras'].lower()
            if llm and all(v.lower() == w for v in llm):
                continue  # minden LLM-szavazat szerint változatlan (nem régies; vége ≠ végett)
            if not [v for v in szab + llm if v.lower() != w]:
                continue
            sorsz = int(d['sorszam'])
            n = sorsz - 1 - sum(1 for k in kieso[d['igehely']] if k < sorsz)
            sz = vers[d['igehely']]
            sp = list(betu.finditer(sz))
            if n >= len(sp) or sp[n].group(0) != d['alak_modern']:
                raise SystemExit('a token helye a versben nem azonosítható: %s %s' % (d['igehely'], d['sorszam']))
            jelolt = sz[:sp[n].start()] + '[' + sp[n].group(0) + ']' + sz[sp[n].end():]
            meglevo = '|'.join(sorted({v for v in szab + llm if v}))
            sorok.append([d['igehely'], d['sorszam'], d['alak_helyesiras'], meglevo, jelolt])
    return sorok


def kor5(a):
    if a.llm_valasz:
        if not a.modell:
            raise SystemExit('--modell kötelező (a ténylegesen futott modell neve)')
        kerdes = []
        with open(os.path.join(ROOT, KI5), encoding='utf-8') as f:
            for l in f:
                if not l.startswith('#') and not l.startswith('id\t'):
                    kerdes.append(l.rstrip('\n').split('\t'))
        valasz = {}
        for fn in sorted(os.listdir(a.llm_valasz)):
            if re.match(r'valasz_\d+\.tsv$', fn):
                with open(os.path.join(a.llm_valasz, fn), encoding='utf-8') as f:
                    for l in f:
                        m = l.rstrip('\n').split('\t')
                        if len(m) == 2:
                            valasz[m[0]] = m[1].strip()
        hiany = [r[0] for r in kerdes if r[0] not in valasz]
        if hiany or len(valasz) != len(kerdes):
            raise SystemExit('a válasz nem teljes: %d hiányzik %s' % (len(hiany), hiany[:5]))
        import json
        with open(os.path.join(a.llm_valasz, 'hivasok.jsonl'), encoding='utf-8') as f:
            hivasok = [json.loads(l) for l in f if l.strip()]
        tok = sum(h.get('total_tokens', 0) for h in hivasok)
        with open(os.path.join(ROOT, KOR5_TABLA), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: %s --kor 5 --llm-valasz (F96.3, 5. kör: DT-F96u) — modell-kimenet (modell_ellenorizetlen), '
                    'kézzel nem szerkeszthető | modell=%s (Claude Code subagent, előfizetés, API nélkül; vak, a teljes '
                    'verssel, tokenenként) | forras=%s (sha256:%s) | scope=a változatlanul maradt, eltérő szavazatú '
                    'jelölt tokenek (%d) | token: %d (%d hívás) | ts=%s\n'
                    % (SZKRIPT, a.modell, KI5, sha(KI5), len(kerdes), tok, sum(h.get('hivasok', 0) for h in hivasok),
                       ts_mezo(a.futas_ts)))
            f.write('\t'.join(['id', 'igehely', 'sorszam', 'alak', 'meglevo_jeloltek', 'opus_alak']) + '\n')
            for r in kerdes:
                f.write('\t'.join(r[:5] + [valasz[r[0]]]) + '\n')
        with open(os.path.join(ROOT, KOR5_NAPLO), 'w', encoding='utf-8', newline='\n') as f:
            for h in hivasok:
                f.write(json.dumps(h, ensure_ascii=False) + '\n')
        print('kor5: %d válasz; token: %d; kiírva: %s' % (len(valasz), tok, KOR5_TABLA))
        return
    sorok = [['T%04d' % n] + r for n, r in enumerate(kor5_kerdesek(), 1)]
    ki_ut = os.path.join(a.kimenet, 'regies_szken_kor5.tsv') if a.kimenet else os.path.join(ROOT, KI5)
    if a.kimenet:
        os.makedirs(a.kimenet, exist_ok=True)
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --kor 5 (F96.3, 5. kör: DT-F96u, 1. opció) — kézzel nem szerkeszthető | forras=%s '
                '(sha256:%s) + %s (sha256:%s) + %s (sha256:%s) | scope=a modern szövegben változatlanul maradt jelölt '
                'tokenek, ahol legalább egy forrás változtatna (%d), a felszólító és a -nd- jövő nélkül; '
                'meglevo_jeloltek: a szabály- és LLM-jelöltek; vers: a modern versszöveg, a token [szögletes '
                'zárójelben] | ts=%s\n'
                % (SZKRIPT, I_TOKENEK, sha(I_TOKENEK), VERSEK, sha(VERSEK), KM, sha(KM), len(sorok), most()))
        f.write('\t'.join(['id', 'igehely', 'sorszam', 'alak', 'meglevo_jeloltek', 'vers']) + '\n')
        for r in sorok:
            f.write('\t'.join(r) + '\n')
    print('kor5: %d token-kérdés; kiírva: %s' % (len(sorok), ki_ut))
    if a.llm_kerdes:
        if os.path.abspath(a.llm_kerdes).startswith(ROOT):
            raise SystemExit('a kérdések a repón kívülre mennek')
        os.makedirs(a.llm_kerdes, exist_ok=True)
        for b in range(0, len(sorok), a.koteg):
            with open(os.path.join(a.llm_kerdes, 'kerdes_%02d.tsv' % (b // a.koteg + 1)), 'w', encoding='utf-8') as f:
                for r in sorok[b:b + a.koteg]:
                    f.write('\t'.join([r[0], r[3], r[5]]) + '\n')
        print('LLM-kérdés: %d köteg → %s' % ((len(sorok) + a.koteg - 1) // a.koteg, a.llm_kerdes))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--llm-kerdes', default=None)
    ap.add_argument('--koteg', type=int, default=380)
    ap.add_argument('--llm-valasz', default=None, help='a válaszok könyvtára (a repón kívül)')
    ap.add_argument('--modell', default=None)
    ap.add_argument('--futas-ts', default=None,
                    help='a --llm-valasz újraírásnál az LLM-futás eredeti ideje (a fejléc futas_ts mezője)')
    ap.add_argument('--kimenet', default=None, help='a szken próbája (maradék-mérés) a repón kívülre')
    ap.add_argument('--kor', type=int, default=3, choices=(3, 4, 5),
                    help='4: a 3. kör utáni kihagyás-osztályok (DT-F96r); 5: tokenszintű kérdés (DT-F96u)')
    a = ap.parse_args()
    if a.kor == 5:
        kor5(a)
        return
    if a.llm_valasz:
        llm_valasz(a.llm_valasz, a.modell, a.kor, a.futas_ts)
        return
    tok = beolvas()
    s = Szken(tok, a.kor)
    alak, elso, jel, vala, velso = s.futtat()
    elotag = 'S' if a.kor == 4 else 'R'
    sorok = []
    n = 0
    for w in sorted(alak):
        n += 1
        ih, vr = versreszlet(tok, elso[w])
        sorok.append(['%s%04d' % (elotag, n), 'alak', w, str(alak[w]), jel[w], ih, vr])
    for k in sorted(vala):
        n += 1
        ih, vr = versreszlet(tok, velso[k])
        sorok.append(['%s%04d' % (elotag, n), 'vala', k, str(vala[k]), '', ih, vr])
    if a.kor == 4:
        jo = jelolt_opus_nelkul(tok)
        gy = collections.Counter()
        je = {}
        for i, m in enumerate(tok):
            w = m[2].lower()
            if w in jo and not m[4] and w not in alak:
                gy[w] += 1
                je.setdefault(w, i)
        for w in sorted(gy):
            n += 1
            ih, vr = versreszlet(tok, je[w])
            sorok.append(['%s%04d' % (elotag, n), 'jelolt', w, str(gy[w]), jo[w], ih, vr])
    nev = 'regies_szken_kor4.tsv' if a.kor == 4 else 'regies_szken.tsv'
    ki_ut = os.path.join(a.kimenet, nev) if a.kimenet else os.path.join(ROOT, KI4 if a.kor == 4 else KI)
    if a.kimenet:
        os.makedirs(a.kimenet, exist_ok=True)
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        cimke = ('--kor 4 (F96.3, 4. kör: DT-F96r, 2. opció; a 3. kör utáni kihagyás-osztályok)' if a.kor == 4
                 else '(F96.3, 3. kör: N-F96d/e, DT-F96q)')
        kerdezett = LLM_TABLAK + ([KOR3_TABLA] if a.kor == 4 else [])
        f.write('# GENERÁLT: %s %s — kézzel nem szerkeszthető | forras=%s (sha256:%s)%s + %s | '
                'scope=a modern szövegben maradt régies-igealak-jelöltek: %d alak (%d token), %d vala előtti pár '
                '(%d token)%s; a szabaly_jelolt a végződés szerinti mai alak (igeragozas.mult), modell_ellenorizetlen '
                '| ts=%s\n'
                % (SZKRIPT, cimke, KM, sha(KM),
                   ' + %s (sha256:%s)' % (ALAKOK, sha(ALAKOK)) if a.kor == 4 else '',
                   ' + '.join('%s (sha256:%s)' % (t, sha(t)[:12]) for t in kerdezett if os.path.exists(os.path.join(ROOT, t))),
                   len(alak), sum(alak.values()), len(vala), sum(vala.values()),
                   ', %d jelölt opus-szavazat nélkül' % sum(1 for r in sorok if r[1] == 'jelolt') if a.kor == 4 else '',
                   most()))
        f.write('\t'.join(['id', 'tipus', 'kerdes', 'gyakorisag', 'szabaly_jelolt', 'elso_igehely', 'versreszlet']) + '\n')
        for r in sorok:
            f.write('\t'.join(r) + '\n')
    print('alak: %d (%d token); vala: %d pár (%d token); jelölt: %d; kiírva: %s'
          % (len(alak), sum(alak.values()), len(vala), sum(vala.values()), sum(1 for r in sorok if r[1] == 'jelolt'), ki_ut))
    if a.llm_kerdes:
        if os.path.abspath(a.llm_kerdes).startswith(ROOT):
            raise SystemExit('a kérdések a repón kívülre mennek')
        os.makedirs(a.llm_kerdes, exist_ok=True)
        for b in range(0, len(sorok), a.koteg):
            with open(os.path.join(a.llm_kerdes, 'kerdes_%02d.tsv' % (b // a.koteg + 1)), 'w', encoding='utf-8') as f:
                for r in sorok[b:b + a.koteg]:
                    f.write('\t'.join([r[0], r[1], r[2], r[6]]) + '\n')
        print('LLM-kérdés: %d köteg → %s' % ((len(sorok) + a.koteg - 1) // a.koteg, a.llm_kerdes))


if __name__ == '__main__':
    main()
