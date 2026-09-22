# ISTENTISZT_V3_POTLAS.md — egyetlen végrehajtási prompt

Ez a fájl az `ISTENTISZT_V3_BRIEF.md` pótlása: minden szükséges szöveg és csere-tábla benne van. Más forrásra nincs szükség. A fájlt másold a repó gyökerébe, commitold (`ISTENTISZT_V3_POTLAS.md`), majd hajtsd végre a P1–P6 tételeket sorrendben. Megállás (⛔) csak a jelzett pontokon.

## Közös szabályok

- A csere-táblák oszlopait **tabulátor** választja el; első sor a fejléc. A beolvasás gépi legyen (a táblát a fájlból olvasd, ne kézzel másold).
- Minden csere a „régi" szöveg alapján történik, a megadott sorszámú sorban (a `65d581b` szerinti sorszám, az I3/I4 betoldások miatt eltolódhatott: keresd meg a sort úgy, hogy a „régi" szöveg pontosan egyszer forduljon elő benne). `I3c` sorszám = az I3(c)-vel beszúrt kiegészítő blokk. Ha egy „régi" nulla vagy több helyen illeszkedik, ⛔ állj meg és jelentsd a sort.
- A blockquote-ok (`>` kezdetű sorok, forrásidézetek) **nem változnak**; a kiejtés a magyar fordításba és a kézi prózába kerül.
- Ez jóváhagyott kézi szövegmódosítás (G11 kivétel). A csere-táblákon kívül a kézi szöveg bájtra azonos marad.
- Minden tétel után `ellenoriz.py` kód 0, és tételenként commit.

## P1 — Thayer G1941 fordítás, kiejtéssel

A `adat/lexikon_hivatkozasok.tsv` `szotar=Thayer`, `strong=G1941` sorának `forditas_hu` mezője legyen pontosan a következő (egy sor, a mostani, kiejtés nélküli szöveg helyett):

