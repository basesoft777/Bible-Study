#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_elott.py -- F216: helyi kapu push előtt. Ugyanazt futtatja, amit a
`.github/workflows/ellenorzes.yml` bukó lépései (az ág saját fején; a CI a PR és a main összefésült fáján fut, ezért
lemaradt ágnál FIGYELEM jelzi a lemaradást), így a HIBA a push előtt derül ki, nem a CI-ben
(egy piros CI-kör kb. 4 perc és egy session-kör).

A szabály (egy hely): `.claude/commands/kovetkezo.md`, „PUSH ELŐTT” szakasz. A `/kiadas` 6. lépése és a `/lap-javit`
csak hivatkozik rá.

Használat (a repó gyökeréből, az ág commitjai után, push előtt):
    python eszkozok/push_elott.py                      # az alap: a `git merge-base origin/main HEAD`
    python eszkozok/push_elott.py --alap origin/main   # más alap
    python eszkozok/push_elott.py --pr-cim "[ELLENŐRZŐ] ..."   # az E16-hoz (alapból a nyitott PR címe, ha a `gh` látja)
    python eszkozok/push_elott.py --lepes E18          # csak a nevében a szöveget tartalmazó lépések (javítás utáni gyors újrafutás;
                                                       # a push előtti kapu a teljes futás)
    python eszkozok/push_elott.py --reszleges          # F223: csak az érintett lépések (l. lent); ismeretlen fájlnál a teljes kapu
    python eszkozok/push_elott.py --gyors              # munka közbeni gyors próba (cél: legfeljebb 5 perc); NEM push előtti kapu
    python eszkozok/push_elott.py --ci-egyezes         # csak annak ellenőrzése, hogy a lépéslista egyezik a workflow-val
Kilépési kód: 0 = 0 HIBA (push mehet), 1 = van HIBA, 2 = futási hiba.

Részleges mód (F223, `--reszleges`; csak helyi, a CI mindig a teljes futás): kis változásra ne fusson újra a teljes kapu.
Minden lépéshez (LEPES_AZON) a `RESZLEGES_LEKEPEZES` mondja meg, mely változott útvonalak teszik érintetté (egy hely).
Egy lépés akkor fut, ha (1) nincs róla zöld jegyzés (az ág első futása: minden lépés fut), vagy (2) az utolsó zöld futása óta
(`git diff <akkori fej> HEAD`; ez a main-behozás utáni változást is tartalmazza) olyan fájl változott, amely a lépés
mintájára illeszkedik. Az E2-E39 (futtat.py) minden változott fájlra fut: maga is diff-hatókörű. Biztonsági szabály: ha egy
változott fájl egyik mintára sem illeszkedik, vagy a fájl törlődött/átneveződött/típust váltott, vagy a jegyzés/diff nem
olvasható, a teljes kapu fut. A jegyzés a `git rev-parse --git-dir` alatti `push_elott_zold.json`; csak tiszta fán, teljes
(nem `--lepes`) futás után frissül, a bukott lépésé törlődik.

Gyors próba (`--gyors`; munka közben, a push előtti kapu helyett soha): csak a változáshoz kötött ellenőrzések. A változás az utolsó zöld
gyors próba óta (a `.git` alatti `push_elott_gyors.json`; nincs, vagy nem őse a fejnek: az ág teljes diffje). Fut: az E2–E39 a változott
fájlokra (a diff alapja a gyors pont), a hash-őr, és a `GYORS_LEKEPEZES` szerint érintett lépés (E1, E38–E39, kinyerő-ellenőrzés, E18); a
tesztfájl csak akkor, ha maga változott, vagy a forrása név szerint hivatkozik egy változott `eszkozok/` modulra (`gyors_tesztek`). A
lapgenerálás (F217) csak akkor, ha a diff a generátort vagy a lap bemenetét érinti (`lap_erintes`: a bemeneti jegyzék útvonalai), és
`motivumok/<ID>.md`-nél csak az érintett lapra (`--id`). Az olvasó-tesztek nem futnak (a teljes kapu futtatja). Ismeretlen fájl nem kér
teljes kaput. A zöld jegyzéshez (`--reszleges`) nem nyúl. A push előtt, a PR előtt egyszer: a teljes kapu.

Olvasó-tesztek (F232, DT-F232a (b)): ha az ág az olvasó kódját érinti (`teszt_futtat.py` `_OLVASO_KOD`), a kapu a `teszt_futtat.py --gyors`
móddal fel is futtatja az olvasó gyors tesztjeit (a lassú `teszt_szintek.py` és `teszt_arculat.py` nélkül; a teljes sor a menet saját
futása) és az olvasói mércét (`teszt_olvasoi_merce.py`) a helyi `pardes.db`-n; egy elbukott tesztfájl egyszer újrafut (ingadozás:
jelzés, nem bukás); másodszor is piros: a kapu 1-et ad.
A mérce eltérése figyelmeztetés (a diff a futás kimenetében). Ez a lépés CSAK helyi: a CI-ben nincs teszt-adatbázis (N-F232a).
Gép sora (`eszkozok/gepsor.py`; MUNKAMENET „Menet-ellenőrzés”, 5. pont): a teljes kapu (nem `--reszleges`, nem `--lepes`) egészében a gép
közös FIFO-sorában fut; a részleges és a `--lepes` futás csak a lapot generáló lépéseket (F217 generált nézetek, E2–E39: az E28 is generál)
futtatja a sorban. A sor mindig a helyi ellenőrzés-zár (`ellenorzes.zar`) előtt veendő, soha nem utána.
Bekötés-összevetés (OLVASO-GYORS, 2026-11-23): ugyanitt fut a `bekotesi_leltar.py --osszevet <alap>`: HIBA, ha az olvasóban az alapon (merge-base)
látszó blokk, tábla vagy adatkészlet az ágon nem látszik, feltételhez kötött vagy másik fülön áll (`olvaso_szerver/merce/bekotes_kivetel.tsv`: kivétel, indokkal).

A lépéslista (LEPESEK) az egyetlen forrás a helyi futáshoz; a `--ci-egyezes` (a CI-ben is fut) megbukik, ha a
`.github/workflows/ellenorzes.yml` bukó lépései eltérnek tőle: egy Python-hívás hiányzik valamelyik oldalról, vagy egy
állandó argumentumú hívás szövege (pl. `--szigoru`) más, a futási adattól függő hívásokból kötelező argumentum hiányzik,
a `--ci-egyezes` lépés ki van kommentelve, vagy a bukó lépés némítva van (`continue-on-error: true`, `|| true`, nem
szereplő `K<n>` kilépési kód). A CI-ben csak jelentés-lépések (tanulmány-audit, PR-komment)
maradhatnak a lépéslistán kívül (EGYEZES_KIVETEL).
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, '.github', 'workflows', 'ellenorzes.yml')
PY = sys.executable

# A CI-ben a futtat.py jelentésében a szabályonkénti minta (alap: 3) a HIBA-sorok megjelenítéséhez kevés lehet.
MINTA = '50'

