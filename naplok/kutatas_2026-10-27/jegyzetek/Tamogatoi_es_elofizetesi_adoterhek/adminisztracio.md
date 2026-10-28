# Visszatérő adminisztratív és megfelelőségi teher: (A) önkéntes támogatói/adomány modell vs. (B) fizetős digitális előfizetés — Magyarország, 2025–2026

**Módszertani megjegyzés (fontos a report-írónak):** Ebben a menetben a WebFetch és a curl
minden elsődleges forrásnál elbukott (DNS / proxy `connect_rejected`: njt.jog.gov.hu, nav.gov.hu,
eur-lex.europa.eu, szamlazz.hu, adozona.hu). **Minden alább idézett „Cited Finding” keresési
találat-kivonatra (snippet) épül, nem a teljes oldal elolvasására.** A jogszabályhelyek egy része
háttértudásból származik; ezek **nem** a Cited Findings alatt, hanem az Inferences alatt állnak,
„[háttértudás, nem ellenőrizve]” jelöléssel. Nem jogi és nem adótanácsadás. Minden óra- és
forintbecslés **[becslés]**.

## 1. Bizonylatolás: számla vs. nyugta, NAV Online Számla, pénztárgép, számlázó-integrációk; adomány bizonylatolása

### Takeaway
(B)-ben minden előfizetési díjról bizonylat kell; a gyakorlatban a legegyszerűbb és legelterjedtebb út a fizetési szolgáltató webhookjára automatikusan kiállított elektronikus számla (amely NAV-adatszolgáltatással jár, de ezt a számlázó automatikusan intézi), így havonta előfizetőnként egy számla keletkezik (pl. 300 előfizető ≈ 3 600 számla/év). (A)-ban a tiszta (ellenszolgáltatás nélküli) adományról nem kell számla; cégtámogatónak közhasznú alapítvány adhat adományigazolást.

