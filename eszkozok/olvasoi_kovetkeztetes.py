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


def kizart(n_vizsgalt, elutasitva, nyitott, okok, forrasok, n_motivum):
    """`okok`: [(ok, szám)] csökkenő sorrendben (az „egyéb” nélkül); `forrasok`: [(forrás, szám)]."""
    if not n_vizsgalt:
        return None
    lelet = '%d helyet vizsgáltunk meg jelöltként; elutasítva: %d' % (n_vizsgalt, elutasitva)
    lelet += ', döntésre vár: %d.' % nyitott if nyitott else '.'
    if okok:
        lelet += ' A leggyakoribb ok: „%s” (%d)' % okok[0]
        lelet += ', utána „%s” (%d).' % okok[1] if len(okok) > 1 else '.'
    if forrasok:
        lelet += ' A jelöltek forrása: %s.' % _szamlista(sorted(forrasok, key=lambda x: -x[1]))
    kov = []
    if n_motivum:
        kov.append('%s helyet vizsgáltunk, mint ahány a motívumhoz tartozik (%d, illetve %d)'
                   % (_szorzo(n_vizsgalt / n_motivum), n_vizsgalt, n_motivum))
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

def lxx(n, egyezo, eltero, hianyzik, egyeb, gorog_nev):
    """`gorog_nev`: a motívum görög szava névelővel, kiejtéssel („az epikaleó”), vagy ''."""
    if not n:
        return None
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

def minosites(parok, erintett, n, osszes=None):
    if not n:
        return None
    if not parok:
        return ('A hagyományos gyűjtemények utalásai közül egy sem köti össze a motívum két saját helyét. %s a motívumnak '
                'nincs független külső megerősítése.' % KOVETKEZTETES)
    lelet = ('%s %d a motívum két saját helyét köti össze, ez %d helyet érint a %d-ból.'
             % ('A %d utalásból' % osszes if osszes else 'Az utalások közül', parok, erintett, n))
    p = szazalek(erintett, n)
    fokozat = 'erős' if erintett / n >= 0.67 else 'közepes' if erintett / n >= 0.34 else 'gyenge'
    resz = 'a fele (%d%%)' % p if 45 <= p <= 55 else 'a %d%%-a' % p
    return ('%s %s a motívum helyeinek %s két független gyűjteményben is összetartozik, ez %s külső megerősítés.'
            % (lelet, KOVETKEZTETES, resz, fokozat))


# --- 5. Kapcsolatok ---

def kapcsolatok(n, csomopont, tipusok, magas):
    """`tipusok`: [(típus, szám)] csökkenő sorrendben; `magas`: a magas bizonyosságú sorok száma."""
    if not n:
        return None
    lelet = '%d kapcsolat %d helyet köt össze: %s; %d magas' % (
        n, csomopont, ', '.join('%d %s' % (m, t.lower()) for t, m in tipusok), magas)
    lelet += ', %d alacsonyabb bizonyosságú.' % (n - magas) if n - magas else ' bizonyosságú.'
    fo_t, fo_n = tipusok[0]
    if fo_t.lower() == 'beteljesedés' and fo_n / n >= 0.5:
        szerk = 'a motívum helyei ószövetségi ígéretből újszövetségi beteljesedésbe tartó láncot alkotnak'
    elif fo_n / n >= 0.67:
        szerk = 'a motívum helyei túlnyomórészt %s jellegűek' % fo_t.lower()
        if fo_t.lower() == 'párhuzam':
            szerk = 'a motívum helyei túlnyomórészt párhuzamos előfordulások, nem egymásra épülő lánc'
    else:
        szerk = 'a motívum helyei között többféle kapcsolat van, egyik sem uralkodó'
    biz = {'szinte': 'a kapcsolatok szinte mind biztosak', 'tobbseg': 'a kapcsolatok többsége biztos',
           'fele': 'a kapcsolatok fele-kétharmada biztos', 'keves': 'a kapcsolatok többsége bizonytalan'}[fok(magas / n)]
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

def sece(szo_nev, n_megfelelo, sajat_nevek, tars=''):
    """`szo_nev`: a szó névelővel („az epikaleó”); `sajat_nevek`: a megfelelők közül a motívum saját szavai (névelővel);
    `tars`: a szókapcsolat másik szava (névelővel), amely párosul a motívum másik nyelvű szavával (pl. a sém mellett
    a kárá), vagy ''."""
    if not n_megfelelo:
        return None
    lelet = 'A kétnyelvű szótár (SECE) %s szónak %d megfelelőjét adja a másik bibliai nyelven' % (szo_nev, n_megfelelo)
    if sajat_nevek:
        return ('%s; köztük van a motívum saját szava, %s. %s a szótár is megerősíti, hogy a két szó egymás párja.'
                % (lelet, _lista(sajat_nevek), KOVETKEZTETES))
    if tars:
        return ('%s; a motívum másik nyelvű szava nincs köztük. %s a szókapcsolatban nem ez a szó, hanem %s felel meg a '
                'másik nyelv szavának.' % (lelet, KOVETKEZTETES, tars))
    return ('%s; a motívum másik nyelvű szava nincs köztük. %s a szótár ezt a párt nem ismeri; a kapcsolatot csak a '
            'fordítás (LXX) mutatja.' % (lelet, KOVETKEZTETES))


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