# Állandó argumentumú hívások: a szövegük szó szerint szerepel a workflow-ban (a --ci-egyezes ezt ellenőrzi).
# A `None`-t tartalmazó (futási adattól függő) hívások csak szkript-szinten egyeznek.
STATIKUS_TESZTEK = [
    'eszkozok/ellenorzes/tesztek/test_szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_tanulmany.py',
    'eszkozok/teszt_ellenoriz_31.py',
    'eszkozok/teszt_ellenoriz_32.py',
    'eszkozok/teszt_ellenoriz_33.py',
    'eszkozok/teszt_ellenoriz_35.py',
    'eszkozok/teszt_gyokerok_kapuk.py',
    'eszkozok/teszt_hatastortenet.py',
    'eszkozok/teszt_proza_allitas.py',
    'eszkozok/teszt_push_elott.py',
    'eszkozok/teszt_gepsor.py',
    'eszkozok/ellenorzes/tesztek/test_zar.py',
    'eszkozok/teszt_brief_lezaras.py',
    'eszkozok/teszt_lepes_jelzes.py',
    'eszkozok/teszt_generalt_nezetek.py',
    'eszkozok/olvaso_szerver/teszt_tervor.py',
]
STATIKUS_HIVASOK = [
    'eszkozok/ellenorzes/kovetelmeny_kapu.py HAMART-001 --szigoru',
    'eszkozok/ellenorzes/allitas_adat.py --minden --szigoru',
    'eszkozok/proza_allitas.py --kapu',
    'eszkozok/visszhang/tanu_kinyer.py ellenoriz',
    'eszkozok/szakirodalom_kinyer.py ellenoriz',
    'eszkozok/teszt_feladatok.py',
] + STATIKUS_TESZTEK
# Futási adattól függő hívások (a workflow-ban változókkal): a szkript-útvonal egyezik.
DINAMIKUS_SZKRIPTEK = [
    'eszkozok/ellenorzes/futtat.py',
    'eszkozok/ellenorzes/study_fajlok_szurese.py',
    'eszkozok/ellenoriz.py',
    'eszkozok/feladatok.py',
    'eszkozok/generalt_nezetek.py',
    'eszkozok/lapgen/hash_or_kapu.py',
]
# A futási adattól függő hívások kötelező argumentumai (a hívásaik egyikében szerepelniük kell).
DINAMIKUS_ARGUMENTUMOK = {
    'eszkozok/ellenorzes/futtat.py': ['--valtozott', '--diff-alap', '--diff-fej', '--pr-cim', '--esemeny',
                                      '--commit-uzenet-fajl', '--minta'],
    'eszkozok/ellenoriz.py': ['--md'],
    'eszkozok/feladatok.py': ['ellenoriz', '--pr-alap'],
    'eszkozok/generalt_nezetek.py': ['--ir', '--pr-modositott'],
    'eszkozok/lapgen/hash_or_kapu.py': ['--valtozott-lista'],
}
# Csak a CI-ben futó, nem bukó jelentés-lépések.
EGYEZES_KIVETEL = [
    'eszkozok/ellenorzes/tanulmany_audit.py',
    'eszkozok/ellenorzes/pr_komment.py',
]
# A workflow-ban kötelező, a CI-egyezést őrző lépés.
EGYEZES_PARANCS = 'eszkozok/push_elott.py --ci-egyezes'


# ---------------------------------------------------------------------------
# F223: részleges mód -- lépés -> érintő útvonalminták (egy hely)
# ---------------------------------------------------------------------------
# A részleges módban kihagyható lépések azonosítói. Az E2-E39 (futtat.py) és a CI-egyezés nincs köztük: mindig futnak.
L_E1 = 'E1'                       # study-szűrés + ellenoriz.py
L_GYOKEROK = 'E38-E39'            # követelménylista- és állítás-adat kapu
L_TESZT_SZABALY = 'teszt-szabaly'  # test_szabalyok.py, test_tanulmany.py
L_TESZT_KAPU = 'teszt-kapuk'      # teszt_ellenoriz_3x, gyokerok_kapuk, hatastortenet, proza_allitas, push_elott, brief_lezaras
L_TESZT_KINYER = 'teszt-kinyer'   # tanu_kinyer.py / szakirodalom_kinyer.py ellenoriz
L_E18 = 'E18'                     # feladatok.py ellenoriz + tesztjei
LEPES_AZON = (L_E1, L_GYOKEROK, L_TESZT_SZABALY, L_TESZT_KAPU, L_TESZT_KINYER, L_E18)

_MIND = frozenset(LEPES_AZON)
_ADAT_KONYVTAR = (r'(?:adat|konkordancia|lexikon|motivumok|motivumlog|tematikus_lezart|genezis|ujszovetseg|melyelemzesek|'
                  r'nyilt_mag|visszhang|generalt|generalt_proba|forditas|kozlemeny|bovitmenyek|f21p|f22|f172|fp2|nyilt_karoli_strong|'
                  r'nyilt_karoli_modern)')
# (név, minta, az érintett lépések). Egy fájl érintett lépései az illeszkedő sorok uniói; az üres halmaz: csak az E2-E39
# fut (a fájl ismert, és egyetlen kihagyható lépés sem függ tőle). Egyik sorra sem illeszkedő fájl: teljes kapu.
RESZLEGES_LEKEPEZES = [
    # a kód és a CI minden lépést érint (a tesztek és a kapuk is itt élnek)
    ('kód és CI', r'^(?:eszkozok|\.github)/', _MIND),
    # a sablonokat a generátorok és a kapuk olvassák
    ('sablonok', r'^sablonok/', _MIND),
    # adat és generált/forrás réteg: az adatkapuk és a kinyerő-ellenőrzések; a szabály-tesztek fixture-rel futnak
    ('adat- és forrásrétegek', r'^' + _ADAT_KONYVTAR + r'/', frozenset({L_E1, L_GYOKEROK, L_TESZT_KINYER, L_TESZT_KAPU})),
    # döntés- és nyitott-tétel-nyilvántartás: az ellenoriz.py hivatkozás-szabályai olvassák
    ('nyilvántartások', r'^(?:DONTESEK|NYITOTT_FELADATOK)\.md$', frozenset({L_E1})),
    # brieffejlécek, a feladatkövető generált blokkja és térképe (E18: a PR a generált fájlt nem módosíthatja)
    ('briefek', r'^(?:F\d+_[\w]+_BRIEF|FELADATOK)\.md$|^(?:FELADATTERKEP\.html|feladatterkep\.json)$',
     frozenset({L_E18})),
    # a feladatkövető a kontextus-olvasási fájlok méretét/szintjét is méri (feladatok.py KONTEXTUS_OLVAS, SZINT_KONNYITETT_FAJL)
    ('szabályfájlok', r'^(?:CLAUDE|CSAPDAK|MUNKAMENET|BRIEF_SABLON)\.md$', frozenset({L_E18})),
    # csak olvasott/emberi dokumentumok: egyetlen kihagyható lépés sem függ tőlük (csak .md; a naplok/ alatti .py/.tsv/.txt
    # fájlt kód tölti be, az ismeretlen: teljes kapu)
    ('naplók, PR-onkénti tételek, parancsok', r'^(?:naplok|dontesek|nyitott|beerkezo|archivum|\.claude/commands|\.claude/agents)/.*\.md$',
     frozenset()),
    ('gyökér-dokumentumok', r'^(?:MUNKATERV|README)\.md$', frozenset()),
]
ZOLD_FAJL = 'push_elott_zold.json'
ZOLD_VERZIO = 1   # a RESZLEGES_LEKEPEZES vagy a lépés-azonosítók módosításakor nő: a régi jegyzés érvénytelen


