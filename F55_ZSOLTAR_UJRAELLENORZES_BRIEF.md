---
feladat: 55
cim: A régi, egy verssel eltolt zsoltár-kivonatra épülő állítások újraellenőrzése
kod: ZSOLTAR_UJRAELLENORZES
tipus: feladat
fazis: 1
modell: opus
munka: ertelmezo
allapot: lezarva
pr: 424
lezarva_osszegzes: "M0: 32 szűrt hely, 15 csoport; M1: módosul 4, megáll 2, visszavonandó 0; a HAMART-001 Bun-naplója javítva (Zsolt 53:1 → 53:2 / LXX 52:2), a tanulmány jelölve; M2: +2 TEREMT-002 lxx-hid audit-sor; DT-F55a–f; nyitott: N-F55a–d; független ellenőr 2 kör (6 + 3 eltérés, javítva vagy döntve); zárás: naplok/ZSOLTAR_UJRAELLENORZES_zaras.md"
ag: claude/f55-zsoltar
ad: minden kézi forrásbeli állítás, amely a régi LXX_kivonat eltolt vagy hiányzó zsoltárversére épült, felmérve, és soronként ítélettel (megáll / módosul / visszavonandó) a helyes vers LXX_OS-szövege alapján; a módosuló állítások a forrásrétegben javítva, az új lxx-hid futások az auditok.tsv-ben naplózva
kovetkezo: "Te: a PR #424 merge-e a te döntésed; nyitott: N-F55a–d."
olvas: ["konkordancia/LXX_OS/*.tsv", konkordancia/Karoli_1908.tsv, naplok/FORRASKIVEZETES_M5_M7.md, naplok/FORRASKIVEZETES_M5_eltereslista.tsv, adat/jeloltek.tsv, tematikus_lezart/, genezis/, ujszovetseg/, melyelemzesek/, motivumok/, motivumlog/, naplok/T1_TEREMT002_auditok_munkalap.tsv, naplok/LXX_OS_LEFEDETTSEG_M0.md]
ir: [adat/auditok.tsv, tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md, tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, "naplok/ZSOLTAR_UJRAELLENORZES_*"]
fugg: [42, 54]
---

# F55_ZSOLTAR_UJRAELLENORZES_BRIEF.md — A régi, eltolt zsoltár-kivonatra épülő állítások

*FELADATOK #55 · Modell: opus · v1 · 2026.10.05 · forrás: a #42 (FORRASKIVEZETES, PR #176) nyitott tétele, `naplok/FORRASKIVEZETES_M5_M7.md` (f3)*

## 1. Cél

A régi `LXX_kivonat_Zsoltarok.tsv` a feliratos zsoltárokban egy verssel el volt tolva: a „Zsolt 22:2” sor például a Károli 22:3 görög szövegét adta. A #42 az `LXX_OS`-re állt át, ezért ez a hiba ma már nem keletkezik. Az eltéréslista (`naplok/FORRASKIVEZETES_M5_eltereslista.tsv`) **739 eltolt** (`zsoltar_eltolas`) és **66 csak a régiben meglévő** (`csak_regi_vers`) zsoltárverset sorol fel.

Ami a régi adatra épült, az ma is a kézi forrásokban áll. A feladat megkeresi ezeket az állításokat, és mindegyikről eldönti, hogy a helyes vers görög szövegével megáll-e.

**Előfelmérés (a befogadáskor, `manual`, ts=2026-10-05).** A #42 által listázott helyekből az eltéréslistával összevetve:

| Hely | Vers | Eltéréslista | Várható érintettség |
|---|---|---|---|
| `Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` 3/c táblázat | Zsolt 53:1 („LXX-számozás”, διεφθάρησαν G1311) | `csak_regi_vers` (az új forrás ma n=0) | **érintett**: a vers azonosítása és a görög alak forrása kérdéses; a 158. sor Zsolt 14:1 / 53:2 lelete is ezen áll |
| ugyanott | Zsolt 14:1 | nem eltolt | valószínűleg nem érintett |
| `adat/jeloltek.tsv` TEREMT-002 | Zsolt 80:6–7 | `zsoltar_eltolas` | az elutasítás héber kritériumon áll (nincs H8414+H0922 pár), az LXX-adat nem döntő; ellenőrizendő |
| ugyanott | Zsolt 33:6, 104:30, 107:40 | nem eltolt | valószínűleg nem érintett |
| `Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` 84–96. sor | Zsolt 116:4, 116:17 és az LXX-ellenőrzés zsoltárversei | ellenőrizendő | az „15/17 igehely ἐπικαλέομαι” számítás zsoltárverseit kell összevetni |

