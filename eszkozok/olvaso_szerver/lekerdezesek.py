"""Az olvasói szerver összes SQL-je (#76 M2, M0 3.6). Máshol SQL nem áll (N-F76c: a Semgrep-szabály ezt őrzi).

Szabályok:
- minden érték paraméter (`?`); a bemenet sosem kerül az SQL szövegébe;
- az egyetlen szövegben összeállított rész a `?,?,?` helyőrző-lánc az `IN (...)` listákhoz (csak a darabszám függ a
  bemenettől, a tartalom nem), a rendezés és a LIMIT fix;
- a függvények `sqlite3.Connection`-t kapnak (csak olvasó, authorizerrel; l. adatbazis.py) és egyszerű Python-
  szerkezeteket (tuple, dict, list) adnak vissza; HTML-t nem állítanak elő.
Az adatok a #60 pilot (`eszkozok/olvaso_pilot/db_meres.py`: `db_vers`, `db_szo`, `db_gorog`) blokk-logikájából
vannak átírva; a D2-egyezést a `teszt_olvaso_szerver.py` méri.
"""
import re
import unicodedata
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------------------------------------------------
# normalizálás
# ---------------------------------------------------------------------------------------------------------------------
STRONG_RE = re.compile(r'^([HGhg])0*([0-9]{1,4})([A-Za-z]?)$')


def hnorm(s):
    """`h216` / `H0216` / `G1504a` -> `H0216` / `G1504A`; érvénytelen bemenetre None."""
    m = STRONG_RE.match((s or '').strip())
    if not m:
        return None
    return '%s%04d%s' % (m.group(1).upper(), int(m.group(2)), m.group(3).upper())


def konyv_slug(kk_kod):
    """`1Móz` -> `1Moz`: az URL-ben használt ASCII-sített könyvkód."""
    return ''.join(c for c in unicodedata.normalize('NFD', kk_kod) if unicodedata.category(c) != 'Mn')


def csupasz_alak(szo):
    return re.sub(r'[^\wáéíóöőúüűÁÉÍÓÖŐÚÜŰ-]', '', szo).lower()


def tisztit_tbesg(jel):
    jel = re.sub(r'<ref=[^>]*>', '', jel)
    jel = re.sub(r'<BR\s*/?>', '\n', jel)
    return re.sub(r'<[^>]+>', '', jel).replace('__', '').strip()


def _helyorzok(n):
    return ','.join('?' * n)


def _in(con, sql_elo, sql_uto, lista, elo_param=(), uto_param=(), csomag=400):
    """`sql_elo (?,?,...) sql_uto` lekérdezés `lista` elemeire csomagokban; az eredménysorok összefűzve."""
    ki = []
    lista = list(lista)
    for i in range(0, len(lista), csomag):
        resz = lista[i:i + csomag]
        ki.extend(con.execute(sql_elo + '(' + _helyorzok(len(resz)) + ')' + sql_uto, tuple(elo_param) + tuple(resz) + tuple(uto_param)).fetchall())
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# meta, licenc, navigáció
# ---------------------------------------------------------------------------------------------------------------------
def meta(con):
    return {k: v for k, v in con.execute('SELECT kulcs, ertek FROM meta WHERE kulcs NOT LIKE ?', ('hash:%',))}


def meta_sorok(con):
    """A teljes `meta` tábla (kulcs, érték), kulcs szerint rendezve: az adatbázis-kulcs (gyorsítótár) ebből hash-elődik."""
    return con.execute('SELECT kulcs, ertek FROM meta ORDER BY kulcs').fetchall()


def meta_hashek_db(con):
    return con.execute("SELECT COUNT(*) FROM meta WHERE kulcs LIKE 'hash:%'").fetchone()[0]


def tabla_licencek(con):
    """{tabla: dict(licenc_allapot, kereskedelmi, licenc_dataset, cimke)}."""
    return {t: {'allapot': a, 'kereskedelmi': k, 'dataset': d, 'cimke': c}
            for t, a, k, d, c in con.execute('SELECT tabla, licenc_allapot, kereskedelmi, licenc_dataset, cimke FROM tabla_licenc')}


def licenc_share_alike(con):
    """{dataset: share_alike} a `licencek` táblából."""
    return {d: s for d, s in con.execute('SELECT dataset, share_alike FROM licencek')}


