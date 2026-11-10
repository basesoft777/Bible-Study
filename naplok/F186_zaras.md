# F186 — zárójelentés (THAYER_JELENTESPONT_97; végrehajtó: claude-opus-5-5; 2026-11-10)

- **Hatókör:** T0–T4 és a T6-ból a jelentés (`naplok/F186_jelentes.md`); a T5 a #187-é. Az ellenőr, a PR és a push az orkesztrátoré.
- **Egyeztetett eltérés:** a SORREND szerint a #121 előbb jönne; a #121 `megallt`, az ága nem írja az `eszkozok/thayer_jelolt/`-ot, ezért a KIZAR nem akadályozott. A `naplok/F186_zaras.md` az orkesztrátor kérésére készült (nincs a brief `ir`-jében).
- **T1 (seed-201, a javítás előtt):** két vak Opus-kitöltő, 200/200 egyezés egymással; könyv/vers 200/200, jelentéspont **189/200 = 94,5%** (Wilson 90,4–96,9).
- **T2:** K1 bekezdésen belüli fej (9 hiba) és K2 hamis bekezdés-eleji fej (1) javítva a `bont.py`-ban; a szakasztábla 17 093 → 17 266 sor. A seed-201 a javított táblán 199/200 (tájékoztató). A ⛔ T3 nem kellett.
- **T4 (seed-202, a javított táblán):** könyv/vers 200/200; jelentéspont **192/200 = 96,0%** (Wilson 92,3–98,0). **A kapu (≥ 194/200) nem teljesült.** Az okok: K1b (túl szigorú kizárás), K1c (a Thayer kihagyja a „j”-t), K2b, és egy forrás-torzulás (K4).
- **Kulcsváltozás:** 140 Strong, 1 009 szakaszkulcs (a tételes lista a jelentés 8. A mellékletében).
- **#7-hatás:** 636 hash-eltérő Thayer-fordítássor 61 Strongban (539 csak eltolódott, 97 szövege változott). A mechanizmus a `szolista.py` `elavult_hash` jelzése és az `ellenoriz.py` 13. szabálya; ez most SÉRTÉS (694 tétel, korábban RENDBEN). Az `adat/forditasok.tsv`-t nem írtam.
- **Tesztek:** `teszt_bont` és `teszt_vers_jelentes` zöld; a `teszt_lanc` `Betolto.test_ellenoriz` a 17 093-as számon bukik (a fájl nincs az `ir`-ben); a `Sigla`-hiba már korábban is fennállt.
- **Nyitott (döntésre vár):**
  - DT-F186a: második szabálykör + seed-203 (javaslat), vagy T3, vagy a 96,0% elfogadása;
  - DT-F186b: a 636 fordítássor sorsa (átkulcsolás hash szerint, javaslat);
  - DT-F186c: `ir`-en kívüli egysoros javítások;
  - N-F186a (K3, `zaro`), N-F186b (`bcv`-hiba).
- A brief `allapot`-a `fut` marad; a lezárás az orkesztrátoré.