Az előfelmérés nem teljes körű: csak a #42-ben grep-pel talált helyeket nézte. A teljes kört az M0 állítja elő.

## 2. Hatókör

**Benne van:**
- teljes körű keresés a kézi forrásrétegben (`tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `motivumok/`, `motivumlog/[ID].md`): minden zsoltárvers, amelyhez görög alak, LXX-Strong-szám vagy LXX-alapú állítás tartozik, és amely a 739 + 66 vers között van (M0);
- soronkénti ítélet a helyes vers `LXX_OS`-szövege alapján (M1);
- a módosuló állítások javítása a forrásrétegben, és az új `lxx-hid` futások naplózása az `adat/auditok.tsv`-ben (M2).

**Nincs benne:**
- generált fájl (`lexikon/`, törzscikk) kézi írása: ez a #36 renderelése;
- a pilot- és próba-példányok (`motivumlog/lexikon_pilot/`, `generalt_proba/`): ezek változatlanok maradnak (DT-F42a), a jelentés csak jelöli őket;
- a `naplok/T1_TEREMT002_auditok_munkalap.tsv`: történeti munkalap, nem módosul;
- az `adat/auditok.tsv` meglévő sorainak átírása: a napló csak bővül (új sor, régi sor marad);
- a nem zsoltár-könyvek eltérései (`strong_eltero`, `nagy_eltero`): ezek a #42 eltéréslistájában dokumentáltak.

## 3. Lépések

**Előfeltétel:** a #54 lezárva a `main`-en. A #54 a zsoltár-feliratok kulcsolását is javíthatja, ezért az ítélet a javított `LXX_OS`-en alapul.

### M0 — Teljes felmérés (csak olvas) és ⛔

Jelentés: `naplok/ZSOLTAR_UJRAELLENORZES_M0.md`, táblázat: `naplok/ZSOLTAR_UJRAELLENORZES_helyek.tsv`.

1. **Keresés:** a hatókör minden kézi forrásfájljában a zsoltárhivatkozások (`Zsolt N:v`, `Psalm`, `LXX-számozás`, valamint görög szóalak vagy `G####` ugyanabban a sorban vagy táblázatsorban). A mintát és a találatszámot a jelentés rögzíti.
2. **Szűrés:** csak az a hely marad, amelynek verse az eltéréslistán `zsoltar_eltolas` vagy `csak_regi_vers` kategóriájú (a #54 után is ellenőrizve).
3. **Hatás:** minden helyhez rögzítendő, hogy az állítás a görög adaton áll-e (és ha igen, mi a régi és mi a helyes görög alak és Strong-szám), vagy csak hivatkozás, és a döntést más kritérium hordozza (pl. héber negatív kritérium).
4. **A mostani `lxx-hid` futtatása** minden érintett versre, a parancs saját proveniencia-sorával.

**⛔ Megállás.** A felhasználó az érintett helyek listáját látja, és jóváhagyja:
- **(a)** a hatókört: ha az M0 a fenti `ir` listán kívüli fájlban talál érintett állítást, az `ir` bővítését;
- **(b)** a javítás formáját a kézi forrásokban: csere `【NAPLO: … javítva, F55】` jelöléssel (javaslat), vagy csak jelölés a régi szöveg mellett.

### M1 — Ítélet soronként

Minden érintett állításra:
- **megáll:** a helyes vers görög szövege ugyanazt az állítást támasztja alá (esetleg más versszámmal);
- **módosul:** az állítás igaz, de a vers vagy a görög alak más;
- **visszavonandó:** az állítás a helyes adattal nem tartható.

Indoklás a helyes vers `LXX_OS`-sorával és proveniencia-sorral. **Hiányt nem szabad gyenge vagy asszociatív anyaggal kitölteni** (CLAUDE.md 3. szabály). Ha a helyes versre az `LXX_OS` sem ad adatot, az ítélet „nincs adat”, és az állítás LXX-része visszavonandó.

### M2 — Javítás a forrásrétegben

- A „módosul” és „visszavonandó” ítéletek átvezetése az M0 (b) döntése szerint. Az értelmező próza egy kézben marad: aki egy tanulmányt vagy naplót javít, előbb az egészet elolvassa (CLAUDE.md, KONTEXTUS K1).
- Ha a javítás egy motívum minősítését, egy jelölt döntését (`adat/jeloltek.tsv`) vagy egy lelet ★ státuszát érintené: **⛔**, `DONTESEK.md`-tétel, a döntés a felhasználóé. A jelölttáblát a feladat nem írja.
- Az új `lxx-hid` futások új sorként kerülnek az `adat/auditok.tsv`-be; táblaírás előtt összevetés az eredetivel (CLAUDE.md, TSV).

### M3 — Zárás

- `naplok/ZSOLTAR_UJRAELLENORZES_zaras.md` (≤20 sor): ítéletenkénti végszámok, a javított fájlok listája, a #36-ra váró generált oldalak listája.
- A `fuggetlen-ellenor` jelentése: `naplok/ELLENOR_ZSOLTAR_UJRAELLENORZES.md`.
- A brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Az M0 keresése teljes körű és reprodukálható: a minta, a fájlkör és a találatszám a jelentésben áll.
- **K2.** Minden érintett hely szerepel a táblázatban ítélettel, indokkal, a helyes vers `LXX_OS`-adatával és proveniencia-sorral.
- **K3.** A kézi forrásokban nincs olyan LXX-zsoltárállítás, amely a régi, eltolt adatra épül, és nincs jelölve vagy javítva.
- **K4.** Generált fájl, pilot- vagy próba-példány, a T1-munkalap és az `auditok.tsv` meglévő sorai nem változtak.
- **K5.** Jelölt-, minősítés- vagy ★-változás csak `DONTESEK.md`-döntés után.
- **K6.** A CI zöld; a független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A feladat a #42 nyitott tétele; csonkként befogadva (PR #177). | #42 zárás, felhasználó |
| v1 | 2026-10-05 | Függ a #54-től: a zsoltár-feliratok kulcsolása ott javulhat, az ítélet a javított `LXX_OS`-en áll. | levezetett függés (`konkordancia/LXX_OS/*.tsv`) |
| v1 | 2026-10-05 | A hatókör a teljes kézi forrásréteg, nem csak a #42-ben talált öt hely; a T1-munkalap és a pilot-példányok nem módosulnak. | befogadási előfelmérés |
| v1 | 2026-10-05 | Jelölt-, minősítés- és ★-változás nem a feladat döntése: ⛔ és `DONTESEK.md`. | CLAUDE.md, KONTEXTUS K1 |
| v1 | 2026-10-19 | A befagyasztás (DT74 (3)) feloldva: a #11 1. lépcsője a main-en (PR #417). | felhasználó, 2026-10-19 |
| v1 | 2026-10-19 | M0 ⛔: (a) az `ir`-ből kikerül a két archivált Segitsegul-út (DT-F55a); (b) csere `【NAPLO: … javítva, F55】` jelöléssel, a régi versszám látható marad (DT-F55b); (c) az M2 audit-sorai a PR #420 merge-e után (DT-F55c). | orkesztrátor, a felhasználó felhatalmazásával |
| v1 | 2026-10-19 | Az ellenőr 1. körének tartalmi eltérései: a HAMART-001 audit-sorai most nem kerülnek be (DT-F55d, N-F55b); az F55-jelölés a rés előtt marad, a rés forrásneve a 2. lépcsős migrációban (DT-F55e, N-F55c); a Z02/Z03 történeti forrásnév + „53:1 sort nézték” jelölés (DT-F55f). | orkesztrátor, a felhasználó felhatalmazásával |
| v1 | 2026-10-19 | A 2. ellenőrzési kör 1. eltérése: a DT-F55d döntése marad, az indoka a SEMA 2.9 commit-szabályára (DT103) pontosítva; a HAMART-001 retroaktív ID, csak KÉZI jelentést kapna. Lezárva (M3). | orkesztrátor, a felhasználó felhatalmazásával |