```
G1941 — ἐπικαλέω (epikaleó), ἐπικαλῶ (epikaló): 1. aorisztosz ἐπεκαλεσα (epekalesza); (szenvedő és közép alak, jelen idő ἐπικαλοῦμαι (epikalúmai)); perfektum szenvedő ἐπικέκλημαι (epikeklémai); pluskvamperfektum egyes szám 3. személy ἐπεκέκλητο (epekekléto), és az augmentum elhagyásával (vö. Winer, Grammatika, 12. §, 5; Buttmann, 33 (29)) ἐπικεκλητο (epikekléto) (ApCsel 26:32, Lachmann); 1. aorisztosz szenvedő ἐπεκλήθην (epekléthén); jövő idő közép ἐπικαλέσομαι (epikaleszomai); 1. aorisztosz közép ἐπεκαλεσάμην (epekaleszamén); a Septuagintában igen gyakran a קָרָא (kárá) fordítása; 1. nevet tenni valakire, melléknéven nevezni: τινα (tina) (Xenophón, Platón és mások), Mt 10:25 G T Tr WH (a Rec.-ben ἐκάλεσαν (ekaleszan)); szenvedő alakban ὁ ἐπικαλούμενος (ho epikalúmenosz): akit melléknéven neveznek, Lk 22:3 R G L; ApCsel 10:18; 11:13; 12:12; 15:22 R G; továbbá ὅς ἐπικαλεῖται (hosz epikaleitai), ApCsel 10:5; 10:32; ὁ ἐπικληθείς (ho epiklétheisz), Mt 10:3 (R G); ApCsel 4:36; 12:25; egyenértékű a ὅς ἐπεκλήθη (hosz epekléthé) kifejezéssel, ApCsel 1:23. Közép jelentésű szenvedő alak (vö. Winer, Grammatika, 38. §, 3): megengedni, hogy valakit melléknéven nevezzenek: Zsid 11:16; közép alak τινα (tina)-val: 1Pét 1:17 εἰ πατέρα ἐπικαλεῖσθε τόν (ei patera epikaleiszthe ton) stb., azaz ha (magatoknak) Atyaként hívjátok őt, azaz ha Atyátoknak nevezitek. 2. ἐπικαλεῖται τό ὄνομα τίνος ἐπί τινα (epikaleitai to onoma tinosz epi tina), a héber פ עַל פ... שֵׁם נִקְרָא... (pe al pe … sém nikrá …) mintájára: „valakinek a nevét nevezik valaki fölött, azaz az ő nevéről nevezik, vagy neki szenteltnek nyilvánítják" (vö. Gesenius, Thesaurus iii., 1232a. o.): ApCsel 15:17, az Ám 9:12-ből (a szóban forgó név Isten népéé); Jak 2:7 (a név: οἱ τοῦ Χριστοῦ (hoi tú Khrisztú)). 3. τίνι (tini), a tárgy tárgyesetével; tulajdonképpen: valamit rákiáltani valakire (vö. angol to cry out upon (or against) one); „valamit bűnként vagy szemrehányásként valakinek a terhére róni; valakit valamilyen vádpont alapján perbe idézni, bűncselekményért perbe fogni; hibáztatni valakit valamiért, vádolni valakit valamivel" (Arisztophanész, Béke 663; Thuküdidész 2, 27; 3, 36; Platón, Törvények 6, 761 e.; 7, 809 e.; Dio Cassius 36, 28; 40, 41, és gyakran a szónokoknál (vö. a κατηγορέω (katégoreó) címszót)): εἰ τῷ οἰκοδεσπότῃ Βηλζεβουλ ἐπεκάλεσαν (ei tó oikodeszpoté Bélzebúl epekaleszan) (azaz a Belzebúllal való kapcsolattal, az ő segítségének elfogadásával vádolták, vö. Mt 9:34; 12:24; Mk 3:22; Lk 11:15), πόσῳ μᾶλλον τοῖς ὀικιακοις αὐτοῦ (poszó mallon toisz oikiakoisz autú), Mt 10:25, L WH széljegyzeti olvasata a Vaticanus nyomán (lásd fent az 1. pontot); ezt az olvasatot Rettig védte a Studien und Kritiken 1838-as évfolyamában, 477. skk. o., valamint Alexander Buttmann (1873) ugyanebben a folyóiratban, 1860, 343. o., és újszövetségi grammatikájában is, 151 (132); (továbbá Weiss a Meyer-kommentár 7. kiadásában, az adott helynél). Ez a kifejezés azonban (Belzebúl a Belzebúl segítsége helyett) túl nehézkes ahhoz, hogy ne valamely tudatlan írnok javítását sejtesse, aki azon botránkozott meg, hogy (e hely kivételével) az evangéliumokban sehol sem mondják Jézus ellenségeiről, hogy Belzebúlnak nevezték volna őt. 4. segítségül hívni (mint a német anrufen), invokálni; közép alakban: segítségül hívni magának, a maga javára: valakit segítőként, ApCsel 7:59, ahol τόν κύριον Ἰησοῦν (ton kürion Iészún) értendő (βοηθόν (boéthon), Platón, Euthüdémosz 297 c.; Diodórosz 5, 79); τινα μάρτυρα (tina martüra): tanúmul, 2Kor 1:23 (Platón, Törvények 2, 664 c.); bíróként, azaz hozzá fellebbezni, hozzá folyamodni: Καίσαρα (Kaiszara), ApCsel 25:11; 26:32; 28:19; (τόν Σεβαστόν (ton Szebaszton), ApCsel 25:25); szenvedő főnévi igenévvel, ApCsel 25:21 (hogy megtartassék). 5. héber mintára (mint a יְהוָה בְּשֵׁם קָרָא (kárá besém JHVH): segítségül hívni a JHVH név kimondásával, 1Móz 4:26; 12:8; 2Kir 5:11 stb.; vö. Gesenius, Thesaurus, 1231b. o. (vagy héber szótára a קָרָא (kárá) címszónál); a kifejezés magyarázata az, hogy az Istenhez intézett imádságok rendszerint az isteni név segítségül hívásával kezdődtek: Zsolt 3:2; 6:2; 7:2 stb.) ἐπικαλοῦμαι τό ὄνομα τοῦ κυρίου (epikalúmai to onoma tú küriú): segítségül hívom (a magam javára) az Úr nevét, azaz segítségül hívom, imádom, tisztelem az Urat, azaz Krisztust: ApCsel 2:21 (a Jóel 2:32-ből); ApCsel 9:14, 21; 22:16; Róm 10:13; 1Kor 1:2; τόν κύριον (ton kürion), Róm 10:12; 2Tim 2:22; (a görög íróknál gyakran ἐπικαλεῖσθαι τούς Θεούς (epikaleiszthai túsz Theúsz), mint Xenophón, Cyril [értsd: Kürupaideia] 7, 1, 35; Platón, Tímaiosz 27 c.; Polübiosz 15, 1, 13).
```

