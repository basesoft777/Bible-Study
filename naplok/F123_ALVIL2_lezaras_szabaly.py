# -*- coding: utf-8 -*-
"""F123.ALVIL2.9 — DT-F123j: a cikkenként rögzített lépésszámú lezárás rögzítése
(`F123_MIGRACIO2_BRIEF.md`, `MUNKAMENET.md`, `DONTESEK.md`). Egyszeri átíró szkript;
minden csere pontosan egyszer illeszkedik, különben megáll."""
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def csere(p, parok):
    s = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    t = s.replace('\r\n', '\n')
    for a, b in parok:
        if t.count(a) != 1:
            sys.exit('nem illeszkedik (%s): %s' % (p, a[:70]))
        t = t.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', nl))


SZABALY = ('**A lezárás cikkenként rögzített lépésszámú (DT-F123j, a felhasználó jóváhagyásával, 2026-11-02: „mehet”):** '
           '(1) gépi kapuk — az `ellenoriz.py` 24. és 25. szabálya, az olvasói kapu, a Feed — feltétel; (2) a felhasználó átnézése a lapnézeten; '
           '(3) **egy** javítókör az átnézés alapján; (4) 1. kiadás. Ami ezután derül ki (a Fable határ- és lektori köre az új prózán, a Kiadó kérdései, '
           'későbbi észrevétel), az a **2. kiadás bemenete**, nem az 1. kiadás feltétele („a lektori átnézés eredménye egy új kiadás”). A régi lektori kérdések '
           '(az elavult prózáról) nem ellenőrzési lépés: a Kiadón „az újraírás okafogyottá tette” jelöléssel zárandók, külön lépésben.')

csere('F123_MIGRACIO2_BRIEF.md', [
    ('**Egy cikk akkor kész, ha mind a hat teljesül** (4. szakasz):',
     '**Egy cikk akkor kész, ha mind a hat teljesül** (4. szakasz; a lépésszám rögzített, DT-F123j):'),
    ('6. a Fable-kör (határ, lektor) csak a felhasználó előzetes jóváhagyásával futott; a kérdései a Kiadóban megválaszolva.\n',
     '6. az átnézés alapján **egy** javítókör lefutott, utána a gépi kapuk (3–4.) újra zöldek. A Fable-kör (határ, lektor) és a Kiadó kérdései nem az 1. kiadás feltételei, hanem a 2. kiadás bemenetei (DT-F123j).\n'),
    ('Ezután jön a lezárás: 1. kiadás az `adat/kiadasok.tsv`-ben, `motivumok.tsv` verzió-emelés (C5).\n',
     'Ezután jön a lezárás: 1. kiadás az `adat/kiadasok.tsv`-ben, `motivumok.tsv` verzió-emelés (C5).\n\n' + SZABALY + '\n'),
    ('- **U5. Határ- és lektori kör (Fable) — ⛔ minden futás előtt a felhasználó jóváhagyása kell, kreditből fizetendő.**',
     '- **U5. (DT-F123j óta: az 1. kiadás után, a 2. kiadás bemenete) Határ- és lektori kör (Fable) — ⛔ minden futás előtt a felhasználó jóváhagyása kell, kreditből fizetendő.**'),
    ('Kifogásnál vissza az U3/U4-re. **Csak ezután lezárás:**',
     'Kifogásnál **egy** javítókör (U3/U4: a próza gazdája javít, a gépi kapuk újra zöldek; DT-F123j); második átnézési kör nincs, ami utána derül ki, a 2. kiadás bemenete. **Csak ezután lezárás:**'),
    ('4. **Olvasói kapu (Feed 9): 0 BUKÁS**; a Feed mind a 9 kapuja zöld (`python eszkozok/muhely_allapot.py --motivum X`).',
     '4. **Olvasói kapu (Feed 9): 0 BUKÁS**; a Feed mind a 9 kapuja zöld (`python eszkozok/muhely_allapot.py --motivum X`); a régi lektori kérdések „az újraírás okafogyottá tette” jelöléssel zárva (DT-F123j).'),
    ('6. **Fable-kör** csak a felhasználó előzetes, rögzített jóváhagyásával futott (dátum, idézet a motívum naplójában); a kérdései a Kiadóban megválaszolva, az átvezetés kész.',
     '6. **Egy javítókör** az átnézés alapján lefutott (DT-F123j). A **Fable-kör** nem feltétel: ha fut, csak a felhasználó előzetes, rögzített jóváhagyásával (dátum, idézet a motívum naplójában), és a kérdései a 2. kiadás bemenetei.'),
    ('**Nyitott (⛔):**',
     '**A v2 menetének pontosítása:**\n- **DT-F123j** ✅ — a lezárás cikkenként rögzített lépésszámú: gépi kapuk → a felhasználó átnézése → egy javítókör → 1. kiadás; a Fable-kör, a Kiadó kérdései és a későbbi észrevétel a 2. kiadás bemenete; a régi lektori kérdések okafogyott jelöléssel zárva. A felhasználó jóváhagyása: „mehet” (2026-11-02, az orkesztrátor közvetítésével). Alkalmazva: 1., 3. (U5, U6), 4. szakasz; `MUNKAMENET.md` „A lezárás menete motívumonként”.\n\n**Nyitott (⛔):**'),
])

