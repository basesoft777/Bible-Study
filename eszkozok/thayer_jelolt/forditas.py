#!/usr/bin/env python
"""A Thayer szakaszonkénti fordításának lánca: az M3 parancsai (F132; DT-F132b (3), DT-F132c, DT-F132d (1), DT-F132h).

A #128 BDB-ágának (`eszkozok/emeles.py szakasz_*`) Thayer-párja; a #128 fájljait nem módosítja, a szótárfüggetlen elemeket
importálja: a helyőrzőket, a terminológiát, a Károli-táblát és a kötelező alakokat (`emeles.py`), a javítóréteget
(`normalizal.py`), a tokent, a kulcsot és a csoportosítást (`bdb_jelolt/szakasz_bemenet.py`, a `thayer_bemenet.py`-on át), a
közös kapukat (`forditas_kapuk.kapuk_futtat_szakaszos`, benne `14_szakasz`, `15_tiltott`) a `16_sigla`-val (`thayer_kapuk.py`).
Prompt: `forditas/prompt_v5_1.md` (DT-F132k (2): a v5 + „Kiegészítő szabály (v5.1) — Thayer-szócikk”); `{{ADATBLOKK}}`:
`thayer_jelolt/adatblokk.py`.

Ez a modul NEM fordít: a fordítást a hívó (az M3 Sonnet-menete, DT-F132d (S), DT-F132g) végzi a kiírt promptokból.

  lista       az M3 futási listája (szolista.py; DT-F132h) -> --ki
  elokeszit   STRONG --mappa M: tokenes forrás, helyőrzős változat, csoportonként a prompt (adatblokkal), meta
  ellenoriz   STRONG --be VÁZLAT [--mappa M] [--ki VÉGLEGES]: helyőrző-visszaállítás, javítóréteg, kapuk
  rogzit      STRONG --be VÉGLEGES --allapot sonnet|opus|kezi --modell NÉV: a munkatáblába (naplok/F132_THAYER_SZAKASZ_munka.tsv),
              szakaszonként `jelentes_szam = sz<n>`, `forras_hash` = a szakasz SHA-1-e; kapuhiba esetén nem rögzít
  beir        STRONG… --allapot …: a munkatábla szakaszsorai az adat/forditasok.tsv-be; a régi `teljes` sor: nem `kezi` ->
              `--regi-elavult`-tal `elavult` (DT-F132c (i)); `kezi` -> nem `kezi` szakaszsor csak `--kezi-marad`-dal, a régi
              sor érvényes marad (DT-F132c (ii)); jóváhagyott (`--allapot kezi`) sor `--regi-elavult --kezi-felulir`-ral.
              Minden más sor bájtra változatlan (írás előtt ellenőrizve).

  python eszkozok/thayer_jelolt/forditas.py elokeszit G1941 --mappa <scratchpad>/m3
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import datetime
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
ESZK = os.path.join(GYOKER, 'eszkozok')
for _u in (ITT, ESZK):
    if _u not in sys.path:
        sys.path.insert(0, _u)
import adatblokk  # noqa: E402
import emeles as E  # noqa: E402
import kulcs  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402
import thayer_kapuk as TK  # noqa: E402

SZOTAR = TB.SZOTAR
PROMPT_UT = os.path.join(GYOKER, 'forditas', 'prompt_v5_1.md')  # DT-F132k (2): a v5 + Thayer-kiegészítés; a v5 a BDB-é
FORDITASOK_UT = E.FORDITASOK_UT
MUNKA_UT = os.path.join(GYOKER, 'naplok', 'F132_THAYER_SZAKASZ_munka.tsv')
FEJLEC = E.FORDITASOK_FEJLEC
ALLAPOTOK = E.ALLAPOTOK


def forras(strong):
    sp = kulcs.strong_pad(strong)
    szak = TB.szakaszok(sp) if sp else None
    if szak is None:
        raise SystemExit('%s nincs a thayer_szakaszok.tsv-ben' % strong)
    return sp, szak


def prompt_epit(sp, csoport, darab_info=''):
    """Az `emeles.prompt_epit` Thayer-párja: azonos helyőrzők, az `{{ADATBLOKK}}` a Thayer-adatblokk."""
    with open(PROMPT_UT, encoding='utf-8') as fh:
        sablon = fh.read().split(E.PROMPT_JELOLO, 1)[1].lstrip('\n')
    term, _ = E.terminologia_szoveg()
    f = TB.tokenes(csoport)
    return (sablon
            .replace('{{SZOTAR}}', SZOTAR)
            .replace('{{TERMINOLOGIA}}', term)
            .replace('{{KAROLI_TABLA}}', E.karoli_szoveg())
            .replace('{{STRONG}}', kulcs.strong_eredeti(sp))
            .replace('{{DARAB_MEGJEGYZES}}', darab_info)
            .replace('{{KOTELEZO_ALAKOK}}', E.kotelezo_alakok_szoveg(TB.nezet(csoport)))
            .replace('{{ADATBLOKK}}', adatblokk.blokk(sp, csoport))
            .replace('{{FORRAS_SZOVEG}}', f))


def cmd_lista(a):
    ts = a.ts or datetime.date.today().isoformat()
    sorok = szolista.lista(ts)
    szoveg = szolista.fajl_szoveg(sorok, ts)
    if a.ki:
        E.kiir(szoveg, a.ki)
    else:
        sys.stdout.write(szoveg)


def cmd_elokeszit(a):
    sp, szak = forras(a.strong)
    os.makedirs(a.mappa, exist_ok=True)
    alap = os.path.join(a.mappa, sp)
    tok = TB.tokenes(szak)
    bontott, hely = E.helyorzo_bont(tok)
    E.kiir(tok, alap + '_szakasz_forras.txt')
    E.kiir(bontott, alap + '_szakasz_hely.txt')
    with open(alap + '_szakasz_hely.json', 'w', encoding='utf-8') as fh:
        json.dump(hely, fh, ensure_ascii=False, indent=0)
    cs = TB.csoportok(szak)
    meta = {'strong': sp, 'szotar': SZOTAR, 'illesztes': szak[0]['illesztes'],
            'szakaszok': [{'sorszam': x['sorszam'], 'hash': x['hash'], 'hossz': len(x['szoveg'])} for x in szak],
            'csoportok': [[x['sorszam'] for x in c] for c in cs]}
    with open(alap + '_szakasz.json', 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    for i, c in enumerate(cs):
        E.kiir(prompt_epit(sp, c, E.darab_info_szoveg(i, len(cs))), '%s_c%d_prompt.md' % (alap, i + 1))
    print('%s: %d szakasz, %d csoport, %d helyőrző; illesztés: %s' % (sp, len(szak), len(cs), len(hely), szak[0]['illesztes']))


def utofeldolgoz(sp, szak, nyers, kivetel=()):
    """-> (végleges, változások, kapueredmények, átment)."""
    import normalizal as N
    import forditas_kapuk as K
    f_tok, f_nt = TB.tokenes(szak), TB.nezet(szak)
    vegleges, valt = N.normalizal(nyers, SZOTAR)
    vegleges, csere = K.terminologia_kisnagybetu_csere(f_nt, vegleges, bizonytalan_lista=list(kivetel))
    valt = list(valt) + [('5_kisnagybetu %s -> %s (%s)' % (alak, kot, angol), db) for angol, alak, kot, db in csere]
    eredm = TK.kapuk_futtat_thayer(f_tok, vegleges, bizonytalan=kivetel)
    return vegleges, valt, eredm, TK.atment(eredm)


def cmd_ellenoriz(a):
    sp, szak = forras(a.strong)
    with open(a.be, encoding='utf-8') as fh:
        vazlat = fh.read().strip('\n')
    if a.mappa:
        with open(os.path.join(a.mappa, sp + '_szakasz_hely.json'), encoding='utf-8') as fh:
            hely = json.load(fh)
        vazlat, hiany, tobbszor = E.helyorzo_visszaallit(vazlat, hely)
        if hiany or tobbszor:
            print('FIGYELEM: hiányzó helyőrzők %s; többször használt %s' % (hiany, tobbszor))
    vegleges, valt, eredm, ok = utofeldolgoz(sp, szak, vazlat, a.kivetel)
    print('javítóréteg: %s' % (', '.join('%s=%d' % v for v in valt) or 'nincs változás'))
    for n, e, r in eredm:
        print('  %-22s %-8s %s' % (n, e, r))
    print('ATMENT' if ok else 'BUKOTT')
    if a.ki:
        E.kiir(vegleges, a.ki)
    return 0 if ok else 1


def szakasz_sorok(sp, szak, szoveg, allapot, modell, datum, term_verzio, megjegyzes):
    import forditas_kapuk as K
    eleje, hu = K.szakasz_bont(szoveg)
    if eleje or [n for n, _ in hu] != [x['sorszam'] for x in szak]:
        raise SystemExit('a fordítás tokenjei nem a forrás szakaszai (%s)' % sp)
    return [{'szotar': SZOTAR, 'strong': sp, 'entry_id': kulcs.strong_eredeti(sp), 'jelentes_szam': TB.jelentes_szam(n),
             'mezo': 'forditas_hu', 'forras_hash': x['hash'], 'forditas_hu': t, 'allapot': allapot, 'modell': modell,
             'datum': datum, 'terminologia_verzio': term_verzio, 'megjegyzes': megjegyzes}
            for (n, t), x in zip(hu, szak)]


def cmd_rogzit(a):
    sp, szak = forras(a.strong)
    with open(a.be, encoding='utf-8') as fh:
        szoveg = fh.read().strip('\n')
    if '\t' in szoveg or '\n' in szoveg:
        raise SystemExit('a fordítás tabot vagy sortörést tartalmaz — TSV-be nem írható')
    vegleges, valt, eredm, ok = utofeldolgoz(sp, szak, szoveg, a.kivetel)
    if vegleges != szoveg:
        raise SystemExit('a --be nem a javítóréteg kimenete (futtasd előbb: ellenoriz --ki)')
    if not ok:
        raise SystemExit('kapuhiba — a sorok nem rögzíthetők (önújrapróba, utána naplok/F132_THAYER_SZAKASZ_bukottak.tsv)')
    _, term_verzio = E.terminologia_szoveg()
    megj = '; '.join(x for x in (
        a.megjegyzes or '',
        ('terminológia-kivétel (bizonytalan_feloldasok): ' + ', '.join(a.kivetel)) if a.kivetel else '') if x)
    uj = szakasz_sorok(sp, szak, szoveg, a.allapot, a.modell, a.datum or datetime.date.today().strftime('%Y.%m.%d'),
                       term_verzio, megj)
    sorok = list(E.tsv_dict_sorok(MUNKA_UT)) if os.path.exists(MUNKA_UT) else []
    sorok = [r for r in sorok if not (r['szotar'] == SZOTAR and r['strong'] == sp)] + uj
    E.tsv_ir(MUNKA_UT, FEJLEC, sorok, megjegyzes='F132 munkatábla (adat/forditasok.tsv sémája) — beírás előtt; '
                                                'írja: python eszkozok/thayer_jelolt/forditas.py rogzit')
    print('rögzítve: Thayer %s, %d szakaszsor (%d karakter) -> %s'
          % (sp, len(uj), sum(len(r['forditas_hu']) for r in uj), os.path.relpath(MUNKA_UT, GYOKER)))


def beir(strongok, allapot, datum=None, megjegyzes=None, regi_elavult=False, kezi_felulir=False, kezi_marad=False,
         munka_ut=None, forditasok_ut=None):
    """A munkatábla szakaszsorainak beírása (l. a modul docstringjét). -> a változott/új sorok száma."""
    munka_ut, forditasok_ut = munka_ut or MUNKA_UT, forditasok_ut or FORDITASOK_UT
    munka = list(E.tsv_dict_sorok(munka_ut))
    with open(forditasok_ut, encoding='utf-8', newline='') as fh:
        eredeti = fh.read()
    sorok = eredeti.split('\n')
    assert sorok[-1] == '', 'a forditasok.tsv nem sortöréssel végződik'
    sorok = sorok[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    assert sorok[fej_i].split('\t') == FEJLEC, sorok[fej_i]
    datum = datum or datetime.date.today().strftime('%Y.%m.%d')
    i_all, i_megj = FEJLEC.index('allapot'), FEJLEC.index('megjegyzes')
    idx = {tuple(s.split('\t')[:5]): i for i, s in enumerate(sorok) if i > fej_i and s and not s.startswith('#')}
    valtozott = set()
    for s in strongok:
        sp, szak = forras(s)
        sajat = [r for r in munka if r['szotar'] == SZOTAR and r['strong'] == sp and TB.sorszam_jelentesbol(r['jelentes_szam']) is not None]
        if [TB.sorszam_jelentesbol(r['jelentes_szam']) for r in sajat] != [x['sorszam'] for x in szak]:
            raise SystemExit('%s: a munkatábla szakaszsorai nem fedik le a szakaszokat (rogzit előbb)' % sp)
        if [r['forras_hash'] for r in sajat] != [x['hash'] for x in szak]:
            raise SystemExit('%s: a munkatábla forras_hash-e nem a mai szakaszoké — újra rögzítendő' % sp)
        teljes_k = (SZOTAR, sp, kulcs.strong_eredeti(sp), 'teljes', 'forditas_hu')
        regi_marad = False
        if teljes_k in idx:
            regi = sorok[idx[teljes_k]].split('\t')
            if regi[i_all] == 'kezi' and allapot != 'kezi':
                if not kezi_marad:
                    raise SystemExit('%s: a régi `teljes` sor `kezi` — nem `kezi` szakaszsorok csak --kezi-marad-dal (DT-F132c (ii))' % sp)
                regi_marad = True
            elif regi[i_all] == 'kezi' and not kezi_felulir:
                raise SystemExit('%s: a régi `teljes` sor `kezi` — jóváhagyott szakaszsorok csak --kezi-felulir-ral' % sp)
            if not regi_marad and not regi_elavult:
                raise SystemExit('%s: van régi `teljes` sor — --regi-elavult kell (DT-F132c (i))' % sp)
            if not regi_marad and regi[i_all] != 'elavult':
                regi[i_all] = 'elavult'
                regi[i_megj] = '; '.join(x for x in (regi[i_megj], 'felváltva: szakaszonkénti fordítás (%s; DT-F132c)' % datum) if x)
                sorok[idx[teljes_k]] = '\t'.join(regi)
                valtozott.add(idx[teljes_k])
        for r in sajat:
            r = dict(r, allapot=allapot, datum=datum)
            if megjegyzes:
                r['megjegyzes'] = megjegyzes
            uj = '\t'.join(r.get(m, '') for m in FEJLEC)
            k = tuple(uj.split('\t')[:5])
            if k in idx:
                if sorok[idx[k]].split('\t')[i_all] == 'kezi' and not kezi_felulir:
                    raise SystemExit('védett kezi sor: %s' % (k,))
                sorok[idx[k]] = uj
                valtozott.add(idx[k])
            else:
                sorok.append(uj)
                idx[k] = len(sorok) - 1
                valtozott.add(len(sorok) - 1)
    for i, s in enumerate(eredeti.split('\n')[:-1]):
        if i not in valtozott and sorok[i] != s:
            raise SystemExit('váratlan eltérés a %d. sorban — megállok' % (i + 1))
    for s in sorok:
        assert s.startswith('#') or len(s.split('\t')) == len(FEJLEC), s[:80]
    with open(forditasok_ut, 'w', encoding='utf-8', newline='') as fh:
        fh.write('\n'.join(sorok) + '\n')
    return len(valtozott)


def cmd_beir(a):
    n = beir(a.strongok, a.allapot, a.datum, a.megjegyzes, a.regi_elavult, a.kezi_felulir, a.kezi_marad)
    print('adat/forditasok.tsv: %d sor változott/új (%s)' % (n, ', '.join(a.strongok)))


def parser():
    ap = argparse.ArgumentParser(description='F132: a Thayer szakaszonkénti fordításának lánca')
    al = ap.add_subparsers(dest='parancs', required=True)
    p = al.add_parser('lista')
    p.add_argument('--ki')
    p.add_argument('--ts')
    p.set_defaults(fv=cmd_lista)
    p = al.add_parser('elokeszit')
    p.add_argument('strong')
    p.add_argument('--mappa', required=True, help='kimeneti mappa (a repón kívül)')
    p.set_defaults(fv=cmd_elokeszit)
    p = al.add_parser('ellenoriz')
    p.add_argument('strong')
    p.add_argument('--be', required=True)
    p.add_argument('--mappa')
    p.add_argument('--ki')
    p.add_argument('--kivetel', nargs='*', default=[])
    p.set_defaults(fv=cmd_ellenoriz)
    p = al.add_parser('rogzit')
    p.add_argument('strong')
    p.add_argument('--be', required=True)
    p.add_argument('--allapot', required=True, choices=ALLAPOTOK)
    p.add_argument('--modell', required=True, help='a fordító tényleges modell-azonosítója (a saját környezetből); kötelező')
    p.add_argument('--datum')
    p.add_argument('--megjegyzes')
    p.add_argument('--kivetel', nargs='*', default=[])
    p.set_defaults(fv=cmd_rogzit)
    p = al.add_parser('beir')
    p.add_argument('strongok', nargs='+')
    p.add_argument('--allapot', required=True, choices=ALLAPOTOK)
    p.add_argument('--datum')
    p.add_argument('--megjegyzes')
    p.add_argument('--regi-elavult', action='store_true')
    p.add_argument('--kezi-felulir', action='store_true')
    p.add_argument('--kezi-marad', action='store_true')
    p.set_defaults(fv=cmd_beir)
    return ap


def main():
    a = parser().parse_args()
    r = a.fv(a)
    return r or 0


if __name__ == '__main__':
    sys.exit(main())