def konyvek(con):
    """[(kk_kod, slug, teljes_nev, sorrend)] a Biblia sorrendjében."""
    return [(k, konyv_slug(k), n, o) for k, o, n in con.execute('SELECT kk_kod, sorrend, teljes_nev FROM konyv ORDER BY sorrend')]


def fejezetek(con, kk):
    """[(fejezet, versek_szama)] egy könyvre."""
    return con.execute('SELECT fejezet, COUNT(*) FROM vers WHERE konyv=? GROUP BY fejezet ORDER BY fejezet', (kk,)).fetchall()


def fejezet_versek(con, kk, fej):
    return con.execute('SELECT igehely, vers, karoli_szoveg FROM vers WHERE konyv=? AND fejezet=? ORDER BY vers', (kk, fej)).fetchall()


def vers_van(con, ig):
    return con.execute('SELECT 1 FROM vers WHERE igehely=?', (ig,)).fetchone() is not None


def nyelvtani_strongok(con):
    return {r[0] for r in con.execute('SELECT strong FROM grammatikai_strongok')}


def szofajok(con, strongok):
    return {s: z for s, z in _in(con, 'SELECT strong, szofaj FROM strong_szotar WHERE strong IN ', '', strongok)}


# ---------------------------------------------------------------------------------------------------------------------
# fejezet: szavak és párosítás (Olvasópult, Interlineáris, Munkaasztal)
# ---------------------------------------------------------------------------------------------------------------------
def fejezet_szavak(con, kk, fej):
    """{igehely: [ (sorszam, szo, [(er_sorszam, er_szo, strong, bizonyossag), ...]), ... ]}
    A magyar szavak a `token_karoli`-ból (oldal='hu'), a párosítás a `token_par`-ból, **pozíció szerint**
    (`hu_sorszam` = a magyar szó sorszáma; nem Strong-szám szerint)."""
    ki = defaultdict(list)
    sor = con.execute(
        "SELECT tk.igehely, tk.sorszam, tk.szo, tp.er_sorszam, tp.er_szo, tp.strong, tp.bizonyossag "
        "FROM vers v JOIN token_karoli tk ON tk.igehely=v.igehely AND tk.oldal='hu' "
        "LEFT JOIN token_par tp ON tp.igehely=tk.igehely AND tp.hu_sorszam=tk.sorszam "
        "WHERE v.konyv=? AND v.fejezet=? ORDER BY v.vers, tk.sorszam, tp.er_sorszam", (kk, fej)).fetchall()
    for ig, sz, szo, ers, erszo, st, bz in sor:
        lista = ki[ig]
        if not lista or lista[-1][0] != sz:
            lista.append((sz, szo, []))
        if st is not None:
            lista[-1][2].append((ers, erszo, st, bz))
    return ki


def fejezet_eredeti(con, kk, fej):
    """{(igehely, sorszam): (kiejtes, angol_tukorford, rovid_jelentes)} a fejezet eredeti szavaira (az Interlineáris csempékhez; a
    `token_par.er_sorszam` a `token_eredeti.sorszam`-ra illeszkedik)."""
    return {(ig, sz): (kiej or '', tukor or '', rovid or '') for ig, sz, kiej, tukor, rovid in con.execute(
        "SELECT e.igehely, e.sorszam, e.kiejtes, e.angol_tukorford, e.rovid_jelentes FROM vers v JOIN token_eredeti e ON e.igehely=v.igehely "
        "WHERE v.konyv=? AND v.fejezet=?", (kk, fej))}


def fejezet_parositatlan(con, kk, fej):
    """{igehely: [(sorszam, szo, strong)]} — az eredeti szavak, amelyek `sorszam`-a nem szerepel a `token_par` `er_sorszam`
    oszlopában (az Interlineáris nézet vers alatti külön sora)."""
    ki = defaultdict(list)
    for ig, sz, szo, st in con.execute(
            "SELECT tk.igehely, tk.sorszam, tk.szo, tk.strong FROM vers v JOIN token_karoli tk ON tk.igehely=v.igehely AND tk.oldal='er' "
            "WHERE v.konyv=? AND v.fejezet=? AND NOT EXISTS (SELECT 1 FROM token_par tp WHERE tp.igehely=tk.igehely AND tp.er_sorszam=tk.sorszam) "
            "ORDER BY v.vers, tk.sorszam", (kk, fej)):
        ki[ig].append((sz, szo, st))
    return ki


