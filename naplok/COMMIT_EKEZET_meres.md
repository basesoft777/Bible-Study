# naplok/COMMIT_EKEZET_meres.md — #112 M0 mérés (E30)

*Modell: claude-sonnet-5-5 · 2026-10-19 · proveniencia: `forras=manual`, `scope=origin/main --no-merges`, szkript: `eszkozok/ellenorzes/szabalyok.py::e30_meres`, `ts=2026-10-19` — nem lekérdezés, a besorolás kézi.*

## 1. Módszer

- Korpusz: `git log --no-merges origin/main` (3592 commit), a gépi commitok (`szamkiosztas:`, `FELADATOK.md frissítés (gép)`) kihagyva.
- Szókészlet: a kézi commitok üzenetében legalább 3-szor előforduló ékezetes szó ékezetlen alakja (a szókészlet így a projekt saját nyelvéből áll; nem külső szótár).
- Kihagyott részek: kódrész (`` `…` ``), fájlút/fájlnév, azonosító (`DT-F09a`, `F112`, `ISTENTISZT-001`), `Co-Authored-By:` sor; kötőjel-, perjel-, aláhúzás-, pont-, `=`-szomszédos tokenek.
- Kizárási lista: `eszkozok/ellenorzes/e30_ascii_alakok.tsv` (alak, ok, forrás).
- Újrafuttatás (repó gyökeréből; a korpusz a `1a6a6eef` commitig tart, az `origin/main` azóta mozog, ezért a fej rögzített). Az M0b 50 soros listája a `c668bb36` commit kizárási fájljával reprodukálható (`git show c668bb36:eszkozok/ellenorzes/e30_ascii_alakok.tsv`):

```
python -c "import sys; sys.path.insert(0,'eszkozok/ellenorzes'); import szabalyok as S; S.e30_meres('', '1a6a6eef')"
```

A minta: `random.Random(112).shuffle`, az első 50 találat. A találat = (üzenet, ékezetlen alak) pár.

## 2. M0a — csak a vitathatatlan kizárásokkal

A kizárási lista: a fejlécmező-nevek és értékek (`allapot`, `kovetkezo`, `fugg`, `lezarva`, `megallt`, `fazis`, `tipus`, `hianyzik`, `elerheto`, `korlatos`) és a kétértelmű párok (`meg`, `mert`, `kor`, `sem`, `fel`, `arany`, `mar`, `helyen`, `szinten`, `hozza`, `ben`).

```
commit (merge nelkul): 3592, gepi kihagyva: 296, kezi: 3296
szokeszlet: 2354, kizaras: 21
jelolt uzenet: 659, jelolt talalat: 3416
30 leggyakoribb: konyv=46, ket=41, kezi=34, nelkul=32, valodi=31, forras=29, javitas=28, naplo=25, korabban=25, forditatlan=24, korabbi=24, frissitve=23, ellenorzes=22, utan=22, javitva=21, kulon=21, belso=20, generalt=20, regi=20, ures=20, talalat=19, fajl=19, felhasznalo=19, sajat=19, elott=19, jeloltek=18, indoklas=18, jelentes=18, tisztazatlan=17, javit=16
```

**Minta pontossága: 42 / 50 = 84%** (8 hamis pozitív; a 16. sor `kiegeszitve` valódi hiba, a független ellenőr javította).

