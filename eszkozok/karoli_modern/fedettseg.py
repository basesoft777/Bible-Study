#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.0 — fedettségi mérés: a Károli 1908 szóalakjaiból mennyire ad a #94 szótárialak-tábla
egyértelmű modern alakot, mennyihez kell szabály, és mennyi a bizonytalan (LLM-jelölt) maradék.

Determinisztikus, API nélkül. Csak olvas: `konkordancia/Karoli_1908.tsv` (a tokenizálás a
`eszkozok/karoli_strong/tokenek.py` `tokenizal` függvényével, hogy a szóalak ugyanaz legyen,
amelyen a Károli–Strong párosítás `hu_sorszam`-a áll), `adat/szoto/karoli_szotari_alak.tsv`.
Ír: egy mérőtáblát (alakonként egy sor, `--ki`, alapértelmezés `adat/karoli_modern/fedettseg_alakok.tsv`),
az összesítést a stdout-ra. A mérőtábla nem a kiadott réteg, és nem javaslat: osztályozás.

Alakszintű osztályok (az első illeszkedő nyer, ebben a sorrendben):

  regies_lista         ismert régies igealak jegy nélkül (vala-, lőn-család, vagyon) → szabály (DT128)
  igealak_gyakori      régies jegy, a 200 leggyakoribb jegyes kisbetűs alak között → szabály (DT140: K6)
  igealak_ritka        régies jegy a ritka alakon (N-F94h: ~6% hibás jegy) → LLM-jelölt (brief .2/1)
  regies_gyanu         jegy nélküli, de régiesnek látszó igealak: igei tő + régies végződés (-á, -é, -a, -e,
                       -ának, -ék, -ván …), -nd- jövő (mondándok), vagy a #94 kivételtáblájának jegy nélküli,
                       a szótári alaktól eltérő sora (tőn, vőn, jő) → LLM-jelölt
  helyesiras_szabaly   a karakterszabály (cz → c, czcz → cc, nyny → nny, lyly → lly …) maga adja → szabály
  helyesiras_tabla     a #94 mai szótári alakja csak helyesírásban tér el (ékezet, e/ö, kettőzés), és az
                       eltérés az alak elejére esik: a modern alak a táblából egyértelmű
  nem_elotag           helyesírási eltérés, de nem az alak elején (tőváltó alak) → LLM-jelölt
  lemmavaltas          a mai szótári alak nem csak helyesírásban tér el (leány → lány, ki → aki, e → ez,
                       férfiú → férfi): a DT128 szerint a szókincs nem változik → döntési kérdés, nem csere
  valtozatlan          egyik sem
  tablan_kivul         a token (kisbetűsen sem) szerepel a szótárialak-táblában

A tokenszintű, szövegkörnyezetfüggő esetek külön számlálva: a *vala* (segédigei / létigei; az
előző token igei-e), az „a” + ki-/mely-/mi- különírt vonatkozó névmás (N-F94f), és a -ék/-ák végű
jegyes alakok (mult.E1 / mult.T3 tárgyas alakilag egyezik, napló 16.).

Igei tő (heurisztika, manual): a szótári alak (az -ik nélkül) + -ni, -ani, -eni vagy múlt idejű
-t/-tt alak szerepel a korpuszban, vagy a szótári alaknak van jegyes sora.

Használat:
    python eszkozok/karoli_modern/fedettseg.py
    python eszkozok/karoli_modern/fedettseg.py --ki <út>