def fo_lista(parok, nyelvtani, szofaj_map):
    """A fő szó szabályával rendezett lista: [(strong, bizonyossag), ...]; az első a fő szó, a többi a „több héber szót ad
    vissza” esetben a kísérő (a pilot `hu_szavak[].fo` és `.tobbi`)."""
    funkcio = ('elöljárószó', 'kötőszó', 'partikula', 'névmás', 'indulatszó')

    def funkcioszo(st):
        return any(f in (szofaj_map.get(st) or '') for f in funkcio)

    fo = [(st, bz) for (_, _, st, bz) in parok if st not in nyelvtani]
    fo.sort(key=lambda k: (k[1] != 'magas', funkcioszo(k[0])))
    return fo


def fo_szo(parok, nyelvtani, szofaj_map):
    """A pilot szabálya (adat.py): ha egy Károli-szó több eredeti szót ad vissza, a fő szó előbb a `magas`
    bizonyosságú, azon belül a tartalmas szófajú (nem elöljáró/kötőszó/partikula/névmás/indulatszó); a nyelvtani
    Strong-számok kimaradnak. Visszaad: (strong, bizonyossag) vagy None."""
    fo = fo_lista(parok, nyelvtani, szofaj_map)
    return fo[0] if fo else None


def szovegbe_igazit(szoveg, szavak):
    """A `token_karoli` szavai írásjel nélküliek; a vers szövegéből (`vers.karoli_szoveg`) visszaadja a szavakhoz tartozó
    írásjelet. `szavak`: a tokenek szövege sorrendben. Visszaad: [(kiir, szokoz_utan)]: `kiir` = nyitó írásjel + szó + záró írásjel;
    `szokoz_utan` hamis, ha a következő szó közvetlenül kapcsolódik (kötőjel: *Béth-Semes* = Béth, Semes).
    Ha egy szó nem található a szövegben (a sorrendben), a kimenet a szó maga, írásjel nélkül, és a keresés a helyén marad."""
    ki, pos, n = [], 0, len(szoveg or '')
    for szo in szavak:
        i = (szoveg or '').find(szo, pos)
        if i < 0 or not szo:
            ki.append((szo, True))
            continue
        pre = szoveg[pos:i].strip()
        if pre and (any(c.isalnum() for c in pre)):
            pre = ''                                       # átugrott szavak: nem tapasztjuk a szóra
        j = i + len(szo)
        k = j
        while k < n and not szoveg[k].isalnum() and not szoveg[k].isspace():
            k += 1
        ki.append((pre + szo + szoveg[j:k], not (k < n and not szoveg[k].isspace())))
        pos = k
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# vers-lap blokkok
# ---------------------------------------------------------------------------------------------------------------------
def karoli_szoveg(con, ig):
    r = con.execute('SELECT karoli_szoveg FROM vers WHERE igehely=?', (ig,)).fetchone()
    return r[0] if r else None


def par(con, ig):
    """{hu_sorszam: [(strong, bizonyossag), ...]}"""
    ki = defaultdict(list)
    for hs, st, bz in con.execute('SELECT hu_sorszam, strong, bizonyossag FROM token_par WHERE igehely=? ORDER BY hu_sorszam, er_sorszam', (ig,)):
        ki[hs].append((st, bz))
    return dict(ki)


def bizonyossag_ertekek(con):
    """A `token_par` bizonyosság-értékei (a fejezet-lap `par-<érték>` osztályainak értékkészlete; a regiszter-őr, #98 M2)."""
    return sorted(r[0] for r in con.execute('SELECT DISTINCT bizonyossag FROM token_par WHERE bizonyossag IS NOT NULL'))


def par_szavak(con, ig):
    """[(hu_sorszam, hu_szo, er_sorszam, er_szo, strong, bizonyossag)] a Károli–Strong párosítás blokkhoz."""
    return con.execute('SELECT hu_sorszam, hu_szo, er_sorszam, er_szo, strong, bizonyossag FROM token_par WHERE igehely=? ORDER BY hu_sorszam, er_sorszam', (ig,)).fetchall()


def eredeti_szavak(con, ig):
    """[(sorszam, nyelv, strong_nyers, alak, kiejtes, szoto, rovid_jelentes, angol_tukorford)]"""
    return con.execute('SELECT sorszam, nyelv, strong_nyers, alak, kiejtes, szoto, rovid_jelentes, angol_tukorford FROM token_eredeti WHERE igehely=? ORDER BY sorszam', (ig,)).fetchall()