| # | commit | jelölt -> javaslat | sor | besorolás |
|---|---|---|---|---|
| 1 | `3494854d` | szamkiosztas -> számkiosztás | alcímre. A tétel helyőrző marad (végleges számot a szamkiosztas ad). | hamis pozitív |
| 2 | `01f820bf` | szandekosan -> szándékosan | diff. E2-E16: 0 talalat. E1 tovabbra is szandekosan piros (S1.5 zarja). | valódi hiba |
| 3 | `8d805135` | tetel -> tétel | szakaszba (scope a vartnal kisebb volt), 1. tetel renumberelve | valódi hiba |
| 4 | `72a7a519` | ellenorizve -> ellenőrizve | Kulon ellenorizve (a Jer 37:4/37:5 betu-utotagos Latin_vers-sorok | valódi hiba |
| 5 | `0c0e2463` | megfelelo -> megfelelő | a betu -- ha egyik sem, a megfelelo atiras-karaktert (b/k/p) lagy alakra | valódi hiba |
| 6 | `ea792f94` | rogzitve -> rögzítve | kivezetve) es D28 (26, nem 24 heber jelolt) explicit rogzitve; a 26 | valódi hiba |
| 7 | `372f95f7` | ket -> két | 0 sora van - a ket verset osszekoto pontos hatar tovabbra sem | valódi hiba |
| 8 | `250bd900` | kezi -> kézi | kezi, átnézésre. | valódi hiba |
| 9 | `10d87335` | kulon -> külön | (zfill(4)) menthetne meg mind a 35 egyedi szocikket -- kulon tetelkent, | valódi hiba |
| 10 | `4813588f` | megjegyzes -> megjegyzés | NYITOTT_FELADATOK.md N34: a forditas_ubs.tsv megjegyzes mezoje (4 sor) nem | hamis pozitív |
| 11 | `b574d8ae` | ujrameres -> újramérés | KK7.5.3: ujrameres es jelentes - K1-K6 mind RENDBEN | valódi hiba |
| 12 | `62dc6320` | kotelezo -> kötelező | modszertana, kotelezo kereszthivatkozas-naplo, fejezethatar-javitasok); | valódi hiba |
| 13 | `5f2068e6` | kerult -> került | mert csak az 1Moz 14:18 (15) es a Zak 6:13 (9) talalat kerult | valódi hiba |
| 14 | `c482ea05` | szakaszaban -> szakaszában | 1. szakaszaban. | valódi hiba |
| 15 | `032a767b` | hibas -> hibás | tul-jelzes, nem hibas adat, csak pontatlanabb kategorizalas. | valódi hiba |
| 16 | `5e94c9d4` | kiegeszitve -> kiegészítve | adat/SEMA.md: a 2.14 tabla kiegeszitve a megjegyzes mezovel; a 2.10 | valódi hiba |
| 17 | `c136e924` | felhasznalo -> felhasználó | felhasznalo dontese kovetkezik. | valódi hiba |
| 18 | `e6697673` | kovetkezmenye -> következménye | hogy egy eddig fel nem tart osszeolvadt Karoli-vers (Ezs 3:26) kovetkezmenye, | valódi hiba |
| 19 | `23616837` | terkep -> térkép | A KK igehely_mt oszlopa az irányadó, a terkep EGYIK_SEM sorai nem használtak; | hamis pozitív |
| 20 | `6ccd3d76` | kerult -> került | tablazatabol -- a CI zold a PR #57-en, a sor a "Kesz" listaba kerult. | valódi hiba |
| 21 | `a17841d4` | all -> áll | 2. a Claude Haiku 4.5 sora egysegesnyi nevezovel all: 80,8% (97/120), a | valódi hiba |
| 22 | `ae9339f9` | mostantol -> mostantól | - D8: a HIBA mostantol a diff altal hozzaadott/modositott sorokra | valódi hiba |
| 23 | `e9cf5d13` | torzscikk -> törzscikk | torzscikk (nincs lexikonoldal). A motivumok/TEREMT-002.md prózájából semmi | valódi hiba |
| 24 | `84b5e913` | blokkolo -> blokkoló | F46.8: fuggetlen ellenori jelentes (ELTERES 6, nem blokkolo) | valódi hiba |
| 25 | `e35a3274` | kodot -> kódot | `e10_spirit_lelek` mostantol kizarolag a backtickes inline kodot vagja ki | valódi hiba |
| 26 | `4850acaa` | sajat -> saját | kommentben szereplo "feltehetoen a forras sajat prefix-index | valódi hiba |
| 27 | `4297a84e` | utotag -> utótag | F88.1: a TIPNR-betöltő kifejezett utótag-szabálya — alapszám a strong oszlopban, új utotag oszlop, strong_nyers marad (DT111) | hamis pozitív |
| 28 | `4850acaa` | javitotta -> javította | tartalmi minoseget is javitotta, nem csak a 35 uj sort adta hozza. | valódi hiba |
| 29 | `c482ea05` | torolve -> törölve | (jovahagyasra var); a korabbi Girdlestone-mondat torolve (D18 ota | valódi hiba |
| 30 | `340255fc` | dontesnaplo -> döntésnapló | F05: dontesnaplo D38-D40, CI E5 retroaktiv jeloles | valódi hiba |
| 31 | `fc3de78a` | tokennel -> tokennél | gondolkodási tokennel (F3V3 és F8V3 kész, a napló 2.127677 USD-jéhez viszonyítva); mock-tesztek. | hamis pozitív |
| 32 | `9342ad6d` | nevet -> nevét | egyenlőséggel kiadódó nevet / névalakot (Nea+Polis, Ben-+Hesed, Shushan-+Eduth, house of+Ashtaroth). | hamis pozitív |
| 33 | `942d18ec` | kitoltve -> kitöltve | F46.11: brief lezarva, pr kitoltve | valódi hiba |
| 34 | `1d497feb` | bir -> bír | F22.Bir: api_koteg begyujt (bir) | hamis pozitív |
| 35 | `c136e924` | javitas -> javítás | Nincs javitas ebben a commitban -- csak a jelentes mentese. A | valódi hiba |
| 36 | `f2e5402b` | letezik -> létezik | ELTERO_SZOVEGALAP: 205, meg hianyzik: 12). 8 db "nem letezik a | valódi hiba |
| 37 | `b2257019` | cim -> cím | Javitas: PR #38-ban veletlenul torolt cim nelkuli zaro tartalom visszaallitasa | valódi hiba |
| 38 | `c1e327a9` | kotelezo -> kötelező | uj fajl, a 4_PaRDeS_tematikus_sablon.md v13 altal eloirt kotelezo | valódi hiba |
| 39 | `cc344fe9` | eleg -> elég | onmagaban eleg szuk halmaz (l. 1Moz_7v1-24 es 1Moz_12v1-20 auditja). A | valódi hiba |
| 40 | `7b930fa4` | szamozott -> számozott | szamozott hasznalati resz kezdodik -- pontosan az a hatarfajta, amit a | valódi hiba |
| 41 | `f14d924b` | ellenorzes -> ellenőrzés | \| futas \| kimenet_token \| finish_reason \| hosszarany \| 1. ellenorzes \| | valódi hiba |
| 42 | `b0005288` | alatamasztas -> alátámasztás | 1Moz_7v1-24: Rom 9:27 gyok-szintu lexikai alatamasztas + uj Remez-pont (nismat chajjim); kockazat-riport 3. jelzo pontositasa | valódi hiba |
| 43 | `d1911591` | ellenori -> ellenőri | F76.14: ellenori jelentes mentve (ELLENOR_F76_M2.md) | valódi hiba |
| 44 | `e568ccf7` | tobb -> több | A celzott ujraellenorzes a db84fca-ra egy sulyos hibat es tobb kisebb | valódi hiba |
| 45 | `cc6997cb` | igy -> így | uj koltseg-tsv-sort kap (a cache-elt usage-bol) -- igy egy megismetelt vagy | valódi hiba |
| 46 | `2595ddce` | ellenorzi -> ellenőrzi | Uj vedelmi vonal: nulla_kimenet_e() minden A-esetnel ellenorzi, hogy a | valódi hiba |
| 47 | `ab34d162` | cimke -> címke | F42.7: M6 N9 — a licencjelölés egyetlen forrása az adat/licencek.tsv (cimke oszlop), KJV-sor tisztazatlan, TBESH-megjegyzés javítva | hamis pozitív |
| 48 | `cfb1defa` | javitva -> javítva | szerepel, jelolt_marad egyetlen jelöltnél is; 21 javitva -> 9 javitva, 84 jelolt_marad | valódi hiba |
| 49 | `c56575b7` | fajl -> fájl | RETIRED jelzessel kihagyva, ha a fajl hianyzik (a kulcs-/hash-ellenorzes | valódi hiba |
| 50 | `53d73a94` | dokumentalva -> dokumentálva | Strong-utkozes-feloldasi szabaly dokumentalva a | valódi hiba |

A hamis pozitívok oka: oszlopnév (`megjegyzes`, `utotag`, `cimke`), értékkészlet-elem (`terkep`), igehely-rövidítés (`bir`), Action-név (`szamkiosztas`), és két szó, amelynek az ékezetlen alakja helyes (`nevet`, `tokennel`: a `tokennél` a szókészlet zaja).

## 3. M0b — a séma-mezőnevekkel és -értékekkel bővített lista

Bővítés: a brief-fejlécek kulcsai és zárt értékei, az `adat/*.tsv` oszlopnevei és ≤15 elemű értékkészletei (a forrás soronként az `ok`/`forras` mezőben), valamint a M0a hamis pozitívjai közül a `nevet`, `tokennel`, `szamkiosztas`, `bir`. **Figyelem: ez a lista részben az M0a mintán tanult, ezért az M0b pontossága enyhén optimista.** Új véletlen minta: a lista változása miatt más találatok kerültek az első 50-be.

```
commit (merge nelkul): 3592, gepi kihagyva: 296, kezi: 3296
szokeszlet: 2354, kizaras: 50
jelolt uzenet: 626, jelolt talalat: 3303
30 leggyakoribb: konyv=46, ket=41, kezi=34, nelkul=32, valodi=31, javitas=28, naplo=25, korabban=25, forditatlan=24, korabbi=24, frissitve=23, ellenorzes=22, utan=22, javitva=21, kulon=21, belso=20, generalt=20, regi=20, ures=20, talalat=19, fajl=19, felhasznalo=19, sajat=19, elott=19, jeloltek=18, indoklas=18, jelentes=18, tisztazatlan=17, javit=16, szabaly=16
```

**Minta pontossága: 45 / 50 = 90%** (5 hamis pozitív; a 35. sor `kiegeszitve` valódi hiba, a független ellenőr javította).

| # | commit | jelölt -> javaslat | sor | besorolás |
|---|---|---|---|---|
| 1 | `9e2e4af1` | jelmagyarazat -> jelmagyarázat | jel-vazlat, vz-torzs, vz-fo, vz-jel, vz-al, jcim, kolcsonzott, jelmagyarazat, | hamis pozitív |
| 2 | `f6c7480b` | osszesen -> összesen | ures diff, osszesen 40 talalat mindket sorrendben. | valódi hiba |
| 3 | `effd33c0` | klon -> klón | F9.J25: tiszta klon igazolas valodi git worktree-vel (HEAD-blob osszevetes), k9_egyedites assert 50/30/4/26 | valódi hiba |
| 4 | `164c1fbd` | zarojelentesben -> zárójelentésben | F9.J26: a 32 maradek ismeretlen sor osszesitese a zarojelentesben | valódi hiba |
| 5 | `799c3d96` | ertek -> érték | trivialis (helytelen) ertek csendben felulirta a valodi Heber-celpontot. | valódi hiba |
| 6 | `8bc57219` | nelkul -> nélkül | parositas, nem szemantikai). Emberi felulvizsgalat nelkul nem | valódi hiba |
| 7 | `2ebbb391` | elott -> előtt | versifikacios-terkep alapu Igehely-cimkezes elott | valódi hiba |
| 8 | `021ab39b` | retroaktiv -> retroaktív | 4 study 7. szakaszának retroaktiv atirasa 7-oszlopos audit-tablazatra (koteg #4) | valódi hiba |
| 9 | `7f0df734` | valodi -> valódi | FJ2: 3e versszamozas - 13/15 a repo sajat LXX_OS hezaga, nem valodi elteres; Karoli-KJV versszam osszevetes | valódi hiba |
| 10 | `62dc6320` | javitas -> javítás | Dontesi fajl v36 changelog + leltar-javitas, playbook GIT-ELLENORZES szakasz | valódi hiba |
| 11 | `135f1171` | repon -> repón | hunk-parszolasat egy ideiglenes git repon. | valódi hiba |
| 12 | `0292a9dd` | egyeb -> egyéb | nincs_a_nezetben 9, egyeb 0. Teszt: 38, OK. | hamis pozitív |
| 13 | `f2e5402b` | kizaras -> kizárás | Karoliban" kizaras (Hós 11:12, 13:16, 2:23) - a Karoliban nem letezo | valódi hiba |
| 14 | `ea792f94` | kozos -> közös | 1. Nincs kozos Strong-normalizalo fuggveny a projektben -- legalabb 7 | valódi hiba |
| 15 | `372f95f7` | kizaras -> kizárás | A load_versifikacios_terkep()-ben uj kizaras: minden Gorog_LXX_vers/ | valódi hiba |
| 16 | `db84fca6` | erintett -> érintett | masolatban. Varatlan, empirikusan igazolt eredmeny: mind a 4 erintett | valódi hiba |
| 17 | `e431509e` | hibas -> hibás | (L1-L8) fixture-re: ures sor, csonka sor, REF_RE-hibas ref, zarojel | valódi hiba |
| 18 | `da8d0ac2` | javitasa -> javítása | 1Moz_15_bovitett.md v1 -> v2: formazasi hiba javitasa + 7. Lexikai audit szakasz felvetele | valódi hiba |
| 19 | `2ebbb391` | versnel -> versnél | - Minden olyan versnel, ahol egy Karoli-vers TOBB nyers LXX-verset | valódi hiba |
| 20 | `f9bdfdbf` | terkep -> térkép | terkep-fajlbol kovetkeztetve) ertekeli a feloldhatosagot. | valódi hiba |
| 21 | `98faa094` | ezert -> ezért | diff -r lexikon/ ezert teljes lefedettseget ad. | valódi hiba |
| 22 | `36be1898` | utotag -> utótag | levágva; strong_nyers marad, új utotag oszlop; SEMA 1.2; G6202 a jelentésbe. | hamis pozitív |
| 23 | `0fdfbc5a` | vesz -> vész | (hosszabb kulcs elsőbbsége) továbbra is részt vesz. | hamis pozitív |
| 24 | `715ae7f6` | kezi -> kézi | F06.11: workflow kezi inditasra (workflow_dispatch), futtatas.txt torolve | valódi hiba |
| 25 | `dd395d4b` | azota -> azóta | Mutacios futas (uj eldobhato agon, e75823d, azota torolve): --regi-commit | valódi hiba |
| 26 | `a17841d4` | megjegyzes -> megjegyzés | 4. a DeepSeek G1941 csonkolasi megjegyzes kiegeszult a tenyleges token- | valódi hiba |
| 27 | `aaf75bf1` | torolve -> törölve | A "hodolat" fogalmat Istenre alkalmazo levezetes torolve a 2. pont | valódi hiba |
| 28 | `ac359c05` | ezert -> ezért | kereszthivatkozast, ezert a LXX_versificacios_terkep.tsv automatikus | valódi hiba |
| 29 | `5a06dccc` | fajlt -> fájlt | a mappa `## Fajlok` tablazata meg a regi 6 KJV/ASV fajlt sorolja, a 7 uj | valódi hiba |
| 30 | `385477d2` | hatas -> hatás | KK1b-5: hatas ujraszamolasa Zsoltarokkal (67.9%), K1-K8 ellenorzes | valódi hiba |
| 31 | `ac359c05` | szot -> szót | cimkezi at a mar meglevo sorokat, nem ad hozza/vesz el szot. | valódi hiba |
| 32 | `58739182` | all -> áll | nevezovel all (80,8% = 97/120, a HIBA nelkuli 85,1%-ot is feltuntetve), | valódi hiba |
| 33 | `c8a8d0b8` | indoklas -> indoklás | (napló + rövid hivatkozás a jeloltek.tsv indoklas végén). | hamis pozitív |
| 34 | `ff86defd` | jovobeli -> jövőbeli | README-kent rogzitve jovobeli tobb-szavas formulak kereseshez. | valódi hiba |
| 35 | `5e94c9d4` | kiegeszitve -> kiegészítve | adat/SEMA.md: a 2.14 tabla kiegeszitve a megjegyzes mezovel; a 2.10 | valódi hiba |
| 36 | `b83f9f26` | visszairas -> visszaírás | visszairas). | valódi hiba |
| 37 | `ea6b62dd` | ertekek -> értékek | betu-utotagos Gorog/Heber/Latin ertekek TULNYOMO tobbsege (~99%) | valódi hiba |
| 38 | `084365be` | tenylegesen -> ténylegesen | tenylegesen barmelyik fajlra alkalmazta -- ez buktatta a KARBANTARTAS | valódi hiba |
| 39 | `b588a9ad` | szamozas -> számozás | - Napló: F41_wlc_hatar_ellenorzes.tsv (Préd/Ézs: KJV = WLC, TAHOT_kivonat eltér), F41_wlc_versszam_ellenorzes.tsv, F41_bsb_megfeleltetes.tsv (új oszlo | valódi hiba |
| 40 | `ea792f94` | elfogadasa -> elfogadása | Valasz a felhasznalo negy kerdesere (S1.4 elfogadasa utan, S1.5 elott): | valódi hiba |
| 41 | `02c8bfa7` | ujrafuttatva -> újrafuttatva | szerkesztesevel), ujrafuttatva: 5/5 BDB-javaslat jovahagyott, 0 javaslat. | valódi hiba |
| 42 | `36a02743` | javitva -> javítva | indoklasi hibajat (a 88ddca8-ban mar javitva) ez a kor talalta meg. A | valódi hiba |
| 43 | `8df66503` | kesobbi -> későbbi | kesobbi minoseg-javitasok: tartalom/proveniencia keveredes | valódi hiba |
| 44 | `e568ccf7` | hivja -> hívja | egyik oldal sem hivta. Javitva: mostantol a VALODI fuggvenyt hivja | valódi hiba |
| 45 | `edb326fb` | kozepes -> közepes | magas + lehetetlen típusú kozepes; a 6 MT-számozású Károli-alak Macula MT->Károli | valódi hiba |
| 46 | `0a253620` | sajat -> saját | vizsgalt igehely sajat sorabol induljunk. | valódi hiba |
| 47 | `edde7cec` | korabban -> korábban | Javitas utan: 4Moz 12 15/15, 4Moz 13 34/34 (korabban 16/33 volt) - | valódi hiba |
| 48 | `9a3f8830` | sorszamok -> sorszámok | betu-utotag-szakasz, uj sorszamok. Melleklet: a korabban itt kozolt | valódi hiba |
| 49 | `a455b06e` | jelentese -> jelentése | DT27: fuggetlen-ellenor jelentese (ELTERES, 2 tetel) | valódi hiba |
| 50 | `7319b5d4` | kereszthivatkozas -> kereszthivatkozás | Bibliai Motivumlexikon tervezesi naplo felvetele + kereszthivatkozas | valódi hiba |

