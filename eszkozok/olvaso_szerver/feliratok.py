"""feliratok.py — az olvasó fordítótáblája (DT897; a #231 rögzíti a helyét és formáját, a #233 ugyanezt használja).

A tábla: `konfig/feliratok.tsv`, oszlopai `kulcs`, `hu`, `en` (az angol oszlop üresen maradhat; üres angolnál a magyar áll).
Kulcs: pontokkal tagolt azonosító (`szk.hivatkozas`, `blokk.szo.bdb_apparatus`). A szöveg `%(nev)s` helyőrzőt tartalmazhat,
a `F('kulcs', nev=…)` hívás tölti ki. A felirat sima szöveg: a hívó escape-eli (a `Markup('…%s…') % F(…)` alak ezt megteszi).
Ismeretlen kulcs: kimondott hiba (`KeyError`), nem néma üres felirat; a tábla ismétlődő kulcsa betöltési hiba.

Hatókör: a #231 és a #233 által írt vagy átírt feliratok (blokkcím, gomb, rögzített olvasói mondat, súgó). A régi,
nem érintett feliratok kiemelése nem része (DT897). A belső kulcsok olvasói neve nem ide, hanem a névtáblába tartozik (DT906).
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TABLA_UT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'konfig', 'feliratok.tsv')
NYELV = os.environ.get('PARDES_FELIRAT_NYELV', 'hu')


def betolt(ut=TABLA_UT):
    """{kulcs: {'hu': …, 'en': …}}; a `#` kezdetű és az üres sorok kimaradnak. Hibát dob ismétlődő kulcsnál és hiányzó magyarnál."""
    tabla, fej = {}, None
    with open(ut, encoding='utf-8') as f:
        for n, sor in enumerate(f, 1):
            sor = sor.rstrip('\n')
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fej is None:
                fej = mezok
                if fej[:2] != ['kulcs', 'hu']:
                    raise ValueError('a feliratok.tsv fejléce: kulcs, hu, en (%s)' % fej)
                continue
            d = dict(zip(fej, mezok + [''] * (len(fej) - len(mezok))))
            if d['kulcs'] in tabla:
                raise ValueError('a feliratok.tsv %d. sora: ismétlődő kulcs: %s' % (n, d['kulcs']))
            if not d['hu']:
                raise ValueError('a feliratok.tsv %d. sora: üres magyar szöveg: %s' % (n, d['kulcs']))
            tabla[d['kulcs']] = {'hu': d['hu'].replace('\\n', '\n'), 'en': d.get('en', '').replace('\\n', '\n')}
    return tabla


TABLA = betolt()


def F(kulcs, **param):
    """A kulcs felirata a beállított nyelven (`PARDES_FELIRAT_NYELV`, alap: hu; üres angolnál a magyar), a helyőrzők kitöltve."""
    sor = TABLA[kulcs]
    s = (sor.get(NYELV) or sor['hu'])
    return s % param if param else s


def Fv(kulcs, alap):
    """A kulcs felirata, vagy `alap`, ha a kulcs nincs a táblában (szabad nevű konfigurációs érték olvasói neve, pl. a hozzáférési
    szint: a konfiguráció neve szabad, a tábla csak az ismert neveket fordítja)."""
    return F(kulcs) if kulcs in TABLA else alap
