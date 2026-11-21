"""lapgen.megjelenites.md.eleje — a lap kerete, első rész (S8a): a lap eleje, a Kivonat, a Tartalomjegyzék és a
Jelmagyarázat.

Minden látható mondat a sablontáblából jön (`fej.*`, `kivonat.*`, `tartalom.*`, `jm.*`); a Kivonat a kézi forrás
rése, változatlanul. Minden szakaszszám, szakaszcím és belső horgony a szakaszrendből jön (GK-10): a
Tartalomjegyzék a szakaszrend nézetének minden szakaszát sorolja (a még el nem készülteket is, mert a lap szerkezete
a szakaszrend), a Jelmagyarázat két szakaszhivatkozása (a szótári pontok, a Hatástörténet) a sorszámot kéri le.
"""
from lapgen import konfig
from lapgen.megjelenites.md import keret as K
from lapgen.megjelenites.md.iro import horgony_jel
from lapgen.szakaszok import KRITERIUM_HORGONY
from lapgen.szoveg import cim_horgony, prov

FEJ, KIVONAT, TARTALOM, JELMAGYARAZAT = 'fej', 'kivonat', 'tartalom', 'jelmagyarazat'
SZOCIKKEK, HATASTORTENET = 'szocikkek', 'hatastortenet'
NEM_LISTAZOTT = (FEJ, TARTALOM)   # a Tartalomjegyzék önmagát és a lap elejét nem sorolja
SZOTARI_PONTOK = 'jm.szotari_pontok'
HATAS_KULCSOK = ('jm.t10',)       # a Hatástörténet sorszámát kérő sor(ok)

# A Jelmagyarázat törzsének sorai a sablontábla kulcsaival, sorrendben; az üres karakterlánc üres sor.
TORZS = (
    'jm.t01',
    'jm.t02',
    'jm.t03',
    'jm.t04',
    'jm.t05',
    '',
    'jm.t06',
    'jm.t07',
    'jm.t08',
    'jm.t09',
    'jm.t10',
    'jm.t11',
    '',
    'jm.t12',
    'jm.t13',
    'jm.t14',
    '',
    'jm.t15',
    'jm.t16',
    'jm.t17',
    'jm.t18',
    'jm.t19',
    'jm.t20',
    'jm.t21',
    'jm.t22',
    '',
    'jm.t23',
    'jm.t24',
    'jm.t25',
    '',
    'jm.szotari_pontok',
    '',
    'jm.t26',
    'jm.t27',
    '',
    'jm.t28',
    'jm.t29',
    'jm.t30',
    '',
    'jm.t31',
    'jm.t32',
    'jm.t33',
    'jm.t34',
    '',
    'jm.t35',
    'jm.t36',
)


def megjelenit_fej(iro, m, keret, forrasok):
    ny = keret.ny
    iro.sor(prov('GENERÁLT: {} | rések: {}', konfig.GENERATOR_JELOLO, m.forras_study))
    iro.ures()
    iro.cimsor(1, ny.s('fej.cim', motivum=keret.motivum, cim=m.cim))
    iro.ures()
    if m.meghatarozas is not None and m.azonossag is not None:
        motivum = ny.s('fej.motivum', megh=m.meghatarozas, azon=ny.nev('azonossag', m.azonossag))
    elif m.meghatarozas is not None:
        motivum = ny.s('fej.motivum.megh', megh=m.meghatarozas)
    elif m.azonossag is not None:
        motivum = ny.s('fej.motivum.azon', azon=ny.nev('azonossag', m.azonossag))
    else:
        motivum = ny.s('fej.motivum.cim', cim=m.cim)
    iro.sor(motivum)
    iro.ures()
    # a kritérium egyetlen teljes helye a lap eleje; a horgonyára hivatkozik az 1.1 és a többi szakasz (DT872)
    iro.sor(horgony_jel(KRITERIUM_HORGONY), ny.s('fej.hatar', cim=ny.s('fej.hatar.cim'), kriterium=m.kriterium))
    iro.ures()
    iro.sor(ny.s('fej.tagabb', fol=m.folerendelt))
    iro.ures()
    iro.sor(ny.s('fej.kolofon', horgony=cim_horgony(ny.s('cim.kolofon'))))
    iro.ures()