A hátralévő hamis pozitívok: oszlopnevek, amelyek az `adat/*.tsv` fejlécéből nem jönnek ki (`utotag`, `indoklas`, `megjegyzes` — a `konkordancia/` és `naplok/` táblákból), `egyeb` (értékkészlet), a `vesz` (helyes szó) és egy azonosító-lista.

## 4. Mellékhatás: a séma-lista elvesz valódi hibát

A bővített lista a közönséges szavak mezőneveit is kizárja (`forras`, `cim`, `kod`, `heber`, `gorog`, `szotar`, `tanulmany`, `archiv`). Ezek prózában valódi hibák lennének (M0a: `forras` 29 találat, a 6. leggyakoribb), de oszlopnévként helyesek, és a szabály nem tudja megkülönböztetni őket (D3: inkább kihagy).

## 5. Összegzés

| | jelölt üzenet | jelölt találat | minta (50) | pontosság |
|---|---|---|---|---|
| M0a | 659 | 3416 | 42 valódi / 8 hamis | 84% |
| M0b | 626 | 3303 | 45 valódi / 5 hamis | 90% |

- Az 50 elemes minta 95%-os konfidencia-intervalluma kb. ±9–10 százalékpont, tehát a valódi pontosság 75–95% közé esik. HIBA-szinthez ez kevés.
- A jelölt üzenetek aránya (kb. 19%) magas: a repó commitjainak ötöde ékezetlen. A ma mergelt történeten az E30 emiatt csak PR `base..head`-re futhat (G4).

