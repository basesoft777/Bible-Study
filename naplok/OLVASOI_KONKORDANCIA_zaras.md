# Zárójelentés — #76 OLVASOI_KONKORDANCIA, 1. menet (M0 és M1)

*Állapot: a feladat NEM kész, `allapot: megallt`. Ez a menet az M0 (terv) és az M1 (helyi környezet) lépéseit fedi; az M2–M7 hátravan. Ág: `claude/olvasoi-konkordancia` (F76.0–F76.8).*

- **M0:** terv és hat döntés (DT-F76c 🟢, 2026-10-14): Flask, alak ∪ szótári alak, frázis a `token_karoli`-ból, `pardes_nezet` süti csak váltáskor, `systemd-run` korlát a disztribúción belül, helyben a teljes db authorizerrel, nyilvános célgépen szűrt példány. A terv: `naplok/OLVASOI_KONKORDANCIA_M0.md`.
- **M1:** `pardes` WSL-disztribúció (Ubuntu 24.04, `E:\WSL\pardes`), Python 3.12 uv-vel, `pardes.db` a disztribúció saját lemezén, korlátozott indítás (`/statusz` 200). Az M1 zárónaplója az M0 fájl 4.3 szakaszában van. A mért méretek ott állnak (`ext4.vhdx` 2,73 GiB az M1 végén).
- **Szótövező aranyminta 3.12-n:** hibrid v2 súlyozva 99,1%, bájtra azonos a Windowson rögzítettel.
- **Független ellenőr:** `naplok/ELLENOR_F76.md`, 8 eltérés. Javítva: E2, E4–E8. **Nyitott: E1 és E3.**
- **E1 (K4 frissesség) NYITOTT:** a D5 három táblát eltérőnek mért (`vers_szamozas`, `lxx_versszam`, `nave_vers`): a `Karoli_versmegfeleltetes.tsv` (F91.10) és a `LXX_versificacios_terkep.tsv` (F91.12) az építés (`epites_ts=2026-10-13T18:10:45Z`) után módosult. A `pardes.db` a #91 előtti állapot. Újraépítés kell az M5 előtt (`eszkozok/sqlite_epit.py`); ez kívül esik az `ir` mezőn.
- **E3 NYITOTT:** az F79/F92/F95 építő-tesztek nem futottak 3.12-n (a ritka klónban nincs `konkordancia/`); a 3.12 az aranyminta alapján véglegesedett, ez az M0-ban kimondva.
- **Egyeztetett eltérések a briefhez:** Python 3.12 (3.11 helyett), `E:\WSL\pardes` (`D:\WSL\pardes` helyett), frázis-keresés a `token_karoli`-ból.
- **Nyitott döntés a felhasználónak:** ki, mikor és melyik ágon építi újra a `pardes.db`-t. Addig az M2 mehet, de a Zsolt-lapok és a Nave/LXX-versszám blokkok a régi számozást mutatnák.
- **Nem történt meg:** merge, M5–M7, a rootfs letöltési méretének mérése (utólag nem mérhető).
- **Következő:** M2 (alkalmazás), külön `/kovetkezo`-val, ugyanezen az ágon.
