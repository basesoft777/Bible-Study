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

## Javaslat

A minta jelenlegi formajaban (`^H\d{4}$`) helyesen zarja ki a H9xxx
morfologiai tartomanyt es a TBESH.lexicon ervenytelen index-kulcsait
(`H9`, `H90`, `H900`), de mellekhatasakent a fenti 35 nem-toltott, egyedi
Strong-kulcsot is kidobja. Javitas: a szuro elott a Strong-kulcsot
nullaval-kitoltes-normalizalni kellene (`H%d` -> `H%04d`, azaz `re.sub`
vagy `zfill(4)` a szamresz-en), MIELOTT a 4-jegyu es H9xxx-teszt lefut --
igy a 964 artalmatlan duplikatum egyszeruen eggye olvadna a mar meglevo
toltott parjaval, a 35 egyedi pedig bekerulne a tablaba toltott formaban
(`H0122` stb.). Ez kulon tetelkent (S1.5 vagy uj N-tetel) vihetne be a
`tbesh_konszolidalt_import.py`-ba; jelen jelentes csak ellenorzes, a
tablat nem irja at.
