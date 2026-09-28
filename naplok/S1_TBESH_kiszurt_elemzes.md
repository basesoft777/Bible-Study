# S1 ellenorzes -- a 9d42da9 TBESH-szigoritas kiszurt kulcsai

scope=konkordancia/TBESH.txt + konkordancia/lexikonok_nyers/TBESH.lexicon (nyers Strong-kulcs union), regi szuro (^H\d+$) vs. uj szuro (^H\d{4}$ + H9xxx-kizaras, 9d42da9) | forras=eszkozok/_tmp_tbesh_kiszurt_elemzes.py (csak ellenorzes, ismetelt jatszas) | ts=2026-09-28

Regi szuro szerinti egyedi Strong-kulcsok (~9688-as allapot): 9688
Uj szuro szerinti egyedi Strong-kulcsok (~8639-es allapot): 8639
Kiszurt kulcsok (regi_unio - uj_unio): 1049
Ujonnan bekerult kulcsok (uj_unio - regi_unio, varhatoan 0): 0

Megjegyzes: a 9688/8639 a kommit-uzenetben szereplo *sor*szam a konszolidalt tablaban (Strongonkent egy sor); ez az elemzes ugyanezt a kulcshalmazt jatssza ujra a ket regexbol, ezert a 1049 es a jelentett 1049 kozotti kisebb elteres (ha van) az esetlegesen 0-hosszu vagy ures szocikkek kezelesebol adodhat -- l. alant.

## Kategoriak

| Kategoria | Darab |
|---|---|
| (a) H9xxx | 50 |
| (b) 4 jegynel rovidebb / ervenytelen | 999 |
| (c) betu-utotagos kiterjesztett Strong-szam | 0 |
| (d) egyeb | 0 |
| **osszesen** | **1049** |

### (a) H9xxx -- teljes lista

H9000, H9001, H9002, H9003, H9004, H9005, H9006, H9007, H9008, H9009, H9010, H9011, H9012, H9013, H9014, H9015, H9016, H9017, H9018, H9019, H9020, H9021, H9022, H9023, H9024, H9025, H9026, H9027, H9028, H9029, H9030, H9031, H9032, H9033, H9034, H9035, H9036, H9037, H9038, H9039, H9040, H9041, H9042, H9043, H9044, H9045, H9046, H9047, H9048, H9049

### (b) 4 jegynel rovidebb / ervenytelen -- teljes lista

H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H27, H28, H29, H30, H31, H32, H33, H34, H35, H36, H37, H38, H39, H40, H41, H42, H43, H44, H45, H46, H47, H48, H49, H50, H51, H52, H53, H54, H55, H56, H57, H58, H59, H60, H61, H62, H63, H64, H65, H66, H67, H68, H69, H70, H71, H72, H73, H74, H75, H76, H77, H78, H79, H80, H81, H82, H83, H84, H85, H86, H87, H88, H89, H90, H91, H92, H93, H94, H95, H96, H97, H98, H99, H100, H101, H102, H103, H104, H105, H106, H107, H108, H109, H110, H111, H112, H113, H114, H115, H116, H117, H118, H119, H120, H121, H122, H123, H124, H125, H126, H127, H128, H129, H130, H131, H132, H133, H134, H135, H136, H137, H138, H139, H140, H141, H142, H143, H144, H145, H146, H147, H148, H149, H150, H151, H152, H153, H154, H155, H156, H157, H158, H159, H160, H161, H162, H163, H164, H165, H166, H167, H168, H169, H170, H171, H172, H173, H174, H175, H176, H177, H178, H179, H180, H181, H182, H183, H184, H185, H186, H187, H188, H189, H190, H191, H192, H193, H194, H195, H196, H197, H198, H199, H200, H201, H202, H203, H204, H205, H206, H207, H208, H209, H210, H211, H212, H213, H214, H215, H216, H217, H218, H219, H220, H221, H222, H223, H224, H225, H226, H227, H228, H229, H230, H231, H232, H233, H234, H235, H236, H237, H238, H239, H240, H241, H242, H243, H244, H245, H246, H247, H248, H249, H250, H251, H252, H253, H254, H255, H256, H257, H258, H259, H260, H261, H262, H263, H264, H265, H266, H267, H268, H269, H270, H271, H272, H273, H274, H275, H276, H277, H278, H279, H280, H281, H282, H283, H284, H285, H286, H287, H288, H289, H290, H291, H292, H293, H294, H295, H296, H297, H298, H299, H300, H301, H302, H303, H304, H305, H306, H307, H308, H309, H310, H311, H312, H313, H314, H315, H316, H317, H318, H319, H320, H321, H322, H323, H324, H325, H326, H327, H328, H329, H330, H331, H332, H333, H334, H335, H336, H337, H338, H339, H340, H341, H342, H343, H344, H345, H346, H347, H348, H349, H350, H351, H352, H353, H354, H355, H356, H357, H358, H359, H360, H361, H362, H363, H364, H365, H366, H367, H368, H369, H370, H371, H372, H373, H374, H375, H376, H377, H378, H379, H380, H381, H382, H383, H384, H385, H386, H387, H388, H389, H390, H391, H392, H393, H394, H395, H396, H397, H398, H399, H400, H401, H402, H403, H404, H405, H406, H407, H408, H409, H410, H411, H412, H413, H414, H415, H416, H417, H418, H419, H420, H421, H422, H423, H424, H425, H426, H427, H428, H429, H430, H431, H432, H433, H434, H435, H436, H437, H438, H439, H440, H441, H442, H443, H444, H445, H446, H447, H448, H449, H450, H451, H452, H453, H454, H455, H456, H457, H458, H459, H460, H461, H462, H463, H464, H465, H466, H467, H468, H469, H470, H471, H472, H473, H474, H475, H476, H477, H478, H479, H480, H481, H482, H483, H484, H485, H486, H487, H488, H489, H490, H491, H492, H493, H494, H495, H496, H497, H498, H499, H500, H501, H502, H503, H504, H505, H506, H507, H508, H509, H510, H511, H512, H513, H514, H515, H516, H517, H518, H519, H520, H521, H522, H523, H524, H525, H526, H527, H528, H529, H530, H531, H532, H533, H534, H535, H536, H537, H538, H539, H540, H541, H542, H543, H544, H545, H546, H547, H548, H549, H550, H551, H552, H553, H554, H555, H556, H557, H558, H559, H560, H561, H562, H563, H564, H565, H566, H567, H568, H569, H570, H571, H572, H573, H574, H575, H576, H577, H578, H579, H580, H581, H582, H583, H584, H585, H586, H587, H588, H589, H590, H591, H592, H593, H594, H595, H596, H597, H598, H599, H600, H601, H602, H603, H604, H605, H606, H607, H608, H609, H610, H611, H612, H613, H614, H615, H616, H617, H618, H619, H620, H621, H622, H623, H624, H625, H626, H627, H628, H629, H630, H631, H632, H633, H634, H635, H636, H637, H638, H639, H640, H641, H642, H643, H644, H645, H646, H647, H648, H649, H650, H651, H652, H653, H654, H655, H656, H657, H658, H659, H660, H661, H662, H663, H664, H665, H666, H667, H668, H669, H670, H671, H672, H673, H674, H675, H676, H677, H678, H679, H680, H681, H682, H683, H684, H685, H686, H687, H688, H689, H690, H691, H692, H693, H694, H695, H696, H697, H698, H699, H700, H701, H702, H703, H704, H705, H706, H707, H708, H709, H710, H711, H712, H713, H714, H715, H716, H717, H718, H719, H720, H721, H722, H723, H724, H725, H726, H727, H728, H729, H730, H731, H732, H733, H734, H735, H736, H737, H738, H739, H740, H741, H742, H743, H744, H745, H746, H747, H748, H749, H750, H751, H752, H753, H754, H755, H756, H757, H758, H759, H760, H761, H762, H763, H764, H765, H766, H767, H768, H769, H770, H771, H772, H773, H774, H775, H776, H777, H778, H779, H780, H781, H782, H783, H784, H785, H786, H787, H788, H789, H790, H791, H792, H793, H794, H795, H796, H797, H798, H799, H800, H801, H802, H803, H804, H805, H806, H807, H808, H809, H810, H811, H812, H813, H814, H815, H816, H817, H818, H819, H820, H821, H822, H823, H824, H825, H826, H827, H828, H829, H830, H831, H832, H833, H834, H835, H836, H837, H838, H839, H840, H841, H842, H843, H844, H845, H846, H847, H848, H849, H850, H851, H852, H853, H854, H855, H856, H857, H858, H859, H860, H861, H862, H863, H864, H865, H866, H867, H868, H869, H870, H871, H872, H873, H874, H875, H876, H877, H878, H879, H880, H881, H882, H883, H884, H885, H886, H887, H888, H889, H890, H891, H892, H893, H894, H895, H896, H897, H898, H899, H900, H901, H902, H903, H904, H905, H906, H907, H908, H909, H910, H911, H912, H913, H914, H915, H916, H917, H918, H919, H920, H921, H922, H923, H924, H925, H926, H927, H928, H929, H930, H931, H932, H933, H934, H935, H936, H937, H938, H939, H940, H941, H942, H943, H944, H945, H946, H947, H948, H949, H950, H951, H952, H953, H954, H955, H956, H957, H958, H959, H960, H961, H962, H963, H964, H965, H966, H967, H968, H969, H970, H971, H972, H973, H974, H975, H976, H977, H978, H979, H980, H981, H982, H983, H984, H985, H986, H987, H988, H989, H990, H991, H992, H993, H994, H995, H996, H997, H998, H999

