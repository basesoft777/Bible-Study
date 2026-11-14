# F200 HIBA-szint mérés — a próza-állítás ellenőrző ELTÉR-soraink minősítése (N-F200d)

*2026-11-14, claude-sonnet-5-5. A feladat: a `proza_allitas.py` ELTÉR-sorainak minősítése a vers szövege alapján (valós hiba / téves riasztás) a két új formájú forráson, a HIBA-szintre emelés előtt (N-F200d feltétele; a felhasználó: „ez menjen most”).*

## Eredmény egy mondatban

| Lap | ELTÉR a mérés elején | valós hiba | téves riasztás | ELTÉR a javítás után |
|---|---|---|---|---|
| HAMART-001 (`motivumok/HAMART-001.md` + a `kapcsolodas` sorai) | 4 | 0 | 4 | 0 (egyezik: 120) |
| ISTENTISZT-001 (`motivumok/ISTENTISZT-001.md` + a `kapcsolodas` sorai) | 0 | – | – | 0 (egyezik: 42) |

A téves riasztás nem nulla (4/4 a HAMART-001-en), de mind a négy oka gépileg javítható, és javítva van az eszközben, teszttel (`eszkozok/teszt_proza_allitas.py`, `F200_7` osztály): ezért a HIBA-szintre emelés megtörtént (E41, `proza_allitas.py --kapu`; DT-F200e). A pilot-próbán mért 10 valós ELTÉR (F200.2) a HAMART-001 javítókörei (F182, F206) óta nincs meg: ma a forrásban nincs valós ELTÉR-sor.

## A négy HAMART-001 ELTÉR-sor minősítése

A vers szövege: Károli 1908 (`konkordancia/Karoli_1908.tsv`), a héber szórend és a Strong-sor a TAHOT-ból (`TAHOT_kivonat.tsv`), az újszövetségi helyek a `adat/elofordulasok.tsv`-ből.

| # | Hely | Állítás | Vers | Ítélet | Indok | Az ok és a javítás |
|---|---|---|---|---|---|---|
| 1 | `HAMART-001.md:147` (rés: modszertan) | „A motívum **öt lexikai** újszövetségi helyén a lánc szava … ugyanott áll.” (a következő mondat: „A hatodik, a Jel 22:3, tematikus hely, a lánc szava nélkül”) | – | **téves riasztás** | Az adatban 6 újszövetségi hely van (8 vers), de ebből a Jel 22:3 tematikus (`gerinc_elem` = `tematikus:1Móz 3:17`, `strong` üres); a lexikai hely 5 (Róm 8:21, Gal 3:13–14, Zsid 6:7–8, Jel 11:18, Jel 19:2). A mondat szó szerint a lexikai helyekre szól, és a hatodikat nevezi meg kivételnek. | A szám-próba a „lexikai” minősítést nem ismerte, a hat helyhez mérte. Javítva: a „lexikai” minősítés a tematikus helyek nélküli csoportra mér („újszövetségi lexikai: 5 hely, 7 vers”: egyezik). A hatókör-jelzés (⚑, a csoportban tematikus hely van) is megszűnik ott, ahol a mondat a lexikai csoportot nevezi. |
| 2 | `HAMART-001.md:153` (rés: modszertan) | „a **„föld színéről”** fordulattal” — az 1Kir 13:34-ben és az Ámós 9:8-ban; az 1Kir 14:15-ben és a 2Kir 17:23-ban „a földről” | 1Kir 14:15 | **téves riasztás** | A fordulat az **előtte** álló két helyre szól. 1Kir 13:34 Károli: „a föld színéről való kiirtatásának”, TAHOT: `… H5921 H6440 H9009 H0127` (a színe + a föld szomszédos). Ámós 9:8: „a földnek színéről”, TAHOT: `H5921 H6440 H9009 H0127` (szomszédos). Az 1Kir 14:15-ben a mondat éppen azt mondja, hogy a „föld színéről” fordulat **nincs** ott („erről a jó földről”; TAHOT: `H5921 H9009 H0127`, H6440 nincs). A próza tehát pontos. | A fordulat-próba az idézetet a **következő** igehely-csoporthoz rendelte, nem a legközelebbihez. Javítva: a legközelebbi igehely-csoport dönt (az idézet előtt, ha az közelebb van); a nyers esetben (a fordulat a követő helyre szól, és hiányzik) a próba továbbra is ELTÉR (teszt: `test_fordulat_valodi_hiba_marad`). |
| 3 | `HAMART-001.md:153` (rés: modszertan) | „**„a földről”**” (az 1Kir 14:15-ben és a 2Kir 17:23-ban) | 2Kir 17:23 | **téves riasztás** | A 2Kir 17:23 Károli: „az ő földéből”, TAHOT: `H5921 H0127` (a föld szava áll, a színe nélkül). A „föld színe fordulat nélkül” (a prózában) a 2Kir 17:23-ra pontos, mert ott a színe Istené („az ő színe elől”). | A próba a „a földről” idézet két szavából az „a” + „föld…” előtagpárt kereste, és az „a…” előtag bármely „a-val kezdődő” szót (az **á**tok szavát, árar H0779) is találta; a névelős idézet nem kétszavas fordulat. Javítva: a névelővel kezdődő idézet nem fordulat-próba tárgya. |
| 4 | `elofordulasok.tsv:246` (adat: kapcsolodas) | „Jeremiás a próféták és a nép bűnéről mondja: „a hamis esküvés miatt gyászol a föld …”. A héberben itt az **átok szava áll (álá)**, ugyanaz, amely az Ézs 24:6-ban megemészti a földet; a Károli esküvésnek fordítja.” | Jer 23:10 | **téves riasztás** | A Jer 23:10 TAHOT-sora: `H3588 H5003 H4390 H9009 H0776 H3588 H9006 H6440 H0423 H0056 H9009 H0776 …`: az `H0423` (אָלָה, álá) áll a versben. A mondat az **álá**-t nevezi meg (a Károli esküvésnek fordítja), és az Ézs 24:6-ra is ezt mondja; a lánc „átok” szavai (árar H0779, katára G2671) közé az álá nem tartozik, a próba pedig csak a lánc szótárából döntött. | A szójelenlét-próba a mondat saját zárójeles megnevezését („áll (álá)”) nem használta. Javítva: ha a mondat a szót átírással megnevezi, a vers azonos kiejtésű szava (vagy a forrás fejlécének átírása) dönt; megnevezés nélkül a lánc szava dönt (teszt: `test_megnevezett_szo_*`). A próba a szó jelenlétét ítéli, nem azt, hogy az álá „átok-e”: ez a kézi listán marad. |