def fajl_lepesei(fajl, lekepezes=None):
    """Egy változott fájl érintett lépései (frozenset), vagy None, ha ismeretlen (egyik mintára sem illeszkedik)."""
    lekepezes = RESZLEGES_LEKEPEZES if lekepezes is None else lekepezes
    fajl = fajl.replace('\\', '/')
    talalt = False
    erintett = set()
    for _nev, minta, lepesek in lekepezes:
        if re.match(minta, fajl):
            talalt = True
            erintett |= set(lepesek)
    return frozenset(erintett) if talalt else None


def erintett_lepesek(valtozasok, lekepezes=None):
    """A változások `[(státusz, útvonal), ...]` alapján (git diff --name-status; az átnevezés/másolás státusza R/C, a törlésé D,
    a típusváltásé T) az érintett lépések halmaza és az indoklás. A halmaz None: teljes kapu kell (ismeretlen fájl vagy nem
    csak hozzáadás/módosítás)."""
    erintett = set()
    for st, fajl in valtozasok:
        if st not in ('A', 'M'):
            return None, 'a(z) %s fájl állapota %s (törlés/átnevezés/típusváltás): teljes kapu' % (fajl, st)
        ln = fajl_lepesei(fajl, lekepezes)
        if ln is None:
            return None, 'ismeretlen útvonal (nincs rá minta): %s -- teljes kapu' % fajl
        erintett |= ln
    return erintett, ''


def olvaso_erintett(fajlok):
    """F232: a változott fájlok közül az olvasó kódja (a `teszt_futtat.py` `_OLVASO_KOD` listája: az egy hely; az `adat/` és a
    `konkordancia/` nem: azok változására az olvasó tesztjei nem indulnak, a lassúakat a `--diff` a `LASSU_LEFEDETT` szerint választja)."""
    if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import teszt_futtat
    ki = []
    for f in fajlok:
        n = f.replace('\\', '/')
        if any(n == e or (e.endswith('/') and n.startswith(e)) for e in teszt_futtat._OLVASO_KOD):
            ki.append(n)
    return ki


def fuggo_tesztek(fajlok):
    """F232 (ELLENOR_F232 1.): azok a gyors tesztfájlok (`teszt_futtat.py` `GYORS_FUGGO`), amelyeknek egy közvetlen bemenete változott,
    de az olvasó kódja nem (ott a `--diff` az egész készletet futtatja). Rendezett lista."""
    if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import teszt_futtat
    valtozott = {f.replace('\\', '/') for f in fajlok}
    return sorted(t for t, bemenetek in teszt_futtat.GYORS_FUGGO.items() if valtozott & set(bemenetek))


def olvaso_tesztek_futtatasa(fut, nev, argv, py=None):
    """F232 (orkesztrátori döntés, 2026-11-22): az olvasó-tesztek egy lépése ingadozás-védelemmel. Az első futás után minden elbukott
    tesztfájlt (`[teszt_futtat] <fájl>: HIBA`) egyszer újrafuttat (`teszt_futtat.py --fajl`); ha az ismétlés zöld, a kimenet jelzi, hogy
    ingadozott (N-F232c), és a lépés nem bukik; ha másodszor is piros, a lépés bukik. Az újrafuttatás nélküli hiba (pl. környezeti,
    kilépési kód 2, vagy nem azonosítható fájl) azonnal bukik. Visszaad: (kilépési kód, a futások kimenete, ingadozott fájlok listája)."""
    py = py or PY
    n_hibas, n_sor = len(fut.hibas), len(fut.hiba_sorok)
    rc, ki = fut.lepes(nev, argv)
    if rc != 1:
        return rc, ki, []
    bukott = sorted(set(re.findall(r'\[teszt_futtat\] (teszt_\w+\.py): HIBA', ki)))
    if not bukott:
        return rc, ki, []
    print('FIGYELEM: elbukott olvasó-teszt (%s); egyszeri újrafuttatás (ingadozás-védelem, N-F232c)' % ', '.join(bukott))
    del fut.hibas[n_hibas:]
    del fut.hiba_sorok[n_sor:]
    rc2, ki2 = fut.lepes(nev + ' -- újrafuttatás', [py, 'eszkozok/teszt_futtat.py'] + [x for f in bukott for x in ('--fajl', f[:-3])])
    ujra_bukott = set(re.findall(r'\[teszt_futtat\] (teszt_\w+\.py): HIBA', ki2)) if rc2 != 0 else set()
    ingadozott = [f for f in bukott if f not in ujra_bukott] if rc2 != 2 else []
    if ingadozott:
        print('FIGYELEM: INGADOZÓ olvasó-teszt (elsőre piros, az ismétlésre zöld): %s -- a lépés nem áll meg; a teszt javítása az N-F232c.'
              % ', '.join(ingadozott))
    return rc2, ki + ki2, ingadozott


# Gyors próba (`--gyors`): lépés -> a változott útvonalak, amelyek érintik (a kód általános sora nélkül: kódnál csak a lépés saját szkriptje).
GYORS_LEKEPEZES = [
    (L_E1, r'^' + _ADAT_KONYVTAR + r'/|^sablonok/|^(?:DONTESEK|NYITOTT_FELADATOK)\.md$|^eszkozok/(?:ellenoriz\.py|ellenorzes/study_fajlok_szurese\.py)$'),
    (L_GYOKEROK, r'^' + _ADAT_KONYVTAR + r'/|^sablonok/|^eszkozok/ellenorzes/(?:kovetelmeny_kapu|allitas_adat)\.py$'),
    (L_TESZT_KINYER, r'^adat/|^eszkozok/visszhang/|^eszkozok/szakirodalom_kinyer\.py$'),
    (L_E18, r'^(?:F\d+_[\w]+_BRIEF|FELADATOK|CLAUDE|CSAPDAK|MUNKAMENET|BRIEF_SABLON)\.md$|^(?:FELADATTERKEP\.html|feladatterkep\.json)$'
            r'|^eszkozok/(?:teszt_)?feladatok\.py$'),
]
GYORS_FAJL = 'push_elott_gyors.json'
# a lapgenerátor saját kódja és táblái; a többi bemenet a bemeneti jegyzékből (`adat/lapgen_bemenetek.tsv` `utvonal`)
LAP_KOD = r'^eszkozok/(?:lapgen/|general\.py$|generalt_nezetek\.py$)|^adat/(?:lapgen_|generalt_nezetek\.tsv$)'


