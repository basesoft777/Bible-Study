"""F239 U2 — a TEREMT-001 nyitott jelöltjeinek döntése (egyszeri szkript).

Az U1 28 `nyitva` blokksorát a lexikai negatív kritérium szerint dönti el (`elutasítva`, olvasói indoklással),
felvesz két Septuaginta-többlet sort (Jób 36:16, Zsolt 71:21: a görögben ἄβυσσος, a héberben nincs tehóm),
és a 2Pét 2:4 régi indoklásának vegyes írású szavát (ábüσσος) javítja. A határ indoklása: naplok/F239_hatar.md.

Futtatás: python naplok/F239_U2_jelolt_dontes.py        (száraz: csak kiírja a változást)
          python naplok/F239_U2_jelolt_dontes.py --ir   (írás; előtte és utána soronkénti összevetés)
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/jeloltek.tsv'
DATUM = '2026.11.23'
REF = 'F239 U2 · naplok/F239_hatar.md · motivumok.tsv negativ_kriterium'
VEG = 'A motívumba csak az a hely tartozik, ahol a héber szövegben a tehóm, az Újszövetségben az ἄβυσσος áll.'


def lex(n, karoli, szo, atiras, jelentes, toldalek=''):
    hol = 'ezekben a versekben főként' if n > 1 else 'itt'
    return ('Összesítő sor %d versre: a Károli %s szava %s a(z) %s (%s, „%s”) fordítása, nem a tehómé; '
            'a tehóm és az ἄβυσσος a versekben nem áll.%s %s' % (n, karoli, hol, szo, atiras, jelentes, toldalek, VEG))


def osztalytalan(n, karoli, toldalek=''):
    return ('Összesítő sor %d versre: a Károli %s szava itt nem a tehómot fordítja, hanem más szót vagy körülírást; '
            'a tehóm és az ἄβυσσος a versekben nem áll.%s %s' % (n, karoli, toldalek, VEG))


# igehely → új indoklás (a 28 U1-sor; a versszám a blokkok-fájlból, a lexéma a gépi glossza-illesztésből, ellenőrizve)
DONTES = {
    '1Kir 4:29': osztalytalan(8, '„mély” csoportjának'),
    '1Kor 2:10': lex(6, '„mélység” csoportjának', 'βάθος', 'bathosz', 'mélység'),
    '1Móz 2:21': lex(6, '„mély (álom)”', 'תַּרְדֵּמָה', 'tardémá', 'mély álom'),
    '1Sám 17:49': ('Összesítő sor 2 versre: az 1Sám 17:49-ben a Károli „mélyede” szava a טָבַע (tába, „belesüllyed”) '
                   'fordítása; a Zsolt 69:3 „mély” és „örvény” szava a מְצוֹלָה (mecólá, „a tenger mélye”) és a '
                   'שִׁבֹּלֶת (sibbólet, „áradat”) fordítása. A tehóm és az ἄβυσσος a versekben nem áll. ' + VEG),
    '2Kor 11:25': lex(1, '„mélység”', 'βυθός', 'büthosz', 'a nyílt tenger mélye'),
    '2Sám 22:16': osztalytalan(2, '„örvény”'),
    '2Sám 22:17': osztalytalan(15, '„mélység” csoportjának'),
    '3Móz 13:3': lex(15, '„mély/mélyebb” csoportjának', 'עָמֹק', 'ámók', 'mély'),
    'ApCsel 20:9': lex(3, '„mély” csoportjának', 'βαθύς', 'bathüsz', 'mély'),
    'Dán 2:22': lex(1, '„mély”', 'עֲמִיק', 'ámík, arámi', 'mély dolog'),
    'Ez 23:34': osztalytalan(3, '„fenékig”'),
    'Ez 26:20': lex(9, '„mélység” csoportjának', 'בּוֹר', 'bór', 'verem, gödör'),
    'Ez 27:34': lex(3, '„mélység” csoportjának', 'מַעֲמַקִּים', 'maamakkím', 'mélységek'),
    'Hós 9:9': lex(7, '„mélyen” csoportjának', 'עָמַק', 'ámak', 'mélyre ás, mélyen tesz'),
    'Ján 4:11': lex(1, '„mély”', 'βαθύς', 'bathüsz', 'mély', ' A „kút” a φρέαρ (phrear).'),
    'Jób 12:22': lex(1, '„mélységes (titkok)”', 'עָמֹק', 'ámók', 'mély dolog'),
    'Jób 41:31': lex(10, '„mélység/örvény” csoportjának', 'מְצוֹלָה', 'mecólá', 'a tenger mélye',
                     ' A Jób 41:31-ben a görög fordítás erre a szóra ἄβυσσος-t hoz, de a héberben nem a tehóm áll.'),
    'Luk 6:48': lex(1, '„mélyre”', 'βαθύνω', 'bathünó', 'mélyre ás'),
    'Mt 18:6': lex(1, '„(a tenger) mélysége”', 'πέλαγος', 'pelagosz', 'nyílt tenger'),
    'Péld 9:18': lex(1, '„(a pokol) mélye”', 'עָמֵק', 'ámék', 'mély'),
    'Péld 22:14': lex(2, '„mély”', 'שׁוּחָה', 'súhá', 'verem'),
    'Péld 25:3': lex(1, '„mélység”', 'עֹמֶק', 'ómek', 'mélység'),
    'Zsolt 7:16': lex(1, '„mélyre (vájja)”', 'חָפַר', 'háfar', 'ás', ' A „verem” a שַׁחַת (sahat).'),
    'Zsolt 69:16': lex(1, '„örvény”', 'מְצוֹלָה', 'mecólá', 'a tenger mélye', ' A „verem” a בְּאֵר (beér).'),
    'Zsolt 95:4': lex(1, '„mélység”', 'מֶחְקָר', 'mehkár', 'kikutatott mély hely'),
    'Zsolt 106:43': lex(1, '„mélyebben”', 'מָכַךְ', 'mákak', 'lesüllyed'),
    'Ézs 44:27': ('A Septuaginta többlete: a görög fordítás itt ἄβυσσος-t hoz, a héber szövegben viszont nem a tehóm '
                  'áll, hanem a צוּלָה (cúlá, „a tenger mélye”); a Károli „mélység” szava ezt fordítja. ' + VEG),
    'Jób 42:8': ('Adathiba: a szótár a tehóm szócikkében a Zsolt 42:8-at idézi, a feldolgozás a könyv nevét elhagyta, '
                 'és a hivatkozás a Jób 42:8-ra került. A Jób 42:8-ban a tehóm nem áll; a Zsolt 42:8 a motívum helye.'),
}

UJ_FORRAS = ('F239 U1 LXX-híd: a Septuaginta ἄβυσσος-verse, a héber versben a tehóm nélkül '
             '(naplok/F239_U1_TEREMT-001_lxx_g0012.tsv) | scope=LXX_OS-teljes (G0012) × TAHOT_kivonat.tsv (H8415) '
             '| forras=konkordancia/LXX_OS/*.tsv | ts=2026-11-23')
UJ_SOROK = [
    ('Jób 36:16', 'A Septuaginta többlete: a görög fordítás itt ἄβυσσος-t hoz („mélység, alatta zuhatag”), a héber '
                  'szövegben viszont a רַחַב (rahab, „tág tér”) áll, a Károli „tág mezőre” szavával; tehóm a versben '
                  'nem áll. ' + VEG),
    ('Zsolt 71:21', 'A Septuaginta többlete: a görög fordítás az előző vers mondatát („a föld mélységeiből ismét '
                    'felhoztál”) itt megismétli, ἄβυσσος-szal; a héber versben és a Károliban („Megsokasítod az én '
                    'nagyságomat”) tehóm nem áll. A szó a Zsolt 71:20-ban áll, az a motívum helye. ' + VEG),
]

REGI_HIBA = ('ábüσσος', 'ἄβυσσος')


def beolvas():
    with open(UT, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def main():
    ir = '--ir' in sys.argv
    sorok = beolvas()
    fej_i = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    fej = sorok[fej_i].split('\t')
    k = {n: i for i, n in enumerate(fej)}
    uj = list(sorok)
    valtozott, talalt = [], set()
    for i, s in enumerate(sorok):
        if i <= fej_i or not s:
            continue
        m = s.split('\t')
        if m[0] != 'TEREMT-001' or m[k['jelolt_tipus']] != 'elofordulas':
            continue
        hely = m[k['igehely']]
        if m[k['dontes']] == 'nyitva' and hely in DONTES:
            m[k['dontes']] = 'elutasítva'
            m[k['indoklas']] = DONTES[hely]
            m[k['datum']] = DATUM
            m[k['dontes_ref']] = REF
            talalt.add(hely)
        elif hely == '2Pét 2:4' and REGI_HIBA[0] in m[k['indoklas']]:
            m[k['indoklas']] = m[k['indoklas']].replace(*REGI_HIBA)
        else:
            continue
        uj[i] = '\t'.join(m)
        valtozott.append(i)
    hiany = set(DONTES) - talalt
    if hiany:
        sys.exit('HIBA: nem talált nyitva sor: %s' % ', '.join(sorted(hiany)))
    letezo = {(s.split('\t')[0], s.split('\t')[1]) for s in sorok[fej_i + 1:] if s}
    veg = len(uj)
    while veg and uj[veg - 1] == '':
        veg -= 1
    hozzafuz = []
    for hely, ind in UJ_SOROK:
        if ('TEREMT-001', hely) in letezo:
            sys.exit('HIBA: kulcsütközés: TEREMT-001 %s' % hely)
        m = [''] * len(fej)
        m[k['id']], m[k['igehely']], m[k['forras_kereses']] = 'TEREMT-001', hely, UJ_FORRAS
        m[k['dontes']], m[k['indoklas']], m[k['datum']] = 'elutasítva', ind, DATUM
        m[k['jelolt_tipus']], m[k['dontes_ref']] = 'elofordulas', REF
        hozzafuz.append('\t'.join(m))
    uj = uj[:veg] + hozzafuz + uj[veg:]
    # összevetés: minden nem érintett sor bájtra azonos, ugyanazon a helyen
    for i, s in enumerate(sorok[:veg]):
        if i not in valtozott and uj[i] != s:
            sys.exit('HIBA: nem érintett sor változott: %d' % (i + 1))
    print('változott sor: %d (ebből 28 döntés, %d javítás), új sor: %d'
          % (len(valtozott), len(valtozott) - 28, len(hozzafuz)))
    if not ir:
        for i in valtozott:
            print('  %d: %s' % (i + 1, uj[i].split('\t')[1]))
        return
    with open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj))
    vissza = beolvas()
    if vissza != uj:
        sys.exit('HIBA: visszaolvasás eltér')
    print('írva: %s (%d sor)' % (UT, len([s for s in vissza if s])))


if __name__ == '__main__':
    main()
