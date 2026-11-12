"""Az olvasói („Mit mutat ez a rész?”) szövegek: előbb a lelet számokkal, utána a rögzített szabály szerinti következtetés.

A felhasználó, 2026-10-30: „mindig vanjuk le a következtetést a találtakból . a magyarázó szöveg az adatokból
induljon.”; a tervezetre: „Mehet”. A függvények tiszták: számokat és neveket kapnak, szöveget adnak; motívumra szabott
értelmezés nincs bennük (CLAUDE.md 3. szabály), a következtetés a küszöbökből jön. A számra és az igehelyre toldalékot
nem tesznek („4 helyen”, „például: 2Móz 33:19”), mert a toldalék a szám kiolvasásától függ.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KOVETKEZTETES = '**Következtetés:**'

# Arány-küszöbök (alsó határ, fokozat): a 13. szerep (OLVASOI_13_KUSZOB) mintájára, minden aránynál ugyanaz.
FOKOK = ((0.90, 'szinte'), (0.67, 'tobbseg'), (0.50, 'fele'), (0.0, 'keves'))


def fok(arany):
    return next(f for k, f in FOKOK if arany >= k)


def szazalek(a, b):
    return round(100 * a / b) if b else 0


def _lista(xs):
    return xs[0] if len(xs) == 1 else '%s és %s' % (', '.join(xs[:-1]), xs[-1])


def _szamlista(parok):
    """[(címke, szám)] -> „1Móz 5, Zsolt 5” (a nulla tagok nélkül)."""
    return ', '.join('%s %d' % (c, n) for c, n in parok if n)


# --- 1. Előfordulások ---

SULYPONT_KUSZOB = 0.40   # F1 (szerkesztői döntés, 2026-11-09: „jó így”): ennyi hely egy könyvben = súlypont
SZOVETSEG_KUSZOB = 0.20  # ennél kisebb arányú szövetség: „főként ószövetségi / újszövetségi”


def elofordulasok_uj(n, osz, usz, konyvek, top_konyvek, magas, konyvnev=None):
    """F182 (A03; F1, K41): az új szerkezetű lap összegző mondata — a súlypont (egy könyvben a helyek legalább 40%-a), a
    szövetség-arány (20% alatt „főként”), a megbízhatóság csak ha nem egyértelmű; a „mindkét szövetség” fordulat nélkül.
    `konyvnev`: a könyv teljes magyar neve a rövidítésből (pl. „1Móz” → „Mózes első könyve”)."""
    if not n:
        return None
    lelet = 'A motívum %d igehelyen fordul elő, %d bibliai könyvben' % (n, konyvek)
    resz = ', '.join('%d %s' % (m, c) for c, m in (('ószövetségi', osz), ('újszövetségi', usz)) if m)
    lelet += ' (%s hely)' % resz if resz else ''
    lelet += '. %d hely azonosítása magas megbízhatóságú' % magas
    if n - magas:
        lelet += ', %d alacsonyabb' % (n - magas)
    lelet += '.'
    kov = []
    if top_konyvek and top_konyvek[0][1] / n >= SULYPONT_KUSZOB:
        k, db = top_konyvek[0]
        nev = (konyvnev or (lambda x: x))(k)
        kov.append('a motívum súlypontja %s (%d helyből %d)' % (nev, n, db))
    if usz and osz and usz / n < SZOVETSEG_KUSZOB:
        kov.append('főként ószövetségi; az Újszövetségben %d hely' % usz)
    elif usz and osz and osz / n < SZOVETSEG_KUSZOB:
        kov.append('főként újszövetségi; az Ószövetségben %d hely' % osz)
    elif usz and osz:
        kov.append('az Ószövetségben %d, az Újszövetségben %d hely' % (osz, usz))
    else:
        kov.append('csak az Ószövetségben' if osz else 'csak az Újszövetségben')
    if fok(magas / n) in ('fele', 'keves'):
        kov.append('sok a bizonytalan azonosítás')
    return '%s %s %s.' % (lelet, KOVETKEZTETES, '; '.join(kov))


def elofordulasok(n, osz, usz, konyvek, top_konyvek, magas):
    """`konyvek`: a könyvek száma; `top_konyvek`: [(könyv, szám)] csökkenő sorrendben; `magas`: a magas megbízhatóságú
    helyek száma."""
    if not n:
        return None
    lelet = 'A motívum %d igehelyen fordul elő, %d bibliai könyvben' % (n, konyvek)
    resz = ', '.join('%d %s' % (m, c) for c, m in (('ószövetségi', osz), ('újszövetségi', usz)) if m)
    lelet += ' (%s hely)' % resz if resz else ''
    if top_konyvek and top_konyvek[0][1] > 1:
        csucs = [k for k, m in top_konyvek if m == top_konyvek[0][1]]
        lelet += '; a legtöbb hely: %s (%d%s)' % (_lista(csucs), top_konyvek[0][1],
                                                   '-%d' % top_konyvek[0][1] if len(csucs) > 1 else '')
    lelet += '. %d hely azonosítása magas megbízhatóságú' % magas
    if n - magas:
        lelet += ', %d alacsonyabb' % (n - magas)
    lelet += '.'
    szov = ('mindkét szövetségben' if osz and usz else 'csak az Ószövetségben' if osz else 'csak az Újszövetségben')
    kiterj = ('a Biblia sok könyvében' if konyvek >= 10 else 'néhány könyvben' if konyvek >= 3
              else 'egy-két könyvre szorítkozva')
    biz = {'szinte': 'a helyek szinte mind biztosan azonosítottak',
           'tobbseg': 'a helyek többsége biztosan azonosított',
           'fele': 'sok a bizonytalan azonosítás', 'keves': 'sok a bizonytalan azonosítás'}[fok(magas / n)]
    return '%s %s a motívum %s, %s fordul elő, és %s.' % (lelet, KOVETKEZTETES, kiterj, szov, biz)


# --- 1/b. Kizárt és vizsgált helyek ---

HATAR_KUSZOB = 0.40
_SZOR = {2: 'kétszer', 3: 'háromszor', 4: 'négyszer', 5: 'ötször', 6: 'hatszor', 7: 'hétszer', 8: 'nyolcszor',
         9: 'kilencszer', 10: 'tízszer'}


def _szorzo(x):
    """A vizsgált / motívumhely arány szóval: „majdnem háromszor annyi”, „több mint kétszer annyi”, „másfélszer annyi”,
    „körülbelül annyi”, „kevesebb”."""
    if x < 0.9:
        return 'kevesebb'
    if x < 1.25:
        return 'körülbelül annyi'
    if x < 1.75:
        return 'másfélszer annyi'
    r = round(x)
    nev = _SZOR.get(r, '%d-szor' % r)
    if abs(x - r) < 0.1:
        return '%s annyi' % nev
    return ('majdnem %s annyi' % nev) if r > x else ('több mint %s annyi' % nev)


def _ezres(n):
    """Ezres tagolás nem törő szóközzel (1 728)."""
    return '{:,}'.format(n).replace(',', '\u00a0')


def kizart_uj(egyenkent, csoport_vers, csoport_sor, elutasitva, nyitott, okok, forrasok, n_motivum):
    """F182 (A07; B07, K12): a `kizart` mondata harmadik személyben (a „vizsgáltunk”, „kerestük”, „döntöttünk” nélkül);
    a számok és a szabály ugyanazok."""
    sz = kizart(egyenkent, csoport_vers, csoport_sor, elutasitva, nyitott, okok, forrasok, n_motivum)
    if not sz:
        return sz
    csere = (
        (' verset vizsgáltunk meg: a motívum szavait a teljes Ó- és Újszövetségben kerestük, és a kereszthivatkozások '
         'ajánlásait is megnéztük.', ' vers került vizsgálat alá: a motívum szavainak keresése a teljes Ó- és Újszövetségre '
         'kiterjedt, és a kereszthivatkozások ajánlásaira is.'),
        (' verset vizsgáltunk meg: a motívum szavait a teljes Ó- és Újszövetségben kerestük.',
         ' vers került vizsgálat alá: a motívum szavainak keresése a teljes Ó- és Újszövetségre kiterjedt.'),
        (' verset vizsgáltunk meg, jelöltként.', ' vers került vizsgálat alá, jelöltként.'),
        (' versről egyenként döntöttünk, ', ' versről egyenként született döntés, '),
        (' verset vizsgáltunk, mint ahány hely a motívumhoz tartozik', ' vers került vizsgálat alá, mint ahány hely a '
         'motívumhoz tartozik'),
    )
    for a, b in csere:
        sz = sz.replace(a, b)
    return sz


def kizart(egyenkent, csoport_vers, csoport_sor, elutasitva, nyitott, okok, forrasok, n_motivum):
    """Versszámok (F123.TUD1B: a vers, nem a táblasor): `egyenkent` az egyenként vizsgált versek, `csoport_vers` az
    összesítő sorok (`csoport_sor` darab) által csoportosan vizsgált versek; `elutasitva`, `nyitott` versben. `okok`:
    [(ok, versszám)] csökkenő sorrendben (az „egyéb” nélkül); `forrasok`: [(forrás, versszám)]."""
    n_vizsgalt = egyenkent + csoport_vers
    if not n_vizsgalt:
        return None
    # F123.HAMART3 (a felhasználó átnézése): a mondat nem tautologikus („vizsgáltunk N … elutasítva N”), és megmondja,
    # hogy a vizsgált versek a motívum helyein túl vannak
    elej = ('A motívum %s helyén túl további %s verset vizsgáltunk meg' % (_ezres(n_motivum), _ezres(n_vizsgalt))
            if n_motivum else '%s verset vizsgáltunk meg' % _ezres(n_vizsgalt))
    if csoport_vers:
        # F123.HAMART3 javítókör: a kereszthivatkozásokról csak akkor szól, ha a jelöltek között van ilyen forrás
        ajanlas = any(('TSK' in f or 'Károli-kereszthivatkozás' in f) and n for f, n in (forrasok or []))
        elej += (': a motívum szavait a teljes Ó- és Újszövetségben kerestük%s.'
                 % (', és a kereszthivatkozások ajánlásait is megnéztük' if ajanlas else ''))
    else:
        elej += ', jelöltként.'
    if nyitott:
        dont = ' Ezek közül %s nem tartozik a motívumhoz, %s döntésre vár.' % (_ezres(elutasitva), _ezres(nyitott))
    else:
        dont = ' Egyik sem tartozik a motívumhoz'
    if csoport_vers:
        dont += ('%s %s versről egyenként döntöttünk, %s versről közös ok alapján, csoportosan.'
                 % (':' if not nyitott else ' Közülük', _ezres(egyenkent), _ezres(csoport_vers)))
    elif not nyitott:
        dont += '.'
    lelet = elej + dont
    if okok:
        lelet += ' A leggyakoribb ok: „%s” (%d vers)' % okok[0]
        lelet += ', utána „%s” (%d vers).' % okok[1] if len(okok) > 1 else '.'
    if forrasok:
        lelet += ' A jelöltek forrása (vers): %s.' % _szamlista(sorted(forrasok, key=lambda x: -x[1]))
    kov = []
    if n_motivum:
        x = n_vizsgalt / n_motivum
        if round(x) > 10:   # a „…-szor annyi” toldaléka a szám kiejtésétől függ: nagy aránynál az átlag mondja ki
            kov.append('a motívum minden helyére átlagosan %d vizsgált vers jut (%d vizsgált vers, %d motívumhely)'
                       % (round(x), n_vizsgalt, n_motivum))
        else:
            kov.append('%s verset vizsgáltunk, mint ahány hely a motívumhoz tartozik (%d, illetve %d)'
                       % (_szorzo(x), n_vizsgalt, n_motivum))
    if okok and elutasitva:
        if okok[0][1] / elutasitva >= HATAR_KUSZOB:
            kov.append('a határt leginkább ez az ok húzza meg: „%s”' % okok[0][0])
        else:
            kov.append('a határt több ok együtt húzza meg')
    if not kov:
        return lelet
    k = '. '.join(s if i == 0 else s[0].upper() + s[1:] for i, s in enumerate(kov))
    return '%s %s %s.' % (lelet, KOVETKEZTETES, k)


# --- A motívum kulcsszavai ---

def kulcsszavak(kombok):
    """`kombok`: [(nyelv: 'héber'|'görög', [szónév névelővel], helyek száma)]."""
    if not kombok:
        return None
    kombok = sorted(kombok, key=lambda k: k[0] != 'héber')
    reszek = []
    for ny, nevek, n in kombok:
        reszek.append('%s %s%s (%d hely)' % ('héberül' if ny == 'héber' else 'görögül', _lista(nevek),
                                             ' együtt' if len(nevek) > 1 else '', n))
    egyszavas = all(len(nevek) == 1 for _ny, nevek, _n in kombok)
    if egyszavas:
        lelet = 'A motívumot %s hordozza: %s.' % ('nyelvenként egy szó' if len(kombok) > 1 else 'egy szó',
                                                 ', '.join(reszek))
    else:
        lelet = 'A motívumot %s hordozza: %s.' % ('%d szókapcsolat' % len(kombok) if len(kombok) > 1 else
                                                 'egy szókapcsolat', '; '.join(reszek))
    if egyszavas:
        return '%s %s %s egyetlen szó jelzi a motívumot.' % (
            lelet, KOVETKEZTETES, 'mindkét szövetségben' if len(kombok) > 1 else 'a motívum helyein')
    kov = []
    for ny, nevek, _n in kombok:
        szov = 'az Ószövetségben' if ny == 'héber' else 'az Újszövetségben'
        kov.append('%s %s' % (szov, 'két szó együttes jelenléte kell a motívumhoz' if len(nevek) == 2 else
                               '%d szó együttes jelenléte kell a motívumhoz' % len(nevek) if len(nevek) > 2 else
                               'egy szó elég'))
    return '%s %s %s.' % (lelet, KOVETKEZTETES, ', '.join(kov))


# --- 3. LXX-fordítói döntések, 6. szerep ---

def lxx(n, egyezo, eltero, hianyzik, egyeb, gorog_nev, nincs_gorog=False):
    """`gorog_nev`: a motívum görög szava névelővel, kiejtéssel („az epikaleó”), vagy ''. `nincs_gorog`: a motívumnak
    nincs görög (újszövetségi) szava (F12, TEREMT-002): nincs mivel egyezzen, a mondat ezt mondja ki."""
    if not n:
        return None
    if nincs_gorog:
        tobbi = []
        if eltero:
            tobbi.append('%d helyen saját görög szóval adja vissza' % eltero)
        if hianyzik:
            tobbi.append('%d helyen a görögből hiányzik' % hianyzik)
        if egyeb:
            tobbi.append('%d helyen az azonosítás függőben' % egyeb)
        lelet = ('A motívumnak nincs görög szava, ezért az újszövetségi szóval való egyezés nem mérhető; a görög '
                 'fordítás (Septuaginta) a motívum %d ószövetségi helyéből %s.' % (n, ', '.join(tobbi) or 'egyiket sem adja vissza'))
        return ('%s %s a motívum a görög Ószövetségen át nyelvileg nem kapcsolódik az Újszövetséghez; a görög szöveg azt '
                'mutatja, hogyan adta vissza a fordító a héber szavakat (3. LXX-fordítói döntések).' % (lelet, KOVETKEZTETES))
    szo = ' (%s)' % gorog_nev.split(' ', 1)[1] if gorog_nev else ''
    lelet = ('A motívum %d ószövetségi helyéből %d helyen a görög fordítás (Septuaginta) ugyanazt a szót használja%s, '
             'mint az Újszövetség' % (n, egyezo, szo))
    tobbi = []
    if eltero:
        tobbi.append('%d helyen mást' % eltero)
    if hianyzik:
        tobbi.append('%d helyen a görögből hiányzik' % hianyzik)
    if egyeb:
        tobbi.append('%d helyen az azonosítás függőben' % egyeb)
    lelet += ('; ' + ', '.join(tobbi) if tobbi else '') + '.'
    f = fok(egyezo / n)
    p = szazalek(egyezo, n)
    kov = {'szinte': 'a görög Ószövetség szinte mindenütt (%d%%) ugyanazzal a szóval adja vissza a motívumot, ezért az '
                     'újszövetségi helyek nyelvileg is közvetlenül visszakapcsolódnak az ószövetségiekhez' % p,
           'tobbseg': 'a görög Ószövetség a legtöbb helyen (%d%%) ugyanazzal a szóval adja vissza a motívumot, ezért az '
                      'újszövetségi helyek nyelvileg is közvetlenül visszakapcsolódnak az ószövetségiekhez' % p,
           'fele': 'a görög Ószövetség a helyek felén-kétharmadán (%d%%) adja vissza ugyanazzal a szóval a motívumot; a '
                   'nyelvi kapcsolat részleges' % p,
           'keves': 'a görög Ószövetség csak a helyek %d%%-án használja ugyanazt a szót: a kapcsolat nem nyelvi, csak '
                    'tartalmi' % p}[f]
    return '%s %s %s.' % (lelet, KOVETKEZTETES, kov)


def lxx_uj(n, egyezo, eltero, hianyzik, egyeb):
    """F182 (A20, K20): az 5. szakasz és a 4.6 összegzése versben mérve (a tábla soronként egy Károli-vers); a
    toldalék a „vers” szón áll, nem a számon."""
    if not n:
        return None
    lelet = ('A motívum ószövetségi helyei %d versre terjednek; ezek közül %d versben a görög fordítás (Septuaginta) '
             'ugyanazt a szót használja, mint az Újszövetség' % (n, egyezo))
    tobbi = []
    if eltero:
        tobbi.append('%d versben mást' % eltero)
    if hianyzik:
        tobbi.append('%d versben a görögből hiányzik' % hianyzik)
    if egyeb:
        tobbi.append('%d versben a megfelelő nincs megállapítva' % egyeb)
    lelet += ('; ' + ', '.join(tobbi) if tobbi else '') + '.'
    p = szazalek(egyezo, n)
    kov = {'szinte': 'a görög Ószövetség szinte minden versben (%d%%) ugyanazzal a szóval adja vissza a motívumot, ezért '
                     'az újszövetségi helyek nyelvileg is közvetlenül visszakapcsolódnak az ószövetségiekhez' % p,
           'tobbseg': 'a görög Ószövetség a versek többségében (%d%%) ugyanazzal a szóval adja vissza a motívumot, ezért '
                      'az újszövetségi helyek nyelvileg is visszakapcsolódnak az ószövetségiekhez' % p,
           'fele': 'a görög Ószövetség a versek felén-kétharmadán (%d%%) adja vissza ugyanazzal a szóval a motívumot; a '
                   'nyelvi kapcsolat részleges' % p,
           'keves': 'a görög Ószövetség csak a versek %d%%-ában használja ugyanazt a szót: a kapcsolat nem nyelvi, csak '
                    'tartalmi' % p}[fok(egyezo / n)]
    return '%s %s %s.' % (lelet, KOVETKEZTETES, kov)


_SZAMNEV = {1: 'egy', 2: 'két', 3: 'három', 4: 'négy', 5: 'öt', 6: 'hat', 7: 'hét', 8: 'nyolc', 9: 'kilenc', 10: 'tíz'}


def szam_bol(n):
    """A szám -ból/-ből ragja a kiejtett alak utolsó szava szerint (46-ból, 47-ből, 100-ból, 1000-ből)."""
    n = abs(int(n))
    e, t10 = n % 10, (n // 10) % 10
    if e:
        return 'ből' if e in (1, 2, 4, 5, 7, 9) else 'ból'
    if t10:
        return 'ből' if t10 in (1, 4, 5, 7, 9) else 'ból'
    if n and n % 1000 == 0 and n % 1000000:
        return 'ből'
    return 'ból'


def nevelo_szam(n):
    """A számnév előtti névelő: „az” a magánhangzóval kezdődő kiejtés előtt (1, 5, 50–59, 500–599, 1000–1999)."""
    n = abs(int(n))
    return 'az' if n == 1 or str(n)[0] == '5' or 1000 <= n < 2000 else 'a'


def lxx_hid(n, egyezo, szocsalad, eltero, nincs_par, nincs_megall, szamozas, hianyzik, par_nevek):
    """A lektor és a Fable közös véleménye (1–2.): az 5. szakasz és a 4.6 összegzése. A görög Ószövetség és az
    Újszövetség közti szóhíd azokon a héber szavakon át vezet, amelyeknek a motívumban van újszövetségi párja; a többi
    szónál egyezés eleve nem várható, ott nincs következtetés. A „nincs megállapítva” és a „nem párosítva” külön áll."""
    if not n:
        return None
    ki = ['A motívum ószövetségi helyei %d versre terjednek.' % n]
    par_n = egyezo + szocsalad + eltero
    if par_nevek:
        reszek = []
        for k, sz in ((egyezo, 'ugyanazt a szót használja, mint az Újszövetség'),
                      (szocsalad, 'ugyanannak a szócsaládnak egy másik tagját'), (eltero, 'mást')):
            if k:
                reszek.append('%d versben %s' % (k, sz))
        ki.append('A görög Ószövetség és az Újszövetség közti szóhíd %s szón át vezet, %s szaván: ezek %d megállapított '
                  'versében a görög fordítás %s.' % (_SZAMNEV.get(len(par_nevek), str(len(par_nevek))),
                                                     _lista(par_nevek), par_n, ', '.join(reszek) or 'egyikben sem áll'))
    if nincs_par and par_nevek:
        ki.append('A többi szónak a motívumban nincs újszövetségi párja (%d vers), ott egyezés nem várható.' % nincs_par)
    elif nincs_par:
        ki.append('A motívum héber szavainak a motívumban nincs újszövetségi párja (%d vers), ezért egyezés nem várható.'
                  % nincs_par)
    tobbi = []
    if nincs_megall:
        tobbi.append('%d versben a megfelelő nincs megállapítva' % nincs_megall)
    if szamozas:
        tobbi.append('%d versben a versszámozás eltérése miatt nincs párosítva' % szamozas)
    if hianyzik:
        tobbi.append('%d versben a szó a görögből hiányzik' % hianyzik)
    if tobbi:
        ki.append(_lista(tobbi)[0].upper() + _lista(tobbi)[1:] + '.')
    if par_n:
        arany = (egyezo + szocsalad) / par_n
        jelzo = 'erős' if arany >= 0.67 else 'részleges' if arany >= 0.34 else 'gyenge'
        ki.append('%s a nyelvi híd %s szón át vezet, és ott %s: szócsalád szerint %d/%d vers.'
                  % (KOVETKEZTETES, _SZAMNEV.get(len(par_nevek), str(len(par_nevek))), jelzo, egyezo + szocsalad, par_n))
    return ' '.join(ki)


def lxx_szo_uj(nev, n, egyezo, szocsalad, eltero, nincs_par, hianyzik, egyeb, szamozas, van_par):
    """A lektor és a Fable közös véleménye (1.): a 4.6 szavankénti mondata. Újszövetségi pár nélküli szónál a lelet
    kimondja, hogy egyezés nem várható, és következtetés nincs; párral bíró szónál a szócsaládot is számolja."""
    if not n:
        return None
    nev = nev[0].upper() + nev[1:]
    if not van_par:
        reszek = ['%d versben más görög szó áll' % (nincs_par + eltero)] if nincs_par + eltero else []
        for k, sz in ((hianyzik, 'a szó a görögből hiányzik'), (egyeb, 'a megfelelő nincs megállapítva'),
                      (szamozas, 'a versszámozás eltérése miatt nincs párosítva')):
            if k:
                reszek.append('%d versben %s' % (k, sz))
        return ('%s a motívum %d ószövetségi versében áll; a szónak a motívumban nincs újszövetségi párja, ezért egyezés '
                'nem várható. A görög fordításban %s.' % (nev, n, '; '.join(reszek) if reszek else 'egyikről sincs adat'))
    reszek = []
    for k, sz in ((egyezo, 'ugyanaz a görög szó áll, mint az Újszövetségben'),
                  (szocsalad, 'ugyanannak a szócsaládnak egy másik tagja áll'), (eltero, 'más görög szó áll'),
                  (hianyzik, 'a szó a görögből hiányzik'), (egyeb, 'a megfelelő nincs megállapítva'),
                  (szamozas, 'a versszámozás eltérése miatt nincs párosítva')):
        if k:
            reszek.append('%d versben %s' % (k, sz))
    lelet = '%s a motívum %d ószövetségi versében áll; a görög fordításban %s.' % (
        nev, n, '; '.join(reszek) if reszek else 'egyikről sincs adat')
    if n >= LXX_SZO_MIN and (egyezo + szocsalad) / n >= 0.67:
        return ('%s %s ennél a szónál a görög Ószövetség az újszövetségi szót vagy annak szócsaládját használja '
                '(%d/%d vers).' % (lelet, KOVETKEZTETES, egyezo + szocsalad, n))
    return lelet


LXX_SZO_MIN = 5   # F182 (A13, K10): ennyi vers alatt a szóról nincs következtetés


def lxx_szo(nev, n, egyezo, eltero, hianyzik, egyeb, szamozas=0):
    """F182 (A13; F11, K61): a 4.6 szavankénti mondata — lelet egy teljes mondatban, következtetés csak elég versnél."""
    if not n:
        return None
    reszek = []
    for k, t in ((egyezo, 'ugyanaz a görög szó áll, mint az Újszövetségben'), (eltero, 'más görög szó áll'),
                 (hianyzik, 'a szó a görögből hiányzik'), (egyeb, 'a megfelelő nincs megállapítva'),
                 (szamozas, 'a versszámozás eltérése miatt nincs párosítva')):
        if k:
            reszek.append('%d versben %s' % (k, t))
    lelet = '%s a motívum %d ószövetségi versében áll; a görög fordításban %s.' % (
        nev[0].upper() + nev[1:], n, '; '.join(reszek) if reszek else 'egyikről sincs adat')
    if n < LXX_SZO_MIN:
        return lelet
    if egyezo / n >= 0.67:
        return '%s %s ennél a szónál a görög Ószövetség az újszövetségi szót használja.' % (lelet, KOVETKEZTETES)
    if egyezo / n <= 0.10 and eltero / n >= 0.5:
        return '%s %s ennél a szónál a görög Ószövetség nem az újszövetségi szót használja.' % (lelet, KOVETKEZTETES)
    return lelet


# --- 4. Kereszthivatkozások ---

def kereszthivatkozasok(n, talalt, osszes):
    if not n:
        return None
    if not talalt:
        return ('A motívum %d helyéről a hagyományos gyűjtemények (TSK, Károli) nem mutatnak más bibliai helyre. %s a '
                'motívumot a régi kereszthivatkozások nem kötik más helyekhez.' % (n, KOVETKEZTETES))
    return ('A motívum %d helyéből %d helyről mutat utalás más bibliai helyre a hagyományos gyűjteményekben (TSK, '
            'Károli), összesen %d. %s a helyek %d%%-át a régi kereszthivatkozások is összekötik más helyekkel; hogy ezek '
            'közül melyik mutat a motívum saját helyeire, azt a Minősítés mondja meg.'
            % (n, talalt, osszes, KOVETKEZTETES, szazalek(talalt, n)))


# --- Minősítés ---

def minosites(parok, erintett, n, osszes=None, rag=False):
    if not n:
        return None
    if not parok:
        return ('A hagyományos gyűjtemények utalásai közül egy sem köti össze a motívum két saját helyét. %s a motívumnak '
                'nincs független külső megerősítése.' % KOVETKEZTETES)
    # a lektor és a Fable közös véleménye (5.): `rag` (az új szerkezetű lap) — a rag és a névelő a számhoz igazodik
    lelet = ('%s %d a motívum két saját helyét köti össze, ez %d helyet érint %s.'
             % ('A %d utalásból' % osszes if osszes else 'Az utalások közül', parok, erintett,
                ('%s %d-%s' % (nevelo_szam(n), n, szam_bol(n))) if rag else 'a %d-ból' % n))
    p = szazalek(erintett, n)
    fokozat = 'erős' if erintett / n >= 0.67 else 'közepes' if erintett / n >= 0.34 else 'gyenge'
    resz = 'a fele (%d%%)' % p if 45 <= p <= 55 else 'a %d%%-a' % p
    return ('%s %s a motívum helyeinek %s két független gyűjteményben is összetartozik, ez %s külső megerősítés.'
            % (lelet, KOVETKEZTETES, resz, fokozat))


# --- 5. Kapcsolatok ---

def kapcsolatok(n, csomopont, tipusok, magas, kozepes=None):
    """`tipusok`: [(típus, szám)] csökkenő sorrendben; `magas`: a magas bizonyosságú sorok száma; `kozepes`: a közepes
    bizonyosságúaké (ha megadott, a nem magas sorokat nem nevezi „bizonytalannak”, lap-javit HAMART-001, lektor 17.)."""
    if not n:
        return None
    lelet = '%d kapcsolat %d helyet köt össze: %s; %d magas' % (
        n, csomopont, ', '.join('%d %s' % (m, t.lower()) for t, m in tipusok), magas)
    if kozepes is not None and n - magas:
        alacsony = n - magas - kozepes
        lelet += ', %d közepes%s bizonyosságú.' % (kozepes, (', %d alacsony' % alacsony) if alacsony else '')
    else:
        lelet += ', %d alacsonyabb bizonyosságú.' % (n - magas) if n - magas else ' bizonyosságú.'
    fo_t, fo_n = tipusok[0]
    if fo_t.lower() == 'beteljesedés' and fo_n / n >= 0.5:
        szerk = 'a motívum helyei ószövetségi ígéretből újszövetségi beteljesedésbe tartó láncot alkotnak'
    elif fo_n / n >= 0.67:
        szerk = 'a motívum helyei túlnyomórészt %s jellegűek' % fo_t.lower()
        if fo_t.lower() == 'párhuzam' and kozepes is None:
            szerk = 'a motívum helyei túlnyomórészt párhuzamos előfordulások, nem egymásra épülő lánc'
        elif fo_t.lower() == 'párhuzam':
            # lektor 17. (csak az új szerkezetű lapon, ahol a hívó a közepes számot átadja; a régi lapok szövege
            # változatlan, E28): a „párhuzam” típus nem mond ellent a láncnak
            szerk = ('a motívum helyeit túlnyomórészt párhuzam köti össze: a későbbi hely ugyanazt a szót vagy '
                     'szerkezetet hozza vissza, nem egy korábbi ígéretet teljesít be')
    else:
        szerk = 'a motívum helyei között többféle kapcsolat van, egyik sem uralkodó'
    keves = 'a kapcsolatok többsége bizonytalan'
    if kozepes is not None and 2 * kozepes > n:   # ELLENOR_HAMART_lapjavit 5.: csak ha valóban többség
        keves = 'a kapcsolatok többsége közepes bizonyosságú'
    elif kozepes is not None:
        keves = 'a kapcsolatok kevesebb mint fele magas bizonyosságú'
    biz = {'szinte': 'a kapcsolatok szinte mind biztosak', 'tobbseg': 'a kapcsolatok többsége biztos',
           'fele': 'a kapcsolatok fele-kétharmada biztos', 'keves': keves}[fok(magas / n)]
    return '%s %s %s, és %s.' % (lelet, KOVETKEZTETES, szerk, biz)


# --- 5/b. Kapcsolódó motívumok ---

SZOMSZEDOS = 'szomszédos'


def kapcsolodo(sajat, nyitott):
    """`sajat`: [(másik motívum, típus, bizonyosság)]; `nyitott`: a döntésre váró motívumközi jelöltek száma."""
    if not sajat:
        lelet = 'A motívumnak még nincs rögzített kapcsolata más motívummal'
        lelet += '; %d döntésre vár.' % nyitott if nyitott else '.'
        return lelet
    mot = {}
    for m, _t, _b in sajat:
        mot[m] = mot.get(m, 0) + 1
    tipus = sorted({t for _m, t, _b in sajat})
    lelet = '%d kapcsolat %d másik motívummal (%s), %s' % (
        len(sajat), len(mot), _szamlista(sorted(mot.items())),
        'mind „%s”' % tipus[0] if len(tipus) == 1 else 'típus szerint: %s' % ', '.join(tipus))
    if nyitott:
        lelet += '; további %d döntésre vár' % nyitott
    lelet += '.'
    if tipus == [SZOMSZEDOS]:
        kov = 'a motívum más motívumokhoz eddig csak szövegközelség révén kapcsolódik, tartalmi kapcsolat még nincs igazolva'
    else:
        kov = 'a motívum más motívumokhoz tartalmi kapcsolattal is kötődik'
    return '%s %s %s.' % (lelet, KOVETKEZTETES, kov)


# --- 7. szerep (SECE) ---

def sece(szo_nev, n_megfelelo, sajat_nevek, tars='', nincs_masik=False, lxx_nevek=()):
    """`szo_nev`: a szó névelővel („az epikaleó”); `sajat_nevek`: a megfelelők közül a motívum saját szavai (névelővel);
    `tars`: a szókapcsolat másik szava (névelővel), amely párosul a motívum másik nyelvű szavával (pl. a sém mellett
    a kárá), vagy ''. `nincs_masik` (F12, TEREMT-002): a motívumnak nincs szava a másik nyelven; `lxx_nevek`: a
    megfelelők közül azok (névelővel), amelyekkel a Septuaginta a motívum helyein fordít (`lxx_dontesek.tsv`)."""
    if not n_megfelelo:
        return None
    lelet = 'A kétnyelvű szótár (SECE) %s szónak %d megfelelőjét adja a másik bibliai nyelven' % (szo_nev, n_megfelelo)
    if nincs_masik:
        if lxx_nevek:
            tobb = len(lxx_nevek) > 1
            return ('%s; a motívumnak a másik nyelven nincs saját szava, de a megfelelők között van %s, %s a '
                    'Septuaginta a motívum helyein fordít. %s a szótár ismeri %s, %s a fordítás a szót visszaadja; '
                    'a motívumnak a másik nyelven nincs párja.'
                    % (lelet, _lista(list(lxx_nevek)), 'amelyekkel' if tobb else 'amellyel', KOVETKEZTETES,
                       'azokat a szavakat' if tobb else 'azt a szót', 'amelyekkel' if tobb else 'amellyel'))
        return ('%s; a motívumnak a másik nyelven nincs saját szava. %s a szótár csak a szó lehetséges megfelelőit '
                'mutatja, a motívumnak a másik nyelven nincs párja.' % (lelet, KOVETKEZTETES))
    if sajat_nevek:
        return ('%s; köztük van a motívum saját szava, %s. %s a szótár is megerősíti, hogy a két szó egymás párja.'
                % (lelet, _lista(sajat_nevek), KOVETKEZTETES))
    if tars:
        return ('%s; a motívum másik nyelvű szava nincs köztük. %s a szókapcsolatban nem ez a szó, hanem %s felel meg a '
                'másik nyelv szavának.' % (lelet, KOVETKEZTETES, tars))
    return ('%s; a motívum másik nyelvű szava nincs köztük. %s a szótár ezt a párt nem ismeri; a kapcsolatot csak a '
            'fordítás (LXX) mutatja.' % (lelet, KOVETKEZTETES))


def sece_csoport(nyelv_nev, szavak):
    """F182 (A14; F12, K62): a 4.7 egy mondata. `szavak`: [(szónév írással, megfelelők száma, [a motívum másik nyelvű
    saját szavai írással])]. Következtetés csak ott, ahol a SECE a párt adja; a többi szóról csak a lelet."""
    szavak = [x for x in szavak if x[1]]
    if not szavak:
        return None
    par = [(nev, sj) for nev, _db, sj in szavak if sj]
    nincs = [nev for nev, _db, sj in szavak if not sj]
    if par:
        lelet = ('A kétnyelvű szótár (SECE) a motívum %s szavai közül %s megfelelői között adja a motívum másik nyelvű '
                 'szavát: %s' % (nyelv_nev, _lista([nev for nev, _sj in par]),
                                 '; '.join('%s mellett %s' % (nev, _lista(sj)) for nev, sj in par)))
        lelet += ('; a többi %d szónál a megfelelők között nincs a motívum másik nyelvű szava.' % len(nincs)
                  if nincs else '.')
        return '%s %s a szótár %s; a többi szó párját a fordítás (4.6) mutatja, nem a szótár.' % (
            lelet, KOVETKEZTETES, 'ezt a párt megerősíti' if len(par) == 1 else 'ezeket a párokat megerősíti')
    return ('A kétnyelvű szótár (SECE) a motívum %s szavainál (%s) a megfelelők között nem adja a motívum másik nyelvű '
            'szavát; a párt csak a fordítás (4.6) mutatja.' % (nyelv_nev, _lista(nincs)))


VERSENKENTI_KIS = 2   # F182 (A16; F7, K10): ha minden szó legfeljebb ennyi helyen áll, nincs következtetés


def versenkenti_csoport(nyelv_nev, tesz, szavak, hely_szam):
    """F182 (A16; F7, K64): a 4.9 egy csoportosított mondata. `szavak`: [(szónév írással, helyek, egy jelentésű helyek,
    [a nem egyértelmű helyek igehelye])]; `hely_szam`: a motívum különböző helyeinek száma ezen a nyelven. A kivételek
    igehellyel; kis elemszámnál (minden szó ≤ 2 helyen) következtetés nélkül."""
    szavak = [x for x in szavak if x[1]]
    if not szavak:
        return None
    egy = [nev for nev, n, e, _h in szavak if e == n]
    tobb = [(nev, h) for nev, n, e, h in szavak if e < n]
    if not tobb:
        lelet = 'A %s szavak jelentése a motívum minden %s helyén egyértelmű (%d hely).' % (nyelv_nev, tesz, hely_szam)
    else:
        kiv = _lista(['%s (%s)' % (nev, ', '.join(h)) for nev, h in tobb])
        n_tobb = len({x for _n, h in tobb for x in h})
        if egy:
            lelet = ('A %s szavak közül %s jelentése a helyén egyértelmű; %s helyén a szótár több jelentést enged, ezeknél '
                     'a vers dönt (ez %d hely a motívum %d %s helyéből).'
                     % (nyelv_nev, _lista(egy), kiv, n_tobb, hely_szam, tesz))
        else:
            lelet = ('A %s szavak egyikének jelentése sem egyértelmű a helyén: %s; ezeknél a vers dönt.' % (nyelv_nev, kiv))
    if max(n for _nev, n, _e, _h in szavak) <= VERSENKENTI_KIS:
        return lelet
    ossz_n = sum(n for _nev, n, _e, _h in szavak)
    ossz_egy = sum(e for _nev, _n, e, _h in szavak)
    kov = {'szinte': 'a szavak jelentése a motívum helyein szinte mindenütt egyértelmű',
           'tobbseg': 'a szavak jelentése a motívum helyeinek többségén egyértelmű',
           'fele': 'a szavak jelentése a helyek felén-kétharmadán egyértelmű; a többinél a vers dönt',
           'keves': 'a szavak jelentését a motívum helyeinek többségén a vers dönti el'}[fok(ossz_egy / ossz_n)]
    return '%s %s %s.' % (lelet, KOVETKEZTETES, kov)


# --- 9. szerep (versenkénti jelentés) ---

def versenkenti(szavak):
    """`szavak`: [(szónév névelővel, helyek, egy jelentésű helyek, szövetség: 'ószövetségi'|'újszövetségi')]."""
    szavak = [s for s in szavak if s[1]]
    if not szavak:
        return None
    reszek = []
    for nev, n, egy, tesz in szavak:
        r = 'a motívum %d %s helyéből %d helyen %s egyetlen jelentésben áll' % (n, tesz, egy, nev)
        if n - egy:
            r += ', %d helyen a jelentés nem egyértelmű' % (n - egy)
        reszek.append(r)
    lelet = '; '.join(reszek)
    lelet = lelet[0].upper() + lelet[1:] + '.'
    ossz_n = sum(s[1] for s in szavak)
    ossz_egy = sum(s[2] for s in szavak)
    kov = {'szinte': 'a szó jelentése a motívum helyein szinte mindenütt egyértelmű',
           'tobbseg': 'a szó jelentése a motívum helyeinek többségén egyértelmű',
           'fele': 'a szó jelentése a helyek felén-kétharmadán egyértelmű; a többinél a versből kell eldönteni',
           'keves': 'a szó jelentése a motívum helyein gyakran nem egyértelmű; a versből kell eldönteni'}[fok(ossz_egy / ossz_n)]
    if len(szavak) > 1:
        kov = kov.replace('a szó jelentése', 'a szavak jelentése')
    return '%s %s %s.' % (lelet, KOVETKEZTETES, kov)