def gyors_lepesek(fajlok):
    """A gyors próbában futó kihagyható lépések (set)."""
    ki = set()
    for f in fajlok:
        f = f.replace('\\', '/')
        for l, minta in GYORS_LEKEPEZES:
            if re.search(minta, f):
                ki.add(l)
    return ki


def gyors_tesztek(fajlok, tesztek=None, olvas=None):
    """A gyors próbában futó tesztfájlok: a változott tesztfájl, és az a teszt, amely egy változott `eszkozok/` alatti Python-modult betölt:
    `import M` / `from M import` (csomagon át is), vagy fájlútról, a puszta `'M.py'` névvel (a könyvtárral együtt idézett útvonal adat, nem
    betöltés: pl. egy lépéslista-fixture)."""
    tesztek = STATIKUS_TESZTEK if tesztek is None else tesztek
    olvas = olvas or (lambda t: open(os.path.join(ROOT, t), encoding='utf-8', errors='replace').read())
    valtozott = {f.replace('\\', '/') for f in fajlok}
    modulok = {os.path.splitext(os.path.basename(f))[0] for f in valtozott if f.startswith('eszkozok/') and f.endswith('.py')}
    ki = []
    for t in tesztek:
        if t in valtozott:
            ki.append(t)
            continue
        try:
            forras = olvas(t)
        except OSError:
            ki.append(t)   # nem olvasható: inkább fut
            continue
        if any(re.search(r'(?m)^\s*(?:import|from)\s+(?:[\w.]+\.)?' + re.escape(m) + r'(?![\w])', forras)
               or re.search(r'(?m)^\s*(?:from\s+[\w.]+\s+)?import\s+[\w., ]*(?<![\w.])' + re.escape(m) + r'(?![\w])', forras)
               or re.search(r'[\'"]' + re.escape(m) + r'\.py[\'"]', forras) for m in modulok):
            ki.append(t)
    return ki


def _bemenet_mintak(gyoker=ROOT):
    """A bemeneti jegyzék útvonalai regexként (a `<ID>` csoport: a lap azonosítója; a `*` egy útvonaltag)."""
    mintak = []
    try:
        with open(os.path.join(gyoker, 'adat', 'lapgen_bemenetek.tsv'), encoding='utf-8') as f:
            sorok = f.read().split('\n')
    except OSError:
        return None
    fej = None
    for sor in sorok:
        if not sor or sor.startswith('#'):
            continue
        mezok = sor.split('\t')
        if fej is None:
            fej = mezok
            continue
        if 'utvonal' not in fej or len(mezok) <= fej.index('utvonal'):
            continue
        for ut in mezok[fej.index('utvonal')].split(';'):
            ut = ut.strip()
            if not ut or ut == '-':
                continue
            r = re.escape(ut).replace(re.escape('<ID>'), r'(?P<id>[A-Z0-9]+-\d+)').replace(r'\*', r'[^/]*')
            mintak.append(re.compile('^' + r + '$'))
    return mintak


def lap_erintes(fajlok, gyoker=ROOT):
    """(érintett-e a lap, ID-lista vagy None = minden lap). A generátor kódja és a közös bemenet minden lapot érint; a `motivumok/<ID>.md`
    és az `<ID>`-s bemenet csak a sajátját. A jegyzék olvashatatlan: minden lap."""
    mintak = _bemenet_mintak(gyoker)
    if mintak is None:
        return True, None
    idk, mind = set(), False
    for f in fajlok:
        f = f.replace('\\', '/')
        if re.search(LAP_KOD, f):
            mind = True
            continue
        for m in mintak:
            t = m.match(f)
            if t:
                if 'id' in m.groupindex and t.group('id'):
                    idk.add(t.group('id'))
                else:
                    mind = True
    if mind:
        return True, None
    return bool(idk), sorted(idk)


def gyors_pont(fej):
    """Az utolsó zöld gyors próba feje, ha a mostani fej őse (különben None)."""
    import json
    rc, gitdir, _ = git('rev-parse', '--git-dir')
    if rc != 0:
        return None, None
    ut = os.path.join(gitdir if os.path.isabs(gitdir) else os.path.join(ROOT, gitdir), GYORS_FAJL)
    try:
        with open(ut, encoding='utf-8') as f:
            sha = json.load(f).get('fej')
    except (OSError, ValueError, AttributeError):
        return None, ut
    if not isinstance(sha, str) or git('merge-base', '--is-ancestor', sha, fej)[0] != 0:
        return None, ut
    return sha, ut


def zold_utvonal():
    rc, gitdir, _ = git('rev-parse', '--git-dir')
    if rc != 0 or not gitdir:
        return None
    return os.path.join(gitdir if os.path.isabs(gitdir) else os.path.join(ROOT, gitdir), ZOLD_FAJL)


def zold_beolvas(ut):
    """A lépésenkénti zöld jegyzés: {lépés: fej-sha}; üres, ha nincs, olvashatatlan vagy más verziójú."""
    import json
    try:
        with open(ut, encoding='utf-8') as f:
            adat = json.load(f)
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(adat, dict) or adat.get('verzio') != ZOLD_VERZIO or not isinstance(adat.get('lepesek'), dict):
        return {}
    return {k: v for k, v in adat['lepesek'].items() if k in LEPES_AZON and isinstance(v, str)}


def zold_ment(ut, jegyzes):
    import json
    with open(ut, 'w', encoding='utf-8') as f:
        json.dump({'verzio': ZOLD_VERZIO, 'lepesek': jegyzes}, f, ensure_ascii=False, indent=1)


def valtozasok_git(honnan, fej):
    """`git diff --name-status` a két commit közt: [(státusz, útvonal)] vagy None, ha nem olvasható (pl. az akkori fej
    már nincs meg). Az átnevezésnél mindkét útvonal sorként, R státusszal áll (teljes kaput kér)."""
    rc, ki, _ = git('diff', '--name-status', '--no-renames', honnan, fej)
    if rc != 0:
        return None
    sorok = []
    for s in ki.splitlines():
        r = s.split('\t', 1)
        if len(r) == 2:
            sorok.append((r[0][:1], r[1]))
    return sorok


def lepesek_futtatasa(zold, fej, valtozasok_fn=valtozasok_git, lekepezes=None):
    """Mely lépések futnak. `zold`: {lépés: fej-sha}. Visszaad: (futó lépések halmaza, {lépés: indok}). A lépés fut, ha nincs zöld jegyzése, ha a jegyzett fej
    és a mostani közti változás nem értékelhető (teljes kapu), vagy ha a változás érinti."""
    futo = {}
    cache = {}
    for l in LEPES_AZON:
        sha = zold.get(l)
        if not sha:
            futo[l] = 'nincs zöld jegyzés (első futás ezen az ágon)'
            continue
        if sha == fej:
            continue
        if sha not in cache:
            vk = valtozasok_fn(sha, fej)
            cache[sha] = (None, 'a jegyzett fej (%s) és a mostani közti diff nem olvasható: teljes kapu' % sha[:8]) \
                if vk is None else erintett_lepesek(vk, lekepezes)
        erintett, ok = cache[sha]
        if erintett is None:
            futo[l] = ok
        elif l in erintett:
            futo[l] = 'a(z) %s óta érintő fájl változott' % sha[:8]
    return set(futo), futo


