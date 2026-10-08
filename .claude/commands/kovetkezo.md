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
   Futtasd: `python eszkozok/feladatok.py ellenoriz` (ha nem 0, állj meg és jelezd — a terv → feladat őr hibája is megállít (az őrt a #82 vezeti be): a három terv feladatként megnevezett eleme feladat nélkül, DT-F52g (19); ilyenkor javasold a #52-t vagy a `/befogad`-ot, más feladatot nem indítasz; a `FIGYELEM` sorok nem hibák, de a javaslatban jelezd őket; kivétel az E18 `munka`-figyelmeztetés: az ilyen feladatot a mező kitöltéséig ne ajánld futtathatónak, DT-F32c), `python eszkozok/feladatok.py fuggesek` és `python eszkozok/feladatok.py jeloltek` (az 1. fázis jelöltjei, a kihagyás okával és a csomag-javaslattal; nem indít semmit).
   Az egyeztetési javaslat (5. lépés) előtt vesd össze a `DONTESEK.md` minden nyitott (🟡) tételét a main
   állapotával (`FELADATOK.md` sorai és döntésnaplója, `git log origin/main`): ha a tétel kérdése már
   eldőlt vagy a forrássora megváltozott, jelezd elavultként a javaslatban. Nem zárod le magad, a lezárás
   a felhasználó döntése.
2. ELDÖNTÖTT TÉTELEK: ha a `DONTESEK.md`-ben van „eldöntve”, de „alkalmazásra vár” állapotú tétel, az a feladat az első jelölt.
3. JELÖLT KIVÁLASZTÁSA, ebben a sorrendben (az adatot a brief-fejlécek és a `feladatok.py fuggesek` kimenete adja):
   - FOLYTATAS (F49, D1): a `fut` állapotú, `kovetkezo`-ja `Folytatás:` kezdetű (a `feladatok.py` `FOLYTATAS_ELOTAG` konstansa) félbemaradt feladat (`jeloltek` `FOLYTATAS` sora) megelőzi az új (`nem_indult`) jelölteket; több FOLYTATAS között a kritikus út, majd a feladatszám dönt; a függés- és helyigép-szűrés ugyanaz; a `VAR_RAD` sor (`fut`/`megallt`, `Te:`) tájékoztató, nem jelölt;
   - csak az 1. fázis (`fazis: 1`) feladatai, amíg az 1. fázis minden feladata nincs `lezarva` a main-ben; a `fazis: folyamat` feladat csak alternatívaként jelenik meg, vagy ha a felhasználó választja;
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
   `naplok/*_zaras.md`, a feladat saját `naplok/<F nn>_*`, `naplok/<KÓD>_*` fájljai, és a `naplok/` helyettesítő minta az `ir`-ben. A `naplozas` típusú feladat bármely csomaghoz társulhat
   (`vegrehajto-haiku`), ha nincs ütközése.
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
      hiányzó előfeltétel; legfeljebb 2 alternatív jelölt; a kihagyott feladatok és az okuk egy sorban.
      Csomagnál a felhasználó tagot vehet ki, vagy kérheti az egyfeladatos futást.
   b) Várj. A felhasználó kérdezhet, más feladatot választhat, szűkítheti vagy módosíthatja
      a hatókört, vagy leállíthatja a menetet. Kérdésre válaszolj, módosításnál írd ki az
      új tervet, és várj újra.
   c) Csak a kifejezett „mehet” (vagy egyértelmű igen a végső tervre) indítja a 6. lépést.
      Hallgatás, kétértelmű válasz vagy témaváltás nem jóváhagyás.
   d) Ha a felhasználó a briefben rögzítettől eltérő hatókört kér, azt a zárójelentésben
      „Egyeztetett eltérés” címen rögzítsd.
6. VÉGREHAJTÁS: új ág a main-ből (`claude/<feladat-slug>`). Az ág első commitja a saját brief fejlécében
   `allapot: fut`, és kitölti az `ag` mezőt. A munkát a brief modelljének
   megfelelő végrehajtó subagent végzi (`vegrehajto-sonnet` / `vegrehajto-opus` / `vegrehajto-haiku`).
   `külső:<név>` esetén a `vegrehajto-sonnet` a briefben megadott szkripttel futtatja a
   külső modellt; Claude-dal nem helyettesíti. Gyakran commitolj.
6b. CSOMAG VÉGREHAJTÁSA:
   - Feladatonként külön munkakönyvtár a main-ből:
     `git worktree add ../wt-<feladat-slug> -b claude/<feladat-slug> origin/main`.
   - A végrehajtó subagenteket egyetlen üzenetben, párhuzamosan indítsd, a brief modellje szerint.
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
   mezőbe a folytatási pont egy sorban, `Folytatás:` kezdettel (a `feladatok.py` `FOLYTATAS_ELOTAG` konstansa; ez különbözteti meg a félbemaradt feladatot attól, amin éppen dolgoznak); a zárójelentésbe írd a részletes „Folytatási pont” szakaszt, és állj meg.
   A következő `/kovetkezo` a `FOLYTATAS` sorból onnan folytatja (3. lépés).
   Csomagnál minden feladat a saját ágán, a saját zárójelentésében kap folytatási pontot.
9. ELLENŐRZÉS: futtasd a `fuggetlen-ellenor` subagentet; jelentése: `naplok/ELLENOR_<feladat>.md`.
   Csomagnál feladatonként külön, a saját worktree-jében; az ellenőrök párhuzamosan futhatnak.
10. ZÁRÁS (CLAUDE.md menetzárás): zárójelentés `naplok/<feladat>_zaras.md` (≤20 sor),
    a saját brief fejlécében `allapot: lezarva`, `pr` és `lezarva_osszegzes` kitöltve (a `FELADATOK.md`-t nem
    szerkeszted), push, draft PR a main-be.
    A felhasználónak adott válasz első sora: PR-link + CI-állapot; utána legfeljebb 5 sor.
    Csomagnál: feladatonként külön zárójelentés és draft PR. A válaszban feladatonként egy sor
    (PR-link, CI, ⛔ vagy nyitott tétel), utána legfeljebb 5 sor összesítés.
    A push után a worktree-ket távolítsd el (`git worktree remove`); az ágak maradnak.
11. SOHA: merge, ágtörlés, más feladatsor módosítása, új feladat felvétele, tartalmi döntés.
