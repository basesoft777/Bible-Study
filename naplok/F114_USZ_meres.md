# F114 — az ÚSZ-oldal mérése (3.1, a DT197 döntés előkészítése)

*2026-10-18 · modell: claude-sonnet-5-5 · ág: `claude/tsk-versszam` · mérőszkript: `eszkozok/tsk_versszam_felmeres.py` (új D. rész)*

A `Karoli_versmegfeleltetes.tsv` csak az ÓSZ-t fedi. Az ÚSZ-ön a mérés a TSK KJV-számozású kulcsait veti össze a Károli 1908 vershalmazával: a KJV-oldal vershalmaza a `KJV_Strongs_teljes.tsv` (eBible, angol számozás), a Károli-oldalé a `Karoli_1908.tsv`. A mérés csak a **létező / hiányzó** verseket fogja; az azonos versszámú, de más tartalmú (átrendezett) verset nem (ellenpélda lent: Jel 13:1).

## Eredmény

| Mérés | Érték |
|---|---|
| ÚSZ-könyv / ÚSZ-vers (KJV, Károli) | 27 / 7 954, 7 954 |
| csak a KJV-ben létező vers | 5: 1Kor 3:23, 2Kor 13:14, ApCsel 19:41, Róm 3:31, Róm 8:39 |
| csak a Károliban létező vers | 5: 3Ján 1:15, Jel 12:18, Luk 6:41, Luk 17:36, Mk 9:43 |
| TSK ÚSZ-forrású sor | 144 329 (7 777 egyedi kulcs) |
| ebből eltérő vershalmazú forráskulcs | 8 kulcs, 186 sor |
| TSK-sor, amelynek ÚSZ-célverse eltérő vershalmazú | 214 sor (8 egyedi célvers) |
| az `adat/elofordulasok.tsv` ÚSZ-versei közül érintett | 0 (grep: az 5+5 vers egyike sem szerepel) |

`proveniencia: scope=TSK ÚSZ-forrású és ÚSZ-célú sorai | forras=TSK_kereszthivatkozasok.tsv+KJV_Strongs_teljes.tsv+Karoli_1908.tsv | n=144329 | ts=2026-10-18`

A két halmaz azonos méretű (7 954), az eltérés 5 hely, tehát az ÚSZ-ön a vershalmaz-eltérés alacsony (kb. 0,13% a forrássoroknál, 0,15% a céloldalon), a motívum-adatban nulla.

## Amit a mérés nem fog meg

- A **Jel 13:1** mindkét halmazban megvan, de nem azonos tartalmú: a Károli Jel 12:18 („És álla a tengernek fövenyére.”) a KJV 13:1 első fele, a Károli 13:1 a KJV 13:1 második fele. A TSK-ban `Jel 13:1` 22, `Jel 12:17` 28 forrássorú, `Jel 12:18` nincs; a vershalmaz-összevetés a 12:18 hiányát mutatja, a 13:1 tartalom-eltolódását nem.
- Ugyanilyen tartalmi eltolódás gyanús a 2Kor 13:12–14 (a Károli 13:13-ig), a 3Ján 1:14–15, a Róm 16 vége és az ApCsel 19:40–41 környékén; ezt szöveg-összevetés nélkül nem lehet igazolni.
- Mérési zaj: a KJV eBible-fájl a Mk 9:43 / Luk 6:41 / Luk 17:36 helyen vershalmazában eltér a Károlitól (valószínűleg összevont vers az eBible-ben, nem valódi versszámeltérés); az 5+5 hely egy része ezért nem biztosan valós eltérés.

## Döntés

DT197 (`DONTESEK.md`): (a) ÚSZ-megfeleltetés elkészítése a dataset-szabályok szerint az itt mért 8+ helyre, vagy (b) kimondott korlát: az átváltó az ÚSZ-ön azonosságot ad, N-F114a nyitott tétel. A döntés előtt az F114.1-et nem kezdem el.