csere('MUNKAMENET.md', [
    ('1. **gépi kapuk** (C-g): C-x, C-y → C1 → C-z, C-w → 24. és 25. szabály, Feed 6, új cikknél a teljesség-mérés;\n'
     '2. **határ- és lektori kör** (C-h, Fable — **minden futás előtt a felhasználó jóváhagyásával**, kreditből) → **C-l** döntések a Kiadóban (felület) → átvezetés (C-w) és újragenerálás;\n'
     '3. **olvasói kapu** (C-o, Feed 9): 0 BUKÁS;\n'
     '4. **a felhasználó vizuális átnézése** (C-v ⛔) a renderelt lapon, rögzítve;\n'
     '5. **1. kiadás** (C5): Feed 9/9, `kiadasok.tsv`-sor, verzió-emelés, a lap újragenerálása.\n\n'
     'Egy lépés csak az előző zöldje után indul; bukásnál vissza a próza gazdájához (C-w), és onnan újra az 1. lépéstől. A **C-k** (`/kiadas`) a lezárás után bármikor indítható, és a 2. kiadás bemenete.',
     '1. **gépi kapuk — feltétel** (C-g): C-x, C-y → C1 → C-z, C-w → 24. és 25. szabály, Feed 6, új cikknél a teljesség-mérés; **olvasói kapu** (C-o, Feed 9): 0 BUKÁS;\n'
     '2. **a felhasználó vizuális átnézése** (C-v ⛔) a renderelt lapon (lapnézet), rögzítve;\n'
     '3. **egy javítókör** az átnézés alapján (C-w), utána a gépi kapuk újra zöldek;\n'
     '4. **1. kiadás** (C5): Feed zöld, `kiadasok.tsv`-sor, verzió-emelés, a lap újragenerálása.\n\n'
     'A lépésszám cikkenként rögzített (DT-F123j, a felhasználó jóváhagyásával, 2026-11-02: „mehet”): második átnézési vagy javítókör nincs. '
     'Ami az 1. kiadás után derül ki — a **határ- és lektori kör** (C-h, Fable, **minden futás előtt a felhasználó jóváhagyásával**, kreditből) az új prózán, '
     'a Kiadó (C-l) kérdései, későbbi észrevétel —, az a **2. kiadás bemenete**, nem az 1. kiadás feltétele („a lektori átnézés eredménye egy új kiadás”). '
     'A régi lektori kérdések (az elavult prózáról) nem ellenőrzési lépés: a Kiadón „az újraírás okafogyottá tette” jelöléssel zárandók. '
     'Egy lépés csak az előző zöldje után indul; gépi bukásnál vissza a próza gazdájához (C-w). A **C-k** (`/kiadas`) a lezárás után bármikor indítható, és a 2. kiadás bemenete.'),
])

p = 'DONTESEK.md'
s = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
L = s.split(nl)
i = max(k for k, x in enumerate(L) if x.startswith('| DT-F123p |'))
L.insert(i + 1, '| DT-F123j | #123 MIGRACIO2 és a lezárás menete (`MUNKAMENET.md` C) szakasz; 2026-11-02) | Hány lépésből áll egy új cikk lezárása, és mi az 1. kiadás feltétele? | (a) cikkenként rögzített lépésszám: (1) gépi kapuk (ellenoriz 24./25., olvasói kapu, Feed) — feltétel; (2) a felhasználó átnézése a lapnézeten; (3) egy javítókör az átnézés alapján; (4) 1. kiadás; ami utána derül ki (Fable határ-/lektori kör az új prózán, a Kiadó kérdései, későbbi észrevétel), az a 2. kiadás bemenete · (b) a Fable-kör és a Kiadó kérdései az 1. kiadás feltételei (a DT547 szerinti eddigi sorrend) | (a) | ✅ | **(a)** — a felhasználó jóváhagyása (2026-11-02, „mehet”, az orkesztrátor közvetítésével), összhangban a korábbi szavaival: „a lektori átnézés eredménye egy új kiadás”. A régi lektori kérdések (az elavult prózáról) nem ellenőrzési lépés: a Kiadón „az újraírás okafogyottá tette” jelöléssel zárandók (külön lépés). A DT547 sorrendjéből a Fable-kör az 1. kiadás utánra kerül. Alkalmazva: F123.ALVIL2.9 (`F123_MIGRACIO2_BRIEF.md` 1., 3., 4., 5. szakasz; `MUNKAMENET.md` „A lezárás menete motívumonként”). | `F123_MIGRACIO2_BRIEF.md`; `MUNKAMENET.md` |')
io.open(p, 'w', encoding='utf-8', newline='').write(nl.join(L))

p = 'F123_MIGRACIO2_BRIEF.md'
s = io.open(p, encoding='utf-8', newline='').read()
i = s.index('kovetkezo: "')
j = s.index('"', i + 12)
s = (s[:i] + 'kovetkezo: "Te: ⛔ az ALVIL-001 új cikke az U4 után megállt (ág: claude/alvil-uj-cikk-b72389, draft PR #604). '
     'Hátra (DT-F123j): a felhasználó átnézése a lapnézeten → egy javítókör → 1. kiadás; a régi lektori kártyák „az újraírás okafogyottá tette” '
     'jelöléssel a Kiadón (külön lépés, a Kiadó javítása után); a Fable-kör a 2. kiadás bemenete, csak jóváhagyással. Utána: ⛔ DT549 és az ANTROP-001."'
     + s[j + 1:])
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('kész')
