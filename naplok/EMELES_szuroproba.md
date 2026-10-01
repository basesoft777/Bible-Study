# F28 E5 — Szúrópróba (D49)

*Brief: `F28_EMELES_BRIEF.md` v4, 3. pont 7. lépés · generálta: `python eszkozok/emeles.py naplo_nezet …` · 2026.10.01*

**⛔ Jóváhagyásra vár.** A felhasználó szócikkenként dönt: rendben (→ `kezi`), vagy
kifogás (megjelölt pontokkal). Ha a kifogásolt arány 20% fölött van (az 5 szócikkből
legalább 2 kifogásolt), a menet megáll, és `DONTESEK.md`-tétel nyílik a promptról. A
kérdés a `DONTESEK.md` DT25 tételében.

## A minta

Az E4 (első adag utáni) 34 szócikke `opus` állapottal áll az `adat/forditasok.tsv`-ben
(11 Thayer, 23 BDB). A minta a brief szerint: 10%, de legalább 5 → **5 szócikk**,
rétegzetten (Thayer/BDB arányosan: 2 + 3), köztük legalább egy 10 000 karakternél
hosszabb forrású. Kiválasztás: `python eszkozok/emeles.py minta --seed 28`
(reprodukálható véletlen; előbb egy a 10 000 karakter fölötti háromból — G4151,
H2416, H5315 —, azután a rétegek kvótája szerint).

| Strong | Szótár | Forrás karakter | Megjegyzés |
|---|---|---|---|
| G4151 | Thayer | 23 705 | a 10 000 fölötti elem; a lista leghosszabb szócikke |
| G0282 | Thayer | 702 | terminológia-kivétel: a „Bleek on Heb.” a Zsidókhoz írt levél, nem „héb.” |
| H7585 | BDB | 3 495 | |
| H8004 | BDB | 235 | |
| H8415 | BDB | 1 966 | |

## Módszer (változatlan az első adaghoz képest)

A fordító a menet maga (Opus, `claude-opus-5-5`, subagent-eszköz nincs), helyőrzős
forrásból; javítóréteg és kapuk (az E4 során kalibrálva, l. `naplok/EMELES_naplo.md`
E4 szakasz). Mind a 39 szócikk a végleges kapukon újrafutott: 0 hiba.

## Kapueredmények

| Strong | Szótár | Forrás kar. | Fordítás kar. | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G4151 | Thayer | 23705 | 24473 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.03) | RENDBEN | RENDBEN | — | RENDBEN |
| G0282 | Thayer | 702 | 736 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | — | RENDBEN |
| H7585 | BDB | 3495 | 3665 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.05) | RENDBEN | RENDBEN | RENDBEN | RENDBEN |
| H8004 | BDB | 235 | 232 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (0.99) | RENDBEN | RENDBEN | RENDBEN | RENDBEN |
| H8415 | BDB | 1966 | 2142 | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN | RENDBEN (1.09) | RENDBEN | RENDBEN | RENDBEN | RENDBEN |

Kapuk: 1 héber–görög token · 2 igehely-számpár · 3 Károli-rövidítés · 4 formázás/zárójel · 5 terminológia · 6 hosszarány (csak jelzés) · 8 idézőjel-párok · 9 tagolás · 10 igetörzsek (BDB) · 11 könyv-egyezés.

## G4151 (Thayer, 23705 → 24473 karakter)

`forras_hash=695a977c32710cb46a25383bdabd48a095037720` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 30 forrasjelolo (forditas 34)

**1.** 

> G4151 — πνεῦμα πνεύματος, τό (πνέω), Greek writings from Aeschylus and Herodotus down; Hebrew רוּחַ, Latinspiritus; i. e.:

G4151 — πνεῦμα πνεύματος, τό (πνέω), a görög írásokban Aiszkhülosztól és Hérodotosztól kezdve; héberül רוּחַ, latinul spiritus; azaz:

**2.** 

> 1. a movement of air (gentle) blast;

1. légmozgás, (enyhe) fuvallat;

**3.** 

> a. of the wind: ἀνέμων πνεύματα, Herodotus 7, 16, 1; Pausanias, 5, 25; hence, the wind itself, Joh 3:8; plural Heb 1:7 (1Ki 18:45; 1Ki 19:11; Job 1:19; Psa 103:4, etc.; often in Greek writings).

a. a szélé: ἀνέμων πνεύματα, Hérodotosz 7, 16, 1; Pauszaniasz, 5, 25; innen maga a szél, Ján 3:8; többes számban Zsid 1:7 (1Kir 18:45; 1Kir 19:11; Jób 1:19; Zsolt 103:4 stb.; gyakran a görög írásokban).

**4.** 

> b. breath of the nostrils or mouth, often in Greek writings from Aeschylus down: πνεῦμα τοῦ στόματος, 2Th 2:8 (Psa 32:6, cf. Isa 11:4); πνεῦμα ζωῆς, the breath of life, Rev 11:11 (Gen 6:17, cf. πνοή ζωῆς, ). (πνεῦμα and πνοή seem to have been in the main coincident terms; but πνοή became the more poetic. Both retain a suggestion of their evident etymology. Even in classical Greek πνεῦμα became as frequent and as wide in its application as ἄνεμος. (Schmidt, chapter 55, 7; Trench, § lxxiii.))

b. az orr vagy a száj lehelete, gyakran a görög írásokban Aiszkhülosztól kezdve: πνεῦμα τοῦ στόματος, 2Thessz 2:8 (Zsolt 32:6, vö. Ézs 11:4); πνεῦμα ζωῆς, az élet lehelete, Jel 11:11 (1Móz 6:17, vö. πνοή ζωῆς, ). (A πνεῦμα és a πνοή úgy látszik, nagyjából egybeeső kifejezések voltak; de a πνοή lett a költőibb. Mindkettő megőrzi nyilvánvaló etimológiájának egy árnyalatát. Már a klasszikus görögben is a πνεῦμα éppolyan gyakori és éppolyan tág alkalmazású lett, mint a ἄνεμος. (Schmidt, 55. fej., 7; Trench, § lxxiii.))

**5.** 

