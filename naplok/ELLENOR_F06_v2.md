# ELLENOR_F06_v2 — F06_FORRASFELMERES_BRIEF.md · `origin/main..92b283d` (16 commit, 62 fájl)

*Újraellenőrzés az F06.6 (`e8ff0f1`), F06.7 (`91a3aca`), F06.8 (`92b283d`) után. Készítette a `fuggetlen-ellenor`; a fájlba az orkesztrátor mentette (az ellenőrnek nincs Write-eszköze). Eljárási megjegyzés: `git fetch` nem futott; az `F06_5_osszesito.py`-t az ellenőr nem futtatta, a #8 számait a TSV 87 sorának kézi átszámolásával ellenőrizte.*

**Összegzés: ELTÉRÉS, 3 új, kisebb tétel. Az előző jelentés (`ELLENOR_F06.md`) mind a 7 pontja lezárult.**

## (a) Az előző 13 eltérés állapota

| Eltérés | Állapot | Igazolás |
|---|---|---|
| 1a `GOROG_NELKUL` leírása | **lezárva** | `F06_forras_jelentes.md:62`: görög Strong nincs; 27 sorban van görög szóalak, 11-ben nincs. A TSV-ből újraszámolva: 38 sor; az üres/`-`/`’’` görög mező 11 soron (8, 11, 23, 50, 57, 59, 60, 62, 63, 66, 91) |
| 1b `NINCS_A_VERSBEN` | **lezárva** | `:63-64`: „nem volt mit keresni”; a TSV 20., 45–49., 79–80. sora: kulcsszó `—`, Strong üres; a 2 `NINCS_VERS` az 52. és 88. sor (4Móz 13:34) |
| 2 CI E16 | **nyitott az ellenőr szerint, de az orkesztrátor igazolta:** a PR címe `[ELLENŐRZŐ]` előtagú, `gh pr checks 75` → `ellenorzes pass` | az ellenőr a PR-állapotot nem tudta lekérni |
| 3a–3e idézetek (kjvstudy ISC, 1John419 GPL, scripture-intelligence MIT, luvlylavnder, KJV-Strongs-EBook saját olvasat) | **lezárva** | mind szó szerint megvan a `F06_licenc.tsv` idézet-mezőjében és a `F06_licenc_szovegek/` fájlokban |
| 4 kennethreitz ellentmondás | **lezárva** (kisebb pontatlansággal, lásd új 2) | `F06_kjv_asv.tsv:35-38`; `kjv_asv.py:211-212`: az `igen`-t a `pelda` váltotta ki |
| 5 „minden szám F06-kimenetből” | **lezárva** | FJ-forrású számok külön jelölve; a „900 mp” kikerült (a TSV `420 mp`-et mutat) |
| 6a–6d Macula versszám-ok, „nem letöltési hiba”, „licenc rendben”, 2895 „tövesítés” | **lezárva** | hipotézisként/jelölve; SDBH „Used with permission” (`macula_hebrew__LICENSE.md.txt:21`) |
| 7a költségfejléc | **lezárva** | 0,011926 vs. 0,011927 megnevezve, a sorösszeg mérvadó |
| 7b javaslat-kategóriák | **részben** (scrollmapper, lásd új 3) | studybible.info: NEM |
| 7c elavult állapotsor `F06_felmeres.md:68` | **lezárva** | |
| „Nem ellenőrizhető”: zárás | **lezárva** | `F06_zaras.md` 13 sor; `FELADATOK.md:15` frissítve |
| „Nem ellenőrizhető”: költség (36606454914), ⛔ válasz | **nyitott, változatlan** | a repóból nem igazolható |

## (b) Érintette-e a javítás a BSB-/Macula-számítást?

**Nem.** `git diff --stat 1cae02b 92b283d`: 7 fájl, mind `naplok/*.md`, `F06_5_osszesito.*` vagy `FELADATOK.md`. Az `eszkozok/`, `.github/`, `F06_bsb_*`, `F06_macula_*`, `F06_nave.tsv`, `F06_kjv_asv.tsv`, `F06_licenc.tsv`, `F06_koltseg.tsv`, `F06_licenc_szovegek/`, `adat/`, `konkordancia/`, `lexikon/` diffje üres. Az `F06_5_osszesito.py` változása +17/−0, csak `print` és számlálás, két olvasó `open` van benne, írás és hálózat nincs. **A mérés újrafuttatása nem szükséges.**

