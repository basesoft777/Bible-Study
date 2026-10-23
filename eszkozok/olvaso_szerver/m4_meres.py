"""#76 M4: lapidő-mérés a VPS-t utánzó korlátokkal (1 vCPU, 2 GB RAM), a WSL `pardes` disztribúcióban.

Mit csinál:
  1. a gunicornt (a `gunicorn_conf.py` szerint: gthread, 1 worker, 4 szál) egy `systemd-run --scope` egységben indítja:
     `AllowedCPUs=0`, `CPUQuota=100%`, `MemoryMax=2G`, `MemorySwapMax=0`; a szerver `basesoft` felhasználóként fut (`runuser`);
  2. igazolja, hogy a korlát hat: a scope cgroup-fájljai (cpuset, cpu.max, memory.max, memory.swap.max), a gunicorn-folyamatok
     `Cpus_allowed_list`-je, továbbá két próba ugyanilyen scope-ban: 4 párhuzamos CPU-terhelő folyamat összesített CPU-ideje
     (1 CPU-nál ≈ a falióra), és egy 2,5 GB-os foglalás (a 2 GB-os korlát miatt meg kell halnia), mellette egy 1,5 GB-os (át kell mennie);
  3. a lapokat HTTP-n kéri (új kapcsolat kérésenként), a mérő kliens a 1. CPU-n fut (a korláton kívül);
     „hideg”: minden kérés előtt `sync; echo 3 > /proc/sys/vm/drop_caches` (az OS lap-gyorsítótára üres) és a lap-LRU kikapcsolva;
     „meleg”: egy be nem számított bemelegítő kérés után 5 kérés, a lap-LRU kikapcsolva (minden kérés valódi lapelőállítás);
     „LRU”: az eredeti konfiggal (max_lap=512) a második kérés (a kész lap a szerver gyorsítótárából);
  4. kiírja a gép adatait, a korlát igazolását és a mediánt / p95-öt (legközelebbi rang) laptípusonként és keresésenként (JSON + markdown).

A lap-LRU kikapcsolása: a `konfig/` másolata a repón kívül (`/tmp/pardes_m4_konfig`), benne `max_lap = 0`; a repó konfigja nem változik.
Csak olvas: a `pardes.db` `mode=ro`; a repóba nem ír.

Futtatás (rootként, mert a scope és a drop_caches azt kívánja; jelszó nem kell: `wsl -d pardes -u root`):
    wsl -d pardes -u root -e /home/basesoft/pardes/eszkozok/olvaso_szerver/.venv/bin/python \
        /mnt/c/.../eszkozok/olvaso_szerver/m4_meres.py --kimenet /tmp/m4 [--gyors]
"""
import argparse
import datetime
import json
import math
import os
import platform
import random
import re
import shutil
import sqlite3
import statistics
import subprocess
import sys
import time
import http.client
from urllib.parse import quote, urlencode

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import lekerdezesek as q  # noqa: E402

FELHASZNALO = 'basesoft'
VENV = '/home/basesoft/pardes/eszkozok/olvaso_szerver/.venv'
TULAJDONSAGOK = ['-p', 'AllowedCPUs=0', '-p', 'CPUQuota=100%', '-p', 'MemoryMax=2G', '-p', 'MemorySwapMax=0']

KERESESEK = [
    # (ág, címke, paraméterek)
    ('strong', 'H0216', {'strong': 'H0216'}),
    ('strong', 'H0430 (gyakori)', {'strong': 'H0430'}),
    ('strong', 'H9002 (leggyakoribb)', {'strong': 'H9002'}),
    ('strong', 'G3056 (görög)', {'strong': 'G3056'}),
    ('strong', 'H1254 H0430 (két Strong)', {'strong': 'H1254 H0430'}),
    ('szo_pontos', 'világosság', {'szo': 'világosság', 'mod': 'pontos'}),
    ('szo_pontos', 'föld', {'szo': 'föld', 'mod': 'pontos'}),
    ('szo_pontos', 'Isten', {'szo': 'Isten', 'mod': 'pontos'}),
    ('szo_pontos', 'és', {'szo': 'és', 'mod': 'pontos'}),
    ('szo_alap', 'világosság', {'szo': 'világosság'}),
    ('szo_alap', 'föld', {'szo': 'föld'}),
    ('szo_alap', 'amely', {'szo': 'amely'}),
    ('szo_alap', 'mond', {'szo': 'mond'}),
    ('szo_alap', 'ő', {'szo': 'ő'}),
    ('szo_alap', 'és', {'szo': 'és'}),
    ('szo_c', 'világosság', {'szo': 'világosság', 'mod': 'szoto_strong'}),
    ('szo_c', 'föld', {'szo': 'föld', 'mod': 'szoto_strong'}),
    ('szo_c', 'ki (funkciószó)', {'szo': 'ki', 'mod': 'szoto_strong'}),
    ('frazis', 'a föld', {'frazis': 'a föld'}),
    ('frazis', 'kietlen és', {'frazis': 'kietlen és'}),
    ('frazis', 'és monda az úr', {'frazis': 'és monda az úr'}),
    ('heber', 'בראשית ברא', {'heber': 'בראשית ברא'}),
    ('heber', 'את השמים', {'heber': 'את השמים'}),
    ('heber', 'ויאמר אלהים', {'heber': 'ויאמר אלהים'}),
    ('heber', 'יהוה (1 szó)', {'heber': 'יהוה'}),
]
EXTRA_FEJEZETEK = [('Ézs', 53), ('Ján', 1), ('Róm', 8), ('Jel', 21), ('Zsolt', 119)]


