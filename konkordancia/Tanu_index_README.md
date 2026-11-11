# Tanúindex — egyházatyai és rabbinikus tanúk metaadat-indexe (F191)

A visszhang-réteg (F183) tanúrétegének helyi, szöveg nélküli keresőtáblái. Cél: a tanú-keresés (melyik atya, melyik rabbinikus
hely tárgyalja a verset) ne motívumonként webes keresés, hanem helyi lekérdezés legyen, és minden későbbi lapon újrahasznosítható.
**A tábla mutató, nem bizonyíték:** a tanúállítás a lapra csak az `adat/visszhang_tanuk.tsv` (F183) kinyerő-táblán át kerül, saját
szavas összefoglalóval, a CLAUDE.md 2. szabálya szerint (keresési találatból nincs közvetlen út a lapra).

## Fájlok

| Fájl | Sor | Tartalom |
|---|---|---|
| `Tanu_atyak_index.tsv` | 97 572 | Károli-alakú igehely-tartomány → atya, év, `mu_id`, `hcf_id` (HCF, a kanonikus 66 könyv) |
| `Tanu_atyak_mu.tsv` | 21 790 | `mu_id` → atya, atya-kategória, kiegészítés, mű (`source_title`), forrás-URL |
| `Tanu_rabbinikus_index.tsv` | 5 259 | Károli-alakú igehely-tartomány → rabbinikus mű + hely (Midrash / Talmud / Mishnah / Tosefta / Targum) |

Mind generált (`# GENERÁLT: eszkozok/tanu_index.py …`), kézzel nem szerkeszthető. Olvasás `split('\t')`, a `#` fejlécsorok kimaradnak.
Üres `igehely_veg` = egy verses tartomány; üres `atvezetes` = egyező. A `szelesseg` a tartomány verszáma: **1 = pontos egyvers**; a 10-nél
szélesebb sorok (259 az atyáknál) fejezet- vagy szakaszszintű megjegyzések, nem vers-tanúk.

### `Tanu_atyak_index.tsv` oszlopai
`igehely_kezdet`, `igehely_veg`, `szelesseg`, `atya` (HCF `father_name`), `ev` (a bejegyzés HCF-éve; eltérhet az atya alapévétől), `mu_id`,
`hcf_id` (a HCF `commentary.id` első 10 karaktere, a kötőjellel együtt; a nyers adatbázisban a sor és az idézet innen keresendő), `atvezetes`.
Az `atya_kategoria` (`Tanu_atyak_mu.tsv`) szűrésre való: a HCF nem csak atyákat tartalmaz (Reformation & Modern, Pseudonymous Works,
Canonical Scriptures, Apocrypha … is), a tanúréteghez a korhoz illő kategóriákat kell kiválasztani.

### `Tanu_rabbinikus_index.tsv` oszlopai
`igehely_kezdet`, `igehely_veg`, `szelesseg`, `kategoria`, `mu` (a Sefaria mű-neve), `darab` (ugyanarra a (tartomány, kategória, mű)-re mutató
kapcsolatok száma), `hely` (a rabbinikus hely(ek), ` ; `-vel elválasztva), `kapcsolat_tipus` (Sefaria `Conection Type`), `atvezetes`.

## Forrás és licenc

**HCF** — `HistoricalChristianFaith/Commentaries-Database`, release `latest`, `commentaries.sqlite` (176 242 688 bájt, sha256
`693e4a906ca77b1b0f2f1cf18010dfcc2abdd1db8905143a68c1b504f971cd82`), a `main` commitja `69f0a1cc368f8cda6f35ecfc2a73d8451ef6e8db` (2026-11-10),
letöltve 2026-11-11. Licenc (a repó `LICENSE`): a kompiláció — mappaszerkezet, fájlnevek, **metaadatok**, szkript — „PUBLIC DOMAIN DEDICATION”;
az idézetszövegek egy része jogvédett művekből való, „fair use” alapon szerepel, a dedikáció ezekre nem terjed ki. A GitHub licencmezője `NOASSERTION`.
**Ezért az index a `txt` (idézet) oszlopot nem tartalmazza; csak metaadat.** A CCEL-szöveg szintén nem kerül a repóba.

