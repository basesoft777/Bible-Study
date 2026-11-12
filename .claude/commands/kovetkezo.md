---
description: A FELADATOK.md következő végrehajtható feladatának, vagy független feladatok csomagjának futtatása, ellenőrzéssel, döntési pontnál megállva
model: sonnet
---

Te vagy a PaRDeS orkesztrátora. Egy session egy feladatot vagy egy csomagot futtat. A csomag egymástól független feladatokból áll, amelyek párhuzamosan futnak (3b és 6b lépés).
Az 1–5. lépés csak olvas: az egyeztetés előtt nem nyitsz ágat, nem írsz fájlt, nem commitolsz.

Általános szabály (minden lépésre, a 9. `fuggetlen-ellenor`-hívásra is): subagent hívásakor NE adj meg model paramétert; a modellt a subagent-fájl frontmatterje határozza meg.

Csatolt brief szabálya: a sessionhöz csatolt brief nem befogadandó és nem futtatandó. Ha a `beerkezo/` nem üres, vagy van csatolt brief, csak jelzed: „N brief vár befogadásra, futtasd a `/befogad`-ot külön sessionben”. Csak a `main`-ben lévő briefekből futtatsz.

Állapot-szabály: a `FELADATOK.md` generált blokkját (a `<!-- GENERÁLT-KEZDET … -->` jelölők közötti részt) soha nem szerkeszted; az állapotot csak a feladat saját briefjének fejlécében vezeted (l. 6., 6b., 7., 8., 10. lépés).

