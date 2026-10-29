# VERSMEGF_MT_JAVITAS — napló (FELADATOK #146)

*Brief: `F146_VERSMEGF_MT_JAVITAS_BRIEF.md` · modell: `claude-opus-5-5` (a brief `opus`-t kér; egyezik) · ág: `claude/f146-versmegf-mt-61d410` · 2026-10-28*

Hatókör-bővítés: DT-F146a (az ISTENTISZT-001 lap újragenerálása a #146-ban; a felhasználó szavai a `DONTESEK.md`-ben).

## 1. Módszer (DT207 (c), az F117-eszköz kiterjesztése)

- Szkript: `naplok/F146_mt_felmeres.py` (az `naplok/F117_mt_levezet.py` `igazit`/`jel` függvényét importálja, nem másolja).
- Károli-oldal: `TAHOT_kivonat.tsv` (Károli-kulcs, F85); MT-oldal: `Macula_heber_*.tsv` `ref` oszlopa. A Macula `karoli` oszlopa tanúként kizárva (csak a fájl→könyv hozzárendelésre kell).
- Igazítás: Strong-Jaccard és Jaccard+szószám, monoton DP; blokk: Károli c-1..c+1 ↔ MT c-2..c+2; elfogadás: a két igazítás egyezik és a lépés 1-1.
- Független tanú: a KJV-versszám (`KJV_Strongs_teljes.tsv`). Az MT≠Károli eltérés gépileg akkor igazolt, ha (a) a mért MT-vers azonos a tábla KJV-párjával, vagy (b) ismert MT≠KJV fejezeten (± 1) áll (a Macula-MT és a KJV fejezethossza eltér). Különben `KEZI_OLVASAS`.
- Kimenet: `naplok/F146_mt_felmeres.tsv` (csak az eltérések, a kétséges sorok, a `KEZI` azonossági sorok és a kitöltött `igehely_mt`-jű sorok eltérései; soronként proveniencia).

Proveniencia: `scope=21314 sor (KJV 21031, KEZI 283; üres igehely_mt), + a kitöltött igehely_mt-jű sorok; 929 fejezet, 39 könyv | forras=TAHOT_kivonat.tsv + Macula_heber_*.tsv (ref) + KJV_Strongs_teljes.tsv | eszkoz=naplok/F146_mt_felmeres.py | ts=2026-10-28T21:33Z`

## 2. Jóel (brief 2.1)

A Jóel 1:1–2:27 a mérés szerint Károli = MT (a tábla `KJV`-sora helyes). A **Károli 2:28–32 = MT 3:1–5** és a **Károli 3:1–21 = MT 4:1–21**: 26 vers, mind 1-1 lépés, a két igazítás egyezik, J = 0,83–1,00. A 2:28–29 is ide tartozik (a brief kérdése: a 2:28 = MT 3:1, J = 1,00).

Független KJV-tanú (`naplok/F146_joel_kjv_tanu.py`): a KJV (= Károli-számozás) Strong-halmaza mind a 26 versen a mért MT-verssel erősebb (J = 0,55–1,00), az azonos számú MT-verssel 0,00–0,06. Proveniencia: `scope=Jóel 2:28–3:21 (26 vers) | forras=KJV_Strongs_teljes.tsv+Macula_heber_Joel.tsv(ref) | eszkoz=naplok/F146_joel_kjv_tanu.py | ts=2026-10-28T21:38Z`.

Osztály: a Jóel-sorokban Károli = KJV ≠ MT. Ez **egyik meglévő osztályba sem fér**: `KJV` (üres `igehely_mt`) = Károli = KJV = MT; `MT` = Károli = MT ≠ KJV; `KEZI` kitöltött `igehely_mt`-vel (DT208 (c)) = Károli ≠ KJV és ≠ MT. A brief 2.1 szerint `KEZI` kitöltött `igehely_mt`-vel („ha Károli ≠ MT”); ehhez a `versmegf_javitas.betolt` KEZI-szabályát (`kjv != kar`) bővíteni kell, a fogyasztóknál (`lexikon_general.karoli_mt_vers` jó: a kitöltött `igehely_mt`-t használja) a DT209 őre érvényes.

## 3. Felmérés (brief 2.2) — csak jelentés

| állapot | sor |
|---|---:|
| egyezik (MT = Károli) | 20 323 |
| **eltérés, igazolt** | **982** |
| kétséges (1-2 / 2-1 lépés, `KEZI_OLVASAS`) | 9 |
| `KEZI` sor, Károli = KJV = MT (üres `igehely_mt`; a render nem párosítja) | 93 |
| kitöltött `igehely_mt`, a mérés eltér | 19 (+3 kétséges) |

Az igazolt eltérések könyvenként (a fejezet a Károli-fejezet): 1Kir 32 (4, 5) · 1Krón 117 (6, 12) · 1Móz 33 (31, 32) · 1Sám 15 (21) · 2Kir 22 (11, 12) · 2Krón 33 (2, 14) · 2Móz 63 (8, 22) · 2Sám 44 (18, 19) · 3Móz 30 (6) · 4Móz 77 (13, 16, 17, 30) · 5Móz 74 (12, 13, 22, 23, 29) · Dán 29 (5, 6) · Ez 37 (20, 21) · Hós 15 (1, 12) · Jer 26 (9) · Jób 83 (39, 40, 41) · **Jóel 26 (2, 3)** · Mal 6 (4) · Mik 15 (5) · Neh 68 (4, 7, 9, 10) · Náh 14 (1, 2) · Préd 93 (2, 5, 9, 10, 12) · Zak 17 (1, 2) · Én 13 (7).

Osztály szerint: 827 sor Károli = KJV ≠ MT (a Jóel-esettel azonos új kombináció); 155 sor `KEZI`, Károli ≠ KJV = MT (4Móz 13: 33, Jób 39–40: 49, Préd 2/9/10/12: 73), ahol a tábla KJV-párja maga a tanú.

Megjegyzés: 4 sorban az azonos számú MT-vers Jaccardja is ≥ a mértnél (1Krón 6:1, 3Móz 6:1, 4Móz 17:1, Ez 21:1). Ezek formulaversek, ezért a blokk-igazítás dönt, és a mért pár a szokásos KJV↔MT megfeleltetés. Alacsony J (< 0,6): 1Krón 6:28 (0,57), Neh 10:6 (0,50), mindkettő névlista.

Kétséges (tételes, nem találgatás): 1Krón 12:4 → MT 12:4;12:5 (1-2) · 4Móz 26:1 → 25:19;26:1 (1-2) · Hós 1:11 → 2:2;2:3 (1-2) · Jób 16:22 → 16:22;17:1 (1-2) · Jób 36:33 → 36:33;37:1 (1-2) · Neh 7:67–68 → 7:67 (2-1; az MT-ben nincs 7:68) · Préd 2:26 → 2:25;2:26 (1-2) · Péld 11:31 → 11:31;12:1 (1-2).

Kitöltött `igehely_mt`, mért eltérés: **Ézs 9:1–19** (`MT|tvtms`, a tábla `igehely_mt` = Károli-szám; mért: Károli 9:1 = MT 8:23, 9:2–19 = MT 9:1–18; az N-F85a igazolva); kétséges: Ézs 9:20 → 9:19;9:20, 4Móz 29:39 → 29:39;30:1, Hós 11:11 → 11:11;12:1.

A 93 `KEZI` azonossági sor (`kezi_identitas_javitas`; 4Móz 15, Jób 38, Préd 40) a mérés szerint Károli = KJV = MT, a render mégsem párosítja őket (`karoli_mt_vers` → None). A 2.2 hatókörén kívül esik, csak jelentés.

## 4. A #131 12 verse (brief 2.3)

`naplok/F146_131_versek.py`. Proveniencia: `scope=12 vers (#131 DBH-mérés, brief 2.3) | forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv | eszkoz=naplok/F146_131_versek.py | ts=2026-10-28T21:24Z`

| Károli-vers | tábla | mért MT (J) | ítélet | proveniencia |
|---|---|---|---|---|
| Ézs 7:11 | KJV | 7:11 (0,91) | a tábla helyes; a DBH-hiány valódi (a versen 11 DBH-hivatkozás, a keresett szóra nincs) | `scope=vers:Ézs 7:11 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 1Móz 4:10 | KJV | 4:10 (1,00) | helyes; a hiány valódi (12 hiv. a versen) | `scope=vers:1Móz 4:10 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 1Krón 20:6 | KJV | 20:6 (0,87) | helyes; a hiány valódi (22) | `scope=vers:1Krón 20:6 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 1Krón 20:8 | KJV | 20:8 (0,78) | helyes; a hiány valódi (14) | `scope=vers:1Krón 20:8 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 1Móz 14:19 | KJV | 14:19 (1,00) | helyes; a hiány valódi (13) | `scope=vers:1Móz 14:19 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 1Móz 14:20 | KJV | 14:20 (0,91) | helyes; a hiány valódi (12) | `scope=vers:1Móz 14:20 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| Jób 41:32 | KJV, üres MT | **41:24** (1,00) | **a tábla hibás** (Jób 41: KJV ≠ MT; a 2.2 felmérésben is); a mért versen 6 DBH-hiv. | `scope=vers:Jób 41:32 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| Préd 9:12 | KEZI, KJV 9:10, üres MT | **9:10** (1,00) | **az MT hiányzik** (Károli ≠ KJV = MT); 18 DBH-hiv. | `scope=vers:Préd 9:12 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| 4Móz 13:34 | KEZI, KJV 13:33, üres MT | **13:33** (0,83) | **az MT hiányzik**; 22 DBH-hiv. | `scope=vers:4Móz 13:34 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| Jób 38:7 | KEZI, KJV 38:7, üres MT | 38:7 (1,00) | Károli = KJV = MT, a `KEZI` osztály miatt a render nem párosít; 10 DBH-hiv. | `scope=vers:Jób 38:7 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| Jób 38:16 | ugyanígy | 38:16 (1,00) | ugyanígy; 10 | `scope=vers:Jób 38:16 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |
| Jób 38:30 | ugyanígy | 38:30 (1,00) | ugyanígy; 5 | `scope=vers:Jób 38:30 \| forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv \| eszkoz=naplok/F146_131_versek.py \| ts=2026-10-28T21:24Z` |

Az „üres eredmény nem negatív lelet”: az első hat versnél a DBH-hivatkozás a versen van, csak a keresett szóra nincs; ez a DBH lefedettségének ténye, nem a szó hiánya.

## 5. ⛔ 3.1 — a javítandó halmaz (DT-F146b: döntve, 2026-10-28, „Igen, csak a Jóel”)

Javaslat: **csak a Jóel 26 sora** (Károli 2:28–3:21 → MT 3:1–4:21, `KEZI` kitöltött `igehely_mt`-vel, a `versmegf_javitas` KEZI-szabályának Károli = KJV ≠ MT bővítésével), `forras` új értékkel (`macula_mt_f146`, a DT205 mintájára). A 982 − 26 = 956 többi igazolt eltérés, az Ézs 9, a 9 kétséges sor és a 93 `KEZI` azonossági sor külön tétel (N-F146a), mert ugyanaz az új kombináció ~830 sort érint, és a DT209 fogyasztói (`bsb_import`, `sqlite_epit`, `tsk_kulcs`) ellenőrzése nélkül nem vihető át. A Jóel a lexikonban csak az ISTENTISZT-001-et érinti (`adat/elofordulasok.tsv`: egyetlen Jóel 2:28–3:21-es sor, a Jóel 2:32).

## 6. A javítás (F146.2)

- Bemenet: a `naplok/F146_javitas_bemenet.py` a `konkordancia/Karoli_versmegfeleltetes_javitas.tsv`-be 26 sort ír (`KEZI`, `forras=macula_mt_f146`, soronkénti proveniencia, `elozo:` a régi értékkel) és 1 fejléc-jegyzetet. Őr: a meglévő 350 sor bájtra változatlan. Az újrafuttatás „változatlan”.
- Alkalmazó: `eszkozok/versmegf_javitas.py`. Második `forras`-érték: `macula_mt_f146`. A KEZI-szabály ennél a forrásnál a Károli = KJV ≠ MT esetet is megengedi; a kitöltött `igehely_mt` ≠ Károli-szám kötelező. Külön `# F146 javítás` fejléc-jegyzet készül. Az F117-jegyzet csak az F117-sorokat számolja (változatlanul 346). Egységteszt (`eszkozok/teszt_versmegf_javitas.py`): 23/23 OK; új tesztek: az F146-szabály két negatív és egy pozitív esete, a Jóel-sorok, a jegyzet.
- KK4 (`naplok/KAROLI_KK4_tabla_veglegesit.py`): két próbafutás a repón kívülre bájtazonos (sha256 `a16e9572…d2a3`). Élesítés előtt a `naplok/F146_tabla_osszevet.py` sorról sorra összevetette a régi táblával: 23 203 → 23 204 sor, csak a Jóel 26 adatsora változik (a várt értékkel), és egy fejléc-jegyzet kerül be; minden más sor bájtra azonos. Az éles kimenet azonos a próbával.
- Fogyasztó: `lexikon_general.karoli_mt_vers('Jóel 2:32')` → `Jóel 3:5` (előtte `Jóel 2:32`); a `Jóel 2:27` változatlan.
- DT209: az új sorok ugyanazt a `KEZI` + kitöltött `igehely_mt` kombinációt hordozzák, amelyen a `sqlite_epit` F117.5-őre már most is leáll (174 F117-sor). Új blokkolást nem okoznak; a `bsb_import` és a `sqlite_epit` javítása továbbra is az N-F117a hatóköre.
- A többi eltérés: N-F146a (`NYITOTT_FELADATOK.md`).
- További fogyasztó (ELLENOR_F146): az `eszkozok/f17/macula_kk.py` a kitöltött `igehely_mt`-t elsőbbséggel kezeli. A Macula-táblák következő újragenerálásakor a Jóel 2:28–3:21 sorainak `kk_mod`/`forras` értéke a mai `identitas`-ról `kk_mt`-re változhat. Ez a helyes irány: a Macula `karoli` oszlopa eddig a hibás azonosságot hordozta. Itt nem futtatom, mert a Macula-import nem tartozik e tétel hatókörébe.
- Az F146-jegyzet szövege rögzítetten a Jóelről szól. Ha az N-F146a további `macula_mt_f146` sort hoz, a `versmegf_javitas.py` jegyzetszövegét általánosítani kell.

## 7. Az ISTENTISZT-001 lap újragenerálása (F146.3, DT-F146a)

- A main beolvasztva (7347b950; a PR #500 N-F127a/N-F65b/N59/N60 lapírása is benne van), ütközés nélkül.
- Nulladiff (repón kívül, a scratchpadben): a 8 lexikonlap a mai generátorral, a #146 előtti táblával (0a245b4e) és az újjal. **7 lap bájtra azonos, csak az ISTENTISZT-001 tér el, abban is egyetlen sor: a Jóel 2:32.**
- Az élő lap a #146 előtti táblával generált változattól csak az időbélyegekben (16 sor) és a sorvégekben tér el, tartalmi elmaradása nincs.
- Éles írás: `general.py --cel lexikon --id ISTENTISZT-001` a repón kívülre (bájtra azonos a teljes futás lapjával), majd a lexikon/ alá másolva. A diff 17 sor: 16 időbélyeg és a Jóel 2:32.
- Eredmény: a Jóel 2:32 DBH-oszlopa a „nincs DBH-hivatkozás: keresett MT-vers: Jóel 2:32” helyett a H7121 két egységét (`006562001006000`, `006562001011000`) és a H8034 egységét (`007442001001000`) mutatja, mindegyiket `(MT: Jóel 3:5)` jelöléssel.
- **Új „fordításra vár”: 1** (előtte 0). A H7121 `006562001006000` definíciója a Jóel 3:5-ön most először kerül a lapra, és nincs magyar sora az `adat/forditasok.tsv`-ben. Lefordítása a #121 csatornájába tartozik (DT-F121 szójegyzék és kapuk); itt nem fordítok: N-F146b.

Proveniencia: `scope=lexikon/*_TUDOMANYOS.md (8 lap) | forras=eszkozok/general.py --cel lexikon (régi tábla: git show 0a245b4e, új tábla: F146.2) | ts=2026-10-29`

## 8. A main második beolvasztása (F146.5)

- A main újra beolvasztva (F38 11. adag, PR #501, `adat/forditasok.tsv`), ütközés nélkül.
- Az ISTENTISZT-001 a beolvasztott állapoton a repón kívülre generálva (`general.py --cel lexikon --id ISTENTISZT-001`): az élő laptól **csak az időbélyegekben** tér el, tartalmi különbség nincs. Az élő lapot ezért nem írom újra; a lap a mai main-adatokkal is naprakész.
- A PR #502 (a lap ⓘ-jeinek névelő-javítása) is az ISTENTISZT-001-et írja. Amelyik később kerül a main-re, annak az ágán kell újragenerálni a lapot (`general.py --cel lexikon --id ISTENTISZT-001`, majd összevetni). A két változás más-más sort érint: a #146 a Jóel 2:32 sorát, a #502 a ⓘ-lábjegyzeteket.

Proveniencia: `scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md | forras=eszkozok/general.py --cel lexikon --id ISTENTISZT-001 (a main 17bb2e06 beolvasztása után) | ts=2026-10-29`