## P2 — Kiejtés a 2/b „🇭🇺 Magyarul" bekezdéseiben (54 csere)

```tsv
sor	régi	új
385	׳ק בְּשֵׁם י׳ 	׳ק בְּשֵׁם י׳ (k. besém J., azaz kárá besém JHVH) 
385	hogy ׳י mutassa	hogy ׳י (J., azaz JHVH) mutassa
389	׳ק után	׳ק (k., azaz kárá) után
410	shem I. שֵׁם_864	shem I. שֵׁם (sém)_864
410	Thes.: שׁמה,	Thes.: שׁמה (smh),
410	BN 160: ושׁם,	BN 160: ושׁם (vsm),
410	(különösen הַשֵּׁם = יהוה)	(különösen הַשֵּׁם (hassém) = יהוה (JHVH))
410	főníciai שם;	főníciai שם (sm);
410	sabeus סם;	sabeus סם (szm);
410	arámi שְׁמָא שֵׁם,	arámi שְׁמָא (semá) שֵׁם (sém),
410	palmürai שם)	palmürai שם (sm))
410	abszolút állapotban ׳שׁ	abszolút állapotban ׳שׁ (s., azaz sém)
410	állapotban ׳שׁ 1Móz 12:8	állapotban ׳שׁ (s., azaz sém) 1Móz 12:8
431	ἐπι-καλέω (összevont alakban: ἐπικαλῶ)	ἐπι-καλέω (epi-kaleó) (összevont alakban: ἐπικαλῶ (epikaló))
431	héber קָרָא fordítására	héber קָרָא (kárá) fordítására
431	τ. ὄνομα, ἐπί előtt	τ. ὄνομα (t. onoma), ἐπί (epi) előtt
431	héb. עַל..שֻׁם קָרָא)	héb. עַל..שֻׁם קָרָא (kárá sum … al))
431	(θεόν, θεούς:	(θεόν (theon), θεούς (theúsz):
431	Καίσαρα (Σεβαστόν,	Καίσαρα (Kaiszara) (Σεβαστόν (Szebaszton),
431	ti. τ. Κύριον Ἰησοῦν,	ti. τ. Κύριον Ἰησοῦν (t. Kürion Iészún),
431	μάρτυρα (klasszikus) τ. θεόν,	μάρτυρα (martüra) (klasszikus) τ. θεόν (t. theon),
431	πατέρα, 1Pét	πατέρα (patera), 1Pét
431	τ. κύριον, Róm	τ. κύριον (t. kürion), Róm
431	τ. ὄνομα κυρίου (μου, σου; mint a héb. יְהוָֹה שֻׁם קָרָא)	τ. ὄνομα κυρίου (t. onoma küriú) (μου (mú), σου (szú); mint a héb. יְהוָֹה שֻׁם קָרָא (kárá sum JHVH))
437	G1941 — ἐπικαλέω …	G1941 — ἐπικαλέω (epikaleó) …
437	a קָרָא fordítása	a קָרָא (kárá) fordítása
437	τινα, Mt 10:25	τινα (tina), Mt 10:25
437	ὁ ἐπικαλούμενος, „	ὁ ἐπικαλούμενος (ho epikalúmenosz), „
437	ἐπικαλεῖται τό ὄνομα τίνος ἐπί τινα, a	ἐπικαλεῖται τό ὄνομα τίνος ἐπί τινα (epikaleitai to onoma tinosz epi tina), a
437	3. τίνι tárgy	3. τίνι (tini) tárgy
437	a יְהוָה בְּשֵׁם קָרָא,	a יְהוָה בְּשֵׁם קָרָא (kárá besém JHVH),
437	ἐπικαλοῦμαι τό ὄνομα τοῦ κυρίου,	ἐπικαλοῦμαι τό ὄνομα τοῦ κυρίου (epikalúmai to onoma tú küriú),
437	τόν κύριον, Róm	τόν κύριον (ton kürion), Róm
453	καλέω (összevont alakban: καλῶ)	καλέω (kaleó) (összevont alakban: καλῶ (kaló))
453	a קרא fordítására	a קרא (kárá) fordítására
453	ἐκ előtt	ἐκ (ek) előtt
464	βοάω (összevont alakban: βοῶ; vö. βοή)	βοάω (boaó) (összevont alakban: βοῶ (boó); vö. βοή (boé))
464	a זעק, צעק, קרא fordítására	a זעק (záak), צעק (cáak), קרא (kárá) fordítására
464	héb. זעק על,	héb. זעק על (záak al),
464	Szinonimák: καλέω:	Szinonimák: καλέω (kaleó):
464	; κράζω: kiáltani	; κράζω (kradzó): kiáltani
464	; κραυγάζω: a κράζω nyomatékos	; κραυγάζω (kraugadzó): a κράζω (kradzó) nyomatékos
464	A βοάω érzelmet	A βοάω (boaó) érzelmet
470	G994 — βοάω …	G994 — βοάω (boaó) …
470	a קָרָא, זָעַק, צָעַק fordítása	a קָרָא (kárá), זָעַק (záak), צָעַק (cáak) fordítása
470	3. πρός τινα:	3. πρός τινα (prosz tina):
470	az אֶל...זָעַק fordításaként	az אֶל...זָעַק (záak … el) fordításaként
470	(Vö.: ἀναβοάω, ἐπιβοάω.)	(Vö.: ἀναβοάω (anaboaó), ἐπιβοάω (epiboaó).)
500	ὃν Βριάρεων καλέουσι θεοί („	ὃν Βριάρεων καλέουσι θεοί (hon Briareón kaleúszi theoi) („
500	ὄνομα καλεῖν τινα, „	ὄνομα καλεῖν τινα (onoma kalein tina), „
500	κ. ὄνομα ἐπί τινι, „	κ. ὄνομα ἐπί τινι (k. onoma epi tini), „
500	κ. τινὰ ἐπὶ τῷ ὀνόματι τοῦ πατρός, „	κ. τινὰ ἐπὶ τῷ ὀνόματι τοῦ πατρός (k. tina epi tó onomati tú patrosz), „
500	ὁ καλούμενος, „	ὁ καλούμενος (ho kalúmenosz), „
514	קָרָא [héber ige]	קָרָא (kárá) [héber ige]
```