**Sefaria links** — `Sefaria-Export` `links/links0.csv … links17.csv` (a nyilvános `gs://sefaria-export/` vödörből, 2026-11-11). Licenc: a Sefaria
fejlesztői oldala (https://developers.sefaria.org/docs/usage-of-our-name-and-logo, „Links License”) szerint a kapcsolat-adatkészlet „CC-BY” (a forrás
verziószámot nem ad meg; a szerkesztő elfogadta CC BY-ként, forrásmegjelöléssel: „Sefaria, CC BY”; DT-F191a, 2026-11-11; `adat/licencek.tsv`: tisztázott). A `Sefaria-Export/LICENSE.md` csak a szövegekről szól (szövegenként külön licenc);
**a Sefaria-szövegek nincsenek az indexben.** Forrásmegjelölés: Sefaria.org; a változás jelzése: szűrés és Károli-átvezetés.

| Nyers fájl | sha256 |
|---|---|
| `links0.csv` | `6cad6cf262b0d1570e5d054580f9c79ac71cb134f26308f268b184b3c60ec724` |
| `links1.csv` | `3458162e147b642c40dbe4948b7c270776d773ee9a8d110fa47b388b7039484a` |
| `links2.csv` | `fd04427884a5165d75ff7ed7eb9cd434af040459948c2a3a2a59b76634e6d82d` |
| `links3.csv` | `8085156cd3b756a6de199d46574eb4094ccde75eb6261021f25aef730b9d7ea3` |
| `links4.csv` | `f65e5489a6a1ae1888c338ae17f315e36b2051140a75f8f14a5c4da646c2ed56` |
| `links5.csv` | `949539ae0edcf06d582f4493b884cc965c09b4fbb345ad5dce58be4f125920ec` |
| `links6.csv` | `c1b37c592021bcea07569e72de25d88d35c463bf34dec30a3898083576a9649d` |
| `links7.csv` | `21fb57f9b2512e0281925e41f4d695c22edf35732f993e37469447c86f24261d` |
| `links8.csv` | `23d03b99e3565eb53f4d71e6c6219151f9f5db665ddffd01cf811c006fcc3360` |
| `links9.csv` | `7cc5f483686313505444f53345799f5502165d1f685fa75232511c897c716d6b` |
| `links10.csv` | `1827a03809e4b2353f5f3ffa9e4cd11686eadfe1420177293311b9de92eec977` |
| `links11.csv` | `6282c6c7c388aaad04ec33304e612497a808d1ae665406ece0ecedc2431f9c95` |
| `links12.csv` | `e1d45ec0d80dda3678fc9788df04c6f4eb5f71a60713e96dde5f0c93cfd07c34` |
| `links13.csv` | `2793510a3578aff3fe09d88b0f597bf550ace56b61bd8edbf58722fc7cadbcc2` |
| `links14.csv` | `496184eb19f0cb14169d3a4e4056d6d92877f8e789808edc8fb50bdddfd1ae4d` |
| `links15.csv` | `f8d63b4852f141980f5ddbbce8be92ab4bb94fae522e0b37c0c7cfbdbcc07946` |
| `links16.csv` | `bc1fb3a0b9721389dcdebd8e6ef1ee00eccf878378aa4107eb8e744803f2678d` |
| `links17.csv` | `0ed5d3559f5e621dbf426685cac93d1b58669e482fab38a1e98b4a51a6ddcffc` |