def git(*args):
    r = subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True, encoding='utf-8')
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def lemaradas_szama(alap_ref='origin/main'):
    """Hány commit van az `alap_ref`-ben, ami a HEAD-ben nincs (0: naprakész; nem állapítható meg: 0). Figyelmeztetés, nem HIBA."""
    rc, ki, _ = git('rev-list', '--count', 'HEAD..' + alap_ref)
    return int(ki) if rc == 0 and ki.isdigit() else 0


def python_hivasok(szoveg):
    """A workflow szövegéből a `python <eszkozok/...py> <argok>` hívások (megjegyzéssorok nélkül), soronként
    összevonva (a sorvégi `\\` folytatást egy sorrá)."""
    egy = re.sub(r'\\\s*\n\s*', ' ', megjegyzes_nelkul(szoveg))
    return re.findall(r'python\s+(eszkozok/[\w./-]+\.py)([^\n]*)', egy)


def megjegyzes_nelkul(szoveg):
    """A workflow szövege a teljes soros megjegyzések nélkül (a kikommentelt lépés nem számít lépésnek)."""
    ki = []
    for s in szoveg.splitlines():
        if s.lstrip().startswith('#'):
            continue
        m = re.search(r'\s#', s)   # sor végi megjegyzés (`run: # python ...`), ha az idézőjelek előtte párosak
        if m and s[:m.start()].count('"') % 2 == 0 and s[:m.start()].count("'") % 2 == 0:
            s = s[:m.start()]
        ki.append(s)
    return '\n'.join(ki)


def lepesek_szerint(szoveg):
    """A workflow lépései (`- name:` kezdetű blokkok), megjegyzéssorok nélkül; a fejléc nincs benne."""
    return re.split(r'(?m)^\s*- name:', megjegyzes_nelkul(szoveg))[1:]


def ci_egyezes(szoveg=None):
    """A lépéslista és a workflow egyezése (szoveg: a workflow szövege; alap: a fájl). Visszaadja a hibák listáját."""
    if szoveg is None:
        try:
            with open(WORKFLOW, encoding='utf-8') as f:
                szoveg = f.read()
        except OSError as exc:
            return ['a workflow nem olvasható: %s' % exc]
    hivasok = python_hivasok(szoveg)
    ci_szkriptek = {h[0] for h in hivasok}
    egy_szoveg = re.sub(r'\s+', ' ', megjegyzes_nelkul(szoveg))
    hibak = []
    var = set(DINAMIKUS_SZKRIPTEK) | {s.split()[0] for s in STATIKUS_HIVASOK} | set(EGYEZES_KIVETEL)
    var.add('eszkozok/push_elott.py')
    for sz in sorted(ci_szkriptek - var):
        hibak.append('a workflow-ban van, a push_elott.py lépéslistáján nincs: %s' % sz)
    for sz in sorted((set(DINAMIKUS_SZKRIPTEK) | {s.split()[0] for s in STATIKUS_HIVASOK}) - ci_szkriptek):
        hibak.append('a push_elott.py lépéslistáján van, a workflow-ban nincs: %s' % sz)
    for h in STATIKUS_HIVASOK:
        if 'python ' + h not in egy_szoveg:
            hibak.append('a workflow-ban a hívás szövege eltér: python %s' % h)
    # a futási adattól függő hívások kötelező argumentumai (a hívásaik valamelyikében)
    for sz, kotelezo in sorted(DINAMIKUS_ARGUMENTUMOK.items()):
        argok = ' '.join(a for s_, a in hivasok if s_ == sz)
        for k in kotelezo:
            if not re.search(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', argok):
                hibak.append('a workflow-ban a(z) %s hívásából hiányzik: %s' % (sz, k))
    # az egyezés-lépés: megjegyzés nélküli szövegben szerepel (a kikommentelt nem számít)
    if not any(sz == 'eszkozok/push_elott.py' and '--ci-egyezes' in a for sz, a in hivasok):
        hibak.append('a workflow-ban nincs egyezés-lépés: python %s' % EGYEZES_PARANCS)
    # a bukó lépés tényleg bukhat
    for lepes in lepesek_szerint(szoveg):
        bukok = [sz for sz, _ in python_hivasok(lepes) if sz not in EGYEZES_KIVETEL]
        if not bukok:
            continue
        nev = lepes.split('\n', 1)[0].strip()
        if re.search(r'continue-on-error:\s*true', lepes):
            hibak.append('a bukó lépés nem bukhat (continue-on-error: true): %s' % nev)
        for sz, a in python_hivasok(lepes):
            if sz not in EGYEZES_KIVETEL and re.search(r'\|\|\s*(true|:|exit\s+0)(?!\w)', a):
                hibak.append('a hívás kilépési kódja elnémítva (|| true): python %s' % sz)
        sorok = lepes.splitlines()
        for kv in sorted(set(re.findall(r'(?m)^\s*(\w+)=\$\?\s*$', lepes))):
            minta = r'\$\{?%s\}?(?!\w)' % re.escape(kv)
            if not any(re.search(minta, s) for s in sorok if not re.match(r'\s*%s=' % re.escape(kv), s)):
                hibak.append('a kilépési kód nem szerepel a feltételben (%s): %s' % (kv, nev))
    # az összegző lépés feltételében mindhárom kilépési kód szerepel
    felt = '\n'.join(s for s in megjegyzes_nelkul(szoveg).splitlines() if s.lstrip().startswith('if ['))
    for kv in ('E2E16_KILEPES', 'E1_KILEPES', 'TESZT_KILEPES'):
        if not re.search(r'\$%s' % kv, felt):
            hibak.append('a bukás-lépés feltételében hiányzik: %s' % kv)
    return hibak


TMP_KONYVTAR = None   # a lépések ideiglenes könyvtára (a main() állítja be)


def ideiglenes_konyvtar():
    """Ideiglenes könyvtár a repóval azonos meghajtón. Windowson a szabály-tesztek (test_szabalyok.py) a repó gyökeréhez
    képest relatív útvonalat képeznek az ideiglenes fájlokból, és ez más meghajtón ValueError-ral bukik (pl. a worktree
    E:-n, a %TEMP% C:-n). Ilyenkor a meghajtó gyökerében készül a könyvtár."""
    alap = None
    if os.name == 'nt':
        if os.path.splitdrive(tempfile.gettempdir())[0].lower() != os.path.splitdrive(ROOT)[0].lower():
            alap = os.path.splitdrive(ROOT)[0] + os.sep + 'push_elott_tmp'
            os.makedirs(alap, exist_ok=True)
    return tempfile.mkdtemp(prefix='push_elott_', dir=alap)


class Futas:
    def __init__(self, szuro=None):
        self.szuro = szuro
        self.hibas = []   # (lépés, kilépési kód)
        self.hiba_sorok = []

    def lepes(self, nev, argv, stdin_szoveg=None, fajlba=None):
        """Egy lépés: stdout+stderr összegyűjtve. Kiírja az állapotot; HIBA esetén a HIBA-sorokat, vagy a kimenet végét."""
        if self.szuro and self.szuro not in nev:
            return 0, ''
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        if TMP_KONYVTAR:
            env.update(TEMP=TMP_KONYVTAR, TMP=TMP_KONYVTAR, TMPDIR=TMP_KONYVTAR)
        t0 = time.time()
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, encoding='utf-8', errors='replace',
                           input=stdin_szoveg, env=env)
        felirat = '%s [%d mp]' % (nev, time.time() - t0)
        kimenet = (r.stdout or '') + (('\n' + r.stderr) if r.stderr else '')
        if fajlba:
            with open(fajlba, 'w', encoding='utf-8') as f:
                f.write(r.stdout or '')
        if r.returncode == 0:
            print('RENDBEN  %s' % felirat)
        else:
            print('HIBA     %s (kilépési kód: %d)' % (felirat, r.returncode))
            self.hibas.append((nev, r.returncode))
            sorok = kimenet.splitlines()
            hiba = [s for s in sorok if 'HIBA' in s or 'SÉRTÉS' in s or 'FAIL' in s or 'Error' in s or 'Traceback' in s]
            minta = hiba if hiba else sorok[-25:]
            for s in minta[:80]:
                print('   ' + s)
            if len(minta) > 80:
                print('   ... és további %d sor' % (len(minta) - 80))
            self.hiba_sorok.extend(hiba)
        return r.returncode, kimenet


