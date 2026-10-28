# Kiegészítés: a nyitott pontok lezárása

Gyűjtés: 2026-10-27, a `weboldalak.md` és az `alkalmazasok.md` után. Nyers letöltések: `/tmp/claude-0/-home-user-Bible-Study/40fb57d0-f061-5709-acdb-32b11a763cea/scratchpad/forras/web2/` (a GitHub-fájlok a `gh/`, a CrossWire-fájlok a `crosswire/` alkönyvtárban).

**Jelölés** (ugyanaz, mint a két korábbi jegyzetben):
- **[L]**: letöltöttem és elolvastam, a megállapítás a mentett fájlból visszakereshető.
- **[S]**: csak keresőkivonat (WebSearch), az oldalt nem láttam.
- **[P21] / [P22]**: M. Pintér (2021) vagy Pintér–Márkus (2022) állítása. A cikket [L] olvastam, de a leírt eszközállapot **2021-es, illetve 2022-es**, ma nem ellenőrzött.
- **[K]**: saját következtetés [L] adatból. Nem közvetlen állítás.
- **?**: nincs adat. Nem töltöttem ki feltételezéssel.

**Ezúttal sem kerültem meg semmit.** Az ebo.kre.hu és a btk.kre.hu a proxyn 403-at adott (egy-egy kísérlet). A szit.hu egyetlen udvarias kérésre 429-et adott, ezért kihagytam. A github.com HTML-oldalai és a `gh api` nem voltak elérhetők (403, „not enabled for this session”), a GitHub MCP keresője, kódkeresője és a raw.githubusercontent.com viszont igen. A biblia.hit.hu, az online-biblia.ro, a polarhome.com/biblia, az okosbiblia.hu, a biblegateway.com és a bibles.org a proxyn nem nyílt meg (000), ezért élő állapotukat nem ellenőriztem. A doi.org 403-at adott, a cikket a KRE-repozitórium REST API-ján értem el.

---

## 1. A két áttekintő cikk

### 1.1 M. Pintér Tibor (2021): Online segédletek a magyar nyelvű bibliafordítások olvasásához. *Modern Nyelvoktatás* 27/3–4, 43–57. DOI 10.51139/monye.2021.3-4.43.57 [L]

Forrás: https://real.mtak.hu/240592/1/Onlinesegedletekamagyarnyelvubibliaforditasokolvasasahoz.pdf (mentve: `pinter2021.pdf`, `pinter2021.txt`).

**Hatókör:** csak böngészőből, telepítés nélkül elérhető eszközök. Mobilappok, theWord és Paratext kimarad. Csak a több magyar fordítást hordozó oldalak kerülnek be (a 4. lábjegyzet szerint kimarad az abibliamindenkie.hu, a karolibiblia.hu és a katolikus.hu/szentiras). **Szempontjai:** a szövegegység mérete, a párhuzamos olvasás, a fordítások száma, a kereső típusa, a különleges funkciók. Strong-, szótár- és interlineáris szempont nincs a rácsban. Ezekről csak az ujszov.hu-nál és az Okos Bibliánál szól.

