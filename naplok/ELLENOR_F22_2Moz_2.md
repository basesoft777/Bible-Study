# ELLENOR_F22_2Moz_2.md — második ellenőri kör

*A `fuggetlen-ellenor` ügynök 2. körös jelentése (a hatókör: `origin/main...b0ca1fd`), tömörítve a tételekre; az ügynök szerepköre csak olvasó volt (szkriptet nem futtathatott), a fájlt az orkesztrátor mentette. Az 1. kör: `naplok/ELLENOR_F22_2Moz.md`. A „Kezelés” szakasz az orkesztrátoré. Eljárási megjegyzés az ügynöktől: a közös munkakönyvtárat ellenőrzés közben más munkamenet átváltotta egy másik ágra; az ügynök ezután `git diff <üres fa | origin/main> b0ca1fd -- <fájl>`-lal olvasott. Az orkesztrátor a további munkát külön worktree-ben (`../Bible-Study-f22`) végezte.*

**Minősítés: ELTÉRÉS: 10 tétel.**

## Ami rendben volt (OK)

- **Detektor módszere és önteszt (kód):** DP-igazítás a log-vershosszra, a versszám csak `BONUSZ=0,10` döntetlen-feloldó; valódi adaton azonos versszámnál is jelez (Ézs 9: Károli 20 / eredeti 20, 17 eltolt, `ELTOLT EHIANY KORR_ELT`). Versszöveg nincs a kimenetben (a 3 grep-találat a módszerleírás). Az 1Móz: 1533/1533, 50 fejezet, 0 jelzés. A 2Móz: 35. fejezet 36/35 (`LETSZAM ELTOLT`), 36. fejezet 37/38, 37 eltolt, r(0)=0,15, d=+1, r=0,95; a lista (`versmegfeleltetes.tsv:4–41`): 35:36→36:1, 36:n→36:(n+1). Az összesítés egyezik a fejezettáblával (250 eltolt, 43 Károli-hiány, 12 eredeti-hiány, 95 jelzett fejezet, 1189 fejezet; a TSV-ben 305 adatsor).
- **`_versmegfeleltet`, `eltolt` képzés:** a TAHOT 36:1–38 mindegyike pontosan egyszer kerül be, a 36:38 kulcs megszűnik.
- **K1 a 2Mózre:** 25 733 `er` sor = a TAHOT 2Móz tokenjei; 1213 `hu`/`er` vers; 35:36: 36 hu- és 33 er-sor (a TAHOT 36:1 33 tokenje); 36:37: 22 er-sor (TAHOT 36:38).
- **1Móz, 3Móz nem érintett:** a listában nincs soruk; az 1Móz-táblák/jsonl/minta diffje üres.
- **F21-es hívók:** 8 eszköz hívja paraméter nélkül; az F21 minta bemenete nem változik (az érintett 1Kor 3:3 verset a lista nem érinti).
- **A javító menet:** a minta 38 sor (35:36, 36:1–37), `eredeti_szo` a megfeleltetett vers szószáma; 4–4 köteg, 38–38 `ok` vers; az egyesítő versenként felülír; szúrópróba (12 Strong) egyezik a TAHOT-tal; az 1. kör hamis linkje („járuljon” ↔ H3045) eltűnt. Táblaösszegek: parok 24 487 (magas 23 265, alacsony 1 222), szavak magas 44 591, kezi 0; 36. fejezet 657 link/603 magas; 35. fejezet 618/576.
- **C javító futás:** 4 sor `c/2Moz_javito`, mind `84f12ca7aafb`, kapuhiba 0, 38 vers, 0,044636 USD, 32 721/5 359 token; a plafon 1,00 USD (minimum); `f21p/` változatlan.
- **1. kör kezelése, brief, kulcs-grep, zárt licencű adat:** rendben (a részletek az ügynök jelentésében); a brief `allapot: dontesre_var`, `kovetkezo` „Te:”-vel kezdődik.
- **Nem ellenőrizhető az ügynök szerepköréből:** `egyesit.py --ellenoriz` és K7 (futtatás), a /usage, a CI-jelentés, a PR címe (E16).

## Eltérések (súlyossági sorrendben) és a Kezelés

