# ELLENOR_F20 — független ellenőrzés (`fuggetlen-ellenor`), F20_BEFOGADAS_BRIEF.md v1.3

**Ítélet: NEM TISZTA** — a 2. kör javítható eltéréseit a menet javította (l. alább), de öt tétel felhasználói döntést igényel (U1–U5), ezért a K10 nem teljesül. A jelentéseket az ellenőr szerepköre nem tudta fájlba írni; az itt szereplő összefoglaló a két jelentés tartalma, a javítások a `F20.B8` és a zárócommitok szerint.

Tartomány: `origin/main..HEAD` (`51f9291`..). Az ellenőr a `feladatok.py`-t és a teszteket a szerepköre miatt nem futtathatta (K1, K4, K7 „NEM ELLENŐRIZHETŐ” a saját lekérdezéssel); a menet saját futtatása: `feladatok.py ellenoriz` 40 brief 0 hiba, 42 teszt OK, `general` kétszer változatlan, `futtat.py` E2–E16 0 HIBA, a mutációs próba (`naplok/F20_proba.md`) mindhárom esetet megfogja.

## 1. kör — 11 eltérés és a kezelésük

| Eltérés | Állapot |
|---|---|
| K8/D25: a `main` védett, az Action push-a elbukik; ⛔ jelzés hiányzik | **U1** (felhasználói döntés); a ⛔ a zárójelentésben és a brief `lezarva_osszegzes`-ében szerepel |
| K7/D25: az E18 (`feladatkovetes`) nem kötelező check | **U2** (felhasználói döntés) |
| D21: a #20 `ir` lista hiányos | javítva (`eszkozok/`, `konkordancia/`, `sablonok/`, `fp2/` … ) |
| K5 (d): „jelölést javasol” nem teljesült, jóváhagyás nélkül | **U3** (felhasználói döntés) |
| K2: #12 „Hol” cella | dokumentálva a B4 naplóban (a v1.3-egyezés megtartva) |
| D26: a Kész-dátumok a B3 dátumát kapták; a napló téves állítása | javítva: a dátum a `lezarva_osszegzes`-ből (teszt), a napló helyesbítve |
| TSV proveniencia-sor átírva | visszaállítva (az `origin/main` változat) |
| B3: címsorok átírása, nyitó prompt szövegében átírt brief-nevek | a blokkok visszaállítva (bájtra azonosak a régiekkel); a címsor-átírás (E5) a `TÖRLÉS-SZÁNDÉKOS:` jelöléssel fedett |
| #9 `ir` lista hiányos | javítva (`adat/forditasok.tsv`, `eszkozok/kiejtes.py`, tematikus tanulmány) |
| #9 csonk állapota ellentmond a szövegének | javítva: a törzs és a `kovetkezo.md` 4. lépése a `forras`-t olvassa |
| commit-üzenet számolása | tényként marad (a történet nem írható át) |

## 2. kör — 14 eltérés (9 javítható, 5 felhasználói döntés)

| # | Eltérés | Kezelés |
|---|---|---|
| E1 | a #20 Kész-sora „merge `4ef806d`” (nem merge-commit; a `-S` a brief törzsében lévő szövegre is illeszkedett); a sor a merge előtt már a Kész listában | javítva: a hash csak a fejlécsor (`-G '^allapot: lezarva$'`) bekerülésének first-parent **merge**-commitjából jön; PR-ágon nincs hash. A merge előtti Kész-megjelenés az átállási szabály (a `main`-nek még nincs fejléce a feladatról) következménye, a zárójelentés jelzi |
| E2 | a zárás kerülőútja (`general` kézzel) az E18 miatt nem működik | javítva: a zárás a tényleges állapotot írja, a kerülőút kikerült |
| E3 | 14 átírt címsor, a `TÖRLÉS-SZÁNDÉKOS:` csak két fájlt nevez meg | a zárócommit üzenete megnevezi az `adat/SEMA.md`-t és az `F01`–`F05` első címsorait |
| E4 | lógó `ELLENOR_F20.md` hivatkozás | ez a fájl |
| E5 | #12 `forras` szemantikája (csak a T1–T2-t írja le) | dokumentált (B4 napló); a `forras` háttér-hivatkozás, a cella-egyezés a v1.3-mal indokolja |
| E6 | #9 `ir`: a S2.6–S2.7 célja hiányzott | javítva (tematikus tanulmány felvéve) |
| E7 | F20 `ir`: `fp2/` hiányzott, `MUNKAMENET.md` fölösleges | javítva |
| E8 | #9 `forras` horgony nem egyértelmű | javítva: `#2. menet — kimenet-változtató` |
| E9 | RENDER történeti commit-táblája átírva | visszaállítva |
| E10 | ékezetlen commit-üzenetek (két korai commit) | tényként marad; a CLAUDE.md-szabály ellenére (a push előtti átfogalmazás interaktív rebase-t kívánna, ami itt nem támogatott) |
| U1 | K8/D25: az Action push-a a védett `main`-re | **felhasználói döntés** (ruleset-bypass a `github-actions` számára, vagy PR-t nyitó Action) |
| U2 | K7: az E18 nem kötelező check | **felhasználói döntés** (felvétel a kötelező check-ek közé) |
| U3 | K5 (d): a próba jelölés-elvárása | **felhasználói döntés** (a romboló prompt jelölés-mentes kezelése ésszerű; a brief szó szerinti elvárása nem teljesült) |
| U4 | D28: a B2 jóváhagyása nincs a repóban | rögzítve a munkalap fejlécében (a chatbeli jóváhagyás szövege) |
| U5 | a menet saját briefje v1.2 → v1.3 | Q11 (2b, (e)) és Q2 (E18) a felhasználó döntése; a 🔎 jel a menet javaslata (D33), **jóváhagyandó** |

## A felhasználónak
U1–U3, U5 (🔎): döntést kér. A `naplok/F20_zaras.md` és a PR leírása ezt ismétli.
