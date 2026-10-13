"""F94.0 (FELADATOK #94, SZOTOVEZES): a repón kívüli előmérés három szótövezési mintájának átvétele
az `adat/szoto/` alá, egységes sémával (adat/SEMA.md 2.27).

Csak átvesz, nem javít: a szótári alakok a forrás szerint maradnak; az eltéréseket a DT130 végleges
pontjaitól az `elteres_dt130.py` listázza (a javítás a felhasználó döntése után, F94_SZOTOVEZES_BRIEF.md .0/3).

Használat:
    python eszkozok/szoto/minta_atvetel.py --forras <az előmérés szoto/ könyvtára> [--ts 2026-10-13T00:00Z]

A forráskönyvtár a repón kívül van; az útvonala nem kerül a kimenetbe, csak a fájlnév és a sha256.
Olvasás split('\\t'), írás '\\t'.join() (CLAUDE.md: a csv modul tilos)."""
import argparse
import datetime
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CEL = os.path.join(REPO, 'adat', 'szoto')

OSZLOPOK = ['alak', 'gyakorisag', 'kategoria', 'szotari_alak', 'szotari_alak_mai', 'alapige',
            'tovabbi_elfogadhato', 'ellenorzes', 'indoklas', 'pelda_igehely', 'strong']

# A forrás oszlopneve -> az egységes oszlop
ATNEVEZ = {'to_regies': 'szotari_alak', 'to_mai': 'szotari_alak_mai', 'megjegyzes': 'indoklas'}

# A 3. minta általános (soronként azonos) döntés-szövege: ez az `ellenorzes=felhasznalo` forrása;
# az ettől eltérő, soronkénti döntés-szöveg az `indoklas` végére kerül, [döntés: …] alakban.
ALTALANOS_DONTES = 'felhasználói döntés 2026-10-13: mind ok (a 100 soros lista)'
# Az 1. és 2. minta felhasználói döntéssel lezárt sorainak jele a forrás megjegyzésében
DONTES_JEL = 'felhasználói döntés 2026-10-13'