def p95(xs):
    s = sorted(xs)
    return s[max(0, math.ceil(0.95 * len(s)) - 1)]


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)


def olvas(ut):
    try:
        with open(ut, encoding='utf-8') as f:
            return f.read().strip()
    except OSError as ex:
        return '(nem olvasható: %s)' % ex


# ---------------------------------------------------------------------------------------------------------------------
# gép, adatbázis
# ---------------------------------------------------------------------------------------------------------------------
def gep_adatai(db):
    cpu = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo', encoding='utf-8') if l.startswith('model name')), '?')
    mem = next((l.split()[1] for l in open('/proc/meminfo', encoding='utf-8') if l.startswith('MemTotal')), '?')
    con = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    meta = q.meta(con)                                   # minden SQL a lekerdezesek.py-ban (teszt_olvaso_szerver: TestSzabalyok)
    con.close()
    gunicorn = sh([VENV + '/bin/python', '-c', 'import importlib.metadata as m; print(m.version("gunicorn"), m.version("flask"))']).stdout.strip()
    return {'kernel': platform.release(), 'cpu': cpu, 'nproc_gazda': os.cpu_count(), 'memtotal_kb': int(mem), 'python_szerver': sh([VENV + '/bin/python', '-V']).stdout.strip(),
            'gunicorn_flask': gunicorn, 'sqlite': sqlite3.sqlite_version, 'db': db, 'db_bajt': os.path.getsize(db), 'epites_ts': meta.get('epites_ts'), 'db_mod': meta.get('mod'),
            'systemd': sh(['systemctl', '--version']).stdout.splitlines()[0], 'distro': olvas('/etc/os-release').splitlines()[0]}


def minta(db, seed, n_vers, n_zsolt, n_heber, n_gorog, n_fejezet):
    con = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    slug = {k: s for k, s, _, _ in q.konyvek(con)}
    r = random.Random(seed)
    v1 = [ig for f in range(1, 26) for ig, _, _ in q.fejezet_versek(con, '1Móz', f)]
    vz = [ig for ig, _, _ in q.fejezet_versek(con, 'Zsolt', 22)]
    versek = r.sample(v1, n_vers) + r.sample(vz, min(n_zsolt, len(vz)))
    nyelvtani = q.nyelvtani_strongok(con)
    heb, gor = set(), set()
    for ig in v1 + vz:
        heb.update(sn for sn, _, _ in q.heber_d2(con, ig) if sn and sn.startswith('H') and '+' not in sn)
        gor.update(w['strong'] for w in q.lxx_szavak(con, ig) if w['strong'].startswith('G') and '+' not in w['strong'] and ' ' not in w['strong'])
    heb, gor = sorted(heb - nyelvtani), sorted(gor)
    heb_m = ['H0430', 'H0216'] + r.sample([s for s in heb if s not in ('H0430', 'H0216')], n_heber - 2)
    gor_m = ['G2316'] + r.sample([s for s in gor if s != 'G2316'], n_gorog - 1)
    fej = sorted(r.sample(range(1, 26), n_fejezet))
    con.close()

    def vers_ut(ig):
        kk, fv = ig.rsplit(' ', 1)
        f, v = fv.split(':')
        return '/%s/%s/%s' % (quote(slug[kk]), f, v), '/r/vers/%s/%s/%s' % (quote(slug[kk]), f, v)

    vers_utak = [vers_ut(ig) for ig in versek]
    return {
        'vers': [(ig, u[0]) for ig, u in zip(versek, vers_utak)],
        'vers_toredek': [(ig, u[1]) for ig, u in zip(versek, vers_utak)],
        'szo_heber': [(s, '/szo/' + s) for s in heb_m],
        'szo_gorog': [(s, '/szo/' + s) for s in gor_m],
        'szo_toredek': [(s, '/r/szo/' + s) for s in heb_m[:10] + gor_m[:10]],
        'fejezet': [('1Móz %d' % f, '/%s/%d' % (slug['1Móz'], f)) for f in fej] + [('Zsolt 22', '/%s/22' % slug['Zsolt'])]
                   + [('%s %d' % (k, f), '/%s/%d' % (quote(slug[k]), f)) for k, f in EXTRA_FEJEZETEK],
        'keresesek': [(ag, cimke, '/kereses?' + urlencode(p)) for ag, cimke, p in KERESESEK],
        'populacio': {'1Móz 1–25 vers': len(v1), 'Zsolt 22 vers': len(vz), 'héber Strong (nem nyelvtani, lánc nélkül)': len(heb), 'görög LXX-Strong': len(gor)},
    }


