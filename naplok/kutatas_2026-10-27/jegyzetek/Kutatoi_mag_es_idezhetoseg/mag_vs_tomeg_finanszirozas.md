# Kutatói mag vs. tömegpiac, és a kutatói projekt finanszírozása

*Módszertani megjegyzés: a kutatás 2026.10.27-én futott. Több elsődleges oldal (sefaria.org PDF, mek.unideb.hu PDF) DNS-hiba miatt nem volt letölthető; az alábbi állítások jelentős része a keresőmotor összefoglaló-kivonatán (snippet) alapul, nem a teljes oldal elolvasásán. Ezeket „(snippet)” jelöli. Az „Inferences” alpontok értelmezések, nem adatok.*

## 1. Összehasonlítható projektek: kit szolgáltak először, hogyan nőttek, miből élnek

### Takeaway
A tudós-építette, nyílt adatprojektek (STEPBible, ETCBC/BHSA, Clear/Macula, Perseus) hatása tartós és idézhető, de pénzügyileg kicsik és intézményi/alapítványi támogatásra vagy önkéntességre épülnek; a tömeges elérés (YouVersion, Sefaria) nagy, folyamatos költségvetést igényel, amelyet adományozói hálózat fedez. A Sefaria az egyetlen minta, ahol szöveg+önkéntes fordítói mag után jött a tömeg — de évi ~7,8 M USD kiadással.

