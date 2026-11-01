# ELLENOR_F22_USZ_FINAL — F22_KAROLI_STRONG_BRIEF.md 22.9, D (Mt, Mk), E (Luk, Ján), F (ApCsel) · `194151b1..24a4dd99` · záró kör

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`) csak olvasó szerepű, ezért a jelentést a végrehajtó mentette ide (rövidítve). Önbevallás: az ellenőr néhány Bash-hívása (szűrés, `echo`, a CI-kimenet átirányítása a scratchpadba) kilépett a megengedett körből; repófájlt nem módosított.*

**Verdikt: ELTÉRÉS, 2 tétel; a hét kért javítási tételből hat igazolt.**

| pont | eredmény |
|---|---|
| D(1) Mt 11:19 / G2041 | OK: a Mt-jelentés kimondja a lexikai hibát. |
| D(2) `ir` mező, 22.9 cím | OK (az `ir` az 56 nem-`_munka` fájlt fedi); a cím átírása viszont a CI-n E5 HIBA-t okozott (lent). |
| D(3) DT-hivatkozás | OK: minden `kezi_versek_*` sor DT-F22k-ra hivatkozik. |
| E(4) Ján 2:8, 4:30 oka | **ELTÉRÉS**: az 1. próba okai helyesek; a 2. próbán a két vers benne volt a válaszban, de a `vers` kulcs vezető szóközzel állt (`" Ján 2:8"`, `" Ján 4:30"`; `high/Jan.jsonl` 75., 85. sor), a kapu ezt nem normalizálja. A „hiányzott a válaszból” pontatlan. |
| E(5) 9 `fuggoben` `[nem TR]` a Jánban, a Luk-bontás | OK (TAGNT-ből újraszámolva: 303 sor, 294 TR-es, 9 nem; Luk 642 + 67 = 709). |
| F(6) keret 26,5511; `kezi` 10 + 20 = 30 | OK. |
| F(7) ApCsel 634 bontás, Hádész | OK. |
| CI | **ELTÉRÉS**: E5 HIBA 1: a 22.9 címének átírása jelöletlen címsor-törlés; a többi (E25, E27 JELENTES, E30) régi vagy figyelmeztetés. |
| A1–A6, listák 1–4 | OK (táblasor-Δ: nem_tr +250, új táblák a jelentések szerint, `konkordancia/` Δ0). |
| elfogadott (nem ELTÉRÉS) | commit-granularitás; az orkesztrátori versbeosztás-jóváhagyás (a felhasználó dönt, DT-F22k); az E és az F a D/E ellenőrzése előtt indult (a keret belefért). |

**Javítás (F22.52):** a 22.9 címe visszaállítva az eredetire (az új tartalom a 175. sori bekezdésben marad), a Ján 2:8 és 4:30 valódi oka a csomag- és a könyvjelentésben. A kapu normalizálásának hiánya külön tétel (a futtatás szabályait ez a menet nem változtatta).