### Cited Findings
- Áfa tv. 165. § (1) b): mentesül a számlakibocsátás alól az adóalany, ha a vevő az ellenértéket a teljesítésig készpénzzel, **készpénz-helyettesítő fizetési eszközzel** vagy pénzhelyettesítő eszközzel megfizeti és számlát nem kér; ekkor a 166. § (1) szerint nyugtát kell kibocsátani; a 166. § (2) szerint az adóalany saját döntése alapján nyugta helyett számlát is adhat, ekkor NAV felé adatszolgáltatási kötelezettsége keletkezik — [Adózóna találatai a 165–166. §-ról (snippet)](https://adozona.hu/afa/Itt_a_valasz_mikor_kell_es_mikor_nem_kell_n_O05W8F); [NAV 2020/8. adózási kérdés (snippet)](https://nav.gov.hu/ado/afa/2020_8__Adozasi_kerde20200708_ref1)
- Szakértői válaszok **ellentmondanak** egymásnak abban, hogy a bankkártyás fizetés „készpénz-helyettesítő” fizetésnek minősül-e a nyugtaadás szempontjából (egyik szerint igen, nyugta adható; másik szerint a bankkártyás ügylet nem készpénzfizetéses értékesítés) — [Adózóna, készpénzhelyettesítő címke (snippet)](https://adozona.hu/cimke/k%c3%a9szp%c3%a9nzhelyettes%c3%adt%c5%91)
- Nyugtakibocsátás feltétele többek közt: a vevő nem adóalany és nem jogi személy, a vételár nem éri el a 900 ezer Ft-ot, és nem kér számlát; egy ügyletről egyféle bizonylat készül — [NAV 2020/8. adózási kérdés (snippet)](https://nav.gov.hu/ado/afa/2020_8__Adozasi_kerde20200708_ref1); [Adózóna, nyugta címke (snippet)](https://adozona.hu/cimke/nyugta/13)
- A 48/2013. (XI. 15.) NGM rendelet szerint a nyugtaadási kötelezettséget **csak az 1. mellékletben felsorolt tevékenységeknél** kell kizárólag pénztárgéppel teljesíteni; ha az adóalany nyugta helyett számlát ad, a gépi nyugtaadás alól mentesül, és elektronikus bejelentési/adatszolgáltatási kötelezettsége van (PTGSZLAB/PTGSZLAA nyomtatványok) — [Pothaczki Dóra: Az online pénztárgépre vonatkozó szabályozás rejtelmei, Jogi Fórum (snippet)](https://www.jogiforum.hu/files/publikaciok/pothaczki_dora__az_online_penztargepre_vonatkozo_szabalyozas_rejtelmei[jogi_forum].pdf); [48/2013 NGM rendelet, Adózóna jogtár (snippet)](https://adozona.hu/jogtar/401076_48_2013_XI_15_NGM_rendelet_penztargepek/255070)
- 2025-ben e-pénztárgépekről szóló NGM-rendelettervezet jelent meg a kormany.hu-n (státusza nem ellenőrzött) — [kormany.hu tervezet PDF (snippet)](https://cdn.kormany.hu/uploads/document/4/46/46d/46d2845d2454a06890e6cce799e58c82063d6944.pdf); később „hatályba lépett a rendelet” címmel Adózóna-cikk is megjelent — [Adózóna: E-pénztárgépek (cím)](https://adozona.hu/afa/Epenztargepek_hatalyba_lepett_a_rendelet_ki_6MBB2F)
- Számlázz.hu csomagdíjak (harmadik fél szerint, éves fizetésnél, nettó): #free 0 Ft, #start 20 280 Ft/év, #digital 29 880 Ft/év, #profi 39 480 Ft/év; havi fizetésnél más összegek; az API (Számla Agent) díja a havi bizonylatszámtól függ (sávok nem láthatók) — [Quasa: Billingo vagy Számlázz.hu (snippet; ellenőrizendő a hivatalos árlapon)](https://quasa.io/hu/media/billingo-vagy-szamlazzhu-az-api-es-a-szamlamennyiseg-donti-el)
- A Számla Agent (API) használata külön díjköteles; lejárt előfizetés vagy fizetési késedelem esetén az Agent letiltható — [docs.szamlazz.hu Agent](https://docs.szamlazz.hu/agent/basics/what-is); [Számlázz.hu jogosultságok 2025-06 PDF](https://www.szamlazz.hu/wp-content/uploads/2025/07/jogosultsagok-2025-06.pdf); [szamlazzhu Go-könyvtár README](https://pkg.go.dev/sixhz.com/szamlazzhu)
- A Stripe nem bank; a könyveléshez nem ad bankszámlakivonat-szerű dokumentumot, jellemzően Excel-export vagy képernyőkép — [Adózóna kérdés: Stripe fizetés elszámolása (snippet)](https://adozona.hu/kerdesek/2023_9_13_Stipe_fizetes_elszamolasa_uir)
- Adományigazolás (Tao-kedvezményhez): a támogatott szervezet adja ki; tartalmazza a kiállító és a támogató adószámát, az összeget, a célt, és hogy az adóalap megállapításához készült; csak **közhasznú** szervezet állíthat ki — [Adózóna: Közhasznú szervezetnek juttatott adomány (snippet)](https://adozona.hu/tarsasagi_ado_innovacios_jarulek/Kozhasznu_szervezetnek_juttatott_adomany_ig_UA46FB); [Adózóna: Nélkülözhetetlen igazolások (snippet)](https://adozona.hu/tarsasagi_ado_innovacios_jarulek/Nelkulozhetetlen_igazolasok_nyilatkozatok_a_7KEODJ)
- Előfordul, hogy támogató cég számlát kér az adományról; erről külön Adózóna-cikk szól („Amikor hiába követelik a számlaadást”), a válasz szövege nem volt elérhető — [Adózóna (cím)](https://adozona.hu/afa/Amikor_hiaba_kovetelik_a_szamlaadast_az_nem_VAVUIE)

### Inferences
- [háttértudás, nem ellenőrizve] 2021. január 1-jétől **minden** belföldi adóalany által kiállított számla adatát (B2C-t is) jelenteni kell a NAV Online Számla rendszerbe; a Számlázz.hu/Billingo ezt automatikusan, valós időben elvégzi a NAV technikai felhasználó beállítása után. A nyugta nem jelentendő az Online Számlába (pénztárgépes nyugta a pénztárgépen át megy).
- [értelmezés] Online, kártyás előfizetésnél a gyakorlatban a **számla** a biztonságos út: (a) a nyugta-jogosultság a kártyás fizetésnél vitatott (l. fent), (b) a 48/2013 NGM 1. melléklete jellemzően kiskereskedelmi/vendéglátó TEÁOR-okat sorol fel — hogy egy online előfizetési szolgáltatás szerepel-e, **nem ellenőriztem** (Gap); (c) a számla automatizálható és NAV-ra magától jelentődik. Kiskereshez egyéni vállalkozóként alanyi áfamentességnél is számla/nyugta kell, csak áfa nélkül.
- [értelmezés] Volumen: 300 előfizető × 12 hó = 3 600 számla/év; 1 000 előfizető = 12 000/év. Ez a Számlázz.hu/Billingo API-díjsávjait érinti — a sávokat nem sikerült ellenőrizni. Kézzel ez kezelhetetlen; integráció nélkül **nem** javasolt B.
- [értelmezés] Integráció: Stripe → webhook (`invoice.paid`) → saját kis szolgáltatás → Számla Agent / Billingo API → számla e-mailben. A Barion és SimplePay hazai szolgáltatók; Számlázz.hu/Billingo „kész” integrációját egyiknél sem tudtam megerősíteni (Gap). A Patreon (A-ban) saját maga nyugtáz a támogatónak; a projekt a Patreon-kifizetést egy tételben kapja.
- [értelmezés] Tiszta adomány (ellenszolgáltatás nélkül) nem áfa-köteles ügylet, ezért nem kell róla számla; a könyvelésben banki kivonat + (opcionálisan) adományigazolás a bizonylat. **Ha az adományért viszonzás jár (korai hozzáférés stb.)**, felmerülhet, hogy az részben ellenérték → áfa- és számlaköteles szolgáltatásnyújtás. Ezt a report jelölje nyitott értelmezési kockázatként.
- [háttértudás, nem ellenőrizve] Alapítványnál a kettős könyvvitel / egyszerűsített beszámoló szerinti nyilvántartás kell (adományok cél szerinti/vállalkozási elkülönítése); az SZJA 1%-os összeg elkülönített nyilvántartása.

### Gaps
- A 48/2013 NGM 1. mellékletének hatályos szövege és az e-pénztárgép-rendelet (2025) részletei: a forrásoldal nem volt letölthető.
- NAV hivatalos álláspontja arról, hogy interneten bankkártyával fizetett szolgáltatásnál elég-e nyugta (és milyen formában, pl. e-nyugta) — nem találtam egyértelmű elsődleges forrást.
- Számlázz.hu Agent-díjsávok, Billingo 2025–26-os árai és API-díjai, Barion/SimplePay integrációk: hivatalos árlap nem volt elérhető.

## 2. Fogyasztóvédelem a (B) modellnél: ÁSZF, elállás és lemondás, digitális tartalom, megújulás, elállási gomb, ár, panaszkezelés

### Takeaway
2026. június 19. óta a 45/2014. Korm. rendelet (a 415/2025. (XII. 23.) Korm. rendelettel módosítva) előírja az „elállás a szerződéstől” feliratú online elállási funkciót az elállási időszak alatt. Ez minden méretű vállalkozásra vonatkozik, tehát egy (B) előfizetéses PWA-nak is be kell építenie az ÁSZF/elállási nyilatkozat, a digitális tartalomra vonatkozó elállás-lemondás és a panaszkezelés mellé.

### Cited Findings
- A 45/2014. (II. 26.) Korm. rendelet módosítását a **415/2025. (XII. 23.) Korm. rendelet** végezte; az elállási funkció 2026. június 19-től kötelező; a 22. § új (1a)–(1c) bekezdéssel bővül: (1a) az elállási funkció egyértelműen megfogalmazott, könnyen olvasható online elállási nyilatkozat; (1b) a vállalkozás az **„elállás a szerződéstől”** szöveggel, jól látható és könnyen hozzáférhető módon, az elállási időszak alatt folyamatosan elérhetővé teszi; a hagyományos elállási módok megmaradnak — [fogyasztobarat.hu](https://fogyasztobarat.hu/kotelezo-az-online-elallasi-gomb-a-webshopokban-2026-junius-19-tol/); [virtualjog.hu](https://virtualjog.hu/2026/05/21/online-elallasi-gomb-webshop-2026/); [drnagyildiko.hu](https://drnagyildiko.hu/blog/webshop-elallasi-gomb-szabalyozas/); [Jogtár: 45/2014 hatályos szöveg](https://net.jogtar.hu/jogszabaly?docid=a1400045.kor) (mind snippet)
- **Forrásellentmondás:** a kormany.hu-n közzétett módosítási szöveg a rendelet számának helyén „…/2026” jelölést hordoz (tervezet-változat) — [kormany.hu dokumentum (snippet)](https://kormany.hu/application/documents/84449865-26fd-4689-906c-48c0f9fc8367/download). A 415/2025-ös számot több másodlagos forrás egybehangzóan adja.
- A kötelezettség a vállalkozás méretétől függetlenül minden érintett szereplőre vonatkozik — [Világgazdaság 2026/06 (snippet)](https://www.vg.hu/vilaggazdasag-magyar-gazdasag/2026/06/elallas-gomb-magyar-webaruhaz); [Origo 2026/06](https://www.origo.hu/gazdasag/2026/06/elallasi-gomb-webaruhaz-jogszabaly)
- A gomb nem új jogot teremt, hanem a meglévő 14 napos elállási jog elektronikus gyakorlását teszi lehetővé — [easecert.com (kereskedelmi forrás, óvatosan)](https://easecert.com/hu/pages/eu-withdrawal-button-requirement-2026-complete-guide-for-online-sellers)
- 373/2021. (VI. 30.) Korm. rendelet: a fogyasztó és vállalkozás közötti, digitális tartalom szolgáltatására és digitális szolgáltatás nyújtására irányuló szerződések részletes szabályai; hatálya kiterjed arra, ha a fogyasztó kifizeti vagy vállalja a vételár kifizetését — [njt.jog.gov.hu 2021-373 (snippet)](https://njt.jog.gov.hu/jogszabaly/2021-373-20-22)
- Gyakorlati ÁSZF-minta: a fogyasztó az elállási jogáról a 45/2014 2. melléklete szerinti nyilatkozattal mondhat le digitális tartalomnál, ezt követően elállási joga megszűnik (üzleti dokumentum, nem jogszabály) — [chatt.hu elállási nyilatkozat PDF](https://chatbot-main-ovpjd1.laravel.cloud/legal/2026-07-01/elallasi-nyilatkozat.pdf)

### Inferences
- [háttértudás, nem ellenőrizve] Kötelező elemek (B): ÁSZF (Ptk. 6:77–6:81 ÁSZF-szabályok, 2001. évi CVIII. Ekertv. 5–6. § tájékoztatás, a rendelés elektronikus visszaigazolása); a 45/2014 11. § szerinti szerződéskötés előtti tájékoztatás (ár áfával, időtartam, automatikus megújulás, felmondás feltételei, digitális tartalom funkcionalitása és interoperabilitása); a „fizetési kötelezettséggel járó megrendelés” gomb felirata (45/2014 21. §); visszaigazolás tartós adathordozón.
- [háttértudás, nem ellenőrizve] Elállás: 14 nap; nem tárgyi adathordozón nyújtott digitális tartalomnál a 45/2014 29. § (1) m) szerint az elállási jog akkor szűnik meg, ha a teljesítés a fogyasztó **kifejezett előzetes beleegyezésével** és annak tudomásulvételével kezdődött, hogy elveszíti az elállási jogát, és a vállalkozás ezt visszaigazolta. *Digitális szolgáltatásnál* (folyamatos hozzáférés, ami egy előfizetéses PWA inkább) a kivétel szabálya eltérhet (szolgáltatásnál arányos díj) — ez **ellenőrizendő**, mert a 2026-os gomb éppen az elállási időszak alatt kell, hogy látható legyen.
- [háttértudás, nem ellenőrizve] 373/2021 / (EU) 2019/770: szerződésszerűség, **frissítési kötelezettség** (biztonsági és funkcionális frissítések a szolgáltatás idejére), kellékszavatosság digitális tartalomra, egyoldalú módosítás feltételei (indok az ÁSZF-ben, előzetes értesítés, felmondási jog), offline titkosított cache esetén is a megígért funkcionalitás.
- [háttértudás, nem ellenőrizve] Panaszkezelés (Fgytv. 17/A §): írásbeli panaszra 30 napon belül indokolt válasz; jegyzőkönyv/panasz 3 év (régebben 5 év) megőrzése — **megőrzési idő ellenőrizendő**; a lakóhely szerinti békéltető testületről tájékoztatás; a békéltető eljárásban együttműködési (válaszirat) kötelezettség.
- [értelmezés] Automatikus megújulás: az uniós és magyar szabály szerint átlátható tájékoztatás (ár, ciklus, lemondás módja) a megrendelés előtt; a lemondásnak legalább olyan könnyűnek kell lennie, mint a feliratkozásnak (fogyasztóvédelmi gyakorlat; magyar jogszabályhely nem ellenőrzött).
- [értelmezés] Az elállási gomb technikai teendő: egyszeri fejlesztés (~ egy fiókoldal + visszaigazoló e-mail), utána folyamatos teher alig; de minden elállás → visszatérítés-ügyintézés + sztornó-/helyesbítő számla.

### Gaps
- A 45/2014 22. § (1c) és a 2. melléklet módosított szövege; hogy az elállási funkció digitális tartalomnál a 29. § m) szerinti lemondás után is megjelenítendő-e.
- Hivatalos NFFH/kormányhivatali útmutató az elállási gombhoz előfizetéseknél — nem találtam.

## 3. (A) modell előnyökkel („perk”): alkalmazandó-e a fogyasztóvédelmi jog?

### Takeaway
Erre nem találtam elsődleges forrást; **értelmezési kérdés**: ha a támogatás fejében tényleges szolgáltatás jár (korai hozzáférés), az ügylet ellenérték fejében nyújtott (digitális) szolgáltatásnak minősülhet.

### Cited Findings
- A 373/2021 hatálya ott nyílik meg, ahol a vállalkozás digitális tartalmat/szolgáltatást nyújt **és** a fogyasztó kifizeti vagy vállalja a vételárat — [njt.jog.gov.hu 2021-373 (snippet)](https://njt.jog.gov.hu/jogszabaly/2021-373-20-22)

### Inferences
- [értelmezés — jelölendő] Ha a „perk” csak jelképes (köszönőlista, hírlevél, amely mindenkinek elérhető), az adomány jellege megmarad, fogyasztói szerződés valószínűleg nincs. Ha a perk a fizetéstől függő, máshogy el nem érhető hozzáférés (korai hozzáférés), az könnyen visszterhes szolgáltatásnak minősül → fogyasztóvédelmi, áfa- és számlázási kötelezettségek. Egy alapítvány esetén ez ráadásul **vállalkozási tevékenység** (cél szerinti tevékenységtől elkülönítendő).
- [értelmezés] Kockázatcsökkentés: a perkek legyenek nem kizárólagosak (pl. korai hozzáférés mindenki számára kérhető), vagy a perk legyen nem pénzfüggő; ha Patreonon fut, a Patreon a szerződő fél a támogatóval szemben (merchant of record jelleg — **nem ellenőrzött**).

### Gaps
- Magyar hatósági/bírósági gyakorlat „ellenszolgáltatással járó adomány” fogyasztóvédelmi minősítésére — nem találtam.

## 4. GDPR mindkét modellben

### Takeaway
Mindkét modellben kell adatkezelési tájékoztató, adatkezelési nyilvántartás és adatfeldolgozói szerződések (fizetési és számlázó szolgáltató, tárhely, e-mail); (B)-ben több az adat (fiókok, belépési napló), és a számlák 8 évig megőrzendők.

### Cited Findings
- Nem sikerült elsődleges GDPR/NAIH-forrást letölteni ebben a menetben (fetch blokkolva); a pontok háttértudásból származnak, l. Inferences.

### Inferences
- [háttértudás, nem ellenőrizve] GDPR 13. cikk: adatkezelési tájékoztató; 28. cikk: adatfeldolgozói szerződés (Stripe, Barion, Számlázz.hu/Billingo, Patreon — ezek jellemzően a saját standard DPA-jukat kínálják elfogadásra; a Stripe/Patreon több adatnál önálló adatkezelő); 30. cikk: adatkezelési nyilvántartás (a 250 fő alatti mentesség nem érvényes, ha az adatkezelés rendszeres — egy előfizetői adatbázis az); 33. cikk: incidens 72 órán belül a NAIH-nak; incidensnyilvántartás.
- [háttértudás, nem ellenőrizve] Számv. tv. 169. § (2): a könyvviteli elszámolást közvetlenül és közvetetten alátámasztó bizonylatot legalább 8 évig kell megőrizni → a számlákon szereplő vevőadat jogi kötelezettség alapján 8 évig tárolódik, akkor is, ha az előfizető fiókját törlik (törlési kérelem kezelése: fiók törlése, számlaadatok megtartása).
- [háttértudás, nem ellenőrizve] SZJA 1%: a NAV a kedvezményezettnek csak azon rendelkezők nevét/címét adja át, akik ehhez hozzájárultak; ezekre az adatokra is GDPR-kötelezettség vonatkozik (tájékoztató, célhoz kötöttség).
- [értelmezés] (B)-ben az offline titkosított cache és hozzáférés-vezérlés miatt adatbiztonsági intézkedéseket kell dokumentálni (32. cikk), és a jelszó-visszaállítás, belépési naplók megőrzési idejét meg kell határozni.

### Gaps
- NAIH 2025–26-os útmutatója kis online szolgáltatóknak; Stripe/Barion DPA-feltételek konkrét szövege.

## 5. Alapítványi éves ciklus (A)

### Takeaway
Az alapítvány fő fix éves terhe a beszámoló (+ közhasznúsági melléklet) május 31-ig történő letétbe helyezése és közzététele; ehhez jön a kuratóriumi elfogadás, a könyvelés, az SZJA 1% felhasználásának elszámolása és az adatváltozások bírósági bejelentése.

### Cited Findings
- Egy alapítványi tájékoztató szerint az alapítvány az éves beszámolót a tárgyévet követő év **május 31-ig** elkészíti, és a befogadás után közzéteszi — [Fundamenta alapítványi tájékoztató 2026 (snippet)](https://alapitvany.fundamenta.hu/wp-content/uploads/2026/04/Alapitvanyi-tajekoztato-adomanyozok-reszere_online_2026.pdf)
- Civil határidő-táblázat (EMET) — [emet.gov.hu civil határidők PDF (cím; 2013-as eredetű, 2020-ban feltöltve, elavult lehet)](https://emet.gov.hu/app/uploads/2020/10/civil_hataridok_13_05_27__docx_2-1.pdf)

### Inferences
- [háttértudás, nem ellenőrizve] Ectv. (2011. évi CLXXV.) 30. §: beszámoló + közhasznú szervezetnél közhasznúsági melléklet letétbe helyezése az OBH-nál (birosag.hu, PK-542 űrlap, elektronikusan, ügyfélkapu+/cégkapu) a tárgyévet követő május 31-ig; saját honlapon is közzé kell tenni; a nem teljesítés a nyilvántartásból való törlés kockázatával jár.
- [háttértudás, nem ellenőrizve] Kuratóriumi ülés: a beszámoló elfogadása, határozatok könyve (Ectv./Ptk. alapító okirat szerint), jegyzőkönyv; adatváltozás (székhely, kurátor, cél) bejelentése a törvényszéknél változásbejegyzési kérelemmel (illetékköteles; összeg nem ellenőrzött).
- [háttértudás, nem ellenőrizve] SZJA 1% (1996. évi CXXVI.): a kedvezményezett regisztráció/nyilatkozat a NAV felé; a kapott összeg felhasználásáról beszámolót kell közzétenni (és bizonyos összeghatár felett a NAV-nak megküldeni) — határidők és összeghatárok **ellenőrizendők**.
- [háttértudás] Bankszámla kötelező; számlavezetési díj havonta (összeg bankfüggő, nem ellenőrzött); NAV-bevallások (pl. társasági adó bevallás alapítványnál is, ha van vállalkozási tevékenység; nulla bevallás esetei) — a könyvelő hatásköre.

### Gaps
- Aktuális (2025–26) birosag.hu civil útmutató, letétbe helyezés díja (alapítványnál díjmentes-e), SZJA 1% közzétételi határidő. Ezeket egy másik kutató (jogi formák) is lefedheti.

## 6. Fizetési szolgáltatók: KYC alapítványnál vs. egyéni vállalkozónál; Patreon-kifizetés magyar bankra

### Takeaway
A Patreon nem-amerikai alkotótól W-8BEN-t (magánszemély) vagy W-8BEN-E-t (szervezet, pl. alapítvány) kér a kifizetés előtt; a kifizetési díj országfüggő. A KYC-különbségre alapítvány és egyéni vállalkozó között nem találtam elsődleges forrást.

### Cited Findings
- Minden nem amerikai alkotónak W-8BEN-t vagy W-8BEN-E-t kell beadnia a kifizetéshez (Settings → Payouts and Taxes); új kifizetési mód hozzáadása 5 napos zárolást indít; a kifizetés 1–5 nap; 24 óránként kérhető; eltérő pénznemű támogatói fizetésnél 2,5% átváltási díj; a kifizetési díj országfüggő (pl. USD-ből átváltásnál 0,25 USD + 1,55%, 10 USD minimum) — [Lilach Bullock blog, Patreon-összefoglaló (harmadik fél; ellenőrizendő a Patreon súgóban)](https://www.lilachbullock.com/?p=147216)

### Inferences
- [háttértudás, nem ellenőrizve] Stripe/Barion/SimplePay onboarding: egyéni vállalkozónál adószám + személyazonosság + bankszámla; alapítványnál emellett a bírósági kivonat, a képviselő(k) azonosítása, tényleges tulajdonos (Pmt. szerinti nyilatkozat; alapítványnál a kuratórium elnöke/tagjai). Egyszeri, de adatváltozáskor (kurátorcsere) ismétlődik.
- [értelmezés] A Patreon-bevétel a könyvelésben egy összegben, devizában érkezik; a Patreon-kimutatás kell bizonylatnak (hasonló a Stripe-problémához: nincs banki kivonat-jellegű dokumentum).

### Gaps
- A Patreon hivatalos súgóoldalai és a magyar (HUF/EUR) kifizetési díj; Barion/SimplePay alapítványi KYC-dokumentumlista.

## 7. (B) technikai-üzemeltetési adminisztráció: fiókok, jelszó, visszatérítés, chargeback, sikertelen fizetés, támogatási órák

### Takeaway
Megbízható, forrásolt benchmarkot a „támogatási óra / 100 előfizető” mutatóra nem találtam; a létező számok forrás nélküli iparági becslések, ezért az alábbi óraszám saját [becslés].

### Cited Findings
- B2C SaaS: 2–5 ticket/ügyfél/hó (forrás nélküli „industry estimate”) — [count.co](https://count.co/metric/company-support-trends); egy másik forrás 0,3–0,8 ticket/ügyfél (időszak megjelölése nélkül) — [upgrowth.in](https://upgrowth.in/?p=34770). A két szám nagyságrendben ellentmond.
- Zendesk-eredetű iránymutatás szerint az ügyfelek 10–30%-a lép egyáltalán kapcsolatba a supporttal (B2B SaaS) — [getmonetizely.com](https://www.getmonetizely.com/articles/support-ticket-volume-the-critical-metric-that-can-transform-your-customer-service-strategy) (snippet)
- A Stripe Billing automatikus számlagenerálást és sikertelen fizetés-újrapróbálást (dunning) kínál — [metacto.com költségelemzés (snippet)](https://www.metacto.com/blogs/the-complete-cost-breakdown-of-stripe-billing-setup-integration-maintenance)

### Inferences
- [becslés] Egy egyszerű, önkiszolgáló (jelszó-visszaállítás, lemondás, számlaletöltés a fiókban) magyar nyelvű PWA-nál havi 2–8% ügyfél keres meg (kisebb, mint a SaaS-számok, mert a termék egyszerű); ügyenként 5–15 perc → **100 előfizetőre ~0,5–2 óra/hó**. Ez a fenti 10–30%-os kapcsolatfelvételi arányból és rövid ügyidőből lefelé korrigált becslés, nem mérés.
- [becslés] Chargeback ritka (kis összeg), de egyenként 30–60 perc; visszatérítés + sztornó számla egyenként 10–20 perc; sikertelen fizetés: automatizált dunning mellett havi néhány kézi eset.
- [becslés] Offline titkosított cache: „elveszett hozzáférés”/eszközcsere-ügyek a leggyakoribb nem-pénzügyi tickettípus lehet.

### Gaps
- Magyar vagy kis B2C-előfizetésre vonatkozó, forrásolt support-benchmark.

## 8. Összesítő ellenőrzőlista és havi idő-/költségbecslés modellenként

### Takeaway
[becslés] A (B) modell tranzakciónként, havonta és évente is több adminisztrációval jár (számlavolumen, fogyasztóvédelmi megfelelés, support), míg az (A) modell terhe főleg éves, fix jellegű (alapítványi beszámoló, könyvelés). A végső különbséget a könyvelési díj és a (B) support-terhe dönti el.

### Cited Findings
- A forrásolt elemeket l. az 1–7. pontban (Számlázz.hu csomagdíjak harmadik féltől; elállási gomb 2026.06.19-től; Patreon W-8BEN; support-benchmark hiánya).

### Inferences

**(A) Önkéntes támogatás (alapítvány, perkek nélkül vagy jelképes perkekkel)**
- Tranzakciónként: semmi (nincs számla); cég-támogatónak kérésre adományigazolás (közhasznú jogállás esetén).
- Havonta: banki/Patreon-kimutatás átadása a könyvelőnek; támogatói lista frissítése (köszönőlista csak hozzájárulással).
- Évente: beszámoló + közhasznúsági melléklet → kuratóriumi elfogadás → OBH-letét és honlapon közzététel május 31-ig; SZJA 1% elszámolás/közzététel; adatkezelési nyilvántartás és tájékoztató felülvizsgálata; Patreon adóűrlap érvényességének ellenőrzése.
- Esetenként: adatváltozás bejelentése; KYC-frissítés kurátorcserekor.
- **[becslés] Időigény:** ~1–2 óra/hó + évi ~8–15 óra (beszámoló-ciklus) ≈ **2–3 óra/hó átlagosan**.
- **[becslés] Pénzbeli költség:** könyvelő alapítványra (piaci ár, nem ellenőrzött) + bankszámla + Patreon/fizetési díj (forgalomarányos). A könyvelési díjat a másik kutató (formák/költségek) ellenőrzött számmal adja meg; itt nem találtam forrást.

**(B) Fizetős előfizetés (egyéni vállalkozó vagy Kft.)**
- Tranzakciónként (havonta előfizetőnként): automatikus számla (+ NAV Online Számla automatikus), sikeres/sikertelen terhelés kezelése (automatizált dunning), elállás/visszatérítés esetén sztornó számla.
- Havonta: Stripe/Barion kimutatás + számlalista egyeztetése a könyvelővel; support-ügyek; áfabevallás (ha áfakörös — a gyakoriság a másik kutatóé); panaszok nyilvántartása.
- Évente: ÁSZF, adatkezelési tájékoztató, árak felülvizsgálata; DPA-k felülvizsgálata; (Kft.) beszámoló.
- Egyszeri, de karbantartandó: ÁSZF + szerződéskötés előtti tájékoztatás + „megrendelés fizetési kötelezettséggel” gomb + **„elállás a szerződéstől” funkció (2026.06.19-től)** + digitális tartalomnál a lemondó nyilatkozat folyamata + visszaigazoló e-mail; békéltető testületi tájékoztatás; frissítési kötelezettség (373/2021) dokumentálása.
- **[becslés] Időigény:** 300 előfizetőnél: support ~1,5–6 óra/hó (l. 7. pont), könyvelői egyeztetés/egyeztetés ~1–2 óra/hó, fogyasztóvédelmi/ÁSZF-karbantartás évi ~5–10 óra → **~3–9 óra/hó**.
- **[becslés] Pénzbeli költség:** számlázó (Számlázz.hu #start/#digital éves díja 20 280 / 29 880 Ft + nem ismert Agent-API díj — harmadik fél szerint), fizetési szolgáltatói díj (forgalomarányos, nem ellenőrzött), könyvelő (nem ellenőrzött), egyszeri ÁSZF-jogi díj (nem ellenőrzött).

### Gaps
- Könyvelési díjak, Stripe/Barion/SimplePay jutalékok és a Számlázz.hu Agent-díjsávok ellenőrzött számai — ebben a menetben nem voltak letölthetők; a report-írónak a többi kutató számaival kell kitöltenie, vagy „nem ellenőrzött” jelöléssel hagynia.