## (c) Idézetek és #8 számok

Az eBible-, basokant- és elcafe7-idézetek szó szerint egyeznek (az elcafe7 `LICENSING.md`-ben a „nave” 0 találat, tehát a „Nave-et nem” állítás igaz). A #8 számai a TSV-ből: `LXX_MEGFELELO` 39 (37 `strong` + 2 `szoalak`), `GOROG_NELKUL` 38 = 27 + 11, `NINCS_A_VERSBEN` 8, `NINCS_VERS` 2; összesen 87.

## (d) N27 és N29 kulcsszámok — a jelentés egyezik a TSV-kkel

- **N27 Nave:** `basokant/nave` 5322 lista, `nave.txt` 4 565 849; `theonize` 32 253 sor, 4980 Topic, 92 609 reláció (mind leképezhető, nem leképezhető 0); `elcafe7` 5319, 40 089, 40 088, 1.
- **N29 KJV/ASV:** eBible KJV 66 könyv, 31 102 vers, 31 099 Strong-címkés (zip: 81 könyv); ASV 66/31 102/30 978; `luvlylavnder` KJV 31 102/31 102, ASV 31 086/31 086; KJV-Strongs-EBook `lemma_strong=355850`; keresés 10/0/2/0; scrollmapper 420 mp időkorlát.

## Új eltérések (kisebb)

1. **A „27 görög szóalak” definíciója** (`F06_macula_87_hely.tsv:71`; `F06_forras_jelentes.md:62`): az Ézs 26:19 sorának görög mezője `"{δ}"`, ez jelölő, nem szóalak, de az összesítő `JEL_URES = ('', '-', '’’')` szóalaknak számolja. Kizárva 26/12 lenne. **A #8 bemenetét érinti.**
2. **kennethreitz „Genezis 1:1 mintapélda”** (`F06_forras_jelentes.md:29`): a `F06_kjv_asv.tsv:37` `genezis_1_1_pelda` mezője Jn 1:1-et idéz. A következtetés helyes, a leírás pontatlan.
3. **scrollmapper „NEM”** (`F06_forras_jelentes.md:33`): a cellában „nincs minősítés” áll, tehát a NEM nem mérésen vagy licencen alapul; önellentmondó címke.

## Nem ellenőrizhető az ellenőrnek

A PR #75 CI-állapota: az ellenőr helyi futtatása cím nélkül E16 HIBÁ-t, `[ELLENŐRZŐ]` előtagú címmel 0 találatot ad. (Az orkesztrátor a tényleges állapotot lekérte: `ellenorzes pass`.)

## Javítás (F06.10)

*Az ellenőri jelentés fenti része rögzített, nem módosult; ez a szakasz a három új eltérés javítását rögzíti.*

1. **Görög szóalak száma:** az összesítő szűrője (`naplok/F06_5_osszesito.py`) most csak azt tekinti szóalaknak, ami görög betűt tartalmaz, és nem `{…}` alakú jelölő (az idézőjelek lecsípése után; a TSV-ben a jelölő `"{δ}"` alakban áll). Újraszámolva a `F06_macula_87_hely.tsv`-ből (38 `HEBER_SZO_GOROG_NELKUL` sor): **26 sorban van valódi görög szóalak, 12-ben nincs** (a kizárt értékek: `"{δ}"`, `-`, `’’`; a `{…}` jelölőt tartalmazó sor 1, az Ézs 26:19). A TSV-ben szóalak-szám nem tárolt, ezért az `F06_macula_87_hely.tsv` nem módosult. Frissítve: `F06_forras_jelentes.md`, `F06_zaras.md`, `F06_5_osszesito.txt`.
2. **kennethreitz:** a jelentés leírása pontosítva: a `kjvstudy_org/` könyvtárnév miatt minősült KJV/ASV-nek; a `word_studies.json` mintapéldája Jn 1:1, a két HTML-sablon mintája Genezis 1:1. A következtetés (nincs tömeges címkézés) változatlan.
3. **scrollmapper:** a címke „NEM MÉRT (időkorlát)”; a `F06_zaras.md` „Egyeztetett eltérés”-ként rögzíti.

A mérés nem futott újra, a workflow nem indult (`eszkozok/fj2/**` és `futtatas.txt` érintetlen).