## ISTENTISZT-001

0 ELTÉR-sor. A forrás (`motivumok/ISTENTISZT-001.md`, F194, 10-es sablon szerint) lánc-szava a hívás (kárá, H7121); a próba 42 sort ítélt egyezőnek, 139 kézi sor van (jelzés ⚑ a `naplok/ALLITAS_ISTENTISZT-001_atnezes.md` szerint nézve). Téves riasztás: nincs.

## A régi formájú források (tájékoztatásul; nem gátol)

Az N-F200c szerint ezekben a lánc szavai nincsenek megnevezve, ezért ott csak az idézet-, a fordulat- és a számpróba fut; az ELTÉR-sorok jórészt jelöletlen saját fordítások idézőjelben. A javítás után (az `--kapu` futása): ALVIL-001 0, ANTROP-001 1, HODIT-001 7, KIRALY-001 5, MENNY-001 1, TEREMT-001 27, TEREMT-002 8 ELTÉR. Ezeket a kapu **nem méri** (régi forma), és ezt soronként kimondja; a sorokat nem minősítettem (a lapok új cikként, nulláról készülnek, F123).

## A HIBA-szint hatóköre és megvalósítása

- **Egység:** E41 (`adat/SEMA.md` 3.11, generálva), CI-lépés: `python eszkozok/proza_allitas.py --kapu` (`.github/workflows/ellenorzes.yml`), helyi tükör: `push_elott.py` `STATIKUS_HIVASOK`.
- **Csak az ELTÉR-osztály** (gépi ítélet) **HIBA**; a kézi ⚑ lista és a „kézi” sorok jelentés.
- **Csak az új formájú forrás.** A forma felismerése gépi, és kimondott: új formájú a forrás, ha a próza megnevezi a lánc szavait (a próba szókészlete nem üres), vagy a NAPLÓ-sora a `10_PaRDeS_U3_proza_prompt_sablon.md`-re hivatkozik. A régi formájú forrást a kimenet soronként kimondja („régi formájú forrás … nem mérve”), nem csendben marad ki. Az `adat/lap_befagyasztas.tsv` nem alkalmas kivétel-listának: az ISTENTISZT-001 a lapja miatt van rajta (a forrása új formájú), a lapja pedig a forrásától független.
- **Új cikk:** a TEREMT-001 új cikkének forrása a 10-es sablon szerint készül (NAPLÓ-sor, megnevezett lánc-szavak), ezért az első commitjától automatikusan a kapu hatókörébe kerül; külön bejegyzés nem kell.
- **Mit nem fog meg:** a gép a szó jelenlétét, a szópárt, a fordulat szomszédosságát, az idézetet és a számot ítéli; hogy a mondat *alanya* vagy *jelentése* pontos-e, a kézi listán marad (⚑).

## Proveniencia

scope=`motivumok/HAMART-001.md` + `motivumok/ISTENTISZT-001.md` rései és `adat/elofordulasok.tsv` `kapcsolodas` (id=HAMART-001, id=ISTENTISZT-001) | forras=`eszkozok/proza_allitas.py` (a mérés a javítás előtti és utáni állapoton), `konkordancia/Karoli_1908.tsv`, `TAHOT_kivonat.tsv`, `TAGNT_kivonat.tsv`, `adat/elofordulasok.tsv` | ts=2026-11-14. A nyers futási kimenet a repón kívülre (scratchpad) készült; a Károli-szöveg és a Strong-sor kivonata a fenti táblában áll.
