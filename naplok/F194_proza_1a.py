# -*- coding: utf-8 -*-
"""F194.23 — az ISTENTISZT-001 2. kiadása, U3: az 1/a prózája (adat/elofordulasok.tsv `kapcsolodas`, `funkcio`).

A 20 igehely leíró mondata és „Funkció:” sora nulláról, egy kézből (claude-opus-5-5), a 10-es prompt és a 9-es sablon
„Az 1/a igehelyenkénti prózája” szerint: kerek mondat, az idézet a Károli-vers szó szerinti része, a funkció
„címke — magyarázat”. A 2Móz 33:19 és 34:5 a DT-F194b szerint: a héber szerkezet azonos, a magyar fordítás kiáltásként
adja vissza; a „be nem sorolható” jelölés kikerül. A régi mondatból nem költözik át szöveg.

Írás előtt: minden idézet („…”) a vers Károli-szövegében áll (konkordancia/Karoli_1908.tsv); csak a 20 sor három
mezője változhat (összevetés); a `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F194_proza_1a.py [--ir]"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/elofordulasok.tsv'
MOT = 'ISTENTISZT-001'
PROV = ('scope=manual | forras=F194 ISTENTISZT-001 2. kiadás, U3 (claude-opus-5-5; a Károli-vers: '
        'konkordancia/Karoli_1908.tsv; a 2Móz 33:19, 34:5: DT-F194b) | ts=2026-11-12')

UJ = {
    '1Móz 4:26': (
        'Séth fiának, Énósnak születése után a vers egy kort jelöl meg: „Akkor kezdték segítségül hívni az Úrnak '
        'nevét”. A motívum helyei közül ez az első; a mondat nem nevez meg személyt, azt mondja ki, hogy ekkor '
        'kezdődött a segítségül hívás.',
        '🌱 kezdet — a motívum első helye: a segítségül hívás kezdetét mondja ki, személy megnevezése nélkül'),
    '1Móz 12:8': (
        'Ábrám Béthel és Hái között felüti a sátrát, „és ott oltárt építe az Úrnak, és segítségűl hívá az Úr '
        'nevét”. A motívum helyei közül itt kapcsolódik először a segítségül hívás az oltárépítéshez; a kettő az '
        '1Móz 13:4-ben és a 26:25-ben is együtt áll.',
        '🔁 oltár és név — a segítségül hívás az oltárépítéshez kapcsolódik'),
    '1Móz 13:4': (
        'Ábrám visszamegy annak az oltárnak a helyére, „melyet ott elsőben készített vala”, és ott ismét „segítségűl '
        'hívá ott Ábrám az Úrnak nevét”. A vers maga utal vissza az 1Móz 12:8 oltárára: a segítségül hívás ugyanazon '
        'a helyen ismétlődik.',
        '🔁 visszatérés — ugyanannál az oltárnál ismétlődik a segítségül hívás'),
    '1Móz 21:33': (
        'Ábrahám tamariskusfákat ültet Beérsebában, „és segítségűl hívá ott az örökkévaló Úr Istennek nevét”. A név '
        'mellett itt isteni jelző is áll: az örökkévaló Isten, a héberben אֵל עוֹלָם (él olám); oltárt a vers nem '
        'említ.',
        '➕ jelzővel bővült név — a segítségül hívott név mellé az örökkévaló Isten jelzője kerül'),
    '1Móz 26:25': (
        'Izsák oltárt épít, „és segítségűl hívá az Úrnak nevét”, felüti a sátrát, szolgái pedig kutat ásnak. Ugyanaz '
        'a három elem áll itt, oltár, sátor és segítségül hívás, mint Ábrám helyén az 1Móz 12:8-ban: a gyakorlatot a '
        'következő nemzedék folytatja.',
        '👨‍👦 öröklés — Ábrahám gyakorlatát Izsák ugyanazokkal az elemekkel folytatja'),
    '2Móz 33:19': (
        'Az Úr azt ígéri Mózesnek, hogy dicsősége elvonul előtte, és azt mondja: „kiáltom előtted az Úr nevét”. A '
        'héber szerkezet ugyanaz, mint a segítségül hívás formulájában, a hívás igéje, a név és utána az Úr neve; a '
        'magyar fordítás itt kiáltásként adja vissza, nem segítségül hívásként.',
        '📣 kiáltás a néven — a formula szerkezete az Úr saját mondatában; a fordítás kiáltásként adja vissza'),
    '2Móz 34:5': (
        'Az Úr felhőben leszáll, „és ott álla ő vele, és nevén kiáltá az Urat”. Ez a 2Móz 33:19-ben ígért jelenet; a '
        'héberben ugyanaz a szerkezet áll, a magyar fordítás itt is kiáltásként adja vissza, és a vers nem mondja meg, '
        'ki áll ott és ki a kiáltó.',
        '📣 kiáltás a néven — a 2Móz 33:19-ben ígért jelenetben ugyanaz a szerkezet áll'),
    '1Kir 18:24': (
        'Illés két hívást állít szembe egymással: „hívjátok segítségül a ti istenteknek nevét, és én is segítségül '
        'hívom az Úrnak nevét”. Az lesz az Isten, aki tűz által felel: a formula itt annak a mércéje, melyik név '
        'hívására jön válasz, és a vers a két név hívását egy mondatban mondja ki.',
        '⚔️ szembeállítás — a formula két név hívását állítja egymással szembe'),
    '1Kir 18:25': (
        'Illés felszólítja a Baál prófétáit, hogy készítsék el elsőként a tulkot, „és hívjátok segítségül a ti '
        'istenteknek nevét”. A név után itt nem az Úr neve áll, hanem a „ti istenteknek” neve, a héberben אֱלֹהֵיכֶם '
        '(elóhéchem); a hely ellenpontként tartozik a motívumhoz.',
        '⚔️ ellenpont — Illés a Baál prófétáit a formulával szólítja fel, az Úr neve nélkül'),
    '1Kir 18:26': (
        'A Baál prófétái reggeltől délig „segítségül hívák a Baálnak nevét”, de „nem jött szó, sem felelet”. A '
        'formula szerkezete megvan, a név helyén azonban a Baál neve áll, a héberben הַבַּעַל (habbaal), és a hívásra '
        'nincs válasz.',
        '⚔️ válasz nélküli hívás — a Baál nevének hívására nem jön felelet'),
    '2Kir 5:11': (
        'Naámán haragjában elmondja, mit várt Elizeustól: hogy kijön hozzá, és „segítségül hívja az Úrnak, az ő '
        'Istenének nevét”. A formulát itt egy idegen mondja ki, Izrael prófétájának várt cselekvéseként, a gyógyítás '
        'mozdulata előtt.',
        '👁️ kívülálló szemével — egy idegen ismeri a formulát, és a prófétától várja'),
    'Zsolt 116:4': (
        'A zsoltáros felidézi a bajt, amelyben volt: „És az Úrnak nevét segítségül hívám”, és kéri, hogy az Úr '
        'szabadítsa meg a lelkét. A formula itt első személyben, a szabadulásért mondott könyörgés szavaként áll.',
        '🙏 könyörgés — a segítségül hívás a bajban mondott személyes kérés'),
    'Zsolt 116:13': (
        'A megszabadult zsoltáros fogadalma: „A szabadulásért való poharat felemelem, és az Úrnak nevét hívom '
        'segítségül”. Ugyanaz a formula, amely a zsoltár 4. versében a bajban hangzott el, itt a hála cselekvésének '
        'része.',
        '🍷 hála — a szabadulás után ugyanaz a formula a hálaadás része'),
    'Zsolt 116:17': (
        'A zsoltár harmadszor mondja ki a formulát: „Néked áldozom hálaadásnak áldozatával, és az Úr nevét hívom '
        'segítségül”. A segítségül hívás itt a hálaáldozat mellett áll, a 13. vers fogadalmát ismételve.',
        '🔁 ismétlés a hálaáldozatnál — a zsoltár harmadik segítségül hívása'),
    'Jóel 2:32': (
        'A próféta ígérete szerint „mindaz, a ki az Úrnak nevét hívja segítségül, megmenekül”, mert a Sion hegyén és '
        'Jeruzsálemben lesz a szabadulás. A héber szöveg számozása szerint ez a Jóel 3:5; a vers görög fordítását '
        'idézi az Újszövetség (ApCsel 2:21, Róm 10:13).',
        '🎯 ígéret — a segítségül hívás a megmenekülés feltétele; az Újszövetség ezt a mondatot idézi'),
    'Sof 3:9': (
        'Isten azt ígéri, hogy a népek ajkát tisztává változtatja, „hogy mind segítségül hívják az Úr nevét, hogy egy '
        'akarattal szolgálják őt”. A formula itt nem egy ember vagy Izrael cselekvése, hanem a népekre vonatkozó '
        'jövőbeli ígéret.',
        '🔮 a népek ígérete — a segítségül hívás minden népre kiterjed'),
    'ApCsel 2:21': (
        'Péter a pünkösdi beszédében Jóel próféciáját idézi: „mindaz, a ki az Úrnak nevét segítségül hívja, '
        'megtartatik”. A görög mondat szó szerint a Jóel 2:32 görög fordítása, az ἐπικαλέω (epikaleó) igével és a '
        'névvel.',
        '🎯 idézet — a Jóel-ígéret az Újszövetségben, szó szerint'),
    'ApCsel 22:16': (
        'Pál megtérésének elbeszélésében Ananiás így szól hozzá: „Kelj fel és keresztelkedjél meg és mosd le a te '
        'bűneidet, segítségül híván az Úrnak nevét.” A segítségül hívás a keresztség mellett áll; a Textus Receptus '
        'itt az Úr nevét mondja (τοῦ κυρίου, tú küriú), a kritikai szövegkiadás az ő nevét (αὐτοῦ, autú).',
        '💧 keresztség — a segítségül hívás a megtérés és a keresztség mellett'),
    'Róm 10:13': (
        'Pál a hitről és a vallástételről szóló érvelésében Jóelt idézi: „minden, a ki segítségül hívja az Úr nevét, '
        'megtartatik”. A görög mondat a Jóel 2:32 görög fordításának mondata, a bevezető tagmondat (καὶ ἔσται, kai '
        'esztai) nélkül és egy kötőszóval (γάρ, gar); az előző vers szerint ebben nincs különbség zsidó és görög között.',
        '🎯 idézet — Pál a Jóel-ígéretet mindenkire érvényesnek mondja'),
    '1Kor 1:2': (
        'Pál a korinthusi gyülekezetet köszönti, „mindazokkal egybe, a kik a mi Urunk Jézus Krisztus nevét segítségül '
        'hívják bármely helyen”. A név után itt Jézus Krisztus neve áll, és a vers a gyülekezet mellé állítja mindazokat, '
        'akik őt segítségül hívják.',
        '⛪ Jézus Krisztus neve — a segítségül hívók Jézus Krisztus nevét hívják, a gyülekezettel együtt'),
}

KULSO_VERS = {'ApCsel 22:16': None, 'Róm 10:13': None}  # a mondat a szomszédos versre csak hivatkozik, nem idéz


def main(ir):
    sorok = open(UT, encoding='utf-8', newline='').read().split('\n')
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    fej = sorok[fej_i].split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    karoli = {l.split('\t', 1)[0]: l.split('\t', 1)[1].rstrip('\r') for l in
              open('konkordancia/Karoli_1908.tsv', encoding='utf-8').read().split('\n')[1:] if '\t' in l}
    eredeti = list(sorok)
    latott = set()
    for n in range(fej_i + 1, len(sorok)):
        r = sorok[n].split('\t')
        if len(r) < 2 or r[0] != MOT:
            continue
        hely = r[1]
        assert hely in UJ, hely
        kap, funk = UJ[hely]
        for idezet in re.findall(r'„([^”]+)”', kap):
            if idezet in ('ti istenteknek',):
                assert idezet in karoli[hely]
                continue
            assert idezet.rstrip('.') in karoli[hely], (hely, idezet)
        assert ' — ' in funk and '„' not in funk, hely
        r[ix['kapcsolodas']], r[ix['funkcio']], r[ix['proveniencia']] = kap, funk, PROV
        sorok[n] = '\t'.join(r)
        latott.add(hely)
    assert latott == set(UJ), set(UJ) - latott
    elter = [i for i in range(len(sorok)) if sorok[i] != eredeti[i]]
    assert 1 <= len(elter) <= 20, len(elter)   # F194.23: az első írás 20 sor, a javítókör kevesebb
    print('%s: %d sor (%s), mezők: kapcsolodas, funkcio, proveniencia' % (UT, len(elter), MOT))
    if ir:
        open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
    else:
        print('(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
