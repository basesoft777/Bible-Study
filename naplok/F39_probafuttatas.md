# F39 próbafuttatás (indítás nélkül)

*2026.10.01 · ág: `claude/upbeat-wright-81rpah` · a `/kovetkezo` 1. lépésének parancsai; semmi nem indult el*

## ellenoriz
```
FIGYELEM	F37_TANULMANY_ELLENORZES_BRIEF.md	az `ir` helyettesítő mintát tartalmaz (naplok/): adj meg konkrét fájlt
59 brief, 0 hiba, 1 figyelmeztetés
```

## jeloltek
```
KIHAGYVA	#7	állapot: brief_kell
JELOLT	#22	"Károli–Strong párosítás könyvenként, két modellel (Sonnet + Gemini); első könyv: 1Mózes"
KIHAGYVA	#23	vár: #37
KIHAGYVA	#27	halasztva
KIHAGYVA	#30	vár: #32, #39
JELOLT	#33	Forrásaink licencének rendezése (az F24 utófeladata)
JELOLT	#35	Régi „Sir” hivatkozások migrálása JSir-re és a „Szentlélek” / „Isten Lelke” helyek egységesítése „Szent Szellem”-re
JELOLT	#38	A teljes BDB héber szótár magyar fordítása Opusszal, megállási pontokkal
CSOMAG	#22 #33 #35 #38
```

## fuggesek (KIZAR, FIGYELEM, KOR sorok)
```
KIZAR	9	32	MUNKAMENET.md	×
KIZAR	9	36	lexikon/	×
KIZAR	9	37	MUNKAMENET.md	×
KIZAR	26	30	CLAUDE.md	×
KIZAR	26	32	CLAUDE.md	×
KIZAR	30	32	CLAUDE.md	×
KIZAR	30	37	eszkozok/ellenorzes/	×
KIZAR	32	37	MUNKAMENET.md	×
KIZAR	32	39	eszkozok/feladatok.py	×
```

## tesztek
```
----------------------------------------------------------------------
Ran 60 tests in 0.160s

OK
```

## Értékelés

A várt jelölt #35, #38, #23 volt. A valós állapot: **#35 és #38 jelölt**, ezek mellett a #22 (`dontesre_var`; a DONTESEK nyitott tételeit az orkesztrátor a 3. lépésben külön vizsgálja) és a #33 (a `kovetkezo` mezője előfeltételt ír: a DT-F24 „alkalmazva”) mechanikusan szabad. A **#23 nem jelölt: vár a #37-re**, mert az `ATALAKITASI_TERV.md.md`-t olvassa (F23 `olvas`), a #37 pedig írja (F37 `ir`). Ez valódi írás–olvasás sorrend (2. szabály), a javítás nem szünteti meg. A `sablonok/` olvasás kontextus (könyvtár-prefix), az nem ad sorrendet. A #37 viszont nem 1. fázisú és több feladatra vár, ezért a #23 gyakorlatilag a #37 után indulhat; ha ezt nem akarod, a #23 `olvas` listájának szűkítése tartalmi döntés (nem az orkesztrátoré).
