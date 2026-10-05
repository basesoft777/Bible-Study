"""F58 M2: Macula héber morfológiai kód -> magyar feloldás, kizárólag az
adat/morf_kulcs_heber.tsv táblából (OSHB-jelkulcs, CC BY 4.0).

Szabályok:
- Emlékezetből írt leképezés nincs: a pozíciók sorrendje (`szerkezet` sorok), a
  jelek és megnevezések mind a táblából jönnek.
- Ismeretlen vagy a nyelven nem értelmezhető jel: a nyers jel marad, a kimenet
  `hianyzo` mezője és a szövegben a `[?jel]` jelöli; csendes kitöltés nincs.
- A Macula-kód nyelvjelölőt nem hordoz; a törzsbetűk jelentése nyelvenként más.
  Ha a nyelv nem ismert (`nyelv=None`) és a törzsjel mindkét nyelvben szerepel,
  a feloldás kétértelmű (`ketertelmu=True`, mindkét olvasat a szövegben).
  A szó nyelve a `adat/morf_nyelv_aramai.tsv`-ből jön (`nyelv_szohoz`).

Használat:
    python eszkozok/morf_feloldas.py Vqp3ms [H|A]
    python eszkozok/morf_feloldas.py --lefedettseg [jelentes.md]
"""
import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# a forrás 4. jegyzete: „Participles ... require no person, though they do take a state”,
# „Generally verbs require no state” -> ez a két pozíció elhagyható; a többi kötelező
OPCIONALIS = ('person', 'state')

KULCS_UT ='adat/morf_kulcs_heber.tsv'
ARAMAI_UT = 'adat/morf_nyelv_aramai.tsv'

# a forrás szófaj-táblázatának oszlopfejei (angol megnevezés) -> pozíció-azonosító a táblában;
# a „type” oszlop értelme szófajonként a tipus_<szófaj> szakasz (igénél az igetipus)
SLOT_POZICIO = {'stem': 'igetorzs', 'person': 'szemely', 'gender': 'nem', 'number': 'szam',
                'state': 'allapot'}


def sorok_olvas(ut):
    fej = None
    for l in open(ut, encoding='utf-8'):
        l = l.rstrip('\n')
        if not l or l.startswith('#'):
            continue
        p = l.split('\t')
        if fej is None:
            fej = p
            continue
        yield dict(zip(fej, p))


class Kulcs:
    def __init__(self, ut=KULCS_UT):
        self.tabla = {}      # (pozicio, nyelv) -> {kod: (forras, hu)}
        self.szerkezet = {}  # szofaj -> [(slot_forras, slot_hu), ...]
        self.szofaj = {}
        self.helykitolto = None
        for r in sorok_olvas(ut):
            poz, nyelv, kod = r['pozicio'], r['nyelv'], r['kod']
            if poz == 'szerkezet':
                if not r['jelentes_forras']:
                    self.szerkezet[kod] = []
                else:
                    f = r['jelentes_forras'].split(' > ')
                    h = r['jelentes_hu'].split(' > ')
                    self.szerkezet[kod] = list(zip(f, h))
            elif poz == 'szofaj':
                self.szofaj[kod] = (r['jelentes_forras'], r['jelentes_hu'])
            elif poz == 'helykitolto':
                self.helykitolto = (kod, r['jelentes_forras'], r['jelentes_hu'])
            else:
                self.tabla.setdefault((poz, nyelv), {})[kod] = (r['jelentes_forras'], r['jelentes_hu'])

    def pozicio_az(self, szofaj, slot_forras):
        if slot_forras == 'type':
            return 'igetipus' if szofaj == 'V' else 'tipus_' + szofaj
        return SLOT_POZICIO[slot_forras]

    def keres(self, pozicio, jel, nyelv):
        """A jel jelentései a pozícióban: [(nyelv, forras, hu)]. nyelv=None: mindkét nyelv."""
        talalat = []
        nyelvek = ['*', 'H', 'A'] if nyelv is None else ['*', nyelv]
        for ny in nyelvek:
            e = self.tabla.get((pozicio, ny), {}).get(jel)
            if e:
                talalat.append((ny, e[0], e[1]))
        return talalat


