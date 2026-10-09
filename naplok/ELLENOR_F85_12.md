ELTÉRÉS: 7 tétel

# ELLENOR_F85_12 — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main...claude/tahot-verskulcs` (fókusz: 335dfda8..9fb8dafd = F85.12 [e5c4d122, 32e1c894], F85.13 [60e26e7d], F85.14 [9fb8dafd])

*A `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott, csak olvasott); az orkesztrátor mentette le, rövidítve, érdemben változatlanul. Az 5–7. tétel nem esedékes. A `versbeosztas.py --onteszt`, a `tahot_verskulcs_igazolas.py` és az `egyesit.py --ellenoriz` futtatása nem volt megengedett: ezeknél kódolvasás vagy NEM ELLENŐRIZHETŐ áll. Eljárási jelzés az ellenőrtől: néhány Bash-hívása csövet tartalmazott, mind csak olvasott.*

| pont | eredmény | indok |
|---|---|---|
| (1) heredoc: DT-F85a végállapot | OK, egy pontatlansággal (7. sor) | az e5c4d122 szövegéből kiestek a backtickes fájlnevek („Péld  tábláinak”, „megszűnt  forrást”); a 32e1c894 visszaírta; dupla szóköz a DONTESEK.md DT-F85a soraiban nincs több, a cella vége ép |
| (1) heredoc: commit-üzenetek | OK | mind a 17 F85.x üzenet ép (ékezetek rendben, csonka mondat nincs, backtickes fájlnevet egyik sem tartalmaz, ezért nem is veszíthetett) |
| (1) heredoc: váratlan fájl | OK | a `git log --stat` szerint minden commit csak a vártakat módosította; `f22/versmegfeleltetes.tsv` és `F22_versbeosztas.md` csak az F85.8-ban íródott; a munkafa tiszta |
| (1) heredoc-gyanú az F85.13-ban | **ELTÉRÉS (alacsony)** | `F85_jelentes.md:183`: „kézi tábla 97 +  összevonás-fájl 7” (dupla szóköz, valószínű kiesett token; az ok nem ellenőrizhető) |
| (2) önteszt 6. pont | OK (kódolvasás) | a teszt a nyers listán vizsgálja: a 2Móz-ra nincs szegmens, a `2Móz 36:38` kulcsnak 0 sora van, a `2Móz 35:36` és `2Móz 36:37` megvan; a detektor kódja nem változott; a futás kimenete NEM ELLENŐRIZHETŐ |
| (2) generált f22-kimenetek | OK | `f22/versmegfeleltetes.tsv`, `F22_versbeosztas.md`: csak a 0483fd9f (F85.8) érintette |
| (2) proveniencia-döntés rögzítése | OK | a `parok_*` nem íródott újra (`adat/` diff üres) |
| **(2) / ⛔ `ir`: versbeosztas.py** | **ELTÉRÉS (közepes)** | az e5c4d122 módosította az `eszkozok/karoli_strong/versbeosztas.py`-t (a #22-vel közös eszköz), de a brief `ir` listája nem tartalmazza; a brief diffje csak a `kovetkezo` sort változtatta; a jelentés (244., 235. sor) hamisan állítja, hogy az `ir` bővült |
| (3) DT-F85a jóváhagyás, ellentmondás | OK | a jóváhagyás rögzítve (`manual`, chat, nem lekérdezéssel ellenőrizhető); az ellentmondás megszűnt |
| (3) `F85_kivezetett_sorok.tsv` tartalom | OK | 97 kivezetve + 7 visszakerült + 2 új = 106 sor; a kézi sorok 89 eltolt / 6 nincs_karoli / 2 torol; `versosszevonas.tsv` 9 adatsor |
| **(3) `F85_kivezetett_sorok.tsv` generált fájl átírva** | **ELTÉRÉS (alacsony–közepes)** | a fejléc `# GENERÁLT: eszkozok/tahot_verskulcs_kivezetes.py`; az F85.13 átírta (új `allapot_F85_10_utan` oszlop), a generátor nem változott; a fejléc generátor-proveniencia már nem igaz (CLAUDE.md: generált fájlt ne írj át) |
| (3) számok | OK | 290 → 12 (278 + 12); TAHOT 469 301 sor fejléccel |
| **(3)/(4) maradék számhiba** | **ELTÉRÉS (alacsony)** | a „nem érintett sorok” 462 972 a `split(b'\n')` záró üres elemét is számolja (valós: 462 971); `F85_igazolas.md:13`, `F85_igazolas.tsv:8`, `F85_jelentes.md:190, 229`; a jelentés 167. sora belül ellentmond |
| (3) proveniencia-sorok | OK | `F85_igazolas.md:5` |
| (3) jelentés 12. szakasz | **ELTÉRÉS (alacsony)** | a „Nincs kódváltozás” téves: az F85.13 az `igazolas.py`-t módosította (+20 sor); a „9.5 pont” valójában 10.3 |
| (4) `tokenek.py` `beolvasztott`/`erintett_e` szándék | OK (kódolvasás) | régi alakú sorokra a régi viselkedés; új alakú sorokra a Károli-kulcs védett; a régi `eredeti` címkék már nem védettek |
| (4) mellékhatás a #22 többi könyvére | OK (kódolvasás) | a módosított ág ma nem fut (a detektor-listában csak 12 ÚSZ-sor, a kézi táblában nincs adatsor); csak az igazolás d) pontja futtatja |
| **(4) `erintett_e` elméleti kockázat** | **ELTÉRÉS (alacsony)** | a kizárás nemcsak a `nincs_karoli`-ra hat: egy `eltolt` sor, amelynek `eredeti`-je a `beolvasztott_uj`-ban van, megkettőzhet egy verset; ma elérhetetlen, az önteszt nem fedi |
| (4) Hós/Préd 13.2 összevetés | OK | 34 = 23+11, 39 = 19+20, 47 = 38+9 a TAHOT-ból és a `F85_kulcsvaltas.tsv`-ből igazolva; a többi Hós/Préd kulcs változatlan (kódolvasás); futtatás NEM ELLENŐRIZHETŐ |
| (4) `igazolas.py` n) negatív próba, d) kontroll | OK (kódolvasás) | a viszonyítási alap független (`git show 8ce6e95c~1`), a próba ideiglenes másolaton fut, a repóbeli `versosszevonas.tsv` adatsora nem változott; a d) kontroll a régi és az új kódot megkülönbözteti |
| (5) sértetlenség | OK | `adat/` és `konkordancia/` nulla diff (a TAHOT kivételével); a TAHOT az F85.6 óta nem változott; 38 tábla blobja azonos; `futtat.py`: HIBA-szintű találat nincs |
| Korábbi ELLENOR_F85_8 eltérései | 6/7 javult | maradék: 462 972; új: az `ir`-hiány és a generált fájl átírása |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) ⛔/`ir`:** az F85.12 az `ir`-en kívüli, #22-vel közös `eszkozok/karoli_strong/versbeosztas.py`-t módosította, és a jelentés (244., 235. sor) hamisan állítja, hogy az `ir` bővült.
2. **(alacsony–közepes) Generált fájl:** a `naplok/F85_kivezetett_sorok.tsv` ad hoc átírva, a generátor-proveniencia már nem igaz.
3. **(alacsony) DT-F85a:** a heredoc-javítás után a mondat csak a `parok_*` táblákat nevezi, pedig az igazolás szerint a `szavak_*` proveniencia-sora is eltér.
4. **(alacsony) Szám:** a „nem érintett sorok” 462 972 helyett 462 971.
5. **(alacsony) Kód, elméleti:** a `tokenek.py:210` `erintett_e`-kizárás egy `eltolt` sorra is hat (megkettőzés); ma elérhetetlen, nem fedi önteszt.
6. **(alacsony) Jelentés 12.:** a „Nincs kódváltozás” téves; a „9.5 pont” valójában 10.3.
7. **(alacsony) Valószínű kiesett token:** `F85_jelentes.md:183` („97 +  összevonás-fájl”).
