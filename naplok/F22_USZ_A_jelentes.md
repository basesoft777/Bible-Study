# F22_USZ_A_jelentes.md — a 22.9 A csomag összesítője (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim)

*A számok szkriptkimenetből jönnek: a 11 könyvjelentés (`naplok/F22_<könyv>_jelentes.md`), `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py --ellenoriz`, a `f22/api_termeles/futasnaplo.tsv` és a `f22/api_termeles/high/_munka/*.json` (a javító körbe került kötegek). Ág: `claude/amazing-mayer-t276r0`. Módszer: D45 (csak Sonnet, Message Batches API, `effort=high`, `prompt_v3`, 10 verses kötegek, soros futtatás a fenti sorrendben). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Könyvenként

| könyv | Károli-vers | modellhez | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körbe került köteg | `[nem TR]` | ebből párosított | régi arany (kizárás nélkül) |
|---|---|---|---|---|---|---|---|---|---|---|
| Tit | 46 | 46 | 6 | 0.2162 | 0.0047 | 6/46 | k005 (egész köteg: érvénytelen JSON, 6 vers) | 11 | 0 | nincs hármas |
| 2Thessz | 47 | 47 | 5 | 0.2809 | 0.0060 | 0/47 | — | 20 | 0 | nincs hármas |
| 2Pét | 61 | 61 | 8 | 0.3593 | 0.0059 | 1/61 | k005 (versenkénti, 1 vers) | 36 | 2 | 100.0% (2/2) |
| 2Tim | 83 | 83 | 13 | 0.4118 | 0.0050 | 31/83 | k003 (egész köteg: érvénytelen JSON, 10 vers); k007 (egész köteg: érvénytelen JSON, 10 vers); k008 (egész köteg: érvénytelen JSON, 10 vers); k009 (versenkénti, 1 vers) | 21 | 0 | 100.0% (1/1) |
| 1Thessz | 89 | 89 | 13 | 0.5074 | 0.0057 | 12/89 | k001 (versenkénti, 1 vers); k002 (versenkénti, 1 vers); k007 (versenkénti, 1 vers); k009 (egész köteg: érvénytelen JSON, 9 vers) | 36 | 2 | 0.0% (0/1) |
| Kol | 95 | 95 | 11 | 0.5107 | 0.0054 | 10/95 | k007 (egész köteg: érvénytelen JSON, 10 vers) | 45 | 10 | nincs hármas |
| Fil | 104 | 102 | 13 | 0.4975 | 0.0049 | 12/102 | k006 (egész köteg: érvénytelen JSON, 10 vers); k011 (egész köteg: érvénytelen JSON, 2 vers) | 37 | 2 | nincs hármas |
| 1Pét | 105 | 105 | 11 | 0.5728 | 0.0055 | 0/105 | — | 53 | 1 | 100.0% (1/1) |
| 1Ján | 105 | 105 | 11 | 0.6526 | 0.0062 | 0/105 | — | 43 | 1 | nincs hármas |
| Jak | 108 | 108 | 11 | 0.5162 | 0.0048 | 0/108 | — | 52 | 7 | nincs hármas |
| 1Tim | 113 | 113 | 14 | 0.5429 | 0.0048 | 20/113 | k003 (egész köteg: érvénytelen JSON, 10 vers); k004 (egész köteg: érvénytelen JSON, 10 vers) | 21 | 2 | nincs hármas |
| **össz** | **956** | **954** | **116** | **5.0680** | **0.0053** | **92/954** | | **375** | **27** | |

A végleges kapuhiba mind a 11 könyvben 0; az `egyesit.py --konyv <könyv> --ellenoriz` mind a 11-re „rendben”. A futásnapló minden új sorában `prompt_sha256_12 = 84f12ca7aafb` (a `prompt_v3` változatlan).

## 2. Költség, keret, újravetítés

