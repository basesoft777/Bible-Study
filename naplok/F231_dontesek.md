# F231 (#810) — az integrátor döntései

Forrás: szerkesztői döntés (az integrátor, `local_ee039369`, a felhasználó felhatalmazásával). A döntés fájlban él (MUNKAMENET „Szereposztás”, PR #835).
A végrehajtó session: `claude-opus-5-5`, ág: `claude/olvaso-egyben-3464e1`.

| # | Dátum | Döntés | Állapot | Végrehajtva |
|---|---|---|---|---|
| D1 | 2026-11-23 | A tervőr tárolt sémája (`teszt_adat/pardes_sema.sql`, `pardes_meretek.tsv`) vissza a main-beli alakra. | ⛔ visszavonva (D2) | F231.19 (`34d54557`), visszavonva az F231.20-ban |
| D2 | 2026-11-23 | Visszavonja: D1. A 12 tábla (`generalt_nezetek`, `heti_*`, `keret_*`, `lap_befagyasztas`, `lapgen_*`, `olvasoi_nevtabla`, `otlettar`, `tematikus_sajat_szo`) a main saját `adat/*.tsv`-jéből épül (`sqlite_epit.py` `_adat_tablak`), az F231.15-ös séma helyes; az F231.19 revertje. | ✅ | F231.20 (`4965e727`) |
| D3 | 2026-11-23 | #37: a versszámozás-tábla „Osztály”, „A megfeleltetés forrása” és az LXX „Forrás” oszlopa visszajön, a main szerinti helyen és láthatósággal. Indok: a szerkesztő 2026-11-23-i szabálya („ami a main-en látszott, az újra látszik”). Az olvasói alak megengedett, az elvétel nem. | ✅ (DT-F231d) | F231.21 (`0643b13a`) |
| D4 | 2026-11-23 | #27: a „Domén kód” és az „Azonosító” oszlop visszajön, ahol a main-en látszott (ugyanaz az indok). | ✅ (DT-F231e) | F231.21 (`0643b13a`) |
| D5 | 2026-11-23 | G0264: a Thayer-blokk „modell-kimenet” címkéje nem jön vissza, mert nincs mögötte fordítás (a hamis jelleg-címke félrevezető). | ✅ (DT-F231f) | F231.21 (`0643b13a`): a kapu kivétellistáján „eldöntve” |
| D6 | 2026-11-23 | A H8415 csonka jelentéscíme („mély) tenger, amely elborítja Tírust (párhuzamban”) nem állhat a felületen; a technikai mód a végrehajtóé. | ✅ | F231.21 (`0643b13a`): a pótcím zárójele ép, a félbevágott zárójel kimarad; most „(mély) tenger, amely elborítja Tírust” |
| D7 | 2026-11-23 | Az F232 pillanatkép-mérce (`merce/*.txt`) frissítése csak a szerkesztő nézése után. | ✅ | F231.23 (a D8 szerint külön PR-ban) |
| D8 | 2026-11-23 | Kérdés: a D7 szerinti F232-mérce-frissítés a nézés után ugyanabba a PR-ba kerüljön-e? Döntés: nem; a #810 a nézett fejen (88fd78b7) merge-elt, a mérce-frissítés külön gyors sávos PR a main-ből (OLVASO-GYORS: merce/*.txt + naplók), soronkénti besorolással (naplok/F231_merce_indoklas.md). Indok: a nézett hash szabálya (DT886) szerint a jóváhagyás utáni commit új nézést kérne; a mérce a jóváhagyott, most a main-en álló állapotot rögzíti. Forrás: szerkesztői döntés (az integrátor, a felhasználó felhatalmazásával). | ✅ | F231.23 (ez a PR); a D7 ezzel alkalmazva |
| D9 | 2026-11-23 | A #231 briefjének (`F231_SZOKARTYA_EGYSEGES_BRIEF.md`) fejléce lezárva: állapot lezárt (a #810 merge-ével, `a3405522`); következő: nincs — az olvasó újraépítése a 218c után (IRANY). Ok: a „fut” állapot miatt a 241 a `teszt_olvasoi_merce.py` kizárás-listáján áll. Forrás: szerkesztői döntés (az integrátor, a felhasználó felhatalmazásával). | ✅ | F231.24 (a mérce-frissítő PR-ban); az állapot értéke a fejléc-szabály szerinti `lezarva` |

A D3–D5 a `dontesek/uj/olvaso-egyben-3464e1.md`-ben is áll (helyőrzővel: DT-F231d, DT-F231e, DT-F231f).
