# -*- coding: utf-8 -*-
"""F194.30 — a lektor 22 tételének javítóköre (az egyetlen) a forrásban: motivumok/ISTENTISZT-001.md.

A tételszámok a naplok/KIADAS_ISTENTISZT-001_lektor_2kiadas.md szerintiek. Bekezdésenként cserél: a régi bekezdés elejét
ellenőrzi (előtag), és a teljes sort az új szövegre cseréli. A 2. és a 21. tétel a lap elején álló, a felhasználó által
jóváhagyott kritériumot is érinti; azt ez a kör nem írja át (N-F194h), csak a Kivonat határ-bekezdését.
Futtatás a repó gyökeréből: python naplok/F194_lektor_javitokor.py"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

P = 'motivumok/ISTENTISZT-001.md'

UJ = {
    # 3., 15., 16.: a Kivonat 1. bekezdése
    'A motívum azt a bibliai formulát követi,': (
        'A motívum azt a bibliai formulát követi, amelyben valaki az Úr nevét hívja segítségül: a héberben קָרָא בְּשֵׁם '
        'יְהוָה (kárá besém Jahve), szó szerint „hívni az Úr nevén”. A formula Énós nemzedékében kezdődik: „Akkor kezdték '
        'segítségül hívni az Úrnak nevét” (1Móz 4:26). Ábrám és Izsák oltáránál ismétlődik (1Móz 12:8, 13:4, 26:25), '
        'Beérsebában az örökkévaló Isten nevével (1Móz 21:33). A Kármel-hegyen Illés két név hívását állítja szembe '
        'egymással, és a Baál nevének hívására „nem jött szó, sem felelet” (1Kir 18:24-26); a zsoltáros a bajban és a '
        'szabadulás után is az Úr nevét hívja segítségül (Zsolt 116:4, 13, 17). A fordulópont Jóel mondata: itt a '
        'segítségül hívás már nem egy ember vagy egy nemzedék cselekvése, hanem általános ígéret, „mindaz, a ki az Úrnak '
        'nevét hívja segítségül, megmenekül” (Jóel 2:32), és Sofóniásnál a népekre is kiterjed (Sof 3:9). Az Újszövetség '
        'Jóel mondatát idézi (ApCsel 2:21, Róm 10:13), az 1Kor 1:2-ben pedig a név után Jézus Krisztus neve áll: Pál a '
        'korinthusi gyülekezetet „mindazokkal egybe” köszönti, „a kik a mi Urunk Jézus Krisztus nevét segítségül hívják '
        'bármely helyen”.'),
    # 16.: a Kivonat 2. bekezdése
    'A motívum 20 helyen, 10 bibliai könyvben áll:': (
        'A motívum 20 helyen, 10 bibliai könyvben áll: 16 az Ószövetségben, 4 az Újszövetségben. Az ószövetségi helyek '
        'közül öt a Genezisben áll, Énós nemzedékétől Izsákig; kettő Mózes második könyvében, az Úr Mózesnek tett '
        'ígéretében és a hozzá tartozó jelenetben (2Móz 33:19, 34:5); négy a Királyok könyveiben (a Kármel-hegyi jelenet '
        'három verse és Naámán elvárása, 2Kir 5:11); három a 116. zsoltárban; egy-egy Jóelnél és Sofóniásnál. Az '
        'újszövetségi helyek közül kettő Jóel idézete (ApCsel 2:21, Róm 10:13), egy Pál megtérésének elbeszélése '
        '(ApCsel 22:16), egy a korinthusi levél köszöntése (1Kor 1:2).'),
    # 2., 17., 21.: a Kivonat határ-bekezdése
    'Ide az a hely tartozik, amelyben a hívás igéjét': (
        'Ide az a hely tartozik, amelyben a hívás igéje (kárá) és a név (besém, „a nevén”) együtt áll, és a név után az '
        'Úr neve, a יְהוָה (Jahve) következik: valaki az Úr nevét hívja segítségül. Az ige és a név sorrendje változhat: a '
        '116. zsoltárban a név áll elöl („az Úrnak nevét segítségül hívám”, Zsolt 116:4). Nem tartozik ide, ahol a név '
        'szava megvan, de az Úr neve helyén névmási rag áll, „nevemet”, „nevedet”, „nevét” (például Zak 13:9, Zsolt '
        '105:1, Jer 10:25), sem az, ahol Isten szólít meg embert a nevén (Ézs 43:1, 45:3), vagy más név áll (Ézs 44:5). '
        'Az Újszövetségben az ἐπικαλέω (epikaleó) ige mellett a névnek, az ὄνομα (onoma) szónak és az Úr megnevezésének '
        'is állnia kell: az ApCsel 9:14 és 9:21 „nevedet”, illetve „ezt a nevet” mondata kimarad, és a név nélküli '
        'segítségül hívás is (Róm 10:12, 10:14, 2Tim 2:22). A mérce a Károli alapszövege, a Textus Receptus; az ApCsel '
        '22:16-ban a Textus Receptus a név után az Urat mondja, a kritikai szövegkiadás az Úr helyett névmást olvas (az ő '
        'nevét). Kivétel az 1Kir 18:25-26: itt a név után „a ti istenteknek”, illetve „a Baálnak” neve áll, és a két '
        'vers a Kármel-hegyi jelenet ellenpontjaként marad a motívumban. Nem tartozik ide a szenvedő szerkezet sem '
        '(nikrá … al), amely azt mondja ki, hogy egy nép, egy ház vagy a láda az Úr nevét viseli, vagyis az övé (például '
        '2Sám 6:2, Jer 7:10-14, 5Móz 28:10): ez hovatartozás, nem segítségül hívás, akkor is, ha ugyanaz a két szó áll '
        'benne; az Újszövetségben ilyen a Zsid 11:16, ahol Isten nem szégyenli, „hogy Istenöknek neveztessék”. A 2Móz '
        '33:19 és 34:5 a formula szerkezetét hordozza, a név után az Úr nevével; a magyar fordítás ott kiáltásként, '
        'kihirdetésként adja vissza.'),
    # 12., 20.: Miért fontos, H7121
    '**Jelentősége:** a BDB a hívás igéjének két jelentését': (
        '**Jelentősége:** a BDB a hívás igéjének két jelentését választja szét, és a motívum helyei mindkettőben '
        'előfordulnak. A Qal 2.c jelentés a segítségül hívás: a szótár meghatározása szerint az Úr nevével hívni, azaz a '
        'nevet használni a segítségül hívásban, és ide sorolja az 1Móz 4:26-ot, a 12:8-at, a 2Kir 5:11-et, az 1Kir '
        '18:24-et, a Baál nevével pedig az 1Kir 18:24-26-ot. Ugyanide teszi a Jer 10:25-öt és a vele azonos Zsolt 79:6-ot '
        'is; ezeket a motívum nem veszi fel, mert bennük az Úr neve helyén névmási rag áll. A Qal 3.b jelentés a név '
        'kihirdetése, és ide a 2Móz 33:19-et és a 34:5-öt teszi, az 5Móz 32:3 és a Zsolt 99:6 mellé. A motívum a két '
        'jelentést nem a szótár szerint választja szét, hanem a szerkezet szerint: a 2Móz 33:19-ben és a 34:5-ben is a '
        'hívás igéje, a név és utána az Úr neve áll. A szótári jelentés a szóról szól, a motívum a formula funkciójáról; '
        'a kettő egymás mellett áll. A motívum helyei közül a szócikk ezeket nem idézi: 1Móz 13:4, 21:33, 26:25, a Zsolt '
        '116 három verse, Jóel 2:32 és Sof 3:9.'),
    # 13., 20.: Miért fontos, a görög fordítás
    '**Jelentősége:** a héber hívás-ige görög megfelelőiből': (
        '**Jelentősége:** a héber hívás-ige görög megfelelőiből a 4.7 pont szójegyzéke 49 különböző szót sorol fel, a '
        'formula helyein viszont a görög fordítás többnyire ugyanazt az igét választja. A 16 ószövetségi versből 13-ban '
        'az ἐπικαλέω (epikaleó) áll, ugyanaz, amelyet az Újszövetség használ: 12-ben egyedül, az 1Kir 18:24-ben pedig '
        'Illés hívásánál, ahol a héber hívás-ige kétszer szerepel, és a görög a Baál prófétáinak hívását a kiáltás '
        'igéjével (βοάω, boaó) adja vissza. A 2Móz 33:19-ben és a 34:5-ben ugyanennek a szócsaládnak egy másik tagja, az '
        'előtag nélküli καλέω (kaleó) áll. A Zsolt 116:17-ben az itt használt görög szövegkiadásban hiányzik a segítségül '
        'hívás mondata (l. a nyitott kérdéseket). A görög fordító tehát a formulát többnyire a segítségül hívás igéjével '
        'hozza; az Úr Mózesnek tett ígéretében és a hozzá tartozó jelenetben az előtag nélküli igét írja.'),
    # 10., 11.: Peshat
    '**Peshat — a formula szavai.**': (
        '**Peshat — a formula szavai.** A formula három szóból áll: a hívás igéjéből (kárá), a névből egy elöljárószóval '
        '(besém, „a nevén”, „a névvel”) és az Úr nevéből (Jahve). Szó szerint tehát nem kérést mond, hanem azt, hogy '
        'valaki az Úrhoz a nevén szól. Az ige önmagában hívást, kiáltást vagy elnevezést jelent; a segítségül hívás '
        'jelentését az ige és a név együttese adja meg, ezért a Károli a Baál nevének hívását is „segítségül hív”-nak '
        'fordítja (1Kir 18:25-26), és a BDB is ugyanabba a jelentésbe sorolja. A motívumhoz az a hely tartozik, ahol a név '
        'után az Úr neve áll. A Genezis helyein a formula cselekvést rögzít: oltárépítés után (1Móz 12:8, 26:25), '
        'ugyanannál az oltárnál visszatérve (1Móz 13:4), fa ültetése után (1Móz 21:33). A Targum, a héber szöveg arámi '
        'fordítása, ezen a négy helyen a hívás igéje helyett az imádkozás igéjét (celá) írja; ugyanezt az igét használja '
        'az 1Móz 4:26-ban is, ott azonban a mondatot megfordítja: szerinte Énós napjaiban az emberek felhagytak az '
        'imádkozással az Úr nevében. A görög fordítás ugyanitt azt mondja, hogy Énós „remélte” (ἤλπισεν, élpiszen) '
        'segítségül hívni az Úr nevét. A motívum a héber szöveget és a Károlit követi, amely a kezdetet mondja ki. A 2Móz '
        '33:19-ben és 34:5-ben a Targum megtartja a hívás igéjét (kerá).'),
    # 1., 4., 5.: Remez
    '**Remez — hová mutat a formula.**': (
        '**Remez — hová mutat a formula.** A motívum helyei közötti erős kapcsolatok közül három csoport emelkedik ki; a '
        'többi erős kapcsolat a Genezis helyeit és az 1Móz 4:26-ot köti a későbbi helyekhez. Az első csoport Jóel '
        'ígéretétől vezet az Újszövetségig: az ApCsel 2:21 görögül szó szerint a Jóel 2:32 görög fordítását hozza, a Róm '
        '10:13 ugyanezt a mondatot a bevezető tagmondat (καὶ ἔσται, kai esztai) nélkül, egy kötőszóval (γάρ, gar). A '
        'második a Kármel-hegyi jelenet: Illés ugyanazzal a formulával szólítja fel a Baál prófétáit, amellyel ő maga az '
        'Úr nevét hívja, és a vers maga kimondja a mércét: „a mely isten tűz által felel, az az Isten” (1Kir 18:24). A '
        'harmadik a 116. zsoltár: ugyanaz a beszélő háromszor mondja ki ugyanazt a mondatot, előbb a bajban (116:4), '
        'aztán a szabadulás után a pohárnál és a hálaáldozatnál (116:13, 17). Közepes erősségű kapcsolat köti az 1Móz '
        '4:26-ot a 2Kir 5:11-hez, ahol az Úr neve mellett „az ő Istenének” megnevezése is áll, és a Róm 10:13-at az 1Kor '
        '1:2-höz és az ApCsel 22:16-hoz: ezekben a kapcsolat a közös szavakon áll, idézés nélkül.'),
    # 3., 16., 22.: Drash
    '**Drash — mit tanít.**': (
        '**Drash — mit tanít.** A helyek együttese három tételt mutat. Az első: a formula a névhez kötött. A '
        'Kármel-hegyen a hívás igéje és a név szerkezete mindkét oldalon ugyanaz, a különbség a név után álló szó: az Úr '
        'neve vagy a Baálé, és a Baál nevének hívására „nem jött szó, sem felelet” (1Kir 18:26). A második: a segítségül '
        'hívás egy-egy ember cselekvéséből általános ígéretté tágul. A Genezis helyein egy ember vagy egy nemzedék hívja '
        'segítségül az Urat; Jóelnél „mindaz”, aki segítségül hívja, megmenekül (Jóel 2:32), Sofóniásnál a népek ajka '
        'változik meg, hogy „mind segítségül hívják az Úr nevét” (Sof 3:9), és Pál a Jóel-idézet előtt kimondja, hogy '
        '„nincs különbség zsidó meg görög között” (Róm 10:12). A harmadik: az Újszövetség egyik helyén a név után Jézus '
        'Krisztus neve áll: a korinthusi levél a gyülekezetet azokkal együtt köszönti, „a kik a mi Urunk Jézus Krisztus '
        'nevét segítségül hívják bármely helyen” (1Kor 1:2); hogy a Róm 10:13 „Ura” is őt jelenti-e, az a vitatott pontok '
        'kérdése. Ez a lap olvasata: a helyek azt mutatják, hogy a formulát a név határozza meg, és hogy a formula köre a '
        'helyek sorában egyre tágul.\n\n'
        '*Proveniencia: scope=1Kir 18:26, Jóel 2:32, Sof 3:9, Róm 10:12, 1Kor 1:2 (a Károli-szöveg) | '
        'forras=konkordancia/Karoli_1908.tsv | ts=2026-11-12 · a helyek sora: scope=adat/elofordulasok.tsv '
        '(id=ISTENTISZT-001) | forras=split(\'\\t\') | n=20 | ts=2026-11-12*'),
    # 19., 22.: Sod
    '**Sod — a név, amelyet hívnak, és amelyet kimondanak.**': (
        '**Sod — a név, amelyet hívnak, és amelyet kimondanak.** A formula szerkezete két irányban áll a motívumban. Az '
        'ember szájában segítségül hívás: Énós nemzedéke, Ábrám és Izsák, a zsoltáros, és Jóel ígérete szerint mindenki, '
        'aki segítségül hívja, az Úr nevét hívja segítségül. Az Úr saját mondatában ugyanez a szerkezet szól: „kiáltom '
        'előtted az Úr nevét” (2Móz 33:19). A 34:5 ugyanezt a szerkezetet hozza a kiáltó megnevezése nélkül, és a '
        'következő versben „az Úr elvonula ő előtte és kiálta: Az Úr, az Úr” (2Móz 34:6). A motívum helyei szerint tehát '
        'az a név, amelyet az ember segítségül hív, ugyanaz, amelyet az Úr maga kiált ki Mózes előtt.\n\n'
        '*Proveniencia: scope=2Móz 33:19, 34:5, 34:6 (a Károli-szöveg és a héber szerkezet) | '
        'forras=konkordancia/Karoli_1908.tsv + TAHOT_kivonat.tsv | ts=2026-11-12*'),
    # 6., 7., 8.: vitatott pont, 2Móz 34:5
    '**A 2Móz 33:19 és 34:5: kiáltás vagy segítségül hívás.**': (
        '**A 2Móz 34:5: ki kiált a néven.** A 2Móz 33:19-ben az Úr beszél („kiáltom előtted az Úr nevét”), a kérdés a '
        '34:5, ahol ugyanez a szerkezet a kiáltó megnevezése nélkül áll: „és ott álla ő vele, és nevén kiáltá az Urat”. '
        'Az egyik olvasat szerint itt az Úr kiáltja ki a saját nevét, ahogy a 33:19-ben ígérte: a következő versben „az '
        'Úr elvonula ő előtte és kiálta: Az Úr, az Úr” (2Móz 34:6); a BDB a két helyet a név kihirdetéséhez sorolja, a '
        'görög fordítás az előtag nélküli καλέω (kaleó) igét írja, a Targum pedig nem az imádkozás igéjét, hanem a '
        'hívásét. A másik olvasat szerint a 34:5-ben Mózes hívja segítségül az Úr nevét: a héber mondat a kiáltót külön '
        'nem nevezi meg, a szerkezet ugyanaz, mint az emberi segítségül hívás helyein, és a latin fordítás, a Vulgata így '
        'is érti: nála Mózes áll ott az Úrral, és ő hívja segítségül az Úr nevét (stetit Moyses cum eo, invocans nomen '
        'Domini). A lap a kérdést nem dönti el; mindkét hely a formula szerkezete miatt tartozik a motívumhoz.'),
    # 9.: az 1Móz 4:26 nem vitatott pont, hanem hatástörténeti adat (a Peshatba került) — a bekezdés kimarad
    '**Az 1Móz 4:26: kezdet vagy hanyatlás.**': None,
    # 18.: Róm 10:13
    '**A Róm 10:13 „Ura”: az Úr Jóel könyvében, vagy Jézus.**': (
        '**A Róm 10:13 „Ura”: az Úr Jóel könyvében, vagy Jézus.** Pál a Jóel 2:32-t idézi, ahol a héber szövegben az '
        'Úr neve, a יְהוָה (Jahve) áll, és a görög fordítás ezt κύριος (küriosz) szóval adja vissza. Az egyik olvasat '
        'szerint a Róm 10:13 „Úr”-a ugyanaz, mint Jóelnél: Pál mondata a Jóel 2:32 görög fordításának mondata, amelyben '
        'a κύριος a héber Jahve helyén áll, és a mondat az idézetben sem kap új alanyt. A másik szerint az Úr itt Jézus: '
        'négy verssel korábban Pál azt írja: „ha a te száddal vallást teszel az Úr Jézusról, és szívedben hiszed, hogy az '
        'Isten feltámasztotta őt a halálból, megtartatol” (Róm 10:9), és az 1Kor 1:2-ben a segítségül hívott név Jézus '
        'Krisztus neve. A Thayer-szótár a görög ige ezen jelentésénél a második olvasatot adja. A lap a kérdést nem '
        'dönti el.'),
    # 22.: a határ második ellenőrzése, a kiinduló számmal
    '**A határ második ellenőrzése.**': (
        '**A határ második ellenőrzése.** A listát kétszer nézte át egy második olvasó, aki nem vett részt az '
        'összeállításában, és a határ következetességét kérdezte; a kérdésekben a szerkesztő döntött. Az első kör a 33 '
        'helyes listán futott. Nyomán kikerültek azok a helyek, amelyekben a név után nem az Úr neve, hanem névmási rag '
        'áll (például a Zak 13:9), és az újszövetségi helyek közül azok, amelyekben a név nem hangzik el (Róm 10:12, '
        '10:14, 2Tim 2:22, 1Pét 1:17); a Zsolt 99:6 kint maradt, mert benne a hívás és a név nem a formula szerkezetében '
        'áll. A 2Móz 33:19 és 34:5 bent maradt, mert a név után az Úr neve áll, és az 1Kir 18:25-26 ellenpontként maradt '
        'bent, kimondott kivételként. Így a 33 helyből 22 maradt. A második kör ugyanezt a mércét alkalmazta az '
        'Újszövetségre: az ApCsel 9:14 és 9:21 kikerült, mert bennük a név után nem az Úr megnevezése áll, hanem '
        '„nevedet”, illetve „ezt a nevet”. Így lett a 22 helyből 20.'),
    # 14.: a görög mérce
    '**Melyik görög szöveg a mérce.**': (
        '**Melyik görög szöveg a mérce.** Az újszövetségi helyeknél a Károli alapszövege, a Textus Receptus a mérce. A '
        'négy újszövetségi hely közül egyben tér el a kritikai szövegkiadás, és ott sem a görög igében, hanem a név után '
        'álló szóban: az ApCsel 22:16-ban a Textus Receptus az Urat mondja (τοῦ κυρίου, tú küriú), a kritikai kiadás '
        'névmást, az ő nevét (αὐτοῦ, autú); a latin Vulgata itt a kritikai szöveget követi. A görög igét érintő '
        'szövegváltozat egyik helyen sincs (l. a 9. szakasz újszövetségi táblázatát); az ApCsel 2:21 és az 1Kor 1:2 '
        'szövegváltozatai a formulát nem érintik, a Róm 10:13-on nincs szövegváltozat.'),
}


def main():
    sorok = open(P, encoding='utf-8').read().split('\n')
    hasznalt = set()
    ki = []
    i = 0
    while i < len(sorok):
        s = sorok[i]
        talalt = [k for k in UJ if s.startswith(k)]
        if talalt:
            k = talalt[0]
            assert k not in hasznalt, k
            hasznalt.add(k)
            if UJ[k] is None:
                # a bekezdés és az utána álló üres sor kimarad
                if i + 1 < len(sorok) and sorok[i + 1] == '':
                    i += 1
            else:
                ki.append(UJ[k])
        else:
            ki.append(s)
        i += 1
    hianyzik = set(UJ) - hasznalt
    assert not hianyzik, hianyzik
    open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(ki))
    print('%s: %d bekezdés cserélve vagy kivéve' % (P, len(hasznalt)))


if __name__ == '__main__':
    main()