## 6. Megvalósítás (DT-F112a: 3. változat, 2026-10-19)

- Kizárólista: **a szűk (M0a) lista**, 21 sor — az orkesztrátor döntése (DT-F112a): az M0b bővítés (84% -> 90%) mintára illeszkedik és valódi hibát nyel el (`forras`, `cim`, `kod`), ezért nem kerül be. Az M0b szakasz tájékoztató.
- Szint: FIGYELMEZTETÉS (`SZINT['E30']`), `FAJLSZINTU_SZABALYOK` tagja; a CI nem pirosodik.
- Hatókör: csak a PR `base..head` kézi, nem-merge commitjai; `push` eseménynél és `--teljes` módban nem fut (G4). A szókészlet az alap (`base`) commitjaiból épül, a PR saját commitjai nem szólnak bele.
- Találat-részlet: rövid hash (`fajl` mező), `` `ékezetlen` -> `ékezetes` ``. Kézi futtatásnál (`--commit-uzenet-fajl`, base/head nélkül) a hash `-`.
- Kézi próba (repón kívüli ideiglenes fájl: `F9.9: ket konyv javitas, a forras naplo es allapot: fut`): 5 találat (`ket`, `konyv`, `javitas`, `forras`, `naplo`); az `allapot` a kizárási lista miatt nem jelöl, a `forras` jelöl (5 találat a `naplo`-val). A saját ág commitjain: 0 találat.
- Az újraértékelés (HIBA-szint) 20 PR után: a PR-ok jelölési aránya és a javítások száma alapján, külön döntés.
- Ismert korlát: a szabály csak kisbetűs tokent néz (`[a-z]{3,}`), ezért a mondat- vagy üzenetkezdő nagybetűs (`Javitas: …`) és a csupa nagybetűs ékezetlen szót nem jelzi. Ez szándékos (D3: inkább kihagy; a tulajdonnevek és rövidítések elkülönítése nélkül a hamis pozitív arány nőne); a hiány a 20 PR utáni újraértékelés (N-F112a) tárgya.
