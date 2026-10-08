# F22_2Kron_jelentes.md — Károli–Strong párosítás: 2Krónika (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Kron`, `egyesit.py --ellenoriz --konyv <könyv>`, `f22_elemzes.py --konyv 2Krón`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Krón-sorainak összesítése, a `f22/api_termeles/high/_munka/2Kron_k*.json` hibaüzenetei). Ág: `claude/f22-2kron` (az 1Krón PR #253 merge-e után, a main-ről). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Sorrend: DT57 (1), a BDB-haszon mérése szerint az 1Krón után a 2Krón.*

*Az `f22_elemzes.py` a magyar könyvnévvel (`2Krón`) futott; az ASCII-név (`2Kron`) a régi arany szűrésén némán 0-t ad (l. `naplok/ELLENOR_F22_1Kron.md` 1. eltérés). A 2Krónnál a két futás kimenete a régi arany pontján is azonos, mert a `Karoli_Strong_kivonat.tsv`-ben nincs `2Ch` sor (az `1Ch`-nak 6 van).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.08, chat: „mehet a 2 krónika”)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a 2Krón tiszta (822/822 vers, 36 fejezet, K-hiány 0, E-hiány 0, eltolt 0), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Krón'`).
- **Minta:** `f22/minta_2Kron.tsv`, 822 vers (= a `Karoli_1908.tsv` `2Krón ` sorai), 83 köteg (10 vers/köteg, az utolsó 2).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_018KwM1zea9Lr19sujwPESFE`, 83 kérés (2026-10-08T15:02Z); javító kör `msgbatch_016HDbJ9Ca6BvRQKwmGReEfL`, 10 kérés (15:10Z).
- **Futásnapló** (2Krón: 93 sor, `futas=api_termeles/high/2Kron`): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézs, a Jer és az 1Krón soraiban).

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 83 | 73 | 10 köteg (14 vers) | 6,0758 | 988 993 / 1 017 361 |
| 2. próba (javító) | 10 | 10 | 0 | 0,2425 | 143 769 / 19 745 |
| **összesen** | 93 | | | **6,3183** | |

A javító körbe került kötegek: 6, 9, 12, 19, 22, 23, 40, 47, 75, 82. Mind versszintű kapuhiba (gazdátlan eredeti sorszám, kétszer vagy sehol sem szereplő magyar sorszám, üres partnerlista); **formátumhibás (érvénytelen JSON) köteg nincs** (az 1Krónnál öt volt).

A könyvplafonból (822 × 0,0074 × 1,5 = 9,12 USD) 6,32 fogyott; a futásnapló futó összege 27,0121 USD (Ézs 7,0834 + Jer 9,0552 + 1Krón 4,5552 + 2Krón 6,3183), a globális 110 USD-ből.

**A versenkénti költség 0,0077 USD: az API-s könyvek közül ez az első, amely a plafon alapját (0,0074) meghaladja** (Ézs 0,0055, Jer 0,0066, 1Krón 0,0048). Az ok a kimenet: az 1. körben 1 017 361 kimeneti token 822 versre, az 1Krónnál 631 833 volt 942 versre. A plafon (×1,5) bőven fedte; a hátralévő könyvekre adott, 0,0074-gyel számolt költségbecslés viszont ennél a könyvnél alulbecslés lett volna.

## 1a. Szkriptkimenet

```
Sonnet: 83 köteg, 822 vers; kapuhiba első próbára 1.7% (14/822); végleg 0.0% (0/822)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Kron`: `parok_2Kron.tsv` 20 341 link (mind `alacsony`, `S`; a fájl 20 343 sora a proveniencia- és a fejlécsorral), `szavak_2Kron.tsv` 41 218 token (41 220 sor). A szavak bontása: hu 20 132 (16 044 `parositva`, 4 088 `betoldas`), er 21 086 (18 820 `parositva`, 2 266 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `2Krón ` sorainak száma (21 086). Az átnézési sor (`naplok/F22_2Kron_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv <könyv>` (2026.10.08, ezen az ágon): 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón — mind „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Krón` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/20341), alacsony 100.0% (20341/20341), kezi 0.0% (0/20341); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/41218), alacsony 100.0% (41218/41218), kezi 0.0% (0/41218).

