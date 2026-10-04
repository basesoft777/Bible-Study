# ELLENOR_KONTEXTUS — F32_KONTEXTUS_BRIEF.md · origin/main..claude/f32-kontextus

*A `fuggetlen-ellenor` jelentései (összefoglalva; az ellenőr nem írhat, a fájlt az orkesztrátor mentette).*

## 1. kör — ELTÉRÉS: 6 tétel
Javítva: duplikált `kovetkezo.md`-sor; hiányzó `git diff --stat` a naplóban; téves F33/F42 állítás. Nyitottként a felhasználóhoz ment: (1) `munka` nélküli motívumíró, (2) K-D9 hivatkozás, (3) K3.2 korlát.

## 2. kör (HEAD 292752a után) — ELTÉRÉS: 4 tétel
| # | Eltérés | Kezelés |
|---|---|---|
| 1 | A `MUNKA_ELOZMENY = (9, 35, 36)` a végrehajtó saját döntése; az F09/F36 emiatt csak `FIGYELEM`-et kap, így egyedül futtathatónak ajánlható (K-D4 ellen); a kód megjegyzése „2. eltérés”-re hivatkozik | **DT-F32c 🟢 (1. opció, 2026.10.04):** a kivétel marad, de a `/kovetkezo` nem ajánlja őket (az 1. fázisnál a `jeloltek` is kihagyja; l. 3. kör). A megjegyzés javítva (1. eltérés). |
| 2 | A napló valódi-repó próbái elavultak, MUNKA_HIANY-próba nincs | **Javítva** (frissítés a naplóban; a viselkedést a 19 teszt fedi). |
| 3 | A zárójelentés elavult (🟡, nincs teszt, dontesre_var) | **Javítva** (új zárójelentés). |
| 4 | Doksi (F09, F36) és kód (9, 35, 36) előzménylistája eltér | **Javítva** (`BRIEF_SABLON.md`). |

OK: DT-F32b (🟢, hivatkozások érvényesek); K3.2 korlát rögzítve; DT-F32a 🟢 és az F23 ⛔ pont; 19 új teszt és a `teszt_feladatok.py` import; motívumfájl és `adat/`/`konkordancia/` érintetlen; `futtat.py` E2–E16 és E19: 0 találat. Nem ellenőrizhető az ellenőrnek: a tesztek és az `ellenoriz` futtatása; a felhasználói döntések ténye (chat).

## 3. kör (F32.13) — `9541cf1..4cbb34c`

Ellenőr: `fuggetlen-ellenor` (friss kontextus). Hatókör: 1 commit, 8 fájl, +31/−12; motívum-, adat- és `generalt_proba/` fájl nem változott (`git diff --stat` üres); `futtat.py --valtozott … --diff-alap 9541cf1 --diff-fej 4cbb34c` → rc=0. A `csomag()` a `jeloltek()`-ből dolgozik, tehát örökli a kizárást; a `csomag` CLI a `csomag_hiba()`-n át szintén elutasít.

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | (közepes) A `jeloltek` új ága a valós F09/F36-ra hatástalan: mindkettő `fazis: 2`, a `jeloltek` csak 1. fázist vizsgál; a DONTESEK, a zárás, a napló és ez a jelentés gépi kihagyást állított; a teszt 1. fázisú fixture-rel fut | Javítva (F32.14): a négy szöveg pontosítva — a védelem az F09/F36-ra a `kovetkezo.md` 1. lépésének szabálya (E18 `FIGYELEM`-sor), a `jeloltek` csak 1. fázisnál. Kód nem változott: a `/kovetkezo` 2. fázisú jelöltlistát ma nem gépből kap. |
| 2 | (alacsony) `KONTEXTUS_szabalyok.md` elavult 🟡/19 teszt sor jelöletlen; a zárás „2 kör”-t ír | Javítva (F32.14): elavult-jelölés; zárás „3 kör”. |

Az ellenőr szerepköre miatt nem futtatott parancsokat a végrehajtó futtatta (F32.13 előtt és után): `test_feladatok_kontextus.py` → 20 teszt OK; `teszt_feladatok.py` → az F32.13 után 1 hiba (`MaiAllapotTest.test_jeloltek`: a fixture #35-je `munka` nélkül motívumot ír, az új ág helyesen kihagyja), javítva F32.15-ben → 91 teszt OK; `feladatok.py ellenoriz` → `71 brief, 0 hiba, 3 figyelmeztetés`, rc=0; `fuggesek` rc=0; `jeloltek` → JELOLT #43.
