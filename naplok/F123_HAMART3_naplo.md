# F123 — a HAMART-001 új cikkének menetnaplója (U2–U4, U3b, U7)

*#123 MIGRACIO2 v2 · ág: `claude/sweet-goldwasser-00aa45` (a `c6aa7b0c` main-ről) · 2026-11-05 · sablon: `9_` v1 (DT585)*

## 0. Modell-ellenőrzés és indulás

A kért modell (a brief `modell` mezője): `opus`; a session tényleges modellje: `claude-opus-5-5`. **Egyezik** (F123.HAMART3.1). Az U1 a `hamart-u1` sessionben futott (PR #609): a gépi lépések az X.A-hoz képest nem változtak (`naplok/F123_U1_HAMART-001_valtozas.md`).

## U2. Döntések átvétele és a nyitott jelöltek elbírálása (F123.HAMART3.1–3)

**A 23 vers (az U1 vizsgálatlan különbsége).** Az X.A 1 256 új verséből 23 a teljesség-mérésben nem ELTÉRÉS, hanem `J:nyitva`: pontosan a DT542 szerint az X.A után beírt jelölt-sorok versei (Hós 10:8 + a 14 lánc-hely 22 verse). 1 256 − 23 = 1 233; fordított irányú eltérés 0 (`naplok/F123_HAMART3_23vers.py`, `.tsv`).

**Érvényes, nem kerül újra elő:** a `jeloltek.tsv` HAMART-001-sorainak régi döntései, DT542–DT544, DT593 (a H7451 és a H7043 nem a lánc szava).

**A szűretlen Strong-blokkok kézi átnézése (DT543 (b))** gépi mintakereséssel (`naplok/F123_HAMART3_formula.py`, `.tsv`): az 582 versből 42 a négy mintára (F1 adamá + pānîm + pusztító ige; F2 sáchat + föld; F3 chámász + erec; F4 chattát + föld), mind a 42 elolvasva a Károli-szöveggel.

**A javaslat** (a teljes szöveg a session-csoport jegyzetmappájában: `HAMART-001_U2_javaslat.md`) és **a döntés — DT683:** az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket és hozza is meg« (2026-11-03), 2026-11-05: „A–E: mehet, mind, ahogy a javaslatban áll.”

| Tétel | Döntés |
|---|---|
| (A) a 8 régi `nyitva` (DT544) | mind elutasítva (kiáltó vér; szövetségi bálványimádás; a 2Pét 3:10, 12 tűz-ítélete; erkölcsi jellemzés) |
| (B) a DT542 27 jelöltje | Hós 10:8, Ez 12:19, Mal 3:11 beépítve; a többi elutasítva |
| (C) a 4 Strong-blokk (582 vers) | elutasítva a régi napló lexémánkénti okaival; új beépítés: 1Móz 7:4, 7:23, Sof 1:2-3, Jer 51:25 |
| (D) a Károli- és a szótár-blokkok | elutasítva; a Jel 22:3 beépítve, „tematikus, nem lexikai” jelöléssel |
| (E) DT593 következménye, szótári gerinc | 1Móz 6:5 → `tematikus:1Móz 6:5`; 1Móz 8:21 → H0127; a gerinc a BDB/Thayer idézőhelye szerint; `SZOTARI_GERINC` → `aktiv` |

Kikötés (végrehajtva): az Ez 12:19 és a Sof 1:2-3 indoklása kimondja a különbséget az elutasított „föld színéről” helyektől. A „föld színéről” / Ádám–Izrael kiűzetés-párhuzam: **N-F123ha** (a 2. kiadásra). Hat új elutasítási ok (`adat/elutasitasi_okok.tsv`); a 105 elutasítás mind besorolható. Utójavítás (F123.HAMART3.3): öt beépített sor indoklásának idézete a Károli szó szerinti szövegére.

## U3. A próza (F123.HAMART3.5)

- `motivumok/HAMART-001.md` nulláról, egy kézből (claude-opus-5-5), a `9_` v1-re; az alapanyag az U1 kivonata (`naplok/F123_alapanyag_HAMART-001.md`), célzott olvasással; mondat a régi szövegből nem költözött át. A régi tanulmány, napló, forrásréteg, törzscikk és 1/a próza: `archivum/HAMART-001/` (ARCHÍV fejléc); a brief `olvas`/`ir` mezője az archív útvonalra mutat; az E28-listán a HAMART-001.
- Az X.T: a régi tanulmány visszaírt leleteinek függő beírási teendője (a régi 307–316. sor) az archiválással megszűnt; a motívumforrás 【NAPLO】 sora rögzíti.
- Az 1/a 60 helye kerek mondat + „Funkció:” sor (`proza_1a.py`: 60/60 arany; előtte 52-ből 43 kerek, 0 Funkció-sor). Minden „…” idézet és `karoli_szo` a Károli-vers szó szerinti része (`naplok/F123_HAMART3_u3_adat.py` saját ellenőrzése, és az olvasói kapu IDEZET-osztálya).
- `adat/motivumok.tsv`: a negatív kritérium olvasói nyelven, szó szerint ellenőrizhető, a TR-mércével és a név szerinti tematikus kivételekkel; a fölérendelt fogalom olvasói nyelven.
- A `9_` v1 öt szabálya: (1) hat saját elutasítási ok; (2) lexémánként egy blokk-sor (a meglévő 77 blokk-sor, U1); (3) TR-mérce — a tíz újszövetségi helyen a motívum szava a TR-ben és a kritikai kiadásokban ugyanott áll (`naplok/F123_HAMART3_tr_kritikai.py`, `.tsv`; a Jel 19:2 ἔφθειρεν a bizánci szövegben hiányzik, a TR-ben áll); (4) Septuaginta-többlet a motívumban nem előfordulás (a LXX csak tényként, a görög szavaknál); (5) idézetek jelöléssel.
- Az azonosság-hordozó `strukturális`, ezért a Kivonat kimondja, hogy a lista keresési módszer eredménye.
- A 4. (szakirodalom) és az 5.T (tanítói egyezés) szakasz `INAKTÍV` (ellenőrzött lekérdezés nem futott; a régi Derek Prince-hivatkozás archívumban).
- Kiejtés: a jóváhagyott alak (`adat/kiejtes_kivetelek.tsv`): árar, adámá (`naplok/F123_HAMART3_kiejtes.py`; a `jeloltek.tsv` régi indoklásai az elutasítási minták miatt változatlanok).

**A szótári gerinc táblái (bontás):** `adat/szotar_szakasz_cimke.tsv` +21 = BDB 13 (H0127 -/1/-, -/3/-, -/4/-; H0779 Qal; H6975 -/1/-; H2403 -/1/-; H7843 Niph'al, Pi'el/1, Hiph'il/1, Hiph'il/2; H7451 BDB8032 -/10/c; H0423 -/3/-; H0056 Qal) + Thayer 8 (G5356 -/1/-; G1944, G2671, G5351, G2652, G2626 fej; G1311 -/1/-; G1261 -/1/-); `adat/lexikon_hivatkozasok.tsv` +21: ugyanezek kulcssorai (a szakasz angol szövegével). A Jer 51:25 `Hif'íl 1` besorolása a menet saját ítélete: a BDB a verset nem idézi.

## U3b. A 12. szótári blokk (Nave) — DT595

A jelöltlista a mai 60 soron újraszámolva (34 téma; az U1 listája 52 soron 31-et adott). **Döntés (DT684, az orkesztrátor döntése a felhasználó felhatalmazásával, 2026-11-05: „U3b Nave: mehet, ahogy javasoltad.”):** 7 `kivalasztott` (CURSE, FALL OF MAN, GROUND, FLOOD, ANTEDILUVIANS, THISTLE, BANISHMENT), 2 `tiltott` (SIN, DEPRAVITY OF MAN: a bűn általában felé hígítana), 25 `kizart` (személy, könyv, mellékes vagy túl tág téma), indokkal (`naplok/F123_HAMART3_nave.py`). A 23 magyar név Sonnet-tervezet (claude-sonnet-5-5), a `glossza_lexikon_forditas.py nave` kapui után; három a lap szóhasználatára simítva (`naplok/F123_HAMART3_nave_hu.py`). A lap 12. blokkja: 7 téma, magyarul.

## Fordítás (a cikk menetében, Sonnettel; DT587 mintája)

A lap Thayer/BDB-szövegéből fordítatlan volt: **Thayer G1261** (διαλογισμός) és **G2626** (κατακλύζω). Menet (`naplok/F123_HAMART3_forditas.py`): a `thayer_api_koteg` kéréseinek user-szövege fájlba (`terv`/`kuldendo_prompt`, adag 9002 `hamart1`); két `general-purpose` subagent, `model: sonnet` (tényleges modell: claude-sonnet-5-5) a kérés szövegét fájlból olvasta és a választ fájlba írta; `kapuz`: mindkettő kész az 1. próbán; `rogzit` a munkatábla repón kívüli másolatán (a `naplok/F132_*` nem változott); `forditas.beir(…, 'sonnet')`: 6 sor az `adat/forditasok.tsv`-ben. Mérés nem futott (a felhasználó szabálya). A lapon maradt „fordításra vár” (13): UBS-jelentések és TBESG-megfelelők, nem Thayer/BDB.

## U4. Kapuk (F123.HAMART3.4–8)

- `ellenoriz.py`: SÉRTÉS 0; 17–20. RENDBEN (a szótári gerinc aktív); 24. RENDBEN; 25.: a HAMART-001 60/60 arany; 28–29. és 33. RENDBEN.
- Olvasói kapu: **0 BUKÁS** (22 figyelmeztetés). Előtte 17 BUKÁS: 11 IDEZET (10 a kapu hibája: a tartomány-sor második versét nem vetette össze; 1 a Jer 51:25 prózájában a Jel 19:2-ből vett idézet — átírva), 2 ATIRAS (árar, adámá), 3 KONYV (4Makk, 2Pe, Siral), 1 ZAROJEL (a BDB-gyök).
- Generátor- és kapujavítás (F123.HAMART3.4), mind a legkisebb javítással, nulla-diffel (nyolc lapon 0 eltérő sor): az olvasói kapu tartomány-idézete és 3–4Makk; a generátor „Siral” → „JSir” és a BDB-gyök zárójele. A nyílt mag exportjában a blokk-kulcs „|”-t is tartalmazhat (`nyilt_mag_export.py` `BLOKK_RX`; a HAMART-001 Károli-blokkjai nélküle nem bontódtak ki: 62 BUKÁS → 0; a többi motívum exportsora nem változott).
- Lap: `general.py --cel lexikon --id HAMART-001 --ir` (128 495 → 449 576 bájt; a legnagyobb rész az 1/b kizárt helyei — 271 elutasítás — és a 21 szócikkes szótári háttér); a napló-, index- és nyitott-nézet újragenerálva (E28).
- C-z (`proza_lefedettseg.py`), helyi CI (`futtat.py`), `feladatok.py ellenoriz`: a PR-ban.

## U7. Nyílt mag

`python eszkozok/nyilt_mag_export.py`, kapu: `nyilt_mag_kapu.py` **0 BUKÁS** (9 figyelmeztetés: KJV-versszámozási megjegyzések az indoklásokban). A brief U7 lépése: ez minden további cikk kiadásának lépése; a Zenodo új változata a felhasználó lépése (a felhasználó döntése az orkesztrátor továbbításában, 2026-11-05).

## Ami a felhasználóra és az orkesztrátorra vár

- ~~A Nave-döntés jóváhagyása (U3b)~~ — megvan: DT684.
- A lap vizuális átnézése (U6), a felhasználóé; utána egy javítókör, 1. kiadás.
- A független ellenőrzés (`fuggetlen-ellenor`) a PR diffjén.

## U4 javítókör (F123.HAMART3.13)

A független ellenőr 12 ELTÉRÉS-e és a javítás tételenként: `naplok/ELLENOR_F123_HAMART-001.md` („A javítókör”). Eszköz: `naplok/F123_HAMART3_javitokor.py`. Az E19 hét hibájából hat kulcsolási hiba volt (a szócikk-azonosító nullázása), egy valódi fordításhiány (Thayer G2652, Sonnettel lefordítva). A CI E2/E4/E19 javítása: `eszkozok/ellenorzes/szabalyok.py`.
