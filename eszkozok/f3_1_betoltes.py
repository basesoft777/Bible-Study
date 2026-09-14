# -*- coding: utf-8 -*-
"""
F3.1 retroaktiv betoltes -- konnyu csoport (Melkizedek KIRALY-001,
Segitsegul hivni / ISTENTISZT-001) + a 4.6 gate visszamenoleges
alkalmazasa + haromertekue statusz bevezetese.

Egyszeri, kezi futtatasu szkript -- NEM resze a lekerdez.py/betolt.py
eszkoztarnak, csak ennek az F3.1 menetnek a jegyzokonyve, hogy a
betoltes reprodukalhato es ellenorizheto legyen. Minden sor eloszor
osszeall memoriaban es hossz-ellenorzesen at kell mennie, csak utana
irodik lemezre -- igy egyetlen elgepelt mezoszam sem torhet el csendben
egy TSV-oszlopot.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, "adat")


def prov(forras, ts):
    return "scope=manual | forras=%s | ts=%s" % (forras, ts)


MELK_STUDY = "Melkizedek_tematikus.md"
IST_STUDY = "Segitsegul_hivni_az_Urat_tematikus.md"

# ---------------------------------------------------------------------
# 1. motivumok.tsv -- ket sor, haromertekue statusszal es a 4.6 gate
#    mezoivel
# ---------------------------------------------------------------------

motivumok = [
    (
        "KIRALY-001",
        "Melkizedek — király-pap rendje, kenyér és bor",
        "Melkizedek-rend",
        "Krisztológia",
        "Drash/Sod",
        "publikálható",
        "v2",
        "2026.09.10",
        "lexikai",
        "az igehelynek vagy név szerint Melkizedeket kell megneveznie/rá hivatkoznia (a \"rendje szerint\" formulával), vagy a BDB H3548 \"priest-king\" lexikai sense alá kell tartoznia — a puszta \"pap\" vagy \"király\" cím külön-külön nem elég (l. a BDB \"chieftain (exercising priestly functions)\" alkategória kizárása, Jetró/Dávid fiai/Ira)",
        "papi és királyi tisztség kombinációja általában (bármely \"pap-király\" szereplő, Melkizedekre/a H3548 priest-king sense-re való hivatkozás nélkül)",
        "v12",
        "tematikus_lezart/Melkizedek_tematikus.md",
    ),
    (
        "ISTENTISZT-001",
        "Segítségül hívni az Úr nevét",
        "Névbe vetett segítségülhívás",
        "Pneumatológia/istentisztelet",
        "Drash",
        "publikálható",
        "v2",
        "2026.09.09",
        "formulaikus",
        "az igehelynek a קָרָא + בְּ (aktív, invokáló szerkezet: \"[valaki] hívja segítségül [Isten nevét]\") mintát kell mutatnia — a passzív נִקְרָא...עַל szerkezet (birtoklás/hovatartozás kifejezése, nem invokáció) kizárja a besorolást, még akkor is, ha ugyanazt a két gyököt használja (l. D-minta, 2Sám 6:2, Jer 7:10-14, 5Móz 28:10, ÚSZ-párja Zsid 11:16)",
        "istentisztelet/imádság általában (bármely invokációs forma, a קָרָא בְשֵׁם formulán kívül)",
        "v12",
        "tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md;motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md",
    ),
]

# ---------------------------------------------------------------------
# 2. elofordulasok.tsv -- KIRALY-001 (9 sor) + ISTENTISZT-001 (29 sor)
#    Minden sorhoz proveniencia = manual (l. adat/SEMA.md 1.5) — a
#    Melkizedek/Segitsegul hivni audit a lekerdez.py (F2) elkeszulte
#    elott, kezzel/web_search-csel futott.
# ---------------------------------------------------------------------

kiraly_rows = [
    (
        "KIRALY-001", "1Móz 14:18-20",
        "Melkizedek, Sálem királya, egyszerre \"a Felséges Isten papja\" — kenyeret és bort hoz, megáldja Ábrámot, aki tizedet ad neki. Első előfordulás, minden előzmény és genealógia nélkül.",
        "Pshat", "🌱 alap-előfordulás — a motívum legelső megjelenése",
        "H3548", "H3548", "H3548", "1", "priest-king", "pap-király",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsolt 76:3",
        "\"Sálemben van az ő sátora, és lakóhelye Sionban\" — a Sálem=Jeruzsálem/Sion azonosítás, ugyanazzal a Strong-számmal (H8004), mint 1Móz 14:18-nál — lexikai, nem csak tematikus kapcsolat.",
        "Remez", "helynév-azonosítás, lexikai kapocs",
        "H8004", "H8004", "H8004", "", "", "helynév, Jeruzsálem rövidüléseként/archaizáló neveként; a BDB explicit Zsolt 76:3-at idézi Gen 14:18 mellett",
        "", "", "", prov(MELK_STUDY, "2026-09-09"),
    ),
    (
        "KIRALY-001", "2Móz 19:6",
        "\"Ti pedig lesztek nékem papok királysága\" — a Sínai-szövetségben Izráel egésze kap kollektív király-pap identitást, a lévita papság intézményesítése előtt. Ugyanaz a כֹּהֵן gyök, mint Melkizedeknél, de itt nem egy egyén, hanem egy egész nép viseli.",
        "Remez", "egyéni → kollektív szintre emelve",
        "H3548", "H3548+H4467", "H3548", "1", "priests and kings at once in their relation to the nations", "egyszerre papok és királyok a nemzetekhez való viszonyukban",
        "papok", "tartalom-alapú", "magas", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsolt 110:4",
        "\"Megesküdt az Úr és meg nem másítja: Te vagy pap örökké Melkhisédek rendje szerint\" — próféciai eskü-formula, dávidi/individuális szintre visszavéve a mintát.",
        "Remez", "próféciai megerősítés, dávidi szintre szűkítve",
        "H3548", "H3548", "H3548", "1", "Messianic priest-king like Melchizedek", "messiási pap-király, mint Melkizedek",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zak 6:13",
        "\"pap lesz az ő királyi székén\" — próféciai kép egyetlen alakról, aki egyszerre ül a trónon és visel papi tisztséget.",
        "Remez", "explicit \"pap a trónon\" kép, próféciai megerősítés",
        "H3548", "H3548+H3678", "H3548", "1", "Messianic priest and king", "messiási pap és király",
        "pap", "tartalom-alapú", "magas", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsid 5:6",
        "A Zsolt 110:4 első idézetei, bevezetve Krisztus főpapságának témáját.",
        "Drash", "krisztológiai betöltés, első idézet",
        "G5010", "", "", "", "", "",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsid 5:10",
        "A Zsolt 110:4 idézése, Krisztus főpapságának bevezetése.",
        "Drash", "krisztológiai betöltés",
        "G5010", "", "", "", "", "",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsid 6:20",
        "A Zsolt 110:4 idézése, Krisztus \"örökkévaló főpap Melkhisédek rendje szerint\" bevezetése.",
        "Drash", "krisztológiai betöltés",
        "G5010", "", "", "", "", "",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
    (
        "KIRALY-001", "Zsid 7:1-28",
        "A Melkizedek-rend teljes kifejtése: nagyobb a lévita rendnél (a tized-jelenetből levezetve), örökkévaló (argumentum e silentio), a törvény megváltozásának alapja.",
        "Drash/Sod", "krisztológiai betöltés, teljes kifejtés",
        "G5010", "G5010+G0813+G0282", "", "", "", "",
        "", "", "", prov(MELK_STUDY, "2026-09-08"),
    ),
]

istentiszt_rows = [
    ("ISTENTISZT-001", "1Móz 4:26",
     "A formula első előfordulása — Séth fia, Énós nemzedéke; a Kain-vonal önerős civilizációépítése utáni korszakváltás jele.",
     "Drash", "🌱 alap-előfordulás — a motívum legelső megjelenése a kánonban, minden későbbi eset erre vezethető vissza",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "call with name of Yahweh (i.e. use it in invocation)", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Móz 12:8",
     "Ábrám, Bétel-Ai között — oltárépítés + segítségül hívás első összekapcsolása.",
     "Drash", "🔁 ismétlődés — a formula második, még nem rögzült szokásként ismétlődő megjelenése",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Móz 13:4",
     "Ábrám visszatér ugyanahhoz az oltárhoz Egyiptomból; a formula tudatos, felkeresett szokássá válik.",
     "Drash", "⭐ küszöb-előfordulás — a 3. genezisi eset, ami miatt a motívum elérte az önálló tematikus feldolgozáshoz szükséges gyakoriságot",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Móz 21:33",
     "Ábrahám, Beérseba — a formula kiegészül egy isteni jelzővel: אֵל עוֹלָם, \"örökkévaló Isten\".",
     "", "➕ bővülés — a formula első alkalommal egészül ki isteni jelzővel, új teológiai tartalmat hordozva",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Móz 26:25",
     "Izsák, Beérseba — a minta szó szerint átöröklődik a második pátriárka-nemzedékre, ugyanazon a helyszínen.",
     "", "👨‍👦 öröklés — a gyakorlat generációk között, tudatos folytonossággal adódik át",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Kir 18:24",
     "Illés a Kármelen: \"ti a ti isteneitek nevét hívjátok, és én segítségül hívom az Úr nevét\" — nyilvános, versengő kontextus, a kontraszt magán a versen belül.",
     "Remez", "⚔️ nyilvános versengés — a formula először jelenik meg nyilvános, két isten közötti próbatételi kontextusban",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "specific appeal to Yahweh to display his power", "Jahve nevével, konkrét felszólítás hatalma megmutatására",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Kir 18:25",
     "A Baál-próféták felszólítása: \"hívjátok segítségül a ti istenetek nevét\".",
     "Remez", "⚔️ nyilvános versengés (folytatás) — a próbatétel gyakorlati végrehajtása",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "with name of Baal", "Baál nevével",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Kir 18:26",
     "A Baál-próféták ismétlődő, sikertelen invokációja — a formula kudarca a kontraszt kiteljesedése.",
     "Remez", "⚔️ nyilvános versengés (folytatás) — a próbatétel kudarca",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "with name of Baal", "Baál nevével",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "2Kir 5:11",
     "Naámán elvárása Elizeus felől — a formula ismertsége a nem-izraeli szereplő szájában is.",
     "Remez", "🔁 ismétlődés, kívülálló szemszögéből",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Sof 3:9",
     "Eszkatológiai ígéret — a népek megtisztított ajka egy akarattal hívja segítségül az Urat.",
     "Remez", "🔮 eszkatológiai kitekintés — a formula jövőbeli, univerzális beteljesedésének előrevetítése",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c (rokon)", "", "",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Zak 13:9",
     "Sof 3:9 párja: a megtisztított maradék segítségül hívja Isten nevét, és Isten válaszol — kétirányú szövetségi megerősítés.",
     "Remez", "🔮 eszkatológiai kitekintés (folytatás) — kétirányú szövetségi megerősítéssé bővíti az ígéretet",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "",
     "segítségül hívja ... nevemet", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "Zsolt 116:4",
     "A zsoltáros saját, személyes hála-könyörgésének első megfogalmazása: \"segítségül hívom az Úr nevét\".",
     "Remez", "🔁 ismétlődés, személyes könyörgésben",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Zsolt 116:13",
     "A formula második, szó szerinti megismétlése ugyanabban a zsoltárban, a \"szabadulás poharának\" felemelése kontextusában.",
     "Remez", "🔁 ismétlődés, személyes könyörgésben",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Zsolt 116:17",
     "A formula harmadik megismétlése, hála-áldozat felajánlása kontextusában.",
     "Remez", "🔁 ismétlődés, személyes könyörgésben",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Jóel 2:32",
     "Az ószövetségi megfogalmazás csúcspontja: \"mindaz, aki segítségül hívja az Úr nevét, megmenekül\" — ezt Péter (ApCsel 2:21) és Pál (Róm 10:13) is szó szerint idézi. Károli-számozás: Jóel 3:5.",
     "Remez", "🎯 előkép/beteljesedés — az ÓSZ-i ígéret, amit az ÚSZ tételesen, szó szerint idéz",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Róm 10:14",
     "Pál közvetlenül folytatja az érvelést: \"Mimódon hívják segítségül, a kiben nem hittek?\" — ugyanaz a görög ige, mint 10:13-nál.",
     "Remez", "🎯 előkép/beteljesedés (folytatás) — Pál közvetlenül továbbviszi az érvelést ugyanabban a szakaszban",
     "G1941", "G1941", "", "", "", "",
     "hívják segítségül", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-06")),
    ("ISTENTISZT-001", "1Kor 1:2",
     "\"…mindazokkal egybe, a kik a mi Urunk Jézus Krisztus nevét segítségül hívják bármely helyen\" — a formula első explicit alkalmazása Krisztusra, a gyülekezet önmeghatározása.",
     "Remez", "🎯 előkép/beteljesedés (kiterjesztés) — a formula önálló egyházi azonosító-formulává válik",
     "G1941", "G1941", "", "", "", "",
     "segítségül hívják", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "2Tim 2:22",
     "\"…azokkal egyetembe, a kik segítségül hívják az Urat tiszta szívből\" — a segítségül hívás mint közösségválasztási kritérium.",
     "Remez", "🎯 előkép/beteljesedés (kiterjesztés) — a formula önálló egyházi azonosító-formulává válik",
     "G1941", "G1941", "", "", "", "",
     "segítségül hívják", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "1Pét 1:17",
     "\"…ha Atyának hívjátok őt…\" — az invokáció \"Atya\" megszólításra alkalmazva; a görög ige azonos, a Károli nem tartja meg a \"segítségül\" szót.",
     "Remez", "🎯 előkép/beteljesedés (kiterjesztés) — a formula önálló egyházi azonosító-formulává válik",
     "G1941", "G1941", "", "", "", "",
     "hívjátok", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "ApCsel 9:14",
     "\"…mindazokat…, kik a te nevedet segítségül hívják\" — Saul üldözési célpontjainak leírása, a korai keresztények azonosító megnevezése.",
     "Remez", "🎯 előkép/beteljesedés (kiterjesztés) — a formula önálló egyházi azonosító-formulává válik",
     "G1941", "G1941", "", "", "", "",
     "segítségül hívják", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "ApCsel 9:21",
     "\"…a kik ezt a nevet hívják segítségül\" — az ApCsel 9:14-es leírás közvetlen megismétlése ugyanabban a fejezetben.",
     "Remez", "🔁 ismétlődés — az ApCsel 9:14-es leírás közvetlen megismétlése",
     "G1941", "G1941", "", "", "", "",
     "hívják segítségül", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "ApCsel 22:16",
     "\"…segítségül híván az Úrnak nevét\" — Pál saját megtérés-elbeszélésében, a keresztséggel összekapcsolva.",
     "Remez", "🎯 előkép/beteljesedés (kiterjesztés) — a formula önálló egyházi azonosító-formulává válik",
     "G1941", "G1941", "", "", "", "",
     "segítségül híván", "tartalom-alapú", "magas", prov(IST_STUDY, "2026-09-08")),
    ("ISTENTISZT-001", "Zsolt 105:1",
     "\"Hívjátok segítségül az ő nevét, hirdessétek a népek közt az ő cselekedeteit\" — a genezisi hagyományból örökölt formula önálló, liturgikus felhasználása, nem a történetszál narratív folytatása.",
     "Remez", "⇄ párhuzam — formulai/liturgikus örökség a genezisi hagyományból, nem narratív folytonosság",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "1Krón 16:8",
     "A Zsolt 105:1 szinte szó szerinti megismétlése a frigyláda Sátor elé állításának liturgiájában.",
     "Remez", "⇄ párhuzam — formulai/liturgikus örökség a genezisi hagyományból, nem narratív folytonosság",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Ézs 12:4",
     "Szó szerint majdnem azonos a Zsolt 105:1-gyel, eszkatológiai hálaének kontextusban.",
     "Remez", "⇄ párhuzam — formulai/liturgikus örökség a genezisi hagyományból, nem narratív folytonosság",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c", "", "invokálni, segítségül hívni",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Jer 10:25",
     "\"…a nemzetségekre, akik a Te nevedet nem hívják segítségül\" — a formula tagadó, vádló formában, fordított szórenddel.",
     "Remez", "⇄🚫 párhuzam, tagadó forma — a formula elmulasztása mint vád, fordított szórenddel",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c (tagadva)", "", "invokálni — tagadó szerkezetben, a mulasztás vádjaként",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "Zsolt 79:6",
     "A Jer 10:25 szinte szó szerinti párhuzama, azonos vádló szerkezettel.",
     "Remez", "⇄🚫 párhuzam, tagadó forma — a formula elmulasztása mint vád, fordított szórenddel",
     "H7121+H8034", "H7121+H8034", "H7121", "2.c (tagadva)", "", "invokálni — tagadó szerkezetben, a mulasztás vádjaként",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "2Móz 33:19",
     "Isten maga jelenti ki Mózesnek: \"kihirdetem előtted az Úr nevét\" — nem az ember hívja segítségül Isten nevét, hanem Isten mondja ki a sajátját.",
     "Remez", "❓ be nem sorolható — a szereplők szerepe felcserélődik, egyik meglévő kategóriába sem illik tisztán (A/B/C tipológia, B-eset)",
     "H7121+H8034", "H7121+H8034", "H7121", "3", "proclaim", "kihirdetni, kinyilatkoztatni (NEM invokáció)",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
    ("ISTENTISZT-001", "2Móz 34:5",
     "Ugyanaz a jelenet folytatása: \"az Úr nevében kiáltott\" — Isten végrehajtja az előző fejezetben megígért önkihirdetést.",
     "Remez", "❓ be nem sorolható — a szereplők szerepe felcserélődik, egyik meglévő kategóriába sem illik tisztán (A/B/C tipológia, B-eset)",
     "H7121+H8034", "H7121+H8034", "H7121", "3", "proclaim", "kihirdetni, kinyilatkoztatni (NEM invokáció)",
     "", "", "", prov(IST_STUDY, "2026-09-05")),
]

# ---------------------------------------------------------------------
# 3. jeloltek.tsv -- integritasi szabaly 2 (SEMA.md 3.2): minden
#    elofordulasok sorhoz tartozzon jeloltek sor, dontes=beépítve.
# ---------------------------------------------------------------------

jeloltek_rows = []
for row in kiraly_rows + istentiszt_rows:
    id_, igehely, kapcsolodas = row[0], row[1], row[2]
    prov_str = row[-1]
    ts = prov_str.split("ts=")[1]
    datum = ts.replace("-", ".")
    forras_kereses = (
        "négyforrásos audit (TAHOT/TAGNT/TSK/Károli-Strong), retroaktív F3.1 betöltés"
        if id_ == "KIRALY-001" else
        "pozíció-alapú frázis-keresés + BDB/TSK/LXX audit, retroaktív F3.1 betöltés"
    )
    karoli_szo, azon_mod, megb = row[10], row[11], row[12]
    jeloltek_rows.append((
        id_, igehely, forras_kereses, "beépítve", kapcsolodas,
        karoli_szo, azon_mod, megb, datum,
    ))

# ---------------------------------------------------------------------
# 4. kapcsolatok.tsv -- KIRALY-001 (TSK-igazolt párok) + ISTENTISZT-001
#    (a study 1/b táblázata, Típus-mező v1 szerint)
# ---------------------------------------------------------------------

kiraly_kapcsolatok = [
    ("1Móz 14:18-20", "2Móz 19:6", "KIRALY-001", "Párhuzam", "egyéni eset → kollektív, nemzeti szintre emelve, lévita rend előtt", "magas", "Remez"),
    ("1Móz 14:18-20", "Zsolt 110:4", "KIRALY-001", "Előkép", "egyszeri esemény → örökkévaló, próféciai \"rendé\" emelve; TSK 14 szavazat", "magas", "Remez"),
    ("Zsolt 110:4", "Zak 6:13", "KIRALY-001", "Párhuzam", "próféciai visszautalás → explicit \"pap a trónon\" kép; TSK 9 szavazat", "magas", "Remez"),
    ("1Móz 14:18-20", "Zak 6:13", "KIRALY-001", "Párhuzam", "közös H3548 priest-king sense; TSK csak 2 szavazat, gyenge megerősítés", "közepes", "Remez"),
    ("2Móz 19:6", "1Pét 2:9", "KIRALY-001", "Beteljesedés", "szó szerinti LXX-idézés (βασίλειον ἱεράτευμα); TSK 22 szavazat", "magas", "Drash"),
    ("Zsolt 110:4", "Zsid 5:6", "KIRALY-001", "Beteljesedés", "a Zsolt 110:4 első idézete, Krisztus főpapságának bevezetése", "magas", "Drash"),
    ("Zsolt 110:4", "Zsid 5:10", "KIRALY-001", "Beteljesedés", "a Zsolt 110:4 idézése", "magas", "Drash"),
    ("Zsolt 110:4", "Zsid 6:20", "KIRALY-001", "Beteljesedés", "a Zsolt 110:4 idézése", "magas", "Drash"),
    ("Zsolt 110:4", "Zsid 7:1-28", "KIRALY-001", "Beteljesedés", "a Melkizedek-rend teljes kifejtése, a Zsolt 110:4 nyomán", "magas", "Drash/Sod"),
]

istentiszt_kapcsolatok = [
    ("1Móz 4:26", "Sof 3:9", "ISTENTISZT-001", "Párhuzam", "azonos szereposztás (ember hívja segítségül Isten nevét), más kánoni ponton", "magas", "Remez"),
    ("1Móz 4:26", "2Kir 5:11", "ISTENTISZT-001", "Párhuzam", "azonos szereposztás, parafrazált formában — nincs szó szerinti egyezés", "közepes", "Remez"),
    ("1Móz 4:26", "Jóel 2:32", "ISTENTISZT-001", "Párhuzam", "azonos szereposztás, az ószövetségi megfogalmazás csúcspontjáig", "magas", "Remez"),
    ("Jóel 2:32", "Róm 10:14", "ISTENTISZT-001", "Beteljesedés", "szó szerinti LXX-idézés-lánc (2:32⇒Róm 10:13⇒10:14)", "magas", "Remez"),
    ("Róm 10:14", "1Kor 1:2", "ISTENTISZT-001", "Párhuzam", "azonos görög ige (ἐπικαλέομαι), egyházi azonosító-formulává válás — nincs szó szerinti idézés", "közepes", "Remez"),
    ("Róm 10:14", "2Tim 2:22", "ISTENTISZT-001", "Párhuzam", "azonos görög ige, egyházi azonosító-formulává válás", "közepes", "Remez"),
    ("Róm 10:14", "1Pét 1:17", "ISTENTISZT-001", "Párhuzam", "azonos görög ige, egyházi azonosító-formulává válás", "közepes", "Remez"),
    ("Róm 10:14", "ApCsel 9:14", "ISTENTISZT-001", "Párhuzam", "azonos görög ige, üldözési kontextus", "közepes", "Remez"),
    ("ApCsel 9:14", "ApCsel 9:21", "ISTENTISZT-001", "Párhuzam", "szó szerinti megismétlés ugyanabban a fejezetben", "magas", "Remez"),
    ("Róm 10:14", "ApCsel 22:16", "ISTENTISZT-001", "Párhuzam", "azonos görög ige, megtérés-elbeszélés", "közepes", "Remez"),
    ("1Móz 4:26", "2Móz 33:19", "ISTENTISZT-001", "Variáns", "A/B/C tipológia B-esete — azonos szerkezet (קָרָא+שֵׁם), felcserélt alany/tárgy (Isten mondja ki a saját nevét)", "magas", "Remez"),
    ("2Móz 33:19", "2Móz 34:5", "ISTENTISZT-001", "Párhuzam", "ugyanaz a jelenet, ugyanaz a szereposztás (Isten önkinyilatkoztatása)", "magas", "Remez"),
    ("1Móz 12:8", "1Móz 13:4", "ISTENTISZT-001", "Párhuzam", "Ábrám explicit visszatér ugyanahhoz az oltárhoz", "magas", "Drash"),
    ("1Móz 13:4", "1Móz 26:25", "ISTENTISZT-001", "Párhuzam", "öröklés — azonos szereposztás nemzedékek közt, azonos helyszín (Beérseba)", "magas", "Drash"),
    ("1Móz 21:33", "1Móz 26:25", "ISTENTISZT-001", "Párhuzam", "öröklés — azonos szereposztás nemzedékek közt, azonos helyszín", "magas", "Drash"),
    ("1Kir 18:24", "1Kir 18:25", "ISTENTISZT-001", "Párhuzam", "egyazon pericope közvetlenül egymást követő versei", "magas", "Remez"),
    ("1Kir 18:25", "1Kir 18:26", "ISTENTISZT-001", "Párhuzam", "egyazon pericope közvetlenül egymást követő versei", "magas", "Remez"),
    ("Zsolt 116:4", "Zsolt 116:13", "ISTENTISZT-001", "Párhuzam", "egyazon zsoltáros, szó szerinti ismétlés", "magas", "Remez"),
    ("Zsolt 116:13", "Zsolt 116:17", "ISTENTISZT-001", "Párhuzam", "egyazon zsoltáros, szó szerinti ismétlés", "magas", "Remez"),
    ("Zsolt 105:1", "1Krón 16:8", "ISTENTISZT-001", "Párhuzam", "csaknem szó szerint azonos szöveg (1Krón 16 a Zsolt 105/96/106 összeállítását idézi)", "magas", "Remez"),
    ("Zsolt 105:1", "Ézs 12:4", "ISTENTISZT-001", "Párhuzam", "szinte szó szerinti egyezés a formulában", "magas", "Remez"),
    ("Jer 10:25", "Zsolt 79:6", "ISTENTISZT-001", "Párhuzam", "csaknem szóról szóra azonos, tagadó forma; Károli-KH mindkét irányban megerősíti", "magas", "Remez"),
    ("Sof 3:9", "Zak 13:9", "ISTENTISZT-001", "Párhuzam", "azonos szereposztás, kétirányú megerősítéssel kiegészítve", "magas", "Remez"),
]

kapcsolatok_rows = kiraly_kapcsolatok + istentiszt_kapcsolatok

# ---------------------------------------------------------------------
# 5. Hossz-ellenorzes MINDEN sorra, MIELOTT barmit is irnank -- igy egy
#    elgepelt mezoszam kivetellel all le, nem csendes oszlop-eltolassal.
# ---------------------------------------------------------------------

for _r in motivumok:
    assert len(_r) == 13, ("motivumok sor hossza nem 13: %r" % (_r,))
for _r in kiraly_rows:
    assert len(_r) == 15, ("KIRALY elofordulas sor hossza nem 15: %r" % (_r,))
for _r in istentiszt_rows:
    assert len(_r) == 15, ("ISTENTISZT elofordulas sor hossza nem 15: %r" % (_r,))
for _r in jeloltek_rows:
    assert len(_r) == 9, ("jeloltek sor hossza nem 9: %r" % (_r,))
for _r in kapcsolatok_rows:
    assert len(_r) == 7, ("kapcsolatok sor hossza nem 7: %r" % (_r,))

# Kulcs-egyedisegi ellenorzes (id + igehely) az elofordulasok.tsv-hez.
elof_all = kiraly_rows + istentiszt_rows
kulcsok = [(r[0], r[1]) for r in elof_all]
assert len(kulcsok) == len(set(kulcsok)), "duplikalt id+igehely kulcs az elofordulasok kozott"

# ---------------------------------------------------------------------
# 6. Iras -- csak az osszes ellenorzes utan.
# ---------------------------------------------------------------------


def w(path, rows):
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write("\t".join(row) + "\n")


w(os.path.join(ADAT, "motivumok.tsv"), motivumok)
w(os.path.join(ADAT, "elofordulasok.tsv"), elof_all)
w(os.path.join(ADAT, "jeloltek.tsv"), jeloltek_rows)
w(os.path.join(ADAT, "kapcsolatok.tsv"), kapcsolatok_rows)

print("motivumok sorok:", len(motivumok))
print("KIRALY-001 elofordulas sorok:", len(kiraly_rows))
print("ISTENTISZT-001 elofordulas sorok:", len(istentiszt_rows))
print("jeloltek sorok:", len(jeloltek_rows))
print("kapcsolatok sorok:", len(kapcsolatok_rows))
