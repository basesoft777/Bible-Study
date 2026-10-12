# F22_Bir_jelentes.md — Károli–Strong párosítás: Bírák (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Bír`, `egyesit.py --konyv Bír` és `--ellenoriz`, `f22_elemzes.py --konyv Bír`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Bír-sorainak összesítése (`futas = api_termeles/high/Bir`, `cimke = bir`), a `f22/api_termeles/high/_munka/Bir_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, a Péld-menet után (`ced1bf8`); a Péld még nincs a main-ben. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a DT57 (1) mért listájából csak a Jób maradt (döntésre vár, `naplok/F22_Peld_jelentes.md` 5.). A BDB-haszon friss mérése (`naplok/F22_konyvsorrend_meres.py`, 2026-10-09T06:17Z, a Péld-del együtt) szerint a tiszta versbeosztású könyvek közül a Bír adja a legtöbbet a 7. adagnak az Eszt után (77 előfordulás, 2 NINCS-szócikk) és a hátralévő sornak a Dán és a Jób után (655 / 98); a DT54 is ezt tette a Zsoltárok utánra. Indítás: felhasználó, chat, 2026.10.09: „mehet a birák”.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.09)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Bír tiszta (618/618 vers, 21 fejezet), a listában nincs sora. Szimuláció: nyers 618 vers / 15 384 token = leképezett 618 vers / 15 384 token; Károli-vers pár nélkül és gazdátlan vers nincs; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Bír'`).
- **Minta:** `f22/minta_Bir.tsv`, 618 vers (= a `Karoli_1908.tsv` `Bír ` sorai), 62 köteg (10 vers/köteg, az utolsó 8).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01TFbKjz1vBa8zebrv9NJgQb`, 62 kérés (2026-10-09T06:19Z); javító kör `msgbatch_01JrvWTq6Wx6H2iA3DWVnqYx`, 12 kérés (06:25Z).
- **Futásnapló** (Bír: 74 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 62 | 50 | 12 köteg (13 vers) | 4,1310 | 725 431 / 681 118 |
| 2. próba (javító) | 12 | 12 | 0 | 0,2601 | 165 865 / 18 849 |
| **összesen** | 74 | | | **4,3911** | |

A javító körbe került kötegek: 2, 7, 13, 26, 27, 29, 35, 42, 47, 51, 52, 53. Egész köteg nem bukott (formátumhiba nincs); a 13 vers versszintű kapuhiba (9 gazdátlan eredeti sorszám, 3 többször vagy sehol nem szereplő magyar sorszám, 1 hibás pár-forma).

A könyvplafonból (618 × 0,0074 × 1,5 = 6,86 USD) 4,39 fogyott; a futásnapló futó összege 43,4598 USD (Ézs–Péld 39,0687 + Bír 4,3911), a globális 110 USD-ből. Versenként 0,0071 USD (a plafon alapja 0,0074): a Bír hosszú elbeszélő versei miatt a kimenet nagy (681 118 token).

## 1a. Szkriptkimenet

```
Sonnet: 62 köteg, 618 vers; kapuhiba első próbára 2.1% (13/618); végleg 0.0% (0/618)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Bír`: `parok_Bir.tsv` 14 939 link (mind `alacsony`, `S`; a fájl 14 941 sora a proveniencia- és a fejlécsorral), `szavak_Bir.tsv` 29 913 token (29 915 sor). A szavak bontása: hu 14 529 (11 904 `parositva`, 2 625 `betoldas`), er 15 384 (13 932 `parositva`, 1 452 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Bír ` sorainak száma (15 384). Az átnézési sor (`naplok/F22_Bir_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv Bír` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Bír` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/14939), alacsony 100.0% (14939/14939), kezi 0.0% (0/14939); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/29913), alacsony 100.0% (29913/29913), kezi 0.0% (0/29913).

Link-forrás megoszlás (parok): S 14939. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 618 (Bír 10:1, Bír 10:10, Bír 10:11, Bír 10:12, Bír 10:13, Bír 10:14, Bír 10:15, Bír 10:16, Bír 10:17, Bír 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 738 | 0.0% (0/738) | 100.0% (738/738) | 0.0% (0/738) | 1561 | 0.0% (0/1561) | 100.0% (1561/1561) | 0.0% (0/1561) |
| 2 | 562 | 0.0% (0/562) | 100.0% (562/562) | 0.0% (0/562) | 1100 | 0.0% (0/1100) | 100.0% (1100/1100) | 0.0% (0/1100) |
| 3 | 678 | 0.0% (0/678) | 100.0% (678/678) | 0.0% (0/678) | 1407 | 0.0% (0/1407) | 100.0% (1407/1407) | 0.0% (0/1407) |
| 4 | 599 | 0.0% (0/599) | 100.0% (599/599) | 0.0% (0/599) | 1193 | 0.0% (0/1193) | 100.0% (1193/1193) | 0.0% (0/1193) |
| 5 | 520 | 0.0% (0/520) | 100.0% (520/520) | 0.0% (0/520) | 1021 | 0.0% (0/1021) | 100.0% (1021/1021) | 0.0% (0/1021) |
| 6 | 1029 | 0.0% (0/1029) | 100.0% (1029/1029) | 0.0% (0/1029) | 2087 | 0.0% (0/2087) | 100.0% (2087/2087) | 0.0% (0/2087) |
| 7 | 771 | 0.0% (0/771) | 100.0% (771/771) | 0.0% (0/771) | 1543 | 0.0% (0/1543) | 100.0% (1543/1543) | 0.0% (0/1543) |
| 8 | 792 | 0.0% (0/792) | 100.0% (792/792) | 0.0% (0/792) | 1579 | 0.0% (0/1579) | 100.0% (1579/1579) | 0.0% (0/1579) |
| 9 | 1317 | 0.0% (0/1317) | 100.0% (1317/1317) | 0.0% (0/1317) | 2615 | 0.0% (0/2615) | 100.0% (2615/2615) | 0.0% (0/2615) |
| 10 | 365 | 0.0% (0/365) | 100.0% (365/365) | 0.0% (0/365) | 773 | 0.0% (0/773) | 100.0% (773/773) | 0.0% (0/773) |
| 11 | 1001 | 0.0% (0/1001) | 100.0% (1001/1001) | 0.0% (0/1001) | 1933 | 0.0% (0/1933) | 100.0% (1933/1933) | 0.0% (0/1933) |
| 12 | 330 | 0.0% (0/330) | 100.0% (330/330) | 0.0% (0/330) | 663 | 0.0% (0/663) | 100.0% (663/663) | 0.0% (0/663) |
| 13 | 600 | 0.0% (0/600) | 100.0% (600/600) | 0.0% (0/600) | 1202 | 0.0% (0/1202) | 100.0% (1202/1202) | 0.0% (0/1202) |
| 14 | 588 | 0.0% (0/588) | 100.0% (588/588) | 0.0% (0/588) | 1144 | 0.0% (0/1144) | 100.0% (1144/1144) | 0.0% (0/1144) |
| 15 | 511 | 0.0% (0/511) | 100.0% (511/511) | 0.0% (0/511) | 986 | 0.0% (0/986) | 100.0% (986/986) | 0.0% (0/986) |
| 16 | 893 | 0.0% (0/893) | 100.0% (893/893) | 0.0% (0/893) | 1782 | 0.0% (0/1782) | 100.0% (1782/1782) | 0.0% (0/1782) |
| 17 | 320 | 0.0% (0/320) | 100.0% (320/320) | 0.0% (0/320) | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) |
| 18 | 803 | 0.0% (0/803) | 100.0% (803/803) | 0.0% (0/803) | 1646 | 0.0% (0/1646) | 100.0% (1646/1646) | 0.0% (0/1646) |
| 19 | 880 | 0.0% (0/880) | 100.0% (880/880) | 0.0% (0/880) | 1737 | 0.0% (0/1737) | 100.0% (1737/1737) | 0.0% (0/1737) |
| 20 | 1077 | 0.0% (0/1077) | 100.0% (1077/1077) | 0.0% (0/1077) | 2176 | 0.0% (0/2176) | 100.0% (2176/2176) | 0.0% (0/2176) |
| 21 | 565 | 0.0% (0/565) | 100.0% (565/565) | 0.0% (0/565) | 1133 | 0.0% (0/1133) | 100.0% (1133/1133) | 0.0% (0/1133) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 0; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** n.é. (0/0).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): n.é. (0/0).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): n.é. (0/0).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: a Bírákban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.
- **Régi arany nincs a könyvben** (0 hármas a `Karoli_Strong_kivonat.tsv`-ben): ezen a könyvön nincs külső pontossági támpont; a minőséget csak a kapu és a pilot mért értéke (Sonnet 97,3%) jelzi.

## 4. Kiegészítések ebben a menetben

- K9: a Bír bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `kovetkezo`, `ir`, D25, v2.19.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Bir.md`.
- Kézi átnézés: Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- PR és merge a felhasználóé (az ág a Péld- és a Bír-menetet együtt hordozza).
- A következő könyv a felhasználó döntése; a mérés szerinti tiszta jelöltek: Eszt (7. adag: 148), 2Sám, 1Sám, 1Kir, Neh, 2Kir; a Dán (37 detektorsor) és a Jób (41. fejezet, N-F83a) előtt versbeosztás-döntés kell.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Bir.md`)

Az ellenőr egy alacsony súlyú eltérést talált, adatot nem érint. A számokat pontos könyvegyezéssel (`\tapi_termeles/high/Bir\t`, `cimke=bir`, `^Bír `, `Bir_k*.json`) és `lekerdez.py`-jal igazolta. A saját CI-futásában HIBA szintű találat nincs; az E25 3 és az E27 92 találata repószintű.

- **Versbeosztás:** a detektorban és a kézi táblákban nincs Bír-sor; 618/618 kulcs; tartalmi összevetés 1:1, 5:1, 5:31, 21:25 egyezik.
- **Strong a TAHOT-ból:** 76 er-token mintavétele 76/76 egyezik; mind a 15 384 er-sor egyetlen H-Strongot visel.
- **Eltérés (6b, alacsony):** a `672860b` commit tárgya „K9”-et említ, de a `datasetek.tsv`/`SEMA.md` módosítás a `4a9b096`-ban van (annak a tárgya „datasetek.tsv és SEMA 2.20 bővítve” a törzsben). A pusholt történetet nem írom át; a helyes hozzárendelés itt rögzítve.
- **Nem ellenőrizhető az ellenőrnek:** a BDB-mérés számai (a szkriptet nem futtathatta). A mérést az orkesztrátor futtatta (`python naplok/F22_konyvsorrend_meres.py`, 2026-10-09T06:17:56Z): Bír 7. adag 77 / 2, hátralék 655 / 98; Eszt 7. adag 148 / 2; ezek a jelentésben idézett értékek. Az `egyesit.py --ellenoriz` futását az 1a szakasz rögzíti.