| Eszköz (2021-es állapot) | Amit Pintér tulajdonít neki | Strong | Interlin. | Szótár | Konkord./keresés | Párhuz. olvasó | Megjegyzés ma (2026) |
|---|---|---|---|---|---|---|---|
| **Szentírás.hu** (Jeromos Bibliatársulat) | a „leghasznosabb”; egyszerre egy fordítás, fordításváltás; vers- és hivatkozás-kapcsoló; szóalapú keresés fordítás- és könyvszűréssel; GitHub, API, widgetek | – | – | – | ✅ szókeresés | ❌ (nincs osztott ablak) | A leírt kód 2025 óta a **szentiras.eu**-n fut. A szentiras.hu 2025-től új, zárt rendszer [weboldalak.md L]. |
| **ujszov.hu** (Jeromos Bibliatársulat) | görög ÚSZ (Westcott–Hort 1881/1903); görög szavak magyar megfelelője/megfelelői; a lemma előfordulásai más könyvekben („kattintgatással”); ragozott alakok; a vers fordítása a szentiras.hu Bibliáiban; szabadszavas kereső nincs | (lemma) | ✅ szószintű görög→magyar | ✅ görög–magyar | ◐ lemmára kattintva | ❌ | Az **ujszov.szentiras.eu ma a szentiras.eu/GNT-re irányít át** [L, `ujszov_home.html`]. A régi kód archív GitHub-repó (`briff/ujszov.szentiras.eu`, AGPL-3.0, README: „Az ujszov.hu oldal forráskódja 2026. júniusig”) [L]. |
| **BibleGateway** | 3 magyar fordítás (Károli 1908, UF 1990, EFO 2012); legfeljebb 5 párhuzamos panel; csak szókezdetre keres; jegyzet, PDF | ❌ | ❌ | ❌ | ◐ | ✅ | nem magyar fejlesztés; nem ellenőriztem (proxy) |
| **Párhuzamos Bibliaolvasó** (NYTI, parallelbible.nytud.hu) | táblázatos, korlátlan számú fordítás; csak igehelyre keres; történeti fordítások betűhű és normalizált alakban; KJV 1769; a szövegek GitHubon | ❌ | ❌ | ❌ | ❌ (csak igehely) | ✅ | l. 3. szakasz [L] |
| **On-line Biblia / Okos Biblia** (Szabó Bálint, biblia.szeroczei.hu) | összehasonlító olvasás színes diff-fel, két fordítás párhuzamosan; keresés szóra, igehelyre és **„a magyar olvasók tekintetében egyedülállóan” Strong-számra**; Strong-keresésnél „a Strong-féle görög lexikon magyarázatát, illetve annak magyar fordítását adja vissza”; „a legsokoldalúbb” | ◐ Strong-keresés | ❌ | ◐ Strong-lexikon, P21 szerint magyar fordítással | ✅ | ✅ (2 fordítás) | **Eltérés:** 2026-ban [L] a Strong-oldalon **angol** definíciót láttam (`weboldalak.md`). Hogy a magyar fordítás megszűnt-e, vagy csak a görögre vonatkozott, ? |
| **GlobalBible** (bibles.org, ABS) | RÚF és az „Újszövetség: élet, igazság és világosság” (Biblica); belső allúziók felugró ablakban; csonkolásos keresés | ❌ | ❌ | ❌ | ◐ | ✅ | nem ellenőriztem (proxy) |
| **On-line Biblia** (Hit Gyülekezete, biblia.hit.hu) | Károli 1908 + 5 angol; ékezet nélküli és szóeleji keresés | ❌ | ❌ | ❌ | ✅ | ✅ (lefelé bővül) | nem ellenőriztem (proxy) |
| **Online Biblia** (online-biblia.ro, KKERPE) | Károli 1908, ÚRK 2011, 2 angol, 1 román; kalauzok | ❌ | ❌ | ❌ | ✅ | ✅ | nem ellenőriztem (proxy) |
| **Egyesített Bibliaolvasó** (EBO, ebo.kre.hu, KRE) | **26 fordítás: 1 héber, 1 görög, 1 német, 1 lovári, 3 angol, 19 magyar**; 6 felekezet napi igéje párhuzamosan; fejezetenként, egymás mellett, háttérszínes kiemeléssel; **„jelenleg nem rendelkezik keresővel”**; terv: lexikonok és segédanyagok becsatornázása; a fejlesztést tanulmánykötet dokumentálja | ? | ❌ (nem szószintű) | ❌ (terv) | ❌ | ✅ | l. 7. szakasz |
| **Felebarát vagy embertárs** (2014, nyomtatott) | 11 fordítás részletei egymás mellett | – | – | – | – | (nyomtatott) | nem online |
| Konkordancia: **Árpádffy Zoltán Károli-konkordanciája** (polarhome.com/biblia) | a Károli 1908 alapján készült online konkordancia | ❌ | ❌ | ❌ | ✅ magyar szó | ❌ | nem ellenőriztem (proxy). A korábbi „Károli-konkordancia online: nem található” [S] állítás így **pontosítandó**: P21/P22 szerint volt ilyen. |

A cikk említi még: Christodouloupoulos–Steedman 100 nyelvű bibliakorpusza (a magyar a Károli 1908); Paratext / Digital Bible Library; a szentiras.hu GitHub- és API-oldala. A Strongot csak az Okos Bibliánál, a szószintű görög–magyar megfelelést csak az ujszov.hu-nál, magyar héber szótárt egyik eszköznél sem tulajdonítja. **EBO-ra vonatkozó Strong-, interlineáris- vagy szótárállítás nincs a cikkben.**

### 1.2 M. Pintér Tibor – P. Márkus Katalin (2022): The Role of Online Bible Readers in Biblical Concordance Making. *Hungarian Studies Yearbook* IV, DOI 10.2478/HSY-2022-0009 [L]; magyar változat: Online bibliaolvasók szerepe és terminológiai megoldások keresése a bibliai konkordanciakészítésben, *Alkalmazott Nyelvtudomány* 2022/1, DOI 10.18460/ANY.2022.1.005 [L]

Forrás: krepozit.kre.hu, DSpace REST, item `2e50af85-…` (HSY) és `2c694fd3-…` (ANY). Mentve: `hsy.pdf`/`hsy.txt`, `any2022.pdf`/`any2022.txt`. A HSY-cikk licence CC BY-NC-ND 3.0. A kutatást az „Egyesített Bibliaolvasó (EBO) fejlesztése és kutatási perspektívái” KRE-pályázat (20738B800) támogatta.