MINTAK = [
    dict(forras='szoto_aranyminta_tervezet.tsv', cel='szoto_minta_1_fejlesztes.tsv', n=213,
         scope='1Móz 1–25 Károli-szóalakjai (token_karoli, oldal=hu), rétegzett válogatás; a gyakoriság az 1Móz 1–25-ön belüli',
         allapot='fejlesztési halmaz (a hibrid v1/v2 ezen hangolva); a szótári alakok modell-javaslatok, a felhasználó a sorokat nem nézte („mehet”): ellenorzes=modell_ellenorizetlen'),
    dict(forras='szoto_fuggetlen_minta.tsv', cel='szoto_minta_2_fejlesztes.tsv', n=180,
         scope='Zsolt 1–41 és Ézs 40–55 Károli-szóalakjai (token_karoli, oldal=hu), az 1. minta alakjai nélkül, rétegzett; '
               'a terv szerinti Gal/Ef/Zsid rész ÜRES maradt, mert a token_karoli csak az ÓSZ 39 könyvét tartalmazta; '
               'a gyakoriság a Zsolt 1–41 + Ézs 40–55 hatókörön belüli',
         allapot='eredetileg független minta, a hibrid v2 hangolása óta fejlesztési halmaz; a 6 nyitott sor a felhasználó döntésével '
                 'lezárva (ellenorzes=felhasznalo), a többi a felhasználó „mehet”-jével, soronkénti átnézés nélkül (modell_ellenorizetlen)'),
    dict(forras='szoto_harmadik_minta.tsv', cel='szoto_minta_3_ellenorzott.tsv', n=113,
         scope='Jer, Jób, Luk, Jak Károli-szóalakjai (vers.karoli_szoveg), az 1. és 2. minta alakjai nélkül, rétegzett, mag 20261013; '
               'a gyakoriság a négy könyvön belüli; Strong-adat a forrásban nincs (a strong oszlop üres)',
         allapot='mind a 113 sort a felhasználó ellenőrizte (2026-10-13): ellenorzes=felhasznalo; a soronkénti, nem általános döntés-szöveg '
                 'az indoklas végén [döntés: …]; a szótári alakokat a modell a hibrid futtatása ELŐTT rögzítette'),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def beolvas(p):
    sorok = open(p, encoding='utf-8').read().split('\n')
    meta = [s for s in sorok if s.startswith('#')]
    adat = [s.rstrip('\r') for s in sorok if s and not s.startswith('#')]
    fej = adat[0].split('\t')
    rekordok = []
    for s in adat[1:]:
        m = s.split('\t')
        if len(m) != len(fej):
            sys.exit(f'HIBA: {os.path.basename(p)}: {len(m)} mező, a fejléc {len(fej)}: {s[:60]}')
        rekordok.append(dict(zip(fej, m)))
    return meta, fej, rekordok


def atalakit(minta, r):
    u = {o: '' for o in OSZLOPOK}
    for k, v in r.items():
        k2 = ATNEVEZ.get(k, k)
        if k2 in u:
            u[k2] = v
    indoklas = u['indoklas']
    if minta['cel'].startswith('szoto_minta_3'):
        e = r['ellenorzes']
        if not e.startswith('felhasználói döntés'):
            sys.exit(f'HIBA: a 3. minta sora nem felhasználói döntés: {r["alak"]}')
        u['ellenorzes'] = 'felhasznalo'
        if e != ALTALANOS_DONTES:
            indoklas = (indoklas + ' ' if indoklas else '') + '[döntés: ' + e + ']'
        if r.get('bizonytalan'):
            indoklas = (indoklas + ' ' if indoklas else '') + '[bizonytalan: ' + r['bizonytalan'] + ']'
    else:
        u['ellenorzes'] = 'felhasznalo' if DONTES_JEL in r.get('megjegyzes', '') else 'modell_ellenorizetlen'
    u['indoklas'] = indoklas
    for k, v in u.items():
        if '\t' in v or '\n' in v:
            sys.exit(f'HIBA: tab/sortörés a mezőben: {r["alak"]} {k}')
    return u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--forras', required=True)
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    a = ap.parse_args()
    os.makedirs(CEL, exist_ok=True)
    for minta in MINTAK:
        p = os.path.join(a.forras, minta['forras'])
        meta, fej, rek = beolvas(p)
        if len(rek) != minta['n']:
            sys.exit(f'HIBA: {minta["forras"]}: {len(rek)} sor, várt {minta["n"]}')
        ki = [atalakit(minta, r) for r in rek]
        nf = sum(1 for u in ki if u['ellenorzes'] == 'felhasznalo')
        prov = (f'# proveniencia: scope={minta["scope"]} | forras={minta["forras"]} (sha256:{sha(p)}; a repón kívüli előmérés, '
                f'2026-10-12/13; átvétel: eszkozok/szoto/minta_atvetel.py, F94.0) | ts={a.ts}')
        fejlec = [prov,
                  f'# allapot: {minta["allapot"]}; felhasznalo {nf}, modell_ellenorizetlen {len(ki) - nf}',
                  '# a forrás saját fejléce (szó szerint): ' + ' // '.join(m.lstrip('# ').strip() for m in meta)]
        if any('\t' in f for f in fejlec):
            sys.exit('HIBA: tab a fejlécben')
        kimenet = os.path.join(CEL, minta['cel'])
        with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(fejlec) + '\n')
            f.write('\t'.join(OSZLOPOK) + '\n')
            for u in ki:
                f.write('\t'.join(u[o] for o in OSZLOPOK) + '\n')
        # visszaolvasás: a sorok száma és a kulcsmezők azonosak a forráséval
        _, fej2, rek2 = beolvas(kimenet)
        assert fej2 == OSZLOPOK and len(rek2) == len(rek)
        for r, r2 in zip(rek, rek2):
            assert r['alak'] == r2['alak'] and r['to_regies'] == r2['szotari_alak'] and r['to_mai'] == r2['szotari_alak_mai']
            assert r['gyakorisag'] == r2['gyakorisag'] and r.get('alapige', '') == r2['alapige']
            assert r.get('tovabbi_elfogadhato', '') == r2['tovabbi_elfogadhato']
        print(f'{minta["cel"]}: {len(ki)} sor (felhasznalo {nf}), forrás sha256 {sha(p)[:12]}')


if __name__ == '__main__':
    main()