A 385. sor első „régi" és „új" értéke szóközre végződik — ez szándékos.

## P3 — Kiejtés a többi kézi szövegben (46 csere)

Érintett helyek: a Mounce- és SECE-táblák (482–492), az LSJ- és SECE-bekezdések (496–518), a βοάω-megjegyzés (525–528), a „Miért fontos" (542, 546), a Minősítés (745, 754 és az I3c blokk), az Alátámasztás (879, 889), a PaRDeS keretrendszer (980), a Módszertani napló (1019, 1032) és a D-minta (1083–1098). A 525. sorban a „βοáω" latin á-t tartalmazó elírás; a csere a helyes görög alakra javítja.

```tsv
sor	régi	új
482	| ἐπικαλέω (G1941) |	| ἐπικαλέω (epikaleó, G1941) |
483	| καλέω (G2564) |	| καλέω (kaleó, G2564) |
484	| βοάω (G994) |	| βοάω (boaó, G994) |
484	… πρός τινα: segítségül	… πρός τινα (prosz tina): segítségül
490	| ἐπικαλέω (G1941) |	| ἐπικαλέω (epikaleó, G1941) |
490	זָכַר, מָצָא, נָקַב, עָשָׂה, **קָרָא**, שׂוּם, שָׁכַן, שֻׁם |	זָכַר (zákar), מָצָא (mácá), נָקַב (nákav), עָשָׂה (ászá), **קָרָא** (kárá), שׂוּם (szúm), שָׁכַן (sákan), שֻׁם (sum) |
491	| καλέω (G2564) |	| καλέω (kaleó, G2564) |
491	אָמַר, בֹּוא, דָבַר, הָיָה, זָכַר, זָעַק, לָקַח, עֲלַל, **קָרָא**, רוּם, שֵׁם |	אָמַר (ámar), בֹּוא (bó), דָבַר (dávar), הָיָה (hájá), זָכַר (zákar), זָעַק (záak), לָקַח (lákah), עֲלַל (alal), **קָרָא** (kárá), רוּם (rúm), שֵׁם (sém) |
492	| βοάω (G994) |	| βοάω (boaó, G994) |
492	אָמַר, הָגָה, הָמָה, זָעַק, זַעַק, כָּנָה, נָהַם, נָהַק, נָשָׂא, פָּצַח, צָהַל, צָוַח, צָעַק, צָרַח, **קָרָא**, רוּעַ, רָעַם, שָׁאַג, שָׁבַע, שָׁעָה |	אָמַר (ámar), הָגָה (hágá), הָמָה (hámá), זָעַק (záak), זַעַק (zaak), כָּנָה (káná), נָהַם (náham), נָהַק (náhak), נָשָׂא (nászá), פָּצַח (pácah), צָהַל (cáhal), צָוַח (cávah), צָעַק (cáak), צָרַח (cárah), **קָרָא** (kárá), רוּעַ (rúa), רָעַם (ráam), שָׁאַג (sáag), שָׁבַע (sáva), שָׁעָה (sáá) |
496	— καλέω teljes	— καλέω (kaleó) teljes
502	a καλέω klasszikus	a καλέω (kaleó) klasszikus
502	a καλέω elsődleges	a καλέω (kaleó) elsődleges
502	az ἐπικαλέομαι-t (ami maga is a καλέω-ból	az ἐπικαλέομαι-t (epikaleomai) (ami maga is a καλέω-ból (kaleó)
504	Az ἐπικαλέω LSJ	Az ἐπικαλέω (epikaleó) LSJ
504	a καλέω alapigéhez	a καλέω (kaleó) alapigéhez
516	ἄγω, ἀναβοάω, ἀναγγέλλω, ἀναγινώσκω, ἀνακράζω, ἀνοίγω,	ἄγω (agó), ἀναβοάω (anaboaó), ἀναγγέλλω (anangelló), ἀναγινώσκω (anaginószkó), ἀνακράζω (anakradzó), ἀνοίγω (anoigó),
516	**βοάω**, ..., ἐγκαλέω,	**βοάω** (boaó), ..., ἐγκαλέω (enkaleó),
516	**ἐπικαλέομαι** (kétszer	**ἐπικαλέομαι** (epikaleomai; kétszer
516	**καλέω**, κηρύσσω, κράζω, ..., ὀνομάζω, παρακαλέω, προσκαλέομαι, ..., φωνέω.	**καλέω** (kaleó), κηρύσσω (kérüsszó), κράζω (kradzó), ..., ὀνομάζω (onomadzó), παρακαλέω (parakaleó), προσκαλέομαι (proszkaleomai), ..., φωνέω (fóneó).
518	H8034 (שֵׁם)	H8034 (שֵׁם, sém)
518	θρόνος, **καλέω**, καλός, καύχημα, **ὄνομα** (kétszer), Σήμ.	θρόνος (thronosz), **καλέω** (kaleó), καλός (kalosz), καύχημα (kaukhéma), **ὄνομα** (onoma; kétszer), Σήμ (Szém).
525	a βοáω saját	a βοάω (boaó) saját
526	καλέω-val és a κράζω-val	καλέω-val (kaleó) és a κράζω-val (kradzó)
528	ἐπικαλέομαι-tól.	ἐπικαλέομαι-tól (epikaleomai).
542	(βοάω ≠ ἐπικαλέομαι,	(βοάω (boaó) ≠ ἐπικαλέομαι (epikaleomai),
542	fordítói döntés (βοάω)	fordítói döntés (βοάω, boaó)
542	illeszkedik a βοάω tipikus	illeszkedik a βοάω (boaó) tipikus
542	eltérést az ἐπικαλέομαι-tól.	eltérést az ἐπικαλέομαι-tól (epikaleomai).
546	tartalmazza a קָרָא-t (kiemelve)	tartalmazza a קָרָא-t (kárá) (kiemelve)
546	a קָרָא fordítása	a קָרָא (kárá) fordítása
546	(ἐπικαλέομαι, καλέω, βοάω)	(ἐπικαλέομαι – epikaleomai, καλέω – kaleó, βοάω – boaó)
745	nincs ἐπικαλέομαι/καλέω a versben	nincs ἐπικαλέομαι (epikaleomai) / καλέω (kaleó) a versben
754	H7121+H8034/ἐπικαλέομαι formulát	H7121+H8034 / ἐπικαλέομαι (epikaleomai) formulát
879	(ἐπικαλέομαι vs. καλέω)	(ἐπικαλέομαι – epikaleomai vs. καλέω – kaleó)
889	(ἐπικαλέομαι/ἐπικαλεῖσθε)	(ἐπικαλέομαι – epikaleomai / ἐπικαλεῖσθε – epikaleiszthe)
980	ugyanez a קָרָא+שֵׁם	ugyanez a קָרָא+שֵׁם (kárá + sém)
1019	15/17 ἐπικαλέομαι;	15/17 ἐπικαλέομαι (epikaleomai);
1032	קָרָא + שֵׁם szerkezet	קָרָא (kárá) + שֵׁם (sém) szerkezet
1083	+ עַל elöljárószó	+ עַל (al) elöljárószó
1084	aktív קָרָא + בְּ szerkezetével	aktív קָרָא (kárá) + בְּ (be) szerkezetével
1091	elöljárószó (בְּ	elöljárószó (בְּ – be
1092	vs. עַל),	vs. עַל – al),
1098	קָרָא+שֵׁם szerkezetnek	קָרָא+שֵׁם (kárá + sém) szerkezetnek
I3c	(H7121, שֵׁם – sém nélkül)	(H7121, שֵׁם (sém) nélkül)
I3c	(τόν κύριον – ton kürion, név nélkül)	(τόν κύριον (ton kürion), név nélkül)
```