**A valós idejű konkordanciát adó oldalak a cikk szerint (2022):**
- **A Biblia mindenkié** (abibliamindenkie.hu/keres/uj/): kis- és nagybetű-érzékeny, kifejezéskeresés; hiperlinkes igehelyek.
- **Szentírás.hu** (/kereses/search): könyv- és fordításszűkítés; vers, fejezet, könyv, ÓSZ vagy ÚSZ szerinti csoportosítás.
- **On-line Biblia** (biblia.hit.hu): ékezet-kapcsoló, szókezdet, helyettesítő karakter, ÉS/VAGY/NEM operátor.
- **biblia.hu** (biblia.biblia.hu): Károli 1908, ékezet- és nagybetű-kapcsoló, ÉS és mínusz operátor. **2026-ban is így működik** [L, 4.2].
- **Okos Biblia** (biblia.szeroczei.hu): szavak, szószerkezetek és karakterláncok keresése; könyvekre vagy könyvcsoportokra szűkítés; **keresés a Strong-konkordancia számaira**.
- **polarhome.com/biblia**: Károli 1908 sima HTML-ben, ékezetek nélkül, helyettesítő karakter; „a legrégebbi”.

**Saját konkordancia:** az ÚRK (Újonnan revideált Károli, Veritas 2011/2021) offline, félautomatikus konkordanciája **az ESV Global Study Bible konkordanciájának 3077 angol címszavára** épül (fordított címszavak; homonímia, lemmatizálás). A cikk idején készült; elérhetősége ?. Eredeti nyelvű (Strong- vagy héber/görög) kulcsa nincs.

**Következtetésük:** a magyar online konkordanciakezelés „nem egységes”, és nincs kielégítő megoldás. Az EBO továbbfejlesztett változata „megpróbál majd megoldást adni” [P22]. Ez **terv, nem igazolt funkció**.

---

## 2. A Bibliatársulat Szómutató Szótárai (bibliatanulmanyozas.bibliatarsulat.hu) [L: nyitó- és indexoldalak; a szócikkeket nem láttam]

Mentve: `btt_home.html`, `btt_oszovetsegiszomutato_index.html`, `btt_ujszovetsegiszomutato_index.html`, `btt_osz_app.html`, `btt_usz_app.html`.

**Mi ez?** Két online szótárprogram a Magyar Bibliatársulat honlapján:
- **Babits Antal: Ószövetségi Szómutató Szótár.** „Az eredeti héber szöveg alapján készült”. Frissítve: Budapest, 2026.06.07. Szerkesztő: Babits Antal (Logos Kiadó).
- **Balázs Károly: Újszövetségi Szómutató Szótár.** „Az eredeti görög szöveg alapján készült”. Az oldal 2020.02.20-i keltezésű. Mottója Ritoók Zsigmond akadémikustól: „a görögül és héberül nem tudóknak is felkínálja a Biblia eredeti nyelvű tanulmányozását”.

**Felépítés** (az alkalmazásoldal HTML-je alapján [L]):
- héber és arámi ábécé (az ÓSZ-ben külön), illetve görög ábécé szerinti ugrás;
- „Héber / Arámi szavak jegyzéke”, illetve „Görög szavak” lista;
- „Magyar szavak jegyzéke” és „Sorszámok”;
- „Szókereső” (magyar szóra) és „Sorszám” mező;
- „Szócikkek” panel „Másolás” gombbal;
- menü: „Kiegészítő anyagok” (köztük Bevezetés), „A szótár használata” / „Súgó”, „Névjegy”.

A nyitóoldal szerint: „Balra alul lehet a fehér mezőbe beírni a keresendő **magyar** kifejezést … a mellette lévő mezőben jelennek meg azok a **sorszámok**, melyeknek szócikkeiben előfordul az adott kifejezés.” Ha a magyar szó nincs a szótárban, akkor „nem is létezik elsődleges jelentésként vagy szinonimaként a keresett szó a héber szöveg alapján”. **Ez tehát fordított (magyar → héber/görög) index is**: a magyar jelentésszavakból vezet a héber/görög címszóhoz.

**Strong-számok?** A felület Strongot nem említ. A sorszámokból viszont következtethető [K]:
- **ÚSZ:** az ábécé-ugrópontok sorszámai egybeesnek a Strong görög számozás betűkezdeteivel: γ = 1042, δ = 1138, ε = 1436, ζ = 2194, η = 2228, ι = 2383, κ = 2504, λ = 2975, μ = 3092. Ezek a Strong G1042 (γαββαθά), G1138 (Δαβίδ), G1436 (ἔα), G2194 (Ζαβουλών), G2228 (ἤ), G2504 (κἀγώ), G2975 (λαγχάνω), G3092 (Μαάθ) számai. **Az ÚSZ-szótár sorszáma tehát valószínűleg a Strong-szám**, ezt a szócikkek nélkül nem igazoltam.
- **ÓSZ:** a sorszámok **nem Strong-számok**. A héber szavak 1-től kb. 8597-ig, az arámiak 8598-tól kb. 9300-ig tartanak, külön blokkban, a Strong viszont a héber és arámi szavakat egy sorban számozza. A bét 805-nél kezdődik, a Strong-ban kb. 870 körül. Saját számozásnak tűnik [K].