- Az A csomag költsége **5.0680 USD** (0.0053 USD/vers, a 22.8 vetítése 5,28 USD volt). A futó összeg 91.437851 USD; a 18 USD-s ÚSZ-keretből (86,3698 + 18 = 104,3698) **12.93 USD maradt** (a kódbeli plafon 104,36 USD).
- Mért egységár a 22.8 és az A együtt: (0.4251 + 5.0680) / (77 + 954) = **0.005328 USD/vers**.

| csomag | vers | vetítés a mért egységárral | ×1,2 tartalékkal |
|---|---|---|---|
| B (Gal, Ef, 2Kor, Zsid) | 863 | 4.60 USD | 5.52 USD |
| C (Róm, 1Kor, Jel) | 1272 | 6.78 USD | 8.13 USD |
| B + C | 2135 | 11.38 USD | 13.65 USD |

A B a maradék 12.93 USD-be biztosan belefér. A B + C ×1,2 tartalékkal (13.65 USD) több a maradéknál; a 22.9 szerint a C-ről a B utáni mért egységárral születik döntés.

## 3. Kapuhiba

Első próbára 92/954 vers (9.6%), végleg 0. Ebből **87 vers egész köteg formátumhibából** jött (a köteg nyers válasza nem érvényes JSON; a 22.8-ban leírt minta: tömb nélküli versobjektumok, prózai közbeszúrás), **5 vers versenkénti kapuhibából** (érvényes JSON, a kapu szabályán bukott: pl. „ezek az eredeti szavak sem a parok jobb oldalán…”, „hibás pár”). A 2Tim első próbás aránya (31/83) három egész formátumhibás kötegből jön (k003, k007, k008), nem tartalmi hibából. A javító kör mind a 11 könyvben 0-ra hozta.

## 4. A `[nem TR]` tokenek: 375, ebből 27 párosított (eltérés a 22.8 P4 elvárásától)

A 22.8-ban mind az 51 `[nem TR]` token `forditatlan` lett; az A csomagban 27/375 (7.2%) **párosított**. Ok (a `tokenek.betolt_eredeti` docstringje szerint): ahol a TR **más alakot** olvas, mint a kritikai szöveg, a TR-es alaknak nincs sora a `TAGNT_kivonat.tsv`-ben; a Károli szavának így a nem TR-es sor az egyetlen görög megfelelője, és a modell ahhoz köti (a `prompt_v3` K szabálya ellenére). A link jelentés szerint többnyire helyes, de a `strong` a kritikai szöveg alakjáé, nem a TR-é (pl. ha a TR más igét olvas, a Strong-szám is más). Az egyes esetek TR-olvasatát ez a menet nem ellenőrizte (külön lekérdezés kell, a TAGNT-kivonatban nincs meg).

