# ELLENOR_F20 — független ellenőrzés (`fuggetlen-ellenor`), F20_BEFOGADAS_BRIEF.md v1.4

**Ítélet (3. kör után): a 3. kör saját ítélete NEM TISZTA volt öt javítható eltérés miatt; ezeket a menet kijavította (l. 3. kör), nyitott felhasználói döntés nincs.** A javítás utáni ellenőri megerősítés (4. kör) a PR-on rögzítendő. A K1, K4, K5, K7 pontokat az ellenőr a szerepköre (csak olvasás, `git`, `futtat.py`) miatt nem tudta a saját lekérdezésével futtatni (NEM ELLENŐRIZHETŐ); a menet saját futtatása: `feladatok.py ellenoriz` 40 brief 0 hiba, 42 teszt OK, `general` kétszer változatlan, `futtat.py` E2–E16 0 HIBA, a mutációs próba (`naplok/F20_proba.md`) mindhárom esetet megfogja, a CI (`ellenorzes`, `feladatkovetes`) zöld.

Az ellenőr nem tud fájlba írni; ez a jelentés a háromkörös jelentés összefoglalója, a javítások a `F20.B8`, `F20.v1.4` és az azt követő commitok szerint.

## 1. kör (v1.3) — 11 eltérés

| Eltérés | Kezelés |
|---|---|
| K8/D25: a `main` védett, az Action push-a elbukik | megoldva: ruleset + `pardes-feladatok` GitHub App (felhasználói beállítás), az Action az App tokenjével pushol (v1.4) |
| K7/D25: az E18 nem kötelező check | megoldva: a ruleset kötelező checkjei `ellenorzes` és `feladatkovetes` (felhasználói beállítás) |
| D21: a #20 `ir` lista hiányos | javítva |
| K5 (d): a jelölés-javaslat nem teljesült | megoldva (v1.4): kötelező lépés a `befogad.md`-ben, a próba újrafuttatva, megfelelt |
| K2: #12 „Hol” cella | dokumentálva a B4 naplóban (a v1.3-egyezés megtartva) |
| D26: Kész-dátumok a B3 dátumát kapták | javítva: a dátum a `lezarva_osszegzes`-ből (teszt) |
| TSV proveniencia-sor átírva | visszaállítva |
| B3: nyitó prompt szövegében átírt brief-nevek; címsorok (E5) | blokkok visszaállítva; a címsor-átírás a `TÖRLÉS-SZÁNDÉKOS:` jelöléssel fedett |
| #9 `ir` lista hiányos; #9 csonk állapota a szövegével ellentmond | javítva |
| commit-üzenet számolása | tényként marad |

## 2. kör — 14 eltérés

E1 (hamis merge-hash): javítva (`-G '^allapot: lezarva$'`, csak merge-commit). E2 (zárás kerülőútja): javítva. E3 (címsorok, `TÖRLÉS-SZÁNDÉKOS`): a B8 commit üzenete megnevezi. E4 (lógó jelentés): ez a fájl. E5 (#12 `forras`): dokumentált. E6–E9 (`ir`-listák, horgony, RENDER történeti sora): javítva. E10 (két korai ékezetlen commit-üzenet): **elfogadott kivétel** (már pusholt). U1–U5: lásd alább.

## 3. kör (v1.4) — 5 eltérés, javítva

| Eltérés | Kezelés |
|---|---|
| a `lezarva_osszegzes` és a generált Kész-sor elavult ⛔-t tartalmazott a védett `main`-ről | javítva: „a main-t ruleset védi, az Action a pardes-feladatok GitHub App tokenjével ír” |
| az `ELLENOR_F20.md` elavult, önellentmondó volt | újraírva (ez a fájl) |
| a 🔎→🔀 csere történeti szövegeket is átírt (v1.3 napló, B4 napló, D33) | helyreállítva: a történeti mondatok a 🔎-t említik, a v1.4 és a D33 a cserét |
| a zárás „a két nagyító az E2 jelölése” pontatlan | javítva: az E2 a U+1F50D nagyító-t figyeli |
| az `f06_forrasfelmeres.yml` push-lépései `contents: read` mellett | dokumentálva a workflow kommentjében (az F06 lezárva; újrafuttatásnál külön döntés) |

## Felhasználói döntések (rendezve)

| # | Tétel | Állapot |
|---|---|---|
| U1 | az Action push-a a védett `main`-re | rendezve: ruleset, bypass csak a `pardes-feladatok` App |
| U2 | az E18 kötelező check | rendezve: `feladatkovetes` kötelező |
| U3 | (d) próba jelölés-elvárása | rendezve (v1.4) |
| U4 | B2 jóváhagyás rögzítése | rögzítve a munkalap fejlécében |
| U5 | a jel: 🔀 (a 🔎 helyett) | rendezve (v1.4, a felhasználó döntése) |

## Elfogadott, nem javítható kivételek
- két korai commit-üzenet ékezet nélkül (4ef806d, e733c86; már pusholt);
- a régi brief-nevek a nyitó prompt blokkokban és a `konkordancia/Karoli_versmegfeleltetes.tsv` proveniencia-sorában maradtak (K3 kivétele a `naplok/` mellett).
