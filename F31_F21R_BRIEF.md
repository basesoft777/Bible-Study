---
feladat: 31
cim: "Károli–Strong párosítás: regressziós mérés az új prompttal (DT21 a–e)"
kod: F21R
tipus: feladat
fazis: 1
modell: sonnet
allapot: lezarva
ad: "prompt_v3; arany v3 (csak ha az a–e érinti és jóváhagyva); F3V3 és Sonnet-futás 200 versen; mérés és teljes bibliai költségvetítés; döntési alap a #22 sorsához"
kovetkezo: "#22 sorsa – felhasználói döntés a mérés számai alapján"
lezarva_osszegzes: "Teljesítve a #21 regressziós mérésében (PR #105), külön nem fut."
olvas: [DONTESEK.md, naplok/F21P_jelentes.md, naplok/F21_zaras.md, f21p/, eszkozok/karoli_strong/, .github/workflows/f21p_pilot.yml, F22_KAROLI_STRONG_BRIEF.md]
ir: [f21p/, naplok/F21R_meres.md, naplok/ELLENOR_F21R.md, DONTESEK.md]
fugg: [21]
nem_fugg: [22]
---

# Károli–Strong párosítás: regressziós mérés az új prompttal

Teljesítve a #21 regressziós mérésében (PR #105), külön nem fut.

**Egy mondatban:** a DT21 a–e konvenciódöntéseit átvezetjük a jegyzetbe és egy új promptba (`prompt_v3`), lefuttatjuk vele a C-t és a Sonnetet a 200 verses pilot-mintán, megmérjük, és megállunk. Éles, teljes bibliai futás **nem** indul.

## Háttér

- A #21 pilot (PR #92) eredménye: egyik mért összeállítás sem felelt meg a döntési szabálynak. A C egyedül 93–94%-os, stabil (a két futása közti eltérés < 0,6 százalékpont), a teljes Bibliára vetítve kb. 42 USD [38–46].
- A DT21 f–k pontjai a PR #92-ben lezárultak. Az a–e pontok „regressziós mérésre átvéve” jelzéssel várnak: ezeket ez a menet hajtja végre.
- A #22 (teljes futás) `dontesre_var` marad. Erről a felhasználó ennek a mérésnek a számai alapján dönt.

## A DT21 a–e döntései (szó szerint, ezeket kell átvezetni)

- **a) K7:** a jegyzet az irányadó, a prompt kivételét (többtagú igei szerkezet) szűkítsd rá.
- **b) C szabály:** a névmás csak ott megy az igére, ahol *'et* + rag áll (K3), máshol `betoldas`.
- **c) „azt/azért … hogy”:** egységesen: a mutató névmás `betoldas`, ha nincs eredetije, a *hogy* a kötőszóra megy.
- **d) 2Móz 26:13 *is*:** marad, a 6. táblázat dokumentálja.
- **e) D szabály:** a rag arra a magyar szóra megy, amelyik a megfelelő személyragot viseli (*szolgálójának* ← -āh).

## Lépések

**R0. Előfeltétel.** Ellenőrizd, hogy a PR #92 a `main`-ben van. Ha nincs, állj meg és jelezd. Új ág a `main`-ből. Olvasd be a pontos útvonalakat (jegyzet, arany, minta), és ha eltérnek a fejléc `olvas`/`ir` listájától, a fejlécet javítsd.

**R1. Jegyzet v2 → a–e.** A `vegrehajto-opus` vezeti át az a–e pontokat a konvenció-jegyzetbe. Utána nézze meg, érinti-e valamelyik pont az arany v2 linkjeit.
- Ha nem érinti: az arany v2 marad a mérési alap, arany v3 nem készül.
- Ha érinti: versenkénti diff az arany v2-höz képest (vers, régi link, új link, melyik a–e pont). **⛔1 Megállás:** a felhasználó jóváhagyja, csak utána fagy be az arany v3.

**R2. `prompt_v3`.** A tíz konvenció és az a–e pontok. A példaversek nem lehetnek a 200 verses mintában (szkripttel ellenőrizve, az eredmény a jelentésbe).