A nyers fájlok a repón kívül vannak (`D:\pardes_tanu\hcf\`, `D:\pardes_tanu\sefaria\`), mert a licenc (HCF) vagy a méret (Sefaria ~680 MB) nem engedi a
repóba tételt (Rendszerfejlesztesi_playbook 2. pont, „Nyers forrás megőrzése”: a hash itt rögzítve, a konverziós szkript a repóban).

## Átvezetés és a veszteséges konverzió naplója

- **Számozás.** A HCF az angol (KJV) számozást, a Sefaria a masszoretikus (MT) számozást használja; a Károli-számra a `Karoli_versmegfeleltetes.tsv`
  `igehely_kjv`, illetve `igehely_mt` oszlopa vezet át (a tartomány eleje és vége külön). `atvezetes`: `egyezo` (üres) | `tabla` (a szám változott) |
  `tabla_hianyzik` (OT-vers, amely a táblában nincs: az azonos szám marad; 2 sor az atyáknál, 5 a rabbinikusnál) | `nt_feltetelezett`
  (az UT-re nincs átvezető tábla: azonos szám feltételezve, 63 972 sor; az UT néhány ismert eltérése kézzel ellenőrizendő).
- **Eldobva (HCF):** a Google Books-URL `dq=`/`q=` paramétere (idézetszöveget hordoz); a `txt` (idézet); a `file_name`; 2 043 sor az apokrif könyvekből (Wisdom, Sirach, Tobit, 1–2 Maccabees, Baruch, Prayer of Azariah,
  Judith — nincs Károli-megfelelő); 2 fordított tartományú sor; **107 sor, amelynek (átvezetés utáni) kezdőverse nem létezik a Károlinál** — a görög Dániel/Eszter-kiegészítések (Dán 13–14, Eszt 10:6, 15:13…) és a Károli-számozástól eltérő versek (pl. KJV Jób 38:39–41 = Károli Jób 39:1–3, mert a versmegfeleltetés ezeket nem tartalmazza) — ezek nem kaphatnak hamis Károli-kulcsot, ezért kimaradtak (`nincs_karoli_vers`). Ehhez jön: a 0. vers az 1. versre, a `≥999`/üres vég a fejezet utolsó versére írva; az átvezetés után megfordult tartomány egy versesre zsugorodik. A `append_to_author_name` a `Tanu_atyak_mu.tsv` `atya_kiegeszites` oszlopában marad.
  261 mű-sor `source_title` nélküli, 9 204 `source_url` nélküli: üresen maradt (a hiányt nem töltjük ki).
- **Eldobva (Sefaria):** minden szöveg; minden nem rabbinikus kategória (Tanakh–Tanakh keresztkapcsolatok, Reference, Jewish Thought, Chasidut, Halakhah,
  Kabbalah, Musar, Liturgy, Responsa, Second Temple); a **középkori Tanakh-kommentárok** (Rashi, Ramban, Ibn Ezra …: Tanakh–Tanakh típusú kapcsolatok, nem
  rabbinikus-kategóriájúak); a Tanakh-oldalon nem csupasz könyvnevű sorok (kommentár-kapcsolatok); 40 fejezetszintű ref nem értelmezhető (Lamentations 1–5: a siralmak fejezetszintű refje a verszámlálás hiánya miatt nem bontható; a fejezet végét az MT-fejezet hossza adja, nem a Károlié). A 7-től eltérő oszlopszámú Sefaria-sorok és a nem egyértelmű `targum`-sorok számlálás nélkül kimaradnak; az azonos (tartomány, mű, ref) hármas egyszer szerepel (a duplikátumok száma a futás kimenetén áll, a fejlécben nem).
- **Csoportosítás (Sefaria):** a (tartomány, kategória, mű, kapcsolat-típus) azonos sorai egyetlen sorba kerülnek; a `darab` a számot, a `hely` az összes refet mutatja.
- **A Sefaria-kategóriák nem tiszta „rabbinikus” kategóriák:** a `Talmud` és a `Mishnah` kategória kései kommentárokat is tartalmaz (Steinsaltz, Ben Yehoyada, Nachalat Avot, Hartman-jegyzetek …; a `mu` oszlopban „ on ”-t tartalmazó nevek). Pl. az 1Móz 4:7 „Mishnah” sorai mind kommentárok. A lapra kerülő tanúhoz a `mu` ellenőrzendő; az `mu`-ban „ on ” szerkezet = kommentár a műhöz.
- **Targum:** a Sefaria `targum` típusú kapcsolatából (mindkét oldal Tanakh-kategóriájú); a Tanakh-oldal a csupasz könyvnév.

## Hatókör

- **Atyák:** a teljes Károli-kanon (66 könyv), 97 572 sor, 6,1 + 3,4 MB.
- **Rabbinikus:** a teljes Tanakh 254 250 sor / ~24 MB lenne, ez a „pár MB”-nál sokkal több, ezért az első körben **csak a lexikonmotívumok igehelyeivel
  átfedő sorok** (`adat/elofordulasok.tsv`, 289 vers; 5 259 sor, 0,5 MB). Új motívum vagy új vers esetén újragenerálás (a nyers adat a `D:\pardes_tanu\`-n),
  vagy a teljes változat (`--teljes`, N-F191a).

## Újragenerálás

```bash
python -I eszkozok/tanu_index.py epit-atyak --sqlite D:/pardes_tanu/hcf/commentaries.sqlite
python -I eszkozok/tanu_index.py epit-rabb --links-mappa D:/pardes_tanu/sefaria
python -I eszkozok/tanu_index.py keres "1Móz 3:17" --max-szelesseg 10
python -I eszkozok/tanu_index.py minta
python eszkozok/teszt_tanu_index.py
```

(`epit-rabb --teljes`: a teljes Tanakh.) A HCF `latest` kiadás havonta frissül: újraépítéskor a `commentaries.sqlite` sha256-ja változik, a fejléc és a
`licencek.tsv` sora is frissítendő.

## HAMART-minta (2026-11-11)

A `python eszkozok/tanu_index.py minta` kimenete (pontos egyvers / a verset fedő, legfeljebb 10 verses tartomány):

| Vers | atya (pontos) | atya (fedő ≤10) | rabbinikus hely (pontos) | rabbinikus (fedő ≤10) |
|---|---|---|---|---|
| 1Móz 3:17 | 8 | 16 | 48 sor / 46 mű (Midrash 38, Talmud 7, Targum 3) | 54 sor / 48 mű |
| 1Móz 4:7 | 4 | 7 | 48 sor / 47 mű (Midrash 22, Mishnah 2, Talmud 20, Targum 4) | 49 sor / 47 mű |
| 1Móz 4:11 | 2 | 5 | 9 sor / 9 mű (Midrash 6, Targum 3) | 10 sor / 10 mű |
| 1Móz 6:5 | 2 | 5 | 54 sor / 54 mű (Midrash 26, Mishnah 7, Talmud 16, Targum 3, Tosefta 4) | 58 sor / 55 mű |
| 1Móz 6:11 | 1 | 1 | 16 sor / 16 mű (Midrash 7, Mishnah 2, Talmud 3, Targum 4) | 16 sor / 16 mű |

Az atyai pontos darabszámok egyeznek a tanúforrás-felmérés (2026-11-11) kézi mérésével (8 / 4 / 2 / 2 / 1).

## Korlátok

- A HCF egy-egy atyához gyakran csak egy részletet vesz fel (`source_title` üres is lehet); az index a HCF lefedettségét tükrözi, nem az atyák teljes művét. Üres eredmény nem negatív lelet.
- A rabbinikus oszlop a Sefaria kapcsolat-adatán alapul: egy kapcsolat nem jelent azonos értelmezést, csak azt, hogy a hely a verset idézi vagy tárgyalja.
- **Nem tartalmaz:** Glossa Ordinaria (Genesishez nincs szabad forrás; N-F176a), Vulgata/LXX (az F183 más tábla), Chain Lineages / BiblIndex (licenc nélkül), earlychurchtexts.com.