### Cited Findings
**STEPBible (Tyndale House, Cambridge)**
- A Tyndale House megrendelte és pénzügyileg, valamint tudományos szakértelemmel támogatta a projektet; később önálló jótékonysági szervezetté (CIO) válását szorgalmazta, ezután a hivatalos részvétele az adatfejlesztésben megszűnt (a kiadási jegyzet 2021-ig terjedő adatra vonatkozik) — [STEPBible-Data releases, GitHub](https://github.com/STEPBible/STEPBible-Data/releases) (snippet)
- A szoftvert és az erőforrásokat önkéntesek építik, a Tyndale House felügyeletével és a Crosswire-rel partnerségben; egyesek idővel, mások pénzzel járulnak hozzá — [STEPBible wiki, Development Team](https://stepweb.atlassian.net/wiki/spaces/SUG/pages/12484612/Development+Team) (snippet)
- Brit Charity Commission (1193950-es szám): 2024.12.31-ig záruló év: összbevétel 2 528 GBP, kiadás 264 GBP; 20 önkéntes, 3 kurátor; „önkéntesek több országban, nulla költséggel” fejlesztenek; a felület 50 „gateway” nyelven érhető el; fő költség a szerver és terheléselosztás (USA) — [Charity Commission register](https://register-of-charities.charitycommission.gov.uk/en/about-the-register-of-charities/-/charity-details/5172044/accounts-and-annual-returns) (snippet)
- Felhasználószámot / Globális Dél-bontást nem találtam nyilvános forrásban — l. Gaps.

**ETCBC / BHSA (VU Amsterdam)**
- A SHEBANQ projektet a CLARIN-NL finanszírozta, 2013 közepétől 2014 közepéig, az ETCBC és a DANS (NWO-partnerrel) végezte — [KNAW Pure, SHEBANQ](https://pure.knaw.nl/portal/en/projects/shebanq/) (snippet)
- A SHEBANQ szövegeinek és adatainak tartós elérhetőségét a DANS és az ETCBC a Német és a Holland Bibliatársulattal partnerségben biztosítja — [Text-Fabric cikk, HIPHIL Novum](https://tidsskrift.dk/hiphilnovum/article/view/142740) (snippet)
- A BHSA Text-Fabric formátumban érhető el (Python-csomag; „tudományos, hozzáférhető és reprodukálható” feldolgozás) — [VU Research, Text-Fabric](https://research.vu.nl/en/publications/text-fabric-what-how-and-why/) (snippet)

**Clear Bible / MACULA**
- A MACULA Hebrew és Greek CC BY 4.0 licencű (szintaxisfák, morfológia, nyelvészeti annotáció) — [HuggingFace adatlap, MACULA-hivatkozással](https://huggingface.co/datasets/NuBerea/vulgate-bridge) (snippet, harmadik fél)
- A Clear Bible, Inc. 2023.08.21-én a Biblica része lett — [biblica.com/clear](https://biblica.com/clear) (snippet)
- Alapítványi adományok, pl. 199 000 USD (National Christian Foundation), 27 000 USD (Tyndale House Foundation) — [CauseIQ](https://causeiq.com/organizations/clear-bible,812408473) (snippet, aggregátor, dátum bizonytalan)

**Perseus Digital Library (Tufts)**
- NEH-támogatás „Perseus on the Web” fázisra: valamivel kevesebb mint 348 881 USD, 2023.07–2026.06; kiegészítő támogatás Tufts-egységektől és a Google-tól — [Perseus updates blog](https://sites.tufts.edu/perseusupdates/?p=1891) (snippet)
- Mellon Foundation: 600 000 USD a Perseids platformra (tantermi együttműködés, tudományos kuráció) — [Perseus updates, Mellon](https://sites.tufts.edu/perseusupdates/?p=321) (snippet; dátum nem ellenőrzött, valószínűleg 2010-es évek eleje — RÉGI)
- Finanszírozók listája: Alpheios, Mellon, IMLS, NEH, NSF, magánadományok, Tufts — [Northwestern libguide](https://libguides.northwestern.edu/perseusdigitallibrary) (snippet)
- A Perseus 4.0 már nincs aktív fejlesztés alatt; a munka a Scaife Viewerbe költözik — [Perseus updates blog](https://sites.tufts.edu/perseusupdates/?p=1891) (snippet)

**Sefaria (szöveg + önkéntesek → tömeg)**
- Alapítás: koncepció 2011, béta 2012, nonprofit bejegyzés 2013; alapítók Joshua Foer (újságíró) és Brett Lockspeiser (volt Google-termékmenedzser) — [Wikipedia: Sefaria](https://en.wikipedia.org/wiki/Sefaria) (snippet; a források eltérnek az évben: [GuideStar](https://www.guidestar.org/profile/46-4406454) 2013-at ad)
- 2013-ra 700+ fordító járult hozzá önkéntesként; korai finanszírozók: Natan Fund, Koschitzky család, Jim Joseph Foundation; a könyvtár 8,5 millió szóról 183 millióra nőtt; ma 300 millió+ szó — [Wikipedia](https://en.wikipedia.org/wiki/Sefaria), [Sefaria timeline sheet](https://voices.sefaria.org/sheets/497242) (snippet)
- 2024: átlag ~775 000 havi felhasználó, októberben közel 900 000; 234 ország — [Sefaria Impact Report 2024](https://www.sefaria.org/static/files/Sefaria_Impact_Report_2024.pdf) (snippet; a PDF nem töltődött le)
- 2024: bevétel ~4,53 M USD, kiadás ~7,76 M USD (Form 990) — [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/organizations/464406454) (snippet)
- 2023-as észak-amerikai felhasználói felmérés létezik — [Jim Joseph Foundation](https://jimjosephfoundation.org/?p=7575) (nem olvastam)

**YouVersion (tömeg)**
- 2025 novemberében 1 milliárd telepítés az alkalmazáscsalád egészére; a telepítések +12% év/év, a napi használat +18%; „egymilliárd megnyitás 39 naponta”; a Szubszaharai Afrikában 37,1 M telepítés 2025-ben (ebből 27,7 M Bible App Lite) — [ChurchLeaders](https://churchleaders.com/news/2208848-youversion-celebrates-milestone-billion-downloads.html), [The Citizen](https://www.thecitizen.co.tz/tanzania/news/national/youversion-bible-app-hits-one-billion-installs-launches-global-bible-month-5297860) (snippet; a számok a cég saját közleményéből, függetlenül nem ellenőrzöttek)

**Logos (lelkészek/tudósok, fizetős)**
- 2024 októberében előfizetéses modellre tért át: Premium (kiscsoport-vezetők, laikus elmélyülők), Pro (lelkészek, igehirdetés-előkészítés), Max (diákok, görög/héber) — [Logos community forum](https://community.logos.com/forums/t/226128.aspx) (snippet)
- Hivatalos oldal: Premium 2 évre 189,80 USD (kedvezménnyel), Pro 284,80 USD, Max 379,80 USD (2 év); a havidíj a források szerint 9,99 USD-tól — [Logos subscriptions](https://logos.com/configure/subscriptions) (snippet; az árak forrásonként eltérnek)
- A Liberty University ingyen adja a Logos Max-ot teológushallgatóinak — [Liberty University](https://www.liberty.edu/information-services/inclusive-access/faithlife/) (snippet) — példa intézményi licencre mint terjesztési csatornára

**Paratext (csak fordítóknak)**
- 2025 januárjában 14 000+ felhasználó (fordítók, konzulensek, korrektorok, projektmenedzserek); UBS–SIL közös projekt, 30 éves — [UBS: 30 Years of Paratext](https://unitedbiblesocieties.org/celebrating-30-years-of-paratext-supporting-bible-translation/) (snippet)
- Ingyenes, de a jogosultságok szintezettek (FOBAI-standardok elfogadása a teljes Translation/Publishing szinthez) — [LingTranSoft](https://lingtransoft.info/node/714) (snippet)

### Inferences
- A tudományos maggal induló projektek sikerét nem felhasználószám, hanem *újrahasznosítás* méri: a STEPBible-adat, a BHSA és a MACULA más eszközökbe (köztük e repóba) épül be. Ez a „idézhetőség” csatornája, és bevételt alig termel (STEPBible 2024: 2 528 GBP bevétel).
- A Paratext 14 000 felhasználóval egy szűk, professzionális közönség világszintű *teljes* lefedése — a szűk mag nem kudarc, ha a mag a terület egészét jelenti. A magyar mag (lelkész ~6–8 ezer becslés) nagyságrendileg hasonló.
- A Sefaria-minta átültetése (szöveg-mag → tömeg) dokumentáltan nagy adományozói tőkét igényelt; ennek magyar megfelelője nem azonosítható.
- Blue Letter Bible és NET Bible jegyzetek: nem kutattam (keretkorlát) — l. Gaps.

### Gaps
- STEPBible felhasználószám és a Globális Dél fordítói elérése: nyilvános számot nem találtam (a Charity Commission TAR PDF-jei talán tartalmaznak).
- ETCBC jelenlegi finanszírozása (NWO, VU) és Text-Fabric-felhasználók száma: nem található.
- Blue Letter Bible, NET Bible (Bible.org) célcsoport és finanszírozás: nem kutatva.
- A Sefaria tudományos (akadémiai) használatáról mért adat: nem jutottam hozzá.

## 2. Diffúziós elmélet: innovátorok, véleményvezérek, lead userek, 1000 rajongó, kétlépcsős kommunikáció

### Takeaway
Az elméletek a mag-első stratégiát támasztják alá *terjesztési* szempontból (a lead userek és véleményvezérek felől indul a diffúzió), de arra, hogy a lelkészek eszközt adnak tovább gyülekezetüknek, empirikus felmérést nem találtam — csak anekdotát.

### Cited Findings
- Von Hippel definíciója (1986, *Management Science*): a lead user olyan igényekkel szembesül, amelyek a piacon általánossá válnak, de hónapokkal-évekkel a piac zöme előtt; és jelentős haszna van a megoldásból, ezért maga is innoválhat — [Wikipedia: Lead user](https://en.wikipedia.org/wiki/Lead_user); elsődleges: [von Hippel & Urban 1988 PDF](https://www.mit.edu/people/evhippel/papers/Lead%20Users%20Eric%20von%20Hippel%20and%20Glen%20Urban%20-%201988.pdf) (RÉGI, de alapmű)
- Kevin Kelly, „1,000 True Fans” (2008): 1000 olyan rajongó, aki évente átlag 100 USD-t fizet, közvetlenül, közvetítő nélkül → 100 000 USD/év; a szám rugalmas (pl. 1000 × 50 USD) — [Gigazine összefoglaló](https://www.gigazine.net/gsc_news/en/20230107-1000-true-fans) (snippet; RÉGI elsődleges szöveg); Li Jin (a16z, 2020): „1,000 True Fans? Try 100” — [a16z](https://a16z.com/1000-true-fans-try-100/); kritika: [Dave Karpf](https://davekarpf.substack.com/p/the-hollow-core-of-kevin-kellys-thousand)
- Lelkészi ajánlás: egy véleménycikk az American Bible Society adataira hivatkozva azt írja, hogy a lelkészeknek ma már alkalmazásválasztásban is tanácsot kell adniuk — [Albany Herald](https://albanyherald.com/features/creede-hinshaw-are-you-more-app-to-read-the-bible/) (vélemény, nem felmérés); egyedi lelkészi ajánlólisták léteznek (YouVersion, Bible.is) — [Faith FPC](https://faithfpc.org/articles/recommended-apps/) (anekdota)
- Rogers-kategóriák (innovátor ~2,5%, korai alkalmazó ~13,5%, korai többség 34%, késői többség 34%, lemaradók 16%; véleményvezérek a korai alkalmazók között): ezt a keresés NEM erősítette meg forrással — ellenőrizendő Rogers *Diffusion of Innovations* (5. kiad., 2003) alapján.

### Inferences
- A projekt tulajdonosa maga lead user (a saját PaRDeS-kutatási igényéből épít). Von Hippel szerint az ilyen eszköz a piac jövőbeli igényét előlegezi, de a szűk szegmensben lesz először értéke.
- Kelly-matek magyar kontextusban: a korábbi kutatás „néhány száz” fizető támogatót becsült; 300 × 50 USD ≈ 15 000 USD/év — kiegészítő, nem fenntartó bevétel (ez számítás, nem adat).
- A kétlépcsős modell (tudós → lelkész → laikus) mellett szól, hogy a Logos tierjei és a Liberty-féle intézményi licenc is a lelkész/hallgató csatornára épít; mellette szóló *mért* magyar vagy nemzetközi adat nincs.

### Gaps
- Empirikus adat arra, hogy lelkészek/tanárok eszközöket terjesztenek gyülekezetükben (pl. ABS State of the Bible, Barna): nem találtam; érdemes célzottan keresni.
- Katz–Lazarsfeld (1955) kétlépcsős modell elsődleges forrása: nem ellenőriztem.
- Rogers számai: nem forrásolva (l. fent).

## 3. Kompromisszumok: szigor és proveniencia vs. egyszerűség; hatásidő; bevétel

### Takeaway
A források azt mutatják, hogy a tudományos eszközök a reprodukálhatóságot és a nyílt licencet hangsúlyozzák (Text-Fabric, CC BY), a tömegeszközök a napi szokást (YouVersion napi használat); a kettő eltérő mérőszámot és költségszerkezetet jelent. A „túl akadémikus a laikusnak” kockázatra a Logos szegmentált tierjei adnak piaci mintát.

### Cited Findings
- A Text-Fabric deklarált célja a tudományos, hozzáférhető és *reprodukálható* feldolgozás — [VU Research](https://research.vu.nl/en/publications/text-fabric-what-how-and-why/) (snippet)
- A Logos ugyanazt a korpuszt három közönségre szegmentálja (laikus elmélyülő / lelkész / héber-görög hallgató) — [Logos forum](https://community.logos.com/forums/t/226128.aspx) (snippet)
- A Paratext jogosultsági szintekkel védi a szakmai standardot (FOBAI), miközben ingyenes — [LingTranSoft](https://lingtransoft.info/node/714) (snippet)
- A YouVersion sikermutatója a telepítés és a napi használat, nem a tartalmi pontosság — [ChurchLeaders](https://churchleaders.com/news/2208848-youversion-celebrates-milestone-billion-downloads.html) (snippet)
- A Perseus 4.0 fejlesztése leállt, a projekt egy új nézőre (Scaife) migrál — a kutatói eszközök nagy hosszú távú karbantartási terhének példája — [Perseus updates](https://sites.tufts.edu/perseusupdates/?p=1891) (snippet)

### Inferences
- Az adat-réteg (proveniencia, verziók, döntésnapló) a kutatói magnak érték, a laikusnak rejtett infrastruktúra: a két közönség nem feltétlenül ütközik, ha a laikus felület *nézet* az adaton (a Sefaria és a Logos is ezt csinálja). Ez értelmezés.
- Hatásidő: a kutatói mag felé a hatás idézéseken át, évek alatt mérhető; a tömegpiacon a versenytársak (YouVersion) ingyenesek és hatalmas skálájúak, magyar nyelvű differenciálás nélkül a tömegstratégia esélye kicsi.
- Bevétel: egyik összehasonlított tudós-építette projekt sem él felhasználói díjból; a Logos az egyetlen fizetős modell, és az kiterjedt licencelt könyvtárra épül.

### Gaps
- Kvantitatív adat arra, hogy a „túl akadémikus” felület milyen arányban veszít laikus felhasználót: nem találtam.

## 4. Finanszírozás kutatói digitális erőforrásra (magyar, európai, nemzetközi magán)

### Takeaway
A nagy összegű állami és EU-s források (NKKP, ERC) PhD-t és befogadó intézményt követelnek; magánszemély közvetlenül szinte sehol nem pályázhat. A reális út: befogadó intézmény (egyetem, egyházi felsőoktatás, HUN-REN) vagy egy saját alapítvány/egyesület, illetve kisebb, magánszemélyt is elfogadó alapítványi támogatások (JTF bizonyos esetekben).

### Cited Findings
**Magyar**
- Az OTKA utódja az NKFIH Nemzeti Kutatási Kiválósági Program (NKKP); alprogramjai tudományterület-függetlenek („bármilyen tudományterületen végezhető felfedező kutatás”) — [ELTE PPK összefoglaló, NKKP_25](https://ppk.elte.hu/media/55/c4/7f4f726be225dcda83c592b497191acdee777fc980061a6cc31097a100b0/nkkp_25_palyazati_felhivas_összefoglaló.pdf) (snippet)
- STARTING_25: 100 M Ft (átl. évi 25 M Ft) + 25 M Ft opcionális kísérleti dologi keret; ADVANCED_25: 120 M Ft (átl. évi 30 M Ft) +…; EXCELLENCE_25: 160 M Ft + 40 M Ft, legfeljebb 2 év (a snippet így közli — az „évi 80 M Ft” átlag ezzel konzisztens); az NKKP 2025–2029-es keretösszege 40 milliárd Ft — [PTE NKKP prezentáció 2025](https://projektek.pte.hu/sites/projektek.pte.hu/files/%20files/NKKP_prez_2025.pdf), [NKFIH](https://nkfih.gov.hu/hivatalrol/eloadasok-publikaciok/nemzeti-kutatasi) (snippet)
- Az NKKP-ra a befogadó intézmény és a vezető kutató együtt pályázik; a vezető kutatónak PhD kell, és magyarországi befogadó intézményhez kell kötődnie; konzorcium nem megengedett — [Wigner pályázati tájékoztató 2024.05.15](https://WIGNER.HU/sites/default/files/inline-files/P%C3%A1ly%C3%A1zati_t%C3%A1j%C3%A9koztat%C3%B3_20240515.pdf) (snippet)
- Egy 2026-os elemzés szerint a legtöbb NKKP-támogatás az élettudományokhoz kerül — [Metszetek 2026/1](https://real.mtak.hu/246598/1/metszetek_2026_1szam_LPL.pdf) (snippet)
- Korábbi OTKA-keretek: 2022-es kiírások 13,5 Mrd Ft (2022–2026), 2021-esek 12,9 Mrd Ft — [NKE Navigátor 2022/1](https://ppi.uni-nke.hu/document/ppi-uni-nke-hu/Navigátor_2022_01.%20szám.pdf) (snippet; RÉGI)
- NKA: létezik 2025-ös nyitó kollégiumi keret-határozat (NKA Bizottság 9/2025. (III.05.)), de a magánszemélyek jogosultságát a talált dokumentum nem tárgyalja — [EMET melléklet](https://emet.gov.hu/app/uploads/sites/2/2025/05/Melleklet-az-NKA-Bizottsaga-9_2025.-III.05.-szamu-hatarozatahoz_1.-sz.-melleklet.pdf) (snippet)
- Bethlen Gábor Alap: a jogosultak szervezetek (civil szervezet, nonprofit társaság, állami intézmény, önkormányzat, egyházi jogi személy); a 2025-ös kiírások határon túli szervezetekre szólnak — [BGA általános útmutató 2022](https://bgazrt.hu/wp-content/uploads/palyazati_kiirasok/kulhoni_tamogatasok/2022/altalanos_palyazati_utmutato_kulhoni_tamogatasok_2022_20220420mod.pdf), [BGA 2025 ifjúsági kiírás](https://bgazrt.hu/wp-content/uploads/palyazati_kiirasok/kulhoni_tamogatasok/2025/palyazati_kiiras_jovo_nemzedeke_program_ifjusagi_2025.pdf) (snippet); egyes BGA-támogatások egyedi kérelemre, kormánydöntéssel születtek — [Telex 2026.04.21](https://telex.hu/transtelex/2026/04/21/magyarorszag-tamogatasok-fidesz-kormany-bethlen-gabor-alapkezelo-erdely-romania-rmdsz) (snippet)

**Európai**
- ERC Starting Grant: legfeljebb 1,5 M EUR / 5 év (+ legfeljebb 1 M EUR kiegészítés); 2–7 évvel a PhD után; befogadó intézmény (EU/társult ország) kötelező, amely a PI-t a projekt idejére alkalmazza — [UKRO 2026 ERC StG](https://www.ukro.ac.uk/wp-content/uploads/2025/07/2026_ERC_Starting_Grant_updated.pdf) (snippet); a határidőt a források eltérően adják (2025.10.14 vs. 2026.10.14) — [Valencia](https://www.uv.es/uvweb/research-service/en/news/erc-starting-grants-call-published-1285923509830/Novetat.html?id=1286499714013) vs. [Swiss Neuroscience](https://swissneuroscience.ch/the-erc-starting-grants-call-2026-is-now-open-submission-deadline-on-14-october-2025/)
- Az ERC finanszírozott bibliai digitális bölcsészeti munkát (pl. *Ancient Worlds in Digital Culture*, Brill, OA, 2016) — [OAPEN](https://library.oapen.org/handle/20.500.12657/29727) (RÉGI)
- A CLARIN nemzeti ága finanszírozott bibliai adatinfrastruktúrát (SHEBANQ, CLARIN-NL, 2013–14) — [KNAW Pure](https://pure.knaw.nl/portal/en/projects/shebanq/) (RÉGI, de precedens)

**Nemzetközi magán**
- John Templeton Foundation: „small grant” küszöb 234 800 USD (2019 körüli közlés, inflációval időnként igazítják); nincs nemzetiségi vagy karrierszakasz-korlát; intézményi kötést preferál, de ha ez nem megoldható, magánszemélynek is adhat — [Religious Studies Project, JTF PDF](https://www.religiousstudiesproject.com/wp-content/uploads/2019/08/John-Templeton-Foundation.pdf), [Grant Plant NM](https://www.thegrantplantnm.com/grant-detail/john-templeton-foundation/) (snippet; RÉGI, ellenőrizendő a templeton.org-on)
- Templeton Religion Trust: csak közvetett adat (az Acton Institute nemzetközi kutatói ösztöndíját támogatja) — [Acton](https://www.acton.org/international-research-grants) (snippet)
- Mellon és NEH a Perseus fő finanszírozói voltak (l. 1. pont) — az NEH amerikai intézményekre korlátozott (ez általános tudás, nem ellenőrzött).
- Tyndale House Foundation (USA, nem azonos a cambridge-i Tyndale House-zal) adott 27 000 USD-t a Clear Bible-nek — [CauseIQ](https://causeiq.com/organizations/clear-bible,812408473) (snippet, aggregátor)

### Inferences
- Egyéni, nem intézményi pályázó számára az NKKP és az ERC formálisan elérhetetlen befogadó nélkül; a legközelebbi út egy magyar teológiai felsőoktatási intézmény (pl. KRE, PPKE, Evangélikus Hittudományi Egyetem) mint befogadó — ez értelmezés, a konkrét intézményi hajlandóság nincs vizsgálva.
- Az NKKP-összegek (25–30 M Ft/év) nagyságrenddel meghaladják egy egyszemélyes adatprojekt költségét; a kisebb, gyorsabb források (NKA, egyházi, alapítványi) jobban illenek, de ezek feltételei nem tisztázottak.
- A STEPBible-modell (jótékonysági szervezet + önkéntesek + szervezet-partner) mutatja, hogy saját egyesület/alapítvány létrehozása megnyitja az NKA/BGA/egyházi pályázatokat — értelmezés.
- A nyílt licenc (CC BY / CC BY-SA, mint a MACULA és az SDBH) a STEPBible/Clear-partnerségek előfeltétele; az SDBH CC BY-SA-örökítése a repó adatára is kihat (a repó CLAUDE.md-je szerint).

### Gaps
- HUN-REN pályázatok magánszemélynek: nem kutatva.
- Egyházi kutatási alapok (Magyarországi Református Egyház, MKPK, MEE): nem találtam forrást.
- NKA aktuális kollégiumi kiírás magánszemélyes jogosultsága (Közgyűjtemények, Ismeretterjesztés, Könyvkiadás): nem tisztázott — emet.gov.hu ellenőrizendő.
- COST Action bibliai/ókori szövegekre: nem találtam aktív akciót; általánosan a COST-részvételhez nem kell finanszírozott intézmény, de ezt nem ellenőriztem forrással.
- Horizon Europe Cluster 2, DARIAH/CLARIN magyar ága (pl. HUN-REN NYTK CLARIN-HU), Erasmus+, Lilly Endowment, SIL/UBS partnerség: nem kutatva (eszközhívás-korlát).
- STEPBible partnerségi lehetőség (pl. a magyar Károli+Strong adat felvétele a STEP-be): a STEP önkéntes, „gateway language” modellje erre utal, de a felvételi eljárást nem vizsgáltam.
