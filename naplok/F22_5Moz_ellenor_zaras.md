# F22 — az 5Móz utólagos ellenőri köre: zárójelentés

*Ág: `claude/f22-5moz-ellenor` · 2026.10.04 · orkesztrátor: Opus, ellenőr: `fuggetlen-ellenor`*

- **Mi történt:** a PR #139-cel ellenőri kör nélkül mergelt 5Móz-menet (`85d4ac0..48b4c24`) független ellenőrzése; jelentés: `naplok/ELLENOR_F22_5Moz.md`.
- **Minősítés:** ELTÉRÉS, 5 tétel (közepes 2, alacsony 3). Az adat rendben: 959 vers, 96 köteg, er-tokenek = TAHOT (22 865), csak-Sonnet jelölés mind `alacsony`/`S`, kapuhiba 13/959, végleg 0, régi arany 7/7, kulcs- és zártadat-grep 0.
- **Eltérések:** (1) elmaradt ellenőri kör — ezzel pótolva; (2) SEMA 2.20 csak-Sonnet felsorolásából hiányzik az 5Móz — javítva (F22.24); (3) DT-F22c ellentmondás — a main-en rendezve; (4) a jelentés 4. szakasza elavult — javítva (F22.24); (5) az `ir:` listából hiányzott az ellenőri jelentés — javítva.
- **Brief-fejléc:** `allapot: megallt`, `kovetkezo`: „Te: a Józs indítása (⛔ 2.)”.
- **Nem ellenőrizhető:** `egyesit.py --ellenoriz` (K7), a hu-tokenek egyszeri szereplése, a kötegenkénti hash-ellenőrzés, a `/usage`-értékek.
- **Eljárási megjegyzés:** az ellenőr három Bash-hívásban szűrőt (`head`/`grep`) használt a szerepkörén túl, és ezt maga jelezte; a kulcs-grepet szabályosan megismételte. A jelentést írási eszköz híján az orkesztrátor mentette.

## Egyeztetett eltérés

A felhasználó a #22 folytatásából csak az 5Móz ellenőri körét kérte („mehet, de csak az ellenőrzés”). A Józs nem indult. Az ellenőrzés után a felhasználó kérésére („mehet”) ugyanezen az ágon a 2. és 4. tétel dokumentációs javítása is elkészült (F22.24: `adat/SEMA.md` 937. sor, `naplok/F22_5Moz_jelentes.md` 4. szakasz); adatfájl nem változott.
