**Próba a HAMART-001 lektorának 34 pontossági tételén: gépileg megfogja 5, kézi listára teszi 18 (ebből 9 ⚑ jelzéssel), nem látja 11 — ebből 8 generált blokkban áll, nem a kézi forrásban; a forrás prózájának 26 tételéből tehát 23 kerül gépi ítélet vagy kézi lista elé.**

# F200 — próza-állítás ellenőrző: próba és jelentés

*FELADATOK #200 · claude-opus-5-5 · 2026-11-11 · brief: `F200_PROZA_ALLITAS_BRIEF.md`*

## A próba

- Forrás: a HAMART-001 mai forrása a main-en (`motivumok/HAMART-001.md`, `adat/elofordulasok.tsv`, a 7095bc63 commit állapota), 159 egység (rés-mondat és `kapcsolodas`-sor).
- Mérce: a lektor kérdéslistája (`naplok/KIADAS_HAMART-001_lektor.md`, a `claude/kiadas-hamart-d4c26f` ágon, #696). Pontossági tétel az, amelynek „Mi a gond” sora az 1. (az igehely maga) vagy a 4. kérdést nevezi: 34 a 46-ból (a feladatleírás 34-es száma ezzel egyezik).
- Parancs: `python eszkozok/proza_allitas.py HAMART-001 --lektor <a lektor fájlja>`; kimenet: `naplok/ALLITAS_HAMART-001.md` (az első sora a fenti szám, a „Összevetés a lektorral” táblája tételenként).
- Illesztés: a tétel „Erre vonatkozik” idézetének legalább 20 karakteres darabja az egység szövegében (a rövid fordulat sok egységre illene).

## Eredmény tételenként

| Eredmény | Lektor-tételek | Mi fogta meg |
|---|---|---|
| **gépi (ELTÉR)** — 5 | 5, 6, 32, 41, 43 | 5 és 32: szópár-alany — az Ez 7:23-ban a megtelés szava mellett a „város” (ír) áll, a föld nem; 32: az Ez 12:19-ből a megtelés igéje (H4390) hiányzik; 6: „a föld szava nélkül” — az 1Kir 13:34-ben és a 2Kir 17:23-ban az adámá (H0127) áll; 41: a „föld színéről” fordulat az 1Kir 14:15-ben (nincs H6440) és a 2Kir 17:23-ban (a két szó nem szomszédos) nem áll; 43: „de más kulcsszóval” — az 1Móz 6:13 idézetének „vég” szava (kéc, H7093) az Ez 7:2-ben, 7:6-ban és az Ámós 8:2-ben is áll |
| **kézi ⚑** — 9 | 8, 12, 14, 21, 29, 31, 34, 35, 38 | 12: a „föld” a Jer 51:46-ban erec (H0776); 29 és 34: a „föld” az 1Móz 6:12–13-ban erec; 14: a lánc „föld” szava nincs a Sof 1:9-ben; 21, 31, 35, 38: kizárólagos állítás („egyetlen”, „először”, „mindig”, „minden előfordulását”) lekérdezés nélkül; 8: ugyanez a jelzés, de véletlen találattal (a mondat a ⚑-t a „nem egyetlen szón” fordulaton kapja; a tétel tárgya, a „minden előfordulása”, ugyanabban a mondatban áll) |
| **kézi** — 9 | 9, 10, 11, 13, 22, 28, 33, 36, 42 | a mondat a listán, a Károli-verssel és a héber sorral; az ítélet emberi/modelles (ki az alany, mi hallatszik, melyik fejezet, mire utal vissza) |
| **nem látja: generált blokk** — 8 | 15, 17, 18, 19, 23, 25, 26, 27 | nem a kézi forrás prózája (6. Kereszthivatkozások, 7. Kapcsolatok, 9. Hatástörténet): N-F200a |
| **nem látja: a forrásban, tétel nélkül** — 2 | 30, 37 | igehely nélküli értelmező mondat („a büntetés nem kívülről jön”; a szavak forrásonkénti kiosztása) kizárólagos szó nélkül |
| **nem látja: gépileg egyezik** — 1 | 40 | „A motívum hat újszövetségi helyén …”: a szám egyezik (6), a hiba (a Jel 22:3-ban nincs lánc-szó) nem szám |

**Pontosság.** A HAMART-001-en a 10 ELTÉR-sor mind valós hiba (a fenti öt tétel). Téves riasztás a végső változatban nincs; a menet közben látott téves riasztások osztályai (a `kapcsolodas` saját versének kihagyása, a tagadás átnyúlása a tagmondaton, a szám alanyának elvétése, a ragot fordító előtag a fordulatban, a felsorolás tagonkénti értelme, a névszói szópár „alanya”, a szótári jelentés idézőjelben) mind gépi szabállyal és teszttel záródtak.

**Más motívumokon** (futásbiztonság; a jelentések nincsenek commitolva): ISTENTISZT-001 3 ELTÉR, ALVIL-001 0, TEREMT-001 27, TEREMT-002 8, HODIT-001 7, KIRALY-001 5, MENNY-001 1. A régi formájú forrásokon a szókészlet üres (N-F200c), ezért ott csak az idézet-, a fordulat- és a számpróba fut; az ELTÉR-sorok jórészt jelöletlen saját fordítás idézőjelben („a Refáim földje” a Károli „óriások”-ja helyett, „nevet akarnak szerezni maguknak”), vagyis ugyanaz a hibaosztály, amelyet az E34 a `kapcsolodas` mezőben mér, itt a résekben is.

## Mit nem tud az eszköz

- **Szerkezet és vonatkozás:** ki az alany, kinek a hangja hallatszik, melyik tagmondathoz tartozik a „szüntelen” (lektor 9, 11). Ezt a lista mutatja, az ítélet a kézi átnézésé (N-F200b).
- **Igehely nélküli olvasat:** a Peshat alá sorolt következtetés (30), a forrásra rá nem kötött állítás (37). A kizárólagos szavakon („mindig”, „először”, „egyetlen”) túl nincs gépi fogása.
- **Generált blokk:** a lap generált része (N-F200a).

## Független ellenőrzés és javítókör

A `fuggetlen-ellenor` (opus) a 9926ae54..2de13efd diffen két ELTÉRÉS-t talált, egy javítókörben mindkettő javult (F200.4):

1. **A „más szó” állítás a következő igehelyre tapadt:** a záradék az előző és a következő igehely-csoport közötti szöveg volt, ezért a „…(Ézs 24:5-6), ahol az átok más héber szóval …” mellékmondat a Hós 4:1-3-ra is ítéletet adott (itt véletlenül „egyezik”). Javítás: az előző csoportra visszautaló vonatkozó mellékmondat (`ahol`, `amely…`, `aki…`) a következő csoport záradékából kimarad (`zaradek_sajat`), és a „más szó” próba csak a saját csoportjára szól. Teszt: `test_vonatkozo_mellekmondat`, `test_mas_szo_az_elozo_csoporte`.
2. **Saját Strong-normalizáló:** az ötjegyű G-kiegészítő kódot csonkolta volna (G20447 → G2044). Javítás: az F62 `strong_util.strong_normalizal`. Teszt: `test_strong_norm_f62`.

A két figyelmeztetésből: a „más kulcsszóval” próba most csak akkor ELTÉR, ha az idézett mondat tartalmi szavainak legalább fele a versben is áll (a HAMART-on az Ez 7:2, 7:6, Ámós 8:2 sora marad); a PR címe az E16 szerint `[ELLENŐRZŐ]` előtagú (a CI-munkafolyamat változik). A harmadik (az előző mondatban megnevezett vers idézete) nyitott, a kézi lista fogja; a HAMART-próbán nem fordult elő.

A javítás után a próba száma változatlan (gépi 5, kézi 18, nem látja 11; 10 ELTÉR), az „egyezik” sorok száma 109 → 108.

## A folyamatba építés

- `MUNKAMENET.md` C-szakasz: új **C-a** sor (a C-w után, a C-g és a lektor, C-k előtt); a „lezárás menete” 1. pontja ezzel bővül.
- `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`: az önellenőrzés után „Állítás-ellenőrzés” lépés: az ELTÉR-sorok javítása a forrásban, a ⚑ tételek átnézése, a kézi lista átadása az olcsó modellnek vagy embernek, mindez a lektor előtt.
- Kapu-szint JELENTÉS (DT-F200b); CI: a tesztek a „Szabaly-tesztek” lépésben.

(proveniencia: scope=motivumok/HAMART-001.md + adat/elofordulasok.tsv (id=HAMART-001) @7095bc63; naplok/KIADAS_HAMART-001_lektor.md @origin/claude/kiadas-hamart-d4c26f | forras=eszkozok/proza_allitas.py | ts=2026-11-11)