def main():
    ap = argparse.ArgumentParser(description='F216: a CI bukó lépései helyben, push előtt.')
    ap.add_argument('--alap', default=None, help='a diff alapja (alap: git merge-base origin/main HEAD)')
    ap.add_argument('--pr-cim', default=None, help='a PR címe (E16); alap: a nyitott PR címe, ha a gh elérhető')
    ap.add_argument('--lepes', default=None, help='csak a nevében ezt a szöveget tartalmazó lépések futnak (a teljes futás a kapu)')
    ap.add_argument('--reszleges', action='store_true',
                    help='F223: csak az érintett lépések futnak (l. a modul leírását); ismeretlen fájlnál a teljes kapu')
    ap.add_argument('--gyors', action='store_true',
                    help='munka közbeni gyors próba (l. a modul leírását); nem push előtti kapu')
    ap.add_argument('--ci-egyezes', action='store_true', help='csak a lépéslista és a workflow egyezését ellenőrzi')
    args = ap.parse_args()

    if args.ci_egyezes:
        hibak = ci_egyezes()
        for h in hibak:
            print('HIBA: ' + h)
        if hibak:
            return 1
        print('RENDBEN: a push_elott.py lépéslistája és a workflow egyezik.')
        return 0
    return sorban(args)


def sorban(args):
    """A teljes kapu a gép közös sorában (`gepsor.py`); a részleges és a `--lepes` futás csak a lapot generáló lépéseknél áll sorba
    (`lap_sor`). A sorban állás a gyerekfolyamatokra öröklődik (`PARDES_SOR_TARTVA`), így a lépések nem állnak be újra."""
    if args.gyors and (args.reszleges or args.lepes):
        print('HIBA: a --gyors nem kombinálható a --reszleges / --lepes kapcsolóval.', file=sys.stderr)
        return 2
    if args.reszleges or args.lepes or args.gyors:
        return kapu(args)
    import gepsor
    with gepsor.Sor('push_elott.py teljes kapu (%s)' % ROOT):
        return kapu(args)


def lap_sor(nev):
    """A lapot generáló lépés sora (a teljes kapuban már sorban áll: akkor nem csinál semmit)."""
    import gepsor
    return gepsor.Sor('push_elott.py: %s (%s)' % (nev, ROOT))


