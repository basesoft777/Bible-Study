# BDB_FORDITAS — a 9. adag (sorrend 1389–1974): tábla-Δ és commitonkénti bontás (DT361, DT56)

*A #38 (BDB_FORDITAS) 9. adagának szakaszonkénti fordítása (4 szelet; prompt v5, `allapot=sonnet`, `modell=claude-sonnet-5-5`). Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 9. adag (1388–1974), az 1388. (H6297) az 8. adagban már kész, nem fordítva újra; így a fordított tartomány 1389–1974 (586 szócikk). Károli-lefedettség a kezdéskor: 100% (`BDB_FORDITAS_karoli_lefedettseg.py --tol 1389 --adagok 1`, DT56). Ág: `ccr-f38-adag9-1`, alap: `84b2eec6`.*

## 1. Tábla-Δ

| tábla | alap (`84b2eec6`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok, a 2 fejlécsor — kommentsor és oszlopfejléc — nélkül) | 8 067 | 11 049 | +2 982 | 2982 / 0 |
| `adat/forditasok.tsv` (fejléces sorszám, `wc -l`) | 8 069 | 11 051 | +2 982 | |
| `naplok/EMELES_munka.tsv` | — | — | +2 982 | 2982 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | — | +2 sor (H4549, H5953; az 1. szelet) | 2 / 0 |
| minden más `adat/` tábla | — | — | 0 | — |

A fenti +2 982 az F38.402–406 Δ-ja; az F38.407–408 javítókör (1/2) a Δ-t nem változtatja (a H0479 sz2 sora 1 sor módosul: `+1 / −1`, a H0479 `teljes` sor nem változik).

Törölt vagy módosított meglévő `forditasok.tsv`-sor az F38.402–406-ban nincs; a H6297 (8. adag) négy sora változatlan (a tévesen újrafordított sorokat az 1. szelet közben visszaállítottam a `git show HEAD:` tartalmára, a bejegyzett Δ 834 új sor, nem 838). `kezi` sorhoz nem nyúltam.

## 2. Commitonkénti bontás

| commit | szelet | szócikk | szakaszsor | új / módosított / törölt sor (`forditasok.tsv`) | forrás-karakter (b: `nezet`) |
|---|---|---|---|---|---|
| F38.402 | 1. (H6581–H7785, sorrend 1389–1540) | 152 | 834 | 834 / 0 / 0 | 149 458 |
| F38.403 | 2. (H7937–H3733, 1541–1710) | 170 | 864 | 864 / 0 / 0 | 151 465 |
| F38.404 | 3. (H4074–H7602, 1711–1908) | 198 | 999 | 999 / 0 / 0 | 149 695 |
| F38.405 | 4. (H7879–H5039, 1909–1974) | 66 | 285 | 285 / 0 / 0 | 47 350 |
| **össz.** | | **586** | **2 982** | **2 982 / 0 / 0** | **497 968** |

Karakterszám-módszer: (a) a `szakasz_bemenet.szakaszok()` `szoveg`-mezőinek összege; (b) a `nezet(szak)` hossza. Az (a) értékek: 148 776 / 150 771 / 148 894 / 47 131. A commitüzenetek a (b) értéket hordozzák (a 3. szelet első üzenetét ezzel egységesítettem, mielőtt bármit pusholtam volna).

## 3. Szeletenkénti Strong-tartomány

A szeletek a `BDB_FORDITAS_sorrend.tsv` sorrend-oszlopa szerint folytonosak; a határuk: 1. szelet H6581 … H7785; 2. H7937 … H3733; 3. H4074 … H7602; 4. H7879 … H5039. (A teljes Strong-lista a `git show <commit> --stat` szócikk-listájából és a `szakasz_beir` kimenetéből — 999 sor, 198 Strong — reprodukálható; a 3. szelet beírt Strong-jai: H4074, H4125, … H7602, ld. a commit szakasz-kimenetét.)

## 4. 17_bdb_javitas (DT55, #67 kapu)

| Strong | forrásbeli hivatkozás | helyes | rögzített alak | kapu |
|---|---|---|---|---|
| H5377 (sorrend 1728) | `Obad 3:7` | `Abd 1:7` | `Abd 1:7 [BDB: Abd 3:7]` | 17_bdb_javitas RENDBEN |
| H0479 (sorrend 1831) | `Ezra 16:8b` | `Ezsd 6:8` | `Ezsd 6:8b [BDB: Ezsd 16:8b]` (F38.408; előtte, F38.404–406: `Ezsd 6:8 [BDB: Ezsd 16:8]b`) | 17_bdb_javitas RENDBEN (felülbírálás nélkül) |