# ---------------------------------------------------------------------------------------------------------------------
# szerver a korlátozott scope-ban
# ---------------------------------------------------------------------------------------------------------------------
class Szerver:
    def __init__(self, db, port, konfig_dir, egyseg, naplo):
        self.db, self.port, self.konfig_dir, self.egyseg, self.naplo = db, port, konfig_dir, egyseg, naplo
        self.p = None

    def indit(self):
        env = ['PARDES_DB=%s' % self.db, 'PARDES_BIND=127.0.0.1:%d' % self.port, 'PYTHONIOENCODING=utf-8', 'HOME=/home/%s' % FELHASZNALO]
        if self.konfig_dir:
            env.append('PARDES_KONFIG_DIR=%s' % self.konfig_dir)
        args = (['systemd-run', '--scope', '--quiet', '--unit=%s' % self.egyseg] + TULAJDONSAGOK
                + ['runuser', '-u', FELHASZNALO, '--', 'env'] + env + [VENV + '/bin/gunicorn', '-c', 'gunicorn_conf.py', 'alkalmazas:letrehoz()'])
        self.f = open(self.naplo, 'w', encoding='utf-8')
        self.p = subprocess.Popen(args, cwd=D, stdout=self.f, stderr=subprocess.STDOUT)
        t0 = time.monotonic()
        while time.monotonic() - t0 < 300:
            try:
                st, _, _ = keres(self.port, '/statusz', idokorlat=30)
                if st == 200:
                    return time.monotonic() - t0
            except OSError:
                pass
            if self.p.poll() is not None:
                raise RuntimeError('a szerver leállt indulás közben; napló: %s' % self.naplo)
            time.sleep(0.5)
        raise RuntimeError('a szerver 300 s alatt nem indult el')

    def cgroup(self):
        cg = sh(['systemctl', 'show', '%s.scope' % self.egyseg, '-p', 'ControlGroup', '--value']).stdout.strip()
        return '/sys/fs/cgroup' + cg

    def igazolas(self):
        cg = self.cgroup()
        procs = olvas(cg + '/cgroup.procs').split()
        folyamatok = []
        for pid in procs:
            cmd = olvas('/proc/%s/cmdline' % pid).replace('\0', ' ')[:90]
            st = olvas('/proc/%s/status' % pid)
            cal = next((l.split(':', 1)[1].strip() for l in st.splitlines() if l.startswith('Cpus_allowed_list')), '?')
            rss = next((l.split(':', 1)[1].strip() for l in st.splitlines() if l.startswith('VmRSS')), '?')
            uid = next((l.split()[1] for l in st.splitlines() if l.startswith('Uid')), '?')
            folyamatok.append({'pid': pid, 'cmd': cmd, 'Cpus_allowed_list': cal, 'VmRSS': rss, 'uid': uid})
        return {'cgroup': cg, 'cpuset.cpus.effective': olvas(cg + '/cpuset.cpus.effective'), 'cpu.max': olvas(cg + '/cpu.max'),
                'memory.max': olvas(cg + '/memory.max'), 'memory.swap.max': olvas(cg + '/memory.swap.max'), 'folyamatok': folyamatok}

    def memoria(self):
        cg = self.cgroup()
        return {'memory.current': olvas(cg + '/memory.current'), 'memory.peak': olvas(cg + '/memory.peak'),
                'memory.events': olvas(cg + '/memory.events').replace('\n', '; ')}

    def leallit(self):
        sh(['systemctl', 'stop', '%s.scope' % self.egyseg])
        if self.p:
            try:
                self.p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.p.kill()
        self.f.close()