def heber_d2(con, ig):
    return [(hnorm(sn) or sn, alak, kiej) for sn, alak, kiej in con.execute(
        "SELECT strong_nyers, alak, kiejtes FROM token_eredeti WHERE igehely=? AND nyelv='H' ORDER BY sorszam", (ig,))]


def macula(con, ig):
    """A Macula-sorok dict-ként (a pilot `macula` mezői + xml_id az arámi/héber nyelvhez)."""
    return [{'xml_id': x, 'szo': a, 'lemma': b, 'strong': hnorm(c) if c else None, 'morf': d, 'szofaj': e, 'gloss': f,
             'lxx': g, 'lxx_strong': hnorm(h) if h else None}
            for x, a, b, c, d, e, f, g, h in con.execute(
                'SELECT xml_id, szo, lemma, strong_nyers, morf, szofaj, gloss, lxx_szo, lxx_strong FROM token_macula WHERE igehely=? ORDER BY rowid', (ig,))]


def morf_kulcs(con):
    """{(pozicio): {(nyelv, kod): jelentes_hu}} az `morf_kulcs_heber`-ből."""
    t = defaultdict(dict)
    for poz, nyelv, kod, hu in con.execute('SELECT pozicio, nyelv, kod, jelentes_hu FROM morf_kulcs_heber'):
        t[poz][(nyelv, kod)] = hu
    return dict(t)


def aramai_xml(con, xml_idk):
    """{xml_id: nyelv} az `morf_nyelv_aramai`-ból (hiányzó sor = héber)."""
    return {x: n for x, n in _in(con, 'SELECT xml_id, nyelv FROM morf_nyelv_aramai WHERE xml_id IN ', '', xml_idk)}


def lxx_szavak(con, ig):
    return [{'szoalak': a, 'lemma': b, 'strong': c or '', 'morf': d, 'szovegforma': e} for a, b, c, d, e in con.execute(
        'SELECT szoalak, lemma, strong, morf, szovegforma FROM lxx_token WHERE karoli_igehely=? ORDER BY szovegforma, pozicio, rowid', (ig,))]


def lxx_szavak_sorrendben(con, ig):
    """Az LXX-vers szavai a szövegbeli sorrendben (a pilot `lxx` listája; a csempe-blokk és a görög párosítás ezt használja)."""
    return [{'szoalak': a, 'lemma': b, 'strong': c or '', 'morf': d} for a, b, c, d in con.execute(
        'SELECT szoalak, lemma, strong, morf FROM lxx_token WHERE karoli_igehely=? ORDER BY CAST(pozicio AS INTEGER), rowid', (ig,))]


def lxx_versszam(con, ig):
    """([lxx_igehely (LXX_OS)], [(forras, lxx_igehely)], terkep_ertek-ek)"""
    lxx = []
    for (x,) in con.execute("SELECT lxx_igehely FROM lxx_versszam WHERE karoli_igehely=? AND forras='LXX_OS' ORDER BY rowid", (ig,)):
        if x not in lxx:
            lxx.append(x)
    extra = [tuple(x[:2]) for x in con.execute("SELECT forras, lxx_igehely FROM lxx_versszam WHERE karoli_igehely=? AND forras!='LXX_OS' ORDER BY rowid", (ig,))]
    terkep = [r[0] for r in con.execute("SELECT DISTINCT terkep_ertek FROM lxx_versszam WHERE karoli_igehely=? AND terkep_ertek IS NOT NULL AND terkep_ertek<>''", (ig,))]
    return lxx, extra, terkep


def versszamozas(con, ig):
    return con.execute('SELECT osztaly, kjv_igehely, mt_igehely, megfeleltetes_forras FROM vers_szamozas WHERE igehely=?', (ig,)).fetchone()


def bsb(con, ig):
    """[(sorszam, angol_szo, strong, morf, szamozas)] — az oszlopnevek közül a két ékezetes nevű kimarad."""
    return con.execute('SELECT sorszam, angol_szo, strong, morf, szamozas FROM bsb WHERE igehely=? ORDER BY sorszam', (ig,)).fetchall()


def kjv(con, ig):
    return con.execute('SELECT sorszam, angol_szo, strong, morf FROM kjv WHERE igehely=? ORDER BY sorszam', (ig,)).fetchall()


