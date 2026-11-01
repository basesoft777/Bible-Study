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