**R3. Szárazbecslés.** A C (F3V3) és a Sonnet (S3V3) várható költsége a 200 versen, valamint a pilot eddigi kumulatív költsége a `futasnaplo.tsv`-ből. **⛔2 Megállás:** a becslést mutasd meg, a trigger csak jóváhagyás után mehet. Ha a kumulatív összeg ezzel 3 USD fölé menne, ezt külön jelezd.

**R4. Futás** (OpenRouter, Actions workflow). Mindkét modell ugyanazzal a `prompt_v3`-mal, ugyanazzal a kapuval. A Sonnet OpenRouter-azonosítóját a futásnaplóba írd. Kemény plafon: a pilot 3 USD-s kerete, kumulatívan. **Az Opus nem fut**, mert az arany is Opus, így a mérése nem lenne független.

**R5. Mérés (P4).** A legfrissebb befagyott aranyra (v3, ha készült, különben v2), rétegenként:
1. **C (F3V3)** egyedül, a két v2-es C-futás (F3V2, F3V2b) mellett, a (c) típusú hibák újrabesorolásával.
2. **Sonnet (S3V3)** egyedül.
3. **Sonnet + C pár:** a Sonnet az A, a C (F3V3) a B szerepben; A∩B = `magas`; az öt feltétellel; döntőbíró nincs. Ha az egyik oldal kapuhibás, a vers minden linkje `alacsony`, és az `alacsony` arányba is beleszámít.

**R6. Költségvetítés (P5).** Teljes Biblia (31 158 vers), 90%-os intervallummal, a C egyedül, a Sonnet egyedül és a Sonnet + C pár. Rétegbesorolás: az F22 szerinti műfaji besorolás a DT21 h) alapján (Prédikátor és Siralmak → költészet, Dániel → próféta, Ruth és Eszter → ÓSZ-próza). A költség-ellenőrzésnél a leave-one-out számít (DT21 g).

**R7. Jelentés és zárás.** `naplok/F21R_meres.md`: összesítő tábla (modell, pontosság, lefedettség, `magas` arány és pontosság, vetített költség) a v2-es számok mellett. A DT21 a–e állapota 🟢 a `DONTESEK.md`-ben; ha új döntési sor kell, csak helyőrzővel (`DT-F<nn>`). Menetzárás a szokott módon: `fuggetlen-ellenor` → `naplok/ELLENOR_F21R.md` → push → draft PR → a záró összefoglaló első sora a PR linkje és a CI állapota.

**⛔3 Megállás a mérés után.** A #22-höz nem nyúlsz: nincs briefdiff, nincs teljes futás, a fejléce `dontesre_var` marad.

## Elfogadási feltételek

- K1: a jegyzet és a `prompt_v3` az a–e mind az öt pontját tartalmazza, pontonként hivatkozva.
- K2: a `prompt_v3` példaversei és a 200 verses minta metszete üres (szkriptkimenet a jelentésben).
- K3: arany v3 csak ⛔1 jóváhagyásával; az arany v2 bájtazonos marad.
- K4: a futásnapló csak hozzáfűzéssel változik; a pilot kumulatív költsége ≤ 3 USD.
- K5: a P4 mindhárom mérése rétegenként, a v2-es C-számokkal egy táblában.
- K6: a P5 három vetítése 90%-os intervallummal, a h) szerinti rétegekkel.
- K7: nulla-diff: `adat/`, `konkordancia/`, a befagyott fájlok, a korábbi `valaszok/*.jsonl`, a #22 brief.
- K8: CI zöld, ellenőri jelentés `TISZTA`.

<!-- KOZVETLEN_FUTTATAS -->
Olvasd be ezt a briefet, és hajtsd végre az R0–R7 lépéseket. Három kötelező megállás van: ⛔1 (arany-diff, csak ha az a–e érinti az aranyat), ⛔2 (szárazbecslés a trigger előtt), ⛔3 (a mérés után). A kérdéseidet gyűjtsd egy csokorba az adott megállásnál. Az Opus nem fut mért modellként, a #22-höz nem nyúlsz, merge-et nem indítasz.
<!-- KOZVETLEN_FUTTATAS -->
