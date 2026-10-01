#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a C (Gemini) oldal futtatója könyvenként; a futtat.py újrahasználva.

A futtat.py köteg- és kapulogikáját, a költségnaplót és a C gondolkodási láncát
(minimal -> low) használja; csak a minta, a könyv, a kimenet és a vezérlés új:

  minta   f22/minta_<könyv>.tsv (a sonnet_koteg.py minta parancsa állítja elő)
  kimenet f22/valaszok/c/<könyv>.jsonl, f22/futasnaplo.tsv (kumulatív költségnapló)
  prompt  f21p/prompt_v3.md (befagyasztva; indítás előtt és a futás végén is hash-ellenőrzés)
  bemenet KJV nélkül (a brief: a KJV a promptban nem igazolt), 10 vers/köteg (koteg_meret)
  modell  google/gemini-3.8-flash, gondolkodás: kötelező minimális szint (a futtat.py szerint)

A Sonnet-oldal válaszait (f22/valaszok/sonnet/) nem olvassa.

VEZÉRLŐFÁJL (f22/futtatas.txt): kulcs=érték sorok, # megjegyzés; MINDEN kulcs kötelező:
    konyv=1Móz        magyar rövidítés (a minta_<ascii>.tsv megléte kell)
    koteg_max=14      legfeljebb ennyi ÚJ köteg ebben a futásban, vagy 'mind'
    koteg_meret=10    vers/köteg (a prófétáknál 5)
    plafon_usd=3.90   kumulatív (napló-összeg) megállási küszöb, 0 < x <= 4.00

Éles hívás csak GitHub Actionsben (GITHUB_ACTIONS=true) vagy F21_ELES_HELYI=igen mellett.

Használat:
    python eszkozok/karoli_strong/f22_c_futtat.py --onteszt
    python eszkozok/karoli_strong/f22_c_futtat.py --vezerlo f22/futtatas.txt

