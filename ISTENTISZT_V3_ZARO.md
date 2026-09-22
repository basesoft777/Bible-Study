# ISTENTISZT_V3_ZARO.md — utolsó kiejtés-pótlás

A `86604a0` állapotra. Tedd a repó gyökerébe, commitold, majd hajtsd végre Z1–Z3-at. A táblákat gépileg olvasd a fájlból (tabulátor-elválasztás, első sor fejléc). Minden „régi" a célhelyén pontosan egyszer illeszkedjen, különben ⛔.

## Z1 — Kézi szöveg (6 csere, `lexikon/ISTENTISZT-001_TUDOMANYOS.md`)

Célsor: a `86604a0` szerinti sorszám; a csere csak abban a sorban történik. A P5-ben jelzett 6 kivétel. A Peshat/Remez/Drash/Sod sorok (943–953) nem változnak.

```tsv
sor	régi	új
383	H7121 (קָרָא),	H7121 (קָרָא, kárá),
415	H8034 (שֵׁם),	H8034 (שֵׁם, sém),
906	(πᾶς ὃς ἂν ἐπικαλέσηται τὸ ὄνομα Κυρίου σωθήσεται)	(πᾶς ὃς ἂν ἐπικαλέσηται τὸ ὄνομα Κυρίου σωθήσεται – pász hosz an epikaleszétai to onoma Küriú szóthészetai)
915	(ἐπικαλέομαι),	(ἐπικαλέομαι, epikaleomai),
976	(ἐπικαλέομαι),	(ἐπικαλέομαι, epikaleomai),
1105	נִקְרָא...עַל (birtoklás	נִקְרָא...עַל (nikrá … al; birtoklás
```

## Z2 — Generált 2. szakasz: `adat/lexikon_hivatkozasok.tsv` `forditas_hu` (25 csere, 5 sor)

Célhely: a `szotar` + `strong` + `jelentes_szam` hármassal azonosított sor `forditas_hu` mezője; a csere csak abban a mezőben történik. A BDB H3548 1 sor a KIRALY-001 oldalt érinti. A két BDB-bejegyzés héber szórendje a forrásban sérült; a héber szöveg változatlan, az átírás a valódi olvasási sorrendet követi.

```tsv
szotar	strong	jelentes_szam	régi	új
BDB	H7121	2.c	׳ק י ׳בְּשֵׁם hívni	׳ק י ׳בְּשֵׁם (k. besém J., azaz kárá besém JHVH) hívni
BDB	H7121	2.c	hívni ׳י nevével	hívni ׳י (J., azaz JHVH) nevével
BDB	H7121	2.c	hogy ׳י mutassa	hogy ׳י (J., azaz JHVH) mutassa
BDB	H7121	3	׳ק צוֺם böjtöt	׳ק צוֺם (kárá com) böjtöt
BDB	H7121	3	׳ק י ׳מוֺעֲדֵי:	׳ק י ׳מוֺעֲדֵי (kárá móadé JHVH):
BDB	H7121	3	׳ק után	׳ק (k., azaz kárá) után
BDB	H7121	3	ל + személy: Jer	ל (le) + személy: Jer
BDB	H7121	3	עַל + személy (ellen	עַל (al) + személy (ellen
BDB	H7121	3	(ל + személy): Bír	(ל (le) + személy): Bír
BDB	H7121	3	׳ק לְשָׁלוֺם אֵלֶיהָ	׳ק לְשָׁלוֺם אֵלֶיהָ (kárá lesálóm éléhá)
BDB	H7121	3	מִקְרָא Ézs	מִקְרָא (mikrá) Ézs
BDB	H7121	3	הַקְּרִיאָה Jón	הַקְּרִיאָה (hakkeriá) Jón
BDB	H7121	3	(+ אֶל)	(+ אֶל (el))
BDB	H3548	1	כֹּהֲנִים מַמְלֶכֶת 2Móz	כֹּהֲנִים מַמְלֶכֶת (mamlekhet kóhaním) 2Móz
BDB	H3548	1	מִדְיָן כֹּהֵן 2Móz	מִדְיָן כֹּהֵן (kóhén midján) 2Móz
BDB	H3548	1	a כהנים is	a כהנים (kóhaním) is
TBESG	G1941	1	τ. ὄνομα, ἐπί előtt	τ. ὄνομα (t. onoma), ἐπί (epi) előtt
TBESG	G1941	1	héb. עַל. . שֻׁם קָרָא)	héb. עַל. . שֻׁם קָרָא (kárá sum … al))
TBESG	G1941	2	(θεόν, θεούς:	(θεόν (theon), θεούς (theúsz):
TBESG	G1941	2	Καίσαρα (Σεβαστόν,	Καίσαρα (Kaiszara) (Σεβαστόν (Szebaszton),
TBESG	G1941	2	ti. τ. Κύριον Ἰησοῦν,	ti. τ. Κύριον Ἰησοῦν (t. Kürion Iészún),
TBESG	G1941	2	μάρτυρα (klasszikus) τ. θεόν,	μάρτυρα (martüra) (klasszikus) τ. θεόν (t. theon),
TBESG	G1941	2	πατέρα, 1Pét	πατέρα (patera), 1Pét
TBESG	G1941	2	τ. κύριον, Róm	τ. κύριον (t. kürion), Róm
TBESG	G1941	2	τ. ὄνομα κυρίου (μου, σου; mint a héb. יְהוָֹה שֻׁם קָרָא)	τ. ὄνομα κυρίου (t. onoma küriú) (μου (mú), σου (szú); mint a héb. יְהוָֹה שֻׁם קָרָא (kárá sum JHVH))
```

## Z3 — Generálás, ellenőrzés, push

`general.py --cel mind --ir`, `--ellenoriz` fixpont, `ellenoriz.py` kód 0. Jelentés: Z1 6/6, Z2 25/25; az ISTENTISZT-001 teljes szövegében (blockquote-okon kívül, a generált részt is beleértve) szkriptes ellenőrzés a kiejtés nélküli görög/héber szavakra — a maradékot sorszámmal listázd; mely oldalak változtak; push commit-hash. Az `ISTENTISZT_V3_BRIEF.md` döntésnaplójába: v5 „Z1–Z2: utolsó kiejtés-pótlás (kézi + lexikon_hivatkozasok)".
