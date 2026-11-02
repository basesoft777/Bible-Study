# Olvasó-szerver tesztjavítás (N-F149a) — napló

Dátum: 2026-11-02 · modell: `claude-sonnet-5-5` · ág: `claude/olvaso-teszt-javitas-c029d1` · alap: `origin/main` (c43c1b4d).

## 1. A mérés

Futtatás: `python eszkozok/teszt_futtat.py` (WSL venv, WSL-natív `~/pardes/pardes.db`, építés 2026-11-02T12:55:43Z — a friss main kódjához és adatához épült, tehát nem elavult DB okozta a bukásokat). A #149 naplója 11 bukást mért; a tervező (`teszt_tervezo`) 1, a BDB-vers 1, a kereső 1, az olvasó-szerver 3, a pilot-aranyminta 5 tesztje bukott.

## 2. Bukásonként: ok és javítás

| Teszt | Ok (a teljes láncon) | Javítás |
|---|---|---|
| `teszt_olvaso_szerver` · `TestD2PilotEgyezes.test_1moz_1_25`, `test_zsolt_22` | A szerver az F128.12 (8a78bfea, 2026-10-21) óta a szakaszonként fordított BDB-Strongokat a közös összefűzőn (`szakasz_bemenet.strong_magyar_sorok`, DT-F128a (a), DT-F128f (3)) olvassa; a D2-mérő (`db_meres.db_szo`) még az „utolsó sor nyer” szabályt használta, így pl. a H0014 magyar BDB-jét hiányzónak látta | `db_meres._bdb_hu`: a közös összefűző (F149.8) |
| `teszt_pilot_aranymintaval` · `…F76f_magyar_alapjelentes…`, `…F76g_bdb_bontas…` | Ugyanaz az ok a pilot-generátornál (`adat.py`): a H0215 magyar BDB-je az utolsó szakaszsor („5 fényleni késztetni…”) lett, ezért az alapjelentése és a bontása eltért | `adat.py`: a közös összefűző, a meta („modell1 / modell2, legkésőbbi dátum”) a szerver formátuma szerint (F149.8) |
| `teszt_pilot_aranymintaval` · `…cimkek_es_utmutato…` | (1) az F128/F38 fordítások óta mind a 8099 BDB-szócikknek van magyar fordítása, így az 1Móz 1 „BDB magyarul” címkéje teljes → nem `arany`; (2) az F22 óta 66 könyv párosított, nem 57 | a teszt a címke osztályát a számlálóból vezeti le, a könyvszámot az adatból veszi (F149.9) |
| `…karoli_strong_konyvek_jelzese…` | az „57 feldolgozott könyv” a pilot kora; F22 (da0a8ea1, eba304a6, 3f8e5cd0, …) óta 66 | a szám az adatból (F149.9) |
| `…magyar_tartalom_a_szo_lapokon` | az N-F131y.2/DT-F131z (9f7ac0e7) óta a megjelenítés a héber sorrendet javítja (pl. „׳ג” → „ג׳”) és a héber futam után LRM-et (U+200E) tesz; a pilot nyers szövegével a 40 karakteres előtag betű szerint nem egyezik | a teszt a héber írásjegyek és az LRM nélkül veti össze a magyar szöveget (F149.9) |
| `teszt_olvaso_szerver` · `TestLapok.test_interlinearis_parositatlan_sor_es_nt` | Az F22 óta az ÚSZ-nek is van `token_par`-ja (Mt: da0a8ea1), ezért az „nincs Károli–Strong párosítás” jelzés a Mt 1:1-en nem jelenhet meg | a teszt megfordítva (F149.9) |
| `teszt_tervezo` · `test_minden_szelektor_talal` | A `.cimkek .cimke.arany` (nem teljes BDB) és az `.allapot.folyamat` („Magyar fordítás nincs”) elem a teljes BDB-magyar óta valódi lapon nem jelenhet meg | indokolt kivétel-lista (`ADATALLAPOT_MIATT_NEM_ELERHETO`), amelynek elemei létező regiszter-elemek kell legyenek (F149.9) |
| `teszt_bdb_vers_jelentes` · `Ujrageneralas.test_bajtra_azonos` | a d940d1d7 (szamkiosztas: DT-F131z → DT445) átírta az `adat/bdb_forras_javitas.tsv`-t, a generált `adat/bdb_vers_jelentes.tsv` fejlécének forrás-hash-e (`6daf33ab54f8`) elavult | újragenerálás `--ts 2026-10-28`-cal; egyetlen fejlécsor változott, soradat nem (F149.10) |
| `teszt_kereses` · `test_szotoken_nelkuli_konyvek_jelzese` | Az F22 óta nincs párosítás nélküli könyv. A teszt elvárása avult; de a szerver is hamis állítást tett: a „Nem keresett könyvek (…): .” sor üres listával is megjelent | DT-F149a (A): a sor csak nem üres listánál; a teszt mindkét ágat nézi (F149.11) |
| (új, a bukáson kívül) szó-lap Károli-alakok | „…a többi könyv még hiányzik” — 66/66 könyvnél hamis | DT-F149a (A): a tagmondat csak akkor áll, ha van párosítás nélküli könyv (F149.11) |

## 3. N-F131z — a fennmaradó három kifejezés

DT-F149b ((a) változat): a BDB-fordítás `forras_hash`-e a javítás nélküli forrásnézetet követi; a héber sorrend-cserét a megjelenítés végzi a magyar szövegben is. A `javitva` kifejezések 13 049 / 13 052-je betű szerint áll a magyarban; a fennmaradó 3 (a fordító átírta vagy szétszedte a héber futamot), a `naplok/BDB_HEBER_SORREND_forditas_kezi.tsv` szerint:

| Strong | szakasz | mi tér el |
|---|---|---|
| H1980 | sz17 | a forrás-alak („י י׳אֲרוֺן ׳)”) nincs betű szerint a magyar szövegben |
| H4828 | sz2 | a forrás-alak („מֵרָעָה (יָסֻר)”) nincs betű szerint a magyar szövegben |
| H8034 | sz5 | a forrás-alak („בְלִישֵֿׁ בְּנֵי”) nincs betű szerint a magyar szövegben |

Kézi javításuk: N-F149b (nem sürgős; a megjelenítésben a forrás alakja marad).

## 4. Megjegyzések

- A `teszt_szintek.py` (lassú) nem része a mérésnek (`--gyors`).
- Az `adat/bdb_vers_jelentes.tsv` újragenerálása adat-réteg-érintés, az orkesztrátor jóváhagyta (2026-11-02).