Kilépési kódok: 0 rendben; 1 köteghiba; 2 előfeltétel/vezérlés; 3 költségplafon.
"""

import argparse
import math
import os
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ITT)
sys.path.insert(0, os.path.dirname(_ITT))
import bemenet  # noqa: E402
import fordit  # noqa: E402
import futtat  # noqa: E402
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

F22 = os.path.join(tokenek.ROOT, 'f22')
PLAFON_KEMENY = 4.00
KULCSOK = ('konyv', 'koteg_max', 'koteg_meret', 'plafon_usd')


class VezerloHiba(Exception):
    pass


def futas_id(konyv):
    """A futás azonosítója: 'c/<ascii könyv>' (a futtat.py valasz_ut-ja így a valaszok/c/ alá ír)."""
    return 'c/%s' % sonnet_koteg.ascii_nev(konyv)


def vezerlo_beolvas(ut):
    if not os.path.exists(ut):
        raise VezerloHiba('nincs vezérlőfájl: %s' % ut)
    with open(ut, encoding='utf-8') as f:
        sorok = [x.strip() for x in f.read().split('\n')]
    ert = {}
    for i, sor in enumerate(sorok, 1):
        if not sor or sor.startswith('#'):
            continue
        if '=' not in sor:
            raise VezerloHiba('%d. sor: nem kulcs=érték alakú: %r' % (i, sor))
        k, v = (x.strip() for x in sor.split('=', 1))
        if k not in KULCSOK:
            raise VezerloHiba('%d. sor: ismeretlen kulcs: %r' % (i, k))
        if k in ert:
            raise VezerloHiba('%d. sor: a(z) %s kulcs kétszer szerepel' % (i, k))
        ert[k] = v
    for k in KULCSOK:
        if k not in ert:
            raise VezerloHiba('hiányzó kötelező kulcs: %s (nincs alapérték)' % k)
    if ert['koteg_max'] == 'mind':
        km = None
    elif ert['koteg_max'].isdigit() and int(ert['koteg_max']) >= 1:
        km = int(ert['koteg_max'])
    else:
        raise VezerloHiba('a koteg_max pozitív egész vagy "mind"')
    if not ert['koteg_meret'].isdigit() or int(ert['koteg_meret']) < 1:
        raise VezerloHiba('a koteg_meret pozitív egész')
    try:
        plafon = float(ert['plafon_usd'])
    except ValueError:
        raise VezerloHiba('a plafon_usd nem szám: %r' % ert['plafon_usd'])
    if not math.isfinite(plafon) or plafon <= 0 or plafon > PLAFON_KEMENY:
        raise VezerloHiba('a plafon_usd 0 és %.2f közé kell essen' % PLAFON_KEMENY)
    return {'konyv': ert['konyv'], 'koteg_max': km, 'koteg_meret': int(ert['koteg_meret']), 'plafon_usd': plafon}


def regisztral(konyv):
    """A futás felvétele a futtat.FUTASOK-ba (kjv=False, prompt_v3, C modell)."""
    fid = futas_id(konyv)
    futtat.FUTASOK[fid] = {'modell': 'C', 'tipus': 'parosit', 'kjv': False, 'reteg': None,
                           'prompt': bemenet.PROMPT_V3_UT}
    return fid


def naplo_ok_migral(kimenet_dir):
    """A meglévő futásnapló kiegészítése az `ok` oszloppal (üres érték a régi soroknál: a 2. sor előtti hívások
    nyers válasza nem maradt meg, az okuk a naplóból csak következtethető, és hiányt nem töltünk ki).
    Igaz, ha módosított. Írás előtt összeveti: az `ok` oszlop elhagyása a régi sorokat bájtra visszaadja."""
    ut = futtat.naplo_ut(kimenet_dir)
    if not os.path.exists(ut) or os.path.getsize(ut) == 0:
        return False
    with open(ut, encoding='utf-8', newline='') as f:
        szoveg = f.read()
    sorok = szoveg.replace('\r\n', '\n').split('\n')
    veg = sorok[-1] == ''
    if veg:
        sorok = sorok[:-1]
    if sorok[0].split('\t')[-1] == 'ok':
        return False
    if sorok[0].split('\t') != futtat.NAPLO_FEJLEC:
        raise ValueError('a futásnapló fejléce nem a várt (nem migrálható): %s' % sorok[0])
    uj = [sorok[0] + '\tok'] + [s + '\t' for s in sorok[1:]]
    if ['\t'.join(s.split('\t')[:-1]) for s in uj] != sorok:
        raise ValueError('a migráció nem reprodukálja a régi sorokat')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(uj) + ('\n' if veg else ''))
    return True


def hash_hibak():
    h = sonnet_koteg.prompt_hash_hiba()
    return [h] if h else []


def futtat_konyv(ctx, v, minta_ut=None):
    """A vezérlés szerinti futás; kilépési kód."""
    fid = regisztral(v['konyv'])
    futtat.NAPLO_OK_OSZLOP = True        # F22: ok oszlop a naplóban (kapu / parse / api)
    naplo_ok_migral(ctx.kimenet_dir)
    if ctx.elvetett_dir is None:         # F22: az elvetett első próbák nyers válasza: f22/elvetett/<konyv>_<koteg>.txt
        ctx.elvetett_dir = os.path.join(ctx.kimenet_dir, 'elvetett')
    minta = futtat.minta_betolt(minta_ut or sonnet_koteg.minta_ut(v['konyv']))
    futtat.KOTEG_MERET = v['koteg_meret']
    ctx.plafon = min(ctx.plafon, v['plafon_usd'], PLAFON_KEMENY)
    print('F22 C: könyv=%s, koteg_max=%s, koteg_meret=%d, plafon (kumulatív) %.2f USD'
          % (v['konyv'], v['koteg_max'] or 'mind', v['koteg_meret'], ctx.plafon), flush=True)
    return futtat.futasok_vegrehajt(ctx, [fid], minta, v['koteg_max'])


def onteszt():
    hibak = []
    tmp = tempfile.mkdtemp()
    # vezérlés
    for rossz, miert in (('konyv=1Móz\nkoteg_max=1\nkoteg_meret=10\n', 'hiányzó plafon'),
                         ('konyv=1Móz\nkoteg_max=0\nkoteg_meret=10\nplafon_usd=3.9\n', 'koteg_max=0'),
                         ('konyv=1Móz\nkoteg_max=1\nkoteg_meret=10\nplafon_usd=4.5\n', 'plafon > 4')):
        ut = os.path.join(tmp, 'v.txt')
        with open(ut, 'w', encoding='utf-8') as f:
            f.write(rossz)
        try:
            vezerlo_beolvas(ut)
            hibak.append('a hibás vezérlés nem hibázott: %s' % miert)
        except VezerloHiba:
            pass
    ut = os.path.join(tmp, 'v.txt')
    with open(ut, 'w', encoding='utf-8') as f:
        f.write('# megjegyzés\nkonyv=1Móz\nkoteg_max=2\nkoteg_meret=10\nplafon_usd=3.90\n')
    v = vezerlo_beolvas(ut)
    if v['koteg_max'] != 2 or v['koteg_meret'] != 10:
        hibak.append('vezérlés értelmezése')
    # mock futás: 3 köteg a mintából, koteg_max=2, majd újraindítás (kihagyja a készet)
    sonnet_koteg.minta_ir(sonnet_koteg.minta_ut('1Móz', tmp), sonnet_koteg.minta_epit('1Móz')[:30])
    mut = sonnet_koteg.minta_ut('1Móz', tmp)
    mock = futtat.MockKuldo()
    ctx = futtat.Kontextus(mock, 'teszt-kulcs', tmp, plafon=PLAFON_KEMENY, alvas=lambda s: None)
    kod = futtat_konyv(ctx, v, mut)
    ut_jsonl = os.path.join(tmp, 'valaszok', 'c', '1Moz.jsonl')
    if kod != 0 or not os.path.exists(ut_jsonl):
        hibak.append('mock futás kilépési kód %s / nincs kimenet a valaszok/c/ alatt' % kod)
    elif len(futtat.koteg_sorok(futas_id('1Móz'), tmp)) != 2:
        hibak.append('a koteg_max=2 nem 2 köteget futtatott')
    v['koteg_max'] = None
    kod = futtat_konyv(ctx, v, mut)
    if len(futtat.koteg_sorok(futas_id('1Móz'), tmp)) != 3:
        hibak.append('az újraindítás nem a hiányzó 3. köteget futtatta')
    if any('f22/valaszok/sonnet' in s['nyers'][0] for s in futtat.koteg_sorok(futas_id('1Móz'), tmp)):
        hibak.append('a Sonnet-válasz a C bemenetében')
    # KJV-sor nincs a C bemenetében
    if any('KJV-TÁMPONT:' in u.split('=== A FELDOLGOZANDÓ VERSEK')[1] for _, u in mock.szovegek):
        hibak.append('KJV-TÁMPONT a feldolgozandó versekben')
    # plafon
    ctx2 = futtat.Kontextus(futtat.MockKuldo(), 'teszt-kulcs', tempfile.mkdtemp(), plafon=PLAFON_KEMENY, alvas=lambda s: None)
    v2 = dict(v, plafon_usd=0.0001)
    if futtat_konyv(ctx2, v2, mut) != futtat.KILEPES_PLAFON:
        hibak.append('a plafon nem állította meg a futást')
    # ok oszlop és az elvetett első próbák (kapu / parse / api); a régi napló migrációja
    hibak += onteszt_ok(tmp)
    futtat.NAPLO_OK_OSZLOP = False
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


def onteszt_ok(tmp):
    hibak = []
    # 1. az ok-besorolás (a kaput nem módosítja)
    jo = '[{"vers":"x"}]'
    for szoveg, finish, valasz_hiba, kh, vart in (('', 'error', None, 10, 'api'), (jo, 'stop', {'code': 429}, 10, 'api'),
                                                 ('nem json', 'stop', None, 10, 'parse'), (jo, 'stop', None, 3, 'kapu'),
                                                 (jo, 'stop', None, 0, '')):
        ert = futtat.ok_besorol(szoveg, finish, valasz_hiba, kh)
        if ert != vart:
            hibak.append('ok_besorol(%r, %r, %r, %r) = %r, várt %r' % (szoveg[:10], finish, valasz_hiba, kh, ert, vart))
    # 2. régi napló migrációja: az új oszlop üres, a régi sorok bájtra visszaállíthatók
    d = tempfile.mkdtemp()
    ut = futtat.naplo_ut(d)
    regi = '\t'.join(futtat.NAPLO_FEJLEC) + '\n' + '\t'.join(['x'] * len(futtat.NAPLO_FEJLEC)) + '\n'
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(regi)
    if not naplo_ok_migral(d) or naplo_ok_migral(d):
        hibak.append('a migráció nem egyszer, pontosan egyszer módosít')
    with open(ut, encoding='utf-8', newline='') as f:
        uj = f.read()
    sorok = uj.split('\n')
    if sorok[0].split('\t')[-1] != 'ok' or sorok[1].split('\t')[-1] != '' or '\n'.join(
            '\t'.join(s.split('\t')[:-1]) for s in sorok[:-1]) + '\n' != regi:
        hibak.append('a migrált napló nem adja vissza a régi sorokat')
    # 3. mock futás kapuhibával és nem-JSON válasszal: ok oszlop, elvetett fájlok
    d = tempfile.mkdtemp()
    ut = futtat.naplo_ut(d)
    sonnet_koteg.minta_ir(sonnet_koteg.minta_ut('1Móz', d), sonnet_koteg.minta_epit('1Móz')[:30])
    mut = sonnet_koteg.minta_ut('1Móz', d)
    elso_vers = [s['igehely'] for s in futtat.minta_betolt(mut)][:30]
    mock = futtat.MockKuldo(hibas_elso={elso_vers[0]}, nem_json_hivas={(futtat.MODELLEK['C'], 3)})
    ctx = futtat.Kontextus(mock, 'teszt-kulcs', d, plafon=PLAFON_KEMENY, alvas=lambda s: None)
    v = {'konyv': '1Móz', 'koteg_max': None, 'koteg_meret': 10, 'plafon_usd': PLAFON_KEMENY}
    kod = futtat_konyv(ctx, v, mut)
    with open(ut, encoding='utf-8') as f:
        n = [dict(zip(futtat.naplo_fejlec(), x.rstrip('\n').split('\t'))) for x in list(f)[1:] if x.strip()]
    okok = sorted(r['ok'] for r in n if r['ok'])
    if kod != 0 or 'kapu' not in okok or 'parse' not in okok or any(o not in ('kapu', 'parse', 'api') for o in okok):
        hibak.append('az ok oszlop értékei a mock futásban: %s (kilépési kód %s)' % (okok, kod))
    fajlok = sorted(os.listdir(ctx.elvetett_dir)) if os.path.isdir(ctx.elvetett_dir) else []
    if len(fajlok) != len(okok) or not all(x.startswith('1Moz_') and x.endswith('.txt') for x in fajlok):
        hibak.append('az elvetett első próbák fájljai: %s (várt %d, elnevezés 1Moz_<koteg>.txt)' % (fajlok, len(okok)))
    return hibak


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--vezerlo', default=None)
    ap.add_argument('--onteszt', action='store_true')
    ap.add_argument('--kimenet-dir', default=F22)
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    if not a.vezerlo:
        print('HIBA: --vezerlo kell (nincs alapértelmezett futás)', file=sys.stderr)
        return 2
    try:
        v = vezerlo_beolvas(a.vezerlo)
    except VezerloHiba as e:
        print('VEZÉRLŐFÁJL HIBA (%s): %s' % (a.vezerlo, e), file=sys.stderr)
        return 2
    if not os.path.exists(sonnet_koteg.minta_ut(v['konyv'])):
        print('HIBA: nincs minta: %s' % sonnet_koteg.minta_ut(v['konyv']), file=sys.stderr)
        return 2
    hk = hash_hibak() + futtat.v3_elofeltetelek()
    if hk:
        for x in hk:
            print('BEFAGYASZTÁS HIBA: %s' % x, file=sys.stderr)
        return 2
    print('prompt_v3 hash: rendben (a futás elején)', flush=True)
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('HIBA: az OPENROUTER_API_KEY környezeti változó nincs beállítva', file=sys.stderr)
        return 2
    if getattr(fordit._valodi_http_kuldo, '__module__', '') == fordit.__name__ \
            and os.environ.get('GITHUB_ACTIONS') != 'true' and os.environ.get('F21_ELES_HELYI') != 'igen':
        print('HIBA: éles OpenRouter-hívás helyben tiltott; az éles futás a workflow dolga', file=sys.stderr)
        return 2
    ctx = futtat.Kontextus(fordit._valodi_http_kuldo, api_key, a.kimenet_dir, plafon=PLAFON_KEMENY)
    kod = futtat_konyv(ctx, v)
    hv = hash_hibak()
    print('prompt_v3 hash a futás végén: %s' % ('RENDBEN' if not hv else 'ELTÉRÉS: %s' % hv[0]), flush=True)
    if hv:
        kod = max(kod, 2)
    print('kész; kilépési kód: %d; a napló összege: %.4f USD (plafon %.2f)'
          % (kod, futtat.naplo_osszeg(a.kimenet_dir), ctx.plafon), flush=True)
    return kod


if __name__ == '__main__':
    sys.exit(main())