def nave(con, ig):
    """[(tema, cimke, hely, tartomanyos, tema_id)] — ismétlődések nélkül, a pilot sorrendjében."""
    ki, lat = [], set()
    for tema, cimke, hely, tart, tid in con.execute('SELECT tema, cimke, nave_hely, tartomanyos, tema_id FROM nave_vers WHERE igehely=? ORDER BY forras_sor, rowid', (ig,)):
        if (tema, cimke, hely) not in lat:
            lat.add((tema, cimke, hely))
            ki.append((tema, cimke, hely, bool(tart), tid))
    return ki


def tipnr(con, ig):
    return con.execute('SELECT nev, nevvaltozat, strong, nyelv FROM tipnr WHERE igehely=? ORDER BY rowid', (ig,)).fetchall()


def lxx_dontesek(con, ig):
    return con.execute('SELECT id, igehely, lxx_igehely, heber_strong, gorog_lemma, gorog_strong, tipus, megjegyzes, bizonyossag, proveniencia FROM lxx_dontesek WHERE igehely=? ORDER BY id', (ig,)).fetchall()


def kapcsolatok(con, ig):
    return con.execute('SELECT forras_igehely, cel_igehely, id, tipus, funkcio, bizonyossag FROM kapcsolatok WHERE forras_igehely=? OR cel_igehely=? ORDER BY id', (ig, ig)).fetchall()


def motivum_elofordulasok(con, ig):
    """Az adatréteg motívum-előfordulásai az igehelyen (a `kapcsolodas` az igehely-tartomány szövege; a mező a lekérdezés
    saját proveniencia-sorát hordozza). A mérlegelhető tartományi egyezést az `igehely_tartomany` tábla adja."""
    return con.execute(
        'SELECT e.id, e.igehely, e.funkcio, e.strong, e.karoli_szo, e.megbizhatosag, e.proveniencia, m.cim '
        'FROM elofordulasok e LEFT JOIN motivumok m ON m.id=e.id WHERE e.igehely=? ORDER BY e.id', (ig,)).fetchall()


def tsk(con, ig):
    return con.execute('SELECT cel_igehely, votes FROM tsk WHERE igehely=? ORDER BY votes DESC, cel_igehely', (ig,)).fetchall()


def kh(con, ig):
    return con.execute('SELECT cel_tol, cel_ig FROM kh WHERE igehely=? ORDER BY rowid', (ig,)).fetchall()


def kh_darab(con, ig):
    return con.execute('SELECT COUNT(*) FROM kh WHERE igehely=?', (ig,)).fetchone()[0]


def ubs_dbh(con, ig):
    """[(strong, lexid, domen, definicio_rovid, glosszak)] az előfordulásra (referencia ∩ jelentés)."""
    return con.execute(
        'SELECT DISTINCT r.strong, r.lexid, j.domen, j.definicio_rovid, j.glosszak FROM ubs_dbh_referenciak r '
        'JOIN ubs_dbh_jelentesek j ON j.lexid=r.lexid WHERE r.igehely=? ORDER BY r.strong, r.lexid', (ig,)).fetchall()


def ubs_d2(con, ig, strongok):
    ki = {}
    for st in set(strongok):
        ki[st] = sorted(x[0] for x in con.execute(
            'SELECT DISTINCT r.lexid FROM ubs_dbh_referenciak r JOIN ubs_dbh_jelentesek j ON j.lexid=r.lexid WHERE r.igehely=? AND r.strong=?', (ig, st)))
    return ki


def nave_fejezet(con, ig):
    """A Nave fejezet-szintű hivatkozásai a vers Károli-fejezetére: [(tema, cimke, hely, tema_id)] ismétlődések nélkül, a TSV sorrendjében
    (a `nave_vers` a fejezet-szintű sorokat nem tartalmazza, SEMA 2.x: a fejezet-nézet a `nave_basokant`-ból jön)."""
    kk, _, vf = ig.rpartition(' ')
    kulcs = kk + ' ' + vf.split(':')[0]
    ki, lat = [], set()
    for tema, cimke, hely, tid in con.execute("SELECT tema, cimke, igehely, tema_id FROM nave_basokant WHERE hely_tipus='fejezet' AND igehely=? ORDER BY rowid", (kulcs,)):
        if (tema, cimke, hely) not in lat:
            lat.add((tema, cimke, hely))
            ki.append((tema, cimke, hely, tid))
    return ki


