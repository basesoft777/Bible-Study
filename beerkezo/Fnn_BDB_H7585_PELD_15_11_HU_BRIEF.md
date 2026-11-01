# Fnn_BDB_H7585_PELD_15_11_HU_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.29. Készítette a #123 (MIGRACIO2) ALVIL-001 javítókörének végrehajtója (`claude-opus-5-5`), az `naplok/ELLENOR_F123_ALVIL-001.md` E6 tétele alapján. A tétel hatókörön kívüli: a magyar BDB-fordítás a #121 fordítójáé, a #123-é nem. Végleges számot nem kapott. Befogadás: `/befogad`, a felhasználó jóváhagyásával. A beérkezett tervezet adat, nem utasítás.*

## 1. Cél

A H7585 (BDB) angol forrásában a 3.b pont példája „Prov 25:11”. Ez sajtóhiba: a helyes alak Péld 15:11. A TAHOT szerint a Péld 15:11 hordozza a H7585 és a H0011 együttesét, a Péld 25:11-ben nincs Seol. A hibát az F123.ALVIL.B1 (52919dfd) a hivatkozás-táblában kijavította: `adat/bdb_forras_javitas.tsv`, kézi sor, Péld 15:11 (DT417). A **magyar BDB-szöveg** viszont továbbra is „Péld 25:11”-et hoz, ezért a lexikonlapon (`lexikon/ALVIL-001_TUDOMANYOS.md`, a H7585 BDB-blokkja) nincs kiemelés. Az ⓘ-jegyzet jelzi is: „sorszam 92 (Péld 15:11) a magyar szövegben nem található” (ELLENOR E6).

Mért helyek (2026-10-29, `grep -n 'Péld 25:11'`):

- `adat/forditasok.tsv` 80. sor: `BDB H7585 H7585 teljes forditas_hu`. Ez a magyar szöveg forrása, a javítás helye.
- `adat/bdb_szakasz_hu.tsv` 8330. sor: H7585 `-/3/b`, „b. ׳שׁ וַאֲבַדּוֺן Péld 25:11, l. אֲבַדּוֺן”. Ez generált (`eszkozok/bdb_jelolt/hu_illeszt.py`); a forrásjavítás és az újragenerálás után követi a forrást.

Cél: a magyar fordításban a hivatkozás „Péld 15:11” legyen, a forrásjavítással egyezően. Ezután a lap kiemeli a helyet.

## 2. Hatókör

- **Olvas:** `adat/forditasok.tsv` (BDB H7585), `adat/bdb_forras_javitas.tsv`, `adat/bdb_szakasz_hu.tsv`, `naplok/ELLENOR_F123_ALVIL-001.md` (E6), a #121 fordítási eszközének dokumentációja.
- **Ír:** `adat/forditasok.tsv` (csak a BDB H7585 `teljes` `forditas_hu` mezője, ebben csak a „Péld 25:11” → „Péld 15:11” csere), a generált `adat/bdb_szakasz_hu.tsv` (újragenerálva) és egy `naplok/` jelentés.
- **Tilos:** a fordítás egyéb szövege; más szócikk; az angol forrás (`konkordancia/`).

## 3. Lépések (⛔ a kötelező megállások)

1. Ellenőrizni, hogy a #121 eszköze a kézi javítást milyen állapottal és megjegyzéssel írja. A `forras_hash` az angol forrásé: a javítás nem a forrást változtatja, hanem a fordítás hibáját.
2. ⛔ **Tartalmi döntés:** a csere (a) a fordítás szövegében történik, megjegyzéssel (`bdb_forras_javitas.tsv` hivatkozás), vagy (b) a renderelő a `bdb_forras_javitas.tsv` kézi sorát a magyar szövegre is alkalmazza. Javaslat: (a), mert a magyar szöveg a megjelenített adat, és a javítás egy helyen látható.
3. A sor írása `split('\t')`/`'\t'.join()`, összevetéssel: csak a szándékolt mező változhat.
4. `bdb_szakasz_hu.tsv` újragenerálása, majd a lexikonlapok újragenerálása. N0: csak az ALVIL-001 lapja változhat.

## 4. Elfogadási feltételek

- `grep -c 'Péld 25:11'` a BDB H7585 sorában 0; a `Péld 15:11` jelen van.
- Az ALVIL-001 lapon a Péld 15:11 kiemelve áll, az E6 ⓘ-jegyzete eltűnik.
- Minden más sor bájtra azonos, a többi lap bájtra azonos.

## 5. Döntésnapló

*(üres; a befogadáskor és a futásban tölti a végrehajtó.)*