PROBA_CPU = r'''
import os, time
t0 = time.time()
gy = []
for _ in range(4):
    pid = os.fork()
    if pid == 0:
        v = time.time() + 3.0
        x = 0
        while time.time() < v:
            x += 1
        os._exit(0)
    gy.append(pid)
for pid in gy:
    os.waitpid(pid, 0)
t = os.times()
print('fal=%.2f cpu_gyerekek=%.2f nproc=%d' % (time.time() - t0, t.children_user + t.children_system, len(os.sched_getaffinity(0))))
'''
PROBA_MEM = r'''
import sys
n = int(sys.argv[1])
b = bytearray(n)
for i in range(0, n, 4096):
    b[i] = 1
print('lefoglalva %d bajt' % n)
'''


def korlat_probak():
    ki = {}
    for nev, args in (('cpu_scope', ['systemd-run', '--scope', '--quiet'] + TULAJDONSAGOK + ['python3', '-c', PROBA_CPU]),
                      ('cpu_korlat_nelkul', ['taskset', '-c', '0-%d' % (os.cpu_count() - 1), 'python3', '-c', PROBA_CPU]),
                      ('mem_2_5G_scope', ['systemd-run', '--scope', '--quiet'] + TULAJDONSAGOK + ['python3', '-c', PROBA_MEM, str(2500 * 1024 * 1024)]),
                      ('mem_1_5G_scope', ['systemd-run', '--scope', '--quiet'] + TULAJDONSAGOK + ['python3', '-c', PROBA_MEM, str(1500 * 1024 * 1024)])):
        r = sh(args)
        ki[nev] = {'kilepes': r.returncode, 'kimenet': (r.stdout + r.stderr).strip()[-300:]}
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# kérés és mérés
# ---------------------------------------------------------------------------------------------------------------------
def keres(port, ut, idokorlat=120):
    t0 = time.perf_counter()
    c = http.client.HTTPConnection('127.0.0.1', port, timeout=idokorlat)
    c.request('GET', ut, headers={'Connection': 'close'})
    r = c.getresponse()
    body = r.read()
    ms = (time.perf_counter() - t0) * 1000
    xc = r.getheader('X-Cache', '')
    c.close()
    return r.status, ms, (xc, len(body))


def ures_cache():
    os.sync()
    with open('/proc/sys/vm/drop_caches', 'w') as f:
        f.write('3\n')


def retegges(ut, reteg):
    """A mérési cím a réteggel (#134: nézetek helyett rétegek; '' = réteg nélkül, a folyó szöveg)."""
    if not reteg:
        return ut
    return ut + ('&' if '?' in ut else '?') + 'reteg=' + reteg


def rbajt(cg):
    """A scope cgroup-jának összes olvasott bájtja (io.stat rbytes, minden eszközre)."""
    if not cg:
        return 0
    return sum(int(m) for m in re.findall(r'rbytes=(\d+)', olvas(cg + '/io.stat')))


def merj(port, tetelek, ismetles, hideg=True, cg=None):
    """tetelek: [(csoport, címke, út)] -> [{csoport, cimke, ut, hideg_ms, meleg_ms[], status, xcache, bajt}]"""
    ki = []
    for cs, cimke, ut in tetelek:
        rec = {'csoport': cs, 'cimke': cimke, 'ut': ut}
        if hideg:
            ures_cache()
            r0 = rbajt(cg)
            st, ms, (xc, n) = keres(port, ut)
            rec.update(hideg_ms=ms, status=st, xcache_hideg=xc, bajt=n, hideg_lemez_olvasas_bajt=rbajt(cg) - r0)
        ki.append(rec)
    for rec in ki:
        st, _, _ = keres(port, rec['ut'])               # bemelegítés (nem számít)
        meleg = []
        xcs = set()
        for _ in range(ismetles):
            st, ms, (xc, n) = keres(port, rec['ut'])
            meleg.append(ms)
            xcs.add(xc)
        rec.update(meleg_ms=meleg, status_meleg=st, xcache_meleg=sorted(xcs), bajt=n)
    return ki


