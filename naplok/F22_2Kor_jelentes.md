# F22_2Kor_jelentes.md — Károli–Strong párosítás: 2Kor (csak Sonnet, Message Batches API) és a 22.9 B csomag zárása

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Kor`, `egyesit.py --konyv 2Kor` és `--ellenoriz`, `f22_elemzes.py --konyv 2Kor`, `nem_tr_lista.py`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Kor-soraiból: `futas = api_termeles/high/2Kor`, `cimke = 2kor`). Ág: `claude/f22-2kor`. Módszer: D45 és a brief 22.9 szerint: `prompt_v3` változatlanul, csak Sonnet (`claude-sonnet-5-5`), Message Batches API, `effort=high`, 10 verses kötegek. Modell-ellenőrzés: a session tényleges modellje `claude-sonnet-5-5`, egyezik a brief `modell: sonnet` mezőjével (az első kísérletnél a session `claude-opus-5-5` volt, ott semmi munka nem történt).*

## 1. Menet

- **Visszatartás oka:** a 2Kor a B csomagból azért maradt ki, mert a `TAGNT_kivonat.tsv` zárójeles sorai hiányoztak (N-F22c); az F90 pótolta őket, a mintát az F90 utáni kivonatból építettük újra (`naplok/F22_versbeosztas.md`, 2Kor: 256 Károli-vers, 256 eredeti vers, 13 fejezet, eltolt 0, K-hiány 0, E-hiány 0; a 8. fejezet GYENGE jelzése hosszkorrelációs jelzés, nem eltolódás).
- **Versbeosztás-jóváhagyás (2026.10.19):** a felhasználó közvetlen ellenőrzése alapján (`naplok/F22_versbeosztas_jovahagyas.md`, chat: „mehet”); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Kor'`).
- **Minta:** `f22/minta_2Kor.tsv`, 256 vers a modellhez, 26 köteg.
- **Batch** (`f22/api_termeles/batchek.tsv`): `msgbatch_01B2fhTDU7FZsH4GrHsvhQGr`, 26 kérés, beküldve 2026-10-19T08:25:58+00:00; mind a 26 sikeres, a befejezés kb. 2 óra 20 perc után volt látható (a 22.8-ban mért 2 perc–2 óra tartományon kívül; a várakozás nem ok a párhuzamosításra, D15, DT60).
- **Futásnapló** (2Kor: 26 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12 = 84f12ca7aafb` (a `prompt_v3` változatlan).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 256 / 256 |
| hívás | 26 (javító kör nem kellett) |
| kapuhiba 1. próbára | 0/256 (0,0%); végleges 0/256 |
| link (`parok_2Kor.tsv`) | 4352, mind `alacsony`, forrás `S` |
| szósor (`szavak_2Kor.tsv`) | 9064 = 4517 Károli + 4547 eredeti |
| Károli-oldal: párosítva / betoldás / fordítatlan | 3748 / 769 / 0 |
| eredeti oldal: párosítva / betoldás / fordítatlan | 3902 / 0 / 645 |
| `kezi` / átnézési sor | 0 / 0 (`naplok/F22_2Kor_atnezes.tsv` fejléc-only) |
| költség | 1.3600 USD (0.00531 USD/vers; bemenet 250 872, kimenet 221 817 token) |

Az `egyesit.py --konyv 2Kor --ellenoriz`: „rendben”. A szósorok száma a Károli- és az eredeti tokenek összegével egyezik. Mivel csak a Sonnet futott, nincs `magas` bizonyosság (két modell egyezése hiányzik): minden link `alacsony`, mint a 22.9 A és B csomagban.

**Régi arany:** a 2Kor-ban nincs régi-arany hármas (`f22_elemzes.py`: 0/0).

**A zárójeles csoportok (N-F22c) a 2Kor-ban** (`naplok/F22_TAGNT_zarojeles_sorok.md`): 2Kor 1:6, 8:14, 10:5, 13:13 érintett; a kivonat az F90 után teljes, a versek ezért `kezi` kényszer nélkül mentek a modellhez és kaptak linkeket (1:6: 35, 8:14: 11, 10:5: 17, 13:13: 15 pár). A 2Kor 13:13 33 eredeti tokenjéből a #22–#33 a Textus Receptus utóirata („πρὸς Κορινθίους δευτέρᾳ ἐγράφη …”), amely a Károliban nincs meg; DT120 szerint a vershez tartozik, ezért helyesen `forditatlan`.

## 3. A `[nem TR]` tokenek: 103, ebből 5 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve, `nem_tr_lista.py`: 45 sor, 19 ÚSZ-könyv).

| vers | er | alak | Strong | Károli-szó (partner) |
|---|---|---|---|---|
| 2Kor 5:12 | 22 | μὴ | G3361 | nem |
| 2Kor 5:12 | 23 | ἐν | G1722 | szívből |
| 2Kor 10:13 | 3 | οὐκ | G3756 | nem |
| 2Kor 12:3 | 10 | χωρὶς | G5565 | kívül |
| 2Kor 12:9 | 15 | τελεῖται. | G5055 | végeztetik el |


## 4. Költség, keret, újravetítés

- A 2Kor költsége **1.3600 USD**; az N-F22c újrapárosítás 15 hívása **0.1891 USD** (`naplok/F22_N-F22c_ujraparositas.md`). A futó összeg a menet elején 94.5049 USD, most **96.0540 USD**; a plafon (`api_koteg.PLAFON_USD`) 104.36 USD, a **maradék 8.31 USD**.
- Mért egységár a 22.8, az A, a B és a 2Kor együtt: **0.005238 USD/vers** ((0.005226 × 1638 + 1.36) / 1894 vers; a B-jelentés egységárából és a 2Kor mért költségéből).

| hátralevő | vers | vetítés | ×1,2 tartalékkal |
|---|---|---|---|
| C (Róm, 1Kor, Jel) | 1272 | 6.66 USD | 7.99 USD |
| Róm + 1Kor | 867 | 4.54 USD | 5.45 USD |

- **A C egészében belefér** a maradékba a ×1,2 tartalékkal (7.99 USD ≤ 8.31 USD, a különbség 0.31 USD). A „rossz eset” (0,0066 USD/vers × 1272 = 8.40 USD) viszont **a maradék fölött van**.
- **A futtató őr akadályt jelenthet a C-nél.** Az `api_koteg.bekuld` a beküldés előtt a *felső* becslést (minden kérés kimenete a `max_tokens`-ig, 0,16 USD/kérés) a plafonhoz méri: a 2Kor 26 kérésére ez 4.41 USD volt, a tényleges 1.36 USD. A C három könyve kb. 44 + 44 + 41 kérés, tehát a felső becslés könyvenként kb. 7 USD; a Róm után a futó összeg kb. 98.3 USD, ehhez az 1Kor felső becslése (kb. 7.1 USD) már a 104.36 USD fölé vinne, pedig a tényleges költség belefér. Ezért a C indítása előtt döntés kell az őr kezeléséről (DT-F22h helyőrző a `DONTESEK.md`-ben); a C nem része ennek a menetnek.

## 5. Az N-F22c újrapárosítás és a következő lépés

Az N-F22c 21 versének újrapárosítása és a 15 vers kényszerének kivezetése a 11 érintett könyvben: `naplok/F22_N-F22c_ujraparositas.md` 4–6. szakasz. **Következő lépés: a C csomag jóváhagyása** (külön, a felhasználótól; a DT-F22h eldöntése után).
