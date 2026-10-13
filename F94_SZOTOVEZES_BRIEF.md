---
feladat: 94
cim: Magyar szótövezés a Károlira — szótári alak és alapige minden szóalakhoz, licenctiszta hibrid eszközzel, mért pontossággal
kod: SZOTOVEZES
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: fut
ag: claude/f94-szotovezes
helyi_gep: igen
ad: a Károli minden szóalakjához szótári alak (Károli- és mai helyesírással), alapige és további elfogadható alak, forrásolt szabályokkal; a hibrid szótövező (v3) az eszkozok/ alatt; négy aranyminta a repóban, a negyedik független, felhasználó által ellenőrzött mérés; a pardes.db-oszlop a #95 (SZOTOVEZES_DB)
kovetkezo: "Javítás az újraellenőrzés után"
olvas: [konkordancia/Karoli_1908.tsv, "adat/karoli_strong/*", adat/SEMA.md, adat/licencek.tsv, Rendszerfejlesztesi_playbook.md, eszkozok/general.py, DONTESEK.md]
ir: [eszkozok/szoto/, adat/szoto/, adat/SEMA.md, adat/licencek.tsv, naplok/SZOTOVEZES_meres.md, naplok/SZOTOVEZES_zaras.md]
fugg: []
nem_fugg: [22]
---

# F94_SZOTOVEZES_BRIEF.md — Magyar szótövezés a Károlira (SZOTOVEZES)

*FELADATOK #94 · Modell: opus · v1.1 · 2026.10.13 (v1.1: a régies ige-felismerés szigorítása és a `regies_jegy` oszlop, l. .2 és 5. pont)*