def osszegez(rek):
    hid = [r['hideg_ms'] for r in rek if 'hideg_ms' in r]
    mel = [x for r in rek for x in r['meleg_ms']]
    mel_lap = [statistics.median(r['meleg_ms']) for r in rek]
    return {'n_lap': len(rek), 'hideg_median': statistics.median(hid) if hid else None, 'hideg_p95': p95(hid) if hid else None,
            'hideg_lemez_mb_median': statistics.median([r['hideg_lemez_olvasas_bajt'] / 1e6 for r in rek]) if hid else None,
            'meleg_median': statistics.median(mel), 'meleg_p95': p95(mel), 'meleg_lapmedian_max': max(mel_lap), 'n_meleg': len(mel),
            'statusok': sorted({r.get('status', 0) for r in rek} | {r['status_meleg'] for r in rek}),
            'xcache': sorted({r.get('xcache_hideg', '') for r in rek if 'xcache_hideg' in r} | {x for r in rek for x in r['xcache_meleg']})}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--db', default='/home/%s/pardes/pardes.db' % FELHASZNALO)
    ap.add_argument('--port', type=int, default=8781)
    ap.add_argument('--kimenet', default='/tmp/pardes_m4')
    ap.add_argument('--ismetles', type=int, default=5)
    ap.add_argument('--seed', type=int, default=76)
    ap.add_argument('--gyors', action='store_true', help='kis minta (próbafutás)')
    a = ap.parse_args()
    if os.geteuid() != 0:
        sys.exit('rootként kell futnia (systemd-run --scope, drop_caches): wsl -d pardes -u root -e …')
    os.makedirs(a.kimenet, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    eredmeny = {'ts_kezdet': ts, 'gep': gep_adatai(a.db), 'modszer': {
        'korlat': 'systemd-run --scope ' + ' '.join(TULAJDONSAGOK[1::2]) + '; a szerver: runuser -u %s, gunicorn -c gunicorn_conf.py (gthread, 1 worker, 4 szál)' % FELHASZNALO,
        'kliens': 'http.client, új kapcsolat kérésenként, CPU-affinitás {1} (a korláton kívül)',
        'hideg': 'sync + drop_caches=3 minden kérés előtt, lap-LRU kikapcsolva (max_lap=0)',
        'meleg': '1 bemelegítő + %d mért kérés laponként, lap-LRU kikapcsolva' % a.ismetles,
        'lru': 'eredeti konfig (max_lap=512): a 2. kérés a gyorsítótárból (5 mért kérés)', 'p95': 'legközelebbi rang', 'seed': a.seed}}
    n = (4, 2, 4, 4, 2) if a.gyors else (20, 10, 20, 20, 9)
    m = minta(a.db, a.seed, *n)
    if a.gyors:
        m['keresesek'] = m['keresesek'][::6]
        m['szo_toredek'] = m['szo_toredek'][:4]
        m['fejezet'] = m['fejezet'][:3]
    eredmeny['minta'] = {k: v for k, v in m.items()}
    eredmeny['korlat_probak'] = korlat_probak()
    print('korlát-próbák:', json.dumps(eredmeny['korlat_probak'], ensure_ascii=False), flush=True)
    os.sched_setaffinity(0, {1})                         # a mérő kliens a korláton kívül, az 1. CPU-n (a próbák után: azok ne örököljék)

    # 1) LRU nélkül: hideg és meleg
    kdir = '/tmp/pardes_m4_konfig'
    shutil.rmtree(kdir, ignore_errors=True)
    shutil.copytree(os.path.join(D, 'konfig'), kdir)
    with open(os.path.join(kdir, 'szerver.toml'), encoding='utf-8') as f:
        t = f.read()
    if 'max_lap = 512' not in t:
        sys.exit('a szerver.toml-ban nincs „max_lap = 512” sor; a mérés nem tudja kikapcsolni a lap-LRU-t')
    with open(os.path.join(kdir, 'szerver.toml'), 'w', encoding='utf-8') as f:
        f.write(t.replace('max_lap = 512', 'max_lap = 0'))
    os.system('chmod -R a+rX %s' % kdir)
    sz = Szerver(a.db, a.port, kdir, 'pardes-m4-nolru', os.path.join(a.kimenet, 'gunicorn_nolru.log'))
    ures_cache()
    eredmeny['indulas_s_nolru'] = sz.indit()
    try:
        eredmeny['igazolas'] = sz.igazolas()
        print('igazolás:', json.dumps(eredmeny['igazolas'], ensure_ascii=False), flush=True)
        csoportok = {}
        for reteg, nev in (('', 'alap'), ('il', 'il')):
            csoportok['vers_' + nev] = [('vers_' + nev, c, retegges(u, reteg)) for c, u in m['vers']]
        csoportok['vers_toredek'] = [('vers_toredek', c, u) for c, u in m['vers_toredek']]
        csoportok['szo_heber'] = [('szo_heber', c, u) for c, u in m['szo_heber']]
        csoportok['szo_gorog'] = [('szo_gorog', c, u) for c, u in m['szo_gorog']]
        csoportok['szo_toredek'] = [('szo_toredek', c, u) for c, u in m['szo_toredek']]
        csoportok['fejezet'] = [('fejezet', c, u) for c, u in m['fejezet']]
        csoportok['kereses'] = [('kereses_' + ag, c, u) for ag, c, u in m['keresesek']]
        nyers = {}
        for nev, tet in csoportok.items():
            t0 = time.monotonic()
            nyers[nev] = merj(a.port, tet, a.ismetles, cg=sz.cgroup())
            print('%-22s kész, %.0f s' % (nev, time.monotonic() - t0), flush=True)
        eredmeny['memoria_nolru'] = sz.memoria()
        eredmeny['igazolas_utana'] = sz.igazolas()
    finally:
        sz.leallit()
    eredmeny['nyers'] = nyers
    oss = {nev: osszegez(r) for nev, r in nyers.items() if not nev.startswith('kereses')}
    ker = {}
    for r in nyers['kereses']:
        ker.setdefault(r['csoport'], []).append(r)
    for ag, rek in ker.items():
        oss[ag] = osszegez(rek)
    eredmeny['osszegzes'] = oss
    eredmeny['kereses_tetelek'] = [{'ag': r['csoport'], 'cimke': r['cimke'], 'hideg_ms': r['hideg_ms'], 'meleg_median': statistics.median(r['meleg_ms']),
                                    'meleg_p95': p95(r['meleg_ms']), 'status': r['status']} for r in nyers['kereses']]

    # 2) LRU-val (eredeti konfig): a kész lap a gyorsítótárból
    sz2 = Szerver(a.db, a.port, None, 'pardes-m4-lru', os.path.join(a.kimenet, 'gunicorn_lru.log'))
    eredmeny['indulas_s_lru'] = sz2.indit()
    try:
        lru = merj(a.port, [('lru_vers', c, u) for c, u in m['vers'][:10]] + [('lru_szo', c, u) for c, u in m['szo_heber'][:5] + m['szo_gorog'][:5]], a.ismetles, hideg=False)
        eredmeny['memoria_lru'] = sz2.memoria()
    finally:
        sz2.leallit()
    eredmeny['nyers']['lru'] = lru
    eredmeny['osszegzes']['lru'] = osszegez(lru)
    eredmeny['ts_veg'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(os.path.join(a.kimenet, 'm4_meres.json'), 'w', encoding='utf-8') as f:
        json.dump(eredmeny, f, ensure_ascii=False, indent=1)

    print('\n| csoport | lapok | hideg medián | hideg p95 | meleg medián | meleg p95 | státusz | X-Cache |')
    print('|---|---:|---:|---:|---:|---:|---|---|')
    for nev, o in eredmeny['osszegzes'].items():
        f = lambda x: '—' if x is None else '%.1f' % x  # noqa: E731
        print('| %s | %d | %s | %s | %s | %s | %s | %s |' % (nev, o['n_lap'], f(o['hideg_median']), f(o['hideg_p95']), f(o['meleg_median']), f(o['meleg_p95']),
                                                          ','.join(map(str, o['statusok'])), ','.join(o['xcache'])))
    print('\n| ág | keresés | hideg | meleg medián | meleg p95 |')
    print('|---|---|---:|---:|---:|')
    for t in eredmeny['kereses_tetelek']:
        print('| %s | %s | %.1f | %.1f | %.1f |' % (t['ag'], t['cimke'], t['hideg_ms'], t['meleg_median'], t['meleg_p95']))
    print('\nmemória (LRU nélkül):', eredmeny['memoria_nolru'])
    print('memória (LRU-val):', eredmeny['memoria_lru'])
    print('kimenet:', os.path.join(a.kimenet, 'm4_meres.json'))


if __name__ == '__main__':
    main()
