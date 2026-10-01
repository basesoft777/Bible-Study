# F28 E4a — Első adag (beépített pilot, 5 szócikk)

*Brief: `F28_EMELES_BRIEF.md` v4, 3. pont 5. lépés · generálta: `python eszkozok/emeles.py naplo_nezet …` a `naplok/EMELES_munka.tsv`-ből · 2026.10.01*

**⛔ Jóváhagyásra vár.** A felhasználó dönt: rendben van-e az 5 fordítás (akkor `kezi`
állapottal kerülnek az `adat/forditasok.tsv`-be, és jöhet a maradék), vagy a prompt v4
javul, és az 5 szócikk újrafordul. A kérdés a `DONTESEK.md` DT-F28-1 tételében.

## Az adag összetétele

| Réteg (brief) | Szócikk | Megjegyzés |
|---|---|---|
| 1 rövid Thayer (a lista legrövidebbje) | **G1944** (337 kar.) | a briefszövegű listán (`naplok/EMELES_lista.tsv`) ez a legrövidebb Thayer-szócikk; a `--szeles` halmazban a G0035 (186 kar.) lenne az (l. `naplok/EMELES_naplo.md` E0) |
| G5590 (hosszú Thayer) | **G5590** (5 950 kar.) | a listán van |
| 1 rövid BDB (a lista legrövidebbje) | **H6093** (187 kar.) | mindkét halmazban ez a legrövidebb |
| H7121 (igetörzses BDB-ige) | **H7121** (10 780 kar.) | a meglévő kézi 2.c és 3 jelentéssel összevetve, l. lent |
| H1121 (óriás) | **H1121** (14 948 kar.) | darabolás nélkül fordult (a kimenet elfért) |

Helyettesítésre nem volt szükség: mind az öt szócikk a listán van.

## Módszer — eltérés a brief E4 leírásától

- **Fordító:** a menet maga, Opus-modellen (`claude-opus-5-5`); `vegrehajto-opus`
  subagent indítására ebben a futtatókörnyezetben nem volt eszköz. A fordítás a
  `forditas/prompt_v4.md` szabályai szerint készült (a kitöltött prompt:
  `python eszkozok/emeles.py prompt <Strong>`), a terminológia az `adat/terminologia.tsv`
  v1.
- **Héber és görög szakaszok:** a fordítás helyőrzős forrásból készült
  (`emeles.py helyorzo`: minden összefüggő héber/görög szakasz ⟦n⟧ jelet kap), és a
  szakaszok gépileg, betűhíven kerültek vissza (`emeles.py ellenoriz --mappa`). Így a
  v4 BDB-blokk 3. szabálya („a héber szöveg változatlan, a jobbról balra írással
  együtt”) a forrás néhol fordított szórendjét is megőrzi; az 1. kapu ezt utólag is
  ellenőrizte.
- **Javítóréteg** (`eszkozok/normalizal.py`): mind az öt szócikken lefutott, egyiken sem
  változtatott (a fordítás már a v4 szerinti alakokat használta).
- **Kapuk:** az első futásnál két kapu hamisan riasztott (H7121: a BDB gyakorisági `_`
  jele Markdown-jelnek, a `procl.` szó `cl.` rövidítésnek látszott), ezeket a
  `forditas_kapuk.py` javította (F28.6). A H1121-nél a 3. kapu a „Tiglat-Pileszernek
  16:7” alakot rövidítésnek vette; az önújrapróba vesszővel választotta el a nevet a
  csupasz igehelytől. A végső változat mind az öt szócikken minden kapun átment.
- **Írás:** a fordítások a `naplok/EMELES_munka.tsv` munkatáblában állnak (az
  `adat/forditasok.tsv` sémájával, `allapot=opus`); az `adat/forditasok.tsv`-be a
  jóváhagyás után kerülnek, `kezi` állapottal (l. DT-F28-1 2. kérdés).

## Kapueredmények

| Strong | Szótár | Forrás kar. | Fordítás kar. | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1944 | Thayer | 337 | 339 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.01) | RENDBEN | RENDBEN | — |
| G5590 | Thayer | 5950 | 6055 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.02) | RENDBEN | RENDBEN | — |
| H6093 | BDB | 187 | 240 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.28) | RENDBEN | RENDBEN | RENDBEN |
| H7121 | BDB | 10780 | 11884 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.10) | RENDBEN | RENDBEN | RENDBEN |
| H1121 | BDB | 14948 | 15926 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.07) | RENDBEN | RENDBEN | RENDBEN |

Kapuk: 1 héber–görög token · 2 igehely-számpár · 3 Károli-rövidítés · 4 formázás/zárójel · 5 terminológia · 6 hosszarány (csak jelzés) · 8 idézőjel-párok · 9 tagolás · 10 igetörzsek (BDB).

## G1944 (Thayer, 337 → 339 karakter)

`forras_hash=f07596094b915d4d06920f0a5ba01b7f4b3331ff` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 0 forrasjelolo (forditas 0)

**1.** 

> G1944 — ἐπικατάρατος ἐπικατάρατον (ἐπικαταράομαι to imprecate curses upon), only in Biblical and ecclesiastical use, accursed, execrable, exposed to divine vengeance, lying under God's curse: Joh 7:49 R G; Gal 3:10 (Deu 27:26); Gal 3:13 (Deu 21:23); (Wis. 3:12 ( Wisdom 3:13 ); Wisdom 14:8>; 4 Macc. 2:19; in the Sept. often for אָרוּר).

G1944 — ἐπικατάρατος ἐπικατάρατον (ἐπικαταράομαι: átkot mondani valakire), csak bibliai és egyházi használatban: átkozott, utálatos, az isteni bosszúnak kitett, Isten átka alatt álló: Ján 7:49 R G; Gal 3:10 (5Móz 27:26); Gal 3:13 (5Móz 21:23); (Bölcs 3:12 (Bölcs 3:13); Bölcs 14:8; 4Makk 2:19; a Septuagintában gyakran a אָרוּר fordítása).

## G5590 (Thayer, 5950 → 6055 karakter)

`forras_hash=aaf77949eefa1168f62295aa5c357d4e9c7ddadd` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 19 forrasjelolo (forditas 24)

**1.** 

> G5590 — ψυχή ψυχῆς, ἡ (ψύχω, to breathe, blow), from Homer down, the Sept. times too many to count for נֶפֶשׁ, occasionally also for לֵב and לֵבָב;

G5590 — ψυχή ψυχῆς, ἡ (ψύχω, lélegezni, fújni), Homérosztól kezdve; a Septuagintában számtalanszor a נֶפֶשׁ fordítása, alkalmanként a לֵב és a לֵבָב szóé is.

**2.** 

> 1. breath (Latinanima), i. e. a. the breath of life; the vital force which animates the body and shows itself in breathing: Act 20:10; of animals, Rev 8:9 (Gen 9:4; Gen 35:18; ἐπιστραφήτω ψυχή τοῦ παιδαρίου, 1Ki 17:21); so also in those passages where, in accordance with the trichotomy or threefold division of human nature by the Greeks, ἡ ψυχή; is distinguished from τό πνεῦμα (see πνευαμ, 2, p. 520a (and references under the word πνεῦμα 5)), 1Th 5:23; Heb 4:12.

1. lehelet (latinul anima), azaz a. az élet lehelete; az az életerő, amely a testet élteti, és a légzésben nyilvánul meg: ApCsel 20:10; állatokról: Jel 8:9 (1Móz 9:4; 1Móz 35:18; ἐπιστραφήτω ψυχή τοῦ παιδαρίου, 1Kir 17:21). Így azokon a helyeken is, ahol – a görögöknél szokásos trichotómiának, vagyis az emberi természet hármas felosztásának megfelelően – ἡ ψυχή megkülönböztetendő τό πνεῦμα-tól (l. πνευαμ, 2, 520a. o. (és a hivatkozásokat a πνεῦμα címszónál, 5)), 1Thessz 5:23; Zsid 4:12.

**3.** 

> b. life: μέριμναν τῇ ψυχή, Mat 6:25; Luk 12:22; τήν ψυχήν ἀγαπᾶν, Rev 12:11; (μισεῖν, Luk 14:26); τιθέναι, Joh 10:11, Joh 10:15, Joh 10:17; Joh 13:37; Joh 15:13; 1Jo 3:16; παραδιδόναι, Act 15:26; διδόναι (λύτρον, which see), Mat 20:28; Mar 10:45; ζητεῖν τήν ψυχήν τίνος (see ζητέω, 1 a.), Mat 2:20; Rom 11:3; add, Mat 6:25; Mar 3:4; Luk 6:9; Luk 12:20, Luk 12:23; Act 20:24; Act 27:10, Act 27:22; Rom 16:4; 2Co 1:23; Phi 2:30; 1Th 2:8; in the pointed aphorisms of Christ, intended to fix themselves in the minds of his hearers, the phrases εὑρίσκειν, σῴζειν, ἀπολλύναι τήν ψυχήν αὐτοῦ, etc., designate as ψυχή in one of the antithetic members the life which is lived on earth, in the other, the (blessed) life in the eternal kingdom of God: Mat 10:39; Mat 16:25; Mar 8:35-37; Luk 9:24, Luk 9:56 Rec.; ; Joh 12:25; the life destined to enjoy the Messianic salvation is meant also in the following phrases ((where R. V. soul)): περιποίησις ψυχῆς, Heb 10:39; κτᾶσθαι τάς ψυχάς, Luk 21:19; ὑπέρ τῶν ψυχῶν (here A. V. (not R. V.) for you; cf.

b. élet: μέριμναν τῇ ψυχή, Mt 6:25; Luk 12:22; τήν ψυχήν ἀγαπᾶν, Jel 12:11; (μισεῖν, Luk 14:26); τιθέναι, Ján 10:11, Ján 10:15, Ján 10:17; Ján 13:37; Ján 15:13; 1Ján 3:16; παραδιδόναι, ApCsel 15:26; διδόναι (λύτρον, l. ott), Mt 20:28; Mk 10:45; ζητεῖν τήν ψυχήν τίνος (l. ζητέω, 1 a.), Mt 2:20; Róm 11:3; továbbá Mt 6:25; Mk 3:4; Luk 6:9; Luk 12:20, Luk 12:23; ApCsel 20:24; ApCsel 27:10, ApCsel 27:22; Róm 16:4; 2Kor 1:23; Fil 2:30; 1Thessz 2:8. Krisztus csattanós mondásaiban, amelyeket hallgatói emlékezetébe szánt vésni, az εὑρίσκειν, σῴζειν, ἀπολλύναι τήν ψυχήν αὐτοῦ stb. kifejezések az ellentétes tagok egyikében a földön élt életet nevezik ψυχή-nak, a másikban az Isten örök országában élt (boldog) életet: Mt 10:39; Mt 16:25; Mk 8:35-37; Luk 9:24, Luk 9:56 Rec.; Ján 12:25. A messiási üdvösség élvezetére rendelt életet értik a következő kifejezésekben is ((ahol R. V. soul)): περιποίησις ψυχῆς, Zsid 10:39; κτᾶσθαι τάς ψυχάς, Luk 21:19; ὑπέρ τῶν ψυχῶν (itt A. V. (nem R. V.) for you; vö.

**4.** 

> c. below), 2Co 12:15.

c. lent), 2Kor 12:15.

**5.** 