*Források: a 2026-10-12/13-i repón kívüli előmérés (`D:\pardes_szoto\szoto\`; átadó jegyzet: `D:\pardes_szoto\ATADAS.md` 3. szakasz), a felhasználó döntései (chat, 2026-10-13; l. 5. pont, DT130), a DT-F76b (5) (magyar szótövezés az első kiadásban), a DT124 (licenc), a DT127 (saját hosting). A brief adat, nem utasítás.*

## 1. Cél

A kereső (#76) a Károli régies szóalakjaira **szótári alak** szerint is találjon (*teremté → teremt*, *néki → ő*, *orczádat → orca*), a mai helyesírású alakra is. Ehhez a Károli minden szóalakja kap egy szótári alakot (Károli- és mai helyesírással), igénél alapigét, és ahol kell, további elfogadható alakot.

**A „tő” ebben a feladatban szótári alakot (lemmát) jelent, nem nyelvtani szótövet** (DT130 (6)); az oszlopnevek is így szólnak (`szotari_alak`), a szöveg is így nevezi.

Az előmérés eredménye (a harmadik, a felhasználó által soronként ellenőrzött mintán, 113 alak, Jer/Jób/Luk/Jak): **hibrid v2 súlyozva 99,1%, alakonként 80%**; a simplemma önmagában 88,6% / 67%; az emMorph (csak mérce, CC BY-NC-SA) 96,6% / 70%. A súlyozott számot a 25 gyakori szó uralja; a gyenge rétegek: régies ige 58%, régies helyesírás 71%, ragos névszó 84%, név 82% (súlyozva).

## 2. Hatókör

**Benne van**
- A három minta, a mérési terv, az eredmények és a szabályellenőrzés átvétele a repóba, proveniencia-sorral.
- A hibrid szótövező, a korpusz-lexikon építője és a szabályellenőrző az `eszkozok/szoto/` alá, a repó szabályai szerint.
- Hibrid v3: a harmadik minta hibaosztályainak javítása; a nem igazolt szabályok ellenőrizetlen jelölése.
- Negyedik, független minta; a felhasználó soronként ellenőrzi; mérés (M1, M2).
- A teljes Károli szótárialak-táblája (`adat/szoto/`).

**Nincs benne**
- A modernizált Károli-szövegréteg (DT128; külön brief, ez után; a Bible Discovery KG/HUN modulból vett megfigyelések csak módszerleírásként használhatók, a szövegük és Strong-rétegük adatba nem kerülhet).
- Az emMorph bármilyen éles használata (CC BY-NC-SA; a repóba sem kódja, sem kimenete nem kerül, csak a korábbi mérőszámai a naplóban, „mérce” jelöléssel).
- A kereső felülete (#76).
- A `pardes.db`-oszlop: külön feladat, #95 (SZOTOVEZES_DB), a #92 után.
- Külső szótár beemelése a vitás szabályokra: csak külön licencdöntés után (l. N-F94b).

## 3. Lépések (⛔ a kötelező megállások)

### .0 — átvétel és döntések (csak a repóba hoz, nem javít)

1. A `DONTESEK.md` DT130 tétele (l. Melléklet), 🟢 állapotban — ha a befogadás nem vitte be.
2. A három minta átvétele `adat/szoto/` alá egységes sémával:
   - `szoto_minta_1_fejlesztes.tsv` (213 alak, 1Móz 1–25; forrás: `szoto_aranyminta_tervezet.tsv`),
   - `szoto_minta_2_fejlesztes.tsv` (180 alak, Zsolt 1–41 + Ézs 40–55; forrás: `szoto_fuggetlen_minta.tsv`; **a Gal/Ef/Zsid rész üres maradt**, mert a `token_karoli` csak az ÓSZ-t tartalmazza — a fájlnév és a proveniencia-sor ezt mondja ki, nem a terv szerinti hatókört),
   - `szoto_minta_3_ellenorzott.tsv` (113 alak; forrás: `szoto_harmadik_minta.tsv`).
   Közös oszlopok: `alak`, `gyakorisag`, `kategoria`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `ellenorzes`, `indoklas`, `pelda_igehely`, `strong`. Az `ellenorzes` értéke soronként: `felhasznalo` (a felhasználó ellenőrizte) / `modell_ellenorizetlen` (a felhasználó „mehet”-tel engedte, sorát nem nézte) — **nem üres, és nem „ellenőrizve”**. Az 1. és 2. mintán a 6 felhasználói döntéssel lezárt sor `felhasznalo`, a többi `modell_ellenorizetlen`.
3. **Eltérés-lista:** az 1. és 2. minta korábbi döntések szerint készült. Gépi összevetés a DT130 végleges pontjaival (lesz külön szótári alak; Seregek; kevéssé; C) képzett igealak alapigével; vagy kettős elfogadás). Az eltérő sorok listája `naplok/SZOTOVEZES_meres.md`-be, **javítás nélkül**. ⛔ A felhasználó dönt soronként vagy csoportosan; a javítás csak utána, `ellenorzes=felhasznalo` jelöléssel.
4. A mérési terv, a három mérés eredménye (M1, M2, harmadik minta) és a szabályellenőrzés összefoglalója a `naplok/SZOTOVEZES_meres.md`-be, mind a saját proveniencia-sorával (a repón kívüli fájl neve + sha256 + ts).
5. A `adat/SEMA.md` új szakasza a `adat/szoto/` tábláiról.

### .1 — eszközök az `eszkozok/szoto/` alá

1. `hibrid.py` (v2, a viselkedés változatlan; az átvétel után a három mintán a mérés ugyanazt a számot adja, mint az előmérés — ez az átvétel próbája).
2. `lexikon_epit.py`: a korpusz-lexikon **a `konkordancia/Karoli_1908.tsv`-ből**, nem a `pardes.db`-ből (a `pardes.db` generált index, nem forrás; DT28). Ez egyben pótolja az ÚSZ-t, amely a `token_karoli`-ból hiányzott. A lexikon generált tábla: `adat/szoto/karoli_lexikon.tsv`, fejlécében `# GENERÁLT: …`.
3. `szabaly_ellenorzes.py` (Strong-támasz: a régi alak tokenjei hordozzák-e az új alak fő Strong-ját, `adat/karoli_strong/`-ból); kimenete `adat/szoto/szabaly_ellenorzes.tsv`.
4. `meres.py`: egyetlen mérő a négy mintára (M1 alakonként, súlyozva, rétegenként; M2 a pooled definícióval, l. 5. pont); a hibrid és a simplemma, emMorph nélkül.
5. A repó szabályai: kódolási őr az importok után, TSV `split('\t')` / `'\t'.join()`, `csv` modul nélkül; abszolút `C:`/`D:` útvonal nincs; Python 3.11 alatt is fut.
6. **Licenc (playbook 2. pont):** a simplemma kódja MIT; **az adatfájljainak licencét a forrásból kell szó szerint idézni** (nem feltételezni). Új `adat/licencek.tsv`-sor a simplemmára és a `adat/szoto/` tábláira. ⛔ Ha a simplemma adata nem MIT-kompatibilis a nyilvános kiadással, megállás, a felhasználó dönt.
7. A `requirements` (vagy a repó szokásos függőségjegyzéke) a simplemma rögzített verziójával (az előmérés: 2.0.0).

### .2 — hibrid v3

A harmadik minta hibaosztályai (a gyakorisággal): *-é* kérdőszócska kötőjellel (*láttad-é, értheti-é, hívhatja-é, elérheted-é, határozod-é*), birtokos + rag (*igéjéért, házadhoz, barátaiért, kerekségének*), igekötő + ismeretlen ige (*meggyarapodnak, feloldja, megütközzék, megkiván → megki*), *magának → mag*, *atyámnak → atyám*, *Melkié* kisbetűsítve, *eljőtök*, *legelőjök → legel*, *kevéssé* (önálló, DT130 (9)). A v2 ismert teljes-Károli hibái is: *hozzá → hoz, alá → al, elé → el, éljen → élj, köteleid → kötelei*, a *-ván/-vén* csonka tő.

- Javítás **szabály- és osztályszinten**, nem egyes alakokra szabva; a kivételtábla bővítése csak általános Károli-ismeretből, nem a mérés hibáiból válogatva (meresi_terv 1.3).
- A szabályellenőrzés 51 szabályából **17 nem alátámasztott** (12 gyenge, 3 ellentmond: *kiván → kíván, falv → falu, félelm → félelem*; 2 adat nélkül: *sűly, fark*; a *cz → c* a korpuszból nem igazolható). Ezek a kimenetben `szabaly_forras=modell_ellenorizetlen` jelölést kapnak; a 34 alátámasztott `korpusz_strong`.
- **A régies ige-felismerés szigorítása (v1.1).** A v2 a jelölt igetövet olyan ragos alakkal is igazolja, amely névszón is előfordul (`-nak/-nek`, `-tok/-tek/-tök`): így a *házának* „régies ige” lesz (*ház* + *-ának*, mert a *háznak* előfordul). A teljes Károlin a leggyakoribb felismert „régies igék” között ott van a *házának, királyának, felé, többé, mellé, közé, halál, Szela* (az előmérésben 2 775 alak, 13 618 token — felső becslés). A szótári alakra ez többnyire nem árt (*házának → ház*), a modernizálásban (DT128) viszont névszóból igealak lenne. Szigorítás: a jelölt tő csak **igei** ragos alakkal igazolható (főnévi igenév, múlt idejű *-t/-tt*, felszólító, *-ván/-vén*); a névszóval közös végződés nem attesztáció. Napló: a teljes Károli 200 leggyakoribb felismert régies igealakja kézi besorolással (ige / nem ige), a szigorítás előtt és után.
- **A régies igei jegy megőrzése (v1.1).** A felismert régies végződés nyelvtani jelentése a kimenetbe kerül (`regies_jegy`), mert a hibrid a felismeréskor ezt már tudja, és a modernizálás (DT128, külön brief) bemenete lesz. Példák: *-á/-é* → `mult.targyas.E3`, *-a/-e* → `mult.alanyi.E3`, *-ának/-ének* → `mult.T3`, *-ék* → `mult.E1`, *-ál/-él* → `mult.E2`, *-jál/-jél* → `felszolito.E2`, *-ván/-vén* → `hatarozoi_igenev`; a teljes értékkészlet a `adat/SEMA.md`-be. **A jegy a régies alakot írja le, nem a mai alakot:** a *monda* jegye `mult.alanyi.E3`, a mai megfelelője mégis *mondta* — a mai alak képzése a modernizálás dolga, saját kivételtáblával, a jegyből közvetlenül nem képezhető. A jegy csak a szigorított felismerés után töltendő ki; nem igei alaknál és a kivételtáblából jövő alaknál (pl. *vala, lőn*) üres, ha a kivételtábla nem ad jegyet.
- Regresszió: a v3 a három fejlesztési mintán nem rosszabb a v2-nél (rétegenként sem); a teljes Károlin a v2-höz képest változott alakok száma és 30 véletlen változás kézi listája a naplóba.
- **A v3 befagyasztása** (sha256 a naplóban) a .3 mintavétele előtt.

### .3 — negyedik minta és mérés

1. Mintavétel a befagyasztott v3 után: ~100–120 Károli-szóalak eddig nem mintázott könyvekből (javaslat: 5Móz, 1Sám, Péld, Ezék, Márk, Ján, Róm, Jel), az eddigi három minta alakjai nélkül, ugyanazzal a rétegzéssel (gyakori, ragos névszó, régies ige, régies helyesírás, mai igealak, név), rögzített véletlen-maggal, a `Karoli_1908.tsv`-ből.
2. A modell szótárialak-javaslatai indoklással, **a hibrid futtatása előtt**; bizonytalan sor jelölve.
3. ⛔ **A felhasználó soronként ellenőrzi** (az `ellenorzes` oszlopot ő tölti). A mérés csak a `felhasznalo` sorokon.
4. Mérés (`meres.py`): M1 a v3-ra, a v2-re és a simplemmára; M2 a negyedik minta lemmáira. A negyedik minta a mérés után fejlesztési halmazzá válik; erre hangolt eredmény már nem független.
5. A teljes Károli szótárialak-táblája: `adat/szoto/karoli_szotari_alak.tsv` (alakonként egy sor: `alak`, `szotari_alak`, `szotari_alak_mai`, `alapige`, `tovabbi_elfogadhato`, `modszer` [kivetel | szabaly | simplemma | lexikon | nev], `szabaly_forras`, `regies_jegy` (v1.1; l. .2), a fejlécben proveniencia-sor és a v3 sha256-ja). Generált tábla; kézzel nem szerkesztendő, a javítás a kivételtáblában vagy a szabályban történik.

### A `pardes.db`-oszlop — külön feladat (#95)

A szótári alak, a mai alak, az alapige és a további elfogadható alak a `pardes.db`-be a #95 (SZOTOVEZES_DB) csonk-feladat, mert a `eszkozok/sqlite_epit.py`-t írja (sorrend: #88 → #89 → #92 → #95 → #76); így a #94 .0–.3 most indulhat (felhasználói döntés, 2026-10-13). A #94 a `adat/szoto/karoli_szotari_alak.tsv`-ig jut.

## 4. Elfogadási feltételek

- **K1.** A három régi minta a repóban, egységes sémával, soronként `ellenorzes` értékkel; az eltérés-lista naplózva és a felhasználó döntésével lezárva.
- **K2.** Az átvett v2 a három mintán bitre ugyanazt az M1-számot adja, mint az előmérés (harmadik minta: 80% / 99,1%).
- **K3.** A negyedik, felhasználó által ellenőrzött mintán a v3 **súlyozva ≥ 90%** (meresi_terv 4. pont), és az M2 (c) (szótári alak vagy Strong) **≥ 98%** a minta lemmáin; mellette alakonként és rétegenként is kiírva, küszöb nélkül. Ha nem éri el: megállás, javaslat a felhasználónak (nem további hangolás ugyanarra a mintára).
- **K4.** Minden szabály `szabaly_forras` jelöléssel (34 `korpusz_strong`, a többi `modell_ellenorizetlen`); a simplemma adatlicence szó szerint idézve a `licencek.tsv`-ben.
- **K5.** Emmorph-kód vagy -kimenet nincs a repóban; abszolút útvonal nincs; `csv` modul nincs; Python 3.11 alatt fut; CI zöld; a független ellenőr eltérés nélkül zár.
- **K6.** (v1.1) A régies ige-felismerés 200 alakos kézi besorolása a szigorítás előtt és után a naplóban; a szigorítás után a besorolt listán nincs névszó régies igeként; a `regies_jegy` csak igei alakon kitöltött.

## 5. Döntésnapló

- **DT130** 🟢 — a szótövezés alapdöntései (a felhasználó, chat, 2026-10-13; a teljes szöveg a Mellékletben).
- **N-F94a** — a különálló igekötő (*meg nem*, *ki fog*, *le … száll*) kezelése nyitott; a v3 nem kezeli, a negyedik mintában jelölendő, ha előfordul.
- **N-F94b** — külső szótár (pl. Hunspell hu_HU, MPL/LGPL) a 17 nem alátámasztott szabály ellenőrzésére: csak külön licencdöntés után; addig az ellenőrizetlen jelölés marad.
- **N-F94c** — a `jó` Strong-párosítása az 1Móz 1:4-ben (H2895 nálunk, H2896 a várható): mellékes lelet, a #94-en kívül vizsgálandó.
- **v1.1** (felhasználó, chat, 2026-10-13: „a” — a brief módosítása a végrehajtás előtt): a régies ige-felismerés szigorítása és a `regies_jegy` oszlop (.2, .3/5, K6). Forrás: a modernizálás előkészítése (DT128), a teljes Károlin mért hamis pozitívok, és egy másik session javaslata a jegy megőrzésére.

## Melléklet — a `DONTESEK.md` tétele (helyőrzővel)

| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |
|---|---|---|---|---|---|---|---|
| DT130 | #94 SZOTOVEZES (az előmérés lezárása) | Milyen szabályok szerint kapjon a Károli minden szóalakja szótári alakot, és milyen eszközzel? *(forrás: a repón kívüli előmérés, `D:\pardes_szoto\szoto\`, 2026-10-12/13; a #94 .0 hozza a repóba)* | eszköz: 1. hibrid (saját szabályok + kivételtábla + Károli-lexikon + simplemma, MIT) · 2. simplemma önmagában · 3. emMorph (CC BY-NC-SA) | 1. | 🟢 | **Felhasználó (chat, 2026-10-13):** (1) a keresés a mai helyesírású alakra is talál; (2) ugyanazon szó régi és mai alakja egy szótári alak (*mely/amely*), két külön szó nem (*esztendő/év*); (3) a ragos névmás szótári alakja a személyes névmás (*néki → ő*); (4) igénél a szótári alak az igekötős ige, az alapige külön oszlop; (5) a nevek Károli átírásában maradnak; (6) a „tő” szótári alak (lemma), nem nyelvtani szótő; a *van* rendhagyó alakjai (*vagy-/van/vol-/val-/le-*) kivételtáblából; (7) a *lesz* külön szótári alak (*lőn, legyen, lészen → lesz*); (8) *Seregek* névként marad, ha Istenre vonatkozik (a Károliban mind a 119 nagybetűs előfordulás a „Seregek Ura/Istene” címben), a kisbetűs *seregek → sereg*; (9) *kevéssé* önálló határozószó; (10) C) képzett igealak: a szenvedő (*veretik, vettetik*) és a *-hat/-het* (*mehet*) külön szótári alak, az alapige-oszlop kitöltve, a mérésben mindkettő helyes; (11) kétértelmű alak (*vagy*: kötőszó / *van* E/2) csak szövegkörnyezetben dönthető, a mérésben mindkét olvasat elfogadott; (12) eszköz: a hibrid; a simplemma önmagában kevés (88,6% súlyozva a harmadik mintán), az emMorph kizárt (NC), csak mérce; (13) a szabályok és a minták szótári alakjai modell-állítások, ezért forrásolandók: a szabályellenőrzés szerint 34 alátámasztott, 17 nem (ellenőrizetlen jelöléssel marad). | `naplok/SZOTOVEZES_meres.md` (a #94 .0 után) |
