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
import sqlite3
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


_MACULA_SQL = ('SELECT xml_id, szo, lemma, strong_nyers, morf, szofaj, gloss, lxx_szo, lxx_strong, lxx_szo_forras, lxx_szo_rahlfs '
               'FROM token_macula WHERE igehely=? ORDER BY rowid')
# F115.4 előtti építés: nincs `lxx_szo_forras` / `lxx_szo_rahlfs` oszlop; a két mező üres marad
_MACULA_SQL_REGI = ("SELECT xml_id, szo, lemma, strong_nyers, morf, szofaj, gloss, lxx_szo, lxx_strong, '', '' "
                    'FROM token_macula WHERE igehely=? ORDER BY rowid')


def macula(con, ig):
    """A Macula-sorok dict-ként (a pilot `macula` mezői + xml_id az arámi/héber nyelvhez).
    Az F115.4 előtt épült adatbázisban az `lxx_forras` és az `lxx_rahlfs` üres (az oszlopok hiányoznak; az `oshl_csalad` mintája)."""
    oszl = {r[1] for r in con.execute('PRAGMA table_info(token_macula)')}
    sql = _MACULA_SQL if {'lxx_szo_forras', 'lxx_szo_rahlfs'} <= oszl else _MACULA_SQL_REGI
    return [{'xml_id': x, 'szo': a, 'lemma': b, 'strong': hnorm(c) if c else None, 'morf': d, 'szofaj': e, 'gloss': f,
             'lxx': g, 'lxx_strong': hnorm(h) if h else None, 'lxx_forras': i or '', 'lxx_rahlfs': j or ''}
            for x, a, b, c, d, e, f, g, h, i, j in con.execute(sql, (ig,))]


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
    saját proveniencia-sorát hordozza). A mérlegelhető tartományi egyezést az `igehely_tartomany` tábla adja.
    Sor: (id, igehely, funkcio, strong, karoli_szo, megbizhatosag, proveniencia, cim, pardes_szint, forras_tanulmany)."""
    return con.execute(
        'SELECT e.id, e.igehely, e.funkcio, e.strong, e.karoli_szo, e.megbizhatosag, e.proveniencia, m.cim, e.pardes_szint, '
        'e.forras_tanulmany FROM elofordulasok e LEFT JOIN motivumok m ON m.id=e.id WHERE e.igehely=? ORDER BY e.id', (ig,)).fetchall()


def motivum_szomszedok(con, mid, ig):
    """A motívum előző és következő előfordulása a kánoni (Károli-) sorrendben: ((igehely, funkcio) | None, (igehely, funkcio) | None).
    Az igehelyek az `elofordulasok` kulcsai; a sorrend a `vers.sorrend`, a nem egy versre szóló kulcs (tartomány) kimarad."""
    sor = con.execute(
        'SELECT v.sorrend, e.igehely, e.funkcio FROM elofordulasok e JOIN vers v ON v.igehely=e.igehely WHERE e.id=? '
        'ORDER BY v.sorrend, e.igehely', (mid,)).fetchall()
    uj = [i for i, r in enumerate(sor) if r[1] == ig]
    if not uj:
        return None, None
    i = uj[0]
    elozo = next(((sor[k][1], sor[k][2]) for k in range(i - 1, -1, -1) if sor[k][1] != ig), None)
    kov = next(((sor[k][1], sor[k][2]) for k in range(i + 1, len(sor)) if sor[k][1] != ig), None)
    return elozo, kov


# ---------------------------------------------------------------------------------------------------------------------
# tanulmányok (F149): a regiszter és a vers -> szakasz index a `pardes.db` generált tábláiból; a tábla hiánya (régebbi építés) üres eredmény
# ---------------------------------------------------------------------------------------------------------------------
def tanulmany_tabla_van(con):
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='tanulmany_hivatkozas'").fetchone() is not None


def tanulmany_van(con, tid):
    """(tanulmany_id, tipus, cim, tartomany, fajl) vagy None."""
    try:
        return con.execute('SELECT tanulmany_id, tipus, cim, tartomany, fajl FROM tanulmany WHERE tanulmany_id=?', (tid,)).fetchone()
    except sqlite3.OperationalError:
        return None


def tanulmany_szoveg(con, tid):
    """A tanulmány markdown-szövege a `tanulmany_szoveg` táblából (a /tanulmany/<id> oldalnak) vagy None."""
    try:
        r = con.execute('SELECT szoveg FROM tanulmany_szoveg WHERE tanulmany_id=?', (tid,)).fetchone()
    except sqlite3.OperationalError:
        return None
    return r[0] if r else None


def tanulmany_tartomanyok(con, tid):
    """[(kezdo, veg)] igehelyek a tanulmány tartományaihoz, a részek sorrendjében."""
    try:
        return con.execute('SELECT kezdo, veg FROM tanulmany_tartomany WHERE tanulmany_id=? ORDER BY resz', (tid,)).fetchall()
    except sqlite3.OperationalError:
        return []


def konyv_tabla_sorok(con):
    """A könyvnév-felismeréshez: [(STEP-kód, kk_kod, teljes név, '')] a `konyv` táblából (a Konyv_normalizalo_tabla sorai)."""
    return [(st or '', kk, nev or '', '') for kk, st, nev in con.execute('SELECT kk_kod, step_kod, teljes_nev FROM konyv ORDER BY sorrend')]


def tanulmanyok_versre(con, ig):
    """([tartalmazó], [hivatkozó]) az igehelyre. tartalmazó: [(id, tipus, cim, tartomany, sorrend, [(horgony, szakasz_cim, fokozat, hivatkozas)])]
    a bővített → mélyelemzés sorrendben; hivatkozó: a tartományán kívül név szerint hivatkozó tanulmányok [(id, tipus, cim, tartomany,
    [(horgony, szakasz_cim, hivatkozas)])]."""
    try:
        sorr = con.execute('SELECT sorrend FROM vers WHERE igehely=?', (ig,)).fetchone()
        if not sorr:
            return [], []
        tart = con.execute(
            'SELECT DISTINCT t.tanulmany_id, t.tipus, t.cim, t.tartomany, t.sorrend FROM tanulmany_tartomany r JOIN tanulmany t '
            'ON t.tanulmany_id=r.tanulmany_id WHERE r.kezdo_sorrend<=? AND r.veg_sorrend>=? '
            "ORDER BY CASE t.tipus WHEN 'bovitett' THEN 0 ELSE 1 END, t.sorrend", (sorr[0], sorr[0])).fetchall()
        hiv = con.execute(
            'SELECT h.tanulmany_id, h.szakasz_horgony, h.szakasz_cim, h.fokozat, h.hivatkozas, h.tartomanyban FROM tanulmany_hivatkozas h '
            'WHERE h.igehely=? ORDER BY h.tanulmany_id, h.rowid', (ig,)).fetchall()
    except sqlite3.OperationalError:
        return [], []
    belul = {}
    kivul = {}
    for tid, hor, cim, fok, ref, tb in hiv:
        if tb:
            belul.setdefault(tid, []).append((hor, cim, fok, ref))
        else:
            kivul.setdefault(tid, []).append((hor, cim, ref))
    tart_ids = {t[0] for t in tart}
    tartalmazo = [(tid, tip, cim, tt, so, belul.get(tid, [])) for tid, tip, cim, tt, so in tart]
    hivatkozo = []
    for tid, lista in kivul.items():
        if tid in tart_ids:
            continue
        t = tanulmany_van(con, tid)
        if t:
            hivatkozo.append((t[0], t[1], t[2], t[3], lista))
    hivatkozo.sort(key=lambda x: (0 if x[1] == 'bovitett' else 1, x[0]))
    return tartalmazo, hivatkozo


def tanulmany_sav(con, kk, fej):
    """A fejezetlap margójeléhez: {vers_szam: [(tanulmany_id, tipus, tartomany, folytatas)]}. `folytatas`: a tartomány a fejezet elején
    már tart (a jel a fejezet első verse előtt áll); különben a tartomány első verse előtt."""
    try:
        ho = con.execute('SELECT MIN(sorrend), MAX(sorrend) FROM vers WHERE konyv=? AND fejezet=?', (kk, fej)).fetchone()
        if not ho or ho[0] is None:
            return {}
        sor = con.execute(
            'SELECT r.tanulmany_id, t.tipus, t.tartomany, r.kezdo_sorrend FROM tanulmany_tartomany r JOIN tanulmany t ON t.tanulmany_id=r.tanulmany_id '
            'WHERE r.kezdo_sorrend<=? AND r.veg_sorrend>=? ORDER BY r.kezdo_sorrend, t.sorrend, r.resz', (ho[1], ho[0])).fetchall()
        vers_sorr = dict(con.execute('SELECT sorrend, vers FROM vers WHERE konyv=? AND fejezet=?', (kk, fej)).fetchall())
    except sqlite3.OperationalError:
        return {}
    ki = {}
    for tid, tip, tt, kez in sor:
        folyt = kez < ho[0]
        vers = vers_sorr.get(ho[0] if folyt else kez)
        if vers is not None:
            ki.setdefault(vers, []).append((tid, tip, tt, folyt))
    return ki


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


_VJ_OSZLOPOK = ('sorszam', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz', 'resz', 'utvonal', 'okkod', 'szurt')


def _sorok_dict(cur):
    """[dict] a lekérdezés soraiból, a kurzor oszlopneveivel (szövegként; a NULL üres)."""
    oszl = [d[0] for d in cur.description]
    return [dict(zip(oszl, ['' if x is None else str(x) for x in r])) for r in cur.fetchall()]


def bdb_szakasz_sorok(con, s):
    """F33 (F182): a BDB-szócikk szakasztáblájának sorai (`adat/bdb_szakaszok.tsv`, SEMA 2.30) — a tagolás egyetlen forrása
    (`bdb_tagolas`). None, ha a tábla hiányzik (régebbi adatbázis)."""
    try:
        return _sorok_dict(con.execute('SELECT * FROM bdb_szakaszok WHERE strong=?', (s,)))
    except sqlite3.OperationalError:
        return None


def bdb_szakasz_hu_sorok(con, s):
    """F33 (F182): a szakasztábla magyar bontása (`adat/bdb_szakasz_hu.tsv`, SEMA 2.32): {sorszám: sor}. None, ha hiányzik."""
    try:
        sorok = _sorok_dict(con.execute('SELECT * FROM bdb_szakasz_hu WHERE strong=?', (s,)))
    except sqlite3.OperationalError:
        return None
    return {r['sorszam']: r for r in sorok}


def bdb_vers_jelentes(con, s):
    """F104: a BDB-szócikk igehely-hivatkozásai jelentésponttal (`adat/bdb_vers_jelentes.tsv`, SEMA 2.29), a szócikkön belüli
    sorrendben: [dict] a `_VJ_OSZLOPOK` mezőivel, és ha a tábla már hordozza (F103), a `csoport`-tal (különben ''). A `s` a
    BDB-sor kulcsa (alias esetén a tábla-Strong). None, ha a tábla hiányzik (régebbi adatbázis): a hívó a gépi számra esik vissza."""
    try:
        oszl = {r[1] for r in con.execute('PRAGMA table_info(bdb_vers_jelentes)')}
        if not oszl:
            return None
        cs = ', csoport' if 'csoport' in oszl else ", ''"
        sorok = con.execute('SELECT %s%s FROM bdb_vers_jelentes WHERE strong=? ORDER BY CAST(sorszam AS INTEGER)'
                            % (', '.join(_VJ_OSZLOPOK), cs), (s,)).fetchall()
    except sqlite3.OperationalError:
        return None
    return [dict(zip(_VJ_OSZLOPOK + ('csoport',), ['' if x is None else str(x) for x in r])) for r in sorok]


def igetorzs_nevek(con):
    """{(nyelv, kód): az igetörzs forrásneve} a `morf_kulcs_heber` `igetorzs` soraiból (OSHB-kód → „qal”, „piel”, „peal” …);
    a BDB-szócikk törzsfejével (Qal, Pi'el, Pe'al) a `blokkok._torzs_kulcs` normalizálásával vethető össze."""
    try:
        return {(ny, k): f for ny, k, f in con.execute(
            "SELECT nyelv, kod, jelentes_forras FROM morf_kulcs_heber WHERE pozicio='igetorzs'")}
    except sqlite3.OperationalError:
        return {}


def tbesh_lemma(con, s):
    """(lemma, STEP-átírás) a TBESH-ből, vagy None: pontos Strong, majd a betűutótagos első sor (H2416 → H2416a), mint a
    lexikon-generátor `tbesg_tbesh_index`-e. A BDB-rövidítés címszó-feloldásához (N-F131x). Hiányzó tábla (licenc) → None."""
    try:
        r = (con.execute('SELECT szo, atiras FROM tbesh WHERE strong=? ORDER BY rowid LIMIT 1', (s,)).fetchone()
             or con.execute("SELECT szo, atiras FROM tbesh WHERE strong GLOB ? || '[a-zA-Z]' ORDER BY rowid LIMIT 1", (s,)).fetchone())
    except sqlite3.OperationalError:
        return None
    return (r[0], r[1]) if r and r[0] else None


_OSSZEFUZO = []


def _osszefuzo():
    """A közös összefűző (F128, DT-F128a (a), DT-F128g (a)): `eszkozok/bdb_jelolt/szakasz_bemenet.py` `strong_magyar_sorok`,
    fájlútvonalról betöltve (a `bdb_jelolt` könyvtár nem kerül a `sys.path`-ra; az összefűző csak stdlib-et használ)."""
    if not _OSSZEFUZO:
        import importlib.util
        import os
        ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bdb_jelolt', 'szakasz_bemenet.py')
        spec = importlib.util.spec_from_file_location('szakasz_bemenet_olvaso', ut)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _OSSZEFUZO.append(m.strong_magyar_sorok)
    return _OSSZEFUZO[0]


def _bdb_magyar_sorok(con, s):
    """A Strong BDB-sorai a táblasorrendben, a közös összefűzőn át: (szöveg, 'szakasz' | 'teljes' | None, a felhasznált sorok).
    A szakaszonként fordított Strong (`jelentes_szam = sz<sorszam>`) szövege a szakaszsorok összefűzése; a többié a `teljes`
    sor (a jóváhagyott `kezi` sor elsőbbségével, DT-F128f (3))."""
    nevek = ('jelentes_szam', 'mezo', 'forditas_hu', 'allapot', 'modell', 'datum')
    sorok = [dict(zip(nevek, r)) for r in con.execute(
        "SELECT jelentes_szam, mezo, forditas_hu, allapot, modell, datum FROM forditasok WHERE szotar='BDB' AND strong=? "
        "ORDER BY rowid", (s,))]
    return _osszefuzo()(sorok)


def bdb_magyar(con, s):
    szoveg, _, _ = _bdb_magyar_sorok(con, s)
    return szoveg.replace('\\n', '\n') if szoveg else None


def bdb_magyar_meta(con, s):
    """A magyar BDB-szócikk fordítás-jelölése: „modell, dátum” (a `forditasok.modell`, `.datum`; ugyanazok a sorok, amelyeket
    `bdb_magyar` összefűz: szakaszsoroknál a modellek az első előfordulás sorrendjében „ / ”-lel, a legkésőbbi dátum)."""
    _, _, hasznalt = _bdb_magyar_sorok(con, s)
    if not hasznalt:
        return None
    modellek = []
    for r in hasznalt:
        if r['modell'] not in modellek:
            modellek.append(r['modell'])
    return '%s, %s' % (' / '.join(str(m) for m in modellek), max(str(r['datum']) for r in hasznalt))


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


def thayer_javitas(szoveg, javitasok):
    """A `thayer_forras_javitas` `javitva` soraival (`elotte`, `javitott_alak`) kiegészített szöveg (F215). A `Thayer_teljes.tsv` 15
    Strongban egy-egy összefüggő szövegrészt elveszít (F132, M1); a beszúrás helye az `elotte` (a sor szövegének a lyuk előtti 20
    karaktere), amely a teljes szócikkben pontosan egyszer áll: ha nem így van, hiba (néma elcsúszás helyett). Az alkalmazás
    gépi azonossága a magyar ággal: `thayer_bemenet.javitott_szoveg` ugyanezt az `elotte` + `javitott_alak` párt használja."""
    for elotte, alak in javitasok:
        if szoveg.count(elotte) != 1:
            raise ValueError('Thayer-javítás: az `elotte` (%r) %d helyen áll a szövegben, nem egyen' % (elotte, szoveg.count(elotte)))
        p = szoveg.index(elotte) + len(elotte)
        szoveg = szoveg[:p] + alak + szoveg[p:]
    return szoveg


def thayer(con, g):
    """A Thayer-szócikk angol szövege a `thayer_forras_javitas` beszúrásaival (F215; a nyers `teljes_szocikk` 15 Strongban szöveget
    veszít). A javítótábla a DB-ben áll (az építő viszi át), a régi/teszt-DB-ben nincs: ott a nyers szöveg."""
    r = con.execute('SELECT teljes_szocikk FROM thayer WHERE strong=?', (g,)).fetchone()
    if not r:
        return None
    try:
        jav = con.execute("SELECT elotte, javitott_alak FROM thayer_forras_javitas WHERE strong=? AND allapot='javitva' "
                          "ORDER BY CAST(sorszam AS INTEGER), CAST(sor_poz AS INTEGER) DESC", (g,)).fetchall()
    except sqlite3.OperationalError:
        return r[0]
    return thayer_javitas(r[0], jav) if jav else r[0]


def magyar_gorog(con, g):
    """[(szotar, jelentes_szam, forditas_hu, mezo)] a Thayer és az UBS DNTG magyar fordításai (a `mezo` különbözteti meg
    az UBS-sorok `definicio_hu` és `glosszak_hu` változatát; F121, DT393). F187 (N-F186g): csak az érvényes sorok — az
    `elavult` sor és az összevonási tagsor (`sz<n>~<m>`, SEMA 2.14, mindig `elavult`) nem."""
    oszl = {r[1] for r in con.execute('PRAGMA table_info(forditasok)')}
    allapot = " AND COALESCE(allapot, '') <> 'elavult'" if 'allapot' in oszl else ''    # régi/teszt-tábla: nincs állapot
    return con.execute("SELECT szotar, jelentes_szam, forditas_hu, mezo FROM forditasok WHERE szotar IN ('Thayer','UBS_DNTG') "
                       "AND strong=? AND forditas_hu <> ''%s AND jelentes_szam NOT LIKE '%%~%%' ORDER BY rowid" % allapot,
                       (g,)).fetchall()


def thayer_szakasz_sorok(con, g):
    """F187: [(sorszam, utvonal, jel)] a Thayer-szakasztáblából (`adat/thayer_szakaszok.tsv`, SEMA 2.34), sorszám szerint, a
    `cim` sor nélkül; [], ha a tábla hiányzik (régebbi adatbázis)."""
    try:
        return [(str(s), u or '', j or '') for s, u, j in con.execute(
            "SELECT sorszam, utvonal, jel FROM thayer_szakaszok WHERE strong=? AND utvonal <> 'cim' "
            "ORDER BY CAST(sorszam AS INTEGER)", (g,))]
    except sqlite3.OperationalError:
        return []


def glossza_heber_hu(con, s):
    """F213 (DT-F213a): a TBESH-glossza magyar fordításának fő sora (`glosszak_heber_hu`, SEMA 2.39, `fo=igen`): (magyar, angol)
    vagy None (nincs sor, vagy a tábla hiányzik)."""
    try:
        r = con.execute("SELECT glossza_hu, glossza_en FROM glosszak_heber_hu WHERE strong=? AND fo='igen' AND glossza_hu <> '' "
                        "ORDER BY rowid LIMIT 1", (s,)).fetchone()
    except sqlite3.OperationalError:
        return None
    return (r[0], r[1] or '') if r else None


def glossza_gorog_hu(con, g):
    """F213 (DT-F213a): a TBESG rövid glosszájának magyar fordítása (`forditasok`, `szotar='TBESG'`, `mezo='glosszak_hu'`),
    az elavult sor nélkül; '' ha nincs."""
    oszl = {r[1] for r in con.execute('PRAGMA table_info(forditasok)')}
    allapot = " AND COALESCE(allapot, '') <> 'elavult'" if 'allapot' in oszl else ''
    sql = "SELECT forditas_hu FROM forditasok WHERE szotar='TBESG' AND mezo='glosszak_hu' AND strong=? AND forditas_hu <> ''" + allapot + \
        " ORDER BY rowid LIMIT 1"
    r = con.execute(sql, (g,)).fetchone()
    return r[0] if r else ''


def bdb_cimkek(con, s):
    """F213: {utvonal: cimke_hu} a BDB jóváhagyott szakaszcímkéiből (`adat/szotar_szakasz_cimke.tsv`, SEMA 2.40); {}, ha nincs."""
    try:
        return {sz: c for sz, c in con.execute(
            "SELECT szakasz, cimke_hu FROM szotar_szakasz_cimke WHERE szotar='BDB' AND strong=? AND cimke_hu <> ''", (s,))}
    except sqlite3.OperationalError:
        return {}


def lxx_par_szo(con, s):
    """F213: {Károli-vers: [görög Strong]} a héber szó szószintű LXX-párjai (Macula, `token_macula.lxx_strong`); a pár nélküli
    token üres szövegként áll. {} ha a tábla hiányzik."""
    ki = defaultdict(list)
    try:
        for ig, g in con.execute('SELECT igehely, lxx_strong FROM token_macula WHERE strong=? ORDER BY igehely, sorszam', (s,)):
            ki[ig].append(g or '')
    except sqlite3.OperationalError:
        return {}
    return dict(ki)


def motivum_helyek_szo(con, s):
    """F213: a szó motívumai: {motívum-id: (a szó saját motívumsorainak igehelyei, a motívum összes igehelye)} (`elofordulasok`);
    az igehely a tábla kulcsa (tartomány is lehet: „Sof 1:2-3”)."""
    try:
        sajat = defaultdict(set)
        for m, ig in con.execute('SELECT id, igehely FROM elofordulasok WHERE strong=?', (s,)):
            sajat[m].add(ig)
        if not sajat:
            return {}
        osszes = defaultdict(set)
        for m, ig in _in(con, 'SELECT id, igehely FROM elofordulasok WHERE id IN ', '', list(sajat)):
            osszes[m].add(ig)
    except sqlite3.OperationalError:
        return {}
    return {m: (sajat[m], osszes[m]) for m in sorted(sajat)}


def ubs_dbh_hu(con, s):
    """F213: {(lexid, mező): magyar} a héber Strong UBS DBH-jelentéseinek magyar fordítása (`forditasok`, `szotar='UBS_DBH'`)."""
    return {(e, m): f for e, m, f in con.execute(
        "SELECT entry_id, mezo, forditas_hu FROM forditasok WHERE szotar='UBS_DBH' AND strong=? AND forditas_hu <> ''", (s,))}


def forditas_bejegyzesek(con, szotar, entryk):
    """F213 (bekötési audit): egy szótár magyar fordításai a `forditasok`-ból a bejegyzések szerint (a Thayer-minta, `magyar_gorog`:
    az elavult sor és az összevonási tagsor nélkül): {(entry_id, jelentes_szam, mezo): magyar}. A bejegyzés a szótár saját kulcsa
    (TBESG/LSJ/TBESH: a Strong; SDBH/SDGNT: a doménkód; tW: a tW-azonosító), így a fordítás minden szónál megjelenik, amelyik
    ugyanazt a bejegyzést mutatja."""
    entryk = sorted({x for x in entryk if x})
    if not entryk:
        return {}
    oszl = {r[1] for r in con.execute('PRAGMA table_info(forditasok)')}
    allapot = " AND COALESCE(allapot, '') <> 'elavult'" if 'allapot' in oszl else ''
    ki = {}
    sql = ("SELECT entry_id, jelentes_szam, mezo, forditas_hu FROM forditasok WHERE szotar=? AND forditas_hu <> ''" + allapot +
           " AND COALESCE(jelentes_szam, '') NOT LIKE '%~%' AND entry_id IN ")
    for e, j, m, f in _in(con, sql, ' ORDER BY rowid', entryk, (szotar,)):
        ki.setdefault((e, j or '', m), f)
    return ki


def glosszak_heber_hu_angol(con, s):
    """F213: {angol glossza: magyar} a héber Strong TBESH-glosszáinak fordítása (`glosszak_heber_hu`, minden sor, nem csak a fő)."""
    try:
        return {en: hu for en, hu in con.execute(
            "SELECT glossza_en, glossza_hu FROM glosszak_heber_hu WHERE strong=? AND glossza_hu <> '' ORDER BY rowid", (s,)) if en}
    except sqlite3.OperationalError:
        return {}


def nave_tema_hu(con, tema_idk):
    """F213: {(tema_id, angol cím vagy ''): magyar} a Nave-témák magyar nevei (`nave_tema_hu`; a téma sora üres `cimke_en`-nel)."""
    try:
        return {(t, c or ''): m for t, c, m in _in(con, "SELECT tema_id, cimke_en, magyar FROM nave_tema_hu WHERE magyar <> '' AND tema_id IN ",
                                                  '', sorted({str(x) for x in tema_idk if x}))}
    except sqlite3.OperationalError:
        return {}


def thayer_cimkek(con, g):
    """F187: {utvonal: cimke_hu} a jóváhagyott szakaszcímkékből (`adat/szotar_szakasz_cimke.tsv`, Thayer); {}, ha a tábla
    hiányzik."""
    try:
        return {sz: c for sz, c in con.execute(
            "SELECT szakasz, cimke_hu FROM szotar_szakasz_cimke WHERE szotar='Thayer' AND strong=? AND cimke_hu <> ''", (g,))}
    except sqlite3.OperationalError:
        return {}


def thayer_vers_pontok(con, g, karoli_vers):
    """F187: a Thayer vers -> jelentéspont tábla (`adat/thayer_vers_jelentes.tsv`, SEMA 2.35) sorai egy versre:
    [(szakasz, utvonal)]; None, ha a tábla hiányzik."""
    try:
        return [(str(sz), u or '') for sz, u in con.execute(
            'SELECT szakasz, utvonal FROM thayer_vers_jelentes WHERE strong=? AND karoli_vers=? ORDER BY CAST(sorszam AS INTEGER)',
            (g, karoli_vers))]
    except sqlite3.OperationalError:
        return None


def ubs_dbh_szo(con, h):
    """[(lexid, domen, definicio_en, glosszak_en, definicio_hu, glosszak_hu)] a héber Strong összes UBS DBH-jelentése
    (F121, DT393): az angol az `ubs_dbh_jelentesek`-ből (lexidenként az első sor), a magyar a `forditasok`-ból
    (`szotar='UBS_DBH'`, `entry_id` = lexid); ahol nincs magyar, az érték üres."""
    hu = {(e, m): f for e, m, f in con.execute(
        "SELECT entry_id, mezo, forditas_hu FROM forditasok WHERE szotar='UBS_DBH' AND strong=? AND forditas_hu <> ''", (h,))}
    ki, lat = [], set()
    for lex, dom, df, gl in con.execute('SELECT lexid, domen, definicio_rovid, glosszak FROM ubs_dbh_jelentesek WHERE strong=? ORDER BY lexid, rowid', (h,)):   # lexidenként az első sor = a fájlsorrend szerinti (ez a hash forrása is)
        if lex in lat:
            continue
        lat.add(lex)
        ki.append((lex, dom, df, gl, hu.get((lex, 'definicio_hu'), ''), hu.get((lex, 'glosszak_hu'), '')))
    return ki


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


# ---------------------------------------------------------------------------------------------------------------------
# keresés (M3, M0 3.6): a lekérdezések paraméteresek; a frázis-sablonok szövege CSAK a szavak számától (2–4) függ, a bemenettől nem.
# A keresés logikája (normalizálás, illesztés, lapozás) a `kereses.py`-ban áll; itt csak SQL van.
# ---------------------------------------------------------------------------------------------------------------------
def vers_adatok(con, igehelyek):
    """{igehely: (sorrend, karoli_szoveg)}"""
    return {ig: (s, t) for ig, s, t in _in(con, 'SELECT igehely, sorrend, karoli_szoveg FROM vers WHERE igehely IN ', '', igehelyek)}


def hu_tokenek_versekre(con, igehelyek):
    """{igehely: [(sorszam, szo), ...]} sorszám szerint (a találati sor kiemeléséhez)."""
    ki = defaultdict(list)
    for ig, sz, szo in _in(con, "SELECT igehely, sorszam, szo FROM token_karoli WHERE oldal='hu' AND igehely IN ", '', igehelyek):
        ki[ig].append((sz, szo))
    for v in ki.values():
        v.sort()
    return ki


def er_tokenek_versekre(con, igehelyek):
    """{igehely: [(sorszam, szo_kis, szo), ...]} sorszám szerint (a héber frázis illesztéséhez)."""
    ki = defaultdict(list)
    for ig, sz, kis, szo in _in(con, "SELECT igehely, sorszam, szo_kis, szo FROM token_karoli WHERE oldal='er' AND igehely IN ", '', igehelyek):
        ki[ig].append((sz, kis or '', szo))
    for v in ki.values():
        v.sort()
    return ki


def par_versekre(con, igehelyek):
    """[(igehely, hu_sorszam, er_sorszam, strong)] a versek Károli–Strong párjai (a kiemeléshez)."""
    return _in(con, 'SELECT igehely, hu_sorszam, er_sorszam, strong FROM token_par WHERE igehely IN ', '', igehelyek)


def vers_sorrendek(con):
    """{igehely: sorrend} a teljes `vers` táblára (egyszer töltődik be; a keresés ezzel rendez, a tokenenkénti `vers`-illesztés helyett)."""
    return {ig: s for ig, s in con.execute('SELECT igehely, sorrend FROM vers')}


def kereses_strong_versek(con, s):
    """{igehely} a versek, amelyekben a Strong-szám előfordul (TAHOT/TAGNT, `token_strong`)."""
    return {r[0] for r in con.execute('SELECT DISTINCT igehely FROM token_strong WHERE strong=?', (s,))}


def kereses_strong_db(con, s):
    return con.execute('SELECT COUNT(*) FROM token_strong WHERE strong=?', (s,)).fetchone()[0]


def kereses_strong_alakok(con, s, n=12):
    """[(hu_szo_kis, db)] a Strong-számhoz párosított Károli-alakok (modell-kimenet: `token_par`), a leggyakoribbak."""
    return con.execute('SELECT hu_szo_kis, COUNT(*) FROM token_par WHERE strong=? GROUP BY hu_szo_kis ORDER BY 2 DESC, 1 LIMIT ?', (s, n)).fetchall()


def kereses_hu_szo_kis(con, kis):
    """[(igehely, sorszam)] a magyar tokenek, amelyek `szo_kis`-e a megadott (pontos alak, kis/nagybetű-független); fedő index (`ix_token_karoli_2`)."""
    return con.execute("SELECT igehely, sorszam FROM token_karoli WHERE szo_kis=? AND oldal='hu'", (kis,)).fetchall()


def kereses_hu_alakok(con, alakok):
    """[(igehely, sorszam, szo)] a magyar tokenek, amelyek `szo`-ja (pontosan, kis/nagybetű-érzékenyen) a listában van (F95 kulcs)."""
    return _in(con, "SELECT igehely, sorszam, szo FROM token_karoli WHERE oldal='hu' AND szo IN ", '', alakok)


def kereses_kotojeles(con, alakok):
    """[(igehely, sorszam, alak)] a kötőjeles alakok darab-tokenjei (`szotari_token_kotojeles`, F95)."""
    return _in(con, 'SELECT igehely, sorszam, alak FROM szotari_token_kotojeles WHERE alak IN ', '', alakok)


def szotari_kereso(con, keresoalak):
    """[(alak, mezok)] a keresőalakhoz (NFC kisbetűs szótári/mai/alapige/további alak) tartozó Károli-alakok."""
    return con.execute('SELECT alak, mezok FROM szotari_kereso WHERE keresoalak=? ORDER BY alak', (keresoalak,)).fetchall()


def szotari_alak_alakra(con, alak):
    """(szotari_alak, szotari_alak_mai) az alakra (pontos, kis/nagybetű-érzékeny), vagy None."""
    return con.execute('SELECT szotari_alak, szotari_alak_mai FROM szotari_alak WHERE alak=?', (alak,)).fetchone()


def kereses_szo_strongjai(con, kis, n=12):
    """[(strong, db)] a magyar alak (`hu_szo_kis`) párosított Strong-számai (ADATVAGYON 4. szakasz 2. pont; modell-kimenet)."""
    return con.execute('SELECT strong, COUNT(*) FROM token_par WHERE hu_szo_kis=? GROUP BY strong ORDER BY 2 DESC, 1 LIMIT ?', (kis, n)).fetchall()


def kereses_tokenek_strongjai(con, tokenek):
    """Counter{strong: db}: a megadott (igehely, hu_sorszam) tokenek `token_par`-beli Strong-számai, a nyelvtaniak (`grammatikai_strongok`)
    nélkül (a (c) mód Strong-ága, F95 M0 6. szakasz). A tokeneket versenként kérdezi le."""
    versek = defaultdict(set)
    for ig, sz in tokenek:
        versek[ig].add(sz)
    nyt = {r[0] for r in con.execute('SELECT strong FROM grammatikai_strongok')}
    c = Counter()
    for ig, hs, st in _in(con, 'SELECT igehely, hu_sorszam, strong FROM token_par WHERE igehely IN ', '', list(versek)):
        if hs in versek[ig] and st not in nyt:
            c[st] += 1
    return c


def kereses_par_strong_tokenek(con, strongok):
    """[(igehely, hu_sorszam)] a magyar tokenek, amelyek a `token_par`-ban a Strong-számok egyikével párosítottak."""
    return _in(con, 'SELECT igehely, hu_sorszam FROM token_par WHERE strong IN ', '', strongok)


def _frazis_sql(n):
    """Az n szavas (2–4) önillesztés szövege: a `token_karoli` egymást követő `sorszam`-ú, azonos `igehely`-ű és `oldal`-ú tokenjei.
    A szöveg csak n-től függ (fix sablon); a szavak paraméterek."""
    alias = 'abcd'[:n]
    sql = 'SELECT a.igehely, a.sorszam FROM token_karoli a'
    for i in range(1, n):
        x = alias[i]
        sql += ' JOIN token_karoli %s ON %s.szo_kis=? AND %s.igehely=a.igehely AND %s.oldal=a.oldal AND %s.sorszam=a.sorszam+%d' % (x, x, x, x, x, i)
    return sql + ' WHERE a.szo_kis=? AND a.oldal=?'


FRAZIS_SQL = {n: _frazis_sql(n) for n in (2, 3, 4)}


def kereses_frazis(con, szavak, oldal='hu'):
    """[(igehely, elso_sorszam)] a 2–4 szavas frázis (pontos `szo_kis` egyezés, egymást követő szavak egy versen belül)."""
    if len(szavak) not in FRAZIS_SQL or oldal not in ('hu', 'er'):
        raise ValueError('a frázis 2–4 szó')
    return con.execute(FRAZIS_SQL[len(szavak)], tuple(szavak[1:]) + (szavak[0], oldal)).fetchall()


def kereses_er_db(con, kisek):
    """A héber tokenek száma, amelyek `szo_kis`-e a listában van (a legritkább frázisszó kiválasztásához)."""
    return sum(r[0] for r in _in(con, "SELECT COUNT(*) FROM token_karoli WHERE oldal='er' AND szo_kis IN ", '', kisek))


def kereses_er_versek(con, kisek):
    """{igehely} a versek, amelyekben a héber `szo_kis` a listában van."""
    return {r[0] for r in _in(con, "SELECT DISTINCT igehely FROM token_karoli WHERE oldal='er' AND szo_kis IN ", '', kisek)}


def kereses_er_tokenek(con, kis):
    """[(igehely, sorszam)] a héber tokenek, amelyek `szo_kis`-e a megadott (fedő index, `ix_token_karoli_2`)."""
    return con.execute("SELECT igehely, sorszam FROM token_karoli WHERE szo_kis=? AND oldal='er' ORDER BY igehely, sorszam", (kis,)).fetchall()


# ---------------------------------------------------------------------------------------------------------------------
# F210: a bibliaválasztó szövegei (a Károli 1908 a `vers`/`token_karoli`-ból; a többi az itteni lekérdezésekkel)
# ---------------------------------------------------------------------------------------------------------------------
def biblia_fejezetek_karoli_kulcs(con, tabla):
    """{kk: [fejezet, ...]} a Károli-kulcsos szövegtáblára: a Károli-fejezetek, amelyekben a táblának van sora. A `tabla`
    a hívó rögzített listájából jön (`bibliak.py`), nem a kérésből."""
    sql = {
        'szoveg_modern': 'SELECT DISTINCT v.konyv, v.fejezet FROM szoveg_modern t JOIN vers v ON v.igehely=t.igehely',
        'szoveg_kjv': 'SELECT DISTINCT v.konyv, v.fejezet FROM szoveg_kjv t JOIN vers v ON v.igehely=t.igehely',
        'bsb': 'SELECT DISTINCT v.konyv, v.fejezet FROM bsb t JOIN vers v ON v.igehely=t.igehely',
        'lxx_token': 'SELECT DISTINCT v.konyv, v.fejezet FROM vers v WHERE EXISTS (SELECT 1 FROM lxx_token t WHERE t.karoli_igehely=v.igehely)',
        'token_eredeti:H': "SELECT DISTINCT v.konyv, v.fejezet FROM vers v WHERE EXISTS (SELECT 1 FROM token_eredeti t WHERE t.igehely=v.igehely AND t.nyelv='H')",
        'token_eredeti:G': "SELECT DISTINCT v.konyv, v.fejezet FROM vers v WHERE EXISTS (SELECT 1 FROM token_eredeti t WHERE t.igehely=v.igehely AND t.nyelv='G')",
    }[tabla]
    ki = defaultdict(list)
    for kk, f in con.execute(sql + ' ORDER BY v.sorrend'):
        if f not in ki[kk]:
            ki[kk].append(f)
    return {kk: sorted(fl) for kk, fl in ki.items()}


def modern_fejezet(con, kk, fej):
    """({igehely: modern versszöveg}, {igehely: [(sorszam, alak)]}) a modernizált Károli fejezetére."""
    szoveg = dict(con.execute('SELECT t.igehely, t.szoveg FROM szoveg_modern t JOIN vers v ON v.igehely=t.igehely WHERE v.konyv=? AND v.fejezet=?', (kk, fej)))
    tok = defaultdict(list)
    for ig, sz, alak in con.execute('SELECT t.igehely, t.sorszam, t.alak FROM token_modern t JOIN vers v ON v.igehely=t.igehely '
                                    'WHERE v.konyv=? AND v.fejezet=? ORDER BY v.vers, t.sorszam', (kk, fej)):
        tok[ig].append((sz, alak))
    return szoveg, tok


def eredeti_fejezet(con, kk, fej, nyelv):
    """{igehely: [(sorszam, alak, strong_lanc)]} a TAHOT (`H`) vagy a TAGNT (`G`) tokenjei a Károli-fejezetre."""
    ki = defaultdict(list)
    for ig, sz, alak, st in con.execute('SELECT t.igehely, t.sorszam, t.alak, t.strong_lanc FROM token_eredeti t JOIN vers v ON v.igehely=t.igehely '
                                        'WHERE v.konyv=? AND v.fejezet=? AND t.nyelv=? ORDER BY v.vers, t.sorszam', (kk, fej, nyelv)):
        ki[ig].append((sz, alak or '', st or ''))
    return ki


def lxx_fejezet(con, kk, fej):
    """{igehely: [(szovegforma, lxx_igehely, szoalak, strong)]} a Septuaginta tokenjei a Károli-fejezet verseire (a szövegbeli
    sorrendben); a Károli-vers nélküli LXX-szakasz nincs benne."""
    ki = defaultdict(list)
    for ig, forma, lxx_ig, szo, st in con.execute(
            'SELECT t.karoli_igehely, t.szovegforma, t.lxx_igehely, t.szoalak, t.strong FROM lxx_token t JOIN vers v ON v.igehely=t.karoli_igehely '
            'WHERE v.konyv=? AND v.fejezet=? ORDER BY v.vers, t.szovegforma, CAST(t.pozicio AS INTEGER), t.rowid', (kk, fej)):
        ki[ig].append((forma or '', lxx_ig or '', szo or '', st or ''))
    return ki


def kjv_fejezet(con, kk, fej):
    """({igehely: [(step_nyers, szoveg)]}, {igehely: [(angol_szo, strong)]}) a KJV fejezetére (Károli-kulcs): a teljes szöveg és a
    Strong-címkés szavak (a `kjv` tábla; a kiadás kizárhatja, ilyenkor a KJV nem választható, bibliak.Tar.van)."""
    szoveg = defaultdict(list)
    for ig, step, sz in con.execute('SELECT t.igehely, t.step_nyers, t.szoveg FROM szoveg_kjv t JOIN vers v ON v.igehely=t.igehely '
                                    'WHERE v.konyv=? AND v.fejezet=? ORDER BY v.vers, t.sorrend', (kk, fej)):
        szoveg[ig].append((step or '', sz or ''))
    cimke = defaultdict(list)
    for ig, szo, st in con.execute('SELECT t.igehely, t.angol_szo, t.strong FROM kjv t JOIN vers v ON v.igehely=t.igehely '
                                   'WHERE v.konyv=? AND v.fejezet=? ORDER BY v.vers, t.sorszam', (kk, fej)):
        cimke[ig].append((szo or '', st or ''))
    return szoveg, cimke


def bsb_fejezet(con, kk, fej):
    """{igehely: [(angol_szo, strong)]} a BSB fejezetére (Károli-kulcs), az angol szórendben; az elhagyott (üres) szó nélkül."""
    ki = defaultdict(list)
    for ig, szo, st in con.execute("SELECT t.igehely, t.angol_szo, t.strong FROM bsb t JOIN vers v ON v.igehely=t.igehely "
                                   "WHERE v.konyv=? AND v.fejezet=? AND t.angol_szo<>'' ORDER BY v.vers, t.sorszam", (kk, fej)):
        ki[ig].append((szo, st or ''))
    return ki
