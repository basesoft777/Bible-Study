# ELLENOR_F22_2Moz.md

*Az ellenőri jelentés a `fuggetlen-ellenor` ügynök kimenete (1. kör), változatlan tartalommal; az ügynök szerepköre csak olvasó volt (nem futtathatott szkriptet, és a fájlt sem írhatta), ezért a fájlt az orkesztrátor mentette. A „Kezelés” szakasz az orkesztrátoré.*

**Brief:** F22_KAROLI_STRONG_BRIEF.md (2Móz menet, könyv-paraméter cserével) · **Tartomány:** `origin/main...HEAD` (91e44bc...2331358; az ág saját F22.* commitjai 68bbece–21cc6e8). A 2331358 merge-commit második szülője az origin/main, és a `git diff origin/main 2331358^2` üres, vagyis a merge csak main-tartalmat hoz.

**Összesítés: ELTÉRÉS: 8 tétel** (súlyossági sorrendben a lap alján).

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| K1 (minden token pontosan egyszer) | NEM ELLENŐRIZHETŐ (részben OK) | `adat/karoli_strong/szavak_2Moz.tsv` | Az `egyesit.py --ellenoriz` futtatása a szerepkörön kívül esik. Részellenőrzés: `git diff --numstat` → parok +23968, szavak +49398 sor (= 23966 / 49396 adatsor + 2 fejléc). A Károli_1908 `^2Móz \d+:\d+\t` találata 1213; a minta_2Moz 1212 sor + fejléc, a 35:36 nincs benne (0 találat). A szavak-táblában a `^2Móz 35:36\t` 36 sor `fuggoben/kezi`, a 2Móz 36:38 22 er-sor `fuggoben/kezi` (49377–49398. sor). |
| K2 (strong a TAHOT-ból) | NEM ELLENŐRIZHETŐ (szúrópróba OK) | `parok_2Moz.tsv:21391` | Gépi ellenőrzést nem futtathattam. Szúrópróba: a parok-tábla 2Móz 36:1, er 3 = בְצַלְאֵל H1212 sora egyezik a TAHOT 2Móz 36:1 3. tokenjével (TAHOT_kivonat.tsv:52232, H1212). |
| K3 (prompt-hash) | OK | `f22/futasnaplo.tsv` | Grep: `\tc/2Moz\t.*\t84f12ca7aafb\t` → 171 / 171 sor ugyanazzal a hash-sel. A `git diff --name-only origin/main...HEAD -- f21p/` üres, a prompt nem változott. |
| K4 (jelentés tartalma) | OK | `naplok/F22_2Moz_jelentes.md:22-47,53-135` | A kapuhiba, az arányok, a régi arany, a C költsége és a /usage szakasz mind megvan. |
| K5 / D8 (C-költség a plafon alatt) | OK | `f22/futasnaplo.tsv:388` | Az utolsó c/2Moz sor futo_osszeg értéke 4.123674, az utolsó c/1Moz soré 2.271971 (217. sor). A különbség 1.851703, a jelentés 1.851702-t ír (kerekítés). Ez a 2,69 USD-s könyvplafon alatt van: 1212 × 2,27/1533 × 1,5 = 2,692. A 4,00 USD-s eredeti plafont a D8 felváltotta. |
| K6 / D6 (nincs zárt licencű adat) | OK (a látható fájlkörre) | — | A `git diff --name-status` szerint nincs új fájl a zárt forrásból, és a `zart_osszevet.py` nem változott. A táblák proveniencia-sora csak a jsonl-, TAHOT- és Karoli-forrást nevezi meg (parok_2Moz.tsv:1). |
| K7 (bájtra azonos újraépítés) | NEM ELLENŐRIZHETŐ | — | Az `egyesit.py` futtatása a szerepkörön kívül esik. |
| K8 (CI) | ELTÉRÉS (feltételes) | `.github/workflows/f22_parositas.yml:0` | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only origin/main...HEAD) --diff-alap origin/main --diff-fej HEAD` → kilépési kód 1, **E16 HIBA**: „a PR erinti az ellenorzot (...f22_parositas.yml), de a cim nem "[ELLENŐRZŐ]" elotagu”. Ugyanez `--esemeny push`-sal: kilépési kód 0, E9 JELENTES 2 (SEMA.md:237-238, a diffhez nem kötődik). A PR-en a CI piros lesz, ha a cím nem `[ELLENŐRZŐ]` előtaggal kezdődik. |
| K9 (bejegyzés) | OK | `adat/datasetek.tsv:89-96`, `adat/SEMA.md:917` | `git diff -- adat/datasetek.tsv adat/SEMA.md`: 8 sort cserélt (nettó 0); a 2Móz-fájlok és a 2Móz-jelentés be vannak jegyezve. A `fuggoben` állapot szerepel a sémában (SEMA.md:938). |
| D1, D2, D5, D7 | OK | brief | Könyvenkénti menet; S + C; a próbaszakasz 14 kötege (futasnaplo.tsv:237: 2.493346 − 2.271971 = 0.221375 USD, × 1213/140 = 1,918); a prompt változatlan. |
| D3 (eltérésnél a Sonnet, `alacsony`) | OK | `parok_2Moz.tsv` | Grep: `\talacsony\tS$` → 1262, `\tC$` → 0, `\tmagas\t` → 22704; összesen 23966. |
| D4 (30%-os keretszabály) | NEM ELLENŐRIZHETŐ | `jelentes.md:12-18` | A /usage értékei nincsenek a repóban. A vetítés számtana (1 pont × 1213/140 ≈ 9) stimmel. |
| D8 kód: a régi F21-viselkedés | OK (kódolvasás) | `eszkozok/karoli_strong/futtat.py:825-835` | Ha `plafon_futas` None, az `elif eddig + becs > ctx.plafon` ág változatlan. A `naplo_osszeg(futas=None)` a régi összegzés. Az `futtat.py --onteszt`-et nem futtattam. |
| D8 önteszt | ELTÉRÉS | `eszkozok/karoli_strong/f22_c_futtat.py:172-224` | Az önteszt nem fedi az új logikát: nincs teszt a `plafon_usd=auto` értelmezésére, a `konyv_plafon` képletére (minimum 1,00), a más könyv sorait kizáró könyvenkénti szűrésre, sem a 60 USD-s összesített korlátra. A 0.0001-es plafonteszt bármelyik ágon átmenne. |
| (1) Az 1Móz táblák változatlanok | OK (a commitolt fájlokra) | — | A `git diff --stat origin/main...HEAD -- 'adat/karoli_strong/*1Moz*'` üres. Hatókör: ez a commitolt fájlokra igaz. Azt nem jelenti, hogy az új `egyesit.py` újrafuttatva bájtra ugyanazt adná; ez NEM ELLENŐRIZHETŐ. A nincs_parja listában nincs 1Móz-sor (grep `Móz` → csak 2Móz és 4Móz), így a kód szerint az új ágak az 1Mózre üresek. |
| (3) Kulcs-grep | OK | — | Grep a teljes repón: `sk-or-v1-[A-Za-z0-9]{8,}\|sk-ant-[A-Za-z0-9]{8,}` → nincs találat. Az `OPENROUTER_API_KEY` csak a workflow 70. sorában, `secrets`-ből. |
| (4) Jelentés számai: 4.1 | OK (táblából visszaszámolva) | `jelentes.md:55,96` | Grep-számok: parok magas 22704, szavak magas 43767, alacsony 5571, kezi 58 (összesen 49396). 36. fejezet: parok 171, ebből magas 73; szavak 1420, ebből magas 435, kezi 22. 35. fejezet szavak: 1313. Mind egyezik a jelentéssel. |
| (4) 4.2 régi arany (2Móz n=6, 5/6) | OK (kézi visszaszámolás) | `Karoli_Strong_kivonat.tsv:218-258` | Grep `Exo` → 6 sor. Ötnél a parok-tábla ugyanazt a Strongot adja (19:6 H3548/H4467, 33:19 és 34:5 H7121+H8034, 15:8 H8415). A 15:5 „a mélységbe” → H9003+H4688, az arany H8415, ez az 1 eltérés. |
| (4) f22_statisztika és 4.3 eltérés-típusok; 5.4 1Móz-számok | NEM ELLENŐRIZHETŐ | `jelentes.md:25-40,112-135,187` | Szkriptfuttatás nélkül nem igazolható. A naplóból: c/2Moz 171 hívás, ebből `kapu` 50, `parse` 3 (grep). Ez egyezik a 9. sorral. |
| (4) eredeti_nelkuli_lista | OK | `naplok/F22_nincs_parja_versek.tsv:118-119` | Az ÖSSZESEN-sorok (61 vers / 795 token, 30 vers / 567 token) egyeznek a jelentés 176-177. sorával. |
| (5) 5.1: 58 kezi token, a 36. fejezet 42,7%-a | OK (a számok) | `jelentes.md:141` | Lásd a fenti grep-számokat (36 + 22 = 58; 73/171 = 42,7%). |
| (5) 5.1 / adatminőség: a 36. fejezet eltolódása a táblában | **ELTÉRÉS** | `parok_2Moz.tsv:21391-21426` | Grep a Karoli_1908 és a TAHOT 35:36–36:2 versein. A Károli 35:36 („Azért Bésaléel és Aholiáb…”) a TAHOT 36:1-gyel egyezik (TAHOT_kivonat.tsv:52230-52241). A Károli 36:n tehát a héber 36:n+1, és a 36:1–37 mind a 37 verse nem megfelelő versekkel párosodott. Ennek ellenére a tábla 73 linket `magas`-nak jelöl. Példa: 21408. sor, 36:1 „járuljon” ↔ דַעַת H3045 magas; 21414. sor, 36:2 „Mózestől” ↔ a héber 36:2 Mózese, ami a Károli 36:1-hez tartozik. A jelentés ezt „gyenge párosításnak” nevezi és N-F22 nyitottként kezeli. A kanonikus táblában viszont semmi nem jelöli, és a `magas` itt nem azt jelenti, amit a D3/pilot mögé tesz (98,7%). |
| A1 (memória vs. lekérdezés) | **ELTÉRÉS** | `eszkozok/karoli_strong/sonnet_koteg.py` (eredeti_nelkuli_versek docstring) | A docstring szerint „a Károli-számozás kettébontja a héber 35:35-öt”. Ezt az adat cáfolja: a Károli 35:36 a héber 36:1 (lásd az előző sort). Ez lekérdezés nélküli, téves értelmezés a kódban. |
| (5.3) A páratlan versek listájának hatóköre | **ELTÉRÉS** | `naplok/F22_nincs_parja_versek.tsv:81`, `jelentes.md:149` | A lista csak a kulcs-végpontokat találja meg, a fejezeten belüli eltolódást nem. Példa a következő könyvre: a TAHOT 4Móz 30:1 „וַיֹּאמֶר מֹשֶׁה” (TAHOT_kivonat.tsv:439711), a Károli 4Móz 30:1 „És szóla Mózes … törzsek fejeinek” (Karoli_1908.tsv:4650), vagyis az egész 4Móz 30 eltolt. A listán csak a 30:17 szerepel. Az 5.3 szakasz („a futtató az ilyen verseket eleve kihagyja”) azt sugallja, hogy a versszámozás-eltérés kezelve van, pedig nincs. |
| Workflow | ELTÉRÉS (alacsony) | `.github/workflows/f22_parositas.yml:7-8,15,91-93` | A megjegyzések elavultak („konyv=1Móz … plafon_usd=3.90 … kemeny korlat 4.00”, „a push csak a claude/f22-1moz agra mehet”), és van egy halott `if false; then : fi` blokk. |
| (8) Brief fejléce | OK / ELTÉRÉS (alacsony) | `F22_KAROLI_STRONG_BRIEF.md:8,11,14,160-166` | `allapot: dontesre_var`, a `kovetkezo` „Te:”-vel kezdődik: OK. Az `ir` listából hiányzik az `f22/minta_2Moz.tsv`, az `f22/valaszok/{sonnet,c}/2Moz.jsonl`, az `f22/elvetett/2Moz_*` és a `naplok/F22_2Moz_atnezes.tsv`; a listában az 1Moz.jsonl szerepel. A D8 felvételéhez nem tartozik verzió-sor. |
| Jelentés 3. szakasz: folytatás | ELTÉRÉS (alacsony) | `jelentes.md:45` vs. `f22/futasnaplo.tsv:363-367` | A jelentés szerint a futás „a 105. kötegtől folytatódott”. A napló szerint a 105. köteg 17:24-kor kész (2 próba), és az újraindítás 17:44:05-kor a 106. köteg 1. próbájával kezdődik. |
| A2 | nem alkalmazható | — | A `NYITOTT_FELADATOK.md` nem változott (`git diff --name-only`). |
| A3–A6 | nem alkalmazható | — | Nincs tanulmány, párhuzam, PaRDeS-réteg vagy nevesített tanító a diffben; az E12–E15 0 találat. |
| Ellenőrzőlista 1: kiszűrt/törölt sorok | OK | `git diff --numstat` | 49 törölt sor, adatsor egy sem (a futasnaplo.tsv csak +171 sor, mind c/2Moz). Kategóriák: datasetek 8 (cserélt), SEMA 1, brief 3, futtatas.txt 3, workflow és szkriptek a többi. Kiszűrve: 1 Károli-vers a mintából (35:36, 36 token → kezi), 1 eredeti vers (36:38, 22 token → kezi). C-oldalon 9 véglegesen kapuhibás vers (S-only, alacsony). |
| Ellenőrzőlista 2: kulcstartomány | OK (fejezetszint) / ELTÉRÉS (lásd 36. fejezet) | `jelentes.md:59-100` | Mind a 40 fejezet szerepel; Károli 1213 vers = 1212 a mintában + 1 kezi. A versmegfeleltetés a 36. fejezetben nem fedi le a tartományt (lásd fent). |
| Ellenőrzőlista 3: a nulla-diff hatóköre | — | — | Az 1Moz táblák üres diffje a commitolt fájlokra vonatkozik. Az új kóddal végzett újragenerálásra és az `--ellenoriz` futására nem. |
| Ellenőrzőlista 4: sorszám-változás, E17 | NEM ELLENŐRIZHETŐ | `DONTESEK.md:11` | Új táblák: +23966 és +49396 adatsor (a main-en 0). Az E17 küszöbe nyitott (DT3, javaslat 1%), és a CI nem futtat E17-et. A bontás a jelentés 4.1 szakaszában megvan (bizonyosság × fejezet). |
| Ellenőrzőlista 5: ⛔ pontok | OK / részben NEM ELLENŐRIZHETŐ | brief:66-69,121 | 1. megállás: a C-vetítés (1,918 < 3,90) és a Sonnet végleges kapuhibája (`\tC$` 0, tehát S-only sor nincs kapuhiba miatt) rendben; a /usage nem ellenőrizhető. 2. megállás: `dontesre_var`, merge nincs. A 106. kötegnél történt plafonleállás után felhasználói döntés jött (D8). |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. A 2Móz 36:1–37 eltolt versmegfeleltetéssel került a kanonikus táblába, 73 `magas` linkkel, jelölés nélkül (parok_2Moz.tsv:21391–).
2. A páratlan versek listája a fejezeten belüli eltolódást nem észleli; a 4Móz 30-ban ugyanez a hiba várható.
3. A `sonnet_koteg.py` docstringje tévesen írja le a 35:36 okát (A1).
4. Az E16 HIBA a PR-en, ha a cím nincs `[ELLENŐRZŐ]` előtaggal.
5. Az önteszt nem fedi a D8 új plafonlogikáját.
6. A workflow megjegyzései elavultak, és van benne halott kód.
7. A brief `ir` listája és verzió-sora hiányos.
8. A jelentés „105. kötegtől” állítása eltér a naplótól (106).

---

## Kezelés (az orkesztrátor, az ellenőri kör után)

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | 36:1–37 eltolt párosítás, `magas` jelölés | **Javítva (kezelve, nem megoldva):** az `adat/…`-ban nincs többé link ezekről a versekről; `f22/kezi_versek_2Moz.tsv` + `egyesit.kezi_felulir()`: a 36:1–37 `kezi`, az átnézési sorban. A tábla új összege: parok 23 795 (magas 22 631, alacsony 1 164); szavak kezi 1 456. Az eltolódás igazolva az adatból (Károli 35:36 ↔ TAHOT 36:1, Károli 36:n ↔ TAHOT 36:(n+1)). A versmegfeleltetés-javítás és a modellek újrafuttatása nyitott (N-F22 helyőrző), jelentés 5.1. |
| 2 | A lista nem észleli a fejezeten belüli eltolódást | **Dokumentálva, nyitva:** a jelentés 5.1/5.3 kimondja a hatókört; az `f22_elemzes.py` új „gyanús fejezetek” sora (nincs link, vagy `magas` < 70%) a 2Mózesre a 36. fejezetet jelzi, az 1Mózesre nem jelez semmit. Önálló eltolódás-detektor a 3Móz előtt (N-F22). |
| 3 | Téves docstring (A1) | **Javítva:** `sonnet_koteg.py`. A jelentés 5.1-ében az első menet téves leírását is helyreigazítottam. |
| 4 | E16 | **Kezelve:** a draft PR címe `[ELLENŐRZŐ]` előtaggal kezdődik. |
| 5 | Önteszt nem fedi a D8-at | **Javítva:** `futtat.plafon_hiba()` kiemelve (a `hivas` ezt hívja), az `f22_c_futtat.py --onteszt` lefedi a képletet (min. 1,00), az `auto`-t, a más könyv sorait kizáró összegzést, a könyvplafon és az összesített korlát megállítását; a `plafon_futas` nélküli (F21) ág változatlan. Önteszt: rendben. |
| 6 | Workflow megjegyzések, halott kód | **Javítva** (`f22_parositas.yml`). |
| 7 | Brief `ir` lista, verzió-sor | **Javítva** (`ir` bővítve: minta, jsonl, elvetett, atnezes, kezi_versek; verzió-sor v2.1). |
| 8 | „105. kötegtől” | **Javítva** a jelentésben: a futás a 106. kötegtől folytatódott. |
| — | Nem ellenőrizhető tételek (K1, K2, K7, f22_statisztika, öntesztek) | **Lefuttattam az orkesztrátor oldalán:** `egyesit.py --ellenoriz` rendben (2Móz és 1Móz), az újraépítés bájtra azonos (K7), az 1Móz táblák változatlanok, az öntesztek rendben; a kimenetek a `F22_2Moz_jelentes.md` 3–4. szakaszában. |

**Az 1. kör után nem készült második, független kör**; a fenti javítások az orkesztrátor saját ellenőrzésével zárultak (jelentés 7/7. pont).
