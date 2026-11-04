# Nyilatkozat a mesterséges intelligencia használatáról és a szerzőségről

<!-- Forrásréteg, kézi szöveg (F163.1). A lapra kötése (kolofon, Módszertan) külön tétel. A [HELYŐRZŐ: …] részeket a szerző tölti ki vagy hagyja jóvá; amíg helyőrző áll benne, a szöveg nem nyilvános. -->

*Állapot: 2026. november 4. A nyilatkozat a munka mai, tényleges gyakorlatát írja le, nem tervet.*

## Két réteg, két idézési egység

A munka két rétegből áll, és a mesterséges intelligencia a kettőt másképp érinti.

| Réteg | Mi tartozik bele | Az MI szerepe | Idézés és licenc |
|---|---|---|---|
| **Nyílt adatmag** | motívumazonosító, meghatározás, kizáró feltétel, előfordulások, kizárt helyek, döntések indoklással | a lekérdezések determinisztikus programok; a besorolási döntéseket MI-segített munkamenet hozza; minden sor megnevezi az eredetét: a lekérdezést, amelyből származik, vagy azt, hogy kézi döntés | önálló adatkészlet, CC BY 4.0 (a nyílt kiadással lép életbe), saját azonosítóval: `<KANONIKUS_FORRAS_URL>` |
| **Termék** | értelmező próza, a szótárak magyar fordítása, a Károli-párosítás, kötet, eszközök | az értelmező prózát és a szótár-fordítást nyelvi modell írta, a Károli-párosítás nagyrészt gépi | a szócikkek mint mű, minden jog fenntartva |

A modell által írt próza tehát a termékréteg része; az adatmag nem tartalmaz modell-prózát, csak döntéseket és rövid indoklásokat, eredetjelöléssel.
<!-- proveniencia: a rétegek határa: #86 megvalósítási terv 1.5 („Nyílt tudományos mag vs. fizetős termék”), a felhasználó kiegészítése az orkesztrátoron át („az adatréteg és a termékréteg szétválik a kutatás szerint”, „nem a GitHub marad a forrás”, 2026-11-04); a mai LICENSE még minden jog fenntartva, a CC BY a nyílt export (#162) kiadásával lép életbe | ts=2026-11-04 -->

## Mit írt mesterséges intelligencia

**Az értelmező szakaszok.** A motívumlapok értelmező szakaszait (Kivonat; Miért fontos ez a lelet; Értelmezés; Alkalmazás és tanítványság; Tanítói egyezés, ahol van; Módszertan és nyitott kérdések) nagy nyelvi modell írta az adatok alapján. A modell neve minden kiadott lap kolofonjában, kiadásonként szerepel (ma mindegyik kiadott lapon: `claude-opus-5-5`, Anthropic). Egy lap értelmező prózáját egy modell írja, és aki módosítja, az egészet újraolvassa.

**Az előfordulások besorolása.** A motívum lehetséges előfordulásait determinisztikus lekérdezések hozzák elő a héber és görög szövegből (szóegyezés, szópár egy versen belül, igealak, Septuaginta-megfelelés). Hogy egy hely a motívumhoz tartozik-e, arról MI-segített munkamenet dönt, és minden döntés indoklással rögzül: a beépített és az elutasított helyek egyaránt. A mai állapotban 792 vizsgált helyből 411 elutasítva, 255 beépítve, 126 nyitott.
<!-- proveniencia: scope=main be54d328, előfordulás-jelöltek (jelolt_tipus=elofordulas) dontes szerint | forras=adat/jeloltek.tsv | ts=2026-11-04 -->

**A szótári anyag magyar fordítása.** A lapokon idézett szótári szócikkek (Brown–Driver–Briggs, Thayer és rövid héber–görög jelentések) magyar szövege túlnyomó részben gépi fordítás nyelvi modellel (`claude-sonnet-5-5`), kis részben kézzel javítva. A fordítás rögzített szakkifejezés-jegyzéket követ, és minden fordított egységnél tárolva van, melyik modell készítette.
<!-- proveniencia: scope=main be54d328, allapot+modell szerinti darabszám (BDB sonnet 29 862, Thayer sonnet 1 967; kezi/opus sorok nagyságrendekkel kevesebb) | forras=adat/forditasok.tsv, adat/glosszak_heber_hu.tsv | ts=2026-11-04 -->

**A Károli-szavak párosítása.** Hogy a Károli-fordítás melyik szava melyik héber vagy görög szónak felel meg, azt nagyrészt gépi párosítás adja. A lap minden ilyen során megnevezi az azonosítás módját és a bizonyosság fokát.

