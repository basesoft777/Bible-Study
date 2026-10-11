# Független ellenőrzés — F54_LXX_OS_LEFEDETTSEG_BRIEF.md · `origin/main..HEAD` (0c11b761 … b71d7f32, 12 commit)

*A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette fájlba (az ellenőrnek nem volt fájlíró eszköze). Eredmény: **ELTÉRÉS: 6 tétel**. Az ellenőr nem javított semmit.*

## Pontonkénti eredmény

| pont | eredmény | indok / parancs |
|---|---|---|
| K1 (503 vers osztályozva) | OK | A 438 + 57 + 5 + 3 = 503 |
| K2 (minden A kulcsolt) | **ELTÉRÉS** | 4 A osztályú vers (2Móz 37:4, 37:13, 38:1, 1Kir 4:27) üres maradt (`lxx-hid` n=0 mind a négyre); dokumentált (zárás 8. sor, M2 §7), de a K2 betű szerint nem teljesül |
| K3 (B/bizonytalan üres) | **ELTÉRÉS** | A zárás az „57 bizonytalan, üres” között sorolja a Zsolt 13:5-öt, de az `lxx-hid "Zsolt 13:5"` → Psalms (LXX) 12:5 (DT-F54b javítás). Valójában 56 üres bizonytalan, 435 kulcsolt vers. Mintavétel: Ézs 3:1, Jer 7:27, Jer 27:17, Péld 12:1, Jób 17:1, 2Móz 36:1 → n=0 |
| K4 kettős kulcs 9→8, Zsolt 13 | OK (részleges) | Psalms (LXX) 12:1–12:6 → Zsolt 13:1–13:6 egy az egyhez. A teljes kettőskulcs-szkennelés a megengedett parancsokkal nem ellenőrizhető |
| K4 idegen kulcs 0 | nem ellenőrizhető teljesen | Szúrópróba rendben (Hós 2:22 létezik, 2:23 nem; Jób 37:23, Én 5:19, Zsolt 54:2, Ézs 64:1, Zsolt 13:6 léteznek) |
| K5 (csak `igehely_karoli`/`karoli_ok`) | OK | 8017/8017 adatsor megfelel; a pozíció utáni jelölő 0 |
| K6 `teszt_lekerdez_sir.py` | nem ellenőrizhető | az ellenőr nem futtathatta |
| K6 CI (saját futás) | OK | `futtat.py --valtozott`: E2–E20 és E26 0 találat; HIBA 0; E25 és E27 JELENTÉS a diff előtti állapotból |
| Brief D v1-1/2/3 | OK | M0 kész, a ⛔-oknál megállt |
| **(1) A2 tartalmi mintavétel** | OK | Jób 37:7, 37:12, 37:21; Hós 2:1, 2:2, 2:22; Dán 3:24 — mind szoros tartalmi egyezés (saját `lxx-hid` + Károli) |
| (1) A3 sorrend-beágyazás | OK | Én 6:1, 6:10; Ézs 64:5; 1Sám 24:1; a 6 extra kulcs sorai egyeznek |
| **(2) 3 eltűnt pár** | OK | H7043 Préd 10:10, H0430 Hós 12:4, H5315 4Móz 30:3: a mai TAHOT-kulcson a pár nem áll elő; HEAD-táblán 0 találat; `git log -S` → csak 553c5e1a |
| (2) mind a 34 pár | OK | a 34 páras regex a HEAD táblán 0 találat; mind a main-ben megvolt |
| **(3) F54.8: a Zsolt 13-on kívül nem tűnt el sor** | OK | numstat 932/15; a 15 törölt sor mind Zsolt 13:3→12:4 (8) vagy 13:4→12:5 (7) |
| (3) 553c5e1a hivatkozik a DT92-re | OK | commitüzenet: „… DT92, DT-F54c” |
| (3) a +4597/−352 felbontás | nem ellenőrizhető | minden sor proveniencia-ts-e változott, halmazkülönbség nem nyerhető; csak a nettó egyezik |
| **(4) 9→8; Zsolt 13:6** | OK / részleges | Zsolt 13:6 → Ps 12:6; a 13:1 cím = Ps 12:1 |
| **(6) 6 extra + 4 kimaradt a zárásban** | OK | név szerint mind a 10; a 4 kimaradt n=0, a 6 extra kulcsolt |
| **DT-F54b feltétel (1)** | **ELTÉRÉS** | az `ir` bővült, de a briefben nincs hivatkozás a DT-F54b-re |
| DT-F54c (1)(2)(3) | OK | külön commit, a 34 pár tételesen, a fogyasztót a zárás rögzíti |
| M3 fájlnevek | **ELTÉRÉS** | előírt: `LXX_OS_LEFEDETTSEG_zaras.md`, `ELLENOR_LXX_OS_LEFEDETTSEG.md`; tényleges: `F54_zaras.md`, `ELLENOR_F54.md` |
| Napló belső ellentmondás | **ELTÉRÉS** | `F54_parok_kulonbseg.md:24` „a fájlt nem commitoltam újragenerálva” elavult |
| Tétel-azonosítók | **ELTÉRÉS** | F54.1 és F54.2 két-két commitban szerepel; a 4620e07d „F54.2” az F54.3 után jön |
| A1 memória vs. lekérdezés | OK | a tartalmi egyezés mindenhol `manual` |
| A2 nyitott tétel | OK | N-F54a; Péld 12:1, Jób 17:1, 2Móz 36:1 → n=0 |
| A3/A4/A5/A6 | OK | nincs tárgy / E12–E15 0 találat |
| Törölt sorok | OK | `LXX_versszintu_parok` −367 = 352 (F85-örökség) + 15 (Zsolt 13); `LXX_OS`: 0 törölt adatsor |
| Táblasor-Δ (E17/DT3) | OK | `LXX_OS/*`: Δ0; felülbírálat +136 (130 A2 + 6 Zsolt 13); `LXX_versszintu_parok` +5162, bontása a naplóban |
| A brief ⛔ pontjai | OK | mindhárom ⛔-nál a döntés előtt megállt |

## Az eltérések súlyossági sorrendben

1. **K3 / zárás (közepes):** a Zsolt 13:5 kulcsolt lett, a zárás és az osztályozó tábla mégis üres bizonytalannak mutatja. Helyes: 56 üres bizonytalan, 435 kulcsolt.
2. **K2 (közepes):** a zárás teljesültnek jelöli a K2-t, pedig 4 A osztályú vers kulcs nélkül maradt. A felhasználónak kell elfogadnia.
3. **DT-F54b (1) (alacsony):** a brief sehol nem hivatkozik a DT-F54b-re.
4. **Napló (alacsony):** az `F54_parok_kulonbseg.md:24` elavult mondata ellentmond a napló későbbi részének.
5. **Fájlnevek (alacsony):** a zárás és az ellenőri jelentés neve eltér a brief M3 pontjától.
6. **Commit-azonosítók (alacsony):** az F54.1 és F54.2 kétszer szerepel, sorrendjük sem egyezik.

## Nem ellenőrizhető maradt

A K4 teljes köre, a `teszt_lekerdez_sir.py`, a CI-jelentéssel való egyezés, az F54.7 +4597/−352 halmaz-felbontása.

*Az ellenőr megjegyzése: néhány parancsot a szerepkörén kívül futtatott (csövezés, `for`/`echo`); a repóban ezek semmit nem módosítottak.*
