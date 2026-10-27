# Előfizetéses (freemium/paywall) modell vs. önkéntes támogatói modell: konverzió, megtartás, elérés

*Forrásmegjegyzés: a WebFetch ebben a környezetben több elsődleges oldalt nem ért el (DNS-hiba: revenuecat.com, saastr.com, rocketshiphq.com, en.wikipedia.org). Az alábbi adatok jelentős része **keresési kivonatból** (snippet) származik, nem a teljes elsődleges dokumentumból; ahol ez így van, jelölöm. Számot nem találtam ki; ahol nincs forrás, a Hiányok szakaszba került.*

## 1. Freemium → fizetős konverziós benchmarkok (fogyasztói app, niche/szakmai SaaS)

### Lényeg (Takeaway)
A telepítésre vetített fizetős konverzió mobilappoknál Nyugat-Európában kb. 2% (D35 medián, 2026-os RevenueCat), az oktatási kategória az egyik leggyengébb; a freemium SaaS-ben az aktív/regisztrált felhasználóra vetített konverzió medián kb. 8%, de az EdTech-szegmensben ~2,6% (egy forrás szerint). A legsikeresebb fogyasztói freemium (Duolingo) is csak ~9%-ot ér el az aktív felhasználókból.

### Hivatkozott adatok (Cited Findings)
- **Telepítés→fizetős (D35), régiónként, minden kategória:** medián 2,6% Észak-Amerika, 2% Nyugat-Európa, 1,4% India/DK-Ázsia (RevenueCat State of Subscription Apps 2026; keresési kivonat, a teljes jelentést nem értem el) — [RevenueCat 2026](https://www.revenuecat.com/state-of-subscription-apps); [Medium-összefoglaló](https://chuvak-pavel.medium.com/state-of-app-monetization-2026-key-trends-from-revenuecat-and-adapty-8bdc23a4bb6f)
- **Oktatás kategória:** a 2025-ös jelentés szerint az Education a legalacsonyabb D35-konverziójú kategóriák egyike („high upfront engagement requirements”); konkrét számot a kivonat nem adott — [RevenueCat 2025](https://www.revenuecat.com/state-of-subscription-apps-2025)
- **Oktatás, 2026:** letöltés→próbaidőszak 6,5%; a próbaidő-lemondások 28,5%-a a 0. napon (ez a legalacsonyabb azonnali lemondási arány a kategóriák közt) — keresési kivonat — [RevenueCat 2026 Education](https://www.revenuecat.com/state-of-subscription-apps-2026-education)
- **Általános konverzió a fizetősig:** „fairly low at 1.7%” (RevenueCat-vezetők interjúja; az évet a kivonat nem azonosítja egyértelműen — bizonytalan) — [SaaStr](https://www.saastr.com/the-state-of-subscription-apps-with-revenuecats-ceo-jacob-eiting-and-growth-advocate-david-barnard)
- **Koncentráció:** a felső 5% app 400× több bevételt termel, mint az alsó 25% (előző évben 200×) — [Subscription Insider a 2025-ös jelentésről](https://subscriptioninsider.com/article-type/news/revenuecats-state-of-subscription-apps-2025-report-ais-dominance-retention-challenges-and-the-shift-away-from-pure-subscriptions); 80% mobilapp nem éri el a havi 1 000 USD előfizetési bevételt — [Start.io a RevenueCat-adatról](https://www.start.io/blog/report-80-of-mobile-apps-fail-to-earn-1000-month-in-subscription-revenue/)
- **Minta:** a 2026-os jelentés 115 000+ appot, 16+ mrd USD bevételt fed le — [SaaStr összefoglaló](https://saastr.com/the-top-10-learnings-from-revenuecats-state-of-subscription-apps-how-115000-mobile-apps-deliver-16b-in-revenue-whats-working-whats-quietly-killing-growth)
- **Freemium SaaS (felhasználó→fizetős):** medián 8%, széles szórás: ~25% a termékek közül 2,5% alatt, 29% 2,5–7,5% között, ~25% 10–15% (ChartMogul + Growth Unhinged + ProductLed, 2026; másodlagos forráson át) — [CrazyEgg](https://www.crazyegg.com/blog/free-to-paid-conversion-rate/); [Userpilot](https://userpilot.com/blog/freemium-to-premium)
- **Iparági szórás:** hagyományos freemium átlag 3,7%; EdTech 2,6%, RegTech 5,8% (FirstPageSage, másodlagos idézet) — [CrazyEgg](https://www.crazyegg.com/blog/free-to-paid-conversion-rate/)
- **Duolingo (aktív felhasználó→fizetős, auditált):** 2025 Q2: 10,9 M fizető előfizető, 128,3 M MAU; „Paid Subscriber Penetration” az LTM MAU-ra vetítve 9,0% (egy éve 8,6%); fizetők +37%, MAU +24% év/év — [Duolingo Q2 2025 levél, SEC](https://www.sec.gov/Archives/edgar/data/1562088/000156208825000165/q2fy25duolingo6-30x25share.htm); [10-Q](https://www.sec.gov/Archives/edgar/data/1562088/000156208825000168/duol-20250630.htm)
- **OpenView-benchmarkot nem találtam** (az OpenView 2023-ban megszűnt; a keresés nem hozta elő a jelentését).

### Következtetések (Inferences)
- Két nevező különböztetendő meg: *telepítés/látogató→fizetős* (≈1–3%) és *aktív felhasználó→fizetős* (SaaS-medián ≈8%, Duolingo ≈9%). Egy magyar niche olvasóappnál a reális kiindulópont a ≈2% (nyugat-európai mobil D35) körüli vagy alatta lévő érték, mert a kategória (oktatás/referencia) a gyengébbek közé tartozik, és Magyarország vásárlóereje a nyugat-európai átlag alatt van (ez utóbbi saját becslés, nem forrásolt).
- A „top 5% vs. alsó 25%” szakadék miatt az átlagos/mediánértékek is optimisták egy kis közönségű termékre: a niche appok többsége a medián alatt van.

### Hiányok (Gaps)
- Az Oktatás/Referencia kategória pontos D35-konverziója és havi churnje (a teljes RevenueCat-PDF nem volt elérhető).
- Kelet-Európa/Magyarország külön régiós adata a RevenueCat-ben — nem találtam.
- Bibliaszoftver-specifikus freemium-konverzió — nincs nyilvános adat.

## 2. Bibliaszoftver-előfizetések: Logos/Faithlife, Bible Gateway Plus, Olive Tree, Accordance, Blue Letter Bible

### Lényeg (Takeaway)
A Logos 2024-es előfizetéses átállásáról csak fórumos és értékelési reakciók nyilvánosak (erős elégedetlenség a régi vásárlóknál); előfizetőszámot vagy churnt a Faithlife nem közöl. A legnagyobb ingyenes, adományalapú bibliakutató oldal (Blue Letter Bible) saját bevallása szerint felhasználóinak kb. 0,1%-a támogatja anyagilag, és 17 évig egy alapítvány tartotta el.

### Hivatkozott adatok (Cited Findings)
- **Logos, 2024. október:** a perpetuális licencet előfizetéses szintek váltották; a korábban megvett könyvtár előfizetés nélkül is elérhető marad (Wikipedia, keresési kivonat; az oldalt közvetlenül nem értem el) — [Wikipedia: Logos Bible Software](https://en.wikipedia.org/wiki/Logos_Bible_Software)
- **Faithlife Connect fogadtatása:** felhasználók szerint a 8,99 USD/hó Faithlife Connect (a korábbi Logos Now árán) már nem tartalmazza a teljes eszköztárat; a teljes eszköztár „több mint kétszer” annyiba kerül; Faithlife-poszt szerint a cél „sustainable business”; a cég átmeneti hosszabbítást és (egy hozzászólás szerint) akár 200 USD-s kuponokat adott — [Logos fórum: „The Why”](https://community.logos.com/discussion/comment/957675); [Logos fórum](https://community.logos.com/discussion/comment/957185); [Logos fórum: path forward](https://community.logos.com/discussion/comment/958370)
- **Elégedetlenség:** „For the First Time I Regret Building a Library in Logos” fórumszál; Puritan Board-szál az átállásról; egy 2024. novemberi szálban felhasználó jelzi, hogy nem újít meg (anekdotikus, nem mért churn) — [Logos fórum](https://community.logos.com/forums/t/225854.aspx); [Puritan Board](https://puritanboard.com/threads/logos-is-switching-to-subscription-based-features.114291/); [Trustpilot](https://ca.trustpilot.com/review/logos.com)
- **Olive Tree:** hibrid — egyedi vásárlás + előfizetési csomagok: Study Pack 2,99–5,99 USD/hó, Commentary Select 8,99–19,99 USD/hó (havonta cserélhető kötetek) — [Olive Tree Subscriptions FAQ](https://help.olivetree.com/hc/en-us/articles/360052844031)
- **Accordance:** főként egyszeri vásárlás (modulok, csomagok); egy Accordance-munkatárs fórumposztja szerint egy esetleges előfizetés csak kiegészítő opció lenne, a közvetlen vásárlás helyett nem — [Accordance fórum](https://forums.accordancebible.com/topic/34253-subscriptionsmembership-feedback)
- **Blue Letter Bible:** az első 17 évben gyakorlatilag teljes finanszírozás a Sowing Circle alapítványtól; az éves költségigény 2 M USD-ra nőtt, ezért önálló, adománygyűjtő nonprofittá vált; ma főként egyéni adományokból, támogatásokból, hirdetésből és könyveladásból él; **„about one-tenth of one-percent of our users support BLB financially”** — [BLB: 20 éves áttekintés](https://www.blueletterbible.org/about/20open.cfm); [BLB donor info](https://www.blueletterbible.org/donorinfo)
- **BLB, 2022:** 3 699 233 USD összes támogatás és adomány; külön 575 000 USD Sowing Circle-támogatás — [Cause IQ](https://www.causeiq.com/organizations/blue-letter-bible,472951572/)
- **Bible Gateway Plus / YouVersion:** előfizetőszámot (BG Plus) nem találtam; a YouVersion ingyenes, adományból működik — erre ebben a menetben nem találtam friss elsődleges számot.

### Következtetések (Inferences)
- A bibliaszoftver-piacon a fizetős modellt a *nagy, kizárólagos, licencelt tartalom* (kommentárok, modern lexikonok) hordozza (Logos, Olive Tree, Accordance). A szabad/közkincs alapanyagra (KJV, Strong, BDB/Thayer) épülő szereplők (BLB) ingyenesek és adományból/alapítványból élnek. A magyar projekt a második csoporthoz áll közelebb: a BDB/Thayer magyar fordítása saját munka, de a forrásszöveg közkincs.
- A BLB 0,1%-os támogatói aránya felső korlátként is tanulságos: egy nagy, ismert, angol nyelvű oldal sem tud a felhasználói töredékénél többet anyagi támogatóvá tenni.
- A Logos-eset azt mutatja, hogy a már ingyen/megvett funkció *utólagos* fizetőssé tétele erős bizalmi kárt okoz a legelkötelezettebb felhasználóknál — releváns, ha a magyar projekt később zárna el ma nyílt réteget.

### Hiányok (Gaps)
- Faithlife előfizetőszám, churn, bevétel — nem nyilvános (magáncég), nem találtam.
- Bible Gateway Plus előfizetőszám és ár — a keresés nem hozta.
- Olive Tree / Accordance előfizetési arányok — nincs adat.

## 3. Paywall vs. önkéntes modell: hírmédia és nyílt projektek

### Lényeg (Takeaway)
A hírmédia-paywallok a látogatók kb. 0,2%-át konvertálják (Piano, 2024. dec.); a Guardian önkéntes modellje 1,4 M rendszeres digitális támogatóig jutott paywall nélkül. Magyarországon az online hírekért fizetők aránya alacsony (8% egy korábbi, 14% egy későbbi, nem azonosított évű DNR-kiadás szerint).

### Hivatkozott adatok (Cited Findings)
- **Piano, 2024. december:** konverziós arány 0,20% (USA 0,34%, Európa 0,15%); a látogatók 16,3%-a látott fizetős ajánlatot — [Piano-előadás, NYPA 2025. március (PDF)](https://nynewspapers.com/wp-content/uploads/2025/04/Mar2025_NYPA_Benchmarks_Belyus.pdf) (keresési kivonat)
- **Piano 2021:** anonim felhasználók konverziója 0,22% (a közönség >90%-a); a kemény paywall 10× jobban konvertál, mint a puha — [MediaPost](https://www.mediapost.com/publications/article/363006/hard-paywalls-have-higher-conversion-rates-than-so.html); [Piano 2021](https://resources.piano.io/articles/pianos-subscription-benchmarks-spring-2021) *(régebbi adat)*
- **Poool:** a paywallra kattintók 2,45%-a fizet elő (más nevező, nem látogatószintű) — keresési kivonat — [The Audiencers](https://theaudiencers.com/the-conversion-funnel-benchmark-report-q3-2023/)
- **Guardian (önkéntes, paywall nélkül):** 2025. márciusig 1,3 M rendszeres támogató (+13%), digitális olvasói bevétel 107 M GBP (+22%); 2026. márciusig 1,4 M (+116 000), 126 M GBP (+17%) — [Press Gazette](https://pressgazette.co.uk/media_business/guardian-reports-bumper-year-for-digital-reader-revenue/); [InPublishing, 2025/26 beszámoló](https://inpublishing.co.uk/articles/guardian-media-group-publishes-202526-statutory-accounts-26908)
- **Reuters DNR 2025:** a gazdagabb országokban 18% fizet online hírért (stagnál), Norvégia 42%, USA 20% — [AcademicJobs-összefoglaló](https://www.academicjobs.com/higher-education-news/reuters-digital-news-report-2025-48-markets-habits-or-academicjobs-1352) (másodlagos)
- **Magyarország:** 8% fizetett online hírért egy korábbi DNR-kiadásban; egy későbbi (évszám nem azonosított, 46 ország/92 000 fős mintával) 14% — [BBJ](https://bbj.hu/analysis/hungarians-increasingly-distrust-mainstream-media-_150977); [Daily News Hungary](https://dailynewshungary.com/reuters-institute-hungarians-do-not-trust-the-news/) — *a 2025-ös magyar számot nem tudtam megerősíteni*
- **Wikipedia (önkéntes, nyílt):** 2023/24-ben 8 M+ adományozó, átlag 10,58 USD; 2024/25-ben csökkent az adományozók száma (az emberi forgalom csökkenésével), de a maradók többet adtak — [Wikimedia Fundraising 2024-25 Report](https://meta.wikimedia.org/wiki/Fundraising/2024-25_Report); [2023-24 Report](https://meta.wikimedia.org/wiki/Fundraising/2023-24_Report)
- **Sefaria (ingyenes, nyílt zsidó szövegtár — legközelebbi analóg):** 2022-es költségvetés közel 5 M USD; 2025-ös cél 2 M USD a Giving Circle-tagoktól; a Jim Joseph Foundation összesen 9,75 M USD-t adott; 2024 márciusában 44 M USD-s kampány, ebből 14 M összegyűlt; nyílt forráskód — [RNS 2023](https://religionnews.com/2023/08/28/10-year-old-jewish-digital-library-revolutionizes-the-people-of-the-book/); [Sefaria Giving Circle](https://help.sefaria.org/hc/en-us/articles/21723740784028-How-to-Join-a-Sefaria-Giving-Circle); [Jim Joseph Foundation](https://jimjosephfoundation.org/grants/sefaria-general-operating-support/); [eJP](https://ejewishphilanthropy.com/delayed-by-israel-hamas-war-sefaria-holds-sold-out-10th-anniversary-gala/)

### Következtetések (Inferences)
- A hírpiaci adat szerint a paywall *a látogatók* ezreléknyi hányadát konvertálja; a Guardian-modell mutatja, hogy önkéntes alapon is lehet nagy fizetőbázist építeni, ha az elérés nagy és a misszió világos — kis közönségnél viszont mindkét modell abszolút száma kicsi.
- A Sefaria a legjobb szerkezeti analóg (nyílt szövegtár + kutatási réteg, vallási közösség): alapítványi + nagyadományozói + közösségi (Giving Circle) mix, **nem** paywall.

### Hiányok (Gaps)
- Olyan nyílt-adat projekt, amely paywallt vezetett be, és mért eredményt közölt — nem találtam.
- Magyar hírmédia-paywall konverziós adat (pl. 444, Telex, HVG) — ebben a menetben nem kerestem/nem találtam.

## 4. A paywall hatása az elérésre/befolyásra (kutatási erőforrásnál)

### Lényeg (Takeaway)
A paywall bevezetése mérhetően csökkenti a forgalmat (oldalletöltés és egyedi látogató egyaránt); a nyílt hozzáférés idézettségi előnye viszont a legátfogóbb szisztematikus áttekintés szerint ellentmondásos, nem bizonyított.

### Hivatkozott adatok (Cited Findings)
- **Lektorált vizsgálat (Journalism Studies, 2020):** 8 helyi hírportál (4 norvég, 4 dán), 52 hét a paywall előtt és után: az oldalletöltések és az egyedi látogatók is csökkentek; a kemény paywall azonnali hatása erősebb, a különbség idővel kiegyenlítődik; a szerzők a civil szerep gyengülését is jelzik — [RUC](https://forskning.ruc.dk/da/publications/paywalls-impact-on-local-news-websites-traffic-and-their-civic-an/); [BI Open](https://biopen.bi.no/bi-xmlui/handle/11250/2688949)
- **NYT 2011 (régi adat):** Hitwise szerint a látogatások 5–15%-kal, az oldalletöltések 11–30%-kal estek a bevezetés körüli 12 napban; a kereső- és közösségi hivatkozási arány nem változott jelentősen — [Search Engine Watch](https://searchenginewatch.com/2011/04/12/hitwise-reports-paywall-causes-decrease-in-overall-visits-to-nytimes-com)
- **Newsday 2010 (régi adat):** egyedi látogatók −21%, oldalletöltés −34% az első hónapban — [CJR](https://www.cjr.org/?p=77550)
- **OA-idézettségi előny:** Langham-Putrow, Bakker & Riegelman (PLOS ONE 2021, 16(6): e0253129) — szisztematikus áttekintés (nem metaanalízis), 134 tanulmány, 17 adatbázis: az eredmények „contradictory and inconclusive”; az eltérés oka az OA-típusok különbsége és a definíciók/metrikák egységesítésének hiánya — [PLOS ONE](https://journals.plos.org/plosone/article%3Fid=10.1371/journal.pone.0253129); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8221498)
- **Újabb munka:** az OA-előny felbontása interdiszciplináris idézésre (arXiv 2024) — [arXiv 2411.14653](https://arxiv.org/pdf/2411.14653) (csak címszinten láttam)

### Következtetések (Inferences)
- Egy kutatási adatforrásnál a forgalom-/elérésveszteség a paywall dokumentált következménye; a „több idézet” érv a nyílt modell mellett viszont nem támasztható alá szilárdan, inkább a forgalmi/keresőbeli láthatósági érv erős.
- A prémiumrétegbe tervezett tartalom (motívumlexikon-oldalak, kutatási döntések) épp az a szöveges, kereshető tartalom, amely a keresőből érkező forgalmat és a hivatkozhatóságot hordozná; elzárásával a projekt fő terméke (a lexikon, CLAUDE.md szerint) válik láthatatlanná.
- Licencmegjegyzés (a repóból, nem webkutatás): az SDBH/SDGNT adatok CC BY-SA 4.0 alatt vannak; az ezekből származó mű fizetős rétegbe tehető, de a share-alike miatt a fizető felhasználó azt szabadon továbboszthatja — ez gyengíti a paywall kizáró erejét. Jogi ellenőrzést igényel.

### Hiányok (Gaps)
- SEO/forgalomvesztés kutatási/referencia oldal (nem hírportál) paywallja után — nem találtam mért esetet.

## 5. Megtartás/churn: fizetős előfizetés vs. rendszeres adomány

### Lényeg (Takeaway)
Az éves előfizetők ~30%-a az első hónapban lemond (RevenueCat); a digitális média előfizetéses churn kb. 4%/hó (Recurly, másodlagos). Adományoknál az FEP szerint az összesített megtartás ~43%, az új adományozóké ~19% — de a *rendszeres (havi) adományozók* lényegesen tartósabbak (Neon One: átlagos élettartam 7,8 év vs. 1,65 év egyszeri adományozónál).

### Hivatkozott adatok (Cited Findings)
- **Éves előfizetés korai lemondása:** ~30% az első hónapban (RevenueCat 2025) — [Subscription Insider](https://subscriptioninsider.com/article-type/news/revenuecats-state-of-subscription-apps-2025-report-ais-dominance-retention-challenges-and-the-shift-away-from-pure-subscriptions)
- **Próbaidő:** a 3 napos próbák lemondásainak 55%-a a 0. napon (RevenueCat 2026) — [SaaStr összefoglaló](https://saastr.com/the-top-10-learnings-from-revenuecats-state-of-subscription-apps-how-115000-mobile-apps-deliver-16b-in-revenue-whats-working-whats-quietly-killing-growth) (keresési kivonat)
- **Digitális média churn:** 4,14% összesen, ebből 1,59 pont nem szándékos (fizetési hiba) — Recurly-benchmark, másodlagos forráson át — [Voxbooster](https://voxbooster.com/blog/patreon-creator-retention-membership-statistics-2026)
- **FEP 2025 Q4 (Bloomerang közlése):** összesített adományozói megtartás 43,3%, ismétlő adományozóké 59,3%, új adományozóké 18,9% — a források eltérnek (Q3 2025 YTD-adat: 31,9% / 43,6% / 14,0%, eltérő időszak) — [DonorPerfect](https://www.donorperfect.com/nonprofit-technology-blog/fundraising-software/afp-fep-q4-2025/); [Bloomerang](https://bloomerang.com/blog/the-state-of-donor-retention-in-one-image) — *az FEP-jelentést közvetlenül nem láttam*
- **Rendszeres adományozó (Neon One, nem FEP):** átlagos élettartam 7,8 év (2025), egyszeri adományozó 1,65 év — [Neon One](https://neonone.com/?p=60020)
- **Patreon:** a platform nem közöl churnt; marketingforrás szerint 3 hónapos megtartás 65% = „jó”, 78% = „kiváló” (forrásolatlan) — [Bonjoro](https://www.bonjoro.com/blog/post/how-a-patreon-creator-maintains-a-98-retention-rate); ICWSM 2022 (El Sanyoura & Anderson) szerint a több alkotót támogató patronok jobban megmaradnak (másodlagos idézet) — [Voxbooster](https://voxbooster.com/blog/patreon-creator-retention-membership-statistics-2026)

### Következtetések (Inferences)
- A rendszeres (havi, automatikus) önkéntes támogatás megtartása nem rosszabb, sőt a Neon One-adat szerint jobb, mint az egyszeri adományé; a különbség a fizetős előfizetéshez képest nem a churnben, hanem a *bázis méretében* van.
- A FEP-számok (főleg egyszeri, éves adományokra) nem vethetők közvetlenül össze a havi előfizetéses churnnel — eltérő mértékegység (éves megtartás vs. havi lemorzsolódás).

### Hiányok (Gaps)
- Magyar rendszeres adományozói megtartási adat — nem találtam.
- Patreon hiteles, platformszintű churnje — nem nyilvános.

## 6. Hibrid modellek (freemium + adomány, „támogatás, ami fel is old”)

### Lényeg (Takeaway)
A sikeres nyílt tudásforrások (Wikipedia, Sefaria, BLB) teljesen ingyenes tartalommal + önkéntes/alapítványi finanszírozással működnek; a fizetős prémium (Duolingo Super) nagy, tömeges közönségre épül, ahol a 9%-os penetráció is milliós fizetőbázist jelent. A Sefaria Giving Circle-je tagsági juttatásokat ad, de nem zár el tartalmat.

### Hivatkozott adatok (Cited Findings)
- Duolingo: 9,0% fizetős penetráció 128,3 M MAU mellett (2025 Q2) — [SEC](https://www.sec.gov/Archives/edgar/data/1562088/000156208825000165/q2fy25duolingo6-30x25share.htm)
- Sefaria Giving Circle: sávos tagsági juttatások adományméret szerint, a tartalom ingyenes marad — [Sefaria Help](https://help.sefaria.org/hc/en-us/articles/21723740784028-How-to-Join-a-Sefaria-Giving-Circle)
- Wikipedia: átlag ~11 USD egyéni olvasói adomány — [Wikimedia Fundraising](https://meta.wikimedia.org/wiki/Fundraising)
- Olive Tree: egyedi vásárlás + előfizetés párhuzamosan — [Olive Tree FAQ](https://help.olivetree.com/hc/en-us/articles/360052844031)

### Következtetések (Inferences)
- **A tulajdonos érvének (≈3 400–3 650 Ft/hó átlagos támogatói befizetés → ugyanennyit fizetnének előfizetésként) gyenge pontja:** az átlagos befizetés a már *önszelektált* támogatók viselkedését írja le (akik misszióért fizetnek, gyakran az átlagosnál többet). Nem mond semmit arról, hogy a felhasználók hány százaléka fizetne kényszerből egy hozzáférésért. A konverziós arány (nevező) a döntő változó, nem az átlagos összeg: paywallnál a benchmarkok 0,2% (látogató) – 2% (telepítés) – ~8% (aktív freemium-felhasználó, SaaS-medián) sávban vannak, az oktatási/EdTech szegmens a sáv alján.
- Kis, niche magyar közönségnél (a teljes potenciális fizetőbázis néhány ezer fő nagyságrend — *saját becslés, nem forrásolt*) a paywall az elérést csökkenti (4. pont), miközben a fizetők abszolút száma valószínűleg csak kicsivel nőne a támogatói modellhez képest — ez a hírmédia-, BLB- és Duolingo-adatokból levont következtetés, nem mért eredmény.
- Hibrid középút analógiák alapján: minden tartalom nyílt, a támogatók kényelmi/közösségi juttatást kapnak (korai hozzáférés, letölthető exportok, névsor, Q&A) — a Sefaria Giving Circle és a Guardian mintájára.

### Hiányok (Gaps)
- Britannica fizetős vs. Wikipedia összehasonlító forgalmi/bevételi adat — ebben a menetben nem kerestem meg.
- Khan Academy adományozói arány — nem kerestem meg.
- Olyan vallási/bibliai magyar nyelvű digitális projekt fizetős vagy támogatói számai, amelyekkel kalibrálni lehetne — nem találtam.
