# ELLENOR_F23_3 — a DT84 átvezetésének független ellenőrzése

*Brief: `F23_MOTIVUM_FORRAS_BRIEF.md` (#23) · tartomány: `origin/main..HEAD` = `44dd751e..cddc8f09` (F23.D0–D7) · ellenőr: fuggetlen-ellenor, claude-opus-5-5 · 2026-10-17. A jelentést az ellenőr írásra képtelen környezete miatt az orkesztrátor mentette el, tartalmilag változatlanul (a táblázat tömörítve).*

**Összegzés: ELTÉRÉS, 8 tétel.** Rendben: modell, tartomány, DT84 (1), (3)–(13) átvezetése, a 36 `【NAPLO` mérés (ALVIL 4, HAMART 3, HODIT 3, ISTENTISZT 14, KIRALY 11, MENNY 1), a SEMA 3/9 szövege változatlan, nincs maradt DT84-es `javaslat`, DT182/c ⛔ jogos, DT66 ✅ és DT84 🟢 helyes, tábla Δ = 0 (E17/DT3), A2/A6 OK; CI: `futtat.py` HIBA 0 csak a commit-üzenettel együtt (E5 a három átnevezett címsorra, `TÖRLÉS-SZÁNDÉKOS` az F23.D6 üzenetében).

## Eltérések súlyossági sorrendben

1. **K3-sértés — DT-F86c.** A „BY-SA-eredetű blokk zárt rétegben nem állhat (DT-F86c)” normatív szabályként áll (`adat/SEMA.md:1314-1315`, `sablonok/9_PaRDeS_motivum_forras_sablon.md:26`, `naplok/MOTIVUM_FORRAS_ci_terv.md:128`), de a DT-F86c `javaslat` (`F86_ELOFIZETES_FEED_BRIEF.md:67`), a DONTESEK-ben nincs sora; a felhasználó csak a DT-F86a-t hozta be.
2. **Maradék audit-út a prózából az `auditok.tsv`-be** (DT84 (2) a., SEMA 3/9 ellen): sablon 4. pont 0. és 1.P sora; pilot 4.3 0. sora (`pilot_terv.md:130`; sablon `:67`, `:68`).
3. **`naplok/MOTIVUM_FORRAS_lekepezes.tsv:41, :78`** „→ `adat` (`auditok.tsv`)” ellentmond a sablon 7.M `generalt` sorának (`sablon:61`, `:84`), jelöletlenül.
4. **pilot 4.3 / 4.1 „jeloltek 32 sor”** elavult: ISTENTISZT-001 `jeloltek.tsv` 92 sor, ebből 32 `beépítve` (F63.5 óta); proveniencia nélkül.
5. **SEMA 3/9 ↔ 3.10.7 4.** (`:1283-1284` ↔ `:1421-1426`): hiányzik a mondat, amely kimondja, hogy a nem igehely-kulcsú adat „meglévő adatúton” íratása kivétel vagy nem kinyerés.
6. **Brief `pr` mező** az új ágon a mergelt #258-ra mutat.
7. **K4:** `naplok/F23_zaras.md:9` — a `git diff --stat` kimenete hiányzik (az állítás igaz: 7 fájl, egyik sem tartalmi).
8. **Sablon 9. pont** számozása (1–8 a DT84 (1)–(8), a 9. a (10)-et foglalja össze) félreolvasható (`sablon:215`).
