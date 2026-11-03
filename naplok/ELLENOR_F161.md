# ELLENOR_F161 — F161_GLOSSZA_LANC_BRIEF.md, független ellenőrzés (két kör)

*Az ellenőr (`fuggetlen-ellenor`, claude-opus-5-5) fájlt nem tudott írni; a jelentéseit a végrehajtó session rögzíti
itt, az ELTÉRÉS-ek listáját szó szerint, a táblák helyett összefoglalva. A teljes szöveg a session átiratában.*

## 1. kör — `origin/main..f32aa913` (F161.0–F161.4): ELTÉRÉS 6

OK: a feloldó (UBS-re azonos a régi kóddal, a TBESG a `tovabbi_forras`-szal), a 13. szabály változatlan, a prompt egyszer
rögzítve, a `bekuld`/`bevesz`/`kapuz`/`javit`/`beir` kódolvasással rendben, a tiltott fájlok nem változtak, a prompt a
v5.2-vel összhangban, a `dontesek/uj` és `nyitott/uj` formája helyes. NEM ELLENŐRIZHETŐ (parancskorlát): a tesztek, a
`szaraz` és a `prompt` futtatása.

ELTÉRÉS-ek súlyossági sorrendben, és a kezelésük:

| # | az ellenőr szavai | kezelés |
|---|---|---|
| 1 | G2 hamis pozitív tulajdonneveken (Simon, Saul, Anna, Agrippa): a helyes fordítás kétszer bukik | F161.7: a nagy kezdőbetűs szó nem angol maradék; teszt |
| 2 | G3 hamis pozitív a „gerinc” szóra az UBS_DBH-definícióban (H2180) | F161.7: `BELSO_KIVETEL`; teszt |
| 3 | Hiányzó TBESG-szűrés: a lánc a `jelentes_szam = rovid` feltételt nem érvényesíti | F161.7: csak `rovid`, UBS-ből csak glossza/definíció; teszt |
| 4 | 2. kör: sem a `bekuld`, sem a `prompt` nem garantálja a bájtra azonos kérést | F161.7: a javító kérés egyetlen user-üzenet, a `bekuld` mindkét kört bájtra ellenőrzi; teszt |
| 5 | Félrevezető címke: „jóváhagyott” magyar definíció nem jóváhagyott sorra is | F161.7: „jóváhagyott” csak `kezi` sornál |
| 6 | Üres assistant-szöveg a javító kérésben, ha az 1. körös kérés sikertelen volt | F161.7: „(nincs korábbi válasz)” |

## 2. kör — `f32aa913..354c01b3` (F161.5–F161.10): ELTÉRÉS 6

OK: az 1. kör hat javítása; a `forditasok.tsv` diffje csak hozzáadás (366 / 0, 31 hunk), a tábla vége érintetlen, az új
sorok a saját blokkjukban; a #608 ágán csak Thayer-kulcs; a `forras_hash` ~11 soron független táblával egyezik; mind a
366 sorban `sonnet` / `claude-sonnet-5-5` / proveniencia / subagent-út; egyenes idézőjel, helyőrző, belső jel 0; a
UBS-jelek 12 definíción a helyükön; a v1 szöveg a v2-ben betűre azonos, a v1 fájl nem változott; a számok (52/183/131,
definíció 101, 23 kérés, 1 javító kör, TBESH 11 677 sor) egyeznek. NEM ELLENŐRIZHETŐ: a subagent modellneve (saját
bevallás), a teljes kulcs-egyediség (szkript nélkül), a #609, a repón kívüli render és a Feed, a tesztek futtatása.

| # | az ellenőr szavai | kezelés |
|---|---|---|
| 1 | CI E5 HIBA 2. A napló két címsora „TÖRLÉS-SZÁNDÉKOS:” jelölés nélkül törlődött | a napló a PR-ban új fájl: a main-hez mért CI-ben (PR-mód) nincs törölt címsor, a lokális futás 0 HIBA; a jelölés az F161.11 üzenetében mégis szerepel |
| 2 | Kisbetűs tulajdonnevek, 4 sor. „adáma”, „benjámin”, „ráfa” ×2. A kapuk ezt nem jelzik | F161.11: kézi javítás (Adáma, Benjámin, Ráfa ×2), a megjegyzésben jelölve; a kapu és a prompt pótlása: N-F161d |
| 3 | G1944 / 001900001001000 (ἐπάρατος), 2 sor. Olyan bejegyzés kapott fordítást, amelyet a LEXV2_2 kizárt, és az azonos forrású kezi definíciótól eltér | F161.11: a definíció a kezi sor szavával („átkozott állapotra vonatkozó”); hogy a lap ezt a kulcsot keresi-e: N-F161d |
| 4 | Angol köznév a `{L:…}`-jelölésben, 6 sor. A prompt v2 és a G2 kivétel ezt átengedi | a jelölést egyetlen renderelő sem kezeli (a régi `{L:Noah…}` sor is nyers): megjelenítési kérdés, N-F161d; a fordítás nem változott |
| 5 | Helyesírás. „alárendeltted” (31569. sor) | F161.11: „alárendelted” |
| 6 | A prompt v2 verziónaplójából hiányzik a v2-bejegyzés | F161.11: pótolva (a fejlécben, a PROMPT-KEZDET előtt: a kérés szövege nem változik) |

A merge-ről a felhasználó dönt.