Link-forrás megoszlás (parok): S 20341. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 822 (2Krón 10:1, 2Krón 10:10, 2Krón 10:11, 2Krón 10:12, 2Krón 10:13, 2Krón 10:14, 2Krón 10:15, 2Krón 10:16, 2Krón 10:17, 2Krón 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 416 | 0.0% (0/416) | 100.0% (416/416) | 0.0% (0/416) | 845 | 0.0% (0/845) | 100.0% (845/845) | 0.0% (0/845) |
| 2 | 532 | 0.0% (0/532) | 100.0% (532/532) | 0.0% (0/532) | 1007 | 0.0% (0/1007) | 100.0% (1007/1007) | 0.0% (0/1007) |
| 3 | 323 | 0.0% (0/323) | 100.0% (323/323) | 0.0% (0/323) | 713 | 0.0% (0/713) | 100.0% (713/713) | 0.0% (0/713) |
| 4 | 413 | 0.0% (0/413) | 100.0% (413/413) | 0.0% (0/413) | 929 | 0.0% (0/929) | 100.0% (929/929) | 0.0% (0/929) |
| 5 | 365 | 0.0% (0/365) | 100.0% (365/365) | 0.0% (0/365) | 772 | 0.0% (0/772) | 100.0% (772/772) | 0.0% (0/772) |
| 6 | 1262 | 0.0% (0/1262) | 100.0% (1262/1262) | 0.0% (0/1262) | 2354 | 0.0% (0/2354) | 100.0% (2354/2354) | 0.0% (0/2354) |
| 7 | 607 | 0.0% (0/607) | 100.0% (607/607) | 0.0% (0/607) | 1229 | 0.0% (0/1229) | 100.0% (1229/1229) | 0.0% (0/1229) |
| 8 | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) | 871 | 0.0% (0/871) | 100.0% (871/871) | 0.0% (0/871) |
| 9 | 738 | 0.0% (0/738) | 100.0% (738/738) | 0.0% (0/738) | 1456 | 0.0% (0/1456) | 100.0% (1456/1456) | 0.0% (0/1456) |
| 10 | 499 | 0.0% (0/499) | 100.0% (499/499) | 0.0% (0/499) | 953 | 0.0% (0/953) | 100.0% (953/953) | 0.0% (0/953) |
| 11 | 405 | 0.0% (0/405) | 100.0% (405/405) | 0.0% (0/405) | 819 | 0.0% (0/819) | 100.0% (819/819) | 0.0% (0/819) |
| 12 | 365 | 0.0% (0/365) | 100.0% (365/365) | 0.0% (0/365) | 759 | 0.0% (0/759) | 100.0% (759/759) | 0.0% (0/759) |
| 13 | 520 | 0.0% (0/520) | 100.0% (520/520) | 0.0% (0/520) | 1064 | 0.0% (0/1064) | 100.0% (1064/1064) | 0.0% (0/1064) |
| 14 | 364 | 0.0% (0/364) | 100.0% (364/364) | 0.0% (0/364) | 731 | 0.0% (0/731) | 100.0% (731/731) | 0.0% (0/731) |
| 15 | 407 | 0.0% (0/407) | 100.0% (407/407) | 0.0% (0/407) | 797 | 0.0% (0/797) | 100.0% (797/797) | 0.0% (0/797) |
| 16 | 398 | 0.0% (0/398) | 100.0% (398/398) | 0.0% (0/398) | 768 | 0.0% (0/768) | 100.0% (768/768) | 0.0% (0/768) |
| 17 | 365 | 0.0% (0/365) | 100.0% (365/365) | 0.0% (0/365) | 703 | 0.0% (0/703) | 100.0% (703/703) | 0.0% (0/703) |
| 18 | 804 | 0.0% (0/804) | 100.0% (804/804) | 0.0% (0/804) | 1639 | 0.0% (0/1639) | 100.0% (1639/1639) | 0.0% (0/1639) |
| 19 | 294 | 0.0% (0/294) | 100.0% (294/294) | 0.0% (0/294) | 570 | 0.0% (0/570) | 100.0% (570/570) | 0.0% (0/570) |
| 20 | 921 | 0.0% (0/921) | 100.0% (921/921) | 0.0% (0/921) | 1818 | 0.0% (0/1818) | 100.0% (1818/1818) | 0.0% (0/1818) |
| 21 | 496 | 0.0% (0/496) | 100.0% (496/496) | 0.0% (0/496) | 969 | 0.0% (0/969) | 100.0% (969/969) | 0.0% (0/969) |
| 22 | 345 | 0.0% (0/345) | 100.0% (345/345) | 0.0% (0/345) | 716 | 0.0% (0/716) | 100.0% (716/716) | 0.0% (0/716) |
| 23 | 522 | 0.0% (0/522) | 100.0% (522/522) | 0.0% (0/522) | 1232 | 0.0% (0/1232) | 100.0% (1232/1232) | 0.0% (0/1232) |
| 24 | 661 | 0.0% (0/661) | 100.0% (661/661) | 0.0% (0/661) | 1391 | 0.0% (0/1391) | 100.0% (1391/1391) | 0.0% (0/1391) |
| 25 | 734 | 0.0% (0/734) | 100.0% (734/734) | 0.0% (0/734) | 1490 | 0.0% (0/1490) | 100.0% (1490/1490) | 0.0% (0/1490) |
| 26 | 582 | 0.0% (0/582) | 100.0% (582/582) | 0.0% (0/582) | 1139 | 0.0% (0/1139) | 100.0% (1139/1139) | 0.0% (0/1139) |
| 27 | 190 | 0.0% (0/190) | 100.0% (190/190) | 0.0% (0/190) | 370 | 0.0% (0/370) | 100.0% (370/370) | 0.0% (0/370) |
| 28 | 674 | 0.0% (0/674) | 100.0% (674/674) | 0.0% (0/674) | 1408 | 0.0% (0/1408) | 100.0% (1408/1408) | 0.0% (0/1408) |
| 29 | 818 | 0.0% (0/818) | 100.0% (818/818) | 0.0% (0/818) | 1761 | 0.0% (0/1761) | 100.0% (1761/1761) | 0.0% (0/1761) |
| 30 | 685 | 0.0% (0/685) | 100.0% (685/685) | 0.0% (0/685) | 1411 | 0.0% (0/1411) | 100.0% (1411/1411) | 0.0% (0/1411) |
| 31 | 553 | 0.0% (0/553) | 100.0% (553/553) | 0.0% (0/553) | 1160 | 0.0% (0/1160) | 100.0% (1160/1160) | 0.0% (0/1160) |
| 32 | 886 | 0.0% (0/886) | 100.0% (886/886) | 0.0% (0/886) | 1708 | 0.0% (0/1708) | 100.0% (1708/1708) | 0.0% (0/1708) |
| 33 | 604 | 0.0% (0/604) | 100.0% (604/604) | 0.0% (0/604) | 1205 | 0.0% (0/1205) | 100.0% (1205/1205) | 0.0% (0/1205) |
| 34 | 882 | 0.0% (0/882) | 100.0% (882/882) | 0.0% (0/882) | 1876 | 0.0% (0/1876) | 100.0% (1876/1876) | 0.0% (0/1876) |
| 35 | 715 | 0.0% (0/715) | 100.0% (715/715) | 0.0% (0/715) | 1449 | 0.0% (0/1449) | 100.0% (1449/1449) | 0.0% (0/1449) |
| 36 | 577 | 0.0% (0/577) | 100.0% (577/577) | 0.0% (0/577) | 1136 | 0.0% (0/1136) | 100.0% (1136/1136) | 0.0% (0/1136) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36.

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

- Nincs: a 2Krónikában nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–1Krón menetekben); a versbeosztás a detektor szerint tiszta.
- A régi arany (2.2) a 2Krónban üres: a `Karoli_Strong_kivonat.tsv`-ben nincs `2Ch` sor, ez valódi üres eredmény, nem szűrési hiba.

## 4. Kiegészítések ebben a menetben

- K9: a 2Krón bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag` (`claude/f22-2kron`), `kovetkezo`, `ir`, D21, v2.15.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_2Kron.md`.
- A korábbi kézi átnézések (1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1) továbbra is a felhasználóé.
- A következő könyv indítása a felhasználó döntése (⛔ 2.). A DT57 (1) mérése szerint a sorrend: Ezsd 162, Jób 159, Ez 147, Péld 145 szócikk; a Jób előtt TAHOT-hiány (Jób 40:1–5, 41) és döntés az 1:2 / 2:1 támogatásról.