**Kapcsolódás fordításhoz:** „A szótár bármelyik Bibliafordításhoz használható.” Nincs RÚF- vagy Károli-szöveghez kötve, bibliaszöveget nem jelenít meg. A „Másolás” menü az indexoldal szerint „igehelyek, bibliai idézetek másolását engedélyezi az egyes szavaknál”, tehát a szócikkek **igehelyeket és idézeteket** tartalmaznak. Ennyiben szómutató, azaz konkordancia-jellegű. Hogy az igehely-lista teljes-e, ? (a szócikket nem láttam).

**Licenc:** „SZERZŐI JOGI VÉDELEM ÉS OLTALOM … mindenfajta másolás, letöltés, sokszorosítás vagy terjesztés bűncselekmény”. Kivétel: a „másolás” menü. A használat ingyenes online, a feltételek elfogadása (jelölőnégyzet) és belépés után. „A szerzői jogokat © Babits Antal és jogörökösei, valamint a © Logos Kiadó birtokolja”. ÚSZ: „© Balázs Károly jogörökösei, valamint a © Logos Kiadó és © Babits Antal szerkesztő”. **Zárt, nem nyílt adat.**

**Amit nem tettem meg:** a használati feltételeket nem fogadtam el a felhasználó nevében, és a szócikk-adatot nem töltöttem le (a feltételek a letöltést tiltják). A szócikk szerkezete (jelentés, magyar glossza, igehely-lista, morfológia) ezért ?. A két szerző–cím párosra a WebSearch nem adott független bibliográfiai találatot [S, negatív].

**Jelentősége a mátrixban:** **ez a második ismert magyar nyelvű héber és görög szótár online** (a Biblia-Felfedező zárt moduljai mellett). Ingyenes, de jogvédett és letölthetetlen. A korábbi „magyar héber szótár online: egyetlen vizsgált oldalon sincs” megállapítás **ezzel megdől**.

---

## 3. parallelbible.nytud.hu (NYTI Párhuzamos Bibliaolvasó) [L]

Mentve: `pb_home.html`, `pb_about.html`, `pb_usage.html`, `pb_info.html`, `pb_README_master.md`, `gh/nytud_LICENSE`.

**Működés:**
- Könyv, fejezet és (opcionálisan tól–ig) vers kiválasztása, tetszőleges számú fordítással. Szabadszavas keresés nincs.
- A versek egymás mellett, időrendben jelennek meg (balra a legrégebbi); az oszlopok mozgathatók.
- Ha egy versnek egy műben több fordítása van, `§§` választja el őket.
- Betűhű (b) és normalizált (n) változat.

**Tartalom** (`/info`):
- **Magyar, 14:** Bécsi kódex, Müncheni kódex (1466), Apor-kódex, Jordánszky-kódex (1516–19), Pesti Gábor (1536), Sylvester (1541), Heltai (1565), Károli Vizsolyi Biblia (1590, csak ÚSZ), Káldi (1626, ÚSZ), Aranyos Biblia (1685, Arcanum Biblia Téka), Károli 1908 (szentiras.hu), Káldi-Neovulgáta 1997, SZIT 2003, MBT újfordítás 2014.
- **Egyéb:** KJV 1769 (Unbound Bible), 3 finn fordítás (Agricola 1548/1552, 1642).
- **Eredeti nyelvű szöveg nincs.** Héber, görög vagy LXX nem szerepel.

**Igazítás:** csak vers- vagy igehelyszintű (könyv–fejezet–vers kulcs, TSV). **Szóigazítás nincs**, Strong nincs. A háttér az Ómagyar Korpusz; a nyelvi elemekre a külön „Régi magyar konkordancia” keres, a régi szövegekben.

**Adat és licenc:**
- A szöveganyag TSV-ben letölthető a GitHubon (`dlt-rilmta/parallelbible`, illetve `nytud/parallelbible`). A README-t és a LICENSE-t a raw.githubusercontent.com-ról olvastam.
- Oszlopok: könyv, fejezet, vers, szöveg; `@@` = eredeti sortörés, `==` = egybeírt szavak.
- **Három modern fordítás (KNB, SZIT, MBT 2014) szerzői jogi okból nincs a repóban.**
- Licenc: a README és a LICENSE fájl szerint **CC BY-SA 4.0**. A README linkje tévesen a CC BY 4.0-ra mutat; a LICENSE-fájl a BY-SA szövegét tartalmazza.
- Hivatkozandó: Simon Eszter – Kalivoda Ágnes (2020): A Párhuzamos Bibliakorpusz és Bibliaolvasó fejlesztése. *Általános Nyelvészeti Tanulmányok* 32. DOI-t nem láttam.

**Jelentősége:** nyílt, idézhető, vers szerint igazított **történeti** magyar bibliakorpusz. Strong- vagy motívumrétege nincs. A referenciaprojekt számára legfeljebb a régi magyar fordítások versszintű összevetéséhez lehet forrásjelölt (CC BY-SA → ShareAlike-kötés).

---

## 4. ujszov.szentiras.eu és biblia.biblia.hu

