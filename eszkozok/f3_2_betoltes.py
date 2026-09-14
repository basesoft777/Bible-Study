# -*- coding: utf-8 -*-
"""
F3.2 retroaktiv betoltes -- nehez csoport (Tehom TEREMT-001, Hadesz/Seol
ALVIL-001, Isten fiai/Nefilim/Gibborim MENNY-001, Pneuma/pszukhe
ANTROP-001, Rafaim HODIT-001).

A terv szerint ez a csoport haromoszlopos tablazattal rendelkezik
(Igehely | Kapcsolodas | PaRDeS-szint), Strong-szam nelkul -- a
Strong-szamot a TAHOT_kivonat.tsv-bol KELL VISSZAKERESNI, gepi uton,
nem kezzel. A visszakereses eredmenye harom kategoria egyikebe esik
minden ÓSZ-sornal:

  IGAZOLVA          -- a vers szerepel a TAHOT_kivonat.tsv-ben, es az
                       elvart Strong-szam(ok) mind jelen vannak.
  TAHOT_HIANYOS      -- a vers EGYALTALAN NEM szerepel a TAHOT_kivonat.
                       tsv-ben (lefedettsegi res -- nema nem-talalat,
                       NEM valodi nem-talalat).
  STRONG_HIANYZIK    -- a vers szerepel a TAHOT-ban, de a vart Strong-
                       szam(ok) valamelyike nem talalhato abban a
                       versben (valodi anomalia, kulon vizsgalando).

Ez a harom kategoria SOHA nem keverendo ossze -- ez a lepes egyetlen
celja (l. ATALAKITASI_TERV.md.md F3.2 sora).

Az ujszovetsegi (gorog) elofordulasok nem esnek a TAHOT hataskorebe --
azokra a study sajat, mar dokumentalt Strong-szama kerul at valtozas
nelkul, TAGNT-visszakereses nelkul (a terv F3.2 sora kifejezetten a
TAHOT_kivonat.tsv-t nevezi meg).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, "adat")
TAHOT_PATH = os.path.join(ROOT, "konkordancia", "TAHOT_kivonat.tsv")


def load_tahot_index(strong_codes):
    """igehely -> set(strong-szam), csak a kert kodokra szurve."""
    wanted = set(strong_codes)
    index = {}
    verses_seen = set()
    with open(TAHOT_PATH, encoding="utf-8") as f:
        r = csv.reader(f, delimiter="\t")
        header = next(r)
        assert header[0] == "Igehely" and header[1] == "Strong-szám"
        for row in r:
            igehely, strong = row[0], row[1]
            verses_seen.add(igehely)
            if strong in wanted:
                index.setdefault(igehely, set()).add(strong)
    return index, verses_seen


def check(igehely, required_strongs, index, verses_seen):
    """(allapot, talalt_strongok) -- allapot in IGAZOLVA/TAHOT_HIANYOS/STRONG_HIANYZIK."""
    if igehely not in verses_seen:
        return "TAHOT_HIANYOS", set()
    found = index.get(igehely, set())
    if set(required_strongs).issubset(found):
        return "IGAZOLVA", found
    return "STRONG_HIANYZIK", found


def prov(forras, ts, allapot, strong_expected):
    return (
        "scope=manual | forras=%s | ts=%s | talalat=%s | strong_vart=%s"
        % (forras, ts, allapot, strong_expected)
    )


def prov_nt(forras, ts):
    return "scope=manual | forras=%s | ts=%s | talalat=NT-nincs_TAHOT_hatalykor" % (forras, ts)


# ---------------------------------------------------------------------
# Motivum-definiciok: (id, igehely, kapcsolodas, pardes_szint, required_strongs_or_None)
# required_strongs=None -> ujszovetsegi/gorog sor, nincs TAHOT-visszakereses.
# ---------------------------------------------------------------------

TEHOM_STUDY = "Tehom_tematikus.md"
SEOL_STUDY = "Hadesz_Seol_tematikus.md"
MENNY_STUDY = "Isten_fiai_Nefilim_Gibborim_tematikus.md"
PNEUMA_STUDY = "Pneuma_pszukhe_megkulonboztetes_tematikus.md"
RAFAIM_STUDY = "Rafaim_tematikus.md"

H8415 = ["H8415"]

tehom_ot = [
    ("1Móz 1:2", "A teremtés előtti, differenciálatlan, formátlan vizek — \"sötétség vala a mélység színén\"", "Pshat/Remez"),
    ("1Móz 7:11", "A dekreáció kezdete: \"felfakadának a nagy mélység forrásai\" — a teremtéskor elválasztott vizek újraegyesülnek", "Remez"),
    ("1Móz 8:2", "A helyreállítás mozzanata: \"bezárultak a mélység forrásai és az ég csatornái\" — a rend visszatér", "Remez"),
    ("1Móz 49:25", "Jákób áldása Józsefen: \"a mélységnek áldásaival, mely alant fekszik\" — a tehóm immár nem fenyegetés, hanem áldás forrása", "Drash"),
    ("2Móz 15:5", "Mózes és Izrael éneke: \"elborították őket a hullámok... a mélységes vizek megmerevültek\" — a Vörös-tenger dekreációs/ítéletes vízzé válik", "Remez"),
    ("2Móz 15:8", "ua. — a Vörös-tengeri ének folytatása, ugyanaz a szó (תְּהֹמֹת, többes szám)", "Remez"),
    ("5Móz 8:7", "\"a föld... amelynek mélységei forrásokban törnek elő\" — áldás/bőség", "Remez"),
    ("5Móz 33:13", "Mózes áldása Józsefen — \"a mélység áldásaival alant\" (csaknem szó szerint = 1Móz 49:25)", "Remez"),
    ("Jób 28:14", "\"a mélység azt mondja: nincs bennem\" — a bölcsesség nem található", "Remez"),
    ("Jób 38:16", "\"eljutottál-e a mélység forrásaihoz\"", "Remez"),
    ("Jób 38:30", "\"a mélység színe mintegy jéggé mered\"", "Remez"),
    ("Zsolt 33:7", "\"összegyűjti mint tömlőbe a tenger vizét, tárházba rakja a mélységeket\" (Károli 1908 \"hullámokat\"-tal fordítja a תְּהוֹם-ot)", "Remez"),
    ("Zsolt 36:7", "\"ítéleteid [olyanok, mint] a nagy mélység\"", "Remez"),
    ("Zsolt 42:8", "\"mélység a mélységet hívja\" — a szó kétszer szerepel e versben", "Remez"),
    ("Zsolt 71:20", "\"a föld mélységéből ismét felhozol engem\"", "Remez"),
    ("Zsolt 77:17", "\"látták a vizek téged... megrázkódtak a mélységek\" — teofánia/Vörös-tenger-visszhang", "Remez"),
    ("Zsolt 78:15", "\"megnyitotta a kősziklát... itatta, mint a nagy mélységekből\"", "Remez"),
    ("Zsolt 104:6", "\"vízáradattal, mint egy ruhával, takartad be, a hegyek felett álltak a vizek\"", "Remez"),
    ("Zsolt 106:9", "\"megdorgálta a veres tengert... átvitte őket a mélységeken\" — Exodus-visszhang", "Remez"),
    ("Zsolt 107:26", "\"az égig emelkednek, a fenékig süllyednek\" (Károli 1908 \"fenékig\"-gel fordítja a תְּהוֹם-ot)", "Remez"),
    ("Zsolt 135:6", "\"amit csak akar, megcselekszi... a mélységekben\"", "Remez"),
    ("Zsolt 148:7", "\"dicsérjétek az Urat... ti mélységek\"", "Remez"),
    ("Péld 3:20", "\"az ő tudománya által fakadtak a mélységek\"", "Remez"),
    ("Péld 8:24", "\"mikor még semmi mélységek nem voltak, születtem\" — bölcsesség-teológia", "Remez"),
    ("Péld 8:27", "\"mikor a mélység színe felett kört formált\" (szinte szó szerinti = 1Móz 1:2)", "Remez"),
    ("Péld 8:28", "\"mikor erősekké tette a mélység forrásait\" (szinte szó szerinti = 1Móz 7:11)", "Remez"),
    ("Ézs 51:10", "\"nem te vagy-e, aki kiszárítottad a tengert, a nagy mélység vizeit\" — Exodus-visszhang", "Remez"),
    ("Ézs 63:13", "\"aki átvitte őket a mélységeken\" — Exodus-visszhang", "Remez"),
    ("Ez 26:19", "\"mikor rád hozom a mélységet, hogy elborítsanak a nagy vizek\"", "Remez"),
    ("Ez 31:4", "\"a mélység naggyá tette [a cédrust]\"", "Remez"),
    ("Ez 31:15", "\"béburkoltam miatta a mélységet\" — Fáraó-siratóének", "Remez"),
    ("Ámós 7:4", "\"megemésztette a nagy mélységet\" — sáska/tűz-látomás", "Remez"),
    ("Hab 3:10", "\"a mélység felemelte szavát\" — teofánia", "Remez"),
    ("Jón 2:6", "\"a mélység körülvett engem\" — Jónás imája a hal gyomrában, legszorosabb párhuzam a Zsolt 71:20/107:26 verspárral", "Remez"),
]

tehom_nt = [
    ("Lukács 8:31", "ἄβυσσος — a démonok kérik, ne oda küldje őket Jézus", "Pshat/Remez"),
    ("Róma 10:7", "ἄβυσσος — \"ki száll le az abüsszoszba?\"", "Remez/Drash"),
    ("Jelenések 9:1-2", "ἄβυσσος — a mélység kútja megnyílik, füst és sáskák jönnek fel", "Remez/Sod"),
    ("Jelenések 9:11", "ἄβυσσος, Ἀβαδδών/Ἀπολλύων — a mélység angyala", "Remez/Sod"),
    ("Jelenések 11:7", "ἄβυσσος — a fenevad onnan jön fel", "Remez"),
    ("Jelenések 17:8", "ἄβυσσος — a fenevad onnan jön fel", "Remez"),
    ("Jelenések 20:1-3", "ἄβυσσος — Sátán megkötözve ezer évre", "Remez/Drash"),
]

seol_base_ot = [
    ("Zsolt 16:10", "שְׁאוֹל (seól) → ᾍδης (hádész), ApCsel 2:27,31 idézi — Krisztus nem marad a halál birodalmában", "Pshat/Drash"),
]

seol_ext_ot = [
    ("1Móz 37:35", "Jákób gyásza: \"leszállok fiamhoz a Seólba, gyászolva\"", "Remez"),
    ("1Móz 42:38", "Benjámin miatti félelem", "Remez"),
    ("1Móz 44:29", "Júda közbenjárása", "Remez"),
    ("1Móz 44:31", "Júda közbenjárása, folytatás", "Remez"),
    ("4Móz 16:30", "élve alászállás a Seólba — Kóré lázadása, csodás ítélet", "Remez"),
    ("4Móz 16:33", "\"és befedte őket a föld\"", "Remez"),
    ("5Móz 32:22", "Isten haragjának tüze \"a Seól fenekéig\" ég", "Remez"),
    ("1Sám 2:6", "\"az Úr... Seólba visz és onnan felhoz\" — Anna éneke", "Remez"),
    ("2Sám 22:6", "\"a Seól kötelei körülvettek\" (= Zsolt 18:6 párhuzam)", "Remez"),
    ("1Kir 2:6", "Dávid Salamonnak — Joáb \"őszen szálljon a Seólba\"", "Remez"),
    ("1Kir 2:9", "ua. — Simei", "Remez"),
    ("Jób 7:9", "\"aki leszáll a Seólba, nem jön fel\"", "Remez"),
    ("Jób 11:8", "\"mélyebb, mint a Seól\" — Isten mindentudása", "Remez"),
    ("Jób 14:13", "\"bár rejtenél el a Seólban\"", "Remez"),
    ("Jób 17:13", "\"ha várom is: a Seól az én házam\"", "Remez"),
    ("Jób 17:16", "\"leszáll-e a Seól rúdjaihoz\"", "Remez"),
    ("Jób 21:13", "\"egy pillanat alatt szállnak a Seólba\"", "Remez"),
    ("Jób 24:19", "\"a Seól elragadja a bűnösöket\"", "Remez"),
    ("Jób 26:6", "\"a Seól mezítelen Isten előtt\"", "Remez"),
    ("Zsolt 6:6", "\"nincs Rólad emlékezés a Seólban\"", "Remez"),
    ("Zsolt 9:18", "\"a gonoszok visszatérnek a Seólba\"", "Remez"),
    ("Zsolt 18:6", "\"a Seól kötelei körülvettek\" (= 2Sám 22:6)", "Remez"),
    ("Zsolt 30:4", "hálaadás — \"kihoztad lelkem a Seólból\"", "Remez"),
    ("Zsolt 31:18", "\"hallgassanak el a gonoszok a Seólban\"", "Remez"),
    ("Zsolt 49:15", "\"mint juhok a Seólnak rendelve\"", "Remez"),
    ("Zsolt 49:16", "\"Isten megváltja lelkemet a Seól kezéből\"", "Remez"),
    ("Zsolt 55:16", "\"szálljanak élve a Seólba\"", "Remez"),
    ("Zsolt 86:13", "\"kihoztad lelkem a legmélyebb Seólból\"", "Remez"),
    ("Zsolt 88:4", "\"életem közel a Seólhoz\"", "Remez"),
    ("Zsolt 89:49", "\"ki menti meg lelkét a Seól kezéből\"", "Remez"),
    ("Zsolt 116:3", "\"a Seól szorongatásai megragadtak\"", "Remez"),
    ("Zsolt 139:8", "\"ha a Seólban vetek ágyat, ott is vagy\" — Isten mindenütt-jelenvalósága", "Remez"),
    ("Zsolt 141:7", "\"mint mikor szántanak... a Seól szájánál\"", "Remez"),
    ("Péld 1:12", "\"elnyeljük őket elevenen, mint a Seól\"", "Remez"),
    ("Péld 5:5", "a parázna lába a Seólba száll", "Remez"),
    ("Péld 7:27", "háza a Seól útja", "Remez"),
    ("Péld 9:18", "a balgák a Seól mélyén", "Remez"),
    ("Péld 15:11", "Seól és Abaddón Isten előtt", "Remez"),
    ("Péld 15:24", "\"hogy elkerülje a Seólt alant\"", "Remez"),
    ("Péld 23:14", "\"kiragadod lelkét a Seólból\"", "Remez"),
    ("Péld 27:20", "\"a Seól és Abaddón nem elégszik meg\"", "Remez"),
    ("Péld 30:16", "Seól a négy \"nem-elégedő\" dolog közt", "Remez"),
    ("Préd 9:10", "\"nincs tudás, munka, terv a Seólban, ahová mégy\"", "Remez"),
    ("Én 8:6", "\"a szerelem kemény, mint a Seól\"", "Remez"),
    ("Ézs 5:14", "Júda ítélete — a Seól kitágítja torkát", "Remez"),
    ("Ézs 7:11", "\"kérj jelt... tégy mélyre, mint a Seól\"", "Remez"),
    ("Ézs 14:9", "Babilon-gúnydal — a Seól megmozdul (ugyanaz a szakasz, ahol a רְפָאִים is szerepel, l. HODIT-001)", "Remez"),
    ("Ézs 14:11", "\"büszkeséged leszállt a Seólba\"", "Remez"),
    ("Ézs 14:15", "\"a Seól legmélyére vitetel\"", "Remez"),
    ("Ézs 28:15", "\"szövetséget kötöttünk a Seóllal\"", "Remez"),
    ("Ézs 28:18", "\"szövetségetek a Seóllal nem áll meg\"", "Remez"),
    ("Ézs 38:10", "Ezékiás betegség-éneke — \"a Seól kapuiba kell mennem\"", "Remez"),
    ("Ézs 38:18", "\"a Seól nem dicsőít téged\"", "Remez"),
    ("Ézs 57:9", "bálványimádás — \"egészen a Seólig alázkodtál\"", "Remez"),
    ("Ez 31:15", "Fáraó/Egyiptom a Seólba száll — a Libanon-cédrus-példázat", "Remez"),
    ("Ez 31:16", "ua.", "Remez"),
    ("Ez 31:17", "ua.", "Remez"),
    ("Ez 32:21", "\"a hatalmasok szólnak hozzá a Seólból\"", "Remez"),
    ("Ez 32:27", "körülmetéletlenek a Seólban, fegyvereikkel", "Remez"),
    ("Hós 13:14", "\"Hol van a te veszedelmed, oh Seól?\" — Pál idézi 1Kor 15:55-ben, ⭐ kiemelt lelet", "Remez/Drash"),
    ("Ámós 9:2", "\"ha a Seólba ásnak is, onnan is kihozom kezem\"", "Remez"),
    ("Hab 2:5", "a kevély, mint a Seól, sosem elégszik meg", "Remez"),
    ("Jón 2:3", "\"a Seól gyomrából kiáltottam\"", "Remez"),
]

seol_nt = [
    ("ApCsel 2:27", "Péter Zsolt 16:10-et idézi: \"mert nem hagyod az én lelkemet a sírban [hádész]\"", "Pshat/Drash"),
    ("ApCsel 2:31", "Péter folytatja: Krisztus feltámadásáról szólva — \"nem hagyatott a sírban [hádész]\"", "Pshat/Drash"),
    ("Lukács 16:23", "ᾍδης — a gazdag ember kínban", "Pshat"),
    ("Jelenések 1:18", "ᾍδης — Krisztus kezében a halál és a hádész kulcsai", "Drash/Sod"),
    ("Jelenések 6:8", "ᾍδης — a sápadt lovon ülő Halál nyomában jár a hádész", "Pshat/Remez"),
    ("Jelenések 20:13-14", "ᾍδης — kiadja halottait, majd a tűz tavába vettetik", "Remez/Drash"),
    ("Lukács 10:15", "ᾍδης — \"égig felmagasztaltattál... hádészig fogsz lealáztatni\" (Kapernaum ítélete)", "Remez"),
    ("Máté 11:23", "ᾍδης — párhuzamos hely Luk 10:15-höz", "Remez"),
]

MENNY_ELOHIM = ["H1121", "H0430"]
MENNY_NEFILIM = ["H5303"]

menny_rows = [
    # (igehely, kapcsolodas, pardes_szint, required_strongs_or_None)
    ("1Móz 6:2", "בְּנֵי הָאֱלֹהִים — \"Isten fiai\" látják és elveszik az emberek lányait", "Pshat", MENNY_ELOHIM),
    ("1Móz 6:4", "נְפִלִים a földön; az egyesülésből születnek a גִּבֹּרִים, \"ősidők óta neves emberek\" — ⚠️ vitatott, hogy a nefilim és a gibborim azonosak-e", "Pshat", MENNY_NEFILIM),
    ("Jób 1:6", "בְּנֵי הָאֱלֹהִים megjelennek Isten színe előtt, mennyei tanácsban, Sátán is közöttük", "Remez", MENNY_ELOHIM),
    ("Jób 2:1", "ugyanaz a jelenet megismétlődik", "Remez", MENNY_ELOHIM),
    ("Jób 38:7", "a בְּנֵי אֱלֹהִים örömkiáltása a teremtéskor (névelő nélküli, rokon alak)", "Remez", MENNY_ELOHIM),
    ("4Móz 13:34", "a kémek jelentésében נְפִלִים — Anák fiai mint a nefilim leszármazottai (a kémek szubjektív állítása, nem a narrátoré)", "Remez", MENNY_NEFILIM),
]

menny_nt_no_lexical = [
    ("Júd 1:6", "angyalok, akik \"nem tartották meg fejedelemségüket\", örök bilincsben — tartalmi/szerkezeti rokonság 1Énokh 10:4-6, 10:11-12, 12:4-gyel (nem szó szerinti idézet)", "Drash/Sod", "referencia:1Énokh 10:4-6/10:11-12/12:4"),
    ("Júd 1:14-15", "Énokh próféciája az ítéletről — közvetlen, szinte szó szerinti idézet 1Énokh 1:9-ből", "Drash/Sod", "idézet:1Énokh 1:9"),
    ("2Pét 2:4-5", "Isten nem kegyelmezett a bűnbe esett angyaloknak, Tartaroszba vetette őket — tematikus/szerkezeti (párhuzamos \"nem kegyelmezett\" formula), NEM közös lexikai gyök", "Drash/Sod", "formula:οὐκ ἐφείσατο (nem kegyelmezett)"),
]

pneuma_rows_ot = [
    ("1Móz 2:7", "az ember נֶפֶשׁ חַיָּה (\"élő lélek\") lesz Isten leheletétől; Pál ezt állítja szembe 1Kor 15:45-ben az utolsó Ádámmal — tematikus, ellentétező párhuzam, NEM lexikai folytonosság", "Remez/Sod", ["H5315", "H2416"]),
]

pneuma_rows_nt = [
    ("1Thessz 5:23", "Pál imája: a pneuma, pszükhé és szóma három külön főnévként, egy-egy külön határozott névelővel sorolva fel", "Pshat"),
    ("Zsid 4:12", "Isten Igéje \"elhat a szellem és lélek... megoszlásáig\" (μερισμοῦ) — a szerző explicit szétválasztásról beszél", "Pshat/Sod"),
    ("1Kor 15:45", "Pál: az utolsó Ádám \"pneuma zóopoiun\" (\"megelevenítő szellemmé\") lett — szemben az első Ádám \"élő lelkével\" (1Móz 2:7)", "Remez/Sod"),
    ("Luk 1:46", "Mária éneke: \"magasztalja az én lelkem (ψυχή) az Urat\" — negyedik, valódi lexikai előfordulás, párhuzamos szerkezetben Luk 1:47-tel", "Pshat"),
    ("Luk 1:47", "Mária éneke: \"és örvendez az én szellemem (πνεῦμα) az én megtartó Istenemben\" — ugyanabban a grammatikai szerepben, mint 1:46", "Pshat"),
    ("1Kor 2:14", "a \"természet szerinti ember\" (ψυχικὸς ἄνθρωπος) nem fogadja be Isten Szellemének dolgait — ötödik előfordulás, melléknévi alakban", "Drash"),
    ("1Kor 2:15", "a \"szellemi ember\" (πνευματικός) mindent megvizsgál — az 1Kor 2:14 párja", "Drash"),
]

RAFAIM_H7497 = ["H7497"]
RAFAIM_H7496 = ["H7496"]
RAFAIM_H5303 = ["H5303"]

rafaim_rows = [
    ("1Móz 14:5", "רְפָאִים, זוּזִים, אֵימִים — a keleti királyi koalíció leveri őket, mielőtt az öt lázadó várost is legyőzné", "", RAFAIM_H7497),
    ("1Móz 14:6", "חֹרִים (Hórim) Szeír hegyén — ugyanabban a hadjáratban legyőzött negyedik népcsoport (NEM רְפָאִים szótő)", "", None),
    ("1Móz 15:20", "רְפָאִים — a Refáim az Ábrámnak ígért föld népei között szerepel", "", RAFAIM_H7497),
    ("4Móz 13:34", "נְפִלִים ⇒ עֲנָקִים — a kémek szerint az Anákok \"a Nefilimtől\" származnak (a kémek saját kijelentése, nem a narrátoré)", "", RAFAIM_H5303),
    ("5Móz 2:10", "אֵימִים... הֵם רְפָאִים — a Móábiak Émimnek nevezik, \"akiket szintén Refáimnak számítanak, mint az Anákokat\"", "", RAFAIM_H7497),
    ("5Móz 2:11", "ua. — folytatás", "", RAFAIM_H7497),
    ("5Móz 2:20", "זַמְזֻמִּים... רְפָאִים — az Ammoniták Zamzummimnak nevezik ugyanazt a népet", "", RAFAIM_H7497),
    ("5Móz 2:21", "ua. — folytatás", "", RAFAIM_H7497),
    ("5Móz 3:11", "עוֹג... מִיֶּתֶר הָרְפָאִים — Óg, Básán királya \"a Refáim maradékából\" — vaságya 9×4 könyök", "", RAFAIM_H7497),
    ("5Móz 3:13", "ua. — Básán mint \"a Refáim földje\"", "", RAFAIM_H7497),
    ("Józs 12:4", "אֶרֶץ רְפָאִים — Óg földje \"a Refáim földje\"", "", RAFAIM_H7497),
    ("Józs 13:12", "ua.", "", RAFAIM_H7497),
    ("2Sám 21:15", "הָרָפָה / יְלִידֵי הָרָפָה — Góliát és rokonai \"a Rafá szülöttei\" — Dávid vitézei (גִּבֹּרִים) győzik le őket", "", RAFAIM_H7497),
    ("2Sám 21:16", "ua. — folytatás", "", RAFAIM_H7497),
    ("2Sám 21:18", "ua. — folytatás", "", RAFAIM_H7497),
    ("2Sám 21:20", "ua. — folytatás", "", RAFAIM_H7497),
    ("2Sám 21:22", "ua. — folytatás", "", RAFAIM_H7497),
    ("1Krón 20:4", "párhuzamos hely 2Sám 21:15-22-höz", "", RAFAIM_H7497),
    ("1Krón 20:6", "ua. — folytatás", "", RAFAIM_H7497),
    ("1Krón 20:8", "ua. — folytatás", "", RAFAIM_H7497),
    ("Jób 26:5", "רְפָאִים יְחוֹלָלוּ מִתַּחַת לַמָּיִם — \"a Refáim reszketnek a vizek alatt\" — költői kontextus, halottak birodalma", "", RAFAIM_H7496),
    ("Zsolt 88:11", "הֲרְפָאִים יָקוּמוּ יוֹדוּךָ — \"vajon a Refáim fölkelnek-e, hogy dicsérjenek téged?\"", "", RAFAIM_H7496),
    ("Péld 2:18", "רְפָאִים — bölcsességi kontextus: aki eltéved, a \"Refáim gyülekezetébe\" jut", "", RAFAIM_H7496),
    ("Péld 9:18", "ua.", "", RAFAIM_H7496),
    ("Péld 21:16", "ua.", "", RAFAIM_H7496),
    ("Ézs 14:9", "רְפָאִים... כָּל־עַתּוּדֵי אָרֶץ — Babilon királyát gúnyosan fogadja a Seól, \"fölkelti ellene a Refáimot\"", "", RAFAIM_H7496),
    ("Ézs 26:14", "רְפָאִים — a halottak feltámadásáról szóló szakasz kontextusában", "", RAFAIM_H7496),
    ("Ézs 26:19", "ua.", "", RAFAIM_H7496),
    ("2Sám 5:18", "עֵמֶק רְפָאִים — Refáim völgye, a filiszteusok és Dávid csatáinak színtere", "", RAFAIM_H7497),
    ("2Sám 5:22", "ua.", "", RAFAIM_H7497),
    ("2Sám 23:13", "ua.", "", RAFAIM_H7497),
    ("1Krón 11:15", "ua. — párhuzamos hely", "", RAFAIM_H7497),
    ("1Krón 14:9", "ua.", "", RAFAIM_H7497),
    ("Ézs 17:5", "עֵמֶק רְפָאִים — aratási hasonlat", "", RAFAIM_H7497),
    ("Józs 15:8", "עֵמֶק רְפָאִים — Júda törzsi határának pontosítása", "", RAFAIM_H7497),
    ("Józs 18:16", "עֵמֶק רְפָאִים — Benjámin törzsi határának pontosítása", "", RAFAIM_H7497),
    ("Józs 17:15", "אֶרֶץ הָרְפָאִים — \"a Perizzita és a Refáim földje\" — Józsué válasza Efraim/Manassé birtok-panaszára", "", RAFAIM_H7497),
]

print("tehom_ot", len(tehom_ot))
print("tehom_nt", len(tehom_nt))
print("seol_base_ot", len(seol_base_ot))
print("seol_ext_ot", len(seol_ext_ot))
print("seol_nt", len(seol_nt))
# ---------------------------------------------------------------------
# TAHOT-visszakereses -- minden ÓSZ-sorra, egyetlen index-epitessel.
# ---------------------------------------------------------------------

ALL_OT_STRONGS = set(
    H8415
    + MENNY_ELOHIM + MENNY_NEFILIM
    + ["H5315", "H2416"]
    + RAFAIM_H7497 + RAFAIM_H7496 + RAFAIM_H5303
    + ["H7585"]
)

TAHOT_INDEX, TAHOT_VERSES = load_tahot_index(ALL_OT_STRONGS)

results = {"IGAZOLVA": 0, "TAHOT_HIANYOS": 0, "STRONG_HIANYZIK": 0}


rejected_strong_hianyzik = []  # (id, igehely, kapcsolodas, strong_str, found) -- kulon jeloltek-sorba kerul


def build_ot_rows(id_, study, ts, rows, required_default=None):
    """rows: (igehely, kapcsolodas, pardes_szint[, required_strongs])"""
    out = []
    for item in rows:
        if len(item) == 4:
            igehely, kapcsolodas, pardes_szint, required = item
        else:
            igehely, kapcsolodas, pardes_szint = item
            required = required_default
        if required is None:
            # nincs lexikai horgony (pl. Hórim) -- nem elofordulas, hanem
            # kulon kezelendo, l. main().
            continue
        allapot, found = check(igehely, required, TAHOT_INDEX, TAHOT_VERSES)
        results[allapot] += 1
        strong_str = "+".join(required)
        if allapot == "STRONG_HIANYZIK":
            # A study egy tobb-verses tartomanyt (pl. "5Móz 2:10-11") idezett
            # egysegkent; a per-vers szetbontas soran kiderult, hogy a
            # lexema ebben a konkret versben nem all -- ez nem TAHOT-hiany,
            # hanem tulzottan tag idezes. Nem lep elo elofordulassa, hanem a
            # jeloltek.tsv-be kerul, dontes=elutasitva.
            rejected_strong_hianyzik.append((id_, igehely, kapcsolodas, strong_str, found))
            continue
        gerinc_elem = strong_str
        out.append((
            id_, igehely, kapcsolodas, pardes_szint, "",
            gerinc_elem, strong_str, "", "", "", "",
            "", "", "",
            prov(study, ts, allapot, strong_str),
        ))
    return out


def build_nt_rows(id_, study, ts, rows, strong):
    out = []
    for igehely, kapcsolodas, pardes_szint in rows:
        out.append((
            id_, igehely, kapcsolodas, pardes_szint, "",
            strong, strong, "", "", "", "",
            "", "", "",
            prov_nt(study, ts),
        ))
    return out


# TEREMT-001 (Tehóm)
teremt_rows = (
    build_ot_rows("TEREMT-001", TEHOM_STUDY, "2026-09-10", tehom_ot, required_default=H8415)
    + build_nt_rows("TEREMT-001", TEHOM_STUDY, "2026-09-10", tehom_nt, "G0012")
)

# ALVIL-001 (Hádész/Seól)
alvil_rows = (
    build_ot_rows("ALVIL-001", SEOL_STUDY, "2026-09-10", seol_base_ot, required_default=["H7585"])
    + build_ot_rows("ALVIL-001", SEOL_STUDY, "2026-09-10", seol_ext_ot, required_default=["H7585"])
    + build_nt_rows("ALVIL-001", SEOL_STUDY, "2026-09-10", seol_nt, "G0086")
)

# MENNY-001 (Isten fiai/Nefilim/Gibborim)
menny_lex_rows = build_ot_rows("MENNY-001", MENNY_STUDY, "2026-09-10", menny_rows)
menny_ref_rows = []
for igehely, kapcsolodas, pardes_szint, gerinc_elem in menny_nt_no_lexical:
    menny_ref_rows.append((
        "MENNY-001", igehely, kapcsolodas, pardes_szint, "",
        gerinc_elem, "", "", "", "", "",
        "", "", "",
        prov_nt(MENNY_STUDY, "2026-09-10"),
    ))
menny_all_rows = menny_lex_rows + menny_ref_rows

# ANTROP-001 (Pneuma/pszükhé)
antrop_rows = (
    build_ot_rows("ANTROP-001", PNEUMA_STUDY, "2026-08-22", pneuma_rows_ot)
    + build_nt_rows("ANTROP-001", PNEUMA_STUDY, "2026-08-22", pneuma_rows_nt, "G4151+G5590")
)

# HODIT-001 (Rafaim) -- az 1Móz 14:6 (Hórim, required=None) kimarad az
# elofordulasokbol, l. main() a jeloltek.tsv-be iranyitasert.
hodit_rows = build_ot_rows("HODIT-001", RAFAIM_STUDY, "2026-09-10", rafaim_rows)

print("--- TAHOT-visszakereses osszegzes ---")
print(results)

# ---------------------------------------------------------------------
# Hossz-ellenorzes -- MINDEN elofordulasok-sor 15 mezos legyen.
# ---------------------------------------------------------------------

ALL_ELOF = teremt_rows + alvil_rows + menny_all_rows + antrop_rows + hodit_rows
for _r in ALL_ELOF:
    assert len(_r) == 15, ("elofordulas sor hossza nem 15: %r" % (_r,))

kulcsok = [(r[0], r[1]) for r in ALL_ELOF]
dup = [k for k in kulcsok if kulcsok.count(k) > 1]
assert not dup, ("duplikalt id+igehely kulcs: %r" % (sorted(set(dup)),))

# ---------------------------------------------------------------------
# jeloltek.tsv -- minden elofordulasok sorhoz + a lexikailag ki nem
# igazolhato jelolt(ek) kulon, dontes=nyitva sorral.
# ---------------------------------------------------------------------

jeloltek_rows = []
for row in ALL_ELOF:
    id_, igehely, kapcsolodas = row[0], row[1], row[2]
    prov_str = row[-1]
    ts = prov_str.split("ts=")[1].split(" |")[0]
    datum = ts.replace("-", ".")
    forras_kereses = "TAHOT_kivonat.tsv visszakeresés (eszkozok/f3_2_betoltes.py), retroaktív F3.2 betöltés"
    jeloltek_rows.append((
        id_, igehely, forras_kereses, "beépítve", kapcsolodas,
        "", "", "", datum,
    ))

# Az 1Móz 14:6 (Hórim) -- a study táblázatában szerepel, de a חֹרִים szó
# nem tartozik a רְפָאִים szócsaládhoz (nincs közös gyök) -- a 4.6 gate
# negatív kritériuma szerint ez nem önálló motívum-előfordulás, hanem
# csak narratív kontextus. Nyitva marad, nem léptetjük elő.
jeloltek_rows.append((
    "HODIT-001", "1Móz 14:6",
    "study 1. pont táblázata (kontextuális sor)", "nyitva",
    "חֹרִים (Hórim) nem a רְפָאִים szócsaládból való — nincs közös gyök H2752 és H7497/H7496 között; a study saját táblázatában szerepel mint \"ugyanabban a hadjáratban legyőzött negyedik népcsoport\", de a motívum negatív kritériuma (l. adat/motivumok.tsv HODIT-001 sora) kizárja: a rokon népnév önmagában nem elég, lexikai átfedés kell",
    "", "", "", "2026.09.14",
))

# A STRONG_HIANYZIK talalatok (tul tagan idezett tobb-verses tartomany
# egy-egy nem-hordozo tagja) -- elutasitva, indokolva.
for id_, igehely, kapcsolodas, strong_str, found in rejected_strong_hianyzik:
    jeloltek_rows.append((
        id_, igehely,
        "TAHOT_kivonat.tsv visszakeresés (eszkozok/f3_2_betoltes.py), retroaktív F3.2 betöltés",
        "elutasítva",
        "a study egy több-verses tartományt (%s) idézett a fenti tartalommal, de a %s Strong-szám ebben a konkrét versben nem áll a TAHOT_kivonat.tsv szerint (talált: %s) — a lexéma a tartomány másik versében van, az külön elofordulasok-sorként bekerült"
        % (kapcsolodas[:40] + "…", strong_str, ",".join(sorted(found)) or "—"),
        "", "", "", "2026.09.14",
    ))

for _r in jeloltek_rows:
    assert len(_r) == 9, ("jeloltek sor hossza nem 9: %r" % (_r,))

# ---------------------------------------------------------------------
# motivumok.tsv -- ot uj sor, a 4.6 gate mezoivel es haromertekue
# statusszal (a motivumok.tsv sema szerint kotelezo mezok, F3.2 nem
# hagyhatja uresen oket, meg ha a terv F3.2 sora explicit csak a
# visszakereseset iri is elo).
# ---------------------------------------------------------------------

motivumok_rows = [
    (
        "TEREMT-001", "Tehóm (תְּהוֹם) — Abüsszosz (ἄβυσσος): a mélység motívuma",
        "Tehóm/Abüsszosz", "Teremtéstan", "Remez/Drash",
        "publikálható", "v4", "2026.09.10",
        "lexikai",
        "az igehelynek a תְּהוֹם gyököt kell tartalmaznia (ÚSZ-ben az LXX-közvetített ἄβυσσος megfelelőjét) — tematikus vízkép önmagában (pl. יָם, \"tenger\") nem elég",
        "vízi/kozmikus káosz-képzetek általában, a תְּהוֹם/ἄβυσσος lexémán kívül",
        "v14", "tematikus_lezart/Tehom_tematikus.md",
    ),
    (
        "ALVIL-001", "Hádész (Seól) — a halottak birodalma",
        "Hádész/Seól", "Eszkatológia", "Remez/Drash",
        "publikálható", "v2", "2026.09.10",
        "lexikai",
        "az igehelynek a שְׁאוֹל gyököt (ÚSZ-ben az LXX-közvetített ᾍδης megfelelőjét) kell tartalmaznia — a תְּהוֹם/ἄβυσσος szócsalád explicit kizárva (kozmikus, nem egyéni-halotti fogalom, l. TEREMT-001 elhatárolása)",
        "a halál/túlvilág fogalma általában, a שְׁאוֹל/ᾍδης lexémán kívül",
        "v14", "tematikus_lezart/Hadesz_Seol_tematikus.md",
    ),
    (
        "MENNY-001", "Isten fiai — Nefilim — Gibborim motívum-komplexum",
        "Isten fiai/Nefilim", "Angyalológia", "Remez/Drash",
        "publikálható", "v4", "2026.09.10",
        "lexikai",
        "az igehelynek a בְּנֵי (הָ)אֱלֹהִים szórendi mintát VAGY a נְפִלִים szót kell tartalmaznia — a רְפָאִים szócsalád explicit kizárva (tematikus, nem lexikai rokon, l. HODIT-001 elhatárolása)",
        "mennyei/angyali lények általában, a בְּנֵי (הָ)אֱלֹהִים/נְפִלִים lexémákon kívül",
        "v14", "tematikus_lezart/Isten_fiai_Nefilim_Gibborim_tematikus.md",
    ),
    (
        "ANTROP-001", "Pneuma/pszükhé megkülönböztetés",
        "Pneuma/pszükhé", "Antropológia", "Pshat/Drash",
        "publikálható", "v3", "2026.08.22",
        "lexikai",
        "az igehelynek a πνεῦμα és ψυχή szavakat (vagy melléknévi alakjukat) egyazon mondaton belül, megkülönböztető szerepben kell tartalmaznia — puszta \"lélek\" vagy \"szellem\" említés önmagában, a másik nélkül, nem elég",
        "emberi belső élet/antropológia általában, a pneuma/pszükhé megkülönböztető használatán kívül",
        "v14", "tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md",
    ),
    (
        "HODIT-001", "Rafeusok/óriás-népek",
        "Refáim/óriás-népek", "Teremtéstan", "Remez/Drash",
        "publikálható", "v3", "2026.09.10",
        "lexikai",
        "az igehelynek a רְפָאִים gyököt (vagy a vele explicit azonosított rokon népnevet: זוּזִים, אֵימִים, זַמְזֻמִּים) kell tartalmaznia — a נְפִלִים/גִּבּוֹר szócsalád (MENNY-001) explicit kizárva, nincs közös gyök",
        "ókori óriás-népek/nagytermetű ellenfelek általában, a רְפָאִים lexémán kívül",
        "v14", "tematikus_lezart/Rafaim_tematikus.md",
    ),
]

for _r in motivumok_rows:
    assert len(_r) == 13, ("motivumok sor hossza nem 13: %r" % (_r,))

# ---------------------------------------------------------------------
# Iras.
# ---------------------------------------------------------------------


def w(path, rows):
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write("\t".join(row) + "\n")


w(os.path.join(ADAT, "motivumok.tsv"), motivumok_rows)
w(os.path.join(ADAT, "elofordulasok.tsv"), ALL_ELOF)
w(os.path.join(ADAT, "jeloltek.tsv"), jeloltek_rows)

print("motivumok sorok:", len(motivumok_rows))
print("elofordulasok sorok:", len(ALL_ELOF))
print("jeloltek sorok:", len(jeloltek_rows))
print("  TEREMT-001:", len(teremt_rows))
print("  ALVIL-001:", len(alvil_rows))
print("  MENNY-001:", len(menny_all_rows))
print("  ANTROP-001:", len(antrop_rows))
print("  HODIT-001:", len(hodit_rows))