def lxx_versszintu(con, ig):
    """{heber_strong: [gorog_strong, ...]} a vers LXX-versszintű együttelőfordulásaira (nem szóillesztés), rendezve (a pilot `lxx_par`)."""
    d = defaultdict(set)
    for h, g in con.execute('SELECT heber_strong, gorog_strong FROM lxx_versszintu_parok WHERE igehely=?', (ig,)):
        d[h].add(g)
    return {h: sorted(g) for h, g in sorted(d.items())}


def heber_strongok_versekre(con, igehelyek):
    """A versek héber szavainak normalizált Strong-számai (TAHOT), a nyelvtaniak nélkül, rendezve."""
    ki = set()
    for (sn,) in _in(con, "SELECT DISTINCT strong_nyers FROM token_eredeti WHERE nyelv='H' AND igehely IN ", '', igehelyek):
        n = hnorm(sn)
        if n:
            ki.add(n)
    return sorted(ki)


def gorog_strongok_versekre(con, igehelyek):
    """A versek görög szavai (LXX_OS): a pilot `gor_szavak` első forrása (a Macula-párokat a héber csempék párosítása adja, l. `oldalak.szamlalok`)."""
    return {st for (st,) in _in(con, "SELECT DISTINCT strong FROM lxx_token WHERE strong <> '' AND karoli_igehely IN ", '', igehelyek) if st}


def karoli_strong_konyvek(con):
    """A Károli–Strong párosítással feldolgozott könyvek ASCII-kódja (a pilot `karoli_konyvek`), rendezve."""
    return sorted({konyv_slug(k) for (k,) in con.execute("SELECT DISTINCT substr(igehely, 1, instr(igehely, ' ') - 1) FROM token_par")})


def hu_par_szavak(con, ig):
    """{hu_sorszam: (hu_szo, [(er_sorszam, er_szo, strong, bizonyossag)])} a Károli-szavak héber párjaihoz („Károli itt”)."""
    ki = {}
    for hs, hu, ers, erszo, st, bz in con.execute('SELECT hu_sorszam, hu_szo, er_sorszam, er_szo, strong, bizonyossag FROM token_par WHERE igehely=? ORDER BY hu_sorszam, er_sorszam', (ig,)):
        ki.setdefault(hs, (hu, []))[1].append((ers, erszo, st, bz))
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# szó-lap blokkok (héber)
# ---------------------------------------------------------------------------------------------------------------------
def strong_szotar(con, s):
    return con.execute('SELECT szoto, kiejtes, szofaj, jelentes, gyok_szarmaztatas FROM strong_szotar WHERE strong=?', (s,)).fetchone()


def strong_van(con, s):
    """Létezik-e a Strong-szám a szótárakban vagy a tokenekben (ismeretlen -> 404)."""
    for t in ('strong_szotar', 'tbesg', 'token_strong'):
        if t == 'strong_szotar' and con.execute('SELECT 1 FROM strong_szotar WHERE strong=?', (s,)).fetchone():
            return True
        if t == 'tbesg' and con.execute('SELECT 1 FROM tbesg WHERE strong=?', (s,)).fetchone():
            return True
        if t == 'token_strong' and con.execute('SELECT 1 FROM token_strong WHERE strong=? LIMIT 1', (s,)).fetchone():
            return True
    return False


def bdb_angol(con, s):
    r = con.execute('SELECT teljes_szocikk FROM bdb WHERE strong=?', (s,)).fetchone()
    return r[0] if r else None


def bdb_magyar(con, s):
    hu = None
    for (szoveg,) in con.execute("SELECT forditas_hu FROM forditasok WHERE szotar='BDB' AND strong=? ORDER BY rowid", (s,)):
        if szoveg and szoveg.strip():
            hu = szoveg.replace('\\n', '\n')
    return hu


def bdb_magyar_meta(con, s):
    """A magyar BDB-szócikk fordítás-jelölése: „modell, dátum” (a `forditasok.modell`, `.datum`; ugyanaz a sor, amelyet `bdb_magyar` választ: az utolsó nem üres)."""
    meta = None
    for szoveg, modell, datum in con.execute("SELECT forditas_hu, modell, datum FROM forditasok WHERE szotar='BDB' AND strong=? ORDER BY rowid", (s,)):
        if szoveg and szoveg.strip():
            meta = '%s, %s' % (modell, datum)
    return meta


def bdb_alias(con, s):
    return con.execute('SELECT tabla_strong, bdb_id, szoveg_hasonlosag FROM bdb_alias WHERE masodlagos_strong=?', (s,)).fetchone()