### 4.1 ujszov.szentiras.eu [L]
- A domain **átirányít a https://szentiras.eu/GNT oldalra** („Görög Újszövetség és magyar újszövetségi szószedet, magyarázatokkal”), amelyet a `weboldalak.md` már leír. **Önálló funkciója ma nincs.**
- A régi ujszov.hu (Pintér 2021 leírása: Westcott–Hort szöveg, szavankénti magyar megfelelők, lemma-előfordulások, ragozott alakok) kódja a `briff/ujszov.szentiras.eu` archív repóban van (AGPL-3.0) [L README/LICENSE]. A README egy `old/db.sql` („ujszovszoszedet”) adatbázist említ, de a fájl a raw-címen **404** volt. A régi szószedet-adat letölthetősége ezért ?.

### 4.2 biblia.biblia.hu [L]
- Mentve: `bibliabiblia_home.html` (cp1250). Kereső három szövegre: **Károli Gáspár fordítása, King James, Luther**.
- Szűkítés: összes könyv, ÓSZ, ÚSZ vagy egy könyv.
- Alapértelmezésben nem betűérzékeny, ékezetre sem érzékeny; kapcsolóval betűérzékeny.
- Szavak között ÉS kapcsolat, `-` kizárás, idézőjeles kifejezés. Igehely beírására a teljes fejezet jelenik meg, a versek kiemelve.
- **Strong-, eredeti nyelvű és szótárfunkció nincs.** Ez magyar szöveges konkordancia (KWIC nélkül, verslista).

---

## 5. SWORD/CrossWire magyar modulok [L]

Forrás: https://www.crosswire.org/ftpmirror/pub/sword/raw/mods.d.tar.gz (a teljes CrossWire `mods.d` könyvtár, kibontva: `crosswire/modsd/`) és https://www.crosswire.org/ftpmirror/pub/sword/raw/mods.d/hunkar.conf. Az ftp.crosswire.org a proxyn 403 volt, a www.crosswire.org nem.

**`Lang=hu` modul a fő CrossWire-tárban: 5, mind bibliaszöveg.** Magyar lexikon- vagy szótármodul nincs.

| Modul | Leírás | Verzió / dátum | Licenc | GlobalOptionFilter |
|---|---|---|---|---|
| HunKar | Revideált Károli Biblia 1908; forrás: github.com/krisek/HunKar (szentiras.hu/KG + abibliamindenkie.hu fejezetcímek); Versification=Calvin | 2.0 / 2020-10-23 | **Public Domain** | OSISHeadings, OSISFootnotes, OSISScripref |
| HunUj | MBT Újfordítású Biblia; forrás: parokia.hu | 1.8.1 / 2021-08-17 | Copyrighted; Permission to distribute granted to CrossWire | OSISFootnotes, OSISHeadings, OSISScripref |
| HunRUF | MBT Revideált Újfordítású Biblia; forrás: abibliamindenkie.hu/uj | 1.0 / 2021-07-13 | Copyrighted; Permission … CrossWire | OSISFootnotes, OSISHeadings, OSISScripref |
| HunKNB | Káldi-Neovulgáta 2013; Szent Jeromos Katolikus Bibliatársulat | 1.0 / 2021-01-14 | Copyrighted; Permission … CrossWire | OSISHeadings |
| HunIMIT | IMIT Bibliája (zsidó) | 1.0 / 2021-04-14 | Public Domain | OSISHeadings |

**Strong-címke:** egyik magyar modulnál sincs `OSISStrongs` (vagy `OSISMorph`, `OSISLemma`) szűrő, és `Feature=StrongsNumbers` sincs. **Strong-taggelt magyar SWORD-modul tehát a CrossWire fő tárában nincs** [L]. Ez megerősíti a repó korábbi [R] állítását a HunKarról.
- A krisek/HunKar README-je [L, raw] szerint a forrás a szentiras.hu/KG (az Énekek Éneke az abibliamindenkie.hu-ról). Strongot nem említ.
- A HunKar a szentiras.hu/KG-ből vett kereszthivatkozásokat hordozza (History_2.0).
- Az AndBible „magyar fordítás” cellája ezért 4-ről **5 SWORD-modulra** bővül (a KNB és az IMIT is elérhető).

---

## 6. GitHub: nyílt magyar bibliai adatok Strong-gal vagy igazítással

Módszer: GitHub MCP repó- és kódkeresés [L találati listák]. Keresések: „hungarian bible strong”, „karoli strong”, „hungarian bible”, „biblia magyar”, „karoli biblia”, „HunKar”, „interlineáris”, „szentiras”, „parallelbible”, „bible strongs hungarian OR magyar”. Kódkeresések: `"Kezdetben teremté" H7225`, `"strong:H7225" Kezdetben`, `"Kezdetben vala az Ige" G3056`, `"strong:G3056" "Ige"`, `"teremté" "strong" OSIS hun`.

