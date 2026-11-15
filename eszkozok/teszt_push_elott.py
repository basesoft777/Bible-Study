#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_push_elott.py -- F216: a `eszkozok/push_elott.py` tesztje.

Fut: python eszkozok/teszt_push_elott.py (a CI szabály-teszt lépésében is). Kilépési kód: 0 = zöld.
"""

import io
import os
import subprocess
import sys
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import push_elott as P

HIBAK = []


def ellenoriz(feltetel, nev):
    if feltetel:
        print('RENDBEN  ' + nev)
    else:
        print('BUKOTT   ' + nev)
        HIBAK.append(nev)


def valos_workflow():
    with open(P.WORKFLOW, encoding='utf-8') as f:
        return f.read()


def main():
    wf = valos_workflow()

    # 1. a valódi workflow egyezik a lépéslistával
    ellenoriz(P.ci_egyezes() == [], 'a valódi workflow egyezik a lépéslistával')

    # 2. egy hiányzó tesztlépés a workflow-ból -> HIBA
    csonka = wf.replace('python eszkozok/teszt_gyokerok_kapuk.py', 'echo kihagyva')
    hibak = P.ci_egyezes(csonka)
    ellenoriz(any('teszt_gyokerok_kapuk.py' in h for h in hibak), 'hiányzó teszt a workflow-ból: HIBA')

    # 3. megváltozott állandó argumentum (--szigoru kiesik) -> HIBA
    gyenge = wf.replace('allitas_adat.py --minden --szigoru', 'allitas_adat.py --minden')
    ellenoriz(any('allitas_adat.py' in h for h in P.ci_egyezes(gyenge)), 'kiesett --szigoru: HIBA')

    # 4. a workflow-ban van egy új, a listán kívüli szkript -> HIBA
    uj = wf.replace('python eszkozok/teszt_proza_allitas.py', 'python eszkozok/teszt_proza_allitas.py\n          python eszkozok/teszt_uj_kapu.py')
    ellenoriz(any('teszt_uj_kapu.py' in h for h in P.ci_egyezes(uj)), 'új szkript a workflow-ban, a listán kívül: HIBA')

    # 5. az egyezés-lépés hiánya -> HIBA
    ellenoriz(any('egyezés-lépés' in h for h in P.ci_egyezes(wf.replace('--ci-egyezes', ''))), 'az egyezés-lépés hiánya: HIBA')

    # 6. a megjegyzéssor nem számít hívásnak
    ellenoriz(P.python_hivasok('# python eszkozok/x.py\n  run: python eszkozok/y.py a b\n') == [('eszkozok/y.py', ' a b')],
              'a megjegyzéssor nem hívás')

    # 7. a sorvégi folytatás egy hívássá áll össze
    folyt = P.python_hivasok('python eszkozok/z.py \\\n  --a 1 \\\n  --b 2\n')
    ellenoriz(folyt and '--a 1' in folyt[0][1] and '--b 2' in folyt[0][1], 'a sorvégi folytatás összevonva')

    # 7a. F216 / 1. ellenőrzés 1.: az egyezés-kapu nem megkerülhető
    ki = wf.replace('python eszkozok/push_elott.py --ci-egyezes', '# python eszkozok/push_elott.py --ci-egyezes')
    ellenoriz(any('egyezés-lépés' in h for h in P.ci_egyezes(ki)), 'a kikommentelt egyezés-lépés: HIBA')
    ellenoriz(any('--diff-alap' in h for h in P.ci_egyezes(wf.replace('--diff-alap', '--x-alap'))),
              'a futtat.py hívásból kiesett kötelező argumentum: HIBA')
    ellenoriz(any('--pr-alap' in h for h in P.ci_egyezes(wf.replace('--pr-alap', '--x-alap'))),
              'a feladatok.py hívásból kiesett --pr-alap: HIBA')
    ellenoriz(any('elnémítva' in h for h in P.ci_egyezes(wf.replace('python eszkozok/teszt_push_elott.py', 'python eszkozok/teszt_push_elott.py || true'))),
              'a hívás után || true: HIBA')
    ellenoriz(any('continue-on-error' in h for h in P.ci_egyezes(wf.replace('- name: Szabaly-tesztek', '- name: Szabaly-tesztek\n        continue-on-error: true'))),
              'a bukó lépésen continue-on-error: HIBA')
    ellenoriz(any('K12' in h for h in P.ci_egyezes(wf.replace(' || [ "$K12" != "0" ]', ''))),
              'a K12 kilépési kód kiesik a feltételből: HIBA')
    ellenoriz(any('TESZT_KILEPES' in h for h in P.ci_egyezes(wf.replace('"$TESZT_KILEPES" != "0"', '"0" != "0"'))),
              'az összegző feltételből kiesik egy kilépési kód: HIBA')

    # 7b. F216 / 1. ellenőrzés 2.: az elmaradt ág száma (nem HIBA, figyelmeztetés)
    ellenoriz(P.lemaradas_szama('HEAD') == 0, 'a HEAD-hez képest nincs lemaradás')
    ellenoriz(P.lemaradas_szama('nincs-ilyen-ref') == 0, 'nem létező alap: 0 (nem HIBA)')
    rc, _, _ = P.git('rev-parse', 'HEAD~1')
    if rc == 0:
        ellenoriz(P.lemaradas_szama('HEAD') == 0, 'a lemaradás a HEAD..alap irányú')

    # 8. a lépés-futtató: bukó lépés HIBA-sorral és nyilvántartással, rendben lévő lépés nem
    fut = P.Futas()
    puf = io.StringIO()
    with redirect_stdout(puf):
        rc_jo, _ = fut.lepes('jó', [sys.executable, '-c', 'print("rendben")'])
        rc_rossz, _ = fut.lepes('rossz', [sys.executable, '-c', 'print("- `HIBA` x.md:1 -- baj"); raise SystemExit(1)'])
    ki = puf.getvalue()
    ellenoriz(rc_jo == 0 and rc_rossz == 1 and len(fut.hibas) == 1 and fut.hibas[0][0] == 'rossz', 'a futtató csak a bukó lépést jegyzi')
    ellenoriz('HIBA     rossz' in ki and '`HIBA` x.md:1' in ki, 'a bukó lépés HIBA-sora kiíródik')

    # 9. a parancssori --ci-egyezes a valódi fájlon 0
    r = subprocess.run([sys.executable, os.path.join(P.ROOT, 'eszkozok', 'push_elott.py'), '--ci-egyezes'],
                       capture_output=True, encoding='utf-8', cwd=P.ROOT)
    ellenoriz(r.returncode == 0, '--ci-egyezes kilépési kódja 0')

    # 10. F223: a részleges mód leképezése és a biztonsági szabály
    mind = frozenset(P.LEPES_AZON)
    ellenoriz(P.erintett_lepesek([('M', 'F223_RESZLEGES_KAPU_BRIEF.md')])[0] == {P.L_E18},
              'brief-fejléc-változás: csak az E18 érintett (a csomag-, adat- és tesztlépések kimaradnak)')
    ellenoriz(P.erintett_lepesek([('M', 'naplok/F223_jelentes.md'), ('A', 'dontesek/uj/x.md'), ('M', '.claude/commands/kovetkezo.md')])[0] == set(),
              'csak .md napló/döntés/parancs: egyik kihagyható lépés sem érintett')
    ellenoriz(P.erintett_lepesek([('M', 'eszkozok/x.py')])[0] == mind, 'kódváltozás: minden lépés érintett')
    ellenoriz(P.erintett_lepesek([('M', '.github/workflows/ellenorzes.yml')])[0] == mind, 'workflow-változás: minden lépés érintett')
    adat = P.erintett_lepesek([('M', 'adat/elofordulasok.tsv')])[0]
    ellenoriz(adat and P.L_E1 in adat and P.L_GYOKEROK in adat and P.L_E18 not in adat and P.L_TESZT_SZABALY not in adat,
              'adatváltozás: az adatkapuk érintettek, az E18 és a szabály-tesztek nem')
    for ismeretlen in ('valami.xyz', 'naplok/szkript.py', 'naplok/adat.tsv', '.claude/settings.json', 'uj_konyvtar/x.md'):
        ek, ok = P.erintett_lepesek([('M', 'F223_RESZLEGES_KAPU_BRIEF.md'), ('M', ismeretlen)])
        ellenoriz(ek is None and ismeretlen in ok, 'ismeretlen fájl (%s): teljes kapu' % ismeretlen)
    for st in ('D', 'R', 'T', 'C'):
        ellenoriz(P.erintett_lepesek([(st, 'naplok/x.md')])[0] is None, 'a(z) %s státuszú változás: teljes kapu' % st)
    ellenoriz(P.fajl_lepesei('naplok\\x.md') == frozenset(), 'a Windows-útvonal perjelre normalizálódik')

    # 10a. a minta-leképezés nem üres, és minden lépés-azonosító szerepel legalább egy mintában
    ellenoriz(set().union(*[l for _, _, l in P.RESZLEGES_LEKEPEZES]) == mind, 'minden lépés-azonosítót legalább egy minta érint')

    # 10b. az E35 (csomagexport-összevetés) brieffejlécre, naplóra és .md-re nem indul; adat-táblára és az exportgenerátorra igen
    sys.path.insert(0, os.path.join(P.ROOT, 'eszkozok', 'ellenorzes'))
    import szabalyok as SZ
    ellenoriz(SZ.e35_kivalto_fajlok(['F223_RESZLEGES_KAPU_BRIEF.md', 'naplok/F223_jelentes.md', 'CSAPDAK.md']) == [],
              'E35: a brief, a napló és a .md nem váltja ki')
    ellenoriz(SZ.e35_kivalto_fajlok(['adat/elofordulasok.tsv', 'eszkozok/nyilt_mag_export.py']) ==
              ['adat/elofordulasok.tsv', 'eszkozok/nyilt_mag_export.py'], 'E35: az adat-tábla és az exportgenerátor kiváltja (a leképezés mindkettőt a teljes körbe vonja)')

    # 10c. a futó lépések a zöld jegyzésből
    def vf(sorok):
        return lambda honnan, fej: sorok

    f_, ok = P.lepesek_futtatasa({}, 'f' * 40, vf([]))
    ellenoriz(f_ == mind and all('első futás' in v for v in ok.values()), 'zöld jegyzés nélkül (első futás): minden lépés fut')
    f_, _ = P.lepesek_futtatasa({l: 'a' * 40 for l in P.LEPES_AZON}, 'a' * 40, vf(None))
    ellenoriz(f_ == set(), 'a jegyzett fej a mostani: semmi sem fut (a diff nem is kell)')
    f_, _ = P.lepesek_futtatasa({l: 'a' * 40 for l in P.LEPES_AZON}, 'b' * 40, vf([('M', 'F1_X_BRIEF.md')]))
    ellenoriz(f_ == {P.L_E18}, 'jegyzett fej óta csak egy brief változott (pl. main-behozás): csak az E18 fut')
    f_, ok = P.lepesek_futtatasa({l: 'a' * 40 for l in P.LEPES_AZON}, 'b' * 40, vf([('M', 'F1_X_BRIEF.md'), ('M', 'ismeretlen.dat')]))
    ellenoriz(f_ == mind, 'jegyzett fej óta ismeretlen fájl: minden lépés fut')
    f_, ok = P.lepesek_futtatasa({l: 'a' * 40 for l in P.LEPES_AZON}, 'b' * 40, vf(None))
    ellenoriz(f_ == mind and all('nem olvasható' in v for v in ok.values()), 'a diff nem olvasható: minden lépés fut')
    vegyes = {l: 'a' * 40 for l in P.LEPES_AZON}
    del vegyes[P.L_E1]
    f_, _ = P.lepesek_futtatasa(vegyes, 'b' * 40, vf([('M', 'naplok/x.md')]))
    ellenoriz(f_ == {P.L_E1}, 'csak a jegyzés nélküli lépés fut, ha a változás egyiket sem érinti')

    # 10d. a zöld jegyzés: kör-oda-vissza, hibás/más verziójú fájl érvénytelen
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        ut = os.path.join(td, P.ZOLD_FAJL)
        ellenoriz(P.zold_beolvas(ut) == {}, 'nincs jegyzésfájl: üres')
        P.zold_ment(ut, {P.L_E1: 'c' * 40})
        ellenoriz(P.zold_beolvas(ut) == {P.L_E1: 'c' * 40}, 'a jegyzés kör-oda-vissza egyezik')
        with open(ut, 'w', encoding='utf-8') as f:
            f.write('{"verzio": %d, "lepesek": {"%s": "c"}}' % (P.ZOLD_VERZIO + 1, P.L_E1))
        ellenoriz(P.zold_beolvas(ut) == {}, 'más verziójú jegyzés: érvénytelen (teljes kapu)')
        with open(ut, 'w', encoding='utf-8') as f:
            f.write('nem json')
        ellenoriz(P.zold_beolvas(ut) == {}, 'olvashatatlan jegyzés: érvénytelen (teljes kapu)')
        with open(ut, 'w', encoding='utf-8') as f:
            f.write('{"verzio": %d, "lepesek": {"ismeretlen-lepes": "c"}}' % P.ZOLD_VERZIO)
        ellenoriz(P.zold_beolvas(ut) == {}, 'ismeretlen lépés-azonosító a jegyzésben: eldobva')

    # 10e. a leképezés lefedi a `--ci-egyezes` lépéslistát: a teljes kaput a --reszleges nem gyengíti
    ellenoriz(P.ci_egyezes() == [], 'a részleges mód nem változtatja a CI-egyezést')

    print()
    if HIBAK:
        print('BUKOTT: %d teszt: %s' % (len(HIBAK), '; '.join(HIBAK)))
        return 1
    print('Minden teszt zöld.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