def kapu(args):

    rc, fej, _ = git('rev-parse', 'HEAD')
    if rc != 0:
        print('HIBA: nem git-munkakönyvtár.', file=sys.stderr)
        return 2
    git('fetch', '-q', 'origin', 'main')
    alap_ref = args.alap or 'origin/main'
    rc, alap, hiba = git('merge-base', alap_ref, 'HEAD')
    if rc != 0:
        print('HIBA: a merge-base nem állapítható meg (%s): %s' % (alap_ref, hiba), file=sys.stderr)
        return 2
    lemaradas = lemaradas_szama(alap_ref)
    if lemaradas:
        print('FIGYELEM: az ág %d committal le van maradva az %s-hez képest; a CI a PR és a main összefésült fáján fut '
              '(refs/pull/N/merge), a kapu az ág saját fején. Fésüld be a main-t (merge vagy rebase), és futtasd újra.'
              % (lemaradas, alap_ref))
    rc, nem_commitolt, _ = git('status', '--porcelain')
    if nem_commitolt:
        print('FIGYELEM: nem commitolt változás van; a CI csak a commitokat látja (alap..HEAD), a kapu is azokat.')
    rc, valtozott, _ = git('diff', '--name-only', alap, fej)
    fajlok = [s for s in valtozott.splitlines() if s]
    rc, uzenetek, _ = git('log', '--format=%B', '%s..%s' % (alap, fej))
    pr_cim = args.pr_cim
    if pr_cim is None:
        pr_cim = ''
        try:
            r = subprocess.run(['gh', 'pr', 'view', '--json', 'title', '-q', '.title'], cwd=ROOT,
                               capture_output=True, encoding='utf-8', timeout=30)
            if r.returncode == 0:
                pr_cim = r.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    print('push_elott: alap %s, fej %s, %d változott fájl, PR-cím: %s' % (alap[:8], fej[:8], len(fajlok), pr_cim or '(nincs)'))
    gyors_ut = None
    if args.gyors:
        pont, gyors_ut = gyors_pont(fej)
        if pont == fej:
            print('push_elott --gyors: a fej (%s) az utolsó zöld gyors próba óta nem változott; nincs mit futtatni.' % fej[:8])
            return 0
        if pont:
            alap = pont
            rc, valtozott, _ = git('diff', '--name-only', alap, fej)
            fajlok = [s for s in valtozott.splitlines() if s]
            rc, uzenetek, _ = git('log', '--format=%B', '%s..%s' % (alap, fej))
        print('push_elott --gyors: GYORS PRÓBA, nem push előtti kapu; a változás %s óta (%s): %d fájl'
              % (alap[:8], 'az utolsó zöld gyors próba' if pont else 'az ág alapja', len(fajlok)))

    fut = Futas(args.lepes)
    global TMP_KONYVTAR
    tmp = TMP_KONYVTAR = ideiglenes_konyvtar()

    # F223: mely kihagyható lépések futnak (teljes mód: mind)
    zold_ut = zold_utvonal()
    zold = zold_beolvas(zold_ut) if zold_ut else {}
    futo = set(LEPES_AZON)
    if args.gyors:
        futo = gyors_lepesek(fajlok) | {L_TESZT_SZABALY, L_TESZT_KAPU}   # a tesztfájlok egyenként szűrve (gyors_tesztek)
        teszt_szuro = set(gyors_tesztek(fajlok))
        print('push_elott --gyors: lépések: %s; tesztek: %s' % (
            ', '.join(l for l in LEPES_AZON if l in futo - {L_TESZT_SZABALY, L_TESZT_KAPU}) or '-',
            ', '.join(os.path.basename(t) for t in STATIKUS_TESZTEK if t in teszt_szuro) or '-'))
    if args.reszleges:
        futo, indokok = lepesek_futtatasa(zold, fej)
        if futo:
            print('push_elott: részleges mód, futó lépések: %s' % ', '.join(l for l in LEPES_AZON if l in futo))
            for l in LEPES_AZON:
                if l in futo:
                    print('  %s: %s' % (l, indokok[l]))
        kihagyott = [l for l in LEPES_AZON if l not in futo]
        if kihagyott:
            print('push_elott: kihagyva (nem érinti a változás): %s' % ', '.join(kihagyott))
    lepes_eredmeny = {}   # lépés-azonosító -> True, ha minden alépése futott és rendben volt

    def kihagyhato(azon, nev, argv, **kw):
        """A kihagyható lépés egy alépése: ha az azonosító nem futó, kihagyva; különben fut, és az eredmény a jegyzéshez gyűlik."""
        if azon not in futo:
            return 0, ''
        rc, ki = fut.lepes(nev, argv, **kw)
        if not (args.lepes and args.lepes not in nev):
            lepes_eredmeny[azon] = lepes_eredmeny.get(azon, True) and rc == 0
        return rc, ki

    # 0. a lépéslista egyezik a workflow-val
    for h in ci_egyezes():
        print('HIBA     CI-egyezés: %s' % h)
        fut.hibas.append(('CI-egyezés', 1))
        fut.hiba_sorok.append(h)

    # 0b. F217: a generált nézetek ideiglenes újragenerálása (mint a CI-ben): a lemezt olvasó kapuk a friss nézeten
    # futnak. A munkapéldány generált fájljai a futás végén visszaállnak (a PR nem commitol generált nézetet).
    sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
    import generalt_nezetek
    generalt_kep = generalt_nezetek.pillanatkep(ROOT)
    _, modositott, _ = git('diff', '--name-only', '--diff-filter=M', alap, fej)
    modositott_fajl = os.path.join(tmp, 'pr_modositott.txt')
    with open(modositott_fajl, 'w', encoding='utf-8') as f:
        f.write(modositott + '\n')
    lap_kell, lap_idk = lap_erintes(fajlok) if args.gyors else (True, None)
    if not lap_kell:
        print('KIHAGYVA F217 generált nézetek (gyors próba: a diff nem érinti a generátort és a lap bemenetét)')
    else:
        id_arg = [x for i in (lap_idk or []) for x in ('--id', i)]
        with lap_sor('F217 generált nézetek'):
            rc_gen, ki_gen = fut.lepes('F217 generált nézetek (generalt_nezetek.py --ir%s)' % (' ' + ' '.join(id_arg) if id_arg else ''), [
                PY, 'eszkozok/generalt_nezetek.py', '--ir', '--jelentes', os.path.join(tmp, 'generalt_jelentes.md'),
                '--pr-modositott', modositott_fajl] + id_arg)

    # 1. E2-E39 (mindig fut: diff-hatókörű szabályok; az E35/E28 maguk is csak az érintő fájlokra)
    uzenet_fajl = os.path.join(tmp, 'commit_uzenetek.txt')
    with open(uzenet_fajl, 'w', encoding='utf-8') as f:
        f.write(uzenetek + '\n')
    if fajlok:
        with lap_sor('E2-E39'):
            fut.lepes('E2-E39 (futtat.py)', [
                PY, 'eszkozok/ellenorzes/futtat.py', '--valtozott'] + fajlok + [
                '--diff-alap', alap, '--diff-fej', fej, '--pr-cim', pr_cim, '--esemeny', 'pull_request',
                '--commit-uzenet-fajl', uzenet_fajl, '--minta', MINTA])
    else:
        print('RENDBEN  E2-E39 (nincs változott fájl)')
    if args.lepes:
        print('FIGYELEM: részleges futás (--lepes %s); a push előtti kapu a teljes futás.' % args.lepes)

    # 1/b. az új lapgenerátor regressziós mércéjének hash-őre (F218a; mindig fut, maga dönti el, érinti-e a változás)
    lista_fajl = os.path.join(tmp, 'valtozott_fajlok.txt')
    with open(lista_fajl, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fajlok) + '\n')
    fut.lepes('F218 mérce hash-őr (hash_or_kapu.py)', [PY, 'eszkozok/lapgen/hash_or_kapu.py', '--valtozott-lista', lista_fajl])

    # 2. E1
    rc, study = kihagyhato(L_E1, 'E1 szűrés (study_fajlok_szurese.py)',
                           [PY, 'eszkozok/ellenorzes/study_fajlok_szurese.py'], stdin_szoveg='\n'.join(fajlok) + '\n')
    study_args = []
    if rc == 0:
        for sor in study.splitlines():
            if sor.strip():
                study_args += ['--study', sor.strip()]
    kihagyhato(L_E1, 'E1 (ellenoriz.py)', [PY, 'eszkozok/ellenoriz.py'] + study_args + ['--md', os.path.join(tmp, 'e1_jelentes.md')])

    # 3. E38-E39 gyökérok-kapuk
    kihagyhato(L_GYOKEROK, 'E39 követelménylista-kapu', [PY, 'eszkozok/ellenorzes/kovetelmeny_kapu.py', 'HAMART-001', '--szigoru'])
    kihagyhato(L_GYOKEROK, 'E38 állítás-adat kapu', [PY, 'eszkozok/ellenorzes/allitas_adat.py', '--minden', '--szigoru'])

    # 4. szabály-tesztek
    for t in STATIKUS_TESZTEK[:2]:
        if args.gyors and t not in teszt_szuro:
            continue
        kihagyhato(L_TESZT_SZABALY, 'teszt: ' + t, [PY, t])
    kihagyhato(L_TESZT_KINYER, 'teszt: eszkozok/visszhang/tanu_kinyer.py ellenoriz', [PY, 'eszkozok/visszhang/tanu_kinyer.py', 'ellenoriz'])
    kihagyhato(L_TESZT_KINYER, 'teszt: eszkozok/szakirodalom_kinyer.py ellenoriz', [PY, 'eszkozok/szakirodalom_kinyer.py', 'ellenoriz'])
    for t in STATIKUS_TESZTEK[2:]:
        if args.gyors and t not in teszt_szuro:
            continue
        kihagyhato(L_TESZT_KAPU, 'teszt: ' + t, [PY, t])

    # 5. feladatkövetés (E18) és tesztjei
    kihagyhato(L_E18, 'E18 feladatok.py ellenoriz', [PY, 'eszkozok/feladatok.py', 'ellenoriz', '--pr-alap', alap])
    if not args.gyors or any(f in ('eszkozok/feladatok.py', 'eszkozok/teszt_feladatok.py') for f in fajlok):
        kihagyhato(L_E18, 'feladatok.py tesztek', [PY, 'eszkozok/teszt_feladatok.py'])

    # 6. F232 (DT-F232a (b)): az olvasó tesztjei és mércéje helyben, a helyi `pardes.db`-n, ha az ág az olvasó kódját érinti.
    # A CI ezeket nem futtatja (nincs teszt-adatbázis; N-F232a: útvonal-szűrt CI a TSV-ből épített DB-n), ezért ez a kapu az
    # egyetlen védelem: piros olvasó-teszttel az ág nem jut át. Orkesztrátori döntés (2026-11-22): a kapu `--gyors` módban fut (a lassú
    # `teszt_szintek.py` és `teszt_arculat.py` nélkül: a 17–22 perces kapu minden olvasós pushnál akadály lenne); a teljes tesztsor a
    # menet saját futása a draft PR előtt. Egy elbukott tesztfájl egyszer újrafut (ingadozás-védelem, N-F232c).
    # Nem része a részleges módnak (L_* lépés-azonosító): a saját feltétele a teljes alap..fej diff.
    olvaso_fajlok = olvaso_erintett(fajlok)
    if args.gyors and (olvaso_fajlok or fuggo_tesztek(fajlok)):
        print('KIHAGYVA olvasó-tesztek (gyors próba; az olvasó kódja vagy egy teszt bemenete változott: a teljes kapu futtatja)')
    elif olvaso_fajlok:
        print('push_elott: az olvasó kódja változott (%d fájl, pl. %s): az olvasó gyors tesztjei futnak a helyi pardes.db-n'
              % (len(olvaso_fajlok), olvaso_fajlok[0]))
        print('FIGYELEM: a lassú tesztek (teszt_szintek.py, teszt_arculat.py) a kapuban nem futnak; a teljes sor a menet saját futása '
              '(`python eszkozok/teszt_futtat.py`) a draft PR előtt (F232).')
        _, olv_ki, _ = olvaso_tesztek_futtatasa(fut, 'F232 olvasó-tesztek (teszt_futtat.py --gyors)',
                                                  [PY, 'eszkozok/teszt_futtat.py', '--gyors'])
        # A bekötés-összevetés: ami az alapon (merge-base) az olvasóban látszott (blokk, tábla, adatkészlet, nézetenként), az az ágon is látsszon.
        # Bukik (HIBA), ha valami eltűnt, feltételhez kötődött vagy másik fülre került; kivétel csak a `merce/bekotes_kivetel.tsv`-ben, indokkal.
        # Csak helyi (a CI-ben nincs adatbázis); a Windows-oldali Python futtatja, mert a git a munkafán itt olvasható.
        fut.lepes('olvasó bekötés-összevetés (bekotesi_leltar.py --osszevet)',
                  [PY, 'eszkozok/olvaso_szerver/bekotesi_leltar.py', '--osszevet', alap])
        for s in olv_ki.splitlines():
            if s.startswith('MÉRCE-ELTÉRÉS'):
                print('FIGYELEM ' + s)
        if any(s.startswith('MÉRCE-ELTÉRÉS') for s in olv_ki.splitlines()):
            print('FIGYELEM: az olvasói mérce eltér a mostani lapoktól: szándékos változásnál a mérce frissítése '
                  '(`teszt_olvasoi_merce.py --merce-frissit`) csak a felhasználó jóváhagyásával történhet, és a PR leírása hivatkozik rá '
                  '(jóváhagyás nélkül a mérce eltérése figyelmeztetés marad, a diffet a fenti MÉRCE-ELTÉRÉS sorok mutatják).')
    elif fuggo_tesztek(fajlok):
        # a lexikon-generátorra/lapra támaszkodó gyors teszt (pl. teszt_visszhang_kapu): csak ez fut (F232, ELLENOR_F232 1.)
        fuggo = fuggo_tesztek(fajlok)
        print('push_elott: az olvasó-tesztek közvetlen bemenete változott: %s' % ', '.join(fuggo))
        olvaso_tesztek_futtatasa(fut, 'F232 függő olvasó-tesztek (teszt_futtat.py --fajl)', [PY, 'eszkozok/teszt_futtat.py'] +
                                 [x for f in fuggo for x in ('--fajl', f[:-3])])
    if any(f.replace('\\', '/').startswith('eszkozok/olvaso_szerver/merce/') for f in fajlok):
        print('FIGYELEM: az olvasói mérce fájljai változtak (eszkozok/olvaso_szerver/merce/): a PR leírása hivatkozzon a felhasználó '
              'jóváhagyására (F232 2.2).')

    # F223: a zöld jegyzés frissítése (csak tiszta fán, nem `--lepes` futás után): a rendben lefutott lépés a mostani fejen
    # zöld, a bukott lépés jegyzése törlődik, a kihagyotté marad
    if zold_ut and not args.lepes and not args.gyors and not nem_commitolt:
        for l, ok in lepes_eredmeny.items():
            if ok:
                zold[l] = fej
            else:
                zold.pop(l, None)
        try:
            zold_ment(zold_ut, zold)
        except OSError as exc:
            print('FIGYELEM: a zöld jegyzés nem menthető (%s): %s' % (zold_ut, exc))

    generalt_nezetek.visszaallit(generalt_kep, ROOT)   # F217: a munkapéldány generált fájljai az eredeti állapotra
    shutil.rmtree(tmp, ignore_errors=True)
    print()
    if fut.hibas:
        print('HIBA: %d bukott lépés: %s' % (len(fut.hibas), '; '.join(n for n, _ in fut.hibas)))
        print('A push ne menjen, amíg nincs 0 HIBA.')
        return 1
    if args.lepes:
        print('0 HIBA a futtatott lépésekben (részleges futás: ez nem a push előtti kapu).')
        return 0
    if args.gyors:
        if gyors_ut and not nem_commitolt:
            import json
            try:
                with open(gyors_ut, 'w', encoding='utf-8') as f:
                    json.dump({'fej': fej}, f)
            except OSError as exc:
                print('FIGYELEM: a gyors pont nem menthető (%s): %s' % (gyors_ut, exc))
        print('0 HIBA a gyors próbában. Ez NEM push előtti kapu: a PR előtt egyszer a teljes `python eszkozok/push_elott.py`.')
        return 0
    if args.reszleges and len(futo) < len(LEPES_AZON):
        print('0 HIBA: a push mehet (részleges mód: a kihagyott lépések zöldek az utolsó futásuk óta, a változás nem érinti őket).')
        return 0
    print('0 HIBA: a push mehet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