def elofordulas(con, s):
    """(előfordulás, könyvek száma)"""
    return con.execute("SELECT COUNT(*), COUNT(DISTINCT substr(igehely, 1, instr(igehely, ' ') - 1)) FROM token_strong WHERE strong=?", (s,)).fetchone()


def nyelvtani(con, s):
    return con.execute('SELECT kategoria, rovid_jelentes, kizaras_oka FROM grammatikai_strongok WHERE strong=?', (s,)).fetchone()


def karoli_alakok(con, s):
    """(összes, magas, [(alak, db), ...] legfeljebb 8) — a pilot `csupasz_alak` szabályával."""
    alak, magas = Counter(), 0
    for hu, bz in con.execute('SELECT hu_szo, bizonyossag FROM token_par WHERE strong=?', (s,)):
        a = csupasz_alak(hu)
        if a:
            alak[a] += 1
            magas += (bz == 'magas')
    return sum(alak.values()), magas, alak.most_common(8)


def lxx_bridge_h(con, s):
    """[(count, greek_strong)] csökkenő sorrendben."""
    return sorted(((int(c), g) for g, c in con.execute('SELECT greek_strong, count FROM lxx_bridge WHERE strong=?', (s,))), reverse=True)


def lxx_bridge_g(con, g):
    return sorted(((int(c), h) for h, c in con.execute('SELECT hebrew_strong, count FROM lxx_bridge WHERE greek_strong=?', (g,))), reverse=True)


def rovid_szotar(con, strongok):
    """{strong: (szoto, jelentes)} a híd-listák címkéihez."""
    return {s: (a, b) for s, a, b in _in(con, 'SELECT strong, szoto, jelentes FROM strong_szotar WHERE strong IN ', '', strongok)}


def sdbh(con, s):
    return con.execute('SELECT domen_kod, domen, glossza, hivatkozas_n FROM sdbh_domenek WHERE strong=? ORDER BY domen_kod', (s,)).fetchall()


def sdgnt(con, s):
    return con.execute('SELECT domen_kod, domen, glossza, hivatkozas_n FROM sdgnt_domenek WHERE strong=? ORDER BY domen_kod', (s,)).fetchall()


def sece_h(con, s):
    r = con.execute('SELECT teljes_szocikk FROM sece_h WHERE strong=?', (s,)).fetchone()
    return r[0] if r else None


def sece_g(con, s):
    r = con.execute('SELECT teljes_szocikk FROM sece_g WHERE strong=?', (s,)).fetchone()
    return r[0] if r else None


def oshl_csalad(con, s):
    """F99 M1: a szó OSHL-gyökcsaládja (`oshl_lexikalis_index` etym_tipus / etym_cel / gyok). Visszaad:
    None, ha az adatbázisban nincsenek gyökcsalád-oszlopok (régebbi építés); különben {'tipusok': [a szó bejegyzéseinek etym_tipus-a],
    'csaladok': [{'gyok_id', 'gyok': (oshl_id, strong, lemma, atiras, szofaj, def_en, gyok), 'tagok': [(oshl_id, strong, lemma, atiras, szofaj, def_en)]}]}.
    A `sub` a gyök (main) bejegyzésre mutat, a `main` a származékait listázza; a gyök-bejegyzésnek nem mindig van Strong-száma."""
    oszl = {r[1] for r in con.execute('PRAGMA table_info(oshl_lexikalis_index)')}
    if not {'etym_tipus', 'etym_cel', 'gyok'} <= oszl:
        return None
    sajat = con.execute('SELECT oshl_id, etym_tipus, etym_cel FROM oshl_lexikalis_index WHERE strong=? ORDER BY rowid', (s,)).fetchall()
    gyok_idk = []
    for oid, tipus, cel in sajat:
        g = oid if tipus == 'main' else (cel if tipus == 'sub' and cel and cel != '—' else None)
        if g and g not in gyok_idk:
            gyok_idk.append(g)
    csaladok = []
    for g in gyok_idk:
        gy = con.execute('SELECT oshl_id, strong, lemma, atiras, szofaj, def_en, gyok, etym_cel FROM oshl_lexikalis_index WHERE oshl_id=? '
                         'ORDER BY rowid LIMIT 1', (g,)).fetchone()
        if not gy:
            continue
        tagok = []
        for t in [x for x in (gy[7] or '').split(',') if x and x != '—']:
            r = con.execute('SELECT oshl_id, strong, lemma, atiras, szofaj, def_en FROM oshl_lexikalis_index WHERE oshl_id=? ORDER BY rowid LIMIT 1',
                            (t,)).fetchone()
            if r:
                tagok.append(r)
        csaladok.append({'gyok_id': g, 'gyok': gy[:7], 'tagok': tagok})
    return {'tipusok': [t for _, t, _ in sajat], 'csaladok': csaladok}