A H0479 esetében a forrás `16:8b` betűjelét eredetileg a jelölés után kellett írni (`… [BDB: Ezsd 16:8]b`), mert a kapu a versfél-betűt nem ismerte (ELLENOR_F38_adag9 1., DT-F38v). A javítókörben (DT-F38v (c), felhasználói döntés) a 17. kapu kalibrációt kapott (F38.407): az Y- és X-minta a–d versfél-betűt is fogad, és a forrás betűjével azonos betűt vár (`Y<betű> [BDB: X<betű>]`); így a H0479 sz2 az F38.408-ban a forrás helyén álló `b`-vel, felülbírálás nélkül rögzült. `BDB_JAVITAS_KAPU_regresszio.py`: 10 915 sor, 0 SÉRTÉS. Más (javítótáblán kívüli) forrásbeli hivatkozást nem javítottam: a „Songs", „Obadiah 3/7" és hasonló torzult alakokat hűen vettem át (az „Obadiah 3/7" → „Abd 3/7").

## 5. Kapu-felülbírálások (DT361)

| Strong / szakasz | kapu | forrásidézet | indok |
|---|---|---|---|
| H3724 — mind a 8 `forditas_hu` sor (sz1–sz8; a `megjegyzes` Strong-szintű) | 8_idezojel | `El „enna (√ dubious; Late Hebrew …` | Az sz6-ban a `„` a forrásban OCR-maradvány (nyitó idézőjel pár nélkül); hűen megtartva, nem cseréltem és nem töröltem a kapu kedvéért. A felülbírálás a rögzítő eszköz Strong-szintű `--kapu-felulir` kapcsolója miatt a Strong mind a 8 sorának `megjegyzes`-ében szerepel, de a tartalmi ok csak az sz6-ra vonatkozik. |
| H5015 (mind a 8 szakaszsor `megjegyzes`-e) | 5_terminologia | `Jen^Kosmol. pass. Tiele^Ass. u. Babylonian Geach.` | A `pass.` itt a *passim* idézési rövidítése, nem „passive"; a kapu a KÖT-kulcs (`pass.` → `szenvedő alakban`) miatt „szenvedő alakban"-t várt volna. Hűen: `passim`. A felülbírálás Strong-szintű (a rögzítő eszköz csak így tudja). |
| H0479 | — (nincs felülbírálás) | `Ezra 16:8b` | Az F38.404–406-ban a `16:8b` betűje a jelölés mögé került; a javítókörben a kapu kalibrációja (F38.407) tette lehetővé a forrás szerinti alakot, felülbírálás nélkül. A DT-F38v (b) szerinti `--kapu-felulir 17_bdb_javitas` felülbírálás sem kellett, mert a kalibráció a kérdést megoldotta. |

A kapuk egyéb elakadásai (9_tagolas, 4_formazas, 1_gorog_heber, 5_terminologia, 11_konyvek) mind **valódi** megoldással, tartalmi változtatás nélkül, az egyszeri újrapróbálkozásban zárultak (pl. szóköz a forrásban nem látható vezérlőkarakter helyén, egy többlet nyitózárójel törlése, `Neh 11:17` könyvjelölés).

## 6. Javítókör 1/2 (ELLENOR_F38_adag9)

| commit | tartalom |
|---|---|
| F38.407 | `eszkozok/forditas_kapuk.py`: `BDB_JELOLES`, `BDB_JELOLES_YX` és a 17. kapu versfél-betű (a–d) kezelése; `eszkozok/teszt_forditas_kapuk.py`: új tesztek (RENDBEN-eset, eltérő/hiányzó/utánírt betű SÉRTÉS, betű nélküli eset változatlan, `bdb_jeloles_vissza`, 2./11./17. kapu együtt) |
| F38.408 | H0479 sz2 újrarögzítve `Ezsd 6:8b [BDB: Ezsd 16:8b]` alakkal (eszközlánc, felülbírálás nélkül); `BDB_JAVITAS_KAPU_naplo.md` újragenerálva |
| F38.409 | ez a napló és a brief `ir`/`kovetkezo` mezője |

## 7. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (minden szelet után és a végén).
- `python eszkozok/teszt_forditas_kapuk.py`: OK (exit 0).
- `python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py`: OK (exit 0).

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ 84b2eec6 és @ HEAD; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`, `git diff --numstat`, `szakasz_bemenet` | ts=2026-10-28)*
