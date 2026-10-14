# ZSOLT_FELIRAT_SZAMOZAS_M2b_macula.md — a `macula_kk.py` hatásmérése (F91, csak mérés)

*Végrehajtó: claude-sonnet-5-5. Eszköz: `eszkozok/f91_macula_hatasmeres.py` (újrafuttatható, a repóba nem ír). Mért adat.*

Proveniencia: `scope=Macula heber, 475 911 morfémasor | forras=konkordancia/Macula_heber_*.tsv | ts=2026-10-14` · `scope=Károli→MT megfeleltetés, minden ÓSZ-könyv | forras=eszkozok/f17/macula_kk.py + konkordancia/Karoli_versmegfeleltetes.tsv + konkordancia/LXX_versificacios_terkep.tsv | ts=2026-10-14` · A1 előtti A tábla: `git show 8be00828^:konkordancia/Karoli_versmegfeleltetes.tsv`.

## 1. Mit olvas a `macula_kk.py` (`karoli_mt_terkep`)

- A `LXX_versificacios_terkep.tsv`-t **pozíció szerint** (`s[0]` = a vers, `s[1]` = `Heber_vers`, `s[5]` = `Karoli_egyezik_hol`); az oszlop nevét sehol nem használja. A térkép `s[0]` kulcsát **Károli-versként** keresi (`terkep.get((konyv, fej, v))`, ahol a `v` a `Karoli_1908.tsv` verse). A kulcs valójában KJV-kulcs (N-F91a, M0b).
- A `Karoli_versmegfeleltetes.tsv`-ből az `igehely_mt` oszlopot (elsőbbség), KEZI osztálynál az üres `igehely_mt` esetén az `igehely_kjv`-t (`kk_kjv`, csak igazolt KJV = MT fejezetnél). A `KK` az irányadó: ahol az `igehely_mt` ki van töltve, a térkép csak az ütközés-listába (`utkozesek`) kerül, a kimenetet nem befolyásolja.

## 2. Mérés (475 911 morfémasor; 23 079 Károli-vers a megfeleltetésben)

| # | Forgatókönyv | Érintett MT-vers | Érintett Macula-morfémasor | Megjegyzés |
|---|---|---|---|---|
| 0 | a commitolt `Macula_heber_*.tsv` `karoli`/`kk_mod`/`allapot` vs a mostani kód + adat újraszámolva | — | **0 eltérés** | a Macula-fájlok szinkronban vannak a kóddal és a mostani A táblával |
| 1 | **A1 hatása**: az A1 előtti vs a mostani `Karoli_versmegfeleltetes.tsv` (térkép változatlan) | **0** | **0** | az A1 csak az `igehely_kjv`-t javította; a Zsolt-sorok a `macula_kk`-ban `igehely_mt`/identitás útján futnak, a KEZI-`igehely_kjv` ág nem érinti a zsoltárokat. A statisztika is azonos (`kk_mt` 1 713, `kk_kjv` 249, `terkep` 3 690, `identitas` 17 235, particio_osszeg 23 079) |
| 2 | **Átnevezés** `Karoli_igehely` → `KJV_igehely` (DT143, B-oldal) | **0** | **0** | pozíció szerinti olvasás: az oszlopnév nem szerepel a kódban; az értékek nem változnak |
| 3 | **A builder KJV-kulcson illeszt** (`sqlite_epit.py`, DT143) | **0** | **0** | a `sqlite_epit.py` változása a `macula_kk.py`-t nem érinti; a térkép értékei változatlanok |
| 4 | *hipotetikus, nem tervezett*: ha a `macula_kk` a térkép kulcsát KJV-kulcsként kezelné (a KJV→Károli átváltás az A tábla `igehely_kjv`-jéből; 1 131 térképsor kulcsa változna) | **1** (Zsolt 13:1, a felirat) | **6** | a `karoli`/`kk_mod`/`allapot` mindhárom mező változna (üres/`nincs` → `Zsolt 13:1`/`identitas`); minden más Károli-vers kimenete azonos |

A 4. sor mellékhatása: az ütközés-lista (`utkozesek`, diagnosztika, nem kimenet) 1 048 → **82** elemre csökkenne (Zsolt 983 → 17; 1Sám 22, Ézs 20, 1Kir 12, Jón 10, Péld 1 változatlan). Vagyis a mostani ütközés-lista a Zsolt-ban főleg a kulcs-félreértésből áll (nem valódi ütközés), de a kimenetet a KK irányadósága miatt ez nem érinti.

## 3. Következtetés és a megállás-feltétel

A tervezett B-oldali M2 (átnevezés + builder-átkulcsolás, DT143) a Macula-adat **egyetlen értékét sem** változtatja: 0 érintett sor az 1–3. forgatókönyvben (az A1 sem), tehát a hatás nem tartalmi, csak név/mechanika; a `macula_kk.py`-hoz a B-oldali M2 nem nyúl. **Nincs DT145 tétel; a 3. lépés (B-oldali M2) mehet.**

Megjegyzés a későbbire (nem döntés, nem tétel): a `macula_kk.py` térkép-használata a térkép KJV-kulcsa miatt látens félreértést hordoz (4. sor). Ha egy későbbi tétel a `macula_kk.py`-t a térkép helyes (KJV-kulcsú) használatára módosítja, azzal a Zsolt 13:1 felirat 6 Macula-sora változna, és az ütközés-lista megtisztulna; ezt a mostani tétel nem végzi.