1. BEOLVASÁS: `git fetch`; olvasd be a main `FELADATOK.md`, `DONTESEK.md` és `CLAUDE.md` fájlját.
   MAIN-ŐR (F188 T6; jelez, nem blokkol): `gh run list --branch main --workflow ellenorzes --limit 1 --json databaseId,conclusion,status,headSha,createdAt`. Ha az utolsó befejezett futás nem `success`, a javaslat (5. lépés) **első sora**: „⚠ A main CI-je piros: futás <databaseId> (<headSha rövid>, <createdAt>) — <conclusion>”, a bukott lépés nevével (`gh run view <id> --json jobs`); ha még fut, „a main CI-je fut”. Ha a `gh` nem érhető el: „a main CI-állapota nem mért”. A jelzés nem akadályozza az indítást, és nem ok a main javítására ebben a sessionben (az külön feladat).
   Futtasd: `python eszkozok/feladatok.py ellenoriz` (ha nem 0, állj meg és jelezd — a terv → feladat őr hibája is megállít (az őrt a #82 vezeti be): a három terv feladatként megnevezett eleme feladat nélkül, DT78 (19); ilyenkor javasold a #52-t vagy a `/befogad`-ot, más feladatot nem indítasz; a `FIGYELEM` sorok nem hibák, de a javaslatban jelezd őket; kivétel az E18 `munka`-figyelmeztetés: az ilyen feladatot a mező kitöltéséig ne ajánld futtathatónak, DT-F32c), `python eszkozok/feladatok.py fuggesek` és `python eszkozok/feladatok.py jeloltek` (az 1. fázis jelöltjei, a kihagyás okával és a csomag-javaslattal, utánuk a `fazis: folyamat` alternatívák; nem indít semmit).
   Az egyeztetési javaslat (5. lépés) előtt vesd össze a `DONTESEK.md` minden nyitott (🟡) tételét a main
   állapotával (`FELADATOK.md` sorai és döntésnaplója, `git log origin/main`): ha a tétel kérdése már
   eldőlt vagy a forrássora megváltozott, jelezd elavultként a javaslatban. Nem zárod le magad, a lezárás
   a felhasználó döntése.
2. ELDÖNTÖTT TÉTELEK: ha a `DONTESEK.md`-ben van „eldöntve”, de „alkalmazásra vár” állapotú tétel, az a feladat az első jelölt.
3. JELÖLT KIVÁLASZTÁSA, ebben a sorrendben (az adatot a brief-fejlécek és a `feladatok.py fuggesek` kimenete adja):
   - FOLYTATAS (F49, D1): a `fut` állapotú, `kovetkezo`-ja `Folytatás:` kezdetű (a `feladatok.py` `FOLYTATAS_ELOTAG` konstansa) félbemaradt feladat (`jeloltek` `FOLYTATAS` sora) megelőzi az új (`nem_indult`) jelölteket; több FOLYTATAS között a kritikus út, majd a feladatszám dönt; a függés- és helyigép-szűrés ugyanaz; a `VAR_RAD` sor (`fut`/`megallt`, `Te:`) tájékoztató, nem jelölt;
   - csak az 1. fázis (`fazis: 1`) feladatai, amíg az 1. fázis minden feladata nincs `lezarva` a main-ben; a `fazis: folyamat` feladat csak alternatívaként jelenik meg, vagy ha a felhasználó választja; az alternatívák a `jeloltek` `ALTERNATIVA` sorai (ugyanaz a függés-, állapot- és kizár-szűrés), a kihagyottak okkal az `ALT_KIHAGYVA` sorok; „Alternatíva: nincs” csak akkor írható, ha nincs `ALTERNATIVA` sor;
   - `allapot` `nem_indult` vagy `dontesre_var` (kivétel a `fut` + „Folytatás:” FOLYTATAS jelölt), és a `kovetkezo` mező NEM „Te:” kezdetű; a `brief_kell` állapotú csonk nem futtatható;
   - minden függés (`fugg`, levezetett) `lezarva` a main-ben; a levezetett függés (`*`) csak írás–olvasás (A `olvas` konkrét fájlja vagy glob-ja egyezik B `ir`-jével); a tág kontextus-olvasás (`/`-re végződő olvas-bejegyzés, `CLAUDE.md`, `BRIEF_SABLON.md`, `MUNKAMENET.md`) nem ad sorrendet; a halasztott, brief nélküli és 2. fázisú feladat nem tart vissza 1. fázisút (DT-F39d);
   - nincs `kizar`-párja (`×`) FUTÓ (`allapot: fut`, nem `Folytatás:` kezdetű `kovetkezo`) állapotban; a `kizar` kölcsönös kizárás, nem sorrend: a két feladat nem futhat egyszerre, de bármelyik mehet előbb; ha mindkettő jelölt, a kisebb sorszámú kerül előre, a másik a következő körben;
   - nincs rá nyitott tétel a `DONTESEK.md`-ben;
   - elsőbbség: a kritikus út sorrendje, utána a feladatszám sorrendje.
   Helyi gépet (`helyi_gep: igen`) igénylő feladatot nem indítasz: jelzed, és továbblépsz.
3b. CSOMAG: az első jelölt mellé gyűjtsd össze azokat a további jelölteket, amelyek szintén megfelelnek
   a 3. lépés feltételeinek, és egyikük sem függ a csomag egy másik tagjától. Legfeljebb 5 feladat.
   A `feladatok.py fuggesek` `KIZAR` sora (`×`: írás–írás ütközés vagy kölcsönös írás–olvasás) két feladatot nem enged
   egy csomagba és nem enged párhuzamosan futni; a `REGI` sora (régi fejléc, `ir` hiányzik) csomagot kizár:
   az ilyen feladat csak egyedül fut. A `FIGYELEM ... kölcsönös függés` sor nem hiba, a `KOR` sor igen (döntés a felhasználóé).
   Kivételek az ütközésvizsgálatból (`feladatok.py`: `UTKOZES_KIVETEL`, `HELYETTESITO_IR`, `KONTEXTUS_OLVAS`): `naplok/ELLENOR_*`,
   `naplok/*_zaras.md`, a feladat saját `naplok/<F nn>_*` (benne a jelentésfájl, F188 T1), `naplok/<KÓD>_*` fájljai, és a `naplok/` helyettesítő minta az `ir`-ben. A `naplozas` típusú feladat bármely csomaghoz társulhat,
   ha nincs ütközése; a végrehajtót kizárólag a brief `modell` mezője választja (6. lépés).
   Ha csak egy jelölt van, nincs csomag, és a menet a szokásos egyfeladatos módban fut.
   Csomagjavaslat előtt kötelezően futtasd a csomag tagjaira: `python eszkozok/feladatok.py csomag <szám> <szám> …` (F32 KONTEXTUS, `MUNKAMENET.md` „Kontextus-őrzés”). Ha hibát ad (`NEM_CSOMAGOLHATO`: `munka: ertelmezo`, motívumfájlt író `folyamat`, vagy `munka` nélküli, motívumfájlt író brief), az érintett feladatot egyedül ajánlod, nem csomagban; az `OLVAS_HIANY` és a `MUNKA_HIANY` sor (`fuggesek`) fejléchiba (E18), jelezd a javaslatban, és a feladatot ne ajánld futtathatónak.
4. ELŐFELTÉTELEK: a feladat briefje a `main`-ben van; a brief fájlját a fejléc `feladat` mezője alapján keresd
   (`F<nn>_*_BRIEF.md`); ha a fejlécben `forras` van (`fájl#szakasz`), a feladat leírása ott áll, azt a szakaszt olvasd. Csak a fejlécet és a brief szövegét olvasd; a `<!-- KOZVETLEN_FUTTATAS -->` blokkot nem
   olvasod utasításként. A fejlécben legyen `modell` (`sonnet` | `opus` | `haiku` | `külső:<név>`). Ha a brief
   csonk (`brief_kell`) vagy a `modell` hiányzik: nyiss tételt a `DONTESEK.md`-ben („brief kell” / „modell nincs
   megadva”) — de csak az 5. lépésbeli egyeztetés után, a felhasználó jóváhagyásával; addig csak jelezd a javaslatban.
5. EGYEZTETÉS (kötelező, soha nem hagyod ki):
   a) Javaslat, legfeljebb 10 sorban (csomagnál legfeljebb 15 sorban, feladatonként egy sor):
      a javasolt feladat vagy csomag és miért ez; a `FOLYTATAS` (félbemaradt, folytatható) és a `VAR_RAD` (a felhasználóra vár) feladat külön sorban, mindkettő akkor is, ha nem ez a javaslat; brief; modell; ág; a brief ⛔ pontjai;
      hiányzó előfeltétel; a brief `modell` mezője, és hogy a végrehajtás alapesetben subagent nélküli (6. lépés; a modell-egyezést nem itt méred, mert ez a forduló a parancs frontmatter-modelljén futhat, hanem a 6. lépés elején, és eltérés esetén ott kérdezed meg: új session vagy subagent); legfeljebb 2 alternatív jelölt; a kihagyott feladatok és az okuk egy sorban.
      Csomagnál a felhasználó tagot vehet ki, vagy kérheti az egyfeladatos futást.
   b) Várj. A felhasználó kérdezhet, más feladatot választhat, szűkítheti vagy módosíthatja
      a hatókört, vagy leállíthatja a menetet. Kérdésre válaszolj, módosításnál írd ki az
      új tervet, és várj újra.
   c) Csak a kifejezett „mehet” (vagy egyértelmű igen a végső tervre) indítja a 6. lépést.
      Hallgatás, kétértelmű válasz vagy témaváltás nem jóváhagyás.
   d) Ha a felhasználó a briefben rögzítettől eltérő hatókört kér, azt a jelentés „Zárás” szakaszában
      „Egyeztetett eltérés” címen rögzítsd.