_KULCS = None


def kulcs():
    global _KULCS
    if _KULCS is None:
        _KULCS = Kulcs()
    return _KULCS


def felold(kod, nyelv=None, k=None):
    """Egy Macula-morfkód feloldása. nyelv: 'H', 'A' vagy None (ismeretlen).

    Visszatér: dict(kod, nyelv, allapot, reszek, hianyzo, ketertelmu, helykitoltos, szoveg).
    allapot: 'teljes' | 'helykitoltovel' (minden jel feloldva, de `x` helykitöltő is van) |
    'ketertelmu' (nyelv nélkül több olvasat; a `ketertelmu` jelző is marad) | 'reszleges' | 'ismeretlen'.
    Az állapot sorrendje: hiányzó jel -> reszleges; helykitöltő -> helykitoltovel; ketertelmu jelző -> ketertelmu;
    egyébként teljes. Ha a nyelv ismeretlen, de egy jel csak az egyik nyelvben
    szerepel (pl. arámi törzs), a szöveg `[csak arámi olvasat]` jelzést kap.
    """
    k = k or kulcs()
    ki = {'kod': kod, 'nyelv': nyelv, 'allapot': 'ismeretlen', 'reszek': [], 'hianyzo': [],
          'ketertelmu': False, 'helykitoltos': False, 'szoveg': ''}
    if not kod:
        ki['hianyzo'].append(('kod', ''))
        ki['szoveg'] = '[?üres kód]'
        return ki
    szof = kod[0]
    if szof not in k.szofaj:
        ki['hianyzo'].append(('szofaj', szof))
        ki['szoveg'] = '[?' + kod + ']'
        return ki
    ki['reszek'].append(('szofaj', szof, [('*',) + k.szofaj[szof]]))
    jelek = list(kod[1:])
    for slot_forras, slot_hu in k.szerkezet.get(szof, []):
        if not jelek:
            break
        poz = k.pozicio_az(szof, slot_forras)
        c = jelek[0]
        talalat = k.keres(poz, c, nyelv)
        if talalat:
            ki['reszek'].append((poz, c, talalat, slot_hu))
            if len({t[2] for t in talalat}) > 1:
                ki['ketertelmu'] = True
            jelek.pop(0)
        elif k.helykitolto and c == k.helykitolto[0]:
            ki['reszek'].append((poz, c, [('*', k.helykitolto[1], k.helykitolto[2])], slot_hu))
            ki['helykitoltos'] = True
            jelek.pop(0)
        elif slot_forras in OPCIONALIS:
            pass  # a forrás 4. jegyzete szerint a személy (igenév) és az állapot (véges ige) nem minden alaknál áll
        else:
            break  # kötelező pozíció jele nem feloldható: a maradék jel hiányként marad (nincs találgatás)
    for c in jelek:
        ki['hianyzo'].append(('nincs_feloldas', c))
    # a kihagyott pozíciókból és a maradékból: ha egy jelet nem tudtunk elhelyezni, az hiány
    # (a kimaradt pozíciók maguk nem hiányok: a jel nem hiányzik, csak a pozíció nem áll)
    reszek_szoveg = []
    for r in ki['reszek']:
        if r[0] == 'szofaj':
            reszek_szoveg.append(r[2][0][2])
        else:
            olvasatok = []
            for ny, forras, hu in r[2]:
                olvasatok.append(hu)
            egyedi = []
            for o in olvasatok:
                if o not in egyedi:
                    egyedi.append(o)
            szoveg = ' / '.join(egyedi)
            if len(r[2]) > 1 and len(egyedi) > 1:
                szoveg += ' [nyelv ismeretlen]'
            elif nyelv is None and len(r[2]) == 1 and r[2][0][0] in ('H', 'A'):
                szoveg += ' [csak ' + {'H': 'héber', 'A': 'arámi'}[r[2][0][0]] + ' olvasat]'
            reszek_szoveg.append(r[3] + ': ' + szoveg)
    for _, c in ki['hianyzo']:
        reszek_szoveg.append('[?' + c + ']')
    ki['szoveg'] = '; '.join(reszek_szoveg)
    if ki['hianyzo']:
        ki['allapot'] = 'reszleges'
    elif ki['helykitoltos']:
        ki['allapot'] = 'helykitoltovel'
    elif ki['ketertelmu']:
        ki['allapot'] = 'ketertelmu'
    else:
        ki['allapot'] = 'teljes'
    return ki