### (c) betu-utotagos kiterjesztett Strong-szam -- teljes lista, normalizalva

(ures -- a regi szuro `^H\d+$` sem engedte at a betu-utotagos kulcsokat, tehat ezek soha nem voltak resze a 9688-as allapotnak; a 9d42da9 valtozas nem erinti oket. A minta tehat nem dob el semmit ebben a kategoriaban.)

### (d) egyeb -- teljes lista

(ures)

## Hianyzo alapszamok H0001-H8674 tartomanyban (nincs soruk a kimeneti tablaban)

Darab: 35

H0122, H0176, H0193, H0217, H0218, H0219, H0223, H0227, H0244, H0310, H0328, H0349, H0352, H0359, H0441, H0454, H0518, H0520, H0565, H0576, H0581, H0657, H0671, H0682, H0738, H0746, H0783, H0805, H0834, H0838, H0859, H0862, H0899, H0953, H0973

## A (b) kategoria 999 tetelenek eredete -- ket kulonbozo eset, nem egy

A (b) kategoria mind a 999 kulcsa a H1-H999 nem-nullaval-kitoltott ("unpadded")
alak (pl. `H122`, nem `H0122`). Ez ket, egymastol elteru sulyu esetre bomlik:

- **964 kulcs: alkalmatlan duplikatum, nincs adatvesztes.** A H1..H999
  tartomanyban 964 esetben a nyers forras (TBESH.txt es/vagy TBESH.lexicon)
  UGYANAHHOZ a Strong-szamhoz **mindket alakot** tartalmazza: a nem toltott
  (`H122`) es a nullaval toltott 4-jegyu (`H0122`) valtozatot is, azonos
  tartalommal. Az uj szuro csak a nem toltott alakot dobja el -- a toltott
  alak megmaradt, tehat az adat a kimeneti tablaban jelen van. Igazolva:
  a kimeneti tabla H0001-H0999 kulcsainak szama 964.
- **35 kulcs: valodi adatvesztes.** Pontosan a fent listazott 35 hianyzo
  alapszamnal a nem toltott alak (pl. `H122`) az **egyetlen** forras --
  sem a TBESH.txt-ben, sem a TBESH.lexicon-ban nincs hozza `H0nnn` toltott
  parja. Mind a 35 kizarolag a TBESH.lexicon SQLite-tablabol szarmazik
  (a TBESH.txt-ben egyaltalan nincs jelen egyik alakban sem). Az uj szuro
  ezeket a valodi, egyedi szocikkeket is kidobja, mert a kulcsuk soha nem
  volt 4 jegyu.

**Kovetkeztetes:** a (b) kategorian beluli 1049-999=50 (a) + 999 (b) = 1049
osszkiszures TOBBSEGE (964/999) artalmatlan -- a 4-jegyu szuro csak egy
redundans alternativ kulcsot tavolitott el. De **35 Strong-szamnal (H0122,
H0176, H0193, H0217, H0218, H0219, H0223, H0227, H0244, H0310, H0328, H0349,
H0352, H0359, H0441, H0454, H0518, H0520, H0565, H0576, H0581, H0657, H0671,
H0682, H0738, H0746, H0783, H0805, H0834, H0838, H0859, H0862, H0899, H0953,
H0973) a szigoritas egy egyedi, mashonnan nem potolhato TBESH-szocikket
tavolitott el a kimeneti tablabol.**

## Javaslat (eredeti allapot -- azota megvalositva, l. alant)

A minta eredeti formajaban (`^H\d{4}$`) helyesen zarta ki a H9xxx
morfologiai tartomanyt, de mellekhatasakent a fenti 35 nem-toltott, egyedi
Strong-kulcsot is kidobta. Javitas: a szuro elott a Strong-kulcsot
nullaval-kitoltes-normalizalni kell (`H%d` -> `H%04d`, `zfill(4)` a
szamresz-en), MIELOTT a 4-jegyu es H9xxx-teszt lefut.