| vers | er | alak | Strong | angol tükör | Károli-szó (partner) |
|---|---|---|---|---|---|
| 2Pét 2:21 | 13 | ὑποστρέψαι | G5290 | to have turned | elpártoljanak |
| 2Pét 2:22 | 18 | κυλισμὸν | G2946 | rolling place | fertőjébe |
| 1Thessz 1:7 | 4 | τύπον | G5179 | an example | példaképekké |
| 1Thessz 2:3 | 11 | οὐδὲ | G3761 | nor | ? |
| Kol 2:2 | 6 | συμβιβασθέντες | G4822 | being knit together | egybeköttetvén |
| Kol 2:2 | 13 | πλοῦτος | G4149 | richness | gazdagságára |
| Kol 2:12 | 5 | βαπτισμῷ | G0909 | baptism | keresztségben |
| Kol 3:22 | 12 | ὀφθαλμοδουλίᾳ | G3787 | eye-service | ? |
| Kol 3:22 | 21 | κύριον. | G2962 | Lord. | Istent |
| Kol 4:1 | 18 | οὐρανῷ. | G3772 | heaven. | mennyekben |
| Kol 4:12 | 18 | σταθῆτε | G2476 | you may be stood | megállhassatok |
| Kol 4:12 | 21 | πεπληροφορημένοι | G4135 | fully complete | ? |
| Kol 4:15 | 7 | Νύμφαν | G3564 | Nympha | Nimfást |
| Kol 4:15 | 12 | αὐτῆς | G0846 | of her | ? |
| Fil 1:11 | 2 | καρπὸν | G2590 | with [the] fruit | gyümölcsével |
| Fil 3:21 | 26 | αὐτῷ | G0846 | to Him | maga |
| 1Pét 3:1 | 22 | κερδηθήσονται, | G2770 | they will be gained, | megnyeressenek |
| 1Ján 1:5 | 5 | ἀγγελία | G0031 | message | üzenet |
| Jak 2:20 | 13 | ἀργή | G0692 | worthless | megholt |
| Jak 3:4 | 22 | βούλεται. | G1014 | decides. | akarja |
| Jak 3:8 | 8 | ἀκατάστατον | G0182 | [it is] an unruly | fékezhetetlen |
| Jak 4:5 | 14 | κατῴκισεν | G6052 | he settled | lakozik |
| Jak 4:9 | 11 | μετατραπήτω | G6060 | should be turned | forduljon |
| Jak 4:12 | 17 | κρίνων | G2919 | judging | kárhoztatod |
| Jak 4:12 | 19 | πλησίον; | G4139 | neighbour? | másikat |
| 1Tim 2:14 | 8 | ἐξαπατηθεῖσα | G1818 | having been deceived | megcsalattatván |
| 1Tim 6:11 | 16 | πραϋπαθίαν· | G6073 | [and] gentleness; | szelídséget |

## 5. N-F22c: a Fil 1:16–17

A két vers görög szövege a `TAGNT_kivonat.tsv`-ben nincs meg (a TAGNT Fil 1:15 a „τινὲς μὲν …”, a Fil 1:18 a „τί γάρ; …” szakasz). A mintából kimaradtak (102 vers a modellhez), a szavaik `fuggoben` állapotúak (`kezi` bizonyosság), link nélkül; a `naplok/F22_Fil_atnezes.tsv` két sora jelöli őket. A párosítás nem pótolja.

## 6. Régi arany

Hármas csak négy könyvben van (2Pét 2, 2Tim 1, 1Thessz 1, 1Pét 1); a mért érték az 1. táblában. Az 1Thessz egyetlen hármasa (`1Th.5.23 G4151+G5590 „valótok; lelketek”`) a mérésben 0/1, de ez **mérési műtermék**, nem eltérés: a régi arany Károli-szava két, pontosvesszővel összefűzött szó, amelyet az `f22_elemzes.py` egy kifejezésként keres („a Károli-szó/kifejezés nem található a vers tokenjei közt: 1”). A `parok_1Thessz.tsv` szerint a párosítás ugyanazt adja: „valótok” (hu 14) → πνεῦμα G4151, „lelketek” (hu 16) → ψυχὴ G5590. Az egyezés tehát 4/4, ha a műtermék nélkül számolunk; a mért (kizárás nélküli) érték változatlanul 4/5.

## 7. ⛔ Megállás — a felhasználó döntése

1. A B csomag (Gal, Ef, 2Kor, Zsid; 863 vers, vetítve 4.60 USD) indítása.
2. A párosított `[nem TR]` tokenek (27) kezelése: (a) maradnak (`alacsony`, `S`), a lista itt áll; (b) `kezi`-be tétel egy kézi listával (az `egyesit.py` felülírási tábláján át); (c) a TR-olvasat lekérdezése és esetenkénti ítélet. A döntés a B és a C futását nem érinti, ugyanaz a jelenség ott is várható.
3. (Tájékoztató, döntés nem kell.) Az `f22_elemzes.py` a pontosvesszővel összefűzött régi-arany Károli-szót nem bontja; ez a C csomagban és a korábbi könyvekben is torzíthat. Javítása külön, kis kódfeladat.