def oshl(con, s):
    """(lexikális index sorai, BDB-helyek)"""
    lex = con.execute('SELECT twot, bdb_id, nyelv, oshl_id, lemma, atiras, szofaj, def_en FROM oshl_lexikalis_index WHERE strong=? ORDER BY rowid', (s,)).fetchall()
    hely = con.execute('SELECT bdb_id, konyv, fejezet, vers FROM oshl_bdb_igehelyek WHERE strong=? ORDER BY sorszam LIMIT 50', (s,)).fetchall()
    return lex, hely


def tbesh(con, s):
    return con.execute('SELECT szo, atiras, morf, gloss, jelentes FROM tbesh WHERE strong=? ORDER BY rowid', (s,)).fetchall()


def tw(con, s):
    return con.execute("SELECT tw_id, kategoria, cim, szoveg FROM tw_szocikkek WHERE instr('+' || strong || '+', '+' || ? || '+') > 0 ORDER BY tw_id", (s,)).fetchall()


# ---------------------------------------------------------------------------------------------------------------------
# szó-lap blokkok (görög)
# ---------------------------------------------------------------------------------------------------------------------
def tbesg(con, g):
    r = con.execute('SELECT szo, atiras, gloss, jelentes FROM tbesg WHERE strong=? ORDER BY rowid LIMIT 1', (g,)).fetchone()
    if not r:
        return None
    return (r[0], r[1], r[2], tisztit_tbesg(r[3] or ''))


def thayer(con, g):
    r = con.execute('SELECT teljes_szocikk FROM thayer WHERE strong=?', (g,)).fetchone()
    return r[0] if r else None


def magyar_gorog(con, g):
    """[(szotar, jelentes_szam, forditas_hu)] a Thayer és az UBS DNTG magyar fordításai."""
    return con.execute("SELECT szotar, jelentes_szam, forditas_hu FROM forditasok WHERE szotar IN ('Thayer','UBS_DNTG') AND strong=? AND forditas_hu <> '' ORDER BY rowid", (g,)).fetchall()


def usz(con, g):
    """(előfordulás, versek száma, [(igehely, karoli_szoveg)] legfeljebb 5)"""
    n = con.execute('SELECT COUNT(*), COUNT(DISTINCT igehely) FROM token_strong WHERE strong=?', (g,)).fetchone()
    versek = con.execute('SELECT v.igehely, v.karoli_szoveg FROM vers v WHERE v.igehely IN (SELECT igehely FROM token_strong WHERE strong=?) ORDER BY v.sorrend LIMIT 5', (g,)).fetchall()
    return n[0], n[1], versek


def usz_lanc(con, g):
    """Hány előfordulás számít „+” Strong-lánc elemeként (a `token_strong` a TAGNT lánc-elemeit külön sorként is számolja,
    DT133 / DT-F76d). A bontás: `usz()` első értéke = az egész mezős előfordulás + ez a szám."""
    return con.execute(
        "SELECT COUNT(*) FROM token_strong s JOIN token_eredeti e ON e.igehely=s.igehely AND e.sorszam=s.sorszam "
        "WHERE s.strong=? AND e.nyelv='G' AND e.strong_lanc LIKE '%+%'", (g,)).fetchone()[0]


def lsj(con, g):
    r = con.execute('SELECT teljes_szocikk FROM lsj WHERE strong=?', (g,)).fetchone()
    return r[0] if r else None


def mcged(con, g):
    return con.execute('SELECT gk_szam, lemma_gorog, atirat, gyakorisag, glossza FROM mcged WHERE strong=? ORDER BY rowid', (g,)).fetchall()


def ubs_dntg(con, g):
    jel = con.execute('SELECT lexid, domen, definicio_rovid, glosszak FROM ubs_dntg_jelentesek WHERE strong=? ORDER BY lexid', (g,)).fetchall()
    ref = con.execute('SELECT lexid, igehely FROM ubs_dntg_referenciak WHERE strong=? ORDER BY lexid, rowid LIMIT 40', (g,)).fetchall()
    return jel, ref