def megjelenit_kivonat(iro, m, keret, forrasok):
    ny = keret.ny
    iro.cimsor(2, ny.s('cim.kivonat'))
    iro.ures()
    K.olvasoi_bekezdes(iro, ny.s('kivonat.olvasoi'))
    for sor in m.sorok:
        if sor is None:
            iro.ures()
        else:
            iro.sor(sor)
    iro.ures()


def _cim(keret, leiro):
    if leiro.szamozott:
        return K.szamozott_cim(keret, leiro.azonosito)
    return keret.ny.s(keret.rend.cim_kulcs(leiro.azonosito))


def tartalom_elemek(keret):
    """A Tartalomjegyzék szakaszai a szakaszrendből: (cím, horgony) párok."""
    ki = []
    for leiro in keret.rend.mind():
        if leiro.nezet != konfig.NEZET_TUDOMANYOS or leiro.azonosito in NEM_LISTAZOTT or leiro.alresz:
            continue
        cim = _cim(keret, leiro)
        ki.append((cim, cim_horgony(cim)))
    return ki


def megjelenit_tartalom(iro, m, keret, forrasok):
    ny = keret.ny
    iro.cimsor(2, ny.s('cim.tartalom'))
    iro.ures()
    K.blokk_nyit(iro, keret, TARTALOM, forrasok)
    K.olvasoi_bekezdes(iro, ny.s('tartalom.olvasoi'))
    elemek = tartalom_elemek(keret)
    iro.sor(ny.s('tartalom.hatokor', n=len(elemek)))
    iro.ures()
    for cim, horgony in elemek:
        iro.sor(ny.s('tartalom.elem', cim=cim, horgony=horgony))
    iro.ures()
    K.blokk_zar(iro, keret, TARTALOM)


def _szotari_pontok(keret):
    """A 4. szakasz pontrendszerének magyarázata: a szavankénti pontok (4.1–4.10) és a motívum egészére vonatkozók
    (4.11–4.14); a 4.11 a Hatástörténet szakaszára mutat (a régi `szotari_pontok_jelmagyarazat`)."""
    ny, szakasz = keret.ny, keret.rend.sorszam(SZOCIKKEK)
    pontok = []
    for n in range(konfig.PONT_ALAPJELENTES, konfig.PONT_PARHUZAM + 1):
        nev = ny.nev('szotari_pont_mondatkozi', str(n))
        if n == konfig.PONT_VISSZHANG:
            pontok.append(ny.s('jm.szotari_pont.visszhang', szakasz=szakasz, pont=n, nev=nev,
                               hatas=keret.rend.sorszam(HATASTORTENET)))
        else:
            pontok.append(ny.s('jm.szotari_pont', szakasz=szakasz, pont=n, nev=nev))
    return ny.s(SZOTARI_PONTOK, cim=K.szamozott_cim(keret, SZOCIKKEK), pontok=pontok, szakasz=szakasz,
                elso=konfig.PONT_ALAPJELENTES, utolso_szo=konfig.PONT_KIEJTES, elso_kozos=konfig.PONT_VISSZHANG,
                utolso=konfig.PONT_PARHUZAM)


def megjelenit_jelmagyarazat(iro, m, keret, forrasok):
    ny = keret.ny
    iro.cimsor(2, ny.s('cim.jelmagyarazat'))
    iro.ures()
    K.blokk_nyit(iro, keret, JELMAGYARAZAT, forrasok)
    K.olvasoi_bekezdes(iro, ny.s('jm.olvasoi'))
    iro.sor(ny.s('jm.hatokor'))
    iro.ures()
    for kulcs in TORZS:
        if not kulcs:
            iro.ures()
        elif kulcs == SZOTARI_PONTOK:
            iro.sor(_szotari_pontok(keret))
        elif kulcs in HATAS_KULCSOK:
            iro.sor(ny.s(kulcs, hatas=keret.rend.sorszam(HATASTORTENET)))
        else:
            iro.sor(ny.s(kulcs))
    iro.ures()
    K.blokk_zar(iro, keret, JELMAGYARAZAT)
