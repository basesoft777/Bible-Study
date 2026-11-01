# THAYER_KAROLI_TELJES (#153) — napló

*Modell: `claude-sonnet-5-5` (egyezik a brief `sonnet` mezőjével). Proveniencia: scope=adat/forditasok.tsv (Thayer, G1941 sz1–sz4), adat/karoli_strong/parok_*.tsv | forras=`eszkozok/thayer_jelolt/karoli_ujraellenoriz.py --meres`, `forditas.py elokeszit/ellenoriz` | ts=2026-11-01*

## M0 — mérés (`THAYER_KAROLI_TELJES_meres.tsv`)
78 nem `elavult` Thayer-sor, régi (Mt, Mk, Luk, Ján, ApCsel nélküli) és teljes mankóval: 1 megerősítés (G4151 sz4), 53 változatlan, 17 `nem_talal` a teljes mankóval is (a régivel is az volt), 8 G1941-sor, ahol a leggyakoribb Károli-tő `hívj`→`segí`. Új, a pótlás miatti `nem_talal` nincs.

## Döntés — DT-F153a
Felhasználó, 2026-11-01, az orkesztrátor chatjében, az orkesztrátor üzenetében szó szerint idézve: „b” (a szűk (b) javaslatra). Tartalma: csak a G1941 sz1–sz4 fordul újra; minden más sor marad; a `kezi` G1941 `teljes` sor csak listára kerül.

## M2 — újrafordítás eredménye
- A G1941 teljes promptja (v5.1, mai adatblokk: 41 link, a ÚSZ-ből le nem fedett könyv: nincs) újra elkészült (`elokeszit`).
- sz1 (címsor `G1941 — ἐπικαλέω`) és sz2 (nyelvtani alakok): nincs jelentésszó, amit a Károli-mankó érintene; a fordítás betűre azonos.
- sz3 (1. jelentés, „nevet adni, elnevezni”) és sz4 (2. jelentés, „az ő nevén hívják”): a „segítségül” a 4–5. jelentés (sz6, sz7) Károli-alakja, ezek az ott álló sorokban már szerepelnek; a sz3/sz4 jelentése a Károli „neveztetik / mellékneve / hívják” csoportja, amelyet a mai fordítás lefed („nevet adni”, „elnevezni”, „nevezitek”, „hívják”). A „segí” mint uralkodó tő hiánya tehát az M0 mérőszám következménye (az uralkodó tő a teljes szócikkre számít, nem szakaszonként), nem fordítási hiba.
- Kísérlet: sz3 „melléknéven nevezni” (Károli „mellékneve ×2”) — a 15. kapu (`15_tiltott`) elutasította (helyette: elnevezni, nevezni), ezért nem rögzíthető.
- A változatlan vázlat (7 szakasz) minden kapun átment (`ATMENT`, 15_tiltott: 0 találat); a vázlat és a végleges szöveg azonos.
- **Következmény: az `adat/forditasok.tsv` nem változott** (0 sor; újrarögzítés ugyanazzal a szöveggel csak dátum-/modellmezőt írna át). Bájt-összevetés: nincs írás.

## `kezi` sorok listája (a felhasználónak, c)
G1941 `teljes` (kezi, nem fordult újra; érvényes marad).

## M1 — eszköz és teszt
`karoli_ujraellenoriz.py` (+ 3 teszt a `teszt_lanc.py`-ban); az `adatblokk.py` docstringje és a `test_g1941_reszei` az új tényhez igazítva (2026-11-01 óta nincs le nem fedett ÚSZ-könyv, PR #537).
A `teszt_lanc.py` 37 tesztjéből 36 zöld; a `Sigla.test_tabla_determinisztikus_es_kezi_vedett` bukik (jelölt 255, az elvárt 0): a sigla-tábla adata, nem e tétel módosítása okozza; külön nyomon követendő.