**Fontos korrekcio a fenti szoveghez kepest:** a `tbesh_konszolidalt_import.py`
eredeti kommentje ("`H9`/`H90`/`H900`... feltehetoen a forras sajat
prefix-index bejegyzesei, nem szotari tetelek") **tevesnek bizonyult**. A
`TBESH.lexicon`-ban a `H9` Strong-tartalma (`אֲבֵדָה` "something lost") pontosan
egyezik a `TBESH.txt` `H0009` sorával, a `H90` (`אֲגָג` Agag) a `H0090`-nel, a
`H900` (`בֹּגְדוֹת` treachery) a `H0900`-nal -- ezek tehat **valodi, csak
nem-toltott Strong-kulcsok**, nem index-artefaktumok. A H9xxx-kizaras
(`^H9\d{3}$`, azaz pontosan a H9000-H9999 morfologiai tartomany) marad
indokolt; a `H9`/`H90`/`H900` (1-3 jegyu) ettol fuggetlen eset, es a
zfill(4)-normalizalas helyesen H0009/H0090/H0900-ra alakitja oket.

## Javitas alkalmazva (`normalizal()`, zfill(4))

A `tbesh_konszolidalt_import.py`-ba bekerult egy `normalizal()` fuggveny,
amely minden nyers, csak-szamjegyeket tartalmazo Strong-kulcsot 4 jegyre
tolt (`H122` -> `H0122`) MIELOTT a `STRONG_H_RE`/`H9XXX_RE` szures lefut.
Betu-utotagos vagy mar 4-jegyu kulcsot valtozatlanul hagy. Ellenorizve:
sem a `TBESH.txt`, sem a `TBESH.lexicon` nem tartalmaz ket kulonbozo nyers
kulcsot (pl. `H9` es `H0009`) egyszerre UGYANABBAN a forrasban -- tehat a
normalizalas nem okozhat forrason-beluli utkozest, csak a mar meglevo,
forrasok-kozotti `konszolidal()` hossz-alapu valasztasi logikaba fut bele
(ugyanugy, mint minden mas Strong, amelynel mindket forras ad szoveget).

Ujrafuttatva (`python eszkozok/tbesh_konszolidalt_import.py`):

| | Regi (9d42da9) | Uj (normalizalas utan) |
|---|---|---|
| Sorok szama | 8639 | **8674** |
| Csak .txt-ben | (nem naplozva) | 0 |
| Csak .lexicon-ban | (nem naplozva) | 542 |
| Mindketto, .txt bovebb | (nem naplozva) | 3006 |
| Mindketto, .lexicon bovebb | (nem naplozva) | 5033 |
| Mindketto, kb. egyenlo | (nem naplozva) | 93 |
| Hianyzo alapszam H0001-H8674 | 35 | **0** |

A novekmeny pontosan 8674-8639=35, egyezik a fent azonositott egyedi
kulcsok szamaval. Ellenorizve: a H0001-H8674 tartomany mind a 8674
alapszamara van sor a kimeneti tablaban (0 hianyzik). Mintapelda:
`H0122` sora most `forras=lexicon`, `lexicon_hossz=131`, tartalommal
toltve (korabban egyaltalan nem volt sora).

**Utolagos korrekcio a "964 artalmatlan duplikatum" allitashoz:** a
kulcs SZINTJEN valoban artalmatlan volt (a sor letezett), de a
TARTALOM szintjen nem -- a normalizalas elott a lexikon-valtozat
`H9`, `H10` stb. alakban soha nem jutott be a `konszolidal()`
hossz-alapu forras-valasztasba, mert a szures mar korabban kidobta.
Igy mind a 964 "duplikatum" Strong korabban **kenyszeruen** `forras=txt`
volt, fuggetlenul attol, hogy a lexikon-valtozat bovebb/jobb lett
volna-e. Az uj futtatas osszehasonlitva a regi tablaval (`git show
10d8733:konkordancia/TBESH_konszolidalt.tsv`): a H0001-H0999
tartomany 964 mar-letezo soraból **515-nel a tartalom valtozott**
(509-nel txt -> lexicon, mert a lexikon szoveg bizonyult hosszabbnak/
teljesebbnek -- pl. `H0007` korabban "1) to perish, vanish..." (csak
angol glossza), most "אֲבַד [A:V] to destroy 1) to perish, vanish..."
(heber lemma + POS-kod is); tovabbi 6-nal txt -> egyenlo, l. a pontos
bontast alant), es 449-nel a tartalom valtozatlan maradt (a txt mar
korabban is a hosszabb/valasztott valtozat volt). A javitas tehat
nemcsak 35 sort mentett meg, hanem 515 mar letezo sor tartalmi
minoseget is javitotta.

## Uj darabszam osszefoglalva

| Mutato | Regi (9d42da9, `8639`-es allapot) | Uj (`normalizal()` zfill(4) utan) |
|---|---|---|
| Sorok szama a `TBESH_konszolidalt.tsv`-ben | 8639 | **8674** |
| Hianyzo alapszam H0001-H8674 | 35 | **0** |
| H0001-H0999 tartomany: uj sor (korabban hianyzott) | -- | 35 |
| H0001-H0999 tartomany: tartalom javult, txt->lexicon (pontositva, l. alant) | -- | 509 |
| H0001-H0999 tartomany: tartalom javult, txt->egyenlo | -- | 6 |
| H0001-H0999 tartomany: tartalom valtozatlan | -- | 449 |

A `konkordancia/TBESH_konszolidalt.tsv`, a `naplok/SZOTAR_S1_4_jelentes.md`
es a `konkordancia/TBESH_TBESG_README.md` ujragenerálva/frissitve es
commitolva ezzel a jelentessel egyutt (S1.5 dokumentacios lepese, egy
commitban).

## Az 509 txt -> lexicon forras-csere reszletes listaja (H0001-H0999)

Pontositas: a korabbi becslesben szereplo "521" a teljes tartalom-valtozast szamolta (barmilyen forras-atmenettel); ebbol pontosan **509** tiszta txt -> lexicon csere, 6 pedig txt -> egyenlo atmenet (a hossz kb. 5%-on beluli lett, l. a tablazat alatt). Osszesen 515 sor tartalma valtozott a H0001-H0999 tartomanyban.

txt -> egyenlo atmenetek: H0113 (txt->egyenlo), H0215 (txt->egyenlo), H0622 (txt->egyenlo), H0798 (txt->egyenlo), H0830 (txt->egyenlo), H0995 (txt->egyenlo)


| kulcs | regi forras | uj forras | txt_hossz | lexicon_hossz | hosszkulonbseg (lex-txt) |
|---|---|---|---|---|---|
| H0007 | txt | lexicon | 90 | 113 | +23 |
| H0008 | txt | lexicon | 11 | 40 | +29 |
| H0009 | txt | lexicon | 28 | 62 | +34 |
| H0010 | txt | lexicon | 11 | 44 | +33 |
| H0011 | txt | lexicon | 50 | 78 | +28 |
| H0012 | txt | lexicon | 11 | 43 | +32 |
| H0013 | txt | lexicon | 11 | 42 | +31 |
| H0014 | txt | lexicon | 103 | 126 | +23 |
| H0015 | txt | lexicon | 24 | 51 | +27 |
| H0016 | txt | lexicon | 13 | 39 | +26 |
| H0017 | txt | lexicon | 65 | 88 | +23 |
| H0018 | txt | lexicon | 28 | 51 | +23 |
| H0019 | txt | lexicon | 40 | 69 | +29 |
| H0020 | txt | lexicon | 26 | 55 | +29 |
| H0024 | txt | lexicon | 136 | 180 | +44 |
| H0025 | txt | lexicon | 108 | 156 | +48 |
| H0034 | txt | lexicon | 191 | 214 | +23 |
| H0035 | txt | lexicon | 33 | 63 | +30 |
| H0046 | txt | lexicon | 83 | 105 | +22 |
| H0047 | txt | lexicon | 152 | 175 | +23 |
| H0055 | txt | lexicon | 56 | 80 | +24 |
| H0056 | txt | lexicon | 224 | 245 | +21 |
| H0057 | txt | lexicon | 131 | 152 | +21 |
| H0058 | txt | lexicon | 46 | 70 | +24 |
| H0060 | txt | lexicon | 104 | 128 | +24 |
| H0061 | txt | lexicon | 84 | 104 | +20 |
| H0062 | txt | lexicon | 94 | 144 | +50 |
| H0064 | txt | lexicon | 57 | 98 | +41 |
| H0065 | txt | lexicon | 75 | 115 | +40 |
| H0069 | txt | lexicon | 69 | 90 | +21 |
| H0070 | txt | lexicon | 68 | 88 | +20 |
| H0072 | txt | lexicon | 138 | 172 | +34 |
| H0073 | txt | lexicon | 87 | 110 | +23 |
| H0075 | txt | lexicon | 58 | 80 | +22 |
| H0076 | txt | lexicon | 40 | 69 | +29 |
| H0077 | txt | lexicon | 57 | 79 | +22 |
| H0079 | txt | lexicon | 48 | 74 | +26 |
| H0080 | txt | lexicon | 39 | 58 | +19 |
| H0081 | txt | lexicon | 24 | 59 | +35 |
| H0082 | txt | lexicon | 31 | 53 | +22 |
| H0083 | txt | lexicon | 71 | 91 | +20 |
| H0084 | txt | lexicon | 70 | 93 | +23 |
| H0088 | txt | lexicon | 114 | 136 | +22 |
| H0092 | txt | lexicon | 180 | 203 | +23 |
| H0093 | txt | lexicon | 4 | 26 | +22 |
| H0095 | txt | lexicon | 20 | 46 | +26 |
| H0096 | txt | lexicon | 41 | 64 | +23 |
| H0097 | txt | lexicon | 44 | 72 | +28 |
| H0098 | txt | lexicon | 120 | 139 | +19 |
| H0099 | txt | lexicon | 13 | 36 | +23 |
| H0100 | txt | lexicon | 222 | 246 | +24 |
| H0101 | txt | lexicon | 128 | 150 | +22 |
| H0102 | txt | lexicon | 37 | 59 | +22 |
| H0103 | txt | lexicon | 32 | 54 | +22 |
| H0105 | txt | lexicon | 34 | 61 | +27 |
| H0106 | txt | lexicon | 4 | 28 | +24 |
| H0108 | txt | lexicon | 4 | 24 | +20 |
| H0109 | txt | lexicon | 82 | 104 | +22 |
| H0115 | txt | lexicon | 97 | 127 | +30 |
| H0117 | txt | lexicon | 144 | 164 | +20 |
| H0119 | txt | lexicon | 254 | 276 | +22 |
| H0124 | txt | lexicon | 47 | 70 | +23 |
| H0125 | txt | lexicon | 19 | 47 | +28 |
| H0126 | txt | lexicon | 47 | 71 | +24 |
| H0128 | txt | lexicon | 39 | 64 | +25 |
| H0129 | txt | lexicon | 61 | 101 | +40 |
| H0131 | txt | lexicon | 77 | 105 | +28 |
| H0132 | txt | lexicon | 30 | 54 | +24 |
| H0134 | txt | lexicon | 206 | 228 | +22 |
| H0136 | txt | lexicon | 119 | 131 | +12 |
| H0142 | txt | lexicon | 121 | 145 | +24 |
| H0145 | txt | lexicon | 49 | 67 | +18 |
| H0147 | txt | lexicon | 15 | 49 | +34 |
| H0148 | txt | lexicon | 27 | 57 | +30 |
| H0149 | txt | lexicon | 41 | 76 | +35 |
| H0150 | txt | lexicon | 96 | 123 | +27 |
| H0154 | txt | lexicon | 72 | 99 | +27 |
| H0155 | txt | lexicon | 143 | 170 | +27 |
| H0158 | txt | lexicon | 54 | 75 | +21 |
| H0159 | txt | lexicon | 30 | 53 | +23 |
| H0160 | txt | lexicon | 163 | 184 | +21 |
| H0162 | txt | lexicon | 15 | 39 | +24 |
| H0163 | txt | lexicon | 53 | 77 | +24 |
| H0165 | txt | lexicon | 5 | 29 | +24 |
| H0166 | txt | lexicon | 27 | 51 | +24 |
| H0167 | txt | lexicon | 98 | 119 | +21 |
| H0174 | txt | lexicon | 52 | 71 | +19 |
| H0178 | txt | lexicon | 169 | 189 | +20 |
| H0180 | txt | lexicon | 13 | 37 | +24 |
| H0181 | txt | lexicon | 17 | 43 | +26 |
| H0182 | txt | lexicon | 50 | 73 | +23 |
| H0183 | txt | lexicon | 192 | 214 | +22 |
| H0184 | txt | lexicon | 88 | 108 | +20 |
| H0185 | txt | lexicon | 41 | 66 | +25 |
| H0188 | txt | lexicon | 56 | 74 | +18 |
| H0190 | txt | lexicon | 4 | 27 | +23 |
| H0191 | txt | lexicon | 161 | 186 | +25 |
| H0194 | txt | lexicon | 64 | 87 | +23 |
| H0195 | txt | lexicon | 46 | 68 | +22 |
| H0196 | txt | lexicon | 7 | 32 | +25 |
| H0199 | txt | lexicon | 66 | 85 | +19 |
| H0200 | txt | lexicon | 18 | 45 | +27 |
| H0202 | txt | lexicon | 80 | 102 | +22 |
| H0204 | txt | lexicon | 164 | 181 | +17 |
| H0210 | txt | lexicon | 59 | 97 | +38 |
| H0212 | txt | lexicon | 123 | 144 | +21 |
| H0213 | txt | lexicon | 212 | 233 | +21 |
| H0214 | txt | lexicon | 289 | 313 | +24 |
| H0216 | txt | lexicon | 279 | 298 | +19 |
| H0225 | txt | lexicon | 26 | 51 | +25 |
| H0228 | txt | lexicon | 21 | 44 | +23 |
| H0231 | txt | lexicon | 57 | 82 | +25 |
| H0232 | txt | lexicon | 126 | 148 | +22 |
| H0233 | txt | lexicon | 18 | 40 | +22 |
| H0234 | txt | lexicon | 74 | 105 | +31 |
| H0235 | txt | lexicon | 158 | 178 | +20 |
| H0236 | txt | lexicon | 44 | 62 | +18 |
| H0237 | txt | lexicon | 111 | 132 | +21 |
| H0238 | txt | lexicon | 133 | 155 | +22 |
| H0239 | txt | lexicon | 35 | 60 | +25 |
| H0240 | txt | lexicon | 26 | 50 | +24 |
| H0242 | txt | lexicon | 77 | 117 | +40 |
| H0243 | txt | lexicon | 70 | 110 | +40 |
| H0246 | txt | lexicon | 16 | 40 | +24 |
| H0247 | txt | lexicon | 176 | 197 | +21 |
| H0248 | txt | lexicon | 3 | 28 | +25 |
| H0249 | txt | lexicon | 100 | 121 | +21 |
| H0253 | txt | lexicon | 16 | 35 | +19 |
| H0254 | txt | lexicon | 17 | 39 | +22 |
| H0255 | txt | lexicon | 38 | 66 | +28 |
| H0258 | txt | lexicon | 48 | 80 | +32 |
| H0259 | txt | lexicon | 247 | 263 | +16 |
| H0260 | txt | lexicon | 27 | 51 | +24 |
| H0264 | txt | lexicon | 23 | 54 | +31 |
| H0268 | txt | lexicon | 75 | 95 | +20 |
| H0269 | txt | lexicon | 198 | 220 | +22 |
| H0270 | txt | lexicon | 176 | 197 | +21 |
| H0272 | txt | lexicon | 62 | 90 | +28 |
| H0305 | txt | lexicon | 37 | 64 | +27 |
| H0306 | txt | lexicon | 230 | 261 | +31 |
| H0307 | txt | lexicon | 112 | 141 | +29 |
| H0312 | txt | lexicon | 72 | 92 | +20 |
| H0314 | txt | lexicon | 133 | 153 | +20 |
| H0318 | txt | lexicon | 81 | 106 | +25 |
| H0322 | txt | lexicon | 30 | 63 | +33 |
| H0327 | txt | lexicon | 14 | 43 | +29 |
| H0330 | txt | lexicon | 19 | 48 | +29 |
| H0331 | txt | lexicon | 114 | 137 | +23 |
| H0332 | txt | lexicon | 63 | 83 | +20 |
| H0334 | txt | lexicon | 61 | 88 | +27 |
| H0335 | txt | lexicon | 67 | 83 | +16 |
| H0336 | txt | lexicon | 3 | 22 | +19 |
| H0337 | txt | lexicon | 11 | 31 | +20 |
| H0338 | txt | lexicon | 21 | 47 | +26 |
| H0339 | txt | lexicon | 28 | 53 | +25 |
| H0340 | txt | lexicon | 96 | 119 | +23 |
| H0341 | txt | lexicon | 40 | 60 | +20 |
| H0342 | txt | lexicon | 14 | 39 | +25 |
| H0343 | txt | lexicon | 129 | 151 | +22 |
| H0344 | txt | lexicon | 18 | 43 | +25 |
| H0346 | txt | lexicon | 47 | 69 | +22 |
| H0351 | txt | lexicon | 6 | 31 | +25 |
| H0353 | txt | lexicon | 19 | 42 | +23 |
| H0354 | txt | lexicon | 16 | 39 | +23 |
| H0355 | txt | lexicon | 15 | 39 | +24 |
| H0357 | txt | lexicon | 178 | 241 | +63 |
| H0358 | txt | lexicon | 61 | 106 | +45 |
| H0360 | txt | lexicon | 17 | 46 | +29 |
| H0361 | txt | lexicon | 25 | 50 | +25 |
| H0362 | txt | lexicon | 69 | 91 | +22 |
| H0364 | txt | lexicon | 84 | 116 | +32 |
| H0365 | txt | lexicon | 157 | 178 | +21 |
| H0366 | txt | lexicon | 18 | 42 | +24 |
| H0367 | txt | lexicon | 13 | 38 | +25 |
| H0369 | txt | lexicon | 128 | 150 | +22 |
| H0370 | txt | lexicon | 15 | 41 | +26 |
| H0371 | txt | lexicon | 28 | 50 | +22 |
| H0374 | txt | lexicon | 250 | 271 | +21 |
| H0375 | txt | lexicon | 23 | 45 | +22 |
| H0377 | txt | lexicon | 62 | 86 | +24 |
| H0380 | txt | lexicon | 74 | 97 | +23 |
| H0381 | txt | lexicon | 25 | 53 | +28 |
| H0382 | txt | lexicon | 74 | 105 | +31 |
| H0383 | txt | lexicon | 53 | 77 | +24 |
| H0386 | txt | lexicon | 121 | 141 | +20 |
| H0388 | txt | lexicon | 130 | 159 | +29 |
| H0389 | txt | lexicon | 69 | 89 | +20 |
| H0390 | txt | lexicon | 73 | 96 | +23 |
| H0391 | txt | lexicon | 64 | 91 | +27 |
| H0392 | txt | lexicon | 115 | 122 | +7 |
| H0393 | txt | lexicon | 13 | 36 | +23 |
| H0394 | txt | lexicon | 5 | 30 | +25 |
| H0395 | txt | lexicon | 26 | 57 | +31 |
| H0396 | txt | lexicon | 29 | 54 | +25 |
| H0399 | txt | lexicon | 126 | 148 | +22 |
| H0400 | txt | lexicon | 58 | 78 | +20 |
| H0402 | txt | lexicon | 135 | 156 | +21 |
| H0403 | txt | lexicon | 120 | 141 | +21 |
| H0404 | txt | lexicon | 44 | 65 | +21 |
| H0405 | txt | lexicon | 25 | 50 | +25 |
| H0406 | txt | lexicon | 77 | 99 | +22 |
| H0407 | txt | lexicon | 77 | 105 | +28 |
| H0411 | txt | lexicon | 12 | 31 | +19 |
| H0413 | txt | lexicon | 412 | 435 | +23 |
| H0415 | txt | lexicon | 89 | 141 | +52 |
| H0416 | txt | lexicon | 89 | 124 | +35 |
| H0417 | txt | lexicon | 26 | 55 | +29 |
| H0418 | txt | lexicon | 34 | 65 | +31 |
| H0421 | txt | lexicon | 21 | 44 | +23 |
| H0422 | txt | lexicon | 153 | 174 | +21 |
| H0423 | txt | lexicon | 76 | 95 | +19 |
| H0424 | txt | lexicon | 65 | 83 | +18 |
| H0426 | txt | lexicon | 54 | 75 | +21 |
| H0427 | txt | lexicon | 19 | 38 | +19 |
| H0430 | txt | lexicon | 208 | 226 | +18 |
| H0432 | txt | lexicon | 29 | 55 | +26 |
| H0434 | txt | lexicon | 71 | 94 | +23 |
| H0435 | txt | lexicon | 78 | 100 | +22 |
| H0437 | txt | lexicon | 15 | 38 | +23 |
| H0439 | txt | lexicon | 88 | 127 | +39 |
| H0442 | txt | lexicon | 77 | 101 | +24 |
| H0444 | txt | lexicon | 39 | 65 | +26 |
| H0451 | txt | lexicon | 45 | 73 | +28 |
| H0457 | txt | lexicon | 103 | 123 | +20 |
| H0480 | txt | lexicon | 10 | 34 | +24 |
| H0481 | txt | lexicon | 83 | 103 | +20 |
| H0482 | txt | lexicon | 18 | 44 | +26 |
| H0483 | txt | lexicon | 35 | 56 | +21 |
| H0484 | txt | lexicon | 58 | 87 | +29 |
| H0485 | txt | lexicon | 71 | 93 | +22 |
| H0487 | txt | lexicon | 56 | 91 | +35 |
| H0488 | txt | lexicon | 38 | 64 | +26 |
| H0489 | txt | lexicon | 9 | 38 | +29 |
| H0490 | txt | lexicon | 5 | 32 | +27 |
| H0491 | txt | lexicon | 9 | 41 | +32 |
| H0492 | txt | lexicon | 22 | 49 | +27 |
| H0495 | txt | lexicon | 79 | 106 | +27 |
| H0500 | txt | lexicon | 74 | 102 | +28 |
| H0502 | txt | lexicon | 50 | 77 | +27 |
| H0503 | txt | lexicon | 124 | 158 | +34 |
| H0504 | txt | lexicon | 50 | 72 | +22 |
| H0507 | txt | lexicon | 56 | 83 | +27 |
| H0509 | txt | lexicon | 14 | 37 | +23 |
| H0510 | txt | lexicon | 110 | 132 | +22 |
| H0512 | txt | lexicon | 88 | 120 | +32 |
| H0513 | txt | lexicon | 56 | 86 | +30 |
| H0514 | txt | lexicon | 95 | 123 | +28 |
| H0515 | txt | lexicon | 78 | 107 | +29 |
| H0516 | txt | lexicon | 131 | 166 | +35 |
| H0517 | txt | lexicon | 123 | 142 | +19 |
| H0519 | txt | lexicon | 79 | 105 | +26 |
| H0522 | txt | lexicon | 38 | 61 | +23 |
| H0525 | txt | lexicon | 53 | 79 | +26 |
| H0527 | txt | lexicon | 17 | 45 | +28 |
| H0528 | txt | lexicon | 134 | 157 | +23 |
| H0529 | txt | lexicon | 56 | 79 | +23 |
| H0530 | txt | lexicon | 45 | 78 | +33 |
| H0533 | txt | lexicon | 14 | 38 | +24 |
| H0534 | txt | lexicon | 42 | 61 | +19 |
| H0535 | txt | lexicon | 179 | 201 | +22 |
| H0536 | txt | lexicon | 12 | 34 | +22 |
| H0537 | txt | lexicon | 12 | 34 | +22 |
| H0538 | txt | lexicon | 48 | 69 | +21 |
| H0542 | txt | lexicon | 50 | 76 | +26 |
| H0543 | txt | lexicon | 29 | 51 | +22 |
| H0544 | txt | lexicon | 12 | 43 | +31 |
| H0545 | txt | lexicon | 72 | 102 | +30 |
| H0546 | txt | lexicon | 21 | 46 | +25 |
| H0547 | txt | lexicon | 61 | 84 | +23 |
| H0548 | txt | lexicon | 75 | 96 | +21 |
| H0551 | txt | lexicon | 21 | 46 | +25 |
| H0552 | txt | lexicon | 21 | 46 | +25 |
| H0553 | txt | lexicon | 381 | 407 | +26 |
| H0554 | txt | lexicon | 46 | 65 | +19 |
| H0555 | txt | lexicon | 8 | 35 | +27 |
| H0556 | txt | lexicon | 8 | 36 | +28 |
| H0561 | txt | lexicon | 49 | 71 | +22 |
| H0562 | txt | lexicon | 49 | 71 | +22 |
| H0563 | txt | lexicon | 4 | 27 | +23 |
| H0570 | txt | lexicon | 43 | 70 | +27 |
| H0572 | txt | lexicon | 60 | 85 | +25 |
| H0574 | txt | lexicon | 8 | 35 | +27 |
| H0575 | txt | lexicon | 73 | 92 | +19 |
| H0577 | txt | lexicon | 109 | 137 | +28 |
| H0578 | txt | lexicon | 14 | 39 | +25 |
| H0579 | txt | lexicon | 195 | 215 | +20 |
| H0584 | txt | lexicon | 69 | 89 | +20 |
| H0585 | txt | lexicon | 60 | 87 | +27 |
| H0587 | txt | lexicon | 47 | 70 | +23 |
| H0588 | txt | lexicon | 71 | 118 | +47 |
| H0589 | txt | lexicon | 48 | 76 | +28 |
| H0590 | txt | lexicon | 12 | 33 | +21 |
| H0591 | txt | lexicon | 32 | 55 | +23 |
| H0592 | txt | lexicon | 21 | 53 | +32 |
| H0594 | txt | lexicon | 27 | 55 | +28 |
| H0596 | txt | lexicon | 27 | 54 | +27 |
| H0599 | txt | lexicon | 123 | 144 | +21 |
| H0601 | txt | lexicon | 39 | 61 | +22 |
| H0602 | txt | lexicon | 74 | 95 | +21 |
| H0603 | txt | lexicon | 29 | 57 | +28 |
| H0604 | txt | lexicon | 100 | 122 | +22 |
| H0605 | txt | lexicon | 190 | 216 | +26 |
| H0610 | txt | lexicon | 20 | 45 | +25 |
| H0611 | txt | lexicon | 26 | 49 | +23 |
| H0614 | txt | lexicon | 20 | 50 | +30 |
| H0615 | txt | lexicon | 26 | 53 | +27 |
| H0616 | txt | lexicon | 53 | 78 | +25 |
| H0618 | txt | lexicon | 16 | 44 | +28 |
| H0624 | txt | lexicon | 78 | 103 | +25 |
| H0625 | txt | lexicon | 30 | 58 | +28 |
| H0626 | txt | lexicon | 23 | 53 | +30 |
| H0627 | txt | lexicon | 10 | 41 | +31 |
| H0628 | txt | lexicon | 39 | 67 | +28 |
| H0629 | txt | lexicon | 43 | 75 | +32 |
| H0631 | txt | lexicon | 280 | 300 | +20 |
| H0640 | txt | lexicon | 59 | 79 | +20 |
| H0642 | txt | lexicon | 370 | 393 | +23 |
| H0643 | txt | lexicon | 6 | 32 | +26 |
| H0644 | txt | lexicon | 84 | 104 | +20 |
| H0645 | txt | lexicon | 127 | 146 | +19 |
| H0646 | txt | lexicon | 320 | 341 | +21 |
| H0648 | txt | lexicon | 10 | 31 | +21 |
| H0650 | txt | lexicon | 46 | 69 | +23 |
| H0651 | txt | lexicon | 12 | 33 | +21 |
| H0652 | txt | lexicon | 62 | 86 | +24 |
| H0653 | txt | lexicon | 54 | 79 | +25 |
| H0655 | txt | lexicon | 31 | 62 | +31 |
| H0656 | txt | lexicon | 37 | 59 | +22 |
| H0659 | txt | lexicon | 20 | 46 | +26 |
| H0660 | txt | lexicon | 14 | 39 | +25 |
| H0661 | txt | lexicon | 48 | 72 | +24 |
| H0662 | txt | lexicon | 121 | 144 | +23 |
| H0664 | txt | lexicon | 95 | 130 | +35 |
| H0665 | txt | lexicon | 39 | 60 | +21 |
| H0666 | txt | lexicon | 17 | 42 | +25 |
| H0667 | txt | lexicon | 45 | 68 | +23 |
| H0668 | txt | lexicon | 45 | 74 | +29 |
| H0674 | txt | lexicon | 41 | 66 | +25 |
| H0678 | txt | lexicon | 46 | 67 | +21 |
| H0679 | txt | lexicon | 34 | 59 | +25 |
| H0680 | txt | lexicon | 140 | 163 | +23 |
| H0681 | txt | lexicon | 144 | 166 | +22 |
| H0685 | txt | lexicon | 29 | 57 | +28 |
| H0686 | txt | lexicon | 89 | 110 | +21 |
| H0688 | txt | lexicon | 60 | 87 | +27 |
| H0689 | txt | lexicon | 9 | 37 | +28 |
| H0691 | txt | lexicon | 89 | 108 | +19 |
| H0693 | txt | lexicon | 178 | 200 | +22 |
| H0694 | txt | lexicon | 36 | 57 | +21 |
| H0695 | txt | lexicon | 39 | 61 | +22 |
| H0696 | txt | lexicon | 54 | 76 | +22 |
| H0697 | txt | lexicon | 128 | 152 | +24 |
| H0698 | txt | lexicon | 23 | 49 | +26 |
| H0699 | txt | lexicon | 82 | 106 | +24 |
| H0700 | txt | lexicon | 67 | 96 | +29 |
| H0702 | txt | lexicon | 4 | 27 | +23 |
| H0705 | txt | lexicon | 5 | 32 | +27 |
| H0707 | txt | lexicon | 115 | 136 | +21 |
| H0708 | txt | lexicon | 13 | 39 | +26 |
| H0712 | txt | lexicon | 18 | 42 | +24 |
| H0713 | txt | lexicon | 18 | 47 | +29 |
| H0717 | txt | lexicon | 47 | 68 | +21 |
| H0719 | txt | lexicon | 56 | 80 | +24 |
| H0724 | txt | lexicon | 20 | 47 | +27 |
| H0727 | txt | lexicon | 69 | 89 | +20 |
| H0729 | txt | lexicon | 93 | 117 | +24 |
| H0730 | txt | lexicon | 100 | 121 | +21 |
| H0731 | txt | lexicon | 24 | 49 | +25 |
| H0732 | txt | lexicon | 175 | 198 | +23 |
| H0736 | txt | lexicon | 27 | 54 | +27 |
| H0737 | txt | lexicon | 44 | 67 | +23 |
| H0741 | txt | lexicon | 27 | 53 | +26 |
| H0750 | txt | lexicon | 43 | 61 | +18 |
| H0752 | txt | lexicon | 46 | 64 | +18 |
| H0753 | txt | lexicon | 86 | 109 | +23 |
| H0760 | txt | lexicon | 90 | 124 | +34 |
| H0762 | txt | lexicon | 52 | 81 | +29 |
| H0763 | txt | lexicon | 54 | 92 | +38 |
| H0766 | txt | lexicon | 15 | 37 | +22 |
| H0768 | txt | lexicon | 142 | 165 | +23 |
| H0769 | txt | lexicon | 124 | 149 | +25 |
| H0774 | txt | lexicon | 128 | 153 | +25 |
| H0779 | txt | lexicon | 215 | 237 | +22 |
| H0780 | txt | lexicon | 192 | 270 | +78 |
| H0781 | txt | lexicon | 85 | 109 | +24 |
| H0782 | txt | lexicon | 15 | 44 | +29 |
| H0786 | txt | lexicon | 19 | 44 | +25 |
| H0793 | txt | lexicon | 37 | 62 | +25 |
| H0794 | txt | lexicon | 17 | 43 | +26 |
| H0795 | txt | lexicon | 104 | 132 | +28 |
| H0799 | txt | lexicon | 60 | 87 | +27 |
| H0800 | txt | lexicon | 4 | 28 | +24 |
| H0807 | txt | lexicon | 61 | 89 | +28 |
| H0808 | txt | lexicon | 39 | 70 | +31 |
| H0809 | txt | lexicon | 96 | 126 | +30 |
| H0810 | txt | lexicon | 27 | 53 | +26 |
| H0811 | txt | lexicon | 59 | 86 | +27 |
| H0814 | txt | lexicon | 4 | 30 | +26 |
| H0815 | txt | lexicon | 13 | 44 | +31 |
| H0816 | txt | lexicon | 294 | 317 | +23 |
| H0817 | txt | lexicon | 149 | 181 | +32 |
| H0818 | txt | lexicon | 54 | 77 | +23 |
| H0819 | txt | lexicon | 154 | 182 | +28 |
| H0820 | txt | lexicon | 63 | 91 | +28 |
| H0821 | txt | lexicon | 37 | 66 | +29 |
| H0822 | txt | lexicon | 14 | 42 | +28 |
| H0823 | txt | lexicon | 48 | 93 | +45 |
| H0824 | txt | lexicon | 36 | 62 | +26 |
| H0827 | txt | lexicon | 63 | 88 | +25 |
| H0829 | txt | lexicon | 77 | 109 | +32 |
| H0833 | txt | lexicon | 308 | 331 | +23 |
| H0835 | txt | lexicon | 72 | 96 | +24 |
| H0837 | txt | lexicon | 9 | 34 | +25 |
| H0839 | txt | lexicon | 9 | 56 | +47 |
| H0842 | txt | lexicon | 205 | 268 | +63 |
| H0849 | txt | lexicon | 16 | 50 | +34 |
| H0851 | txt | lexicon | 146 | 207 | +61 |
| H0854 | txt | lexicon | 156 | 174 | +18 |
| H0855 | txt | lexicon | 11 | 36 | +25 |
| H0860 | txt | lexicon | 19 | 45 | +26 |
| H0861 | txt | lexicon | 7 | 34 | +27 |
| H0864 | txt | lexicon | 84 | 106 | +22 |
| H0865 | txt | lexicon | 215 | 243 | +28 |
| H0866 | txt | lexicon | 45 | 67 | +22 |
| H0868 | txt | lexicon | 98 | 120 | +22 |
| H0870 | txt | lexicon | 12 | 35 | +23 |
| H0871 | txt | lexicon | 54 | 85 | +31 |
| H0872 | txt | lexicon | 101 | 125 | +24 |
| H0874 | txt | lexicon | 94 | 121 | +27 |
| H0875 | txt | lexicon | 17 | 40 | +23 |
| H0877 | txt | lexicon | 18 | 43 | +25 |
| H0879 | txt | lexicon | 55 | 90 | +35 |
| H0883 | txt | lexicon | 92 | 136 | +44 |
| H0884 | txt | lexicon | 78 | 114 | +36 |
| H0885 | txt | lexicon | 155 | 211 | +56 |
| H0887 | txt | lexicon | 289 | 312 | +23 |
| H0889 | txt | lexicon | 18 | 44 | +26 |
| H0890 | txt | lexicon | 53 | 84 | +31 |
| H0891 | txt | lexicon | 55 | 89 | +34 |
| H0892 | txt | lexicon | 28 | 52 | +24 |
| H0894 | txt | lexicon | 149 | 173 | +24 |
| H0898 | txt | lexicon | 129 | 163 | +34 |
| H0900 | txt | lexicon | 58 | 89 | +31 |
| H0901 | txt | lexicon | 22 | 51 | +29 |
| H0906 | txt | lexicon | 18 | 40 | +22 |
| H0907 | txt | lexicon | 32 | 56 | +24 |
| H0908 | txt | lexicon | 84 | 107 | +23 |
| H0909 | txt | lexicon | 118 | 140 | +22 |
| H0910 | txt | lexicon | 90 | 115 | +25 |
| H0913 | txt | lexicon | 44 | 64 | +20 |
| H0914 | txt | lexicon | 336 | 361 | +25 |
| H0915 | txt | lexicon | 43 | 67 | +24 |
| H0916 | txt | lexicon | 23 | 53 | +30 |
| H0918 | txt | lexicon | 34 | 60 | +26 |
| H0919 | txt | lexicon | 43 | 69 | +26 |
| H0922 | txt | lexicon | 22 | 45 | +23 |
| H0923 | txt | lexicon | 45 | 73 | +28 |
| H0925 | txt | lexicon | 28 | 52 | +24 |
| H0926 | txt | lexicon | 418 | 441 | +23 |
| H0927 | txt | lexicon | 97 | 120 | +23 |
| H0928 | txt | lexicon | 36 | 64 | +28 |
| H0929 | txt | lexicon | 117 | 141 | +24 |
| H0931 | txt | lexicon | 53 | 86 | +33 |
| H0933 | txt | lexicon | 42 | 66 | +24 |
| H0934 | txt | lexicon | 197 | 227 | +30 |
| H0936 | txt | lexicon | 96 | 119 | +23 |
| H0937 | txt | lexicon | 93 | 116 | +23 |
| H0939 | txt | lexicon | 8 | 36 | +28 |
| H0943 | txt | lexicon | 80 | 104 | +24 |
| H0944 | txt | lexicon | 18 | 43 | +25 |
| H0945 | txt | lexicon | 94 | 115 | +21 |
| H0947 | txt | lexicon | 318 | 341 | +23 |
| H0948 | txt | lexicon | 54 | 82 | +28 |
| H0949 | txt | lexicon | 121 | 145 | +24 |
| H0950 | txt | lexicon | 9 | 38 | +29 |
| H0951 | txt | lexicon | 8 | 36 | +28 |
| H0952 | txt | lexicon | 102 | 125 | +23 |
| H0954 | txt | lexicon | 311 | 335 | +24 |
| H0955 | txt | lexicon | 5 | 31 | +26 |
| H0958 | txt | lexicon | 36 | 62 | +26 |
| H0961 | txt | lexicon | 12 | 39 | +27 |
| H0962 | txt | lexicon | 145 | 169 | +24 |
| H0963 | txt | lexicon | 8 | 39 | +31 |
| H0964 | txt | lexicon | 76 | 111 | +35 |
| H0965 | txt | lexicon | 26 | 54 | +28 |
| H0966 | txt | lexicon | 87 | 111 | +24 |
| H0967 | txt | lexicon | 66 | 90 | +24 |
| H0969 | txt | lexicon | 43 | 70 | +27 |
| H0970 | txt | lexicon | 16 | 41 | +25 |
| H0971 | txt | lexicon | 24 | 48 | +24 |
| H0972 | txt | lexicon | 46 | 72 | +26 |
| H0974 | txt | lexicon | 190 | 211 | +21 |
| H0975 | txt | lexicon | 10 | 40 | +30 |
| H0976 | txt | lexicon | 22 | 49 | +27 |
| H0977 | txt | lexicon | 111 | 134 | +23 |
| H0979 | txt | lexicon | 5 | 33 | +28 |
| H0980 | txt | lexicon | 131 | 159 | +28 |
| H0981 | txt | lexicon | 140 | 169 | +29 |
| H0982 | txt | lexicon | 202 | 224 | +22 |
| H0983 | txt | lexicon | 35 | 60 | +25 |
| H0984 | txt | lexicon | 71 | 95 | +24 |
| H0985 | txt | lexicon | 27 | 53 | +26 |
| H0986 | txt | lexicon | 23 | 51 | +28 |
| H0987 | txt | lexicon | 16 | 47 | +31 |
| H0989 | txt | lexicon | 52 | 74 | +22 |
| H0991 | txt | lexicon | 32 | 56 | +24 |
| H0992 | txt | lexicon | 65 | 96 | +31 |
| H0993 | txt | lexicon | 74 | 102 | +28 |
| H0994 | txt | lexicon | 94 | 114 | +20 |

## 15 veletlen minta ellenorzese -- lexicon-valtozat minosege a txt-hez kepest

(`random.seed(42)`, a fenti 509-es listabol vett minta, novekvo Strong-sorrendben.)
Mind a 15 esetben a lexicon-valtozat **jobb**: minden esetben tartalmazza a
teljes txt-szoveget VALTOZATLANUL, plusz a heber lemmat es a POS-kodot
(pl. `[H:N-F]`) elore teve -- tisztan bovites, adatvesztes egyik esetben sem
tortent. Osszesites: **15/15 jobb, 0 azonos, 0 rosszabb** -- nincs megallasra
ok, a csere nem igenyel tovabbi vizsgalatot vagy javitast.

| kulcs | verdikt | egy mondatos indoklas |
|---|---|---|
| H0019 | jobb | A lexicon megtartja a teljes txt-glosszat, es hozzateszi a heber lemmat (`אִבְחָה`) es a `[H:N-F]` POS-kodot. |
| H0093 | jobb | A 4 karakteres txt-glossza ("nuts") a lexicon-ban lemmaval, POS-koddal es rovid gloss-elovezetovel egeszul ki, adatvesztes nelkul. |
| H0102 | jobb | A teljes txt-definicio valtozatlanul bekerul, csak a lemma (`אֲגַף`) es POS-kod elozi meg. |
| H0109 | jobb | A hosszabb, tobb-agu (1, 1a) txt-definicio szoveghelyesen megjelenik, kiegeszitve a lemmaval es igetorzs-jelolessel (`[H:V]`). |
| H0145 | jobb | A ket ertelmet felsorolo txt-szoveg valtozatlan, a lexicon csak a lemmat (`אֶ֫דֶר`) es a `[H:N]` kodot teszi ele. |
| H0234 | jobb | A hosszu, technikai txt-definicio ("memorial-offering...") sertetlenul megmarad, a lexicon lemmaval es POS-koddal bovit. |
| H0248 | jobb | A minimalis "arm" txt-glossza a lexicon-ban lemmaval (`אֶזְרוֹעַ`) es POS-koddal egeszul ki, tartalmi veszteseg nelkul. |
| H0307 | jobb | A tulajdonnev-magyarazat (Achmetha/Ecbatana) teljes egeszeben megmarad; a lexicon a nevet ket helyen is kozli (lemma + `Ecbatana` gloss), ami redundans, de nem hibas vagy hianyos. |
| H0570 | jobb | A ket-jelentesu txt-definicio valtozatlan, a lexicon lemmaval (`אֶ֫מֶשׁ`) es hatarozoi POS-koddal (`[H:ADV]`) bovit. |
| H0610 | jobb | A rovid txt-glossza teljesen megmarad, csak lemma es POS-kod kerul ele. |
| H0656 | jobb | A `(Qal)` igealak-jeloles es a teljes definicio valtozatlan, a lexicon lemmaval es `[H:V]` koddal egeszit ki. |
| H0691 | jobb | A harom-agu (CLBL/BDB/TWOT) txt-magyarazat tartalmilag megmarad; a "form and meaning uncertain" (txt) es "dubious" (lexicon) szohasznalati elteres jelentestanilag egyenertekű, nem informaciovesztes. |
| H0763 | jobb | A helynev-magyarazat (Aram-naharaim/Mesopotamia) teljes egeszeben megmarad, a lexicon lemmaval es a nev ismetelt feltuntetesevel bovit. |
| H0768 | jobb | A hosszu, magyarazo labjegyzetes ("arnebeth") txt-definicio szo szerint atkerul, a lexicon csak lemmat es POS-kodot ad hozza. |
| H0923 | jobb | A koszikla-leiras (porphyry, red marble) valtozatlan, a lexicon lemmaval (`בַּ֫הַט`) es POS-koddal bovit. |
