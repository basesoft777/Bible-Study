# Negyedik független ellenőrzés — `F09_SZOTAR_S2_BRIEF.md` (#9)

*Tartomány: `55babf11..ccfe9ae4` (F9.J28–J31); PR merge-base `0d7e9dec`. Ellenőr: `fuggetlen-ellenor`, `claude-opus-5-5` (kért: `opus`). A repóba nem írt; a jelentést az orkesztrátor mentette ide tartalmi változtatás nélkül, rövidítve. Eredmény: **ELTÉRÉS, 4 tétel**. Ténylegesen eltakart veszteséget az ellenőr nem talált.*

## Eltérések súlyossági sorrendben

1. **(közepes) A cellánkénti összevetés több „ismert fajtája” a blokk szerint dönt, nem a változás fajtája szerint** (`eszkozok/render_diff_osztalyoz.py`, `_mezo_kat`), ellentétben a DT-F09g 2026-10-18 (1) pontjával (`DONTESEK.md:266`):
   - `:792-793`: az `5. Szótári` szakaszban a cella bármely cseréje `szerep`. Éles esetek: „Cremer (1895)” → „unfoldingWord …” (`HAMART-001_TORZSCIKK.md:971` ↔ próba `:1141`); a jelmagyarázatból kiesik a `` `kézi (2/b)` `` (élesben `:982`, próbában `:1155`). Mindkettő szándékos, de ugyanígy átmenne például egy „UBS DNTG” → „Mounce” csere is.
   - `:787-788`: az `idezes`/`kolofon` blokkban bármely csere `licenc` (a teszt rögzíti: `teszt_render_diff_osztalyoz.py:80-82`). Éles eset: `(projekt-adat)` → `(minden jog fenntartva)`, 8 fájlban.
   - `:785-786`: a csak számjegyben eltérő cella mindig elfogadott. Átmenne például egy BDB-jelentésszám vagy egy `Zsolt(LXX) 87:11` → `87:12` csere a nem kulcs cellában. Ez konstruált példa, éles előfordulást nem talált.
   - `:765-766`, `:774-777`: az LXX-állapot bármire cserélhető (`egyező` ↔ `eltérő`, `egyező` → `—`; a teszt rögzíti: `:84-85`). Az éles diffben ilyen csere nincs.
2. **(közepes-alacsony) Az (1) lépés nem-None ága cellánkénti összevetés nélkül számol el** (`:580-582`): héber/görög írásjegyes sorban a zárójel-eltérés `kiejtes`, a `_LATIN_ZAROJEL_RE` (`:424`) magyar szót is enged (konstruált példa: `כֹּהֵן (pap)` → `(király)`). Éles előfordulás nincs. A None ág (`:888-892`) rendben.
3. **(alacsony) A `FELHASZNALO_ELFOGADOTT` nem darabszámra kötött** (`:368-407`, `:863-865`): 44 sort 37 kulcs fed le (HODIT-001 5 és TEREMT-001 4 azonos sora egy-egy kulcs). Újrafuttatáskor bármennyi azonos törölt sor elfogadottként menne át. A teszt dict-értékeket számol, nem sorokat.
4. **(alacsony) Elavult dokumentumrészek:**
   - `naplok/SZOTAR_S2_zaras.md:14`: az N-F09h hiányzik a nyitott tételek közül.
   - A `naplok/SZOTAR_S2_ismeretlen.tsv:46` lábléce (`render_diff_osztalyoz.py:1027`) csak a 2026-10-17-i dátumot írja, pedig a 12 sor elfogadása 2026-10-18-i.
   - `naplok/SZOTAR_S2_parositas_minta.md:1`: a cím „3. javító menet”, a tartalom a 4. menetéé.

## Rendben

- A harmadik ellenőrzés 2., 3., 4. és 5. eltérése feloldva; az 1. részben (van cellánkénti összevetés, a None ág túlélés-próbával jár; a fajták tágassága megmaradt).
- Kb. 60 LXX-sor, 15 `5. Szótári` sor, 8 `Teológiai szócikk` sor, 8 jelmagyarázat, 6 összesítés, 8 kizárt-leíró sor, 16 licencsor és a 2Móz 19:6 / 15:5 sorok word-diffje: mind ismert irányú, veszteség nem látszik.
- 44 elfogadott sor, mind törölt irányú; a csoportok 14/2/2/1/6/4/3 és 8/4; a DT-F09g szó szerint tartalmazza a 2026-10-17-i és a 2026-10-18-i döntést; az újrafuttatás megőrzi a `felhasznaloi_besorolas`-t.
- `lekerdez.py karoli "2Móz 19:6"` → „…papok birodalma…” (`scope=range:2Móz 19:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=1 | ts=2026-10-18T07:13Z`).
- A TSK 13 négy helyen azonos; `lekerdez.py tsk "Préd 9:10"` → `Ézs 38,18 Votes=15` (`n=49 | ts=2026-10-18T07:13Z`).
- A zárójelentés 4./4a pontja egyezik a `naplok/SZOTAR_S2_diff.tsv`-vel (`ismeretlen` 0, `felhasznalo_elfogadva` 44); a brief K10 aktuális.
- N-F09h: `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md:232` valós, és a fájl kívül esik a brief `ir` mezőjén.
- K13b üres; CI (`futtat.py`, `[ELLENŐRZŐ]` cím): exit 0, HIBA 0.

## Nem ellenőrizhető

- Az osztályozó újrafuttatása és összevetése a verziózott diff TSV-vel (parancskörön kívül).
- A tesztek, az `ellenoriz.py` és a `feladatok.py ellenoriz` futtatása.
- A 2Móz 15:5 H8415 ↔ „a hullámok” megfeleltetés: a Károli-szöveg mindkét szót tartalmazza, a megfeleltetés mondattani érvet kíván (`manual`).