## Mit nem írt mesterséges intelligencia

Az adattáblákból generált részeket (előfordulás-táblák, szótári blokkok, kapcsolatok, forráslista, kolofon) program állítja elő, nem nyelvi modell; ezek ugyanabból az adatból mindig ugyanúgy készülnek. A kiinduló szövegek (héber és görög szöveg, Károli-fordítás, szótárak) harmadik fél forrásai; a forrásokat és licencüket minden lap felsorolja.

## Ki és mi ellenőriz

| Ellenőrzés | Ki vagy mi végzi | Mit tesz |
|---|---|---|
| Gépi kapuk | program | minden lapon méri az olvasói hibákat (belső jelölés, angol maradék, számeltérés a szöveg és a tábla között, hiányzó forrás stb.); kiadott lapon a hibák száma nulla kell legyen |
| Változás-ellenőrzés | külön, friss kontextusú modellfutás | a munka egy-egy lépésének változásait saját lekérdezéssel újraellenőrzi |
| Lektori kérdéslista | a prózát írótól eltérő modell (`claude-fable-5-1`) | a próza kijelölt helyein kérdez (ellentmond-e az adatnak, érthető-e, állít-e alátámasztás nélkül); nem ír át. Eddig három motívumon futott; kérdései a következő kiadás bemenetei |
| Határ-ellenőrzés | gépi vizsgálat és egy második modell | azt nézi, következetes-e a motívum határa, és nem hígul-e |
| Vizuális átnézés | a szerző | a megjelenő lapot a kiadás előtt átnézi; a jóváhagyás a lap adott változatához kötött, és ha a lap változik, újra át kell nézni |
| Lapjavítás | a szerző (vagy külső lektor) | rámutat egy helyre, a javítást jóváhagyja; a lap kolofonja a javított helyek számát és a jóváhagyókat feltünteti |

## Amit ez a nyilatkozat nem állít

- **Ez nem független szakmai lektorálás.** Az ellenőrzés egy része program, egy része nyelvi modell (modell ellenőriz modellt), az emberi átnézést a szerző maga végzi.
- **Nevesített külső szerkesztőbizottság vagy tanácsadó testület ma nincs.**
- A modell nem szerző, és nem visel felelősséget a szövegért.

## Szerzőség és felelősség

[HELYŐRZŐ: SZERZŐI FELELŐSSÉGVÁLLALÁS — a szerző saját mondata. Javaslat: „A [HELYŐRZŐ: TERMÉKNÉV] szerzője és kiadója [HELYŐRZŐ: SZERZŐ NEVE]. A mesterséges intelligenciával készült szövegeket a fent leírt módon átnéztem és jóváhagytam; a tartalomért én felelek.”]

A tudományos kiadók gyakorlata szerint az MI-eszköz nem lehet szerző, használatát meg kell nevezni és le kell írni, a felelősség az emberi szerzőé (Cambridge University Press, 2023; De Gruyter Brill: elsődlegesen MI által írt cikket vagy fejezetet nem fogad el). Ezért ez a munka mai formájában **adatbázis és szócikkek MI-segített gyűjteménye**, nem lektorált tudományos közlemény. Folyóiratba szánt érvelő szöveget a szerző ír, és ott a fentieket külön nyilatkozatban megnevezi. A Society of Biblical Literature erre vonatkozó szabályát nem találtuk.

## Források

- Cambridge University Press: *Cambridge launches AI research ethics policy* (2023). https://www.cambridge.org/sv/news-and-insights/cambridge-launches-ai-research-ethics-policy
- De Gruyter Brill: *AI-Policy for Authors.* https://degruyterbrill.com/en/ai-for-authors (a kiadói oldal tartalmát keresési kivonatból ismerjük)
- Elsevier: *Generative AI policies for books.* https://www.elsevier.com/de-de/about/policies-and-standards/publishing-ethics-books/generative-ai-policies

<!-- proveniencia (a nyilatkozat tényei): scope=main be54d328 | forras=adat/kiadasok.tsv (proza_modell: 5/5 sor claude-opus-5-5), naplok/KIADAS_{ALVIL-001,ISTENTISZT-001,TEREMT-002}_lektor.md (lektor: claude-fable-5-1), .claude/agents/{lektor,hatar-ellenor,fuggetlen-ellenor}.md, MUNKAMENET.md C-g…C5, C-j, adat/SEMA.md 2.46, 2.48, 2.49, eszkozok/lexikon_general.py kolofon_szerzoseg; kiadói szabályok: naplok/kutatas_2026-10-27/jelentesek/Motivumlexikon_mint_kutatoi_termek.md | ts=2026-11-04 -->