**Eredmény: Strong-számmal ellátott vagy szószinten igazított nyílt magyar bibliaszöveget nem találtam.** A kódkeresés magyar szöveg + Strong-szám kombinációra csak a felhasználó saját repóját (`basesoft777/Bible-Study`) adta. Negatív lelet [L], de a GitHub-kereső nem kimerítő (nem indexelt archív repók, LFS, zip).

| Repó | Mi van benne | Licenc (kód / adat) | Strong / igazítás | Lefedettség |
|---|---|---|---|---|
| `krisek/HunKar` | Károli 1908 OSIS XML, SWORD-modul forrása | README-ben nincs licenc; a CrossWire-conf „Public Domain” | ❌ Strong; ✅ xref (szentiras.hu/KG) | teljes Biblia |
| `nytud/parallelbible` (= `dlt-rilmta/parallelbible`) | Párhuzamos Bibliakorpusz TSV | CC BY-SA 4.0 (LICENSE) | versszintű igazítás, szó- és Strong-szint ❌ | 11 történeti magyar + KJV + 3 finn (a 3 modern kihagyva) |
| `balint-szabo-hungary/hungarian-bible-translations` | közkincs régi magyar fordítások OSIS XML + könyvenkénti TXT; az **Okosbiblia.hu**-ra hivatkozik (a szeroczei-oldal fejlesztője, Szabó Bálint) | Apache-2.0 (LICENSE); a szövegek „public domain” | ❌ | ? (a fájllistát nem láttam, a GitHub-fa nem volt elérhető) |
| `peterpolgar/Biblia-json-xml` | 8 teljes + 10 ÚSZ + IMIT, JSON/XML; forrás: baranyilaszlozsolt.com theWord-modulok | Unlicense (a repóé). **A tartalom egy része jogvédett** (pl. UF 1990, Revideált Károli 2011), a jogtisztaság kétséges | ❌ | sok fordítás |
| `kulcsarrudolf/biblia-hu` (és a `biblia-ruf`, `biblia-ruf-py`) | RÚF 2014 és Revideált Károli 2011 npm/Python könyvtár | kód MIT; a szöveg a kiadók jogvédett anyaga („redistributed with attribution”) | ❌ | 2 fordítás |
| `janos-i/Zefania-XML-Bible-HUN` | Károli, „részben átdolgozott kiadás”, Zefania XML | ? | ? (a README üres) | ? |
| `spthmpsn/Hu1Bible` | Unbound Bible Károli, USFM | ? | ❌ | ? |
| `szentjozsefhackathon/szentiras.eu` | a szentiras.eu forráskódja | **kód AGPL-3.0** [L: LICENSE, README, composer.json] | görög ÚSZ Strong + morfológia (OpenGNT CC BY-SA, ill. BMT) | l. lent |
| `briff/ujszov.szentiras.eu` | a régi ujszov.hu kódja (archív) | AGPL-3.0 | ? | ? |
| `npedrazzini/parallelbibles` | statisztikus szóigazító modellek (SyMGIZA++) 100+ nyelvre, köztük a magyarra; OPUS bible-uedin XML (a magyar a Christodouloupoulos-korpuszból, P21 szerint Károli 1908) | LICENSE-fájl nem található (404) | **gépi szóigazítás angol forrásnyelvhez**, Strong ❌ | magyar: ÓSZ és ÚSZ jelölve |
| `kovzol/bibref` (csak keresőtalálat [S]) | ÚSZ→LXX idézetkereső (Kovács Zoltán) | ? | LXX–ÚSZ, nem magyar adat | – |

