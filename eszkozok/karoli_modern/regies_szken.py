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

Ír (generált): adat/karoli_modern/regies_szken.tsv (a 3. ellenőri kör előtti réteg pillanatképe; az újrafuttatás a
               --kimenet kapcsolóval a maradékot méri: a már kérdezett alak, a kor3-tábláé is, kimarad)
               adat/karoli_modern/igealak_llm_kor3.tsv + _hivasok.jsonl (--llm-valasz)
Használat:
    python eszkozok/karoli_modern/regies_szken.py
    python eszkozok/karoli_modern/regies_szken.py --llm-kerdes <könyvtár a repón kívül> [--koteg N]
    python eszkozok/karoli_modern/regies_szken.py --llm-valasz <könyvtár> --modell <név>
    python eszkozok/karoli_modern/regies_szken.py --kimenet <könyvtár a repón kívül>   (maradék-mérés)
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
VALA_VEG = ('', 'nak', 'nek', 'anak', 'enek', 'ják', 'ja', 'i', 'ik', 'unk', 'ünk', 'juk', 'jük', 'sz', 'tok', 'tek',
            'tök', 'ok', 'ek', 'ök', 'om', 'em', 'öm', 'tt', 'ott', 'ett', 'ött', 't', 'ta', 'te', 'tak', 'ták', 'ték',
            'hat', 'het')


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
    def __init__(self, tok):
        self.tok = tok
        self.sz = collections.Counter()
        for m in tok:
            self.sz[m[2].lower()] += 1
            if m[3]:
                self.sz[m[3].lower()] += 1
        self.volt = set()
        for t in LLM_TABLAK + [KOR3_TABLA]:
            if not os.path.exists(os.path.join(ROOT, t)):
                continue
            with open(os.path.join(ROOT, t), encoding='utf-8') as f:
                for l in f:
                    if not l.startswith('#'):
                        m = l.rstrip('\n').split('\t')
                        self.volt.add(m[2] if t == KOR3_TABLA and len(m) > 2 else m[0])
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

    def szabaly_jelolt(self, w, veg, tip):
        """A végződés szerinti mai alak; None, ha nem képezhető."""
        t = w[:-len(veg)]
        if tip == 'igenev':
            return t + ('va' if veg == 'ván' else 've')
        kot, alap = ir.szetbont(t, self.sz)
        for regi, uj in REGI_TO.items():
            if alap.endswith(regi) and len(alap) == len(regi):
                alap = uj
        if tip == 'pass':
            return t + 'at' + ir.kotohang(t + 'at') if veg == 'aték' else t + 'et' + ir.kotohang(t + 'et')
        if not ir.ige_e(alap, self.sz) and alap not in ir.RENDHAGYO:
            alap2 = alap + 'ik'
            if ir.ige_e(alap2, self.sz):
                alap = alap2
        elif tip == 'ek' and (kot + alap + 'ik') in self.sz:
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
        for i, m in enumerate(self.tok):
            if m[4] or (m[3] and m[3].lower() != m[2].lower()):
                continue
            w0 = m[3] or m[2]
            if w0[:1].isupper() and m[1] != '1':
                continue
            w = w0.lower()
            if len(w) < 4 or w in self.volt or w in NEM_IGE:
                continue
            for veg, tip in VEG:
                if w.endswith(veg):
                    t = w[:-len(veg)]
                    if veg in ('á', 'é') or self.igei(t) or (veg in ('ák', 'ék', 'ám', 'ém', 'ád', 'éd') and self.igei(t + 'ik')):
                        alak[w] += 1
                        elso.setdefault(w, i)
                        jel[w] = self.szabaly_jelolt(w, veg, tip) or ''
                    break
        idx = {(m[0], int(m[1])): i for i, m in enumerate(self.tok)}
        vala = collections.Counter()
        velso = {}
        for i, m in enumerate(self.tok):
            if m[2].lower() in VALA and m[6].startswith('vala_letige'):
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
                    if len(t) >= 3 and self.igei(t):
                        k = w + ' ' + m[2].lower()
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


