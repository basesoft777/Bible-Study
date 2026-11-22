"""Az adatbázis-építés forrás-azonosítója (#101, DT-F101a): az `adat/` és a `konkordancia/` adatfájljainak és a tanulmányszövegek (`motivumok/` stb.) ujjlenyomata.

Az `sqlite_epit.py` építéskor a `meta` táblába írja (`forras:<útvonal>` = `méret|mtime|sha256`, és `forras_osszeg`); az olvasó
(`allapot.py`) és az indító ebből dönti el, hogy a `pardes.db` régebbi-e az adatnál.

Az észlelés kétlépcsős (DT-F101a): az mtime (egész másodpercre kerekítve) + méret csak gyors előszűrő; eltérésnél a `sha256` dönt, mert az mtime
kicsekkoláskor és másoláskor tartalomváltozás nélkül is módosul. Új vagy törölt fájl mindig változás.
Csak a szabványos könyvtárat használja (az `allapot.py` Flask nélkül is importálja).
"""
import hashlib
import os
import sys
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Az építő által olvasott források: az `adat/` és a `konkordancia/` adatfájljai (a `.md` dokumentáció, a `.jsonl` LLM-hívásnapló és a `.html`
# nem adat: a változásuk nem kérhet újraépítést), valamint a tanulmány-/motívumszövegek (`.md`), amelyeket az építő az FTS-be és a tanulmány-
# regiszterbe tölt (sqlite_epit.py `_fts`, `tanulmany_regiszter`). Az építő kódjának változása nem része az azonosítónak (ismert korlát).
RESZEK = ('adat', 'konkordancia')
KIHAGYOTT_UTOTAG = ('.db', '.tmp', '.epit', '.pyc', '.zar', '.md', '.jsonl', '.html', '.log')
TANULMANY_RESZEK = ('motivumok', 'tematikus_lezart', 'genezis', 'ujszovetseg', 'melyelemzesek')
META_ELOTAG = 'forras:'
META_OSSZEG = 'forras_osszeg'


# A háttér-újraépítés pillanatképébe másolt útvonalak (epit_hatter.sh): az építés által ténylegesen megnyitott könyvtárak és fájlok. Levezetés: az
# `sqlite_epit.py --mod teljes` futása `sys.addaudithook('open')` figyelésével (F101.5, naplok/F101_jelentes.md): adat/, konkordancia/, genezis/,
# melyelemzesek/, motivumok/, tematikus_lezart/, ujszovetseg/, eszkozok/ (a modulok), lexikon/ (a HAMART-001 lap) és a gyökér DONTESEK.md. Minden
# más (.claude/ és benne a worktree-k, archivum/, generalt_proba/, naplok/, .git, kozlemeny/ …) kimarad. Új olvasott könyvtár esetén ide kell felvenni
# (a `teszt_indito.py` `test_a_masolando_lista_lefedi_az_epito_forrasait` őrzi a forrás-azonosító könyvtáraira).
MASOLANDO = RESZEK + TANULMANY_RESZEK + ('eszkozok', 'lexikon', 'DONTESEK.md')


def masolando(gyoker):
    """A `MASOLANDO` azon elemei, amelyek a gyökérben léteznek (a `tar` nem hibázik hiányzó útvonalon)."""
    return [x for x in MASOLANDO if os.path.exists(os.path.join(gyoker, x))]


def forrasfajlok(gyoker):
    """A forrásfájlok gyökérhez viszonyított, `/` elválasztós útvonalai, rendezve."""
    ki = []
    for resz in RESZEK + TANULMANY_RESZEK:
        tanulmany = resz in TANULMANY_RESZEK
        alap = os.path.join(gyoker, resz)
        for dp, dn, fn in os.walk(alap):
            dn[:] = [d for d in dn if d != '__pycache__' and not d.startswith('.')]
            for f in fn:
                if f.startswith('.'):
                    continue
                if tanulmany:
                    if not f.endswith('.md'):
                        continue
                elif f.endswith(KIHAGYOTT_UTOTAG):
                    continue
                ki.append(os.path.relpath(os.path.join(dp, f), gyoker).replace('\\', '/'))
    return sorted(ki)


def stat_kulcs(ut):
    """(méret, mtime egész másodpercre kerekítve): a másodperc alatti pontosság fájlrendszerenként (NTFS, 9p, ext4) más, ezért kerekítünk."""
    st = os.stat(ut)
    return st.st_size, int(st.st_mtime)


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for blokk in iter(lambda: f.read(1 << 20), b''):
            h.update(blokk)
    return h.hexdigest()


def azonosito(gyoker, szalak=4):
    """{útvonal: (méret, mtime, sha256)} a mostani fájlokra. A hash-elés szálakon fut (a hashlib felengedi a GIL-t)."""
    fajlok = forrasfajlok(gyoker)

    def egy(rel):
        ut = os.path.join(gyoker, rel)
        meret, mt = stat_kulcs(ut)
        return rel, (meret, mt, sha256_fajl(ut))
    with ThreadPoolExecutor(max_workers=szalak) as ex:
        return dict(ex.map(egy, fajlok))


def osszeg(azon):
    """Az egész forrás-halmaz egyetlen hash-e (útvonal + sha256, rendezve)."""
    h = hashlib.sha256()
    for rel in sorted(azon):
        h.update(('%s\t%s\n' % (rel, azon[rel][2])).encode('utf-8'))
    return h.hexdigest()


def meta_sorok(azon):
    """A `meta` tábla sorai: egy sor fájlonként + az összeg."""
    sorok = [(META_ELOTAG + rel, '%d|%d|%s' % azon[rel]) for rel in sorted(azon)]
    sorok.append((META_OSSZEG, osszeg(azon)))
    return sorok


def meta_olvas(sorok):
    """A `meta` (kulcs, érték) sorokból {útvonal: (méret, mtime, sha256)}; üres, ha az adatbázis nem tárol forrás-azonosítót (régi építés)."""
    ki = {}
    for k, v in sorok:
        if isinstance(k, str) and k.startswith(META_ELOTAG):
            try:
                meret, mt, sha = str(v).split('|')
                ki[k[len(META_ELOTAG):]] = (int(meret), int(mt), sha)
            except ValueError:
                continue
    return ki


def osszehasonlit(gyoker, tarolt, sha_tar=None):
    """(allapot, változások): `friss` | `regebbi` | `nincs_adat` (az adatbázis nem tárol forrás-azonosítót).
    `sha_tar`: folyamaton belüli gyorsítótár {(útvonal, méret, mtime): sha256}, hogy az ismételt ellenőrzés ne hash-eljen újra.
    A változás-lista elemei: `<útvonal> (új|törölt|módosult)`."""
    if not tarolt:
        return 'nincs_adat', []
    ma = {}
    for rel in forrasfajlok(gyoker):
        ma[rel] = stat_kulcs(os.path.join(gyoker, rel))
    valt = []
    for rel in sorted(set(ma) | set(tarolt)):
        if rel not in tarolt:
            valt.append('%s (új)' % rel)
        elif rel not in ma:
            valt.append('%s (törölt)' % rel)
        else:
            meret, mt = ma[rel]
            tmeret, tmt, tsha = tarolt[rel]
            if (meret, mt) == (tmeret, tmt):
                continue
            if meret != tmeret:
                valt.append('%s (módosult)' % rel)
                continue
            kulcs = (rel, meret, mt)
            sha = sha_tar.get(kulcs) if sha_tar is not None else None
            if sha is None:
                sha = sha256_fajl(os.path.join(gyoker, rel))
                if sha_tar is not None:
                    sha_tar[kulcs] = sha
            if sha != tsha:
                valt.append('%s (módosult)' % rel)
    return ('regebbi' if valt else 'friss'), valt


if __name__ == '__main__':
    # `forras_azonosito.py --masolando <gyoker>`: soronként a pillanatképbe másolandó útvonalak (az epit_hatter.sh ezt hívja)
    if len(sys.argv) == 3 and sys.argv[1] == '--masolando':
        print('\n'.join(masolando(sys.argv[2])))
        sys.exit(0)
    print(__doc__, file=sys.stderr)
    sys.exit(2)