## P4 — UBS-oszlop: az üres cellák jelölése (generátor, mind a 8 oldal)

Mért állapot (`65d581b`): az UBS-cella „—" (1) minden ószövetségi sorban, mert az UBS Greek New Testament Dictionary csak az Újszövetséget fedi; (2) 6 újszövetségi sorban, amelyeknek nincs G-tokenje (HAMART-001: Mt 15:19, Mk 7:21-23, 2Pét 3:6-7; MENNY-001: 2Pét 2:4-5, Júd 1:6, Júd 1:14-15); (3) az ANTROP-001 1Kor 2:15 sorában, ahol a token összetett (`G4151+G5590`), és a generátor nem bontja szét.

`eszkozok/lexikon_general.py`:
1. Ószövetségi sor: az UBS-cella szövege `— *(ÓSZ)*`.
2. G-token nélküli újszövetségi sor: `— *(nincs G-token)*`.
3. Összetett tokennél (`+` jellel) a generátor tokenenként végzi a hozzárendelést, és a jelentéseket `G4151: … · G5590: …` alakban, egy cellában adja.
4. Az Előfordulások tábla alatti jelmagyarázat-sorba: „Az UBS-jelentés csak újszövetségi soroknál áll: az UBS Greek New Testament Dictionary az Újszövetséget fedi."
Ellenőrzés: egyik oldalon sincs üres vagy csupasz `—` UBS-cella; az 1Kor 2:15 cellája mindkét tokent tartalmazza (ha valamelyikhez nincs UBS-hozzárendelés, annál `fordítás függőben`/`nincs hozzárendelés` jelölés áll, nem üres).

