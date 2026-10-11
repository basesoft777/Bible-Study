# Független ellenőrzés — F63_JELOLTEK_RETRO_BRIEF.md · `origin/main..HEAD` (HEAD `cba45bd7`, F63.11)

*A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette fájlba (az ellenőrnek nem volt fájlíró eszköze; `git fetch` sem futott nála, a helyi `origin/main` refet használta). Eredmény: **ELTÉRÉS: 9 tétel**. Az ellenőr nem javított semmit. Az ellenőrzött sorok a jelentés idején 22 forrás-visszakeresést fedtek le.*

## Pontonkénti eredmény

| pont | eredmény | indok |
|---|---|---|
| jeloltek 344 → 588, csak hozzáadás | OK | `numstat 244 0`; a 344→588 fizikai sor (adatsorban 342 → 586, Δ +244); törölt/módosított sor 0 |
| más adat/*.tsv érintetlen | OK | csak a `jeloltek.tsv`; az adatot író commit egyedül az F63.5 |
| proveniencia, dontes, indoklas, datum | OK | 244/244 sor; `elutasítva` 236, `nyitva` 8 (HAMART 7, KIRALY 1); kulcsütközés nincs |
| visszakeresés a forrásban (22 sor) | OK, 3 kivétellel | HAMART, ISTENTISZT, KIRALY, ALVIL, HODIT, MENNY, TEREMT sorok igehelye és döntése egyezik a naplóval |
| HAMART 170 sor teljessége | OK | 4/b 97 + 2 + 4/c 71 = 170 |
| ISTENTISZT 60 sor tartománybontása | OK | összeszámolva 60; a „többi 37 TSK-találat” helyesen nem lett sor |
| 3 ellentmondásos sor `nyitva`, N-F63a; 1Móz 11:4 nincs | OK | 2Pét 3:10, 3:12, 1Pét 2:9 csak `nyitva` sorként; `kollokacio G0934 G2406` → 1Pét 2:9 |
| K2 | OK | csak `elutasítva`/`nyitva` |
| K4 | OK (elfogadott eltérés) | DT95 (5), DT96 |
| ANTROP-001: 3 ★ | OK | Fil 1:27 (`nyitva`), 1Pét 1:22, Mt 12:18; `kollokacio G4151 G5590` → 6 vers |
| zajos motívumnál nincs lelet-lap; teljességi látszat | OK | az F63.11 kimondja a HAMART és a MENNY 0 értékének jelentését |
| zárás ↔ mérés számai | OK | HAMART 0/526/501, ISTENTISZT 17/156, KIRALY 6/631, MENNY 0/269 |
| `scan_halmaz` futáskori levezetés; auditok.tsv; hozzafuz alapból száraz; csv | OK | `split('\t')`, nincs `csv`; `auditok.tsv` 0 |
| D v1 #1–#2, A1, A2, A4, A6, nulla-diff hatóköre, táblasor-Δ | OK | `jeloltek.tsv` +244, minden más 0 |
| gate.py, ellenoriz.py, teszt_nem_vizsgalt.py | nem ellenőrizhető | az ellenőr szerepkörében nem futtathatók |
| ⛔ M0 / M2 betartása | nem ellenőrizhető | a DT96/c döntője „Felhasználó (a külső session döntéseit előre elfogadta)”; javasolt a felhasználó közvetlen megerősítése |

## Eltérések súlyossági sorrendben

1. **K3, CI piros (magas):** `ellenorzes/futtat.py --valtozott` → **E9 HIBA 1**, `DONTESEK.md:172` (DT97): angol „sense”. A `naplok/F63_zaras.md` „ellenoriz.py zöld” állítása nem áll; a K5 nem teljesülhet.
2. **KIRALY-001, 6 hiányzó elutasított jelölt (közepes):** 2Móz 2:16, 3:1, 18:1; 2Sám 8:18; 1Kir 4:5; 2Sám 20:26 (`Melkizedek_…naplo.md:29,44`, BDB „chieftain”). Az M0 csak a minősítő tábla első celláját mérte. A H3548-kör tagjai (`scan H3548 --szakasz "2Móz 2:16"` n=1).
3. **`nem_vizsgalt.py` kézi listák (alacsony):** a `CSOPORTOS_KIZARAS` táblán kívüli Strongot (G2672) is a scanbe tesz; az F63.11 megjegyzése szerint a H2403 „táblából nem kiolvasható”, pedig kiolvasható (`elofordulasok.tsv:211`), az `EXTRA` H2403 redundáns. A `KOLLOKACIO_TAGOK` sehol nincs használva.
4. **Egy logika (alacsony):** a „tematikus horgony” a `lista` kimenetéből kimarad (a `jelentes()` nem írja ki); a mérés a `H5315+H2416`-ot „[normál]”-nak címkézi (DT96 nevesített kategóriát kér).
5. **A5/K1 (alacsony):** a KIRALY 1Móz 14:22–23 sorok a Kenneth Copeland (nevesített tanító) sorából jöttek (`Melkizedek_…naplo.md:33,47`), a `forras_kereses` ezt nem jelzi.
6. **M1 (alacsony):** egy commit (F63.5) fűzi hozzá mind a 244 sort, nem motívumonként; a DT95 (6) egyszeri hozzáfűzést hagyott jóvá.
7. **M3 (alacsony):** a zárás fájlneve (`F63_zaras.md`) eltér a brieftől (`JELOLTEK_RETRO_zaras.md`).
8. **A3 (alacsony):** a 2Pét 3:10/12 `nyitva` indoklásából kimaradt a napló „tematikus, nem lexikai” jelölése (`jeloltek.tsv:515–516`; napló `:179`).
9. **ISTENTISZT 1Pét 1:6–7 (alacsony):** az indoklás értelemváltoztató rövidítés (`jeloltek.tsv:533–534`; napló `:61`): a napló szerint a formulát a Jóel 2:32, ApCsel 2:21 és Róm 10:14 *mellett* egyedül a Róm 10:12 hozza.

## Megjegyzések

- Kétpontos diffben (`origin/main..HEAD`) a Neh-táblák törlésnek látszanak: ez az ág elavultságának műterméke (a #275 Neh-merge a leágazás után történt). A merge-base-zel az E5 = 0. Merge előtt érdemes a main-t beolvasztani.
- Nem ellenőrizhető maradt: gate.py, ellenoriz.py, teszt, CI-jelentéssel való egyezés, a ⛔ pontok betartása a repóból.