**szentiras.eu, részletek** [L kód, kódkeresés és raw]:
- A görög szöveg forrása az OpenGNT (`config/translations.php`: „Open Greek New Testament (OGNT) project, CC BY-SA 4.0”, `github.com/eliranwong/OpenGNT`) vagy a Byzantine Majority Text (`briff/byzantine-majority-text`).
- A Strong-szótár bemenete `greek/dictionary.xml`/`.txt`, a tárolóban (`Storage`), nem a repóban.
- A magyar szócikkeket a `szentiras:generate-strong-word-translations` parancs MI-vel generálja (OpenAI vagy Anthropic; az alapértelmezés kódban „claude-3-5-haiku-20241022”), és a modell nevét a bejegyzés `source` mezőjébe írja. Ez proveniencia-jelölés.
- **A görög szószedet licence CC BY-SA 4.0**: `mission.twig`, `dictionary.twig`, `api.twig`, valamint az MCP-szerver instrukciója („szentiras.eu's own material — commentaries, the Greek glossary and similar — is licensed CC BY-SA 4.0”).
- **Tömeges letöltés:** a kódkeresés `path:storage` alatt nem talált adatfájlt, és a repóban nincs dump. A szótár az API-n (`/api/greek-search`) és az MCP `lookup-greek-word` eszközén **szócikkenként** érhető el, ingyenes kulccsal, 60 kérés/perc korláttal (`weboldalak.md`). **Letölthető, kész szótárfájl nem található** [L negatív]. A licenc ugyanakkor az API-n keresztüli gyűjtést és a ShareAlike-továbbadást megengedi.

---

## 7. EBO (Egyesített Bibliaolvasó, ebo.kre.hu): csak másodlagos forrásból

Az ebo.kre.hu és a btk.kre.hu (konferenciaprogram-PDF) a proxyn 403-at adott; nem kerültem meg. Források: P21 [L], P22 [L], WebSearch-kivonatok [S].

- **Tartalom, 2021** [P21]: 26 bibliafordítás (1 héber, 1 görög, 1 német, 1 lovári, 3 angol, 19 magyar); hat felekezet napi igéje és bibliaolvasó kalauza párhuzamosan; fejezetenkénti, egymás melletti megjelenítés, háttérszínes szövegkiemeléssel.
- **Kereső 2021-ben nincs** [P21]. 2022-ben a „továbbfejlesztett változat” konkordancia-megoldást ígér [P22]. Hogy elkészült-e, ?.
- **Strong, interlineáris, szótár:** egyik forrás sem állítja. A tervek „lexikonok” becsatornázásáról szólnak [P21]. → ?, nem ❌.
- **Dokumentáció:** Fabiny Tibor és M. Pintér Tibor (szerk.): *πῶς ἀναγινώσκεις; Hogyan olvasod? Felekezeteket összekötő Egyesített Bibliaolvasó (EBO) felé*, Hermeneutikai Kutatóközpont, 2021. Tanulmányok: grafikai arculat (Borsa), első tervek (Győri), digitalizálás és szinkronizálás (Király: digitalizálás → adattisztítás → importálás → párhuzamosítás; alversekre bontás, pótlólagos számozás), korpuszok a lexikológiában (Pintér–Márkus), egzegetikai haszon (Fabiny). A Pintér–Márkus-fejezet a krepozit-on rekordként megvan (`c09640cb-…`), PDF nélkül [L].
- **Zárókonferencia** [S]: 2024.04.23., Károlyi–Csekonics-palota, „A bibliafordítás aktuális kérdései”. M. Pintér Tibor előadása az EBO-ról mint online fordítási segédletről (https://btk.kre.hu/images/EBO_konf_program.pdf, csak kivonat). Egy 2024-es *Vallástudományi Szemle*-kivonat a Hermeneutikai Kutatóközpont futó projektjei között említi („az összehasonlító bibliaolvasás technikai feltételeit teremti meg”) [S].
- **Mai működése, licence, adatelérhetősége: ?** A konferencia projektzárás volt (3 éves projekt) [S].

---

## 8. Biblia-Felfedező: a maradék kérdések (csak bolti szöveg és kivonat)

- **Play HU-leírás** [L, kivonatolva: `bd_play_desc.txt`]:
  - Strong-számos szöveg: csak a „Károli Gáspár Biblia – Strong számokkal (HUN)”;
  - „görög és héber szótárak”, „keresési és szóelemző eszköz”, kereszthivatkozási rendszer, párhuzamos olvasás, kb. 1000 helyes térkép, Matthew Henry, magyar keresztény könyvek;
  - **interlineáris nézet, Septuaginta/LXX, BHS vagy NA28 nincs a leírásban.**
  - A Play-oldal kapcsolódó appjainál előforduló „NA28, UBS-5, BHS, Septuagint (LXX)” felsorolás **egy másik fejlesztő (Gospel Technologies) appjához** tartozik, nem a BD-hez.
- **iOS-changelog** [L, `apple_biblediscovery_hu.html`], 10.6.1 (márc. 14., a sorrend alapján valószínűleg 2026): „Károli Bibliából (HUN) eltüntettük a vala szavakat és több, mint 400 igének a régies ragozását modernizáltuk … Kb 15 ezer helyet érint a változás. A régies ragozású korábbi változat a Károli Gáspár (KG) modulnév alól letölthető.” Továbbá: a BBE-hez és az AKJV-hez „Strong számokat rendeltünk, saját munka”.
  → **A Strong-párosított HUN szöveg 2026-ban is modernizált Károli, nem az 1908-as szöveg.**
- **Az ÓSZ-párosítás mai teljessége:** a bolti szöveg nem mond sem teljességet, sem hiányt. Új kivonat nem jött [S, negatív]. **Marad nyitott.**
- **Interlineáris, LXX:** a bolti szövegekben nincs nyoma [L negatív], kivonat sincs [S negatív]. **?** marad (a bible-discovery.com és a mobilbiblia.hu modullistája nélkül nem zárható le ❌-ra).

---

## 9. Egyéb, ezúttal elérhető oldalak

- **lexikon.katolikus.hu** [L]: a Magyar Katolikus Lexikon „kísérleti internetes változata”, A–Z címszavakkal. „Az anyagok hitbuzgalmi és lelkipásztori célra szabadon felhasználhatók, azonban kereskedelmi céllal nem.” A minta-szócikk (*szövetség*) részletes bibliateológiai cikk: héber terminus („berit … 285x”), igehely-hivatkozások, ÓSZ/ÚSZ-tagolás. **Ez az egyetlen talált ingyenes, online, magyar bibliai fogalmi szócikkanyag**, de katolikus lexikon, nem motívumlexikon. Proveniencia (szerzőség szócikkenként) ?, kereskedelmi felhasználás tiltott.
- **ppek.hu** [L, címkatalógus]: 1233 kötet. A címjegyzékben bibliai szótár, konkordancia vagy bibliai lexikon nincs. Van *A keresztény szellemiség lexikona*, *Liturgikus lexikon*, *Teológiai kisszótár* (Rahner–Vorgrimler), Farkasfalvy: *Bevezetés az újszövetségi szentírás könyveihez*, és az ÚSZ (Jeromos).
- **dea.lib.unideb.hu** [L, REST-metaadat]: a korábban *Biblikai fogalmi szókönyv*-ként jelölt bitstream (`889c401d-…`) neve `t_dekdb_bibKLT00078503.pdf` (24 MB), leírása **„tartalom”**. Valószínűleg tartalomjegyzék-szkennelés, nem teljes szöveg [K]. A korábbi „PDF-je a DEA-n” állítást **gyengíteni kell**.
- **reformatus.hu** [L]: saját bibliaeszköz nincs, az abibliamindenkie.hu-ra és a Bibliapp-ra mutat.
- **mek.oszk.hu**: célzottan nem vizsgáltam (a feladat nem kérte); a `weboldalak.md` [S]-állítása (a MEK-ben kereshető Károli-szöveg) marad.

---

## 10. Változások a mátrixban (röviden)

1. Új oszlopok: **EBO** [P21/S], **Bibliatársulat Szómutató** [L, belépés előtti oldalak], **parallelbible.nytud.hu** [L].
2. „Héber szótár magyarul” és „Görög szótár magyarul”: a Szómutató ✅ (zárt, ingyenes online). A BD már nem az egyetlen.
3. AndBible: a magyar fordítások száma 5 SWORD-modul (CrossWire [L]). A Strong ❌ most [L], nem [R].
4. szentiras.eu: kód AGPL-3.0 [L]; a görög szószedet CC BY-SA, de tömeges dump nincs, csak API/MCP.
5. szeroczei: a P21 szerinti „magyar fordítású Strong-lexikon” eltér a 2026-os [L] angol definíciótól → ellenőrizetlen pont.
6. Károli-konkordancia online: P21/P22 szerint létezett (Árpádffy, polarhome); ma nem ellenőrizhető.
7. BD: interlineáris és LXX továbbra is ?; a HUN-szöveg 2026-ban modernizált (kb. 15 ezer hely, iOS-changelog [L]).

## 11. Források (URL-ek)

- https://real.mtak.hu/240592/ · https://real.mtak.hu/240592/1/Onlinesegedletekamagyarnyelvubibliaforditasokolvasasahoz.pdf
- https://krepozit.kre.hu/server/api/core/bitstreams/1bd9522b-2583-4f63-9af2-b45a195d25da/content (HSY 2022)
- https://krepozit.kre.hu/server/api/core/bitstreams/84fb115b-261a-41c1-9aec-1ff63067d37a/content (ANY 2022)
- https://bibliatanulmanyozas.bibliatarsulat.hu/ (+ `/oszovetsegiszomutato_index.html`, `/ujszovetsegiszomutato_index.html`, `/oszovetsegiszomutato/`, `/ujszovetsegiszomutato/`)
- https://parallelbible.nytud.hu/ (+ `/about`, `/usage`, `/info`)
- https://raw.githubusercontent.com/dlt-rilmta/parallelbible/master/README.md · https://raw.githubusercontent.com/nytud/parallelbible/master/LICENSE
- https://ujszov.szentiras.eu/ (→ https://szentiras.eu/GNT) · https://biblia.biblia.hu/
- https://www.crosswire.org/ftpmirror/pub/sword/raw/mods.d.tar.gz · https://www.crosswire.org/ftpmirror/pub/sword/raw/mods.d/hunkar.conf · https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=HunKar
- raw.githubusercontent.com: krisek/HunKar, szentjozsefhackathon/szentiras.eu (README, LICENSE, composer.json, ImportGreek.php, GenerateStrongWordTranslations.php), briff/ujszov.szentiras.eu, balint-szabo-hungary/hungarian-bible-translations, peterpolgar/Biblia-json-xml, kulcsarrudolf/biblia-hu, npedrazzini/parallelbibles
- https://lexikon.katolikus.hu/ · https://lexikon.katolikus.hu/S/sz%C3%B6vets%C3%A9g.html · https://ppek.hu/ppekcim.htm · https://reformatus.hu/
- https://play.google.com/store/apps/details?id=com.biblediscovery · https://apps.apple.com/hu/app/biblia-felfedez%C5%91/id1155806176?l=hu (a korábban mentett fájlokból)
- Csak kivonat [S]: https://btk.kre.hu/images/EBO_konf_program.pdf · https://btk.kre.hu/images/vallastudomanyi_szemle/2024-1/VSz_2024_1_250-253.pdf · https://github.com/kovzol/bibref