"""

import argparse
import collections
import difflib
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import tokenek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KAROLI = os.path.join('konkordancia', 'Karoli_1908.tsv')
SZOTARI = os.path.join('adat', 'szoto', 'karoli_szotari_alak.tsv')
KI_ALAP = os.path.join('adat', 'karoli_modern', 'fedettseg_alakok.tsv')
GYAKORI_JEGYES = 200  # DT140: a K6 a 200 leggyakoribb jegyes alakra érvényes

# Ismert régies igealakok, amelyeknek a #94 táblában nincs (vagy nem igealak-) jegyük: a létige és
# a lesz régi múltja, a vagyon. Kézi lista (manual): a DT128 példáiból (lőn → lett, vala → volt).
REGIES_LISTA = {
    'vala', 'valának', 'valék', 'valál', 'valánk', 'valátok',
    'lőn', 'lőnek', 'lőnék', 'lőnél', 'lőnénk', 'lőnetek',
    'vagyon',
}
# néki → neki: a DT128 példája (helyesírás); a reá-család (reá → rá) a DT128-ban nem szerepel: külön számlálva.
SZOALAK_HELYESIRAS = {'néki': 'neki'}
REA_CSALAD = re.compile(r'^reá(m|d|nk|tok|juk|jok)?$')

# Helyesírási karakterszabályok (manual: általános helyesírás-történet; a cz → c a #94-ben is `manual`).
KARAKTER = [('czcz', 'cc'), ('Czcz', 'Cc'), ('cz', 'c'), ('Cz', 'C'), ('nyny', 'nny'), ('lyly', 'lly'),
            ('gygy', 'ggy'), ('tyty', 'tty'), ('szsz', 'ssz'), ('zszs', 'zzs'), ('cscs', 'ccs')]

REGIES_VEG = ['ának', 'ének', 'ánk', 'énk', 'átok', 'étek', 'ván', 'vén', 'aték', 'eték',
              'ák', 'ék', 'ál', 'él', 'á', 'é', 'a', 'e']
ELEMEZETLEN_VEG = ['taték', 'teték', 'tatám', 'tetém', 'tatának', 'tetének', 'tatá', 'teté', 'tatál', 'tetél']
JOVO_ND = re.compile(r'^(.+?)(?:á|é|a|e)nd(?:ok|ek|om|em|asz|esz|od|ed|ja|i|unk|ünk|uk|ük|otok|etek|játok|itek|anak|enek|ják|ik)?$')

EKEZET = str.maketrans({'í': 'i', 'ó': 'o', 'ú': 'u', 'ő': 'ö', 'ű': 'ü'})
NEVMAS = {'ki': re.compile(r'^ki(t|k|ket|nek|knek|ben|kben|ből|re|kre|ről|hez|khez|től|ktől|vel|kkel|ért|kért|n|ken)?$'),
          'mely': re.compile(r'^mely(ek)?(et|ek|nek|ben|ből|re|ről|hez|től|lyel|lyekkel|ért|en|eket|eknek|ekben|ekre|ekről)?$'),
          'mi': re.compile(r'^mi(t|nek|ben|ből|re|ről|hez|től|vel|ért|n)?$')}


def sha256_rov(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()[:12]


def karakter_szabaly(szo):
    for a, b in KARAKTER:
        szo = szo.replace(a, b)
    return szo


def vaz(szo):
    """Helyesírási váz: kisbetű, ékezet nélkül i/o/u/ö/ü, e/ö egybeesik, a kettőzés összevonva."""
    s = karakter_szabaly(szo.lower()).translate(EKEZET).replace('ö', 'e')
    return re.sub(r'(.)\1+', r'\1', s)


def tabla_beolvas():
    sorok = {}
    fej = None
    with open(os.path.join(ROOT, SZOTARI), encoding='utf-8') as f:
        for l in f:
            l = l.rstrip('\n')
            if l.startswith('#'):
                continue
            m = l.split('\t')
            if fej is None:
                fej = m
                continue
            sorok[m[0]] = dict(zip(fej, m))
    return sorok


def korpusz():
    versek = []
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            m = l.rstrip('\n').split('\t')
            if len(m) < 2:
                continue
            versek.append((m[0], tokenek.tokenizal(m[1])))
    return versek


def tablasor(tabla, alak):
    s = tabla.get(alak)
    if s is None and alak != alak.lower():
        s = tabla.get(alak.lower())
    return s


def igei_tovek(tabla, kis_szavak):
    jegyes_lemma = set(s['szotari_alak'] for s in tabla.values() if s['regies_jegy'])

    def igei(lemma):
        if not lemma:
            return False
        if lemma in jegyes_lemma:
            return True
        to = lemma[:-2] if lemma.endswith('ik') else lemma
        if len(to) < 2:
            return False
        return any((to + v) in kis_szavak for v in ('ni', 'ani', 'eni', 'tt', 'ott', 'ett', 'ött'))
    return igei


def helyesiras_atvitel(alak, regi, mai):
    """A mai szótári alak helyesírási eltérését az alakra viszi, ha az eltérés az alak elejére esik."""
    a2, r2 = karakter_szabaly(alak), karakter_szabaly(regi)
    kis = a2.lower()
    if r2 == mai:
        return (a2 if a2 != alak else None), 'karakter'
    sm = difflib.SequenceMatcher(None, r2, mai, autojunk=False)
    nem_egyezo = [(i2, j2) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
    vege, j_vege = nem_egyezo[-1]
    if not kis.startswith(r2[:vege]):
        return None, 'nem_elotag'
    uj = mai[:j_vege] + a2[vege:]
    if alak[:1].isupper():
        uj = uj[:1].upper() + uj[1:]
    return uj, 'tabla'


def osztalyoz(alak, sor, gyakori_jegyes, igei):
    kis = alak.lower()
    if kis in REGIES_LISTA:
        return 'regies_lista', '', ''
    if kis in SZOALAK_HELYESIRAS:
        uj = SZOALAK_HELYESIRAS[kis]
        return 'helyesiras_szabaly', 'DT128 szóalak', uj[:1].upper() + uj[1:] if alak[:1].isupper() else uj
    if sor is None:
        k = karakter_szabaly(alak)
        if k != alak:
            return 'helyesiras_szabaly', 'karakter (táblán kívül)', k
        return 'tablan_kivul', '', ''
    jegy = sor['regies_jegy']
    lemma = sor['szotari_alak']
    if jegy:
        return ('igealak_gyakori' if kis in gyakori_jegyes else 'igealak_ritka'), jegy, ''
    # jegy nélküli régies gyanú
    m = JOVO_ND.match(kis)
    if m and igei(m.group(1)) and len(kis) > len(m.group(1)) + 2:
        return 'regies_gyanu', 'nd_jovo', ''
    if sor['modszer'] == 'kivetel' and kis != lemma and igei(lemma):
        return 'regies_gyanu', 'kivetel_jegy_nelkul', ''
    to = lemma[:-2] if lemma.endswith('ik') else lemma
    if igei(lemma) and kis != lemma:
        for v in REGIES_VEG:
            if kis == to + v or (len(to) > 1 and kis == to[:-1] + v and to[-1] in 'aeáé'):
                return 'regies_gyanu', 'vegzodes:-' + v, ''
    if lemma.endswith('jön') and 'jő' in kis:
        return 'regies_gyanu', 'jő_alak', ''
    if kis == lemma.lower() and sor['modszer'] == 'lexikon':
        # a #94 által elemezetlen alak: végződés-leválasztás, igei tővel
        for v in ELEMEZETLEN_VEG + REGIES_VEG:
            if kis.endswith(v) and len(kis) - len(v) >= 2 and igei(kis[:-len(v)]):
                return 'regies_gyanu', 'elemezetlen:-' + v, ''
        if re.search(r'[uü]v(é|á|ék|ának|ének|ál|él|ván|vén)$', kis) or (re.search(r'(ván|vén)$', kis) and len(kis) > 5):
            return 'regies_gyanu', 'elemezetlen:v-tő', ''
    mai = sor['szotari_alak_mai']
    if lemma != mai:
        if vaz(lemma) != vaz(mai):
            return 'lemmavaltas', '%s→%s' % (lemma, mai), ''
        uj, mod = helyesiras_atvitel(alak, lemma, mai)
        if uj is None:
            return 'nem_elotag', '%s→%s' % (lemma, mai), ''
        if mod == 'karakter':
            return 'helyesiras_szabaly', 'karakter', uj
        return 'helyesiras_tabla', '%s→%s' % (lemma, mai), uj
    k = karakter_szabaly(alak)
    if k != alak:
        return 'helyesiras_szabaly', 'karakter', k
    return 'valtozatlan', '', ''


def ek_ketertelmu(alak, jegy):
    return jegy in ('mult.E1', 'mult.T3', 'mult.E3') and alak.lower().endswith(('ék', 'ák'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', default=KI_ALAP)
    a = ap.parse_args()
    tabla = tabla_beolvas()
    versek = korpusz()
    gy = collections.Counter(t for _, toks in versek for t in toks)
    kis_gy = collections.Counter()
    for t, n in gy.items():
        kis_gy[t.lower()] += n
    kis_szavak = set(kis_gy)
    igei = igei_tovek(tabla, kis_szavak)
    jegyes_kis = {}
    for alak, s in tabla.items():
        if s['regies_jegy']:
            jegyes_kis[alak.lower()] = kis_gy.get(alak.lower(), 0)
    gyakori_jegyes = set(k for k, _ in sorted(jegyes_kis.items(), key=lambda x: (-x[1], x[0]))[:GYAKORI_JEGYES])

    oszt = {}
    alak_db = collections.Counter()
    tok_db = collections.Counter()
    ek_alak = ek_tok = 0
    sorok_ki = []
    for alak in sorted(gy):
        sor = tablasor(tabla, alak)
        o, reszlet, modern = osztalyoz(alak, sor, gyakori_jegyes, igei)
        oszt[alak] = (o, sor)
        ek = ek_ketertelmu(alak, sor['regies_jegy']) if sor else False
        if ek:
            ek_alak += 1
            ek_tok += gy[alak]
        alak_db[o] += 1
        tok_db[o] += gy[alak]
        sorok_ki.append([alak, str(gy[alak]), o, reszlet, modern,
                         sor['szotari_alak'] if sor else '', sor['szotari_alak_mai'] if sor else '',
                         sor['regies_jegy'] if sor else '', sor['modszer'] if sor else '',
                         'igen' if ek else ''])

    # tokenszintű esetek
    vala_seged = vala_let = vala_nyitott = 0
    nevmas = collections.Counter()
    rea = 0
    for _, toks in versek:
        for i, t in enumerate(toks):
            k = t.lower()
            if REA_CSALAD.match(k):
                rea += 1
            if k in ('vala', 'valának'):
                if i == 0:
                    vala_let += 1
                    continue
                elo = toks[i - 1]
                o, s = oszt[elo]
                if s is None:
                    vala_nyitott += 1
                elif igei(s['szotari_alak']) and s['szotari_alak'] not in ('van', 'lesz'):
                    vala_seged += 1
                else:
                    vala_let += 1
            if k == 'a' and i + 1 < len(toks):
                kov = toks[i + 1].lower()
                for csal, rx in NEVMAS.items():
                    if rx.match(kov):
                        if csal == 'mi':
                            harmadik = toks[i + 2] if i + 2 < len(toks) else ''
                            if harmadik[:1].isupper() or harmadik.lower().endswith(('nk', 'ünk', 'unk')):
                                nevmas['mi_birtokos_gyanu'] += 1
                                continue
                        nevmas[csal] += 1

    tokszam = sum(gy.values())
    print('versek: %d, tokenek: %d, szóalak (kis-/nagybetű-érzékeny): %d, kisbetűs szóalak: %d'
          % (len(versek), tokszam, len(gy), len(kis_gy)))
    print('bemenet: %s sha256:%s; %s sha256:%s' % (KAROLI, sha256_rov(KAROLI), SZOTARI, sha256_rov(SZOTARI)))
    rend = ['valtozatlan', 'helyesiras_szabaly', 'helyesiras_tabla', 'igealak_gyakori', 'regies_lista',
            'lemmavaltas', 'regies_gyanu', 'nem_elotag', 'igealak_ritka', 'tablan_kivul']
    print('osztaly\talak\ttoken')
    for o in rend:
        print('%s\t%d\t%d' % (o, alak_db[o], tok_db[o]))
    print('ek_ketertelmu (jegyes -ék/-ák; szövegkörnyezetfüggő)\t%d\t%d' % (ek_alak, ek_tok))
    gyanu = collections.Counter(s[3].split(':')[0] for s in sorok_ki if s[2] == 'regies_gyanu')
    print('regies_gyanu bontás: %s' % dict(gyanu))
    kisb = collections.Counter(s[2] for s in sorok_ki if s[2] in ('igealak_ritka', 'regies_gyanu', 'nem_elotag'))
    llm_kis = set(s[0].lower() for s in sorok_ki if s[2] in ('igealak_ritka', 'regies_gyanu', 'nem_elotag'))
    print('LLM-jelölt alak (kis-/nagybetű-érzékeny): %d; kisbetűsen: %d' % (sum(kisb.values()), len(llm_kis)))
    print('vala/valának: segédigei (előtte igei alak) %d, létigei %d, nyitott (előző token táblán kívül) %d'
          % (vala_seged, vala_let, vala_nyitott))
    print('„a” + névmás (különírt vonatkozó): %s' % dict(nevmas))
    print('reá-család (reá, reám, reád, reánk, reátok …): %d token' % rea)

    ut = os.path.join(ROOT, a.ki)
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/karoli_modern/fedettseg.py (F96.0) — kézzel nem szerkeszthető | '
                'scope=a Károli 1908 minden tokenizált szóalakja (%d) | forras=%s (sha256:%s) + %s (sha256:%s) | '
                'tokenizálás: eszkozok/karoli_strong/tokenek.py tokenizal | mérőtábla (osztályozás), nem a kiadott réteg; '
                'a modern_szabaly oszlop csak a helyesírási osztályokban kitöltött, modell_ellenorizetlen\n'
                % (len(gy), KAROLI, sha256_rov(KAROLI), SZOTARI, sha256_rov(SZOTARI)))
        f.write('\t'.join(['alak', 'gyakorisag', 'osztaly', 'reszlet', 'modern_szabaly', 'szotari_alak',
                           'szotari_alak_mai', 'regies_jegy', 'modszer', 'ek_ketertelmu']) + '\n')
        for s in sorok_ki:
            f.write('\t'.join(s) + '\n')
    print('kiírva: %s (%d sor)' % (a.ki, len(sorok_ki)))


if __name__ == '__main__':
    main()