## P5 — Generálás és ellenőrzés

`general.py --cel mind --ir`, majd `--ellenoriz` fixpont; `ellenoriz.py` kód 0. Ellenőrizd és jelentsd:
1. P2: 54/54, P3: 46/46 csere illeszkedett;
2. a G1941 Thayer-blokkban a görög szavak mellett kiejtés áll;
3. az ISTENTISZT-001 kézi szövegében (blockquote-okon kívül) nem maradt kiejtés nélküli görög vagy héber szó — szkriptes ellenőrzés; a kivételeket (ha vannak) sorszámmal listázd, ne javítsd;
4. P4 ellenőrzése mind a 8 oldalon;
5. a Kivonat kitöltött, a státusz v3 (az ISTENTISZT_V3_BRIEF I5–I6 szerint).

## P6 — Push

`git push`, majd rövid jelentés: a P5 öt pontja, az `ellenoriz.py` összesítője, a push commit-hash. Az `ISTENTISZT_V3_BRIEF.md` döntésnaplójába: v2 „P1: I2 kiejtéssel", v3 „P2–P3: kiejtés a kézi szövegben", v4 „P4: UBS-cellák jelölése".

## Döntésnapló

| Dátum | Döntés |
|---|---|
| 2026.09.22 | **P2, sor=385, régi=„hogy ׳י mutassa"** két nem-idézet sorban illeszkedett: 355. (a `## 2. Szótári háttér` generált `#szocikkek` blokkjában, G1941-alszakasz) és 392. (a kézi `### 2/b. Teljes szótári anyag` alatt, „🇭🇺 Magyarul (BDB):" bekezdés). Döntés: csak a 392. (2/b) sor kapja a cserét; a 355. változatlan. |
| 2026.09.22 | **Szabálypontosítás (P2/P3 egyediség-ellenőrzés):** az illeszkedést csak a kézi szövegben kell keresni — a `<!-- GENERÁLT-KEZDET … -->`/`<!-- GENERÁLT-VÉGE … -->` közötti sorok (a határoló sorokkal együtt) és a blockquote-sorok (`>`-lal kezdődők) ki vannak zárva a keresési/csere-halmazból. Az egyediség ezen a szűrt halmazon értendő; ha így is 0 vagy több illeszkedés van, ⛔. |
| 2026.09.22 | **Generált 2. szakasz kiejtés-hiánya:** a generált `#szocikkek` blokkban (`lexikon_hivatkozasok.tsv` `forditas_hu` mezőiből) kiejtés nélkül maradó görög/héber szavakat a P2/P3 nem javítja a `.md`-ben (kézi szöveg csak); a forrás-tsv soronkénti javítása külön csere-táblát kap. A P5 jelentés felsorolja az érintett `lexikon_hivatkozasok.tsv`-sorokat (szotar, strong, jelentes_szam) és a `forditas_hu` teljes szövegét. |