| # | Eltérés | Súly | Kezelés (az orkesztrátor) |
|---|---|---|---|
| 1 | A detektor az Ézs 9:18–20-at hamisan felelteti meg (a Károli 9:18 a TAHOT 9:17, nem a 9:18); más könyvekben a lista nincs igazolva, a jelentés 5.5 állítása („a későbbi könyvek már a megfeleltetett verset kapják”) nem áll | magas | **Kezelve (szűkítéssel; a módszer javítása nyitott):** `tokenek.VERSBEOSZTAS_JOVAHAGYOTT = ('2Móz',)`: a futtató csak a jóváhagyott könyvek sorait alkalmazza (a `versmegfeleltetes(jovahagyott=False)` az összeset adja); a jelentés 5.5 kimondja, hogy a lista más könyvekben javaslat, az Ézs 9-et példaként megnevezi. A detektor DP-je az Ézs 9 keresztfejezetes eltolódását (Héber 9:1 = Károli 8:23 stb.) nem oldja meg; ez nyitott (N-F22), a 3Mózes előtt a felhasználó látja az eredményt. |
| 2 | `tokenek._versmegfeleltet`: a `nincs_eredeti` Károli-kulccsal azonos kulcsú TAHOT-verset nyomtalanul eldobja (Jób 40:13/16/19, 34 token); a K1-ellenőrzés a leképezett folyamhoz mér | magas (a 2Mózt nem érinti) | **Javítva:** a Károli-oldali kulcsokon álló, de egyetlen sorban sem szereplő eredeti vers gazdátlanná válik (`+1000`-es azonosító), az egyesítő `kezi`-ben viszi; önteszt (`versbeosztas.py --onteszt`) fedi. A jóváhagyott-könyv szűkítés miatt a Jób jelenleg nem is érintett. |
| 3 | A 2Móz-táblák proveniencia-sora nem nevezi meg a javító jsonl-eket és a `versmegfeleltetes.tsv`-t; a `ts` elavult | közepes | **Javítva:** `egyesit.proveniencia_sor` / `bemeneti_ts`: a `forras` a javító menet jsonl-jeit és a listát is tartalmazza (csak ahol van), a `ts` a javító menet utolsó hívása (20:20:36); az 1Móz sora bájtra változatlan. |
| 4 | A jelentés 1. szakasza (7–8. sor) elavult | alacsony | **Javítva.** |
| 5 | A jelentés 5.3 „eleve kihagyja” állítása elavult | alacsony | **Javítva** (nyers kulcs vs. megfeleltetés utáni kimaradás). |
| 6 | `F22_nincs_parja_versek.tsv` a mostani generátorral nem reprodukálható | alacsony | **Javítva:** a generátor `betolt_eredeti(versmegf=False)`-t olvas; újrafuttatva 61 + 30 vers (az eredeti darabszám). |
| 7 | A `4Móz 30:1001` ál-igehely és a hatás nélküli `nincs_karoli` sor (Róm 8:38) nincs dokumentálva | alacsony | **Dokumentálva** (SEMA 2.20); a Róm 8:38 sor a jóváhagyott-szűrés miatt nem érvényesül. |
| 8 | A SEMA nem mondja ki, hogy az `er` sorok `vers`-kulcsa a Károli-kulcs | alacsony | **Javítva** (SEMA 2.20). |
| 9 | A detektor önteszt „váratlan jelzés” ága sosem bukhat el | alacsony | **Javítva:** 5 fejezetes tesztfolyam, minden nem érintett fejezet jelzésmentességét ellenőrzi. |
| 10 | A jelentés 5.5 az ApCsel 24 jelzését kihagyja | alacsony | **Javítva.** |
| — | A trigger csak `[claude/f22-1moz, claude/f22-2moz]` | alacsony | **Javítva:** `branches: ['claude/f22-*']`. |
| — | A docstring-példa (`eredeti_nelkuli_versek`) elavult | alacsony | **Javítva.** |
| — | Az `egyesit` felülírás rejtett kockázata (ha egy újraleképezett vers hiányozna a javító menetből, a fő menet régi indexei némán a leképezett versre kerülnének) | megjegyzés | **Nyitva, dokumentálva:** a 2Mózre mind a 38 vers megvan; általános védelem (a javító menet verslistájának és a leképezés eltolt soraiknak az összevetése) az N-F22 tétele. |

Az orkesztrátor oldalán lefuttatott ellenőrzések a javítások után: `versbeosztas.py --onteszt`, `egyesit.py --onteszt`, `sonnet_koteg.py --onteszt`, `f22_c_futtat.py --onteszt` rendben; `egyesit.py --konyv 2Móz --ellenoriz` és `--konyv 1Móz --ellenoriz` „rendben”; a 2Móz táblák újraépítése bájtra azonos (K7); az 1Móz táblák változatlanok. A javítások utáni **harmadik, független kör nem készült**.
