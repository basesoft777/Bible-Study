# F152 — a K1–K5 (DT-F151c) átvezetése az ISTENTISZT-001-en: mérés és megállás

Ág: `claude/f152-k1k5-atvezetes` (a main-ről, a #557 merge-e után, 3a2dbd51). Megbízás: az orkesztrátor, a
felhasználó jóváhagyásával („Igen, utána”, a #557 merge-e után). Modell: `claude-opus-5-5`.

Állapot: **⛔ megállt, adat nem változott.** A K1–K5 átvezetése előtt két kérdés jött elő, amelyre a
DT-F151c válasza nem ad választ (DT-F152b, DT-F152c), és a Kivonat 3. mondata is jóváhagyásra vár (3.).

## 1. DT-F152b — a K4 hatóköre: mi áll a *besém* után

Mérés: `naplok/F152_k4_meres.py` — scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=33) |
forras=TAHOT_kivonat.tsv (split('\t')) | ts=2026-11-01T19:08Z

| *besém* után | sor | igehelyek |
|---|---|---|
| JHVH (H3068) | 14 | 1Móz 4:26; 12:8; 13:4; 21:33; 26:25; 1Kir 18:24 (második); 2Kir 5:11; Sof 3:9; Zsolt 116:4, 13, 17; Jóel 2:32; 2Móz 33:19; 34:5 |
| *Elohím* + rag / *ha-Báal* | 2 (+1) | 1Kir 18:25 (*elohéchem*), 18:26 (*ha-Báal*); az 1Kir 18:24 első fele is *elohéchem* |
| névmási rag (H9020/H9023/H9021) | 7 | Zak 13:9 (*bismí*); Zsolt 105:1, 1Krón 16:8, Ézs 12:4 (*bismó*); Jer 10:25, Zsolt 79:6, Ézs 64:6 (*bismchá*) |
| ÚSZ (nincs TAHOT-sor) | 10 | Róm 10:12, 13, 14; 1Kor 1:2; 2Tim 2:22; 1Pét 1:17; ApCsel 2:21; 9:14, 21; 22:16 |

A K4 szövege („a *besém* után álló JHVH”) szó szerint a hét ragos sort is kizárná, mert az Ézs 43:1 és
45:3 is ragos (*besimchá*). A különbség a rag gazdája: a hét sorban Isten (Ő beszél, vagy Őt szólítják,
vagy Róla szól a vers), az Ézs 43:1-ben és 45:3-ban a megszólított ember (Jákób, Círus). Kérdés és
opciók: `DONTESEK.md` DT-F152b.

## 2. DT-F152c — a Róm 10:14 kapcsolatai és két motívumközi jelölt

`adat/kapcsolatok.tsv`, ISTENTISZT-001: 10:13 → 10:14 (17), 10:14 → 1Kor 1:2 (18), → 2Tim 2:22 (19),
→ 1Pét 1:17 (20), → ApCsel 9:14 (21), → ApCsel 22:16 (23). A 19. és a 20. sor a K1/K2-vel mindenképp
kiesik. A `jeloltek.tsv` két nyitott motívumközi sora (Róm 10:12, Róm 10:14 ↔ TEREMT-001 Róm 10:7, DT280)
a K2 után nem előfordulás-igehelyen áll. Kérdés és opciók: `DONTESEK.md` DT-F152c.

## 3. A Kivonat 3. mondata — javaslat (jóváhagyásra vár, nincs beírva)

Az F152 A.2 javaslatának 3. mondata a #151 K1–K3 döntésére várt. A K2 óta a név nélküli görög
segítségül hívás ugyanazzal az indokkal áll kint, mint az ApCsel 7:59 („nincs ὄνομα”, `jeloltek.tsv`).
Két változat:

> **(A)** A motívum nem az imádság vagy az istentisztelet általában: a formulán kívüli segítségül hívás
> (például ApCsel 7:59) a tágabb fogalomhoz tartozik, ide nem.

> **(B)** A motívum nem az imádság vagy az istentisztelet általában: a név nélküli segítségül hívás a
> tágabb fogalomhoz tartozik, ide nem, akkor is, ha ugyanaz a görög ige áll benne (ApCsel 7:59; 2Tim 2:22;
> Róm 10:12, 14).

Javaslat: **(B)**. Ez a mondat mondja ki a K2 határát az olvasónak. Az (A) a K2 előtti állapotot írja le.
Alap: `motivumok.tsv` `folerendelt_fogalom` („istentisztelet/imádság általában …”); a négy igehely az
átvezetés után az 1/b.-ben ezzel az indokkal elutasított jelölt. A K2 mondata a DT-F152c-től nem függ.

## 4. Ami a döntések után következik (terv)

1. `jeloltek.tsv`: 1Pét 1:17, 2Tim 2:22, Róm 10:12, Róm 10:14 → `elutasítva`. Az indoklásuk a DT-F151c
   felhasználói idézete, `manual` proveniencia, dátum. A `elofordulasok.tsv` négy sora törlődik, írás
   előtti összevetéssel.
2. A K4 szerint (DT-F152b) az Ézs 43:1, 44:5, 45:3 indoklása új alapra kerül, és a `negativ_kriterium`
   bővül.
3. A K5 szerint az 1Kir 18:25–26 `kapcsolodas`/`funkcio` mezője és a próza jelzi, hogy ott *Elohím* és
   *ha-Báal* áll.
4. `kapcsolatok.tsv` a DT-F152c szerint.
5. A próza: a számok (33 → 29, 23/10 → 23/6), a „3. A Róm 10:12” és a „Róm 10:14” szakasz, a 2Tim 2:22-es
   és az 1Pét 1:17-es említés. A szöveget egészében olvasom (K1), és a Kivonat 3. mondatát a jóváhagyott
   változattal írom.
6. A lap újragenerálása, és utána egy második generálás: annak nulla diffet kell adnia (E28). Végül
   `ellenoriz.py` és `ellenorzes/futtat.py`.

## 5. DT-F152b döntés után — újramérés (adatírás előtt)

A felhasználó döntése (2026-11-01, az orkesztrátoron át): „Csak ahol JHVH áll” — a K4 szó szerint (a). A
`DONTESEK.md` DT-F152b sora ✅. Adat még nem változott.

**Számok** (scope=adat/elofordulasok.tsv, id=ISTENTISZT-001, n=33 | forras=TAHOT_kivonat.tsv
(`naplok/F152_k4_meres.py`) | ts=2026-11-01T19:08Z): kikerül 4 (K1/K2) + 7 (DT-F152b) = 11 sor →
**22 előfordulás, 16 ószövetségi, 6 újszövetségi**. A megmaradó 6 ÚSZ-sor (Róm 10:13; 1Kor 1:2;
ApCsel 2:21; 9:14, 21; 22:16) mindegyikében ὄνομα áll.

**Kapcsolatok** (`adat/kapcsolatok.tsv`, ISTENTISZT-001: 25 sor): a DT-F152b miatt mindenképp kiesik
4 sor: 33 (Zsolt 105:1 → 1Krón 16:8), 34 (Zsolt 105:1 → Ézs 12:4), 35 (Jer 10:25 → Zsolt 79:6),
36 (Sof 3:9 → Zak 13:9). A K1/K2 miatt kiesik 2 (19, 20). A DT-F152c négy sora (17, 18, 21, 23) ettől
nem változik, a kérdés ugyanaz. Végeredmény: 19 sor, ha (b), 15 sor, ha (a).

**Más táblák:** az `auditok.tsv` 228. és 231. sora (Ézs 64:6 adhoc lekérdezés) napló, marad. Az
`lxx_dontesek.tsv` LD003 (Ézs 12:4, βοάω) versszintű LXX-döntés, motívum-id oszlopa nincs, marad;
a Kivonat LXX-mondatából viszont kikerül. A `jeloltek.tsv`-ben a hét sor (38, 50–54, 631) `beépítve` →
`elutasítva`. Motívumközi jelölt ezeken nincs.

**A Kivonatra gyakorolt hatás:**
- 1. bekezdés: „33 igehelyen (23 ószövetségi, 10 újszövetségi)” → 22 (16, 6). A LXX-mondat (19/23,
  eltérés: 2Móz 33:19; 34:5; Ézs 12:4; Zsolt 116:17) az Ézs 12:4 nélkül → várhatóan 13/16. Ez a
  meglévő mondatból levezetett szám, nem mérés; az átvezetéskor újramérem.
- A DT399 NAPLO-jegyzete (Ézs 64:6 beépítése, 32 → 33) történeti, a visszafordítást új NAPLO-jegyzet
  rögzíti.
- **A jóváhagyott 2. mondat** („csak az aktív, invokáló קָרָא בְּשֵׁם (kárá besém) tartozik ide …”)
  a DT-F152b után nem pontos: a határ most a *besém* utáni JHVH szó. Pontosítási javaslat (jóváhagyásra):
  > A motívum határát a szerkezet húzza meg: csak az aktív, invokáló קָרָא בְּשֵׁם יְהוָה (kárá besém
  > JHVH) tartozik ide, amelyben a *besém* után az Úr neve, JHVH áll; ahol névmás áll a helyén
  > („nevedet”, „nevét”), az nem tartozik ide.
  A passzívról szóló mondat (nikrá … al) változatlan.
- **A 3. mondat** (B) változata nem függ a DT-F152b-től.

**Feszültség a K5-tel (kérdés):** az 1Kir 18:25 (*elohéchem*) és a 18:26 (*ha-Báal*) a *besém* után
nem JHVH-t hordoz. A K4 szó szerint kizárná őket, a K5 viszont kontrasztként megtartja. A 22-es szám
ezt a két sort tartalmazza. Javaslat: a `negativ_kriterium` nevesítse a kivételt („… kivéve a
kontrasztként megtartott 1Kir 18:25–26-ot”). A lapon pedig a K5 szerint ez áll: ott *Elohím*, illetve
*ha-Báal* áll.

**A prózára gyakorolt hatás** (`motivumok/ISTENTISZT-001.md`): kiesik a tagadó forma (Jer 10:25,
Zsolt 79:6, Ézs 64:6), a Zsolt 105:1 / 1Krón 16:8 / Ézs 12:4 párhuzam, a Zak 13:9, a „3. A Róm 10:12”
és a „Róm 10:14” szakasz, valamint a 2Tim 2:22 és az 1Pét 1:17 említése. Ez a próza jelentős átírása.
A szöveget egészében olvasom (K1).