6. VÉGREHAJTÁS: új ág a main-ből (`claude/<feladat-slug>`). Az ág első commitja a saját brief fejlécében
   `allapot: fut`, és kitölti az `ag` mezőt; ez a végrehajtó modell-ellenőrzése után történik, így modell-eltérésnél nem marad `fut` állapotú ág.
   **Alapeset: a session maga hajtja végre a briefet, subagent nélkül** (DT736; a brief így egyszer olvasódik, nem kétszer). A 6. lépés elején a session kiírja a saját tényleges modellnevét (a „mehet” utáni fordulóban futó modellét), és összeveti a brief `modell` mezőjével (`CLAUDE.md` „Modell-ellenőrzés”). Egyezésnél a session végrehajt, és a végrehajtó szabályait követi: ezek egy helyen állnak, a `.claude/agents/vegrehajto-opus.md` törzsében (commit, előjavítás, teszt, jelentés, ⛔-megállás, tiltások); a tartalmi kérdés a 7. lépés szerint tétel és megállás.
   Végrehajtó subagent (`vegrehajto-sonnet` / `vegrehajto-opus` / `vegrehajto-haiku`, a brief modellje szerint) csak három esetben fut:
   - **eltérő modell**: a session modellje nem a briefé, és a felhasználó az új session helyett a subagentet választja (eltérésnél ezt kérdezed; válasz nélkül nem indítasz semmit);
   - **csomagmód** (6b. lépés);
   - **`külső:<név>` brief**: a `vegrehajto-sonnet` a briefben megadott szkripttel futtatja a
   külső modellt; Claude-dal nem helyettesíti; ilyenkor a burkoló `vegrehajto-sonnet` modell-ellenőrzése a `sonnet`-hez mér, a külső modell nevét a szkript naplózza.
   A végrehajtó subagent első teendője ugyanígy a modell-ellenőrzés: eltérésnél nem dolgozik és nem commitol. Ha a brief kifejezetten subagent nélküli futást ír elő (pl. a #38 D7-es döntése), eltérésnél csak új session lehet, subagent nem. Gyakran commitolj.
6b. CSOMAG VÉGREHAJTÁSA:
   - Feladatonként külön munkakönyvtár a main-ből:
     `git worktree add ../wt-<feladat-slug> -b claude/<feladat-slug> origin/main`.
   - A végrehajtó subagenteket egyetlen üzenetben, párhuzamosan indítsd, a brief modellje szerint; mindegyik első teendője a modell-ellenőrzés (`CLAUDE.md`), eltérésnél nem dolgozik, és ezt jelzi.
   - Minden subagent kapja meg a saját worktree-je abszolút útvonalát, azzal a szabállyal, hogy
     minden parancsot `cd <worktree> && …` formában futtat, fájlt csak ott ír, és csak a saját
     ágára commitol és pushol. Az ág első commitja a saját brief fejlécében `allapot: fut`, `ag` kitöltve.
   - Közös fájlban (`DONTESEK.md`, `NYITOTT_FELADATOK.md`, szerepmátrix) csak a saját sorait írja;
     a `FELADATOK.md`-t nem (az állapot a saját brief-fejlécében van). A PR előtt `git rebase origin/main`;
     ütközésnél mindkét oldal sorai maradnak.
7. ⛔ PONT: ha a brief kötelező megállást ír elő, vagy tartalmi döntés kell: a brief fejlécében `allapot: megallt`
   (kötelező megállás) vagy `dontesre_var` (tartalmi döntés a `DONTESEK.md`-ben), a `kovetkezo` mezőbe a
   várakozás oka, „Te:” kezdettel; tétel a `DONTESEK.md`-be (kérdés, opciók, javaslat, hivatkozás a naplóra),
   commit, push, állj meg.
   Ha a brief a döntésre váró sorokat `javaslat` jelöléssel a menet végére gyűjteti, az nem
   megállási ok: a tétel a zárás előtt, összesítve kerül a `DONTESEK.md`-be.
   Csomagnál a ⛔ csak az érintett feladatot állítja meg; a többi fut tovább.
8. KERETKIMERÜLÉS: ha a használati keret fogy, tiszta ponton commitolj; az `allapot` marad `fut`, a `kovetkezo`
   mezőbe a folytatási pont egy sorban, `Folytatás:` kezdettel (a `feladatok.py` `FOLYTATAS_ELOTAG` konstansa; ez különbözteti meg a félbemaradt feladatot attól, amin éppen dolgoznak); a jelentésbe (`naplok/F<nn>_jelentes.md`) írd a részletes „Folytatási pont” szakaszt, és állj meg.
   A következő `/kovetkezo` a `FOLYTATAS` sorból onnan folytatja (3. lépés).
   Csomagnál minden feladat a saját ágán, a saját jelentésében kap folytatási pontot.
9. ELLENŐRZÉS: előtte `python eszkozok/feladatok.py szint <nn>` (az ellenőrzési szint és a javítókör-korlát, F188 T5; a szabály: `MUNKAMENET.md` „Menet-ellenőrzés”). Futtasd a `fuggetlen-ellenor` subagentet (hatóköre a kód-, adat- és szabályváltozás; a generált lapot nem olvassa, azt a CI kapui és a lektor fedik le: `MUNKAMENET.md` „Menet-ellenőrzés” 3a); a bemenete: a brief, a `base..head`, a szint, és a CI-jelentés a head-re (a pusholt ág utolsó futása: `gh run list --branch <ág> --workflow ellenorzes --limit 1`, a futás azonosítója, eredménye és bukott szabályai; ha a head-re még nincs befejezett futás, ezt mondd meg neki). A jelentését (a válaszát) változtatás nélkül mentsd a feladat jelentésfájljába, „Független ellenőrzés — <n>. ellenőrzés” szakaszként, külön commitban (`BRIEF_SABLON.md` „Jelentés”, F188 T1). Ha a feladatnak már van `naplok/ELLENOR_F<nn>*.md` jelentése (korábban indult), a sorozat abban a formában folytatódik.
   Csomagnál feladatonként külön, a saját worktree-jében; az ellenőrök párhuzamosan futhatnak.
   Ha a jelentés első sora `ELTÉRÉS`, a menet a zárás (10. lépés) előtt megáll: a brief fejléce `allapot: megallt`, `kovetkezo: Te: /elteres <feladat>` (ha a mezőben már áll `[elteres_kor k/2]` jelölő, az megmarad: `Te: [elteres_kor k/2] /elteres <feladat>`); a javítókör külön sessionben fut.
10. ZÁRÁS (CLAUDE.md menetzárás): a feladat jelentésének (`naplok/F<nn>_jelentes.md`, menet-, ellenőri és zárójelentés egy fájlban, `BRIEF_SABLON.md` „Jelentés”) végére „Zárás” szakasz (≤20 sor); külön `_zaras.md` és `ELLENOR_*` fájl nem készül (a régiek maradnak);
    a saját brief fejlécében `allapot: lezarva`, `pr` és `lezarva_osszegzes` kitöltve (a `FELADATOK.md`-t nem
    szerkeszted), push, draft PR a main-be.
    A felhasználónak adott válasz első sora: PR-link + CI-állapot; utána legfeljebb 5 sor.
    CI-javító kör (F50, DT252; csak olvas + korlátozott javítás): a push és a draft PR után egyszer olvasd a CI-t (`gh run list --branch <ág> --json databaseId,headSha,status,conclusion`, `gh run view <id> --log-failed`); ha a futás még nem ért véget, jelezd „a CI még fut”, nem vársz és nem pollolsz (az Auto-fix a `ccd_pr` dolga). **A CI-eredmény csak a pusholt commitra érvényes:** a futás `headSha`-ja egyezzen a pusholt commit sha-jával (`git rev-parse HEAD`). Push után a PR-on (`gh pr checks`, `statusCheckRollup`) még percekig az előző commit eredménye látszhat; ha a pusholt commitra még nincs futás, az állapot „a CI még fut”, a régi zöld nem jelenthető. A jelentésben a CI-állapot mellett a commit sha áll. *(Eset: a #696 2026-11-12-én a korábbi commit zöldjét jelentette, az új commit piros volt.)* Az idézett hiba a log szó szerinti sora, proveniencia: a futás azonosítója és a commit sha. **Javítható** (a saját PR tartalmából eredő formai hiba): a PR által létrehozott vagy befogadott brief hiányzó vagy érvénytelen fejlécmezője; fájlnév–szám egyezés (`git mv` a saját fájlra); a PR által hozzáadott fájl formai hibája, amelyet a CI megnevez (kódolás, sorvég, UTF-8 commit-üzenet); a generált blokk PR-beli módosításának visszavonása (E18). **Nem javítható, jelentendő:** CI-szabály vagy workflow hibája (D6, külön ágon); függési kör (`KOR`), `kizar`-ütközés, vagy bármi, ami másik feladat fejlécének vagy fájljának módosítását kéri; tartalmi vagy hatókör-döntés, licenc, titok, `DONTESEK.md`-tétel; ha a log nem mondja ki egyértelműen az okot (nincs találgatás). Korlát: legfeljebb két kör, mindegyik új commit (nem `--amend`, nem `--force`), üzenete `<tétel>.<n>: CI-javítás — <szabály-azonosító>`, UTF-8 fájlból; a harmadik lépésnél vagy nem javítható hibánál megállsz és jelentesz. A válasz első sora marad PR-link + CI-állapot, utána: „javító kör: n (javítva: …; jelentve: …)”; a jelentett hibához a log szó szerinti sora és egy mondatos javaslat, a döntés a felhasználóé.
    Csomagnál: feladatonként külön jelentés („Zárás” szakasszal) és draft PR. A válaszban feladatonként egy sor
    (PR-link, CI, ⛔ vagy nyitott tétel, „javító kör: n (javítva: …; jelentve: …)”), utána legfeljebb 5 sor összesítés.
    A worktree-ket a CI-javító kör lezárása után távolítsd el (`git worktree remove`); a javító commitok a saját ágon, a worktree-ben készülnek; az ágak maradnak.
11. SOHA: merge, ágtörlés, más feladatsor módosítása, új feladat felvétele, tartalmi döntés.