def llm_valasz(ki, modell):
    """A válaszfájlok (valasz_NN.tsv: id<TAB>válasz) és a hívásnapló (hivasok.jsonl) beolvasása a
    regies_szken.tsv kérdéseihez; ír: igealak_llm_kor3.tsv (+ hívásnapló)."""
    if not modell:
        raise SystemExit('--modell kötelező (a ténylegesen futott modell neve)')
    kerdes = []
    with open(os.path.join(ROOT, KI), encoding='utf-8') as f:
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
    ts = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    with open(os.path.join(ROOT, KOR3_TABLA), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --llm-valasz (F96.3, DT-F96q) — modell-kimenet (modell_ellenorizetlen), kézzel nem '
                'szerkeszthető | modell=%s (Claude Code subagent, előfizetés, API nélkül; vak, versrészlettel) | '
                'forras=%s (sha256:%s) | scope=a régies-szken minden kérdése (%d: %d alak, %d vala-pár) | '
                'opus_alak: az alak mai alakja; a vala-páron a vala előtti ige mai múlt idejű alakja, ha a vala '
                'segédige, különben - | token: %d (%d hívás) | ts=%s\n'
                % (SZKRIPT, modell, KI, sha(KI), len(kerdes), sum(1 for r in kerdes if r[1] == 'alak'),
                   sum(1 for r in kerdes if r[1] == 'vala'), tok, sum(h.get('hivasok', 0) for h in hivasok), ts))
        f.write('\t'.join(['id', 'tipus', 'kerdes', 'szabaly_jelolt', 'opus_alak']) + '\n')
        for r in kerdes:
            f.write('\t'.join([r[0], r[1], r[2], r[4], valasz[r[0]]]) + '\n')
    with open(os.path.join(ROOT, KOR3_NAPLO), 'w', encoding='utf-8', newline='\n') as f:
        for h in hivasok:
            f.write(json.dumps(h, ensure_ascii=False) + '\n')
    print('kor3: %d válasz; token: %d; kiírva: %s' % (len(valasz), tok, KOR3_TABLA))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--llm-kerdes', default=None)
    ap.add_argument('--koteg', type=int, default=380)
    ap.add_argument('--llm-valasz', default=None, help='a válaszok könyvtára (a repón kívül)')
    ap.add_argument('--modell', default=None)
    ap.add_argument('--kimenet', default=None, help='a szken próbája (maradék-mérés) a repón kívülre')
    a = ap.parse_args()
    if a.llm_valasz:
        llm_valasz(a.llm_valasz, a.modell)
        return
    tok = beolvas()
    s = Szken(tok)
    alak, elso, jel, vala, velso = s.futtat()
    sorok = []
    n = 0
    for w in sorted(alak):
        n += 1
        ih, vr = versreszlet(tok, elso[w])
        sorok.append(['R%04d' % n, 'alak', w, str(alak[w]), jel[w], ih, vr])
    for k in sorted(vala):
        n += 1
        ih, vr = versreszlet(tok, velso[k])
        sorok.append(['R%04d' % n, 'vala', k, str(vala[k]), '', ih, vr])
    ki_ut = os.path.join(a.kimenet, 'regies_szken.tsv') if a.kimenet else os.path.join(ROOT, KI)
    if a.kimenet:
        os.makedirs(a.kimenet, exist_ok=True)
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s (F96.3, N-F96d/e, DT-F96q) — kézzel nem szerkeszthető | forras=%s (sha256:%s) + %s | '
                'scope=a modern szövegben maradt régies-igealak-jelöltek: %d alak (%d token), %d vala előtti pár '
                '(%d token); a szabaly_jelolt a végződés szerinti mai alak (igeragozas.mult), modell_ellenorizetlen\n'
                % (SZKRIPT, KM, sha(KM), ' + '.join('%s (sha256:%s)' % (t, sha(t)[:12]) for t in LLM_TABLAK),
                   len(alak), sum(alak.values()), len(vala), sum(vala.values())))
        f.write('\t'.join(['id', 'tipus', 'kerdes', 'gyakorisag', 'szabaly_jelolt', 'elso_igehely', 'versreszlet']) + '\n')
        for r in sorok:
            f.write('\t'.join(r) + '\n')
    print('alak: %d (%d token); vala: %d pár (%d token); kiírva: %s' % (len(alak), sum(alak.values()), len(vala),
                                                                         sum(vala.values()), ki_ut))
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