> 2. the spirit, i. e. the vital principle by which the body is animated ((Aristotle, Polybius, Plutarch, others; see below)): Luk 8:55; Luk 23:46; Joh 19:30; Act 7:59; Rev 13:15 (here R. V. breath); ἀφιέναι τό πνεῦμα, to breathe out the spirit, to expire, Mat 27:50 cf. Sir. 38:23; Wis. 16:14 (Greek writings said ἀφιέναι τήν ψυχήν, as Gen 35:18, see ἀφίημι, 1 b. and Kypke, Observations, i, p. 140; but we also find ἀφιέναι πνεῦμα θανσίμω σφαγή, Euripides, Hec. 571); σῶμα χωρίς πνεύματος νεκρόν ἐστιν, Jam 2:26; τό πνεῦμα ἐστι τό ζοωποιουν, ἡ σάρξ οὐκ ὠφελεῖ οὐδέν, the spirit is that which animates and gives life, the body is of no profit (for the spirit imparts life to it, not the body in turn to the spirit; cf. Chr. Frid. Fritzsche, Nova opuscc., p. 239), Joh 6:63. the rational spirit, the power by which a human being feels, thinks, wills, decides; the soul: τό πνεῦμα τοῦ ἀνθρώπου τό ἐν αὐτῷ, 1Co 2:11; opposed to σάρξ (which see (especially 2 a.)), Mat 26:41; Mar 14:38; 1Co 5:5; 2Co 7:1; Col 2:5; opposed to τό σῶμα, Rom 8:10; 1Co 6:17, 1Co 6:20 Rec.; ; 1Pe 4:6. Although for the most part the words πνεῦμα and ψυχή are used indiscriminately and so σῶμα and ψυχή put in contrast (but never by Paul; see ψυχή, especially 2), there is also recognized a threefold distinction, τό πνεῦμα καί ἡ ψυχή καί τό σῶμα, 1Th 5:23, according to which τό πνεῦμα is the rational part of man, the power of perceiving and grasping divine and eternal things, and upon which the Spirit of God exerts its influence; (πνεῦμα, says Luther, "is the highest and noblest part of man, which qualifies him to lay bold of incomprehensible, invisible, eternal things; in short, it is the house where Faith and God's word are at home" (see references at end)): ἄχρι μερισμοῦ ψυχῆς καί πνεύματος (see μερισμός, 2), Heb 4:12; ἐν ἑνί πνεύματι, μία ψυχή, Phi 1:27 (where instead of μία ψυχή Paul according to his mode of speaking elsewhere would have said more appropriately μία καρδία). τό πνεῦμα τίνος, Mar 2:8; Mar 8:12; Lukei. 47; Act 17:16; Rom 1:9; Rom 8:16; 1Co 5:4; 1Co 16:18; 2Co 2:13; 2Co 7:13; Gal 6:18; (Phi 4:23 L T Tr WH); Phi 1:25; 2Ti 4:22; ὁ Θεός τῶν πνευμάτων (for which Rec. has ἁγίων) τῶν προφητῶν, who incites and directs the souls of the prophets, Rev 22:6, where cf. Düsterdieck. the dative τῷ πνεύματι is used to denote the seat (locality) where one does or suffers something, like our in spirit: ἐπιγινώσκειν, Mar 2:8; ἀναστενάζειν, Mar 8:12; ἐμβρίμασθαι, Joh 11:33; ταράσσεσθαι, Joh 13:21; ζηιν, Act 18:25; Rom 12:11; ἀγαλλίασθαι, Luk 10:21 (but L T Tr WH here add ἁγίῳ); the dative of respect: 1Co 5:3; Col 2:5; 1Pe 4:6; κραταιουσθαι, Luk 1:80; Luk 2:40 Rec.; ἅγιον εἶναι, 1Co 7:34; ζοωποιηθεις, 1Pe 3:18; ζῆν, 1Pe 4:6; πτωχοί, Mat 5:3; dative of instrument: δεδεμένος, Act 20:22; συνέχεσθαι, Rec.; Θεῷ λατρεύειν, Phi 3:3 R G; dative of advantage: ἄνεσιν τῷ πνεύματι μου, 2Co 2:13 (12); ἐν τῷ πνεύματι, is used of the instrument, 1Co 6:20 Rec. (it is surely better to take ἐν τῷ πνεύματι here locally, of the 'sphere' (Winer's Grammar, 386 (362), cf. 1Co 6:19)); also ἐν πνεύματι, nearly equivalent to πνευματικῶς (but see Winer's Grammar, § 51, 1 e. note), Joh 4:23; of the seat of an action, ἐν τῷ πνεύματι μου, Rom 1:9; τιθέναι ἐν τῷ πνεύματι, to propose to oneself, purpose in spirit, followed by the infinitive (πορεύεσθαι, Act 19:21. πνεύματα προφητῶν, according to the context the souls (spirits) of the prophets moved by the Spirit of God, 1Co 14:32; in a peculiar sense πνεῦμα is used of a soul thoroughly roused by the Holy Spirit and wholly intent on divine things, yet destitute of distinct self-consciousness and clear understanding; thus in the phrases τό πνεῦμα μου προσεύχεται, opposed to ὁ νοῦς μου, 1Co 14:14; πνεύματι λαλεῖν μυστήρια, 1Co 14:2; προσεύχεσθαι, ψάλλειν, εὐλογεῖν, τῷ πνεύματι, as opposed to τῷ νοι 3. "a spirit, i. e. a simple essence, devoid of all or at least all grosser matter, and possessed of the power of knowing, desiring, deciding, and acting";

2. a szellem, azaz az az életelv, amely a testet élteti ((Arisztotelész, Polübiosz, Plutarkhosz, mások; l. alább)): Luk 8:55; Luk 23:46; Ján 19:30; ApCsel 7:59; Jel 13:15 (itt R. V. breath); ἀφιέναι τό πνεῦμα: kilehelni a szellemet, kimúlni, Mt 27:50, vö. Sir 38:23; Bölcs 16:14 (a görög írások ἀφιέναι τήν ψυχήν-t mondtak, mint 1Móz 35:18, l. ἀφίημι, 1 b. és Kypke, Observations, i, 140. o.; de előfordul ἀφιέναι πνεῦμα θανσίμω σφαγή is, Euripidész, Hec. 571); σῶμα χωρίς πνεύματος νεκρόν ἐστιν, Jak 2:26; τό πνεῦμα ἐστι τό ζοωποιουν, ἡ σάρξ οὐκ ὠφελεῖ οὐδέν: a szellem az, ami éltet és életet ad, a test semmit sem használ (mert a szellem ad életet neki, nem pedig fordítva, a test a szellemnek; vö. Chr. Frid. Fritzsche, Nova opuscc., 239. o.), Ján 6:63. az értelmes szellem, az az erő, amellyel az ember érez, gondolkodik, akar, dönt; a lélek: τό πνεῦμα τοῦ ἀνθρώπου τό ἐν αὐτῷ, 1Kor 2:11; szemben a σάρξ-val (l. ott (különösen 2 a.)), Mt 26:41; Mk 14:38; 1Kor 5:5; 2Kor 7:1; Kol 2:5; szemben a τό σῶμα-val, Róm 8:10; 1Kor 6:17, 1Kor 6:20 Rec.; 1Pét 4:6. Bár a πνεῦμα és a ψυχή szavakat többnyire különbségtétel nélkül használják, és így a σῶμα-t és a ψυχή-t állítják szembe (de Pál soha; l. ψυχή, különösen 2), hármas megkülönböztetést is ismernek, τό πνεῦμα καί ἡ ψυχή καί τό σῶμα, 1Thessz 5:23, amely szerint a τό πνεῦμα az ember értelmes része, az isteni és örök dolgok észlelésének és megragadásának képessége, amelyre Isten Szelleme a hatását gyakorolja; (πνεῦμα, mondja Luther, „az ember legmagasabb és legnemesebb része, amely képessé teszi arra, hogy megragadja a felfoghatatlan, láthatatlan, örök dolgokat; egyszóval az a ház, ahol a hit és Isten igéje otthon van” (l. a hivatkozásokat a végén)): ἄχρι μερισμοῦ ψυχῆς καί πνεύματος (l. μερισμός, 2), Zsid 4:12; ἐν ἑνί πνεύματι, μία ψυχή, Fil 1:27 (ahol a μία ψυχή helyett Pál másutt szokásos beszédmódja szerint helyesebben μία καρδία-t mondott volna). τό πνεῦμα τίνος, Mk 2:8; Mk 8:12; Luk i. 47; ApCsel 17:16; Róm 1:9; Róm 8:16; 1Kor 5:4; 1Kor 16:18; 2Kor 2:13; 2Kor 7:13; Gal 6:18; (Fil 4:23 L T Tr WH); Fil 1:25; 2Tim 4:22; ὁ Θεός τῶν πνευμάτων (amely helyett a Rec. ἁγίων-t ad) τῶν προφητῶν, aki a próféták lelkét indítja és irányítja, Jel 22:6, ahol vö. Düsterdieck. a τῷ πνεύματι datívusz annak a székhelynek (helynek) a jelölésére szolgál, ahol valaki tesz vagy elszenved valamit, mint a mi szellemben kifejezésünk: ἐπιγινώσκειν, Mk 2:8; ἀναστενάζειν, Mk 8:12; ἐμβρίμασθαι, Ján 11:33; ταράσσεσθαι, Ján 13:21; ζηιν, ApCsel 18:25; Róm 12:11; ἀγαλλίασθαι, Luk 10:21 (de L T Tr WH itt hozzáteszi: ἁγίῳ); a vonatkozás datívusza: 1Kor 5:3; Kol 2:5; 1Pét 4:6; κραταιουσθαι, Luk 1:80; Luk 2:40 Rec.; ἅγιον εἶναι, 1Kor 7:34; ζοωποιηθεις, 1Pét 3:18; ζῆν, 1Pét 4:6; πτωχοί, Mt 5:3; az eszköz datívusza: δεδεμένος, ApCsel 20:22; συνέχεσθαι, Rec.; Θεῷ λατρεύειν, Fil 3:3 R G; az érdek datívusza: ἄνεσιν τῷ πνεύματι μου, 2Kor 2:13 (12); a ἐν τῷ πνεύματι az eszközre használatos, 1Kor 6:20 Rec. (bizonyára jobb itt a ἐν τῷ πνεύματι-t helyhatározóként venni, a 'szféra' értelmében (Winer's Grammar, 386 (362), vö. 1Kor 6:19)); továbbá ἐν πνεύματι, csaknem = πνευματικῶς (de l. Winer's Grammar, § 51, 1 e. jegyzet), Ján 4:23; a cselekvés székhelyéről, ἐν τῷ πνεύματι μου, Róm 1:9; τιθέναι ἐν τῷ πνεύματι: elhatározni magában, szellemében szándékozni, utána infinitivus (πορεύεσθαι, ApCsel 19:21. πνεύματα προφητῶν: a szövegkörnyezet szerint a prófétáknak Isten Szellemétől indított lelkei (szellemei), 1Kor 14:32; sajátos értelemben a πνεῦμα a Szent Szellemtől teljesen felindított és egészen az isteni dolgokra irányuló lélekre használatos, amely azonban nélkülözi a világos öntudatot és a tiszta értelmet; így a következő kifejezésekben: τό πνεῦμα μου προσεύχεται, szemben a ὁ νοῦς μου-val, 1Kor 14:14; πνεύματι λαλεῖν μυστήρια, 1Kor 14:2; προσεύχεσθαι, ψάλλειν, εὐλογεῖν, τῷ πνεύματι, szemben a τῷ νοι-val 3. „szellem, azaz egyszerű lényeg, amely mentes minden, vagy legalábbis minden durvább anyagtól, és rendelkezik a megismerés, a kívánás, a döntés és a cselekvés képességével”;

**6.** 

> a. generically: Luk 24:37; Act 23:8 (on which see μήτε, at the end); Act 23:9; πνεῦμα σάρκα καί ὀστέα οὐκ ἔχει, Luk 24:39; πνεῦμα ζοωποιουν (a life-giving spirit), spoken of Christ as raised from the dead, 1Co 15:45; πνεῦμα ὁ Θεός (God is spirit essentially), Joh 4:24; πατήρ τῶν πνευμάτων, of God, Heb 12:9, where the term comprises both the spirits of men and of angels.

a. általánosan: Luk 24:37; ApCsel 23:8 (ehhez l. μήτε, a végén); ApCsel 23:9; πνεῦμα σάρκα καί ὀστέα οὐκ ἔχει, Luk 24:39; πνεῦμα ζοωποιουν (megelevenítő szellem), a halottak közül feltámadt Krisztusról mondva, 1Kor 15:45; πνεῦμα ὁ Θεός (Isten lényege szerint szellem), Ján 4:24; πατήρ τῶν πνευμάτων, Istenről, Zsid 12:9, ahol a kifejezés az emberek és az angyalok szellemeit egyaránt magában foglalja.

**7.** 

> b. a human soul that has left the body ((Babrius 122, 8)): plural (Latinmanes), Heb 12:23; 1Pe 3:19.

b. a testet elhagyott emberi lélek ((Babriosz 122, 8)): többes számban (latinul manes), Zsid 12:23; 1Pét 3:19.

**8.** 

> c. a spirit higher than man but lower than God, i. e. an angel: plural Heb 1:14; used of demons, or evil spirits, who were conceived of as inhabiting the bodies of men: (Mar 9:20); Luk 9:39; Act 16:18; plural, Mat 8:16; Mat 12:45; Luk 10:20; Luk 11:26; πνεῦμα Πύθωνος or πύθωνα, Act 16:16; πνεύματα δαιμονίων, Rev 16:14; πνεῦμα δαιμονίου ἀκαθάρτου, Luk 4:33 (see δαιμόνιον, 2); πνεῦμα ἀσθενείας, causing infirmity, Luk 13:11; πνεῦμα ἀκάθαρτον, Mat 10:1; Mat 12:43; Mar 1:23, Mar 1:26, Mar 1:27; Mar 3:11, Mar 3:30; Mar 5:2, Mar 5:8, Mar 5:13; Mar 6:7; Mar 7:25; Mar 9:25; Luk 4:36; Luk 6:18; Luk 8:29; Luk 9:42; Luk 11:24, Luk 11:26; Act 5:16; Act 8:7; Rev 16:13; Rev 18:2; ἄλαλον, κωφόν (for the Jews held that the same evils with which the men were afflicted affected the demons also that bad taken possession of them (cf. Wetstein, N. T.

c. az embernél magasabb, de Istennél alacsonyabb szellem, azaz angyal: többes számban Zsid 1:14; démonokra vagy gonosz szellemekre használva, akikről úgy gondolták, hogy az emberek testében laknak: (Mk 9:20); Luk 9:39; ApCsel 16:18; többes számban, Mt 8:16; Mt 12:45; Luk 10:20; Luk 11:26; πνεῦμα Πύθωνος vagy πύθωνα, ApCsel 16:16; πνεύματα δαιμονίων, Jel 16:14; πνεῦμα δαιμονίου ἀκαθάρτου, Luk 4:33 (l. δαιμόνιον, 2); πνεῦμα ἀσθενείας, betegséget okozó, Luk 13:11; πνεῦμα ἀκάθαρτον, Mt 10:1; Mt 12:43; Mk 1:23, Mk 1:26, Mk 1:27; Mk 3:11, Mk 3:30; Mk 5:2, Mk 5:8, Mk 5:13; Mk 6:7; Mk 7:25; Mk 9:25; Luk 4:36; Luk 6:18; Luk 8:29; Luk 9:42; Luk 11:24, Luk 11:26; ApCsel 5:16; ApCsel 8:7; Jel 16:13; Jel 18:2; ἄλαλον, κωφόν (mert a zsidók úgy tartották, hogy ugyanazok a bajok, amelyek az embereket sújtották, a beléjük költözött démonokat is érintették (vö. Wetstein, N. T.

**9.** 

> i. 279ff; Edersheim, Jesus the Messiah, Appendix xvi.; see δαιμονίζομαι etc. and references)), Mar 9:17, Mar 9:25; πονηρόν, Luk 7:21; Luk 8:2; Act 19:12, Act 19:13, Act 19:15, Act 19:16, (cf. Jdg 9:23; 1Sa 16:14; 1Sa 19:9, etc.).

i. 279kk.; Edersheim, Jesus the Messiah, Appendix xvi.; l. δαιμονίζομαι stb. és a hivatkozásokat)), Mk 9:17, Mk 9:25; πονηρόν, Luk 7:21; Luk 8:2; ApCsel 19:12, ApCsel 19:13, ApCsel 19:15, ApCsel 19:16, (vö. Bír 9:23; 1Sám 16:14; 1Sám 19:9 stb.).

**10.** 

> d. "the spiritual nature of Christ, higher than the highest angels, close to God and most intimately united to him" (in doctrinal phraseology the divine nature of Christ): 1Ti 3:16; with the addition of ἁγιωσύνης (on which see ἁγιωσύνη, 1 (yet cf.

d. „Krisztus szellemi természete, amely a legmagasabb angyaloknál is magasabb, közel van Istenhez, és a legbensőségesebben egyesül vele” (a dogmatikai szóhasználatban Krisztus isteni természete): 1Tim 3:16; a ἁγιωσύνης hozzátételével (ehhez l. ἁγιωσύνη, 1 (de vö.

**11.** 

> 4 a. below)), Rom 1:4 (but see Meyer at the passage, Ellicott on 1 Timothy, the passage cited); it is called πνεῦμα αἰώνιον, in tacit contrast with the perishable ψυχαί of sacrificial animals, in Heb 9:14, where cf. Delitzsch (and especially Kurtz).

4 a. alább)), Róm 1:4 (de l. Meyer a helyhez, Ellicott az 1Tim-hez, az idézett helyhez); πνεῦμα αἰώνιον-nak nevezik, hallgatólagos szembeállításban az áldozati állatok mulandó ψυχαί-jával, a Zsid 9:14-ben, ahol vö. Delitzsch (és különösen Kurtz).

**12.** 

> 4. The Scriptures also ascribe a πνεῦμα to God, i. e. God's power and agency — distinguishable in thought (or modalistice, as they say in technical speech) from God's essence in itself considered — "manifest in the course of affairs, and by its influence upon souls productive in the theocratic body (the church) of all the higher spiritual gifts and blessings"; (cf. the resemblances and differences in Philo's use of τό θεῖον πνεῦμα, e. g. de gigant. § 12 (cf. § 5f); quis rer. div. § 53; de mund. opif. § 46, etc.).

4. Az Írás Istennek is tulajdonít πνεῦμα-t, azaz Isten erejét és munkálkodását — amely gondolatban (vagy modalistice, ahogyan a szakszerű beszédben mondják) megkülönböztethető Isten önmagában vett lényegétől —, „amely az események menetében megnyilvánul, és a lelkekre gyakorolt hatása révén a teokratikus testben (az egyházban) minden magasabb szellemi ajándékot és áldást létrehoz”; (vö. a hasonlóságokat és a különbségeket Philón τό θεῖον πνεῦμα-használatában, pl. de gigant. § 12 (vö. § 5k.); quis rer. div. § 53; de mund. opif. § 46 stb.).

**13.** 

> a. This πνεῦμα is called in the O. T. אֱלֹהִים רוּחַ, יְהוָה רוּחַ; in the N. T. πνεῦμα ἅγιον, τό ἅγιον πνεῦμα, τό πνεῦμα τό ἅγιον (first so in Wis. 1:5 Wis. 9:17; for קֹדֶשׁ רוּחַ, in Psa 50:13, Isa 63:10, Isa 63:11, the Sept. renders by πνεῦμα ἁγιωσύνης), i. e. the Holy Spirit (august, full of majesty, adorable, utterly opposed to all impurity): Mat 1:18, Mat 1:20; Mat 3:11; Mat 12:32; Mat 28:19; Mar 1:8; Mar 3:29; Mar 12:36; Mar 13:11; Luk 1:15, Luk 1:35; Luk 2:25, Luk 2:26; Luk 3:16, Luk 3:22; Luk 4:1; Luk 11:13; Luk 12:10, Luk 12:12; Joh 1:33; Joh 7:39 (L T WH omit; Tr brackets ἅγιον); Joh 14:26; Joh 20:22; Act 1:2, Act 1:5, Act 1:8, Act 1:16; Act 2:33, Act 2:38; Act 4:25 L T Tr WH; Act 5:3,32; 8:18> (L T WH omit; Tr brackets τό ἅγιον), ; Act 9:31; Act 10:38,44,45,47; 11:15,16,24; 13:2,4,9,52; 15:8,28; 16:6; 19:6; 20:28>; Rom 9:1; Rom 14:17; Rom 15:13, Rom 15:16, Rom 15:19 (L Tr WH in brackets); 1Co 6:19; 1Co 12:3; 2Co 6:6; 2Co 13:13 (14); Eph 1:13; 1Th 1:5, 1Th 1:6; 2Ti 1:14; Tit 3:5; Heb 2:4; Heb 6:4; Heb 9:8; 1Jo 5:7 Rec.; Jude 1:20; other examples will be given below in the phrases; (on the use and the omission of the article, see Fritzsche, Ep. ad Romans, ii., p. 105 (in opposition to Harless (on Eph 2:22), et al.; cf. also Meyer on Gal 5:16; Ellicott on Gal 5:5; Winers Grammar, 122 (116); Buttmann, 89 (78))); τό πνεῦμα τό ἅγιον τοῦ Θεοῦ, Eph 4:30; 1Th 4:8; πνεῦμα Θεοῦ, Rom 8:9, Rom 8:14; τό τοῦ Θεοῦ πνεῦμα, 1Pe 4:14; (τό) πνεῦμα (τοῦ) Θεοῦ, Mat 3:16; Mat 12:18, Mat 12:28; 1Co 2:14; 1Co 3:16; Eph 3:16; 1Jo 4:2; τό πνεῦμα τοῦ Θεοῦ ἡμῶν, 1Co 6:11; τό πνεῦμα τοῦ πατρός, Mat 10:20; πνεῦμα Θεοῦ ζῶντος, 2Co 3:3; τό πνεῦμα τοῦ ἐγείραντος Ἰησοῦν, Rom 8:11; τό πνεῦμα τό ἐκ Θεοῦ (emanating from God and imparted unto men), 1Co 2:12; πνεῦμα and τό πνεῦμα τοῦ κυρίου, i. e. of God, Luk 4:18; Act 5:9 (cf. Act 5:4); ; κυρίου, i. e. of Christ, 2Co 3:17, 2Co 3:18 (cf. Buttmann, 343 (295)); τό πνεῦμα Ἰησοῦ, since the same Spirit in a peculiar manner dwelt in Jesus, Act 16:7 (where Rec. omits Ἰησοῦ); Χριστοῦ, Rom 8:9; Ἰησοῦ Χριστοῦ, Phi 1:19; τό ἐν τίνι (in one's soul (not WH marginal reading)) πνεῦμα Χριστοῦ, 1Pe 1:11; τό πνεῦμα τοῦ υἱοῦ (τοῦ Θεοῦ), Gal 4:6; simply τό πνεῦμα or πνεῦμα: Mat 4:1; Mat 12:31, Mat 12:32; Mat 22:43; Mar 1:10, Mar 1:12; Luk 2:1, Luk 2:14; Joh 1:32, Joh 1:33; Joh 3:6, Joh 3:8, Joh 3:34; Joh 7:39; Act 2:4; Act 8:29; Act 10:19; Act 11:12, Act 11:28; Act 21:4; Rom 8:6, Rom 8:16, Rom 8:23, Rom 8:26, Rom 8:27; Rom 15:30; 1Co 2:4, 1Co 2:10, 1Co 2:13 (where Rec. adds ἁγίου); 1Co 12:4,7,8>; 2Co 1:22; 2Co 3:6, 2Co 3:8; 2Co 5:5; Gal 3:3, Gal 3:5, Gal 3:14; Gal 4:29; Gal 5:5, Gal 5:17, Gal 5:22, Gal 5:25; Eph 4:3; Eph 5:9 Rec.; ; Phi 2:1; 2Th 2:13; 1Ti 4:1; Jam 4:5; 1Pe 1:22 Rec.; 1Jo 3:24; 1Jo 5:6, 1Jo 5:8; Rev 22:17. Among the beneficent and very varied operations and effects ascribed to this Spirit in the N. T., the following are prominent: by it the man Jesus was begotten in the womb of the virgin Mary (Mat 1:18, Mat 1:20; Luk 1:35), and at his baptism by John it is said to have descended upon Jesus (Mat 3:16; Mar 1:10; Luk 3:22), so that he was perpetually (μένον ἐπ' αὐτόν) filled with it (Joh 1:32, Joh 1:33, cf. 3:34; Mat 12:28; Act 10:38); hence, to its prompting and aid the acts and words of Christ are traced, Mat 4:1; Mat 12:28; Mar 1:12; Luk 4:1, Luk 4:14. After Christ's resurrection it was imparted also to the apostles, Joh 20:22; Acts 2. Subsequently other followers of Christ are related to have received it through faith (Gal 3:2), or by the instrumentality of baptism (Act 2:38; 1Co 12:13) and the laying on of hands (Act 19:5, Act 19:6), although its reception was in no wise connected with baptism by any magical bond, Act 8:12, Act 8:15; Act 10:44ff. To its agency are referred all the blessings of the Christian religion, such as regeneration wrought in baptism (Joh 3:5, Joh 3:6, Joh 3:8; Tit 3:5 (but see the commentators on the passages, and references under the word βάπτισμα, 3)); all sanctification (1Co 6:11; hence, ἁγιασμός πνεύματος, 2Th 2:13; 1Pe 1:2); the power of suppressing evil desires and practising holiness (Rom 8:2ff; Gal 5:16ff,22; 1Pe 1:22 (Rec.), etc.); fortitude to undergo with patience all persecutions, losses, trials, for Christ's sake (Mat 10:20; Luk 12:11, Luk 12:12; Rom 8:26); the knowledge of evangelical truth (Joh 14:17, Joh 14:26; Joh 15:26; Joh 16:12, Joh 16:13; 1Co 2:6-16; Eph 3:5) — hence, it is called πνεῦμα τῆς ἀληθείας (John the passages cited; 1Jo 4:6), πνεῦμα σοφίας καί ἀποκαλύψεως (Eph 1:17); the sure and joyful hope of a future resurrection, and of eternal blessedness (Rom 5:5; Rom 8:11; 2Co 1:22; 2Co 5:5; Eph 1:13f); for the Holy Spirit is the seal and pledge of citizenship in the kingdom of God, 2Co 1:22; Eph 1:13. He is present to teach, guide, prompt, restrain, those Christians whose agency God employs in carrying out his counsels: Act 8:29, Act 8:39; Act 10:19; Act 11:12; Act 13:2, Act 13:4; Act 15:28; Act 16:6, Act 16:7; Act 20:28. He is the author of charisms or special gifts (1Co 12:7ff; see χάρισμα), prominent among which is the power of prophesying: τά ἐρχόμενα ἀναγγελεῖ, Joh 16:13; hence, τό πνεῦμα τῆς προφητείας (Rev 19:10); and his efficiency in the prophets is called τό πνεῦμα simply (1Th 5:19), and their utterances are introduced with these formulas: τάδε λέγει τό πνεῦμα τό ἅγιον, Act 21:11; τό πνεῦμα λέγει, 1Ti 4:1; Rev 14:13; with ταῖς ἐκκλησίαις added, Rev 2:7, Rev 2:11, Rev 2:17, Rev 2:29; Rev 3:6, Rev 3:13, Rev 3:22. Since the Holy Spirit by his inspiration was the author also of the O. T. Scriptures (2Pe 1:21; 2Ti 3:16), his utterances are cited in the following terms: λέγει or μαρτυρεῖ τό πνεῦμα τό ἅγιον, Heb 3:7; Heb 10:15; τό πνεῦμα τό ἅγιον ἐλάλησε διά Ἠσαΐου, Act 28:25, cf. Act 1:16. From among the great number of other phrases referring to the Holy Spirit the following seem to be noteworthy here: God is said διδόναι τίνι τό πνεῦμα τό ἅγιον, Luk 11:13; Act 15:8; passive, Rom 5:5; more precisely, ἐκ τοῦ πνεύματος αὐτοῦ, i. e. a portion from his Spirit's fullness (Buttmann, § 132, 7; Winer's Grammar, 366 (343)), 1Jo 4:13; or έ᾿κχειν ἀπό τοῦ πνεύματος αὐτοῦ, Act 2:17, Act 2:18 (for its entire fullness Christ alone receives, Joh 3:34); men are said, λαμβάνειν πνεῦμα ἅγιον, Joh 20:22; Act 8:15, Act 8:17, Act 8:19; Act 19:2; or τό πνεῦμα ἅγιον, Act 10:47; or τό πνεῦμα τό ἐκ Θεοῦ, 1Co 2:12; or τό πνεῦμα, Gal 3:2, cf. Rom 8:15; πνεῦμα Θεοῦ ἔχειν, 1Co 7:40; πνεῦμα μή ἔχειν, Jude 1:19; πληροῦσθαι πνεύματος ἁγίου, Act 13:52; ἐν πνεύματι, Eph 5:18; πλησθῆναι, πλησθήσεσθαι, πνεύματος ἁγίου, Luk 1:15, Luk 1:41, Luk 1:67; Act 2:4; Act 4:8, Act 4:31; Act 9:17; Act 13:9; πνεύματος ἁγίου πλήρης, Act 6:5; Act 7:55; Act 11:24; πλήρεις πνεύματος (Rec. adds ἁγίου) καί σοφίας, Act 6:3; πνεύματι and πνεύματι Θεοῦ ἄγεσθαι, to be led by the Holy Spirit, Rom 8:14; Gal 5:18; φέρεσθαι ὑπό πνεύματος ἁγίου 2Pe 1:21; the Spirit is said to dwell in the minds of Christians, Rom 8:9, Rom 8:11; 1Co 3:16; 1Co 6:19; 2Ti 1:14; Jam 4:5 (other expressions may be found under βαπτίζω, II.

a. Ezt a πνεῦμα-t az Ószövetség אֱלֹהִים רוּחַ-nak, יְהוָה רוּחַ-nak nevezi; az Újszövetség πνεῦμα ἅγιον-nak, τό ἅγιον πνεῦμα-nak, τό πνεῦμα τό ἅγιον-nak (először így a Bölcs 1:5 Bölcs 9:17-ben; a קֹדֶשׁ רוּחַ-t a Zsolt 50:13-ban, az Ézs 63:10-ben, az Ézs 63:11-ben a Septuaginta πνεῦμα ἁγιωσύνης-sal adja vissza), azaz a Szent Szellem (fenséges, méltósággal teljes, imádandó, minden tisztátalansággal teljesen ellentétes): Mt 1:18, Mt 1:20; Mt 3:11; Mt 12:32; Mt 28:19; Mk 1:8; Mk 3:29; Mk 12:36; Mk 13:11; Luk 1:15, Luk 1:35; Luk 2:25, Luk 2:26; Luk 3:16, Luk 3:22; Luk 4:1; Luk 11:13; Luk 12:10, Luk 12:12; Ján 1:33; Ján 7:39 (L T WH elhagyja; Tr szögletes zárójelbe teszi: ἅγιον); Ján 14:26; Ján 20:22; ApCsel 1:2, ApCsel 1:5, ApCsel 1:8, ApCsel 1:16; ApCsel 2:33, ApCsel 2:38; ApCsel 4:25 L T Tr WH; ApCsel 5:3,32; 8:18 (L T WH elhagyja; Tr szögletes zárójelbe teszi: τό ἅγιον), ; ApCsel 9:31; ApCsel 10:38,44,45,47; 11:15,16,24; 13:2,4,9,52; 15:8,28; 16:6; 19:6; 20:28; Róm 9:1; Róm 14:17; Róm 15:13, Róm 15:16, Róm 15:19 (L Tr WH szögletes zárójelben); 1Kor 6:19; 1Kor 12:3; 2Kor 6:6; 2Kor 13:13 (14); Ef 1:13; 1Thessz 1:5, 1Thessz 1:6; 2Tim 1:14; Tit 3:5; Zsid 2:4; Zsid 6:4; Zsid 9:8; 1Ján 5:7 Rec.; Júd 1:20; további példák alább, a kifejezéseknél következnek; (a névelő használatáról és elhagyásáról l. Fritzsche, Ep. ad Romans, ii., 105. o. (Harless-szal szemben (az Ef 2:22-höz), et al.; vö. még Meyer a Gal 5:16-hoz; Ellicott a Gal 5:5-höz; Winers Grammar, 122 (116); Buttmann, 89 (78))); τό πνεῦμα τό ἅγιον τοῦ Θεοῦ, Ef 4:30; 1Thessz 4:8; πνεῦμα Θεοῦ, Róm 8:9, Róm 8:14; τό τοῦ Θεοῦ πνεῦμα, 1Pét 4:14; (τό) πνεῦμα (τοῦ) Θεοῦ, Mt 3:16; Mt 12:18, Mt 12:28; 1Kor 2:14; 1Kor 3:16; Ef 3:16; 1Ján 4:2; τό πνεῦμα τοῦ Θεοῦ ἡμῶν, 1Kor 6:11; τό πνεῦμα τοῦ πατρός, Mt 10:20; πνεῦμα Θεοῦ ζῶντος, 2Kor 3:3; τό πνεῦμα τοῦ ἐγείραντος Ἰησοῦν, Róm 8:11; τό πνεῦμα τό ἐκ Θεοῦ (Istentől származó és az embereknek adott), 1Kor 2:12; πνεῦμα és τό πνεῦμα τοῦ κυρίου, azaz Istené, Luk 4:18; ApCsel 5:9 (vö. ApCsel 5:4); ; κυρίου, azaz Krisztusé, 2Kor 3:17, 2Kor 3:18 (vö. Buttmann, 343 (295)); τό πνεῦμα Ἰησοῦ, mivel ugyanez a Szellem sajátos módon Jézusban lakott, ApCsel 16:7 (ahol a Rec. elhagyja a Ἰησοῦ-t); Χριστοῦ, Róm 8:9; Ἰησοῦ Χριστοῦ, Fil 1:19; τό ἐν τίνι (valakinek a lelkében (nem WH széljegyzet)) πνεῦμα Χριστοῦ, 1Pét 1:11; τό πνεῦμα τοῦ υἱοῦ (τοῦ Θεοῦ), Gal 4:6; egyszerűen τό πνεῦμα vagy πνεῦμα: Mt 4:1; Mt 12:31, Mt 12:32; Mt 22:43; Mk 1:10, Mk 1:12; Luk 2:1, Luk 2:14; Ján 1:32, Ján 1:33; Ján 3:6, Ján 3:8, Ján 3:34; Ján 7:39; ApCsel 2:4; ApCsel 8:29; ApCsel 10:19; ApCsel 11:12, ApCsel 11:28; ApCsel 21:4; Róm 8:6, Róm 8:16, Róm 8:23, Róm 8:26, Róm 8:27; Róm 15:30; 1Kor 2:4, 1Kor 2:10, 1Kor 2:13 (ahol a Rec. hozzáteszi: ἁγίου); 1Kor 12:4,7,8; 2Kor 1:22; 2Kor 3:6, 2Kor 3:8; 2Kor 5:5; Gal 3:3, Gal 3:5, Gal 3:14; Gal 4:29; Gal 5:5, Gal 5:17, Gal 5:22, Gal 5:25; Ef 4:3; Ef 5:9 Rec.; Fil 2:1; 2Thessz 2:13; 1Tim 4:1; Jak 4:5; 1Pét 1:22 Rec.; 1Ján 3:24; 1Ján 5:6, 1Ján 5:8; Jel 22:17. Az Újszövetségben ennek a Szellemnek tulajdonított jótékony és igen sokféle működések és hatások közül a következők emelkednek ki: általa fogantatott az ember Jézus Mária szűz méhében (Mt 1:18, Mt 1:20; Luk 1:35), és amikor János megkeresztelte, a Szellem — mondják — leszállt Jézusra (Mt 3:16; Mk 1:10; Luk 3:22), úgyhogy állandóan (μένον ἐπ' αὐτόν) be volt vele töltve (Ján 1:32, Ján 1:33, vö. 3:34; Mt 12:28; ApCsel 10:38); ezért Krisztus tetteit és szavait az ő indíttatására és segítségére vezetik vissza, Mt 4:1; Mt 12:28; Mk 1:12; Luk 4:1, Luk 4:14. Krisztus feltámadása után az apostoloknak is megadatott, Ján 20:22; ApCsel 2. Később Krisztus más követőiről is elbeszélik, hogy hit által (Gal 3:2), vagy a keresztség eszközével (ApCsel 2:38; 1Kor 12:13) és a kézrátétellel (ApCsel 19:5, ApCsel 19:6) kapták meg, bár elnyerése semmiféle mágikus kötelékkel nem kapcsolódott a keresztséghez, ApCsel 8:12, ApCsel 8:15; ApCsel 10:44kk. Az ő munkálkodására vezetik vissza a keresztyén vallás minden áldását, így a keresztségben végbemenő újjászületést (Ján 3:5, Ján 3:6, Ján 3:8; Tit 3:5 (de l. a kommentátorokat ezekhez a helyekhez, és a hivatkozásokat a βάπτισμα címszónál, 3)); minden megszentelődést (1Kor 6:11; innen ἁγιασμός πνεύματος, 2Thessz 2:13; 1Pét 1:2); a gonosz kívánságok elfojtásának és a szentség gyakorlásának erejét (Róm 8:2kk.; Gal 5:16kk.,22; 1Pét 1:22 (Rec.) stb.); a Krisztusért elszenvedett minden üldözés, veszteség és próbatétel türelmes elhordozásának erejét (Mt 10:20; Luk 12:11, Luk 12:12; Róm 8:26); az evangéliumi igazság ismeretét (Ján 14:17, Ján 14:26; Ján 15:26; Ján 16:12, Ján 16:13; 1Kor 2:6-16; Ef 3:5) — ezért nevezik πνεῦμα τῆς ἀληθείας-nak (János az idézett helyeken; 1Ján 4:6), πνεῦμα σοφίας καί ἀποκαλύψεως-nak (Ef 1:17); a jövendő feltámadás és az örök boldogság biztos és örömteli reménységét (Róm 5:5; Róm 8:11; 2Kor 1:22; 2Kor 5:5; Ef 1:13k.); mert a Szent Szellem az Isten országában való polgárjog pecsétje és záloga, 2Kor 1:22; Ef 1:13. Jelen van, hogy tanítsa, vezesse, indítsa, visszatartsa azokat a keresztyéneket, akiknek munkálkodását Isten tanácsvégzései megvalósításában felhasználja: ApCsel 8:29, ApCsel 8:39; ApCsel 10:19; ApCsel 11:12; ApCsel 13:2, ApCsel 13:4; ApCsel 15:28; ApCsel 16:6, ApCsel 16:7; ApCsel 20:28. Ő a karizmák vagy különleges ajándékok szerzője (1Kor 12:7kk.; l. χάρισμα), amelyek közül kiemelkedik a prófétálás képessége: τά ἐρχόμενα ἀναγγελεῖ, Ján 16:13; innen τό πνεῦμα τῆς προφητείας (Jel 19:10); és a prófétákban való hatékonyságát egyszerűen τό πνεῦμα-nak nevezik (1Thessz 5:19), kijelentéseiket pedig ezekkel a formulákkal vezetik be: τάδε λέγει τό πνεῦμα τό ἅγιον, ApCsel 21:11; τό πνεῦμα λέγει, 1Tim 4:1; Jel 14:13; a ταῖς ἐκκλησίαις hozzátételével, Jel 2:7, Jel 2:11, Jel 2:17, Jel 2:29; Jel 3:6, Jel 3:13, Jel 3:22. Mivel a Szent Szellem ihletésével az ószövetségi Írások szerzője is volt (2Pét 1:21; 2Tim 3:16), kijelentéseit a következő szavakkal idézik: λέγει vagy μαρτυρεῖ τό πνεῦμα τό ἅγιον, Zsid 3:7; Zsid 10:15; τό πνεῦμα τό ἅγιον ἐλάλησε διά Ἠσαΐου, ApCsel 28:25, vö. ApCsel 1:16. A Szent Szellemre vonatkozó számos más kifejezés közül a következők látszanak itt említésre méltónak: Istenről azt mondják: διδόναι τίνι τό πνεῦμα τό ἅγιον, Luk 11:13; ApCsel 15:8; szenvedő alakban, Róm 5:5; pontosabban ἐκ τοῦ πνεύματος αὐτοῦ, azaz Szelleme teljességéből egy részt (Buttmann, § 132, 7; Winer's Grammar, 366 (343)), 1Ján 4:13; vagy έ᾿κχειν ἀπό τοῦ πνεύματος αὐτοῦ, ApCsel 2:17, ApCsel 2:18 (mert teljes teljességét egyedül Krisztus kapja, Ján 3:34); az emberekről azt mondják: λαμβάνειν πνεῦμα ἅγιον, Ján 20:22; ApCsel 8:15, ApCsel 8:17, ApCsel 8:19; ApCsel 19:2; vagy τό πνεῦμα ἅγιον, ApCsel 10:47; vagy τό πνεῦμα τό ἐκ Θεοῦ, 1Kor 2:12; vagy τό πνεῦμα, Gal 3:2, vö. Róm 8:15; πνεῦμα Θεοῦ ἔχειν, 1Kor 7:40; πνεῦμα μή ἔχειν, Júd 1:19; πληροῦσθαι πνεύματος ἁγίου, ApCsel 13:52; ἐν πνεύματι, Ef 5:18; πλησθῆναι, πλησθήσεσθαι, πνεύματος ἁγίου, Luk 1:15, Luk 1:41, Luk 1:67; ApCsel 2:4; ApCsel 4:8, ApCsel 4:31; ApCsel 9:17; ApCsel 13:9; πνεύματος ἁγίου πλήρης, ApCsel 6:5; ApCsel 7:55; ApCsel 11:24; πλήρεις πνεύματος (a Rec. hozzáteszi: ἁγίου) καί σοφίας, ApCsel 6:3; πνεύματι és πνεύματι Θεοῦ ἄγεσθαι: a Szent Szellemtől vezettetni, Róm 8:14; Gal 5:18; φέρεσθαι ὑπό πνεύματος ἁγίου 2Pét 1:21; a Szellemről azt mondják, hogy a keresztyének elméjében lakik, Róm 8:9, Róm 8:11; 1Kor 3:16; 1Kor 6:19; 2Tim 1:14; Jak 4:5 (más kifejezések találhatók a βαπτίζω alatt, II.

**14.** 

> b. bb.; γεννάω, 1 at the end and 2 d.; ἐκχέω b.; χρίω, a.); γίνεσθαι ἐν πνεύματι, to come to be in the Spirit, under the power of the Spirit, i. e. in a state of inspiration or ecstasy, Rev 1:10; Rev 4:2. Dative πνεύματι, by the power and aid of the Spirit, the Spirit prompting, Rom 8:13; Gal 5:5; τῷ πνεύματι τῷ ἁγίῳ, Luk 10:21 L Tr WH; πνεύματι ἁγίῳ, 1Pe 1:12 (where R G T have ἐν πνεύματι ἁγίῳ); πνεύματι Θεοῦ, Phi 3:3 L T Tr WH; also ἐν πνεύματι, Eph 2:22; Eph 3:5 (where ἐν πνεύματι must be joined to ἀπεκαλύφθη); ἐν πνεύματι, in the power of the Spirit, possessed and moved by the Spirit, Mat 22:43; Rev 17:3; Rev 21:10; also ἐν τῷ πνεύματι, Luk 2:27; Luk 4:1; ἐν τῷ πνεύματι ἁγίῳ, Luk 10:21 Tdf.; ἐν τῇ δυνάμει τοῦ πνευματου, Luk 4:14; ἐν τῷ πνεύματι τῷ ἁγίῳ εἰπεῖν, Mar 12:36; ἐν πνεύματι (ἁγίῳ) προσεύχεσθαι, Eph 6:18; Jude 1:20; ἐν πνεύματι Θεοῦ λαλεῖν, 1Co 12:3; ἀγάπη ἐν πνεύματι, love which the Spirit begets, Col 1:8; περιτομή ἐν πνεύματι, effected by the Holy Spirit, opposed to γράμματι, the prescription of the written law, Rom 2:29; τύπος γίνου τῶν πιστῶν ἐν πνεῦμα, in the way in which you are governed by the Spirit, 1Ti 4:12 Rec.; (ἐν ἑνί πνεύματι, Eph 2:18); ἡ ἑνότης τοῦ πνεύματος, effected by the Spirit, Eph 4:3; καινότης τοῦ πνευματου, Rom 7:6. τό πνεῦμα is opposed to ἡ σάρξ i. e. human nature left to itself and without the controlling influence of God's Spirit, subject to error and sin, Gal 5:17, Gal 5:19, Gal 5:22; (); Rom 8:6; so in the phrases περιπατεῖν κατά πνεῦμα (opposed to κατά σάρκα), Rom 8:1 Rec., 4; οἱ κατά πνεῦμα namely, ὄντες (opposed to οἱ κατά σάρκα ὄντες), those who bear the nature of the Spirit (i. e. οἱ πνευματικοί), Rom 8:5; ἐν πνεύματι εἶναι (opposed to ἐν σαρκί), to be under the power of the Spirit, to be guided by the Spirit, Rom 8:9; πνεύματι (dative of 'norm'; (cf. Buttmann, § 133, 22 b.; Winer's Grammar, 219 (205))) περιπατεῖν (opposed to ἐπιθυμίαν σαρκός τέλειν), Gal 5:16. The Holy Spirit is a δύναμις, and is expressly so called in Luk 24:49, and δύναμις ὑπιστου, Luk 1:35; but we find also πνεῦμα (or πνεῦμα ἅγιον) καί δύναμις, Act 10:38; 1Co 2:4; and ἡ δύναμις τοῦ πνεύματος, Luk 4:14, where πνεῦμα is regarded as the essence, and δύναμις its efficacy; but in 1Th 1:5 ἐν πνεύματι ἁγίῳ is epexegetical of ἐν δυνάμει. In some passages the Holy Spirit is rhetorically represented as a Person ((cf. references below)): Mat 28:19; Joh 14:16f, 26; Joh 15:26; Joh 16:13-15 (in which passages from John the personification was suggested by the fact that the Holy Spirit was about to assume with the apostles the place of a person, namely of Christ); τό πνεῦμα, καθώς βούλεται, 1Co 12:11; what anyone through the help of the Holy Spirit has come to understand or decide upon is said to have been spoken to him by the Holy Spirit: εἶπε τό πνεῦμα τίνι, Act 8:29; Act 10:19; Act 11:12; Act 13:4; τό πνεῦμα τό ἅγιον διαμαρτύρεταί μοι, Act 20:23. τό πνεῦμα τό ἅγιον ἔθετο ἐπισκόπους, i. e. not only rendered them fit to discharge the office of bishop, but also exercised such an influence in their election (Act 14:23) that none except fit persons were chosen to the office, Act 20:28; τό πνεῦμα ὑπερεντυγχάνει στεναγμοῖς ἀλαλήτοις in Rom 8:26 means, as the whole context shows, nothing other than this: 'although we have no very definite conception of what we desire (τί προσευξώμεθα), and cannot state it in fit language (καθό δεῖ) in our prayer but only disclose it by inarticulate groanings, yet God receives these groanings as acceptable prayers inasmuch as they come from a soul full of the Holy Spirit.' Those who strive against the sanctifying impulses of the Holy Spirit are said ἀντιπίπτειν τῷ πνεύματι τῷ ἁγίῳ, Act 7:51; ἐνυβρίζειν τό πνεῦμα τῆς χάριτος, Heb 10:29. πειράζειν τό πνεῦμα τοῦ κυρίου is applied to those who by falsehood would discover whether men full of the Holy Spirit can be deceived, Act 5:9; by anthropopathism those who disregard decency in their speech are said λύπειν τό πνεῦμα τό ἅγιον, since by that they are taught how they ought to talk, Eph 4:30 (παροξύνειν τό πνεῦμα, Isa 63:10; παραπικραίνειν, Psa 105:33). Cf. Grimm, Institutio theologiae dogmaticae, § 131; (Weiss, Biblical Theol. § 155 (and Index under the phrase, 'Geist Gottes,' 'Spirit of God') Kahnis, Lehre vom Heil. Geiste; Fritzsche, Nova opuscc. acad., p. 278ff; B. D. under the word Spirit the Holy; Swete in Dict. of Christ. Biog. under the phrase, Holy Ghost).

b. bb.; γεννάω, 1 a végén és 2 d.; ἐκχέω b.; χρίω, a.); γίνεσθαι ἐν πνεύματι: a Szellemben lenni, a Szellem hatalma alá kerülni, azaz ihletett vagy elragadtatott állapotba, Jel 1:10; Jel 4:2. A πνεύματι datívusz: a Szellem ereje és segítsége által, a Szellem indítására, Róm 8:13; Gal 5:5; τῷ πνεύματι τῷ ἁγίῳ, Luk 10:21 L Tr WH; πνεύματι ἁγίῳ, 1Pét 1:12 (ahol R G T ἐν πνεύματι ἁγίῳ-t ad); πνεύματι Θεοῦ, Fil 3:3 L T Tr WH; továbbá ἐν πνεύματι, Ef 2:22; Ef 3:5 (ahol az ἐν πνεύματι a ἀπεκαλύφθη-hoz kapcsolandó); ἐν πνεύματι: a Szellem erejében, a Szellemtől megragadva és indítva, Mt 22:43; Jel 17:3; Jel 21:10; továbbá ἐν τῷ πνεύματι, Luk 2:27; Luk 4:1; ἐν τῷ πνεύματι ἁγίῳ, Luk 10:21 Tdf.; ἐν τῇ δυνάμει τοῦ πνευματου, Luk 4:14; ἐν τῷ πνεύματι τῷ ἁγίῳ εἰπεῖν, Mk 12:36; ἐν πνεύματι (ἁγίῳ) προσεύχεσθαι, Ef 6:18; Júd 1:20; ἐν πνεύματι Θεοῦ λαλεῖν, 1Kor 12:3; ἀγάπη ἐν πνεύματι: szeretet, amelyet a Szellem szül, Kol 1:8; περιτομή ἐν πνεύματι: a Szent Szellem által végzett, szemben a γράμματι-val, az írott törvény előírásával, Róm 2:29; τύπος γίνου τῶν πιστῶν ἐν πνεῦμα: abban a módban, ahogyan a Szellem vezérel titeket, 1Tim 4:12 Rec.; (ἐν ἑνί πνεύματι, Ef 2:18); ἡ ἑνότης τοῦ πνεύματος: a Szellem által létrehozott, Ef 4:3; καινότης τοῦ πνευματου, Róm 7:6. A τό πνεῦμα szemben áll a ἡ σάρξ-val, azaz a magára hagyott, Isten Szellemének irányító befolyása nélküli, tévedésnek és bűnnek alávetett emberi természettel, Gal 5:17, Gal 5:19, Gal 5:22; (); Róm 8:6; így a következő kifejezésekben: περιπατεῖν κατά πνεῦμα (szemben a κατά σάρκα-val), Róm 8:1 Rec., 4; οἱ κατά πνεῦμα ti. ὄντες (szemben a οἱ κατά σάρκα ὄντες-val): akik a Szellem természetét hordozzák (azaz οἱ πνευματικοί), Róm 8:5; ἐν πνεύματι εἶναι (szemben a ἐν σαρκί-val): a Szellem hatalma alatt lenni, a Szellemtől vezettetni, Róm 8:9; πνεύματι (a 'norma' datívusza; (vö. Buttmann, § 133, 22 b.; Winer's Grammar, 219 (205))) περιπατεῖν (szemben a ἐπιθυμίαν σαρκός τέλειν-val), Gal 5:16. A Szent Szellem δύναμις, és így is nevezik kifejezetten a Luk 24:49-ben, és δύναμις ὑπιστου, Luk 1:35; de előfordul πνεῦμα (vagy πνεῦμα ἅγιον) καί δύναμις is, ApCsel 10:38; 1Kor 2:4; és ἡ δύναμις τοῦ πνεύματος, Luk 4:14, ahol a πνεῦμα a lényeg, a δύναμις pedig annak hatékonysága; de az 1Thessz 1:5-ben a ἐν πνεύματι ἁγίῳ a ἐν δυνάμει magyarázó kiegészítése. Néhány helyen a Szent Szellem retorikailag személyként jelenik meg ((vö. a hivatkozásokat alább)): Mt 28:19; Ján 14:16k., 26; Ján 15:26; Ján 16:13-15 (János e helyein a megszemélyesítést az indokolta, hogy a Szent Szellem az apostoloknál egy személynek, ti. Krisztusnak a helyét készült elfoglalni); τό πνεῦμα, καθώς βούλεται, 1Kor 12:11; amit valaki a Szent Szellem segítségével megértett vagy elhatározott, arról azt mondják, hogy a Szent Szellem mondta neki: εἶπε τό πνεῦμα τίνι, ApCsel 8:29; ApCsel 10:19; ApCsel 11:12; ApCsel 13:4; τό πνεῦμα τό ἅγιον διαμαρτύρεταί μοι, ApCsel 20:23. τό πνεῦμα τό ἅγιον ἔθετο ἐπισκόπους, azaz nemcsak alkalmassá tette őket a püspöki tisztség betöltésére, hanem megválasztásukra (ApCsel 14:23) is olyan befolyást gyakorolt, hogy csak alkalmas személyeket választottak a tisztségre, ApCsel 20:28; a τό πνεῦμα ὑπερεντυγχάνει στεναγμοῖς ἀλαλήτοις a Róm 8:26-ban, amint az egész szövegkörnyezet mutatja, semmi mást nem jelent, mint ezt: 'bár nincs egészen határozott fogalmunk arról, mit kívánunk (τί προσευξώμεθα), és imádságunkban nem tudjuk megfelelő nyelven kifejezni (καθό δεῖ), hanem csak artikulálatlan sóhajtásokkal tárjuk fel, Isten mégis kedves imádságként fogadja ezeket a sóhajtásokat, mivel a Szent Szellemmel teljes lélekből jönnek.' Akik a Szent Szellem megszentelő indításai ellen küzdenek, azokról azt mondják: ἀντιπίπτειν τῷ πνεύματι τῷ ἁγίῳ, ApCsel 7:51; ἐνυβρίζειν τό πνεῦμα τῆς χάριτος, Zsid 10:29. A πειράζειν τό πνεῦμα τοῦ κυρίου azokra vonatkozik, akik hazugsággal akarják kipuhatolni, meg lehet-e téveszteni a Szent Szellemmel teljes embereket, ApCsel 5:9; antropopatikusan azokról, akik beszédükben nem ügyelnek az illendőségre, azt mondják: λύπειν τό πνεῦμα τό ἅγιον, mivel általa tanulják meg, hogyan kell beszélniük, Ef 4:30 (παροξύνειν τό πνεῦμα, Ézs 63:10; παραπικραίνειν, Zsolt 105:33). Vö. Grimm, Institutio theologiae dogmaticae, § 131; (Weiss, Biblical Theol. § 155 (és a mutató a 'Geist Gottes,' 'Spirit of God' kifejezésnél) Kahnis, Lehre vom Heil. Geiste; Fritzsche, Nova opuscc. acad., 278kk. o.; B. D. a Spirit the Holy címszónál; Swete in Dict. of Christ. Biog. a Holy Ghost kifejezésnél).

**15.** 

> b. τά ἑπτά πνεύματα τοῦ Θεοῦ, Rev. ( (where Rec.st omit ἁπτα)); Rev 4:5; Rev 5:6 (here L omits; WH brackets ἑπτά), which are said to be ἐνώπιον τοῦ θρόνου τοῦ Θεοῦ (Rev 1:4) are not seven angels, but one and the same divine Spirit manifesting itself in seven energies or operations (which are rhetorically personified, Zec 3:9; Zec 4:6, Zec 4:10); cf. Düsterdieck on Rev 1:4; (Trench, Epistles to the Seven Churches, edition 3, p. 7f).

b. τά ἑπτά πνεύματα τοῦ Θεοῦ, Jel. ( (ahol a Rec.st elhagyja a ἁπτα-t)); Jel 4:5; Jel 5:6 (itt L elhagyja; WH szögletes zárójelbe teszi: ἑπτά), amelyekről azt mondják, hogy ἐνώπιον τοῦ θρόνου τοῦ Θεοῦ (Jel 1:4), nem hét angyal, hanem egy és ugyanaz az isteni Szellem, amely hét erőben vagy működésben nyilvánul meg (ezek retorikailag meg vannak személyesítve, Zak 3:9; Zak 4:6, Zak 4:10); vö. Düsterdieck a Jel 1:4-hez; (Trench, Epistles to the Seven Churches, 3. kiadás, 7k. o.).

**16.** 

> c. by metonymy, πενυμα is used of α. "one in whom a spirit (πνεῦμα) is manifest or embodied; hence, equivalent to actuated by a spirit, whether divine or demoniacal; one who either is truly moved by God's Spirit or falsely boasts that he is": 2Th 2:2; 1Jo 4:2, 1Jo 4:3; hence, διακρίσεις πνευμάτων, 1Co 12:10; μή παντί πνεύματι πιστεύετε, 1Jo 4:1; δοκιμάζετε τά πνεύματα, εἰ ἐκ τοῦ Θεοῦ ἐστιν, ibid.; πνεύματα πλανᾷ joined with διδασκαλιαι δαιμονίων, 1Ti 4:1. But in the truest and highest sense it is said κύριος τό πνεῦμα ἐστιν, he in whom the entire fullness of the Spirit dwells, and from whom that fullness is diffused through the body of Christian believers, 2Co 3:17. β. the plural πνεύματα denotes the various modes and gifts by which the Holy Spirit shows itself operative in those in whom it dwells (such as τό πνεῦμα τῆς προφητείας, τῆς σοφίας, etc.), 1Co 14:12.

c. metonímiával a πενυμα a α-re használatos. „akiben egy szellem (πνεῦμα) megnyilvánul vagy megtestesül; innen = egy szellemtől indított, akár isteni, akár démoni szellemtől; aki vagy valóban Isten Szellemétől indíttatik, vagy hamisan dicsekszik azzal, hogy attól indíttatik”: 2Thessz 2:2; 1Ján 4:2, 1Ján 4:3; innen διακρίσεις πνευμάτων, 1Kor 12:10; μή παντί πνεύματι πιστεύετε, 1Ján 4:1; δοκιμάζετε τά πνεύματα, εἰ ἐκ τοῦ Θεοῦ ἐστιν, uo.; πνεύματα πλανᾷ a διδασκαλιαι δαιμονίων-val összekapcsolva, 1Tim 4:1. De a legigazabb és legmagasabb értelemben mondják: κύριος τό πνεῦμα ἐστιν, ő, akiben a Szellem egész teljessége lakozik, és akiből ez a teljesség a keresztyén hívők testére kiárad, 2Kor 3:17. β. a πνεύματα többes szám azokat a különféle módokat és ajándékokat jelöli, amelyekben a Szent Szellem hatékonynak mutatkozik azokban, akikben lakozik (mint τό πνεῦμα τῆς προφητείας, τῆς σοφίας stb.), 1Kor 14:12.

**17.** 

> 5. universally, "the disposition or influence which fills and governs the soul of anyone; the efficient source of any power, affection, emotion, desire," etc.: τῷ αὐτῷ πνεύματι περιεπατήσαμεν, 2Co 12:18; ἐν πνεύματι ἡλίου, in the same spirit with which Elijah was filled of old, Luk 1:17; τά ῤήματα... πνεῦμα ἐστιν, exhale a spirit (and fill believers with it), Joh 6:63; οἵου πνεύματος ἐστε ὑμεῖς (what manner of spirit ye are of) viz. a divine spirit, that I have imparted unto you, Luk 9:55 (Rec.; (cf. B. § 132, 11 I.; Winer's Grammar, § 30, 5)); τῷ πνεύματι, ᾧ ἐλάλει, Act 6:10, where see Meyer; πραυ καί ἡσύχιον πνεῦμα, 1Pe 3:4; πνεῦμα πρᾳότητος, such as belongs to the meek, 1Co 4:21; Gal 6:1; τό πνεῦμα τῆς προφητείας, such as characterizes prophecy and by which the prophets are governed, Rev 19:10; τῆς ἀληθείας, σοφίας καί ἀποκαλύψεως, see above, p. 521b middle (Isa 11:2; Deu 34:9; Wis. 7:7); τῆς πίστεως, 2Co 4:13; τῆς υἱοθεσίας, such as belongs to sons, Rom 8:15; τῆς ζωῆς ἐν Χριστῷ, of the life which one gets in fellowship with Christ, ibid. 2; δυνάμεως καί ἀγάπης καί σωφρονισμοῦ, 2Ti 1:7; ἕν πνεῦμα εἶναι with Christ, equivalent to to be filled with the same spirit as Christ and by the bond of that spirit to be intimately united to Christ, 1Co 6:17; ἐν ἑνί πνεύματι, by the reception of one Spirit's efficency, 1Co 12:13; εἰς ἕν πνεῦμα, so as to be united into one body filled with one Spirit, ibid. R G; ἕν πνεῦμα ποτίζεσθαι (made to drink of i. e.) imbued with one Spirit, ibid. L T Tr WH (see ποτίζω); ἕν σῶμα καί ἐν πνεῦμα, one (social) body filled and animated by one spirit, Eph 4:4; — in all these passages although the language is general, yet it is clear from the context that the writer means a spirit begotten of the Holy Spirit or even identical with that Spirit ((cf. Clement of Rome, 1 Cor. 46, 6 [ET]; Hermas, sim. 9, 13, 18 [ET]; Ignatius ad Magn. 7 [ET])). In opposition to the divine Spirit stand, τό πνεῦμα τό ἐνεργουν ἐν τοῖς υἱοῖς τῆς ἀπειθείας (a spirit) that comes from the devil), Eph 2:2; also τό πνεῦμα τοῦ κόσμου, the spirit that actuates the unholy multitude, 1Co 2:12; δουλείας, such as characterizes and governs slaves, Rom 8:15; κατανύξεως, Rom 11:8; δειλίας, 2Ti 1:7; τῆς πλάνης, 1Jo 4:6 (πλανήσεως, Isa 19:14; πορνείας, Hos 4:12; Hos 5:4); τό τοῦ ἀντιχρίστου namely, πνεῦμα, 1Jo 4:3; ἕτερον πνεῦμα λαμβάνειν, i. e. different from the Holy Spirit, 2Co 11:4; τό πνεῦμα τοῦ νως, the governing spirit of the mind, Eph 4:23. Cf. Ackermann, Beiträge zur theol. Würdigung u. Abwägung der Begriffe πνεῦμα, νοῦς, u. Geist, in the Theol. Studien und Kritiken for 1839, p. 873ff; Büchsenschütz, La doctrine de l'Esprit de Dieu selon l'aneien et nouveau testament. Strasb. 1840; Chr. From Fritzsche, De Spiritu Sancto commentatio exegetica et dogmatica, 4 Pts. Hal. 1840f, included in his Nova opuscula academica (Turici, 1846), p. 233ff; Kahnis, Die Lehre v. hiel. Geist. Part i. (Halle, 1847); an anonymous publication (by Prince Ludwig Solms Lich, entitled) Die biblische Bedeutung des Wortes Geist. (Giessen, 1862); H. H. Wendt, Die Begriffe Fleisch u. Geist im Biblical Sprachgebrauch. (Gotha, 1878); (Cremer, in Herzog edition 2, under the phrase, Geist des Menschen; G. L. Hahn, Theol.

5. egyetemesen: „az a beállítottság vagy befolyás, amely valakinek a lelkét betölti és irányítja; bármely erő, vonzalom, érzelem, vágy stb. hatékony forrása”: τῷ αὐτῷ πνεύματι περιεπατήσαμεν, 2Kor 12:18; ἐν πνεύματι ἡλίου: abban a szellemben, amellyel Illés hajdan be volt töltve, Luk 1:17; τά ῤήματα... πνεῦμα ἐστιν: szellemet árasztanak (és betöltik vele a hívőket), Ján 6:63; οἵου πνεύματος ἐστε ὑμεῖς (milyen szellemből valók vagytok), ti. isteni szellem, amelyet én adtam nektek, Luk 9:55 (Rec.; (vö. B. § 132, 11 I.; Winer's Grammar, § 30, 5)); τῷ πνεύματι, ᾧ ἐλάλει, ApCsel 6:10, ahol l. Meyer; πραυ καί ἡσύχιον πνεῦμα, 1Pét 3:4; πνεῦμα πρᾳότητος: amilyen a szelídeké, 1Kor 4:21; Gal 6:1; τό πνεῦμα τῆς προφητείας: amilyen a próféciát jellemzi, és amely a prófétákat vezérli, Jel 19:10; τῆς ἀληθείας, σοφίας καί ἀποκαλύψεως, l. fent, 521b. o. közepe (Ézs 11:2; 5Móz 34:9; Bölcs 7:7); τῆς πίστεως, 2Kor 4:13; τῆς υἱοθεσίας: amilyen a fiakhoz illik, Róm 8:15; τῆς ζωῆς ἐν Χριστῷ: arról az életről, amelyet az ember a Krisztussal való közösségben kap, uo. 2; δυνάμεως καί ἀγάπης καί σωφρονισμοῦ, 2Tim 1:7; ἕν πνεῦμα εἶναι Krisztussal: = ugyanazzal a szellemmel betöltetni, mint Krisztus, és e szellem köteléke által bensőségesen egyesülni Krisztussal, 1Kor 6:17; ἐν ἑνί πνεύματι: egy Szellem hatékonyságának elnyerése által, 1Kor 12:13; εἰς ἕν πνεῦμα: úgy, hogy egy Szellemmel betöltött egy testté egyesüljenek, uo. R G; ἕν πνεῦμα ποτίζεσθαι (azaz itattattunk) egy Szellemmel átitatva, uo. L T Tr WH (l. ποτίζω); ἕν σῶμα καί ἐν πνεῦμα: egy (közösségi) test, amelyet egy szellem tölt be és éltet, Ef 4:4; — mindezeken a helyeken, bár a nyelvezet általános, a szövegkörnyezetből mégis világos, hogy az író a Szent Szellemtől született, vagy akár azzal a Szellemmel azonos szellemet ért ((vö. Római Kelemen, 1Kor. 46, 6 [ET]; Hermász, sim. 9, 13, 18 [ET]; Ignatiosz ad Magn. 7 [ET])). Az isteni Szellemmel szemben áll τό πνεῦμα τό ἐνεργουν ἐν τοῖς υἱοῖς τῆς ἀπειθείας (egy szellem) amely az ördögtől jön), Ef 2:2; továbbá τό πνεῦμα τοῦ κόσμου: az a szellem, amely a szentségtelen sokaságot mozgatja, 1Kor 2:12; δουλείας: amilyen a rabszolgákat jellemzi és irányítja, Róm 8:15; κατανύξεως, Róm 11:8; δειλίας, 2Tim 1:7; τῆς πλάνης, 1Ján 4:6 (πλανήσεως, Ézs 19:14; πορνείας, Hós 4:12; Hós 5:4); τό τοῦ ἀντιχρίστου ti. πνεῦμα, 1Ján 4:3; ἕτερον πνεῦμα λαμβάνειν, azaz a Szent Szellemtől különböző, 2Kor 11:4; τό πνεῦμα τοῦ νως: az elme irányító szelleme, Ef 4:23. Vö. Ackermann, Beiträge zur theol. Würdigung u. Abwägung der Begriffe πνεῦμα, νοῦς, u. Geist, a Theol. Studien und Kritiken 1839-es évfolyamában, 873kk. o.; Büchsenschütz, La doctrine de l'Esprit de Dieu selon l'aneien et nouveau testament. Strasb. 1840; Chr. From Fritzsche, De Spiritu Sancto commentatio exegetica et dogmatica, 4 Pts. Hal. 1840k., megjelent a Nova opuscula academica című kötetében (Turici, 1846), 233kk. o.; Kahnis, Die Lehre v. hiel. Geist. Part i. (Halle, 1847); egy névtelen kiadvány (Ludwig Solms Lich hercegtől, címe) Die biblische Bedeutung des Wortes Geist. (Giessen, 1862); H. H. Wendt, Die Begriffe Fleisch u. Geist im Biblical Sprachgebrauch. (Gotha, 1878); (Cremer, in Herzog 2. kiadás, a Geist des Menschen kifejezésnél; G. L. Hahn, Theol.

**18.** 

> d. N. Test.

d. N. Test.

**19.** 

> i. § 149ff; J. Laidlaw, The Bible Doctrine of Man. (Cunningham Lects., 7th Series, 1880); Dickson, St. Paul's use of the terms Flesh and Spirit. (Glasgow, 1883); and references in B. D. (especially Amos edition) and Dict. of Christ. Biog., as above, 4 a. at the end.)

i. § 149kk.; J. Laidlaw, The Bible Doctrine of Man. (Cunningham Lects., 7th Series, 1880); Dickson, St. Paul's use of the terms Flesh and Spirit. (Glasgow, 1883); és a hivatkozások a B. D.-ben (különösen az amerikai kiadásban) és a Dict. of Christ. Biog.-ban, mint fent, 4 a. a végén.)

## G0282 (Thayer, 702 → 736 karakter)

`forras_hash=bda0a77cb9ba8c8e4b52618b1f8031d43cc4c61c` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 6 forrasjelolo (forditas 9)

**1.** 

> G282 — ἀμήτωρ (ορος, ὁ, ἡ (μήτηρ), without a mother, motherless; in Greek writings:

G282 — ἀμήτωρ (ορος, ὁ, ἡ (μήτηρ), anya nélküli, anyátlan; a görög írásokban:

**2.** 

> 1. born without a mother, e. g. Minerva, Euripides, Phoen. 666f, others; God himself, inasmuch as he is without origin, Lactantius, instt. 4, 13, 2.

1. anya nélkül született, pl. Minerva, Euripidész, Phoen. 666k., mások; maga Isten, amennyiben nincs eredete, Lactantius, instt. 4, 13, 2.

**3.** 

> 2. bereft of a mother, Herodotus 4, 154, elsewhere.

2. anyjától megfosztott, Hérodotosz 4, 154, másutt.

**4.** 

> 3. born of a base or unknown mother, Euripides, Ion 109 cf. 837.

3. alacsony sorú vagy ismeretlen anyától született, Euripidész, Ion 109, vö. 837.

**5.** 

> 4. unmotherly, unworthy of the name of mother: μήτηρ ἀμήτωρ, Sophocles El. 1154. Cf. Bleek on Heb. vol. ii., 2, p. 305ff 5. in a significance unused by the Greeks, 'whose mother is not recorded in the genealogy': of Melchizedek, Heb 7:3; (of Sarah by Philo in de temul. § 14, and rer. div. haer. § 12; (cf. Bleek as above)); cf. the classic ἀνολυμπιάς.

4. anyához nem illő, az anya névre méltatlan: μήτηρ ἀμήτωρ, Szophoklész, El. 1154. Vö. Bleek a Zsidókhoz írt levélhez, II. köt., 2, 305kk. o. 5. a görögöktől nem használt jelentésben: 'akinek az anyja nincs feljegyezve a nemzetségtáblázatban': Melkisédekről, Zsid 7:3; (Sáráról Philónnál, de temul. 14. §, és rer. div. haer. 12. §; (vö. Bleek, mint fent)); vö. a klasszikus ἀνολυμπιάς.

## H7585 (BDB, 3495 → 3665 karakter)

`forras_hash=0d933c6e4e758d8c3592128ace88502104c94a4f` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 9 forrasjelolo (forditas 9)

Törzskapu: RENDBEN · 

**1.** 

> H7585. sheol שְׁאָ֫לָה Isa 7:11 see שְׁאוֺל 1 below שְׁאֹל שְׁאוֺל, noun feminine^Psa 86:13 (apparently masculine Job 26:6 compare Isa 14:9, see Albr^ZAW xvi(1896), 51) She®°ôl, underworld (√ dubious; שׁאל, i.e. palce of inquiry (reference to necromancy) Jastr^Amos. Jsem. Lang. xiv. 170. cf JBL xix (1900), 88 ff. (Jerem^Lebenn.

H7585. sheol שְׁאָ֫לָה Ézs 7:11, l. שְׁאוֺל 1, a שְׁאֹל שְׁאוֺל alatt, nőnemű főnév^Zsolt 86:13 (láthatóan hímnemű Jób 26:6, vö. Ézs 14:9, l. Albr^ZAW xvi(1896), 51) She®°ôl, alvilág (a √ kétséges; שׁאל, azaz a tudakozódás helye (utalás a halottidézésre) Jastr^Amos. Jsem. Lang. xiv. 170. vö. JBL xix (1900), 88 kk. (Jerem^Lebenn.

**2.** 

> d. Tode 109 'Ort der Entscheidung'); Thes Bö^De Inf. § 158 Di and others compare √ שׁעל, whence שֹׁעַל hallow hand, etc.; ׳שׁ then = hallow place, 'Hölle', hell; other conjectures see Hup^Ps. 6 6 De^5:14 Beer^Bibl. Hades in Holtzmann^Festgabe,1902, 15; most now refrain from positive etymology (e.g. Buhl); Old Aramaic שאול, Syriac ; Assyrian šu-alu is dubious: so reads and interprets Dl^pa 121, Prol.47. 145 Jastr^Amos. J. Semitic Lang. xiv. 165 ff. Ency. Bib^s.v.; opposed to by Bertin^TSBA viii. 269 Jen^Kosmol.223 ff. Zim^KAT 3. 636 and others; see also Muss-Arn^JBL xi (1892), 169 and references); — always absolute, שְׁאוֺל Deut 32:22 52t.,הָ֯ Gen 42:38; Psa 9:18; שְׁאֹל 1Kin 2:6; Job 17:16, הָ֯ Gen 37:35 7t.; + Isa 7:11 (so read for שְׁאָ֫לָה Aq Σ Θ Du Che and now most); —

d. Tode 109 'Ort der Entscheidung'); Thes Bö^De Inf. § 158 Di és mások a שׁעל √-vel vetik össze, amelyből שֹׁעַל: üreges kéz stb.; a ׳שׁ eszerint = üreges hely, 'Hölle', pokol; más feltevéseket l. Hup^Ps. 6 6 De^5:14 Beer^Bibl. Hades in Holtzmann^Festgabe,1902, 15; a legtöbben ma tartózkodnak a határozott etimológiától (pl. Buhl); óarámi שאול, szír ; az asszír šu-alu kétséges: így olvassa és értelmezi Dl^pa 121, Prol.47. 145 Jastr^Amos. J. Semitic Lang. xiv. 165 kk. Ency. Bib^s.v.; ellene Bertin^TSBA viii. 269 Jen^Kosmol.223 kk. Zim^KAT 3. 636 és mások; l. még Muss-Arn^JBL xi (1892), 169 és a hivatkozásokat); — mindig status absolutus, שְׁאוֺל 5Móz 32:22, összesen 52-szer,הָ֯ 1Móz 42:38; Zsolt 9:18; שְׁאֹל 1Kir 2:6; Jób 17:16, הָ֯ 1Móz 37:35, összesen 7-szer; + Ézs 7:11 (így olvasandó שְׁאָ֫לָה helyett Aq Σ Θ Du Che és most a legtöbben); —

**3.** 

> 1 the underworld, ׳שׁ תַּחְתִּית Deut 32:22, מִתַּחַת Isa 14:9; ׳מִשּׁ מִ֑טָּה Prov 15:24; || מָוֶת 5:5; 7:27; Song 8:6; Psa 89:49; whither men descend at death, Gen 37:35 (E), 42:38; 44:29, 31 (J), 1Sam 2:6; 1Kin 2:6, 9; Job 7:9; 21:13; Isa 14:11, 15; Psa 88:4, and Korah and associates go down alive by ׳יs judgment, Num 16:30, 33 (J), compare Psa 55:16; under mountains and sea Job 26:6 (compare 26:5), שׁ ׳בֶּטֶן Jonah 2:3 (compare 2:7); with bars Job 17:16 (si vera 1.: see ᵐ5 Du); שׁ ׳מִּי Psa 141:7; שׁ ׳שַׁעֲרֵי Isa 38:10; personified 28:15, 18 (|| מות). as insatiable monster 5:14; Hab 2:5; Prov 1:12; 27:20; 30:16; as said (figurative) to have snares, שׁ ׳חֶבְלֵי Psa 18:6 = 2Sam 22:6 compare שׁ ׳מְצָרֵי Psa 116:3; opposed to (height of) שָׁמַיִם Amos 9:2; Job 11:8; Psa 139:8 + (opposed to לְמָ֑עְלָה) Isa 7:11 (see above); dark, gloomy, without return Job 17:13 (compare 17:16; 7:9; 10:21; 16:22; all being alike 3:17-19; 21:23-26 ); without work or knowledge or wisdom according to Eccl 9:5-6, 10 (compare Job 14:21, and see רְפָאִים below רפה; yet compare Isa 14:9f.).

1 az alvilág, ׳שׁ תַּחְתִּית 5Móz 32:22, מִתַּחַת Ézs 14:9; ׳מִשּׁ מִ֑טָּה Péld 15:24; || מָוֶת 5:5; 7:27; Én 8:6; Zsolt 89:49; ahová az emberek halálukkor alászállnak, 1Móz 37:35 (E), 42:38; 44:29, 31 (J), 1Sám 2:6; 1Kir 2:6, 9; Jób 7:9; 21:13; Ézs 14:11, 15; Zsolt 88:4, és Kóré és társai elevenen szállnak alá ׳י ítéletéből, 4Móz 16:30, 33 (J), vö. Zsolt 55:16; hegyek és tenger alatt Jób 26:6 (vö. 26:5), שׁ ׳בֶּטֶן Jón 2:3 (vö. 2:7); zárakkal Jób 17:16 (si vera 1.: l. ᵐ5 Du); שׁ ׳מִּי Zsolt 141:7; שׁ ׳שַׁעֲרֵי Ézs 38:10; megszemélyesítve 28:15, 18 (|| מות). mint telhetetlen szörny 5:14; Hab 2:5; Péld 1:12; 27:20; 30:16; mint akinek (átvitt értelemben) tőrei vannak, שׁ ׳חֶבְלֵי Zsolt 18:6 = 2Sám 22:6, vö. שׁ ׳מְצָרֵי Zsolt 116:3; szemben a שָׁמַיִם (magasságával) Ámós 9:2; Jób 11:8; Zsolt 139:8 + (szemben a לְמָ֑עְלָה-mel) Ézs 7:11 (l. fent); sötét, komor, visszatérés nélküli Jób 17:13 (vö. 17:16; 7:9; 10:21; 16:22; ott mindenki egyforma 3:17-19; 21:23-26 ); munka, tudás és bölcsesség nélküli a Préd 9:5-6, 10 szerint (vö. Jób 14:21, és l. רְפָאִים a רפה alatt; de vö. Ézs 14:9k.).

**4.** 

> 2 condition of righteous and wicked distinguished in ׳שׁ (later than 1 Samuel 28, especially inWisdom Literature):

2 az igazak és a gonoszok állapota megkülönböztetve a ׳שׁ-ban (az 1Sám 28-nál később, különösen a bölcsességirodalomban):

**5.** 

> a. wicked לִשְׁא֑וֺלָה יָשׁוּבוּ Psa 9:18, לִשׁ ׳יִדְּמוּ 31:18; death is their shepherd, without power and honour they waste away 49:15 (twice in verse); ׳שׁ consumes them as drought water Job 24:19; righteous dread it because no praise or presence of God there (as in temple) Psa 6:6 (compare 88:5), Isa 38:18; deliverance from it a blessing Psa 30:4; 86:13; Prov 23:14. In Ezek. ׳שׁ is land below, place of reproach, abode of uncircumcised Ezek 31:15-16, 17; 32:21, 27 b. righteous shall not be aban-doned, ׳לשׁ Ezek 16:10 (|| שַׁחַת q. v.; opposed to חַיִּים אִרַח etc., 16:11, compare 17:15), is ransomed from ׳שׁ Ezek 49:16 (compare Ezek 73:23; Ezek 73:25; Isa 57:1-2,); compare Job's expectation and desire Job 14:13; 17:13 (compare 10:21; 19:25f.).

a. gonoszok לִשְׁא֑וֺלָה יָשׁוּבוּ Zsolt 9:18, לִשׁ ׳יִדְּמוּ 31:18; a halál a pásztoruk, erő és tisztesség nélkül sorvadnak el 49:15 (a versben kétszer); ׳שׁ úgy emészti meg őket, mint a szárazság a vizet Jób 24:19; az igazak rettegnek tőle, mert ott nincs dicséret és nincs Isten jelenléte (mint a templomban) Zsolt 6:6 (vö. 88:5), Ézs 38:18; a megszabadulás belőle áldás Zsolt 30:4; 86:13; Péld 23:14. Ezékielnél a ׳שׁ a lenti föld, a gyalázat helye, a körülmetéletlenek lakóhelye Ez 31:15-16, 17; 32:21, 27 b. az igazat nem hagyják el, ׳לשׁ Ez 16:10 (|| שַׁחַת, l. ott; szemben חַיִּים אִרַח stb., 16:11, vö. 17:15), kiváltatik a ׳שׁ-ból Ez 49:16 (vö. Ez 73:23; Ez 73:25; Ézs 57:1-2,); vö. Jób várakozását és vágyát Jób 14:13; 17:13 (vö. 10:21; 19:25k.).

**6.** 

> 3 later distinction of places in ׳שׁ:

3 a helyek későbbi megkülönböztetése a ׳שׁ-ban:

**7.** 

> a. depths of ׳שׁ for sensualist Prov 9:18.

a. a ׳שׁ mélységei az érzékiek számára Péld 9:18.

**8.** 

> b. ׳שׁ וַאֲבַדּוֺן Prov 25:11, see אֲבַדּוֺן. [שַׁחַת and בּוֺר, q. v., when || ׳שׁ, are usually in bad sense(Psa 88:4); probably = pit in ׳שׁ, > ׳שׁ itself as pit; words at least prepare for local distinctions of post-Biblical Judaism and NT.] 4 ׳שׁ figurative of extreme degradation in sin Isa 57:9; as place of exile for Israel Hosea 13:14 (twice in verse) (compare Isa 26:19).

b. ׳שׁ וַאֲבַדּוֺן Péld 25:11, l. אֲבַדּוֺן. [שַׁחַת és בּוֺר, l. ott, ha || ׳שׁ, rendszerint rossz értelemben állnak (Zsolt 88:4); valószínűleg = verem a ׳שׁ-ban, > maga a ׳שׁ mint verem; a szavak legalábbis előkészítik a Biblia utáni zsidóság és az Újszövetség helyi megkülönböztetéseit.] 4 ׳שׁ átvitt értelemben a bűnben való végső lealacsonyodásról Ézs 57:9; mint Izráel száműzetésének helye Hós 13:14 (a versben kétszer) (vö. Ézs 26:19).

## H8004 (BDB, 235 → 232 karakter)

`forras_hash=1049c6a64aeb8f9e5e833a91e6ff3949727a7179` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 2 forrasjelolo (forditas 2)

Törzskapu: RENDBEN · 

**1.** 

> H8004. Shalem II. שָׁלֵם proper name, of a location abbreviated from יְרוּשָׁלַםִ (q. v.), and perhaps (Gunk Dr) intended as archaism Gen 14:18, compare (poetry) Psa 76:3 (|| צִיּוֺן); see Jos^Ant.

H8004. Shalem II. שָׁלֵם tulajdonnév, helynév, a יְרוּשָׁלַםִ rövidült alakja (l. ott), és talán (Gunk Dr) archaizmusnak szánva 1Móz 14:18, vö. (költészet) Zsolt 76:3 (|| צִיּוֺן); l. Jos^Ant.

**2.** 

> i. 10, 2; ᵐ5 Σαλημ and (Psalms) εἰρήνη.

i. 10, 2; ᵐ5 Σαλημ és (Zsoltárok) εἰρήνη.

## H8415 (BDB, 1966 → 2142 karakter)

`forras_hash=14d421d364305891fd999f2ad927705ce7cf6acb` · `allapot=opus` · `modell=claude-opus-5-5` · `terminologia_verzio=v1`

Tagolás-kapu: RENDBEN · 6 forrasjelolo (forditas 7)

Törzskapu: RENDBEN · 

**1.** 

> H8415. tehom תִּהוֺם noun feminine^Gen 7:11 7t. and masculine^Job 28:14 5t. (Albr^ZAW xvi (1896), 62 Kö^ii.

H8415. tehom תִּהוֺם nőnemű főnév^1Móz 7:11, összesen 7-szer, és hímnemű^Jób 28:14, összesen 5-ször (Albr^ZAW xvi (1896), 62 Kö^ii.

**2.** 

> 2. 167 Ency. Bib.^DEEP) deep, sea, abyss (almost always in poetry); — absolute ׳ת Gen 1:2 +; plural absolute תְּהֹמוֺת Psa 77:17 +, etc., ׳בַּתּ Isa 63:13 + Isa 106:9 (only here with article); construct תְּהוֺמוֺת Isa 71:20 (but see 5 infra); —

2. 167 Ency. Bib.^DEEP): mélység, tenger, örvény (csaknem mindig költészetben); — status absolutus ׳ת 1Móz 1:2 és máshol; többes szám, status absolutus תְּהֹמוֺת Zsolt 77:17 és máshol, stb., ׳בַּתּ Ézs 63:13 + Ézs 106:9 (csak itt névelővel); status constructus תְּהוֺמוֺת Ézs 71:20 (de l. 5 lent); —

**3.** 

> 1 deep, of subterranean waters, Gen 49:25 (poem in J; opposed to שָׁמַיִם), Deut 33:13 (opposed to id.); ת מַעְיְנוֺת ׳רַבָּה Gen 7:11; 8:2 (P; || הַשָּׁמַיִם אֲרֻבֹּת), ת ׳עִינוֺת Prov 8:28 (|| שְׁחָקִים), Job 28:14; 38:16 (both || יָם); רַבָּה תְּהוֺם Amos 7:4 (probably), ת ׳מִשְׁמָּטֶיךָ רַבָּה Psa 36:7 (opposed to כְּהַרְרֵי צִדְקָֽתְךָ אֵל), Isa 51:10 (perhaps); so plural תְּהֹמוֺת, Prov 8:24 (|| מַעְיָנוֺת), 3:20 (opposed to שְׁחָקִים), and probably Psa 33:7 (|| הַיָּם מֵי), 135:6 ( + יַמִּים). 2 (deep) sea, overwhelming Tyre Ezek 26:19 (|| הָרַבִּים הַמַּיִם), roaring at theoph. Hab 3:10; in General, || יָם, Job 38:30 (ת ׳מְּנֵי); || מַיִם Jonah 2:6; alonE Job 41:24; figurative, ׳ת ׳אֶלתֿ קוֺרַא 42:8 (|| גַּלִּים מִשְׁבָּרִים,; but possibly here of Jordan, compare 4); in plural = abysses of sea, Exod 15:5, 8 (of Red Sea, so) Isa 63:13 || Psa 106:9; 77:17; also 78:15 (in simile), 107:26 (poetic of hollows of great waves, opposed to שָׁמַיִם); vaguely, כָּלתְּֿהֹמוֺת 135:6; 148:7.

1 mélység, a föld alatti vizekről, 1Móz 49:25 (költemény a J-ben; szemben a שָׁמַיִם-mel), 5Móz 33:13 (szemben ua.); ת מַעְיְנוֺת ׳רַבָּה 1Móz 7:11; 8:2 (P; || הַשָּׁמַיִם אֲרֻבֹּת), ת ׳עִינוֺת Péld 8:28 (|| שְׁחָקִים), Jób 28:14; 38:16 (mindkettő || יָם); רַבָּה תְּהוֺם Ámós 7:4 (valószínűleg), ת ׳מִשְׁמָּטֶיךָ רַבָּה Zsolt 36:7 (szemben a כְּהַרְרֵי צִדְקָֽתְךָ אֵל-mel), Ézs 51:10 (talán); így többes számban תְּהֹמוֺת, Péld 8:24 (|| מַעְיָנוֺת), 3:20 (szemben a שְׁחָקִים-mel), és valószínűleg Zsolt 33:7 (|| הַיָּם מֵי), 135:6 ( + יַמִּים). 2 (mély) tenger, amely elborítja Tíruszt Ez 26:19 (|| הָרַבִּים הַמַּיִם), zúg a teofániánál Hab 3:10; általában, || יָם, Jób 38:30 (ת ׳מְּנֵי); || מַיִם Jón 2:6; önmagában Jób 41:24; átvitt értelemben ׳ת ׳אֶלתֿ קוֺרַא 42:8 (|| גַּלִּים מִשְׁבָּרִים,; de itt talán a Jordánról, vö. 4); többes számban = a tenger mélységei, 2Móz 15:5, 8 (a Vörös-tengerről, így) Ézs 63:13 || Zsolt 106:9; 77:17; továbbá 78:15 (hasonlatban), 107:26 (költőien a nagy hullámok völgyeiről, szemben a שָׁמַיִם-mel); határozatlanul כָּלתְּֿהֹמוֺת 135:6; 148:7.

**4.** 

> 3 primaeval ocean, deep, in Hebrew cosmogony, ת ׳מְּנֵי Gen 1:2 (P; || הַמַּיִם מְּנֵי), Prov 8:27 (|| שָׁמַיִם), Psa 104:6. — (compare, further, Gunk^Schöpfung u. Chaos 21 ff. OCWhitehouse^Hast. DB COSMOGONY Zim^KAT3. 492 f., 509 f., 585).

3 az ősóceán, a mélység a héber kozmogóniában, ת ׳מְּנֵי 1Móz 1:2 (P; || הַמַּיִם מְּנֵי), Péld 8:27 (|| שָׁמַיִם), Zsolt 104:6. — (vö. továbbá Gunk^Schöpfung u. Chaos 21 kk. OCWhitehouse^Hast. DB COSMOGONY Zim^KAT3. 492 k., 509 k., 585).

**5.** 

> 4 deep, depth, of river Ezek 31:4 (Nile; || מַיִם, + נַהֲרוֺתֶיהָ), 31:15 (|| id.); plural of bursts of water fertilizing Canaan, ובהר בבקעה יוצאים Deut 8:7 ( + מַיִם נַחֲלֵי עֲיָנֹת,). — On Psa 42:8 see 2.

4 mélység, mélyvíz, folyóé Ez 31:4 (Nílus; || מַיִם, + נַהֲרוֺתֶיהָ), 31:15 (|| ua.); többes számban a Kánaánt termékennyé tevő vízfakadásokról, ובהר בבקעה יוצאים 5Móz 8:7 ( + מַיִם נַחֲלֵי עֲיָנֹת,). — A Zsolt 42:8-hoz l. 2.

**6.** 

> 5. abyss (si vera lectio): הָאָרֶץ תְּהוֺמוֺת = Shejôl, Psa 71:20, but Ol We תַּחְתִיּוֺת. [תַּחְמֻּכָה] see הפך. תָּו see תוה. below, תּוֺא see תְּאוֺ. [תּוֺאָם] see תאם.

5. örvény (si vera lectio): הָאָרֶץ תְּהוֺמוֺת = Seol, Zsolt 71:20, de Ol We תַּחְתִיּוֺת. [תַּחְמֻּכָה] l. הפך. תָּו l. תוה. alább, תּוֺא l. תְּאוֺ. [תּוֺאָם] l. תאם.

## Fordítói döntések az E4-ben (az első adag listáján felül)

| Angol (forrás) | Magyar (fordítás) | Hol |
|---|---|---|
| Lam (igehely) | JSir | DT24 (a) után; a Sirák fia (Ecclus, Sir.) = Sir |
| Ecclus / Ecclesiasticus (igehely) | Sir | apokrif alak |
| compare (komparatív `מִן`-nel) | comparativus | H7043, H7843 |
| emphatic | emphaticus | arámi szakaszok (H3548, H2416) |
| denominative | denominativum | H7843 |
| Tel Amarna | Tel Amarna | változatlan helynév |
| Zinjirli | zendzsirli | H3678, H7843, H2416 |
| proper name, of a location / of a people | tulajdonnév, helynév / népnév | H8004, H7497, H0127 |
| Isa^2, Isa^3 | Isa^2 (H7451: Ézs^2) | **következetlen**: a H7121-ben Ézs^2, másutt a forrás sziglája maradt |
| She'ôl / Sh®°ôl (folyó szövegben) | Seol | a H7585 fejlécében a sérült forrásalak maradt |

## Az E4 során javított kapuhibák és önújrapróbák

L. `naplok/EMELES_naplo.md` E4 szakasz. Az önújrapróbák mind formaiak (vessző a magyar
szó és a csupasz igehely közé; betoldott zárójel elhagyása; „spirit” → szellem; Sir →
JSir); kapuhiba miatt egyetlen szócikk sem került a bukottak listájára
(`naplok/EMELES_bukottak.tsv` nem készült).