> c. that in which there is life; a living being: ψυχή ζῶσα, a living soul, 1Co 15:45; (Rev 16:3 R Tr marginal reading) (Gen 2:7; plural ); πᾶσα ψυχή ζωῆς, Rev 16:3 (G L T Tr text WH) (Lev 11:10); πᾶσα ψυχή, every soul, i. e. everyone, Act 2:43; Act 3:23; Rom 13:1 (so כָּל־נֶפֶשׁ, Lev 7:17 (27); ); with ἀνθρώπου added, every soul of man (אָדָם נֶפֶשׁ, Num 31:40, Num 31:46 (cf. 1 Macc. 2:38)), Rom 2:9. ψυχαί, souls (like the Latincapita) i. e. persons (in enumerations; cf. German Seelenzahl): Act 2:41; Act 7:14; Act 27:37; 1Pe 3:20 (Gen 46:15, Gen 46:18, Gen 46:22, Gen 46:26, Gen 46:27; Exo 1:5; Exo 12:4; Lev 2:1; Num 19:11, Num 19:13, Num 19:18; (Deu 10:22); the examples from Greek authors (cf. Passow, under the word, 2, vol. ii, p. 2590b) are of a different sort (yet cf. Liddell and Scott, under the word, II. 2)); ψυχαί ἀνθρώπων of slaves (A. V. souls of men (R. V. with marginal reading 'Or lives')), Rev 18:13 (so (Num 31:35); Eze 27:13; see σῶμα, 1 c. (cf. Winer's Grammar, § 22, 7 N. 3)).

c. az, amiben élet van; élőlény: ψυχή ζῶσα, élő lélek, 1Kor 15:45; (Jel 16:3 R Tr széljegyzet) (1Móz 2:7; többes szám); πᾶσα ψυχή ζωῆς, Jel 16:3 (G L T Tr szöveg WH) (3Móz 11:10); πᾶσα ψυχή, minden lélek, azaz mindenki, ApCsel 2:43; ApCsel 3:23; Róm 13:1 (így כָּל־נֶפֶשׁ, 3Móz 7:17 (27)); a ἀνθρώπου hozzátételével: minden emberi lélek (אָדָם נֶפֶשׁ, 4Móz 31:40, 4Móz 31:46 (vö. 1Makk 2:38)), Róm 2:9. ψυχαί, lelkek (mint a latin capita), azaz személyek (felsorolásokban; vö. a német Seelenzahl): ApCsel 2:41; ApCsel 7:14; ApCsel 27:37; 1Pét 3:20 (1Móz 46:15, 1Móz 46:18, 1Móz 46:22, 1Móz 46:26, 1Móz 46:27; 2Móz 1:5; 2Móz 12:4; 3Móz 2:1; 4Móz 19:11, 4Móz 19:13, 4Móz 19:18; (5Móz 10:22); a görög szerzők példái (vö. Passow, a címszónál, 2, II. köt., 2590b. o.) más jellegűek (de vö. Liddell és Scott, a címszónál, II. 2)); ψυχαί ἀνθρώπων rabszolgákról (A. V. souls of men (R. V. széljegyzetben 'Or lives')), Jel 18:13 (így (4Móz 31:35); Ez 27:13; l. σῶμα, 1 c. (vö. Winer's Grammar, 22. §, 7 N. 3)).

**6.** 

> 2. the soul (Latinanimus), a. the seat of the feelings, desires, affections, aversions (our soul, heart, etc. (R. V. almost uniformly soul); for examples from Greek writings see Passow, under the word, 2, vol. ii., p. 2589b; (Liddell and Scott, under the word, II. 3); Hebrew נֶפֶשׁ, cf. Gesenius, Thesaurus ii, p. 901 in 3): Luk 1:46; Luk 2:35; Joh 10:24 (cf. αἴρω, 1 b.); Act 14:2, Act 14:22; Act 15:24; Heb 6:19; 2Pe 2:8, 2Pe 2:14; ἡ ἐπιθυμία τῆς ψυχῆς, Rev 18:14; ἀνάπαυσιν ταῖς ψυχαῖς εὑρίσκειν, Mat 11:29; ψυχή,... ἀναπαύου, φάγε, πίε (WH brackets these three imperatives), εὐφραίνου (personification and direct address), Luk 12:19, cf. Luk 12:18 (ἡ ψυχή ἀναπαύσεται, Xenophon, Cyril 6, 2, 28; ἐυφραίνειν τήν ψυχήν, Aelian v.

2. a lélek (latinul animus), a. az érzelmek, vágyak, vonzalmak és ellenszenvek székhelye (nálunk lélek, szív stb. (R. V. szinte mindig soul); görög írásokból vett példákat l. Passow, a címszónál, 2, II. köt., 2589b. o.; (Liddell és Scott, a címszónál, II. 3); héberül נֶפֶשׁ, vö. Gesenius, Thesaurus II, 901. o., a 3. pontban): Luk 1:46; Luk 2:35; Ján 10:24 (vö. αἴρω, 1 b.); ApCsel 14:2, ApCsel 14:22; ApCsel 15:24; Zsid 6:19; 2Pét 2:8, 2Pét 2:14; ἡ ἐπιθυμία τῆς ψυχῆς, Jel 18:14; ἀνάπαυσιν ταῖς ψυχαῖς εὑρίσκειν, Mt 11:29; ψυχή,... ἀναπαύου, φάγε, πίε (WH e három felszólító alakot szögletes zárójelbe teszi), εὐφραίνου (megszemélyesítés és közvetlen megszólítás), Luk 12:19, vö. Luk 12:18 (ἡ ψυχή ἀναπαύσεται, Xenophón, Cyril 6, 2, 28; ἐυφραίνειν τήν ψυχήν, Aelianus, v.

**7.** 

> h. 1, 32); εὐδοκεῖ ἡ ψυχή μου (anthropopathically, of God), Mat 12:18; Heb 10:38; περίλυπος ἐστιν ἡ ψυχή μου, Mat 26:38; Mar 14:34; ἡ ψυχή μου τετάρακται, Joh 12:27; ταῖς ψυχαῖς ὑμῶν ἀκλυόμενοι (fainting in your souls (cf. ἐκλύω, 2 b.)), Heb 12:3; ἐν ὅλῃ τῇ ψυχή σου, with all thy soul, Mat 22:37; (Luk 10:27 L text T Tr WH); ἐξ ὅλης τῆς ψυχῆς σου (Latinex toto animo), with (literally, from (cf. ἐκ, II.

h. 1, 32); εὐδοκεῖ ἡ ψυχή μου (antropopatikusan, Istenről), Mt 12:18; Zsid 10:38; περίλυπος ἐστιν ἡ ψυχή μου, Mt 26:38; Mk 14:34; ἡ ψυχή μου τετάρακται, Ján 12:27; ταῖς ψυχαῖς ὑμῶν ἀκλυόμενοι (lelketekben elcsüggedve (vö. ἐκλύω, 2 b.)), Zsid 12:3; ἐν ὅλῃ τῇ ψυχή σου, teljes lelkedből, Mt 22:37; (Luk 10:27 L szöveg T Tr WH); ἐξ ὅλης τῆς ψυχῆς σου (latinul ex toto animo), teljes (szó szerint: -ból/-ből (vö. ἐκ, II.

**8.** 

> 12 b.)) all thy soul, Mar 12:30, Mar 12:33 (here T WH omit; L Tr marginal reading brackets the phrase); Luk 10:27 (R G) (Deu 6:5; (Epictetus diss. 3, 22, 18 (cf. Xenophon, anab. 7, 7, 43)); Antoninus 3, 4; (especially 4, 31; 12, 29); ὅλῃ τῇ ψυχή φροντίζειν τίνος (rather, with κεχαρισθαι), Xenophon, mem. 3, 11, 10); μία ψυχή, with one soul (cf. πνεῦμα, 2, p. 520a bottom), Phi 1:27; τοῦ πλήθους... ἦν ἡ καρδία καί ἡ ψυχή μία, Act 4:32 (ἐρωτηθεις τί ἐστι φίλος, ἔφη. μία ψυχή δύο σώμασιν ἐνοικουσα, (Diogenes Laërtius 5, 20 (cf. Aristotle, eth. Nic. 9, 8, 2, p. 1168b, 7; on the elliptical ἀπό μιᾶς (namely, ψυχῆς?), see ἀπό, III.)); ἐκ ψυχῆς, from the heart, heartily (Eph 6:6 (Tr WH with Eph 6:7)); Col 3:23 (ἐκ τῆς ψυχῆς often in Xenophon; τό ἐκ ψυχῆς πένθος, Josephus, Antiquities 17, 6, 5).

12 b.)) lelkedből, Mk 12:30, Mk 12:33 (itt T WH elhagyja; L Tr széljegyzet szögletes zárójelbe teszi a kifejezést); Luk 10:27 (R G) (5Móz 6:5; (Epiktétosz, diss. 3, 22, 18 (vö. Xenophón, anab. 7, 7, 43)); Antoninus 3, 4; (különösen 4, 31; 12, 29); ὅλῃ τῇ ψυχή φροντίζειν τίνος (helyesebben a κεχαρισθαι alakhoz kapcsolva), Xenophón, mem. 3, 11, 10); μία ψυχή, egy lélekkel (vö. πνεῦμα, 2, 520a. o. alul), Fil 1:27; τοῦ πλήθους... ἦν ἡ καρδία καί ἡ ψυχή μία, ApCsel 4:32 (ἐρωτηθεις τί ἐστι φίλος, ἔφη. μία ψυχή δύο σώμασιν ἐνοικουσα, (Diogenész Laertiosz 5, 20 (vö. Arisztotelész, eth. Nic. 9, 8, 2, 1168b. o., 7; az elliptikus ἀπό μιᾶς szerkezetről (ti. ψυχῆς?) l. ἀπό, III.)); ἐκ ψυχῆς, szívből, szívesen (Ef 6:6 (Tr WH az Ef 6:7 versnél)); Kol 3:23 (ἐκ τῆς ψυχῆς gyakran Xenophónnál; τό ἐκ ψυχῆς πένθος, Josephus, Antiquitates 17, 6, 5).

**9.** 

> b. "the (human) soul in so far as it is so constituted that by the right use of the aids offered it by God it can attain its highest end and secure eternal blessedness, the soul regarded as a moral being designed for everlasting life": 3Jo 1:2; ἀγρύπνειν ὑπέρ τῶν ψυχῶν, Heb 13:17; ἐπιθυμίαι, αἵτινες στρατεύονται κατά τῆς ψυχῆς, 1Pe 2:11; ἐπίσκοπος τῶν ψυχῶν, 1Pe 2:25; σῴζειν τάς ψυχάς, Jam 1:21; ψυχήν ἐκ θανάτου, from eternal death, Jam 5:20; σωτηρία ψυχῶν, 1Pe 1:9; ἁγνίζειν τάς ψυχάς ἑαυτῶν, 1Pe 1:22; (τάς ψυχάς πιστῷ κτίστῃ παρατίθεσθαι, 1Pe 4:19).

b. „az (emberi) lélek, amennyiben úgy van megalkotva, hogy az Istentől felkínált segítségek helyes használatával elérheti legfőbb célját, és elnyerheti az örök boldogságot; a lélek mint erkölcsi lény, amely örök életre rendeltetett”: 3Ján 1:2; ἀγρύπνειν ὑπέρ τῶν ψυχῶν, Zsid 13:17; ἐπιθυμίαι, αἵτινες στρατεύονται κατά τῆς ψυχῆς, 1Pét 2:11; ἐπίσκοπος τῶν ψυχῶν, 1Pét 2:25; σῴζειν τάς ψυχάς, Jak 1:21; ψυχήν ἐκ θανάτου, az örök haláltól, Jak 5:20; σωτηρία ψυχῶν, 1Pét 1:9; ἁγνίζειν τάς ψυχάς ἑαυτῶν, 1Pét 1:22; (τάς ψυχάς πιστῷ κτίστῃ παρατίθεσθαι, 1Pét 4:19).

**10.** 

> c. the soul as an essence which differs from the body and is not dissolved by death (distinguished from τό σῶμα, as the other part of human nature (so in Greek writings from Isocrates and Xenophon down; cf. examples in Passow, under the word, p. 2589{a} bottom; Liddell and Scott, under the word, II. 2)): Mat 10:28, cf. 4 Macc. 13:14 (it is called ἀθάνατος, Herodotus 2, 123; Plato Phaedr., p. 245 c., 246 a., others; ἄφθαρτος, Josephus, b. j. 2, 8, 14; διαλυθῆναι τήν ψυχήν ἀπό τοῦ σώματος, Epictetus diss. 3, 10, 14); the soul freed from the body, a disembodied soul, Act 2:27, Act 2:31 Rec.; Rev 6:9; Rev 20:4 (Wis. 3:1; (on the Homeric use of the word, see Ebeling, Lex. Homer, under the word, 3, and references at the end, also Proudfit in Bib. Sacr. for 1858, pp. 753-805)).

c. a lélek mint olyan lényeg, amely különbözik a testtől, és a halállal nem bomlik fel (megkülönböztetve τό σῶμα-tól, mint az emberi természet másik részétől (így a görög írásokban Iszokratésztől és Xenophóntól kezdve; vö. a példákat: Passow, a címszónál, 2589{a}. o. alul; Liddell és Scott, a címszónál, II. 2)): Mt 10:28, vö. 4Makk 13:14 (ἀθάνατος-nak nevezik, Hérodotosz 2, 123; Platón, Phaedr., 245 c., 246 a. o. és mások; ἄφθαρτος, Josephus, b. j. 2, 8, 14; διαλυθῆναι τήν ψυχήν ἀπό τοῦ σώματος, Epiktétosz, diss. 3, 10, 14); a testtől megszabadult lélek, testetlen lélek: ApCsel 2:27, ApCsel 2:31 Rec.; Jel 6:9; Jel 20:4 (Bölcs 3:1; (a szó homéroszi használatáról l. Ebeling, Lex. Homer, a címszónál, 3, és a végén levő hivatkozásokat; továbbá Proudfit, Bib. Sacr., 1858, 753–805. o.)).

## H6093 (BDB, 187 → 240 karakter)

`forras_hash=62bd18a2a251b2578c43e8adbd1b9338700c28f4` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 0 forrasjelolo (forditas 0)

Törzskapu: RENDBEN · 

**1.** 

> H6093. itstsabon עִצָּבוֺן noun [masculine] pain, toil; — ׳ע absolute Gen 3:17 toil; construct יָדֵינוּ עִצְּבוֺן 5:29 (both of agriculture); suffix עִצְּבוֺנֵךְ 3:16 (of travail; all J).

H6093. itstsabon עִצָּבוֺן főnév [hímnemű]: fájdalom, fáradság; — ׳ע status absolutus 1Móz 3:17 fáradság; status constructus יָדֵינוּ עִצְּבוֺן 5:29 (mindkettő a földművelésről); suffixummal עִצְּבוֺנֵךְ 3:16 (a szülés fájdalmáról; mind J).

## H7121 (BDB, 10780 → 11884 karakter)

`forras_hash=7b02618a3285ace6b36965f7d449c9a623175805` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 56 forrasjelolo (forditas 67)

Törzskapu: RENDBEN · Qal Qal Pu Niph Qal Qal Qal Qal Pu Qal Qal

**1.** 

> H7121. qara I. קָרָא_724 verb call, proclaim, read (Late Hebrew id., read aloud, read; Phoenician קרא call; Arabic read aloud, recite (the '†or°¹n), the †or°a¹n; Aramaic קְלרא, call, etc., so Old Aramaic קרא, Nabatean id., Palmyrene id., קרה); — Qal_655 Perfect ׳ק Gen 11:9 +, 3 feminine singular consecutive וְקָרָזת Isa 7:14 (Ges^§ 74g); 2 masculine singular קָרָאתָ Judg 12:1 +, etc.; Imperfect3masculine singular יִקְרָא Gen 2:19 +; suffix יִקְרְאוֺ Jer 23:6, אֵהוּ- Isa 41:2; +; 1singular אֶקְרָא Deut 32:3 +, וָאֶקְרָאֶר 1Sam 28:15 (Ges^§ 48d Nes^Marg. 15); 3 feminine plural וַתִּקְרֶאנָה Ruth 4:17 (twice in verse), וַתִּקְרֶאןָ Num 25:2; 2feminine plural תִּקְרֶאנָה Ruth 1:20-21, etc.; Imperative masculine singular קְרָא Judg 7:3 +, suffix קְרָאֵנִי Psa 50:15, etc.; Infinitive construct קְרָא 1Sam 3:6 +, קְראֹות (Baer אֹת-) Judg 8:1 (Ges^§ 74h); suffix קָרְאִי Psa 4:2 +, etc.; Participle active קוֺרֵא Amos 5:8 +, קֹרֵא Jer 1:15 +; plural קֹרִאים Psa 99:6 (Ges^§§ 74i; 75oo); passive קָרוּא Est 5:12; plural קְרוּאִים 1Sam 9:22; Ezek 23:23, קְרֻאִים 1Sam 9:13 +; construct קְרוּאֵי Num 1:16 Qr (Kt קריאי), 26:9 Kt (Qr קְרִיאֵי, see קָרִיא); —

H7121. qara I. קָרָא_724 ige: hívni, kihirdetni, olvasni (késői héber ua., felolvasni, olvasni; föníciai קרא hívni; arab felolvasni, recitálni (a '†or°¹n), a †or°a¹n; arámi קְלרא, hívni stb., így óarámi קרא, nabateus ua., palmürai ua., קרה); — Qal_655 perfectum ׳ק 1Móz 11:9 és máshol, 3. nőnemű egyes szám consecutivummal וְקָרָזת Ézs 7:14 (Ges^§ 74g); 2. hímnemű egyes szám קָרָאתָ Bír 12:1 és máshol, stb.; imperfectum 3. hímnemű egyes szám יִקְרָא 1Móz 2:19 és máshol; suffixummal יִקְרְאוֺ Jer 23:6, אֵהוּ- Ézs 41:2; és máshol; 1. egyes szám אֶקְרָא 5Móz 32:3 és máshol, וָאֶקְרָאֶר 1Sám 28:15 (Ges^§ 48d Nes^Marg. 15); 3. nőnemű többes szám וַתִּקְרֶאנָה Ruth 4:17 (a versben kétszer), וַתִּקְרֶאןָ 4Móz 25:2; 2. nőnemű többes szám תִּקְרֶאנָה Ruth 1:20-21 stb.; imperativus hímnemű egyes szám קְרָא Bír 7:3 és máshol, suffixummal קְרָאֵנִי Zsolt 50:15 stb.; infinitivus constructus קְרָא 1Sám 3:6 és máshol, קְראֹות (Baer אֹת-) Bír 8:1 (Ges^§ 74h); suffixummal קָרְאִי Zsolt 4:2 és máshol, stb.; aktív participium קוֺרֵא Ámós 5:8 és máshol, קֹרֵא Jer 1:15 és máshol; többes szám קֹרִאים Zsolt 99:6 (Ges^§§ 74i; 75oo); passzív קָרוּא Eszt 5:12; többes szám קְרוּאִים 1Sám 9:22; Ez 23:23, קְרֻאִים 1Sám 9:13 és máshol; status constructus קְרוּאֵי 4Móz 1:16 Qr (Kt קריאי), 26:9 Kt (Qr קְרִיאֵי, l. קָרִיא); —

**2.** 

> 1.

1.

**3.** 

> a. call, cry, utter a loud sound, Judg 9:7; 2Sam 18:25 (in 18:28 read וַיִּקְרַב We, confirmed by ᵐ5^L so Dr and all recent Comm.), Jer 4:6; Dan 8:16 (all + אמר), 2Kin 7:11 (on text see Kit Benz), Isa 6:4; for help Gen 39:15, 18 (J); of pleading in court Isa 59:4 (ב of manner); explicitly גְּדוֺל בְּקוֺל Gen 39:14 (J), 1Kin 18:27-28, 2Kin 18:28 = Isa 36:13 2Chr 32:18, גָּדוֺל קוֺל Ezek 9:1 (+ בְּאָצְנֵי); with אַחֲרֵי person 1Sam 20:37 (+ אָמַר), 24:8 (Gi; v.24:9 van d. H. Baer; + לֵאמֹר), Jer 12:6.

a. hívni, kiáltani, hangos hangot hallatni: Bír 9:7; 2Sám 18:25 (a 18:28-ban olv. וַיִּקְרַב We, megerősíti ᵐ5^L, így Dr és minden újabb Comm.), Jer 4:6; Dán 8:16 (mind + אמר), 2Kir 7:11 (a szövegről l. Kit Benz), Ézs 6:4; segítségért 1Móz 39:15, 18 (J); a bíróság előtti perlésről Ézs 59:4 (ב a módé); kifejezetten גְּדוֺל בְּקוֺל 1Móz 39:14 (J), 1Kir 18:27-28, 2Kir 18:28 = Ézs 36:13 2Krón 32:18, גָּדוֺל קוֺל Ez 9:1 (+ בְּאָצְנֵי); אַחֲרֵי + személy: 1Sám 20:37 (+ אָמַר), 24:8 (Gi; v.24:9 van d. H. Baer; + לֵאמֹר), Jer 12:6.

**4.** 

> b. call cry, object in oratio recta [direct speech] Judg 7:20; 1Sam 3:4 (read שְׁמוּאֵל שְׁמוּאֵל; ᵐ5 Th We Dr Kit Bu HPS), 3:6 (compare ᵐ5), 3:8 (against accents), 3:10 (see שְׁמוּאֵל), 20:38; 2Sam 20:16; 2Kin 11:14; Jer 20:8; Lev 13:45; = utter, speak Jer 36:18; of command Gen 45:1 (E).

b. hívni, kiáltani, a tárgy oratio recta [egyenes beszéd]: Bír 7:20; 1Sám 3:4 (olv. שְׁמוּאֵל שְׁמוּאֵל; ᵐ5 Th We Dr Kit Bu HPS), 3:6 (vö. ᵐ5), 3:8 (a hangsúlyjelek ellenére), 3:10 (l. שְׁמוּאֵל), 20:38; 2Sám 20:16; 2Kir 11:14; Jer 20:8; 3Móz 13:45; = kimondani, mondani Jer 36:18; parancsról 1Móz 45:1 (E).

**5.** 

> 2.

2.

**6.** 

> a. call unto some one: אֶל person (often + אָמַר; sometimes with מִן local), Gen 3:9; 19:5; Exod 3:4; Isa 6:3 + often; with עַל (for אֶל) of satyrs 34:14 (so Vrss Ges Che^Comm. and others > recent Comm. from II. קָרָא or קָרָה which (in Qal) always take accusative); unto ׳י (אֶלׅ (God), in praise Psa 66:17; 1Chr 4:10, usually for help, Judg 15:18; 1Sam 12:17-18, Hosea 7:7 + 3:5; 4:4 +, + עַל person against Deut 15:9; 24:15; to ׳י (לׅ (God) Job 14:14; Psa 57:3; 141:1; to (ל) a servant (for service) 2Kin 4:36; Job 19:16, so (אֶל) 2Sam 1:15; call to (ל) one Jer 3:4 (+ oratio recta [direct speech]), Lam 4:15 (id.), Prov 2:3 (לְבִינָה); subject ׳י Micah 6:9; Jer 35:17.

a. hívni valakit: אֶל + személy (gyakran + אָמַר; néha מִן helyhatározóval), 1Móz 3:9; 19:5; 2Móz 3:4; Ézs 6:3 + gyakran; עַל elöljáróval (אֶל helyett) a szatírokról 34:14 (így Vrss Ges Che^Comm. és mások > az újabb Comm. a II. קָרָא vagy קָרָה igéből, amelyek (Qal-ban) mindig tárgyesetet vonzanak); ׳י-hoz (אֶלׅ (Isten), dicséretben Zsolt 66:17; 1Krón 4:10, rendszerint segítségért, Bír 15:18; 1Sám 12:17-18, Hós 7:7 + 3:5; 4:4 és máshol, + עַל + személy: valaki ellen 5Móz 15:9; 24:15; ׳י-hoz (לׅ (Isten) Jób 14:14; Zsolt 57:3; 141:1; (ל) szolgához (szolgálatra) 2Kir 4:36; Jób 19:16, így (אֶל) 2Sám 1:15; (ל) valakihez kiáltani Jer 3:4 (+ oratio recta [egyenes beszéd]), Sir 4:15 (ua.), Péld 2:3 (לְבִינָה); alanya ׳י Mik 6:9; Jer 35:17.

**7.** 

> b. cry for help, absolute, (in poetry and late) Zech 7:13; Isa 58:9; 65:24; Job 5:1; 9:16; Prov 21:13; Psa 4:2; Psalm 20:10 10t. Psalms (147:9 of young ravens); בֵּאָזְנֵי Ezek 8:18.

b. segítségért kiáltani, abszolút használatban (költészetben és későn) Zak 7:13; Ézs 58:9; 65:24; Jób 5:1; 9:16; Péld 21:13; Zsolt 4:2; Zsolt 20:10, a Zsoltárok könyvében összesen 10-szer (147:9 a fiatal hollókról); בֵּאָזְנֵי Ez 8:18.

**8.** 

> c. ׳ק י ׳בְּשֵׁם call with name of ׳י (i.e. use it in invocation): Gen 4:26; 12:8; 2Kin 5:11; Jer 10:25 = Psa 79:6 16t. (1Kin 18:24 of specific appeal to ׳י to display his power), + Isa 65:1 (see Pu`al); with name of Baal 1Kin 18:24-25, 26.

c. ׳ק י ׳בְּשֵׁם hívni ׳י nevével (azaz használni azt a segítségül hívásban): 1Móz 4:26; 12:8; 2Kir 5:11; Jer 10:25 = Zsolt 79:6, összesen 16-szor (1Kir 18:24 annak konkrét kérésére, hogy ׳י mutassa meg hatalmát), továbbá Ézs 65:1 (l. Pu`al); Baál nevével 1Kir 18:24-25, 26.

**9.** 

> d. late, with accusative dei Isa 43:22; Psa 14:4 4t. Psalms; absolute 116:2.

d. későn, accusativus dei-vel Ézs 43:22; Zsolt 14:4, a Zsoltárok könyvében összesen 4-szer; abszolút használatban 116:2.

**10.** 

> 3 proclaim:

3 kihirdetni:

**11.** 

> a. with accusative of thing procl. Amos 4:5; Gen 41:43; Deut 15:2; Jer 31:6; Lev 25:10 +; ׳ק צוֺם proclaim a fast 1Kin 21:9, 12; Jer 36:9 +, ׳ק י ׳מוֺעֲדֵי Lev 23:2, 4; ׳ק followed by oratio recta [direct speech] Exod 34:6, etc.; followed by ל person Jer 34:8, 15, 17 (twice in verse); Isa 61:1, עַל person (against, concerning) 1Kin 13:4, 32; Jer 49:29; Lam 1:15; proclaim peace to (ל person) Judg 21:13; compare ׳ק לְשָׁלוֺם אֵלֶיהָ Deut 20:10; ׳ק with accusative of congnate meaning with verb מִקְרָא Isa 1:13, הַקְּרִיאָה Jonah 3:2 (+ אֶל).

a. a kihirdetett dolog tárgyesetével: Ámós 4:5; 1Móz 41:43; 5Móz 15:2; Jer 31:6; 3Móz 25:10 és máshol; ׳ק צוֺם böjtöt hirdetni 1Kir 21:9, 12; Jer 36:9 és máshol, ׳ק י ׳מוֺעֲדֵי 3Móz 23:2, 4; ׳ק, utána oratio recta [egyenes beszéd]: 2Móz 34:6 stb.; utána ל + személy: Jer 34:8, 15, 17 (a versben kétszer); Ézs 61:1, עַל + személy (ellen, felől) 1Kir 13:4, 32; Jer 49:29; Sir 1:15; békességet hirdetni valakinek (ל + személy) Bír 21:13; vö. ׳ק לְשָׁלוֺם אֵלֶיהָ 5Móz 20:10; ׳ק az igével rokon jelentésű tárgyesettel: מִקְרָא Ézs 1:13, הַקְּרִיאָה Jón 3:2 (+ אֶל).

**12.** 

> b. ׳ק י ׳שֵׁם Deut 32:3; Psa 99:6; so (earlier) ׳ק י ׳בְשֵׁם Exod 33:19; 34:5 (JE); compare ׳ק יַעֲקֹב בְּשֵׁם Isa 44:5 (but read יִקָּרֵא, Lo Che and most).

b. ׳ק י ׳שֵׁם 5Móz 32:3; Zsolt 99:6; így (korábban) ׳ק י ׳בְשֵׁם 2Móz 33:19; 34:5 (JE); vö. ׳ק יַעֲקֹב בְּשֵׁם Ézs 44:5 (de olv. יִקָּרֵא, Lo Che és a legtöbben).

**13.** 

> c. ׳ק עֲלֵי׳בֵּשׁ Psa 49:12 proclaim (with) name over landed estates, claim possession (Hup Bae); proclaim one's own name Ruth 4:11 = become famous; passive participle proclaimed, i.e. renowned Ezek 23:23.

c. ׳ק עֲלֵי׳בֵּשׁ Zsolt 49:12: a földbirtokok fölött kihirdetni (vele) a nevet, birtokot igényelni (Hup Bae); a saját nevét hirdetni Ruth 4:11 = híressé lenni; a passzív participium: kihirdetett, azaz híres Ez 23:23.

**14.** 

> d. absolute make proclamation (sometimes + לֵאמֹר אָמַר,) Judg 7:3; Jer 2:2 (בְּאָוְנֵי) Zech 1:14, 17; Jonah 3:4; Isa 40:3, 6 +, with עַל concerning Neh 6:7, against 1Kin 13:2; Jonah 1:3.

d. abszolút használatban kihirdetést tenni (néha + לֵאמֹר אָמַר,) Bír 7:3; Jer 2:2 (בְּאָוְנֵי) Zak 1:14, 17; Jón 3:4; Ézs 40:3, 6 és máshol, עַל elöljáróval: valamiről Neh 6:7, valami ellen 1Kir 13:2; Jón 1:3.

**15.** 

> 4.

4.

**16.** 

> a. read aloud, often בְּאָוְבֵי, less often לפְנֵי, with ב of roll, book Jer 36:6, 8, 14; Neh 8:3, 8; 9:3; 2Chr 34:18, + accusative of words Jer 36:8, 10; object omitted Exod 24:7 (E) Jer 36:15; with acc of roll, book 36:15; 36:21; 51:63; 2Kin 22:10; 2Chr 34:24, of letter (סֵפֶר), writing 2Kin 5:7; Isa 29:11-12, Jer 29:29, columns of manuscript 36:23; with accusative of words Josh 8:34-35, Jer 36:6; 51:61; 2Kin 23:2 2Chr 34:30, compare Deut 31:11.

a. felolvasni, gyakran בְּאָוְבֵי, ritkábban לפְנֵי, a tekercset, könyvet jelölő ב elöljáróval Jer 36:6, 8, 14; Neh 8:3, 8; 9:3; 2Krón 34:18, + a szavak tárgyesetével Jer 36:8, 10; a tárgy elmarad 2Móz 24:7 (E) Jer 36:15; a tekercs, könyv tárgyesetével 36:15; 36:21; 51:63; 2Kir 22:10; 2Krón 34:24, levélével (סֵפֶר), írásével 2Kir 5:7; Ézs 29:11-12, Jer 29:29, a kézirat hasábjaiéval 36:23; a szavak tárgyesetével Józs 8:34-35, Jer 36:6; 51:61; 2Kir 23:2 2Krón 34:30, vö. 5Móz 31:11.

**17.** 

> b. read, to oneself, in (ב) a roll, book, Deut 17:19; Neh 8:18, so of vision written on tablets Hab 2:2; with accusative of letter (סֵפֶר) 2Kin 19:14 = Isa 37:14, book 2Kin 22:8; absolute Isa 34:16.

b. olvasni, magában, (ב) tekercsben, könyvben, 5Móz 17:19; Neh 8:18, így táblákra írt látomásról Hab 2:2; a levél (סֵפֶר) tárgyesetével 2Kir 19:14 = Ézs 37:14, a könyvével 2Kir 22:8; abszolút használatban Ézs 34:16.

**18.** 

> c. read, for hear read, 2Kin 22:16.

c. olvasni, felolvasást hallgatni értelemben, 2Kir 22:16.

**19.** 

> 5 summon: usually a. with ל person: Gen 12:18; 20:8-9, Num 22:5, 20, 37; Judg 8:1; 1Sam 3:5-6, 8 (twice in verse) + often (c. 100 t.), + ל reflexive 1Kin 1:28, 32, + אֶל location Exod 19:20, + אֶל person 2Sam 9:2, + infinitive purpose Josh 24:9; Judg 12:1; 14:16; 1Sam 28:15, + מִן local Hosea 11:1; Judg 4:6; + בִּשְׁמֶ֑ךָ Isa 45:4 summon by thy name; specifically summon = invite (especially to feast) Exod 34:15; Judg 14:15 ( + infinitive purpose) 1Sam 16:3 ( + בַּזָּבַ֑ח, read probably ׳לַזּ see HPS), 16:5 ( + ׳לַזּ), 1 Kings 19:26 + (c. 17 t.).

5 megidézni: rendszerint a. ל + személy: 1Móz 12:18; 20:8-9, 4Móz 22:5, 20, 37; Bír 8:1; 1Sám 3:5-6, 8 (a versben kétszer) + gyakran (kb. 100-szor), + visszaható ל 1Kir 1:28, 32, + אֶל + hely 2Móz 19:20, + אֶל + személy 2Sám 9:2, + célhatározói infinitivus Józs 24:9; Bír 12:1; 14:16; 1Sám 28:15, + מִן helyhatározóval Hós 11:1; Bír 4:6; + בִּשְׁמֶ֑ךָ Ézs 45:4: neveden szólítani; különösen megidézni = meghívni (főként lakomára) 2Móz 34:15; Bír 14:15 ( + célhatározói infinitivus) 1Sám 16:3 ( + בַּזָּבַ֑ח, olv. valószínűleg ׳לַזּ, l. HPS), 16:5 ( + ׳לַזּ), 1Kir 19:26 és máshol (kb. 17-szer).

**20.** 

> b. with אֶל person Exod 10:24; Josh 4:4; 10:24; 1Kin 13:21 + (c. 20 t.); אֶל person + ל person (different persons in same relation) Exod 8:21; Jer 42:8; = call for (demand to see), with אֶל person 2Kin 18:18; with ל of thing = demand, require Prov 18:6; compare 27:16 (probably corrupt, see Toy).

b. אֶל + személy 2Móz 10:24; Józs 4:4; 10:24; 1Kir 13:21 és máshol (kb. 20-szor); אֶל + személy + ל + személy (különböző személyek azonos viszonyban) 2Móz 8:21; Jer 42:8; = hívatni (látni kívánni), אֶל + személy 2Kir 18:18; a dolgot jelölő ל elöljáróval = követelni, igényelni Péld 18:6; vö. 27:16 (valószínűleg romlott, l. Toy).

**21.** 

> c. with accusative of person Gen 41:8, 14; Exod 2:7 ( + ל person), 2:7; Amos 5:16 ( + אֶל of thing), Isa 13:3 (ל of thing), 1Sam 3:16; 22:11 + (c. 33 t.), insert וַיַקְרָא in this sense also 2Sam 15:12 ᵐ5^L We Dr and most; + infinitive purpose Num 24:10, ׳ק עַיִט מִמִּוְרָח Isa 46:11; in weakened sense (to bring response, or bring person near) Song 5:6; specifically invite, 1Sam 9:24 (but corrupt, see especially HPS), 1Kin 1:9 (also + ל, MT), 1:10; 12:20 (+ אֶל location), Deut 33:19 (accusative of location); לָהּ קָרוּא אֲנִי Est 5:12, passive participle elsewhere plural, invited ones, guests 1Sam 9:13, 22; 2Sam 15:11; 1Kin 1:41, 49; Zeph 1:7; Prov 9:18; invite or summon (accusative of person) for help, succour, Hosea 7:11; usually object ׳י (in poetry and late) Jer 29:12; 2Sam 22:4, 7 = Psa 18:4; 18:7; Isa 55:6; Lam 3:57; Job 27:10; Psa 50:15; 86:5 8t. Psalms, accusative י ׳שֵׁם Lam 3:55; accusative חכמה Prov 1:28.

c. a személy tárgyesetével 1Móz 41:8, 14; 2Móz 2:7 ( + ל + személy), 2:7; Ámós 5:16 ( + a dolgot jelölő אֶל), Ézs 13:3 (a dolgot jelölő ל), 1Sám 3:16; 22:11 és máshol (kb. 33-szor); ebben az értelemben toldandó be a וַיַקְרָא a 2Sám 15:12-ben is ᵐ5^L We Dr és a legtöbbek szerint; + célhatározói infinitivus 4Móz 24:10, ׳ק עַיִט מִמִּוְרָח Ézs 46:11; gyengült értelemben (választ kiváltani, vagy személyt közel hozni) Én 5:6; különösen meghívni, 1Sám 9:24 (de romlott, l. különösen HPS), 1Kir 1:9 (+ ל is, MT), 1:10; 12:20 (+ אֶל + hely), 5Móz 33:19 (a hely tárgyesetével); לָהּ קָרוּא אֲנִי Eszt 5:12, a passzív participium másutt többes számban: meghívottak, vendégek 1Sám 9:13, 22; 2Sám 15:11; 1Kir 1:41, 49; Sof 1:7; Péld 9:18; segítségül, támogatásra meghívni vagy hívni (a személy tárgyesetével) Hós 7:11; rendszerint ׳י a tárgy (költészetben és későn) Jer 29:12; 2Sám 22:4, 7 = Zsolt 18:4; 18:7; Ézs 55:6; Sir 3:57; Jób 27:10; Zsolt 50:15; 86:5, a Zsoltárok könyvében összesen 8-szor, tárgyesetben י ׳שֵׁם Sir 3:55; tárgyesetben חכמה Péld 1:28.

**22.** 

> d. absolute call, summon Amos 7:4 (+ ל of thing), Isa 22:12 (id.), 1Sam 3:5-6, Zech 7:13; ׳י (God) Isa 52:2; 65:12; 66:4; Job 13:22; 14:15, הָעֵדָה קְרוּאֵי Num 1:17 Qr (Kt קְרִיאֵי), 26:9 Kt (Qr קְרִיאֵי!)

d. abszolút használatban hívni, megidézni Ámós 7:4 (+ a dolgot jelölő ל), Ézs 22:12 (ua.), 1Sám 3:5-6, Zak 7:13; ׳י (Isten) Ézs 52:2; 65:12; 66:4; Jób 13:22; 14:15, הָעֵדָה קְרוּאֵי 4Móz 1:17 Qr (Kt קְרִיאֵי), 26:9 Kt (Qr קְרִיאֵי!)

**23.** 

> e. call and commission, appoint, accusative of person, Isa 48:15; 49:1, + בְּשֵׁם by name, specifically, Exod 31:2; 35:30; Isa 43:1; 45:3.

e. elhívni és megbízni, kinevezni, a személy tárgyesetével, Ézs 48:15; 49:1, + בְּשֵׁם név szerint, kifejezetten, 2Móz 31:2; 35:30; Ézs 43:1; 45:3.

**24.** 

> f. call and endow (with privilege) Isa 51:2; 54:5; 55:5.

f. elhívni és felruházni (kiváltsággal) Ézs 51:2; 54:5; 55:5.

**25.** 

> 6 call=name:

6 hívni = nevezni:

**26.** 

> a. (early and most common usage), call one's name (שֵׁם) so and so, 2 accusative: of person Gen 3:20; 4:25-26, 5:2-3, 29; 34t. Genesis; Exod 2:10, 22; Hosea 1:4, 6, 9; Isa 7:14; 8:3; 9:5 10t. (Jer 46:17 read ᵐ5 שֵׁם קִרְאוּ Gie and others); of places, etc., Gen 4:17; 11:9 17t. Genesis; Judg 1:17, 26; 2:5; 15:19; 18:29 21t.

a. (korai és leggyakoribb használat) valakinek a nevét (שֵׁם) így és így nevezni, két tárgyesettel: személyről 1Móz 3:20; 4:25-26, 5:2-3, 29; Mózes első könyvében összesen 34-szer; 2Móz 2:10, 22; Hós 1:4, 6, 9; Ézs 7:14; 8:3; 9:5, összesen 10-szer (Jer 46:17 olv. ᵐ5 שֵׁם קִרְאוּ Gie és mások); helyekről stb. 1Móz 4:17; 11:9, Mózes első könyvében összesen 17-szer; Bír 1:17, 26; 2:5; 15:19; 18:29, összesen 21-szer.

**27.** 

> b. with accusative of appellation ony, Ezek 39:11.

b. csak a megnevezés tárgyesetével, Ez 39:11.

**28.** 

> c. accusative of person or location + accusative appellative Hosea 2:18; Deut 3:14; Jer 23:6; Isa 58:5; Num 32:41.

c. a személy vagy a hely tárgyesete + megnevező tárgyeset Hós 2:18; 5Móz 3:14; Jer 23:6; Ézs 58:5; 4Móz 32:41.

**29.** 

> d. accusative of person + clause Psa 89:27.

d. a személy tárgyesete + mellékmondat Zsolt 89:27.

**30.** 

> e. = give name to, accusative appellation + ל person (location, or thing):

e. = nevet adni valaminek: a megnevezés tárgyesete + ל + személy (hely vagy dolog):

**31.** 

> (1) person Hosea 2:18; Gen 35:18; 1Sam 4:21; Jer 3:19; 30:17; 33:16 9t.;

(1) személy Hós 2:18; 1Móz 35:18; 1Sám 4:21; Jer 3:19; 30:17; 33:16, összesen 9-szer;

**32.** 

> (2) location, or thing, Judg 18:12; 2Sam 2:16; 5:9; 6:8; Josh 22:34 (name lost, ᵑ6 Hebrew Manuscripts Ins. עֵד; compare Di Steuern), Gen 1:5 (twice in verse); 1:8; 2:19 (twice in verse); Exod 33:7 30t. + Job 17:14 (ל + sentence including name).

(2) hely vagy dolog, Bír 18:12; 2Sám 2:16; 5:9; 6:8; Józs 22:34 (a név elveszett, ᵑ6 héber kéziratok betoldják: עֵד; vö. Di Steuern), 1Móz 1:5 (a versben kétszer); 1:8; 2:19 (a versben kétszer); 2Móz 33:7, összesen 30-szor + Jób 17:14 (ל + a nevet tartalmazó mondat).

**33.** 

> f. with בְּשֵׁם + ל Isa 40:26, compare 65:11 (אַחֵר שֵׁם), Psa 147:4 (שֵׁמוֺת), Ruth 4:17 (שֵׁם + לֵאמֹר), Gen 2:20; 26:18 (twice in verse) (all with שֵׁם).

f. בְּשֵׁם + ל szerkezettel Ézs 40:26, vö. 65:11 (אַחֵר שֵׁם), Zsolt 147:4 (שֵׁמוֺת), Ruth 4:17 (שֵׁם + לֵאמֹר), 1Móz 2:20; 26:18 (a versben kétszer) (mind שֵׁם szóval).

**34.** 

> g. with ל of thing + עַלאשֵׁם 2Sam 18:16.

g. a dolgot jelölő ל + עַלאשֵׁם szerkezettel 2Sám 18:16.

**35.** 

> h. call by ב names the names (accusative) of cities Num 32:38; call to (ב) city, + appelll., + בִּשְׁמוֺ v 42.

h. ב elöljáróval nevekkel nevezni: a városok neveit (tárgyeset) 4Móz 32:38; (ב) várost elnevezni, + megnev., + בִּשְׁמוֺ v 42.

**36.** 

> i. call cities (accusative) בְּשֵׁם, i.e, specify them, Josh 21:9; 1Chr 6:50 (בְּשֵׁמוֺת). Niph`al Perfect3masculine singular נִקְרָא Jer 4:20 +, 1 singular נִקְרֵאתִי Est 4:11, etc.; Imperfect3masculine singular יִקָּרֵא Gen 2:23 +, וַיִּקָּרֵא Ezek 20:29 +, etc.; Participle נִקְרָא Isa 43:7; Jer 44:26; plural נִקְרָאִים Isa 48:1; Est 6:1; —

i. városokat (tárgyeset) בְּשֵׁם nevezni, azaz megnevezni őket, Józs 21:9; 1Krón 6:50 (בְּשֵׁמוֺת). Niph`al perfectum 3. hímnemű egyes szám נִקְרָא Jer 4:20 és máshol, 1. egyes szám נִקְרֵאתִי Eszt 4:11 stb.; imperfectum 3. hímnemű egyes szám יִקָּרֵא 1Móz 2:23 és máshol, וַיִּקָּרֵא Ez 20:29 és máshol, stb.; participium נִקְרָא Ézs 43:7; Jer 44:26; többes szám נִקְרָאִים Ézs 48:1; Eszt 6:1; —

**37.** 

> 1 reflexive, נִק הַקֹּדֶשׁ ׳מֵעִיר Isa 48:2 from the holy city they call themselves.

1 visszaható, נִק הַקֹּדֶשׁ ׳מֵעִיר Ézs 48:2: a szent városról nevezik magukat.

**38.** 

> 2 passive be called:

2 szenvedő: hívatni, neveztetni:

**39.** 

> a. be proclaimed (compare Qal 3), of י ׳שֵׁם Jer 44:26 (בְּפֶה instrumental); of man's name = be famous Ruth 4:14; = be announced Jer 4:20.

a. kihirdettetni (vö. Qal 3), י ׳שֵׁם-ról Jer 44:26 (בְּפֶה eszközhatározó); az ember nevéről = híresnek lenni Ruth 4:14; = bejelentetni Jer 4:20.

**40.** 

> b. be read aloud compare Qal 4): impersonal with ב of book, + בְּאָוְנֵי Neh 13:1; subject records Est 6:1 (לפְנֵי).

b. felolvastatni vö. Qal 4): személytelenül, a könyvet jelölő ב elöljáróval, + בְּאָוְנֵי Neh 13:1; alanya a feljegyzések Eszt 6:1 (לפְנֵי).

**41.** 

> c. be summoned (compare Qal 5: Isa 31:4 (עַל against); Est 3:12; 4:11 (twice in verse); verse); 8: 9; + בְּשֵׁם, i.e. specifically, 2:14, d. be named (compare Qal 6.):

c. megidéztetni (vö. Qal 5: Ézs 31:4 (עַל ellen); Eszt 3:12; 4:11 (a versben kétszer); vers); 8: 9; + בְּשֵׁם, azaz kifejezetten, 2:14, d. neveztetni (vö. Qal 6.):

**42.** 

> (I) appell. subject + ל person Gen 2:23 to her shall be called 'woman', 1Sam 9:9; Isa 32:5; 62:4, 12; Prov 16:21; + ל location 2Sam 18:18; Isa 1:26; 35:8; Jer 19:6.

(I) megnev. alany + ל + személy 1Móz 2:23: 'asszonynak' hívják őt, 1Sám 9:9; Ézs 32:5; 62:4, 12; Péld 16:21; + ל + hely 2Sám 18:18; Ézs 1:26; 35:8; Jer 19:6.

**43.** 

> (2) ונו שְׁמוֺ ׳וְנִקְרָא Deut 25:10, so Gen 35:10; Dan 10:1; Ezek 20:29 (of place); אֶתשִֿׁמְךָ 20:29.

(2) ונו שְׁמוֺ ׳וְנִקְרָא 5Móz 25:10, így 1Móz 35:10; Dán 10:1; Ez 20:29 (helyről); אֶתשִֿׁמְךָ 20:29.

**44.** 

> (3) יְרוּשׁ ׳וְנִקְרְאָה ׳וגו Zech 8:3, so land Deut 3:18, temple Isa 56:7.

(3) יְרוּשׁ ׳וְנִקְרְאָה ׳וגו Zak 8:3, így országról 5Móz 3:18, templomról Ézs 56:7.

**45.** 

> (4) especially י שֵׁם ׳נִקְרָא עַל, denoting ownership, of person Jer 15:16, people Deut 28:10; Jer 14:9; Amos 9:12; Isa 63:19; 2Chr 7:14, ark 2Sam 6:2 (strike out 2nd ᵐ5 שֵׁם We Dr and others), = 1Chr 13:6 (adding עָלָיו Oettli Kau; > Kit^Hpt שָׁם שְׁמוֺ), temple 1Kin 8:43 2Chr 6:33; Jer 7:10-11, 14, 30; 32:34; 34:15, city 25:29; Dan 9:18, city + people 9:19; so name of man 2Sam 12:28, as given to his wife Isa 4:1 (5) be called שֵׁם עַל, i.e. reckoned to, Gen 48:6; Isa 54:5; 61:6; עַלאשֵׁבֶט 1Chr 23:14, compare Ezra 2:61 = Neh 7:63.

(4) különösen י שֵׁם ׳נִקְרָא עַל, a tulajdonjog jelölésére: személyről Jer 15:16, népről 5Móz 28:10; Jer 14:9; Ámós 9:12; Ézs 63:19; 2Krón 7:14, a ládáról 2Sám 6:2 (töröld a 2. שֵׁם szót ᵐ5 We Dr és mások szerint), = 1Krón 13:6 (hozzátéve עָלָיו Oettli Kau; > Kit^Hpt שָׁם שְׁמוֺ), a templomról 1Kir 8:43 2Krón 6:33; Jer 7:10-11, 14, 30; 32:34; 34:15, a városról 25:29; Dán 9:18, a városról + népről 9:19; így az ember nevéről 2Sám 12:28, a feleségének adott névről Ézs 4:1 (5) שֵׁם עַל neveztetni, azaz hozzászámíttatni, 1Móz 48:6; Ézs 54:5; 61:6; עַלאשֵׁבֶט 1Krón 23:14, vö. Ezsd 2:61 = Neh 7:63.

**46.** 

> (6) be called בְּשֵׁם Isa 43:7; 48:1.

(6) בְּשֵׁם neveztetni Ézs 43:7; 48:1.

**47.** 

> (7) יִקּ ׳בְּיִצְתָק זָ֑רַע ךְָָ Gen 21:12, i.e. in (through) ׳יִצ shall seed be reckoned to three; שְׁמִי בָהֶם וְיִקָּרֵא 48:16 through them shall my name be called, i.e. perpetuated.

(7) יִקּ ׳בְּיִצְתָק זָ֑רַע ךְָָ 1Móz 21:12, azaz ׳יִצ által neveztetik neked utód; שְׁמִי בָהֶם וְיִקָּרֵא 48:16: általuk neveztessék az én nevem, azaz maradjon fenn.

**48.** 

> (8) be named = menationed, of person Isa 14:20 (9) subject שֵׁם Eccl 6:10, i.e. thing is known. Pu`al (Ezekiel and Isa^2) Perfect3masculine singular קֹרָא be called, subject appell. + ל person or of thing = be named, Isa 48:8; Ezek 10:13 (׳קוֺ); וְקֹרָא consecutive Isa 58:12; 61:3; 62:2 (חָדָשׁ שֵׁם); בִּשְׁמִי קֹרָא לאֹ גּוֺי 65:1; (< קָרָא or קֹרֵא [Qal 2 c], Vrss Lo Ew Che Di and others); be called and privileged (compare Qal 5 f); Participle ׳יִש מְקרָאִי 48:12.

(8) neveztetni = megemlíttetni, személyről Ézs 14:20 (9) alanya שֵׁם Préd 6:10, azaz a dolog ismert. Pu`al (Ezékiel és Ézs^2) perfectum 3. hímnemű egyes szám קֹרָא hívatni, alanya megnev. + személyt vagy dolgot jelölő ל = neveztetni, Ézs 48:8; Ez 10:13 (׳קוֺ); וְקֹרָא consecutivummal Ézs 58:12; 61:3; 62:2 (חָדָשׁ שֵׁם); בִּשְׁמִי קֹרָא לאֹ גּוֺי 65:1; (< קָרָא vagy קֹרֵא [Qal 2 c], Vrss Lo Ew Che Di és mások); elhívatni és kiváltságot kapni (vö. Qal 5 f); participium ׳יִש מְקרָאִי 48:12.

### H7121 — összevetés a meglévő kézi jelentéssel: 2.c

| Meglévő `kezi` (2026.09.22) | Új fordítás, ugyanez a szakasz |
|---|---|
| c. ׳ק י ׳בְּשֵׁם (k. besém J., azaz kárá besém JHVH) hívni ׳י (J., azaz JHVH) nevével (azaz használni azt a segítségül hívásban): 1Móz 4:26; 12:8; 2Kir 5:11; Jer 10:25 = Zsolt 79:6, összesen 16-szor (1Kir 18:24: annak konkrét kérésére, hogy ׳י (J., azaz JHVH) mutassa meg hatalmát), továbbá Ézs 65:1 (l. Pual); Baál nevével: 1Kir 18:24-25, 26. | c. ׳ק י ׳בְּשֵׁם hívni ׳י nevével (azaz használni azt a segítségül hívásban): 1Móz 4:26; 12:8; 2Kir 5:11; Jer 10:25 = Zsolt 79:6, összesen 16-szor (1Kir 18:24 annak konkrét kérésére, hogy ׳י mutassa meg hatalmát), továbbá Ézs 65:1 (l. Pu`al); Baál nevével 1Kir 18:24-25, 26. |

### H7121 — összevetés a meglévő kézi jelentéssel: 3

| Meglévő `kezi` (2026.09.22) | Új fordítás, ugyanez a szakasz |
|---|---|
| 3 kihirdetni: a. a kihirdetett dolog tárgyesetével: Ámós 4:5; 1Móz 41:43; 5Móz 15:2; Jer 31:6; 3Móz 25:10 és máshol; ׳ק צוֺם (kárá com) böjtöt hirdetni: 1Kir 21:9, 12; Jer 36:9 és máshol; ׳ק י ׳מוֺעֲדֵי (kárá móadé JHVH): 3Móz 23:2, 4; ׳ק (k., azaz kárá) után egyenes beszéd: 2Móz 34:6 stb.; ל (le) + személy: Jer 34:8, 15, 17 (a versben kétszer); Ézs 61:1; עַל (al) + személy (ellen, felől): 1Kir 13:4, 32; Jer 49:29; JSir 1:15; békességet hirdetni valakinek (ל (le) + személy): Bír 21:13; vö. ׳ק לְשָׁלוֺם אֵלֶיהָ (kárá lesálóm éléhá) 5Móz 20:10; ׳ק az igével rokon jelentésű tárgyesettel: מִקְרָא (mikrá) Ézs 1:13, הַקְּרִיאָה (hakkeriá) Jón 3:2 (+ אֶל (el)). | 3 kihirdetni: a. a kihirdetett dolog tárgyesetével: Ámós 4:5; 1Móz 41:43; 5Móz 15:2; Jer 31:6; 3Móz 25:10 és máshol; ׳ק צוֺם böjtöt hirdetni 1Kir 21:9, 12; Jer 36:9 és máshol, ׳ק י ׳מוֺעֲדֵי 3Móz 23:2, 4; ׳ק, utána oratio recta [egyenes beszéd]: 2Móz 34:6 stb.; utána ל + személy: Jer 34:8, 15, 17 (a versben kétszer); Ézs 61:1, עַל + személy (ellen, felől) 1Kir 13:4, 32; Jer 49:29; Sir 1:15; békességet hirdetni valakinek (ל + személy) Bír 21:13; vö. ׳ק לְשָׁלוֺם אֵלֶיהָ 5Móz 20:10; ׳ק az igével rokon jelentésű tárgyesettel: מִקְרָא Ézs 1:13, הַקְּרִיאָה Jón 3:2 (+ אֶל). |

## H1121 (BDB, 14948 → 15926 karakter)

`forras_hash=e8222559909c255008d98be3df9615063646ed72` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 55 forrasjelolo (forditas 60)

Törzskapu: RENDBEN · 

**1.** 

> H1121. ben בֵּן_4870 noun masculine son (MI Phoenician בן; so Sabean CIS^iv. No. 2, compare בני DHM^Semitic Sprachforsch. 6; Arabic ; Assyrian bin (u), Lyon^Sargon 9, 1. 57; especially in bin-bin, grandson COT^Gloss, compare Dl below; Aramaic בַּר, , plural בְּנִין, ; compare Palmyrene, especially Vog^No.

H1121. ben בֵּן_4870 hímnemű főnév: fiú (MI föníciai בן; így szabeus CIS^iv. No. 2, vö. בני DHM^Semitic Sprachforsch. 6; arab ; asszír bin (u), Lyon^Sargon 9, 1. 57; különösen a bin-bin, unoka alakban COT^Gloss, vö. alább Dl; arámi בַּר, , többes szám בְּנִין, ; vö. palmürai, különösen Vog^No.

**2.** 

> 21.

21.

**3.** 

> 31. 36a and others; possibly originally connected with בנה build, so Thes, compare Assyrian bânu, begetter (Dl^Pr 104 & compare Ba^ZMG 1887, 638 ff.); but all traces of this √ lost in Hebrew form; √ perhaps originally bilit. (בֵּן בִּן,) ֗֗֗ בַּן see Sta^§ 183) — absolute ׳בּ Gen 4:25 +; ֵבּןֿ Ezek 18:10; construct בֵּן Gen 49:22 (twice in verse); בֶּןֿ 5:32 +; בֶּן Est 2:5; Neh 6:18, & with prefix Gen 17:17; Num 8:25; 1Chr 27:23; 2Chr 25:5; 31:16-17, בְּנוֺ Num 23:18; 24:3, 15; בְּנִי Gen 49:11; בִּן Deut 25:2; בִּןֿ Exod 33:11 32t. (29 t. in combination בִּןנֿוּן (הושׁע ישׁוע,) יהושׁע); suffix בְּנִי Gen 21:10 +; בִּנְךָ Exod 20:10 +; לִבֱנ֑ךָ Deut 7:3; 1Kin 11:13; בְּנֵךְ Gen 30:14 +; בְּנוֺ 4:17 +; בְּנָהּ 21:10 +; plural בָּנִים 3:16 +; construct בְּנֵי 6:2 +; suffix בָּנַי 31:43 +; בָּנֵינוּ Josh 22:25 +; בְּנֵיכֶם Exod 3:22 +, etc.; —

31. 36a és mások; talán eredetileg összefügg a בנה építeni igével, így Thes, vö. asszír bânu, nemző (Dl^Pr 104 & vö. Ba^ZMG 1887, 638 kk.); de ennek a √-nek minden nyoma elveszett a héber alakban; a √ talán eredetileg kétmássalhangzós (בֵּן בִּן,) ֗֗֗ בַּן l. Sta^§ 183) — status absolutus ׳בּ 1Móz 4:25 és máshol; ֵבּןֿ Ez 18:10; status constructus בֵּן 1Móz 49:22 (a versben kétszer); בֶּןֿ 5:32 és máshol; בֶּן Eszt 2:5; Neh 6:18, & prefixummal 1Móz 17:17; 4Móz 8:25; 1Krón 27:23; 2Krón 25:5; 31:16-17, בְּנוֺ 4Móz 23:18; 24:3, 15; בְּנִי 1Móz 49:11; בִּן 5Móz 25:2; בִּןֿ 2Móz 33:11, összesen 32-szer (29-szer a בִּןנֿוּן (הושׁע ישׁוע,) יהושׁע kapcsolatban); suffixummal בְּנִי 1Móz 21:10 és máshol; בִּנְךָ 2Móz 20:10 és máshol; לִבֱנ֑ךָ 5Móz 7:3; 1Kir 11:13; בְּנֵךְ 1Móz 30:14 és máshol; בְּנוֺ 4:17 és máshol; בְּנָהּ 21:10 és máshol; többes szám בָּנִים 3:16 és máshol; status constructus בְּנֵי 6:2 és máshol; suffixummal בָּנַי 31:43 és máshol; בָּנֵינוּ Józs 22:25 és máshol; בְּנֵיכֶם 2Móz 3:22 és máshol, stb.; —

**4.** 

> 1 son, male child, born of a woman Gen 4:25; 16:11, 15; 17:19 compare 17:16; 18:10, 14; 19:37-38, +?בֶּןבִּֿטְנָהּ Isa 49:15; begotten by a man Gen 5:4f; 5:28; 6:10; 11:11f. + often; || בַּת (בָּנוֺת) daughter 5:4, 7, 10f. 11:11, 13, 15f; Exod 20:10; Deut 5:14; 16:11; 16:14; 1Sam 30:3; 30:6; Job 1:2; 42:13 +; of son as desired Gen 30:2 (compare 15:2; 16:2; 17:17; 18:10f.; 1Sam 1:5-11) 2Kin 4:14, 28; Psa 127:3 +; rejoiced in Gen 30:6 +; beloved Exod 21:5; 2Sam 19:1; 19:3; 19:5; 1Kin 3:26; cared for Deut 1:31; spared Mal 3:17; disciplined & trained Deut 8:5; Prov 3:12; 13:24; 19:18; 29:17; owing reverence, obedience, etc. to parents 6:20; 10:1; 13:1; בְּכוֺרְךָ בִּנְךָ thy first-born son Gen 27:32; הַבְּכֹר הַבֵּן Deut 21:15 compare 1Sam 8:2; הַגָּדֹל בְּנָהּ her elder son Gen 27:15, 42; הַגָּדֹל בְּנוֺ 27:1; הַקָּטָן בְּנָהּ her younger son 27:15, 42. In particular a. בֶּןאִֿמּוֺ son of his mother, i.e. own (uterine) brother Gen 43:29, compare 27:29; Judg 8:19; Psa 50:20; 69:9, & see אֵם; אָבִיךָ בְּנֵי sons of thy father = brethren Gen 49:8 (poetry)

1 fiú, fiúgyermek, asszonytól született 1Móz 4:25; 16:11, 15; 17:19, vö. 17:16; 18:10, 14; 19:37-38, +?בֶּןבִּֿטְנָהּ Ézs 49:15; férfitól nemzett 1Móz 5:4k.; 5:28; 6:10; 11:11k. + gyakran; || בַּת (בָּנוֺת) leány 5:4, 7, 10k. 11:11, 13, 15k.; 2Móz 20:10; 5Móz 5:14; 16:11; 16:14; 1Sám 30:3; 30:6; Jób 1:2; 42:13 és máshol; a fiúról mint kívánt gyermekről 1Móz 30:2 (vö. 15:2; 16:2; 17:17; 18:10k.; 1Sám 1:5-11) 2Kir 4:14, 28; Zsolt 127:3 és máshol; akinek örülnek 1Móz 30:6 és máshol; szeretett 2Móz 21:5; 2Sám 19:1; 19:3; 19:5; 1Kir 3:26; akiről gondoskodnak 5Móz 1:31; akit megkímélnek Mal 3:17; akit fegyelmeznek & nevelnek 5Móz 8:5; Péld 3:12; 13:24; 19:18; 29:17; aki tisztelettel, engedelmességgel stb. tartozik a szüleinek 6:20; 10:1; 13:1; בְּכוֺרְךָ בִּנְךָ elsőszülött fiad 1Móz 27:32; הַבְּכֹר הַבֵּן 5Móz 21:15, vö. 1Sám 8:2; הַגָּדֹל בְּנָהּ az idősebbik fia 1Móz 27:15, 42; הַגָּדֹל בְּנוֺ 27:1; הַקָּטָן בְּנָהּ a fiatalabbik fia 27:15, 42. Különösen: a. בֶּןאִֿמּוֺ az anyja fia, azaz édes (egy anyától való) testvér 1Móz 43:29, vö. 27:29; Bír 8:19; Zsolt 50:20; 69:9, & l. אֵם; אָבִיךָ בְּנֵי atyád fiai = testvérek 1Móz 49:8 (költészet)

**5.** 

> b. דֹדֵיהֶן בְּנֵי = cousins Num 36:11.

b. דֹדֵיהֶן בְּנֵי = unokatestvérek 4Móz 36:11.

**6.** 

> c. בְּנִי my son, as term of kindliness or endearment, used by Eli to Samuel 1Sam 3:6, 16; compare 4:16; 24:17; 26:17, 21, 25, see also Prov 1:8, 10; 2:1 +; compare בִּנְךָ, used by Benhadad of himself to Elisha 2Kin 8:9; by Ahaz to Tiglath-pileser 16:7; especially to express intimate and gracious relation with God: ׳י calls Israel בְכֹרִי בְּנִי Exod 4:22 compare 4:23; Hosea 11:1, see also Psa 80:16 (but compare Che); אלהיכם ליהוה אַתֶּם בָּנִים Deut 14:1; עֶלְיוֺן בְּנֵי Psa 82:6 (|| אלהים); אֵלחָֿ֑י בְּנֵי Hosea 2:1; compare further Deut 32:5 (plural) 32:20 (plural) Isa 1:2, 4; 30:1, 9; Jer 3:14, 22; 4:22; 31:20; of future Davidic king 2Sam 7:14 = 1Chr 17:13 compare Psa 2:7; expressly referred to Solomon 1Chr 22:10; 28:6; also of children (offered in fire) Ezek 16:21.

c. בְּנִי fiam, a jóindulat vagy a szeretet kifejezéseként, Éli szól így Sámuelhez 1Sám 3:6, 16; vö. 4:16; 24:17; 26:17, 21, 25, l. még Péld 1:8, 10; 2:1 és máshol; vö. בִּנְךָ, Benhadad mondja magáról Elizeusnak 2Kir 8:9; Akház Tiglat-Pileszernek, 16:7; különösen az Istennel való bensőséges és kegyelmes viszony kifejezésére: ׳י Izráelt בְכֹרִי בְּנִי nevezi 2Móz 4:22, vö. 4:23; Hós 11:1, l. még Zsolt 80:16 (de vö. Che); אלהיכם ליהוה אַתֶּם בָּנִים 5Móz 14:1; עֶלְיוֺן בְּנֵי Zsolt 82:6 (|| אלהים); אֵלחָֿ֑י בְּנֵי Hós 2:1; vö. továbbá 5Móz 32:5 (többes szám) 32:20 (többes szám) Ézs 1:2, 4; 30:1, 9; Jer 3:14, 22; 4:22; 31:20; az eljövendő Dávid-házi királyról 2Sám 7:14 = 1Krón 17:13, vö. Zsolt 2:7; kifejezetten Salamonra vonatkoztatva 1Krón 22:10; 28:6; gyermekekről is (akiket tűzben áldoztak fel) Ez 16:21.

**7.** 

> d. האלהים בְּנֵי applied to supernatural beings Gen 6:2, 4; Job 1:6; 2:1; אלהים בְּנֵי 38:7; אֵלִים בְּנֵי Psa 29:1 (on which compare Che's note) 89:7.

d. האלהים בְּנֵי természetfeletti lényekre alkalmazva 1Móz 6:2, 4; Jób 1:6; 2:1; אלהים בְּנֵי 38:7; אֵלִים בְּנֵי Zsolt 29:1 (ehhez vö. Che jegyzetét) 89:7.

**8.** 

> e. בֶּןאָֿדָם son of man, compare א ׳בְּנֵי, see אָדָם; אִישׁ בְּנֵי Psa 4:3 & (|| אדם בני) 49:3; 62:10.

e. בֶּןאָֿדָם emberfia, vö. א ׳בְּנֵי, l. אָדָם; אִישׁ בְּנֵי Zsolt 4:3 & (|| אדם בני) 49:3; 62:10.

**9.** 

> f. בֶּןבִּֿנְךָ = thy grandson Exod 10:2; Deut 6:2; Judg 8:22 compare Jer 27:7; plural Exod 34:7; Deut 4:9; 4:25; Judg 12:14; 2Kin 17:41; 2Chron 8:40; Job 42:16; Psa 128:6; Prov 13:22; 17:6; Ezek 37:25; also בֵּן alone with similar reference Gen 29:5 (Laban son of Nahor); Laban calls his daughters' children his own sons 31:28, 43; compare 32:1; so of Naomi Ruth 4:17; רְבִעִים בְּנֵי 2Kin 10:30 sons of the fourth Generation, and, in General, descendants Josh 22:24-25, 27 +; see also below i. below g. constantly, as more precise designation, added to personal name בֶּןיְֿפֻנֶּה כָּלֵב Num 14:30; 32:12; 34:19 +; בִּןנֿוּן יְהוֺשֻׁעַ 11:28; 14:30; 32:12, 28; 34:17 +; בֶּןנְֿבָט יָרָבְעָם 1Kin 12:2, 15 +, etc.; also without personal name (often with implication of contempt) בֶּןקִֿישׁ 1Sam 10:11; בֶּןיִֿשַׁי 20:27, 30, 31; 22:7-8, 9, 13; 25:10; 2Sam 20:1; צְרוּיָה בְּנֵי 16:10; בֶּןרְֿמַלְיָהוּ Isa 7:4-5, 9; 8:16; בֶּןטָֽֿבְאַ֑ל 7:6; compare also לֵוִי בְּנֵי Num 16:7-8,.

f. בֶּןבִּֿנְךָ = unokád 2Móz 10:2; 5Móz 6:2; Bír 8:22, vö. Jer 27:7; többes szám 2Móz 34:7; 5Móz 4:9; 4:25; Bír 12:14; 2Kir 17:41; 2Krón 8:40; Jób 42:16; Zsolt 128:6; Péld 13:22; 17:6; Ez 37:25; a בֵּן önmagában is hasonló vonatkozással 1Móz 29:5 (Lábán, Náhor fia); Lábán a leányai gyermekeit a saját fiainak nevezi 31:28, 43; vö. 32:1; így Naomiról Ruth 4:17; רְבִעִים בְּנֵי 2Kir 10:30: a negyedik nemzedék fiai, és általában: leszármazottak Józs 22:24-25, 27 és máshol; l. még alább i. alatt. g. állandóan, pontosabb megjelölésként, személynévhez fűzve: בֶּןיְֿפֻנֶּה כָּלֵב 4Móz 14:30; 32:12; 34:19 és máshol; בִּןנֿוּן יְהוֺשֻׁעַ 11:28; 14:30; 32:12, 28; 34:17 és máshol; בֶּןנְֿבָט יָרָבְעָם 1Kir 12:2, 15 és máshol, stb.; személynév nélkül is (gyakran megvetés árnyalatával) בֶּןקִֿישׁ 1Sám 10:11; בֶּןיִֿשַׁי 20:27, 30, 31; 22:7-8, 9, 13; 25:10; 2Sám 20:1; צְרוּיָה בְּנֵי 16:10; בֶּןרְֿמַלְיָהוּ Ézs 7:4-5, 9; 8:16; בֶּןטָֽֿבְאַ֑ל 7:6; vö. még לֵוִי בְּנֵי 4Móz 16:7-8.

**10.** 

> h. designated as בֶּןזְֿקֻנִים i.e. born in old age of father Gen 37:3; opposed to הַנְּעוּרִים בְּנֵי sons of one's youth Psa 127:4; also בֶּןבֵּֿיתִי one born in my house Gen 15:3 (i.e. slave) so בַיִת בְּנֵי Eccl 2:7.

h. בֶּןזְֿקֻנִים megjelöléssel, azaz az apa öregkorában született 1Móz 37:3; szemben a הַנְּעוּרִים בְּנֵי kifejezéssel: valaki ifjúkorának fiai Zsolt 127:4; továbbá בֶּןבֵּֿיתִי házamban született 1Móz 15:3 (azaz rabszolga), így בַיִת בְּנֵי Préd 2:7.

**11.** 

> i. in various combinations:

i. különféle kapcsolatokban:

**12.** 

> (α) as expression of contumely, הַמַּרְדּוּת נַעֲוַת בֶּןֿ 1Sam 20:30; הַזֶּה בֶּןהַֿמְּרַצֵּחַ 2Kin 6:32 this son of a murderer; compare בְּנֵינָֿבָל Job 30:8; בְלִישֵֿׁם בְּנֵי ib.; עֹנֲַנָה בְּנֵי Isa 57:3 (|| מְנָאֵף זֶרַע); compare אַחֶרֶת בֶּןאִֿשָּׁה Judg 11:2 (compare 11:1);

(α) a gyalázkodás kifejezéseként, הַמַּרְדּוּת נַעֲוַת בֶּןֿ 1Sám 20:30; הַזֶּה בֶּןהַֿמְּרַצֵּחַ 2Kir 6:32: ez a gyilkos fia; vö. בְּנֵינָֿבָל Jób 30:8; בְלִישֵֿׁם בְּנֵי ugyanott; עֹנֲַנָה בְּנֵי Ézs 57:3 (|| מְנָאֵף זֶרַע); vö. אַחֶרֶת בֶּןאִֿשָּׁה Bír 11:2 (vö. 11:1);

**13.** 

> (β) as term of respect, dignity, בֶּןחֿוֺרִים son of nobles Eccl 10:17 (in Aramaic = free born); בֶּןחֲֿכָמִים Isa 19:11; בֶּןמַֿלְכֵיקֶֿדֶם ib.; compare בֶּןמֶֿלֶךְ Psa 72:1 (|| מֶלֶךְ); בֶּןאֲֿמָתֶ֑ךָ 86:16 in addressing ׳י (|| עַבְדֶּ֑ךָ) & בְּנֵיעֲֿבָדֶיךָ Psalm 102:29; of noble appearance הַמֶּלֶךְ בְּנֵי Judg 8:18. j. often plural with name of ancestor, people, land, or city, to denote descendants, inhabitants, membership in a nation or family, etc.:

(β) a tisztelet, a méltóság kifejezéseként, בֶּןחֿוֺרִים nemesek fia Préd 10:17 (arámiul = szabadnak született); בֶּןחֲֿכָמִים Ézs 19:11; בֶּןמַֿלְכֵיקֶֿדֶם ugyanott; vö. בֶּןמֶֿלֶךְ Zsolt 72:1 (|| מֶלֶךְ); בֶּןאֲֿמָתֶ֑ךָ 86:16 ׳י megszólításában (|| עַבְדֶּ֑ךָ) & בְּנֵיעֲֿבָדֶיךָ Zsolt 102:29; nemes megjelenésről הַמֶּלֶךְ בְּנֵי Bír 8:18.j. gyakran többes számban, az ős, a nép, az ország vagy a város nevével, a leszármazottak, a lakosok, egy nemzethez vagy családhoz való tartozás stb. jelölésére:

**14.** 

> (α) e.g. בְּנֵיעֵֿבֶר Gen 10:21; בְּנֵיחֵֿת 23:3, 5, 7, 10 (twice in verse); 23:11, 16, 18, 20; 25:10; 49:32 (all P); (בְּנֵישֵֿׁת Num 24:17 see below 8); בְּנֵיחֲֿמוֺר Gen 33:19; Josh 24:32; עֵשָׂו בְּנֵי Gen 36:5, 15, 19; Deut 2:4, 8, 12, 22, 29; שֵׂעִיר בְּנֵי Gen 36:20-21, בֶּןֿ(בני)הִנֹּם Josh 15:8 + (compare below גַּיְא); לוֺט בְּנֵי Deut 2:9, 19; Psa 83:9; בְּנֵייֿוֺסֵף (literal Gen 46:27; 48:8; 1Chr 5:1) Num 1:32; 26:28, 37; 34:23; 36:5 (ב ׳מַטֵּה ׳י) + 6 t. Joshua, compare Psa 77:16; even מְנַשֶּׁה שֵׁבֶט חֲצִי בְּנֵי 1Chr 5:23; דָוַיד בְּנֵי (literal 2Sam 8:18 = 1Chr 18:17; 3:1, 9) 2Chr 13:8; 23:3; 32:33; אָסָף בְּנֵי29:13; Ezra 2:41; 3:8 + (see אָסָף); קֹרַח בְּנֵי in titles of Psalm 42-49, 84, 85, 87, 88; especially (β) בְּנֵיעַֿמּוֺן (standing designation of people of Ammon) Gen 19:38 81t. (compare עַמּוֺן & Nö^ZMG 1886, 171 Dr^Sm 66); יַעֲקֹב בְּנֵי (literal 34:7, 13, 25, 27; 35:5, 22, 26; 49:2) 2Kin 17:34; Psa 105:6; Mal 3:6 compare Psa 77:16; & chiefly (γ) יִשְׂרָאֵל בְּנֵי (literal Gen 42:5; 45:21; 46:5; Exod 1:1) 1:7 613t., including Hexateuch 427 (of which 328 P, 49 E, 25 J, 25 D), Judges 61, Samuel Kings Chronicles 73 (23 in reference to ancient history, 10 in opposition to Judah); so also Vrss & variant reading sometimes for יִשׂ ׳בֵּית, e.g. Josh 21:43 + see Di, Ezek 3:1 + see Co; also the reverse 2:3 and elsewhere; note especially בּ ׳עַם יִשְׂרָאֵל Exod 1:9; בּ ׳עַמִּי יִשְׂרָאֵל 3:10; 7:4; יִשְׂרָאֵל בְּנֵי עֲדַת 16:1-2, 9, 10; 17:1; Lev 16:5; 19:2; Num 1:2, 53; 8:9, 20; 13:26; 15:25-26, 17:6; 19:9; 25:6; 26:2; 31:12 (all P); ב ׳דֹּרוֺת ׳יִשׂ Judg 3:2; ׳כָּלבֿ ׳יִשׂ וְכָלהָֿעָם 20:26; ׳ב ׳יִשׂ הַלֵּוִי וּבְּנֵי Nehemiah 10:40; also (δ) יְהוּדָה בְּנֵי (literal Gen 46:12; 26:19; 1Chr 2:3, 10; 4:1) Num 1:26 18t. Numbers, Joshua, Judg 1:8-9, 16 (so read also 1:21; 1:21 compare Josh 15:53 & see below בנימן) 2Sam 1:18; 1Chr 4:27 8t. Chronicles, Jer 7:30 4t. Jeremiah; Hosea 2:2; Joel 4:6; Joel 4:8; Joel 4:19; Obadiah 12 (not in Kings, of Judah or of any other tribe, except לֵוִי בְּנֵי 1Kin 12:31) including יהוּדָה בְּנֵי מַטֵּה Josh 15:1, 20, 21; 21:1; 1Chr 6:50; for usage with other tribes of Israel, see the articles; — but note (ε) לֵוִי בְּנֵי (literal Gen 46:11; Exod 6:16; Num 3:17; 1 Chronicles 5:27; 1Chr 6:1; compare 23:6) Exod 32:28; Num 3:15; 16:7-8, 18:21; Josh 21:10 (as including sons of Aaron etc.); לֵוִי כָּלבְּֿנֵי Exod 32:26; ב ׳כָּלאַֿחֶיךָ ׳ל Num 16:10; ב ׳הַכֹּהֲנִים ׳ל Deut 21:5; 31:9 compare 1Kin 12:31 & Mal 3:8; 1Chr 23:24, 27; 24:20; Ezra 8:15 (distinguished from priests) Neh 12:23; Ezek 40:46 (including צָדוֺק בְּנֵי the priests); also ב ׳מַחֲנוֺת ׳ל 1Chr 9:18; הַלֵּוִי בְּנֵי 12:27; Nehemiah 10:40; הַלְּוִיִם בְּנֵי 15:15; 24:30 (compare also לֵוִי);

(α) pl. בְּנֵיעֵֿבֶר 1Móz 10:21; בְּנֵיחֵֿת 23:3, 5, 7, 10 (a versben kétszer); 23:11, 16, 18, 20; 25:10; 49:32 (mind P); (בְּנֵישֵֿׁת 4Móz 24:17, l. alább 8); בְּנֵיחֲֿמוֺר 1Móz 33:19; Józs 24:32; עֵשָׂו בְּנֵי 1Móz 36:5, 15, 19; 5Móz 2:4, 8, 12, 22, 29; שֵׂעִיר בְּנֵי 1Móz 36:20-21, בֶּןֿ(בני)הִנֹּם Józs 15:8 és máshol (vö. alább גַּיְא); לוֺט בְּנֵי 5Móz 2:9, 19; Zsolt 83:9; בְּנֵייֿוֺסֵף (szó szerint 1Móz 46:27; 48:8; 1Krón 5:1) 4Móz 1:32; 26:28, 37; 34:23; 36:5 (ב ׳מַטֵּה ׳י) + Józsué könyvében 6-szor, vö. Zsolt 77:16; sőt מְנַשֶּׁה שֵׁבֶט חֲצִי בְּנֵי 1Krón 5:23; דָוַיד בְּנֵי (szó szerint 2Sám 8:18 = 1Krón 18:17; 3:1, 9) 2Krón 13:8; 23:3; 32:33; אָסָף בְּנֵי29:13; Ezsd 2:41; 3:8 és máshol (l. אָסָף); קֹרַח בְּנֵי a 42-49, 84, 85, 87, 88. zsoltár címében; különösen (β) בְּנֵיעַֿמּוֺן (Ammon népének állandó megjelölése) 1Móz 19:38, összesen 81-szer (vö. עַמּוֺן & Nö^ZMG 1886, 171 Dr^Sm 66); יַעֲקֹב בְּנֵי (szó szerint 34:7, 13, 25, 27; 35:5, 22, 26; 49:2) 2Kir 17:34; Zsolt 105:6; Mal 3:6, vö. Zsolt 77:16; & főként (γ) יִשְׂרָאֵל בְּנֵי (szó szerint 1Móz 42:5; 45:21; 46:5; 2Móz 1:1) 1:7, összesen 613-szor, ebből a Hexateuchban 427-szer (ebből 328 P, 49 E, 25 J, 25 D), a Bírák könyvében 61-szer, Sámuel, a Királyok és a Krónikák könyveiben 73-szor (23-szor a régi történelemre utalva, 10-szer Júdával szembeállítva); így a Vrss & a variáns olvasat is néha a יִשׂ ׳בֵּית helyett, pl. Józs 21:43 + l. Di, Ez 3:1 + l. Co; fordítva is: 2:3 és másutt; figyeld meg különösen: בּ ׳עַם יִשְׂרָאֵל 2Móz 1:9; בּ ׳עַמִּי יִשְׂרָאֵל 3:10; 7:4; יִשְׂרָאֵל בְּנֵי עֲדַת 16:1-2, 9, 10; 17:1; 3Móz 16:5; 19:2; 4Móz 1:2, 53; 8:9, 20; 13:26; 15:25-26, 17:6; 19:9; 25:6; 26:2; 31:12 (mind P); ב ׳דֹּרוֺת ׳יִשׂ Bír 3:2; ׳כָּלבֿ ׳יִשׂ וְכָלהָֿעָם 20:26; ׳ב ׳יִשׂ הַלֵּוִי וּבְּנֵי Neh 10:40; továbbá (δ) יְהוּדָה בְּנֵי (szó szerint 1Móz 46:12; 26:19; 1Krón 2:3, 10; 4:1) 4Móz 1:26, Mózes negyedik könyvében összesen 18-szor, Józsué könyvében, Bír 1:8-9, 16 (így olvasandó az 1:21-ben is; 1:21, vö. Józs 15:53 & l. alább בנימן) 2Sám 1:18; 1Krón 4:27, a Krónikák könyveiben összesen 8-szor, Jer 7:30, Jeremiás könyvében összesen 4-szer; Hós 2:2; Jóel 4:6; Jóel 4:8; Jóel 4:19; Abd 12 (a Királyok könyveiben nem, sem Júdáról, sem más törzsről, kivéve לֵוִי בְּנֵי 1Kir 12:31), beleértve יהוּדָה בְּנֵי מַטֵּה Józs 15:1, 20, 21; 21:1; 1Krón 6:50; Izráel többi törzsére vonatkozó használatról l. az illető szócikkeket; — de figyeld meg (ε) לֵוִי בְּנֵי (szó szerint 1Móz 46:11; 2Móz 6:16; 4Móz 3:17; 1Krón 5:27; 1Krón 6:1; vö. 23:6) 2Móz 32:28; 4Móz 3:15; 16:7-8, 18:21; Józs 21:10 (Áron fiait is beleértve stb.); לֵוִי כָּלבְּֿנֵי 2Móz 32:26; ב ׳כָּלאַֿחֶיךָ ׳ל 4Móz 16:10; ב ׳הַכֹּהֲנִים ׳ל 5Móz 21:5; 31:9, vö. 1Kir 12:31 & Mal 3:8; 1Krón 23:24, 27; 24:20; Ezsd 8:15 (a papoktól megkülönböztetve) Neh 12:23; Ez 40:46 (beleértve צָדוֺק בְּנֵי, a papokat); továbbá ב ׳מַחֲנוֺת ׳ל 1Krón 9:18; הַלֵּוִי בְּנֵי 12:27; Neh 10:40; הַלְּוִיִם בְּנֵי 15:15; 24:30 (vö. még לֵוִי);

**15.** 

> (ζ) אַהֲרֹן בְּנֵי (literal Exod 28:1, 40; 1 Chronicles 5:29; 1Chr 24:1; often Aaron and his sons literal Exod 27:21; 28:1, 4 +) Lev 3:5, 8, 13; 6:7; 6:11; 7:10; Leviticus 7:83; Josh 21:10; 1Chr 6:35; 6:39; 6:42; 15:4 (+ Levites) 24:1; 24:31; Neh 12:47; also א ׳בְּנֵי הַכֹּהֲנִים Lev 1:5, 8, 11; 2:2; 3:2; Num 3:8; 10:8 & Josh 21:19; 2Chr 31:19; compare 26:18; 29:21; 35:14 (twice in verse); הַכֹּהֵן אַהֲרֹן בְּנֵי Lev 1:7; Josh 21:4 (as subdivision of Levites) 21:13 compare Lev 7:34; וְהַלְּוִּיִּם אַהֲרֹן אֶתבְּֿנֵי יהוה אֶתכֹּֿהֲנֵי2Chr 13:9 compare 13:10; once in singular בֶּןאַֿהֲרֹן הַכֹּהֵן Neh 10:39; see also below אַהֲרֹן;

(ζ) אַהֲרֹן בְּנֵי (szó szerint 2Móz 28:1, 40; 1Krón 5:29; 1Krón 24:1; gyakran Áron és fiai, szó szerint 2Móz 27:21; 28:1, 4 és máshol) 3Móz 3:5, 8, 13; 6:7; 6:11; 7:10; 3Móz 7:83; Józs 21:10; 1Krón 6:35; 6:39; 6:42; 15:4 (+ léviták) 24:1; 24:31; Neh 12:47; továbbá א ׳בְּנֵי הַכֹּהֲנִים 3Móz 1:5, 8, 11; 2:2; 3:2; 4Móz 3:8; 10:8 & Józs 21:19; 2Krón 31:19; vö. 26:18; 29:21; 35:14 (a versben kétszer); הַכֹּהֵן אַהֲרֹן בְּנֵי 3Móz 1:7; Józs 21:4 (a léviták alcsoportjaként) 21:13, vö. 3Móz 7:34; וְהַלְּוִּיִּם אַהֲרֹן אֶתבְּֿנֵי יהוה אֶתכֹּֿהֲנֵי2Krón 13:9, vö. 13:10; egyszer egyes számban בֶּןאַֿהֲרֹן הַכֹּהֵן Neh 10:39; l. még alább אַהֲרֹן;

**16.** 

> (η) צָדוֺק בְּנֵי Ezek 40:26, 44:15 צדוק בני הלוים הכהנים; 48:11 צדוק מנגי הַמְֿקֻדָּשׁ הכהנים (ᵐ5 Sm Co join מ of מבני to preceding word, making plural);

(η) צָדוֺק בְּנֵי Ez 40:26, 44:15 צדוק בני הלוים הכהנים; 48:11 צדוק מנגי הַמְֿקֻדָּשׁ הכהנים (ᵐ5 Sm Co a מבני מ betűjét az előző szóhoz kapcsolják, többes számot képezve);

**17.** 

> (φ) בְּנֵי with names of peoples, lands, and cities, כֻּשִׁיִּים בְּנֵי Amos 9:7; מִצְרַיִם בְּנֵי Ezek 16:26; אַשּׁוּר בְּנֵי 16:28; 23:7, 9, 12, 23; ׳ב הַבְּרִית אֶדֶץ 30:5 (Co strike out ארץ); ׳ב בָּבֶל 23:15. 23:17, 28; ׳ב יְרוּשָׁלַם Joel 4:6; ׳ב צִיּוֺן Joel 2:23; Lam 4:2; Psa 149:2 (compare Zech 9:13). See further (ι) עַמֶּ֑ךָ בְּנֵי Lev 19:18; compare 20:17; Num 22:5; Judg 14:16-17, Ezek 3:11; 33:2, 12, 17, 30; 37:18; Dan 12:1 עַמְּךָ מָּרִיצֵי בְּנֵי 11:14;

(φ) בְּנֵי népek, országok és városok nevével, כֻּשִׁיִּים בְּנֵי Ámós 9:7; מִצְרַיִם בְּנֵי Ez 16:26; אַשּׁוּר בְּנֵי 16:28; 23:7, 9, 12, 23; ׳ב הַבְּרִית אֶדֶץ 30:5 (Co törli: ארץ); ׳ב בָּבֶל 23:15. 23:17, 28; ׳ב יְרוּשָׁלַם Jóel 4:6; ׳ב צִיּוֺן Jóel 2:23; Sir 4:2; Zsolt 149:2 (vö. Zak 9:13). L. továbbá (ι) עַמֶּ֑ךָ בְּנֵי 3Móz 19:18; vö. 20:17; 4Móz 22:5; Bír 14:16-17, Ez 3:11; 33:2, 12, 17, 30; 37:18; Dán 12:1 עַמְּךָ מָּרִיצֵי בְּנֵי 11:14;

**18.** 

> (κ) הָעָם בְּנֵי קֶבֶר 2Kin 23:6; 2Chr 35:5, 7, 12; הָעָם בְּנֵי קִבְרֵי Jer 26:23;

(κ) הָעָם בְּנֵי קֶבֶר 2Kir 23:6; 2Krón 35:5, 7, 12; הָעָם בְּנֵי קִבְרֵי Jer 26:23;

**19.** 

> (λ) בְּנֵיקֶֿדֶם Gen 29:1; Judg 7:12; 8:10; 1Kin 5:10; Job 1:3; Isa 11:14; Jer 49:28; Ezek 25:4, 10;

(λ) בְּנֵיקֶֿדֶם 1Móz 29:1; Bír 7:12; 8:10; 1Kir 5:10; Jób 1:3; Ézs 11:14; Jer 49:28; Ez 25:4, 10;

**20.** 

> (μ) הַמְּדִינָה בְּנֵי Ezra 2:1 = Neh 7:6;

(μ) הַמְּדִינָה בְּנֵי Ezsd 2:1 = Neh 7:6;

**21.** 

> (ν) of bulls, בָשָׁן בְּנֵי Deut 32:14 (song) compare Klo^SK 1872. 254 Di.

(ν) bikákról, בָשָׁן בְּנֵי 5Móz 32:14 (ének), vö. Klo^SK 1872. 254 Di.

**22.** 

> 2 children (male and female) Gen 3:16; 21:7; Exod 21:5; 22:23; hence הַזְכָּרִים מְנַשֶּׁה בְּנֵי Josh 17:2 male children, זָכָר בֵּן Jer 20:15.

2 gyermekek (fiúk és lányok) 1Móz 3:16; 21:7; 2Móz 21:5; 22:23; ezért הַזְכָּרִים מְנַשֶּׁה בְּנֵי Józs 17:2: fiúgyermekek, זָכָר בֵּן Jer 20:15.

**23.** 

> 3 youth, young men (plural) Prov 7:7; Song 2:3.

3 ifjúság, ifjak (többes szám) Péld 7:7; Én 2:3.

**24.** 

> 4 the young of animals Lev 22:28 (שֶׂה אוֺ שׁוֺר) compare Deut 22:6-7, 1Sam 6:7, 10; Zech 9:9; Job 4:11; 28:8; 39:4, 16; — בֶּןבָּֿקָר etc. see below 7b below 5 of plant-shoots מֹּרָת בֵּן Gen 49:22 (twice in verse); also בֵּן Psa 80:16 ? (|| כַּנָּה; see Che^transl. & critical note)

4 az állatok kicsinyei 3Móz 22:28 (שֶׂה אוֺ שׁוֺר), vö. 5Móz 22:6-7, 1Sám 6:7, 10; Zak 9:9; Jób 4:11; 28:8; 39:4, 16; — בֶּןבָּֿקָר stb. l. alább 7b alatt 5 növényhajtásokról מֹּרָת בֵּן 1Móz 49:22 (a versben kétszer); továbbá בֵּן Zsolt 80:16 ? (|| כַּנָּה; l. Che^transl. & kritikai jegyzet)

**25.** 

> 6 figurative of lifeless things, רֶשֶׁף בְּנֵי sparks Job 5:7; stars עַלבָּֿנֶיהָ עַיִשׁ 38:32; arrows בֶּןקָֿ֑שֶׁת 41:2; אַשְׁמָּתוֺ בְּנֵי Lam 3:13; compare בֶּןגָּֿרְנִי i.e. corn of my threshing-floor Isa 21:10.

6 átvitt értelemben élettelen dolgokról, רֶשֶׁף בְּנֵי szikrák Jób 5:7; csillagok עַלבָּֿנֶיהָ עַיִשׁ 38:32; nyilak בֶּןקָֿ֑שֶׁת 41:2; אַשְׁמָּתוֺ בְּנֵי Sir 3:13; vö. בֶּןגָּֿרְנִי, azaz szérűm gabonája Ézs 21:10.

**26.** 

> 7.

7.

**27.** 

> a. member of a guild, order or class, הַנְּבִיאִים בְּנֵי i.e. those belonging to the prophetic order 1Kin 20:35; 2Kin 2:3, 5, 7, 15; 4:1, 38 (twice in verse); 5:22; 6:1; 9:1 (Hoffm RS^Proph, 85, 388, Ki 15 f.; Zehnpf^BAS i, 355 compare Assyrian mâr šipri (šiprâtum), son of a messenger = messenger, and explains from the son's succeeding to father's calling) & בֶּןנָֿבִיא Amos 7:14; probably also הַכֹּהֲנִים בְּנֵי 1Chr 9:30; Ezra 2:61; 10:18; הַשֹּׁעֲרִים בְּנֵי 2:42; compare הַגְּדוּד בְּנֵי2Chr 25:13 men of the troop, see Palmyrene בנישירתא men of the caravan Vog^No, 4 and others; also הַגּוֺלָה בְּנֵי = exiles Ezra 4:1; 6:19-20, 8:35; 10:7, 16 (see גולה below גלה): further, in בֶּןנֵֿכָר = foreigner (only P, poetry, & late) Gen 17:12, 27; Exod 12:43; Lev 22:25; Ezek 44:9 (twice in verse); ׳הַֿנּ׳ב Isa 56:3; בְּנֵיִנֵֿכָר 2Sam 22:45-46, = Psa 18:45; 18:46; Neh 9:2; Isa 60:10; 61:5; 62:8; Ezek 44:7; Psa 144:7; 144:11, ׳בְּנֵיהַֿנּ Isa 56:6; also עִמָּכֶם הַגָּרִים הַתּוֺשָׁבִּים בְּנֵי Lev 25:4-5,.

a. céh, rend vagy osztály tagja, הַנְּבִיאִים בְּנֵי, azaz a prófétarendhez tartozók 1Kir 20:35; 2Kir 2:3, 5, 7, 15; 4:1, 38 (a versben kétszer); 5:22; 6:1; 9:1 (Hoffm RS^Proph, 85, 388, Ki 15 k.; Zehnpf^BAS i, 355 vö. asszír mâr šipri (šiprâtum), követ fia = követ, és ezt abból magyarázza, hogy a fiú követi apját a hivatásában) & בֶּןנָֿבִיא Ámós 7:14; valószínűleg הַכֹּהֲנִים בְּנֵי is 1Krón 9:30; Ezsd 2:61; 10:18; הַשֹּׁעֲרִים בְּנֵי 2:42; vö. הַגְּדוּד בְּנֵי2Krón 25:13: a csapat emberei, l. palmürai בנישירתא: a karaván emberei Vog^No, 4 és mások; továbbá הַגּוֺלָה בְּנֵי = száműzöttek Ezsd 4:1; 6:19-20, 8:35; 10:7, 16 (l. גולה a גלה alatt): továbbá a בֶּןנֵֿכָר = idegen kifejezésben (csak P, költészet, & késői) 1Móz 17:12, 27; 2Móz 12:43; 3Móz 22:25; Ez 44:9 (a versben kétszer); ׳הַֿנּ׳ב Ézs 56:3; בְּנֵיִנֵֿכָר 2Sám 22:45-46, = Zsolt 18:45; 18:46; Neh 9:2; Ézs 60:10; 61:5; 62:8; Ez 44:7; Zsolt 144:7; 144:11, ׳בְּנֵיהַֿנּ Ézs 56:6; továbbá עִמָּכֶם הַגָּרִים הַתּוֺשָׁבִּים בְּנֵי 3Móz 25:4-5.

**28.** 

> b. of animals, בֶּןבָּֿקָר son of (the) herd, i.e. young one of the herd, בָקָר וּבְנֵי בָּקָר 1Sam 14:32 compare בֶּןבָּֿקָר עֵגֶל Lev 9:2 (P); then, in General, one of the herd: fit for food Gen 18:7-8, (J), for sacrifice Num 15:8-9, (P); ׳בןהַֿב only Lev 12:6 (P); especially בֶּןבָּֿקָר מַּר Exod 29:1; Lev 4:3, 14; 16:3; 23:18; Num 7:15-16t. Numbers (all P) + 2Chr 13:9; Ezek 43:19, 23, 25; 45:18; 46:6; בָּקָר בְּנֵי מָּרִים Num 28:11, 19, 27; 29:13, 17 (P); also אֲתֹנוֺ בְּנִי Gen 49:11 (poem, J; || עִירֹה); בְּנֵיצֹֿאן Psa 114:4; 114:6; בֶּןרְֿאֵמִים 29:6; הָרַמָּכִים בְָּנֵי Est 8:10; (הַ)יּוֺנָה בְּנֵי Lev 1:14 7t. Lev + Num 6:10 compare בֶּןיֿוֺנָה Lev 12:6 (all P); נָ֑שֶׁר בְּנֵיֿ Prov 30:17; עֹרֵב בְּנֵי Psa 147:9. 8 ׳ב as relative noun followed by word of quality, characteristic, etc. especially (α) בֶּןֿ(בני)חַיִל = mighty man 1Sam 14:52; 18:17; 2Sam 2:7; 13:28; 17:10 (twice in verse); 1Kin 1:52 7t. Chronicles; ח בני ׳אֲנָשִׁים Judg 18:2; 2Kin 2:16; הֶחָ֑יִל מִבְּנֵי אִישׁ אֶלֶף Judg 21:10;

b. állatokról, בֶּןבָּֿקָר a csorda fia, azaz a csorda egy fiatal állata, בָקָר וּבְנֵי בָּקָר 1Sám 14:32, vö. בֶּןבָּֿקָר עֵגֶל 3Móz 9:2 (P); azután általában a csorda egy állata: ételnek való 1Móz 18:7-8, (J), áldozatra való 4Móz 15:8-9, (P); ׳בןהַֿב csak 3Móz 12:6 (P); különösen בֶּןבָּֿקָר מַּר 2Móz 29:1; 3Móz 4:3, 14; 16:3; 23:18; 4Móz 7:15, Mózes negyedik könyvében összesen 16-szor (mind P) + 2Krón 13:9; Ez 43:19, 23, 25; 45:18; 46:6; בָּקָר בְּנֵי מָּרִים 4Móz 28:11, 19, 27; 29:13, 17 (P); továbbá אֲתֹנוֺ בְּנִי 1Móz 49:11 (költemény, J; || עִירֹה); בְּנֵיצֹֿאן Zsolt 114:4; 114:6; בֶּןרְֿאֵמִים 29:6; הָרַמָּכִים בְָּנֵי Eszt 8:10; (הַ)יּוֺנָה בְּנֵי 3Móz 1:14, Mózes harmadik könyvében összesen 7-szer + 4Móz 6:10, vö. בֶּןיֿוֺנָה 3Móz 12:6 (mind P); נָ֑שֶׁר בְּנֵיֿ Péld 30:17; עֹרֵב בְּנֵי Zsolt 147:9. 8 ׳ב viszonyító főnévként, utána minőséget, jellemzőt stb. jelölő szó, különösen (α) בֶּןֿ(בני)חַיִל = hatalmas férfi 1Sám 14:52; 18:17; 2Sám 2:7; 13:28; 17:10 (a versben kétszer); 1Kir 1:52, a Krónikák könyveiben összesen 7-szer; ח בני ׳אֲנָשִׁים Bír 18:2; 2Kir 2:16; הֶחָ֑יִל מִבְּנֵי אִישׁ אֶלֶף Bír 21:10;

**29.** 

> (β) עַוְלָה בְּנֵי wicked men 2Sam 3:34; 7:10; 1Chr 17:9; Hosea 10:9; ׳בֶּןעֿ Psa 89:23 (for בליעל בני see בליעל);

(β) עַוְלָה בְּנֵי gonosz emberek 2Sám 3:34; 7:10; 1Krón 17:9; Hós 10:9; ׳בֶּןעֿ Zsolt 89:23 (a בליעל בני kifejezéshez l. בליעל);

**30.** 

> (γ) מֶ֑רִי בְּנֵי rebels Numbers 17:25 (compare בַּיִת);

(γ) מֶ֑רִי בְּנֵי lázadók 4Móz 17:25 (vö. בַּיִת);

**31.** 

> (δ) הַתַּעֲרֻבוֺת בְּנֵי sons of pledges = hostages 2Kin 14:14 2Chr 25:24;

(δ) הַתַּעֲרֻבוֺת בְּנֵי a zálogok fiai = túszok 2Kir 14:14 2Krón 25:24;

**32.** 

> (ε) מָוֶת בְּנֵי i.e. those deserving of death 1Sam 26:16; so בֶּןמֿות 2Sam 12:5; תְמוּתָה בְּנֵי appointed or exposed to death Psa 79:11; 102:21; compare (ζ) הַכּוֺת בִּן one worthy of smiting Deut 25:2;

(ε) מָוֶת בְּנֵי, azaz akik halált érdemelnek 1Sám 26:16; így בֶּןמֿות 2Sám 12:5; תְמוּתָה בְּנֵי halálra rendeltek vagy a halálnak kitettek Zsolt 79:11; 102:21; vö. (ζ) הַכּוֺת בִּן aki verést érdemel 5Móz 25:2;

**33.** 

> (η) עֹ֑נִי בְּנֵי Prov 31:5;

(η) עֹ֑נִי בְּנֵי Péld 31:5;

**34.** 

> (θ) חֲלוֺף בְּנֵי 31:8;

(θ) חֲלוֺף בְּנֵי 31:8;

**35.** 

> (ι) שָׁאוֺן בְּנֵי Jer 48:45 = tumultuous ones; so also (= שֵׁאת) שֵׁת בְּנֵי Num 24:17 compare RV Di and others;

(ι) שָׁאוֺן בְּנֵי Jer 48:45 = zajongók; így שֵׁת בְּנֵי is (= שֵׁאת) 4Móz 24:17, vö. RV Di és mások;

**36.** 

> (κ) הַיִּצְהָר כְּנֵי Zech 4:14 i.e. anointed ones;

(κ) הַיִּצְהָר כְּנֵי Zak 4:14, azaz felkentek;

**37.** 

> (λ) בֶּןמֶֿשֶׁק Gen 15:2 son of possession, i.e. heir;

(λ) בֶּןמֶֿשֶׁק 1Móz 15:2: a birtok fia, azaz örökös;

**38.** 

> (μ) בֶּןשָֿׁ֑חַר הֵילֵל Isa 14:12 son of dawn;

(μ) בֶּןשָֿׁ֑חַר הֵילֵל Ézs 14:12: a hajnal fia;

**39.** 

> (ν) of animals שָׁ֑הַץ בְּנֵיִ i.e. proud beasts Job 28:8; 41:26;

(ν) állatokról שָׁ֑הַץ בְּנֵיִ, azaz büszke vadak Jób 28:8; 41:26;

**40.** 

> (ξ) of Jonah's gourd בִּןלַֿיְלָה Jonah 4:10 (twice in verse);

(ξ) Jónás tökéről בִּןלַֿיְלָה Jón 4:10 (a versben kétszer);

**41.** 

> (ο) of a fertile hill בֶּןשֶֿׁמֶן קֶרֶן Isa 5:1.

(ο) termékeny dombról בֶּןשֶֿׁמֶן קֶרֶן Ézs 5:1.

**42.** 

> 9 noun relative of age:

9 életkort jelölő viszonyító főnév:

**43.** 

> a. of men, שָׁנָה מֵאוֺת בֶּןהֲֿמֵשׁ נֹחַ וַיְהִי Gen 5:32; compare 7:6 71t. P; 50:26; Josh 14:7. 14:10; 24:29 (all E); Num 32:11 (J), Deut 31:2; also Judg 2:8; 1Sam 4:15; 2Sam 4:4; 19:33; 19:36; 1Chr 2:21; 23:3, 24, 27; 27:3; 2Chr 24:15; 25:5; 31:16-17, Ezra 3:8; Isa 65:20 (twice in verse); Jer 52:1; 41t. Samuel Kings Chronicles, of kings of accession; note especially (included in above) the phrase וָמָ֑עְלָה שָׁנָה עֶשְׂרִים מִבֶּן Exod 30:14; 38:26; Num 1:3 21t. Numbers 1-3 + 26:2, 4; 32:11; 1Chr 23:24, 27; 2Chr 25:5; Ezra 3:8; compare Lev 27:7; Num 8:24; 26:62; 1Chr 23:3 & without מעלה Num 8:25; 18:16; also שָׁנָה בֶּןשִֿׁשִּׁים וְעַד שׁנה עשׂרים מִבֶּן Lev 27:3 compare 27:5; 27:6; שׁנה בןחֿמשׁים ועד ומעלה שׁנה שׁלשׁים מִבֶּן Num 4:3 (twice in verse) + 12 t. Numbers 4; וּלְמַ֫עְלָה שׁנים שׁלושׁ מבּן2Chr 31:16 compare 31:17; & וּלְמָ֑טָּה שׁנה עשׂרים לְמִבֶּן 1Chr 27:23.

a. emberekről, שָׁנָה מֵאוֺת בֶּןהֲֿמֵשׁ נֹחַ וַיְהִי 1Móz 5:32; vö. 7:6, a P-ben összesen 71-szer; 50:26; Józs 14:7. 14:10; 24:29 (mind E); 4Móz 32:11 (J), 5Móz 31:2; továbbá Bír 2:8; 1Sám 4:15; 2Sám 4:4; 19:33; 19:36; 1Krón 2:21; 23:3, 24, 27; 27:3; 2Krón 24:15; 25:5; 31:16-17, Ezsd 3:8; Ézs 65:20 (a versben kétszer); Jer 52:1; Sámuel, a Királyok és a Krónikák könyveiben 41-szer a királyokról a trónra lépéskor; figyeld meg különösen (a fentiekben benne foglaltatik) a וָמָ֑עְלָה שָׁנָה עֶשְׂרִים מִבֶּן kifejezést 2Móz 30:14; 38:26; 4Móz 1:3, Mózes negyedik könyvének 1-3. fejezetében 21-szer + 26:2, 4; 32:11; 1Krón 23:24, 27; 2Krón 25:5; Ezsd 3:8; vö. 3Móz 27:7; 4Móz 8:24; 26:62; 1Krón 23:3 & מעלה nélkül 4Móz 8:25; 18:16; továbbá שָׁנָה בֶּןשִֿׁשִּׁים וְעַד שׁנה עשׂרים מִבֶּן 3Móz 27:3, vö. 27:5; 27:6; שׁנה בןחֿמשׁים ועד ומעלה שׁנה שׁלשׁים מִבֶּן 4Móz 4:3 (a versben kétszer) + Mózes negyedik könyvének 4. fejezetében 12-szer; וּלְמַ֫עְלָה שׁנים שׁלושׁ מבּן2Krón 31:16, vö. 31:17; & וּלְמָ֑טָּה שׁנה עשׂרים לְמִבֶּן 1Krón 27:23.

**44.** 

> b. of animals, (Hexateuch all P, including H) בֶּןשָֿׁנָה Exod 12:5; 29:38; Lev 9:3; 23:18-19, Num 7:17 28t. Numbers 7, 28, 29; also Micah 6:6; בֶּןשְֿׁנָתוֺ Lev 12:6; 23:12; Num 6:12, 14 12t. Numbers 7; also Ezek 46:13.Note. — בן appears perhaps abbreviated as בּ in a few compound proper names; see בִּדְקַר (= בֶּןדֿקר?), בִּשְׁלָם בִּרְשַׁע, בַּעֲנָה, בַּעֲלִיס, בִּמְהָל, בִּלְשָׁן, (so MV after Schol. Hamâsa^3ed. Freytag; Rö^de libr, hist, interpr, Arab, 20, 21; but this is very uncertain, compare Ol^§ 227 b, p. 613). — On Lag's explanation of אבי in some proper names as for אבן = בן compare Lag^BN 75 & see אבינר p. 4, etc., but this is dubious בְּנוֺ 1Chr 24:26-27, as proper name, masculine in AV RV, but render: the sons of Jaaziah his son, & the sons of Merari by Jaaziah his son, compare VB & Be Öttli.

b. állatokról (a Hexateuchban mind P, a H-t is beleértve) בֶּןשָֿׁנָה 2Móz 12:5; 29:38; 3Móz 9:3; 23:18-19, 4Móz 7:17, Mózes negyedik könyvének 7., 28., 29. fejezetében 28-szor; továbbá Mik 6:6; בֶּןשְֿׁנָתוֺ 3Móz 12:6; 23:12; 4Móz 6:12, 14, Mózes negyedik könyvének 7. fejezetében 12-szer; továbbá Ez 46:13. Megjegyzés. — a בן talán בּ alakra rövidülve jelenik meg néhány összetett tulajdonnévben; l. בִּדְקַר (= בֶּןדֿקר?), בִּשְׁלָם בִּרְשַׁע, בַּעֲנָה, בַּעֲלִיס, בִּמְהָל, בִּלְשָׁן, (így MV Schol. Hamâsa^3ed. Freytag nyomán; Rö^de libr, hist, interpr, Arab, 20, 21; de ez igen bizonytalan, vö. Ol^§ 227 b, 613. o.). — Lag azon magyarázatáról, hogy egyes tulajdonnevekben az אבי az אבן = בן helyett áll, vö. Lag^BN 75 & l. אבינר 4. o. stb., de ez kétséges בְּנוֺ 1Krón 24:26-27, tulajdonnévként, hímnemű az AV RV-ben, de így fordítandó: Jaaziás fiai, az ő fia, & Merári fiai Jaaziás, az ő fia által, vö. VB & Be Öttli.

## Fordítói döntések, amelyeket a jóváhagyás érint

### Terminológia (új, `javaslat` — még nincs az `adat/terminologia.tsv`-ben)

A brief szerint az új szakkifejezések `javaslat` jelöléssel kerülnek a terminológiába, és
a záró tételbe gyűlnek. Az első adag után a táblába **még nem írtam**: ha a prompt v4
változik, a javaslatok is változhatnak. Az első adagban használt megfeleltetések:

| Angol (forrás) | Magyar (fordítás) | Hol |
|---|---|---|
| verb / noun masculine / [masculine] | ige / hímnemű főnév / [hímnemű] | BDB-fejléc |
| absolute (állapot) / construct / suffix / prefix | status absolutus / status constructus / suffixummal / prefixummal | BDB-alaktan |
| Perfect / Imperfect / Imperative / Infinitive construct | perfectum / imperfectum / imperativus / infinitivus constructus | BDB-alaktan |
| Participle active / passive | aktív / passzív participium | BDB-alaktan |
| consecutive | consecutivummal | BDB-alaktan |
| 3 feminine singular | 3. nőnemű egyes szám | BDB-alaktan |
| accusative | tárgyeset | BDB |
| absolute (használat) | abszolút használatban | BDB |
| oratio recta [direct speech] | oratio recta [egyenes beszéd] | BDB |
| igehely utáni `+` | és máshol | a meglévő kézi 3. jelentés szerint |
| `16t.` / `c. 100 t.` | összesen 16-szor / kb. 100-szor | a kézi 2.c szerint |
| twice in verse | a versben kétszer | a kézi 3. szerint |
| read (szövegjavítás) | olv. | BDB |
| id. / ib. | ua. / ugyanott | BDB |
| compare | vö. | v4 BDB-blokk 4. |
| Late Hebrew / Old Aramaic / Sabean / Nabatean / Palmyrene / Assyrian | késői héber / óarámi / szabeus / nabateus / palmürai / asszír | v4 BDB-blokk 2. |
| marginal reading | széljegyzet | Thayer |
| under the word | a címszónál | Thayer |
| vol. ii | II. köt. | Thayer |
| which see | l. ott | v4 BDB-blokk 4. (q.v.) |
| from Homer down | Homérosztól kezdve | v2 4. |
| Xenophon, Herodotus, Plato, Aristotle, Epictetus, Isocrates, Diogenes Laërtius | Xenophón, Hérodotosz, Platón, Arisztotelész, Epiktétosz, Iszokratész, Diogenész Laertiosz | v4 alt. 7. (a brief csak négy nevet rögzít) |
| Lam (igehely) | Sir | `Konyv_normalizalo_tabla.tsv`; a meglévő kézi 3. jelentés `JSir`-t ír |

### Változatlanul hagyott sziglák és idegen elemek

A kiadás- és szerzősziglák (We, Dr, Kit, HPS, Che, Gi, Lo, Ew, Di, Co, Sm, Vrss,
Comm., Qr, Kt, MT, ᵐ5, ᵑ6, Ges^§, Sta^§, Thes, Nö^ZMG stb.), a forrásrétegek
(J, E, JE, P, D, H), a szövegkiadás-jelzetek (L, T, Tr, WH, R, G, Rec.), az A. V. és
R. V. angol idézetei és a gyakoriságjelek (`_724`, `Qal_655`) változatlanok. A H7121
arab idézetének sérült átírása (`'†or°¹n`, `†or°a¹n`) betűhíven maradt.

### A forrás hibáinak kezelése (tartalmi döntés, ellenőrzendő)

- Elírások értelem szerint fordítva: *congnate* → „rokon jelentésű”, *menationed* →
  „megemlíttetni”, *ony* → „csak”, *reckoned to three* → „neked” (H7121).
- Egybeírt latin címke szétválasztva: *Latinanima*, *Latinanimus*, *Latinex toto animo*,
  *Latincapita* → „latinul anima” stb. (G5590).
- Kóbor írásjelek elhagyva: G5590 `ἡ ψυχή;` pontosvesszője és a `; ;`; G1944
  `Wisdom 14:8>` záró `>` jele.
- A H7121 kézi 2.c és 3. jelentése a v1 stílusban, zárójeles átírással készült (pl.
  „׳ק צוֺם (kárá com)”); az új fordítás a v3/v4 kiejtés-tilalma szerint átírás nélküli.