def nyelv_szohoz(aramai):
    """xml_id -> 'A' ha a szó arámi (adat/morf_nyelv_aramai.tsv), különben 'H'."""
    return lambda xml_id: 'A' if xml_id in aramai else 'H'


def aramai_halmaz(ut=ARAMAI_UT):
    return {r['xml_id']: r for r in sorok_olvas(ut)}


def lefedettseg(jelentes_ut=None, kiir=True):
    k = kulcs()
    aramai = aramai_halmaz()
    par = {}      # (kod, nyelv) -> db
    nyelv_nelkul = {}
    elteres = 0
    osszes = 0
    for ut in sorted(glob.glob('konkordancia/Macula_heber_*.tsv')):
        fej = None
        for l in open(ut, encoding='utf-8'):
            l = l.rstrip('\n')
            if not l or l.startswith('#'):
                continue
            p = l.split('\t')
            if fej is None:
                fej = p
                i_id, i_m = p.index('xml_id'), p.index('morf')
                continue
            xid, m = p[i_id], p[i_m]
            ny = 'A' if xid in aramai else 'H'
            if xid in aramai and aramai[xid]['morf'] != m:
                elteres += 1
            par[(m, ny)] = par.get((m, ny), 0) + 1
            nyelv_nelkul[m] = nyelv_nelkul.get(m, 0) + 1
            osszes += 1
    kodok = {m for m, _ in par}
    # 1. (kód, nyelv) párok a szó tényleges nyelvével
    allapot = {'teljes': [0, 0], 'helykitoltovel': [0, 0], 'ketertelmu': [0, 0], 'reszleges': [0, 0], 'ismeretlen': [0, 0]}
    helykit = [0, 0]
    reszleges = []
    for (m, ny), db in sorted(par.items(), key=lambda x: -x[1]):
        f = felold(m, ny, k)
        allapot[f['allapot']][0] += 1
        allapot[f['allapot']][1] += db
        if f['helykitoltos']:
            helykit[0] += 1
            helykit[1] += db
        if f['allapot'] != 'teljes':
            reszleges.append((m, ny, db, f['szoveg']))
    # 2. nyelv nélkül (a kód önmagában): kétértelmű feloldások
    ketertelmu = []
    nny = {'teljes': [0, 0], 'helykitoltovel': [0, 0], 'ketertelmu': [0, 0], 'reszleges': [0, 0], 'ismeretlen': [0, 0]}
    for m, db in nyelv_nelkul.items():
        f = felold(m, None, k)
        nny[f['allapot']][0] += 1
        nny[f['allapot']][1] += db
        if f['ketertelmu']:
            ketertelmu.append((m, db))
    nem_illeszkedo = {}
    for m in kodok:
        fh = felold(m, 'H', k)
        if fh['allapot'] != 'teljes':
            nem_illeszkedo[m] = fh['allapot']
    ketertelmu_arami = sum(db for (m, ny), db in par.items()
                           if ny == 'A' and felold(m, None, k)['ketertelmu'])
    sorok = []
    sorok.append(f'# MORF_KULCS lefedettség (eszkozok/morf_feloldas.py --lefedettseg)\n')
    sorok.append('*proveniencia: scope=konkordancia/Macula_heber_*.tsv (morf oszlop) + adat/morf_kulcs_heber.tsv + '
                 'adat/morf_nyelv_aramai.tsv | forras=a fenti táblák (OSHB-jelkulcs, Macula lowfat lang) | ts=2026-10-05*\n')
    sorok.append(f'- Szó (morféma) összesen: {osszes}; különböző kód: {len(kodok)}; '
                 f'(kód, nyelv) pár: {len(par)}; arámi szó: {sum(db for (m, n), db in par.items() if n == "A")}; '
                 f'az arámi-táblázat morf-értéke a Macula-táblától eltér: {elteres} szón.')
    sorok.append('')
    sorok.append('## 1. A szó tényleges nyelvével ((kód, nyelv) pár)')
    sorok.append('')
    sorok.append('| állapot | pár | szó |')
    sorok.append('|---|---|---|')
    for a in ('teljes', 'helykitoltovel', 'ketertelmu', 'reszleges', 'ismeretlen'):
        sorok.append(f'| {a} | {allapot[a][0]} | {allapot[a][1]} |')
    sorok.append('')
    sorok.append('A `helykitoltovel` állapot: minden jel a táblából feloldva, de legalább egy pozíció a forrás szerinti `x` '
                 '(ismeretlen vagy szükségtelen érték). Nem teljes feloldás, külön számolva.')
    sorok.append('')
    sorok.append(f'Ebből `x` helykitöltőt tartalmaz (a forrás szerint „ismeretlen vagy szükségtelen érték”): '
                 f'{helykit[0]} pár, {helykit[1]} szó.')
    sorok.append('')
    if reszleges:
        sorok.append('Részlegesen vagy nem feloldott párok:')
        sorok.append('')
        sorok.append('| kód | nyelv | szó | kimenet |')
        sorok.append('|---|---|---|---|')
        for m, ny, db, sz in reszleges:
            sorok.append(f'| `{m}` | {ny} | {db} | {sz} |')
    else:
        sorok.append('Nincs részlegesen feloldott pár.')
    sorok.append('')
    sorok.append('## 2. Nyelv nélkül (csak a kód)')
    sorok.append('')
    sorok.append('| állapot | kód | szó |')
    sorok.append('|---|---|---|')
    for a in ('teljes', 'helykitoltovel', 'ketertelmu', 'reszleges', 'ismeretlen'):
        sorok.append(f'| {a} | {nny[a][0]} | {nny[a][1]} |')
    sorok.append('')
    sorok.append(f'Kétértelmű (a törzs jele mindkét nyelvben szerepel, más megnevezéssel): {len(ketertelmu)} kód, '
                 f'{sum(db for _, db in ketertelmu)} szó; ebből tényleg arámi szó: {ketertelmu_arami}. '
                 'Nyelv nélkül ezek mindkét olvasatot kapják, `[nyelv ismeretlen]` jelzéssel.')
    sorok.append('')
    sorok.append('## 3. A héber olvasatban nem teljesen feloldott kódok (az M0 nem illeszkedő kódjai és az x-helykitöltősök)')
    sorok.append('')
    sorok.append('| kód | héber olvasat | szó héberként | szó arámiként | arámi olvasat |')
    sorok.append('|---|---|---|---|---|')
    for m in sorted(nem_illeszkedo, key=lambda x: -nyelv_nelkul[x]):
        fa = felold(m, 'A', k)
        sorok.append(f'| `{m}` | {nem_illeszkedo[m]} | {par.get((m, "H"), 0)} | {par.get((m, "A"), 0)} | {fa["allapot"]} |')
    sorok.append('')
    szoveg = '\n'.join(sorok) + '\n'
    if jelentes_ut:
        open(jelentes_ut, 'w', encoding='utf-8', newline='\n').write(szoveg)
    if kiir:
        print(szoveg)
    return par, allapot, reszleges, ketertelmu


def main(argv):
    if len(argv) >= 2 and argv[1] == '--lefedettseg':
        lefedettseg(argv[2] if len(argv) > 2 else None)
        return
    if len(argv) < 2:
        print(__doc__)
        return
    ny = argv[2] if len(argv) > 2 else None
    f = felold(argv[1], ny)
    print(f['kod'], '|', f['nyelv'] or 'nyelv ismeretlen', '|', f['allapot'])
    print(f['szoveg'])
    if f['hianyzo']:
        print('HIÁNYZÓ:', f['hianyzo'])


if __name__ == '__main__':
    main(sys.argv)
