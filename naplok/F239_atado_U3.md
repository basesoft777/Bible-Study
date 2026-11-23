# F239 átadó — U3 (próza) → U4 (ellenőrzés)

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820). A lépések és döntések indokkal: `naplok/F239_naplo.md`, „U3” szakasz.*

**A próza nem végleges.** A próza az U1b (visszhang 1–2) előtt készült: az integrátor (b) döntése (előbb az U1b, utána a próza; MUNKAMENET C-vh, #825) az üzenetsor késése miatt csak utána ért ide. Az integrátor döntése (2026-11-23, a felhasználó felhatalmazásával): a prózát nem dobjuk el, de lektorhoz és kiadásnak nem megy, amíg az alábbi célzott ellenőrzés le nem zárul. **Következő lépés: egy friss Opus-session**, a teljes próza (`motivumok/TEREMT-001.md` és a 43 × 1/a) elolvasásával; ez a session nem végzi el, mert a kontextusa 150 ezer token fölött van.

## Mi kész, hol áll

| Mi | Hol |
|---|---|
| Az adat-igazolás (a négy döntés az adatban; eltérés nincs) | `naplok/F239_U3_adat_igazolas.py`, `…_adat_igazolas.txt` (F239.11) |
| A határ friss (39. szabály) | `naplok/HATAR_TEREMT-001.md` határdöntés-jele (F239.12, frissítve F239.17) |
| A bírálat: az U2-é a kanonikus; az U3-é második vélemény | `naplok/BIRALAT_TEREMT-001.md`, `naplok/BIRALAT_TEREMT-001_masodik.md`; válaszok: érvnapló D és D2 |
| A Nave-témák magyar neve (4 téma, 6 altétel) | `adat/nave_tema_hu.tsv` (F239.12) |
| A régi adat alakja az új generátorhoz | F239.14 (a commit-üzenet sorolja) |
| **A próza** | `motivumok/TEREMT-001.md` (négy rés), `adat/elofordulasok.tsv` (43 × `kapcsolodas` + `funkcio`), `adat/motivumok.tsv` `meghatarozas` (F239.17) |
| Archívum | `archivum/TEREMT-001/` (régi tanulmány, napló, forrásréteg, törzscikk, 1/a-próza); N58 lezárva |
| Előnézet (repón kívül) | a session scratchpadjában: `elonezet1/lexikon/TEREMT-001_TUDOMANYOS.md` (1329 sor); újra előállítható a lent leírt módon |

**Mérve az előnézeten:** az 1/a 43/43 arany (`proza_1a.lap_meres` az előnézet könyvtárán); az olvasói kapu 5 BUKÁS, mind a generátor saját szövegében (Thayer-fordítás zárójele, „jelölt”, „teljesség-mérése”, „ellenőriztük”, „a lap elején áll” táblaelem), a prózában 0; `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba.

## Nyitott, az U1b után — célzott ellenőrzés (a következő session feladata)

- Az U1b lezárult (F239.15 `0645c1cf`, F239.16 `b9064dc0`; átadó: `naplok/F239_atado_U1b.md`): a lánc az 1Móz 1–8 (DT-F239e), a 9. blokk ószövetségi táblája 3 vers (1Móz 1:2, 7:11, 8:2); a tanúréteg 28 sor, köztük 5 saját szavas atyai tanú (Jeromos: Hab 3:10, 1Móz 1:2, Zsolt 77:17, Jón 2:6; Órigenész: Luk 8:31).
- A Kivonat és a 10. Értelmezés minden mondata, amely a fordítókról, a recepcióról vagy a tanúkról szól, összevetve a kész 9. Hatástörténettel (6-os sablon, „A 9. Hatástörténet szabályai” 6. pont: a 10. nem állít többet a 9.-nél); ahol a 9. többet vagy mást mond, egy kéz igazít. A próza érintett helyei: a Kivonat 1. bekezdésének zárómondata (a görög fordítás); a Miért fontos „A Septuaginta hídja” rése; a Remez „az Újszövetség” bekezdése (a görög Ószövetség igéi); a Vitatott pontok V1 (Gunkel a BDB-ből; „a kommentárirodalomban”), V2 (a görög 1Móz 8:2 igéje), V3, V4 (a görög zsoltárok).
- A lánc változása: a próza „a Genezis négy helye” (Remez) és a funkció-csoportok a motívum helyeiről szólnak, nem a 9. blokk láncáról; megnézendő, hogy a 9. blokk 3 verses ÓSZ-táblája mellett a próza nem mond-e róla mást.

## Az előnézet előállítása

`python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívüli könyvtár>` (előtte `python.exe`-lista, egyszerre egy nehéz futás). Két akadály miatt ma csak ideiglenes, nem commitolt kerülőúttal fut (l. a Generátor-hiányok 1. és 2. pontját): a `adat/motivum_kapcsolatok.tsv`-ben a `DT-F239a` helyőrző ideiglenesen `DT9991`, és az `eszkozok/lapgen/megjelenites/md/kizart.py` 10-szeresnél kisebb arány-mondatának hibája kikapcsolva; futás után mindkettő visszaáll.

## Generátor-hiányok (nem az U3 hatásköre; az integrátornál)

1. **A 3. szakasz arány-mondata** (`lapgen/megjelenites/md/kizart.py`; N-F239a, `nyitott/uj/nervous-kare-9d2361.md`, a 218c-re): ha a vizsgált versek és a motívumhelyek aránya legfeljebb 10-szeres, a generátor `ValueError`-ral megáll („nincs leképezve”). A TEREMT-001 aránya kb. 3. Kell egy nyelvi mondat (vagy a mondat elhagyása) — generátor-változás, nehéz kör.
2. **A döntés-helyőrző a kapcsolatsorban**: az ágon a `DT-F239a` helyőrző a B46 olvasói kapuján megáll; a merge utáni számkiosztás után magától rendeződik.
3. **A BDB-versjelentés tábla (B19, `adat/bdb_vers_jelentes.tsv`, gyártója: `eszkozok/olvaso_szerver/bdb_vers_jelentes.py`)** — *az integrátor döntése: a #240 (PR #821) bővül vele, a gyökérok minden szóra, gépi kapuval; a lapon kézzel nem kerüljük meg; a #239 kiadása addig vár.*: a tehóm (H8415) szócikkében a „(but see 5 infra)” utalást az 5. jelentés kezdetének olvassa, ezért a szócikk 22. pozíciója utáni minden igehely az 5. jelentést („abyss = Seol”, magyarul „örvény”) kapja. A lap 1. táblájának „Jelentés (a szó)” oszlopa így minden ószövetségi soron „örvény · 5”, a lábjegyzet pedig azt mondja, hogy „a BDB az 5. szakaszban maga idézi a helyet” — ez az 1Móz 49:25-re, a 7:11-re stb. hamis. Olvasói hiba, kiadás előtt javítandó; a gyártó szkript és a tábla újragenerálása más szavakat is érinthet. **Az integrátornak elküldve; döntés: #240.**
4. **A teljesség-mérés rögzített útvonala** (B05/B06 `naplok/F123_teljesseg_<ID>…`): a nem F123-as motívum mérését is ott keresi; a TEREMT-001-nél másolattal megoldva (F239.14).

## Az U4 bemenete

- A próza ellenőrzése: `python eszkozok/proza_allitas.py TEREMT-001`, utána az `allitas-ellenor` subagent → `naplok/ALLITAS_TEREMT-001_itelet.md` (független F2-mérés). Figyelem: a `proza_1a.py` és az `olvasoi_kapu.py` alapból a `lexikon/` régi, befagyasztott lapját méri (a TEREMT-001 a `lap_befagyasztas.tsv`-ben áll), nem az új generátor kimenetét: az olvasói kapuhoz `--lexikon-konyvtar <előnézet>/lexikon`, az 1/a-hoz `proza_1a.lap_meres('TEREMT-001', gyoker=<előnézet>)`.
- **Az U2 átadójának U4-listája** (`naplok/F239_atado_U2.md`): a Kivonat „nem cselekszik Isten ellen” mondata és a V1 Vitatott pontja egyezik-e; a Remez nem mondja-e, hogy a Jel 20 „megismétli” a 8:2-t; a Sod és a Módszertan nem mondja-e „a halál mélyét” az Ez 31:15-re; a V4 ténye és nyitott kérdése külön mondatban áll-e.
- A próza saját döntései, amelyeket a lektor nézzen: a Kivonat fordulópontja (az Újszövetség: a víz helyett zárt hely); a Sod zárómondata („a határ felülről jön”, a Jelenések két kulcs-helye és az ezer esztendő); a Drash két tétele; a 2Móz 15:5 1/a-ja (a magyar „mélység” ott a mecólá).
- A visszhang (U1b) a prózával párhuzamosan készül; ha a Hatástörténet-blokk egy prózamondatnak ellentmond, a javítókör (U6) igazítja. A próza az ókori fordítókról és értelmezőkről a Septuaginta lexikai adatán (30/35 vers, 4 többlet) túl nem állít.

## Mit NEM kell elolvasni

Az archivált régi fájlokat; az U1 nyers kimeneteit; a két bírálat teljes szövegét (a válaszok az érvnapló D és D2 szakaszában); a `naplok/F239_U3_*.py` szkripteket (a commit-üzenetek leírják, mit tesznek).

## Nyitott döntések

- A B19 BDB-hiba → #240 (PR #821); a 3. szakasz arány-mondata → N-F239a (218c). Mindkettő kiadás előtt kell.
- A célzott ellenőrzés az U1b után (fent): nyitott, a következő Opus-sessioné.
- A tartalmi döntések (határ, kizárási szabály) változatlanok; új határkérdés nem merült fel.
