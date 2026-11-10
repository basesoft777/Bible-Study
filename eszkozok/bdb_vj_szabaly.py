"""bdb_vj_szabaly.py — a vers -> jelentés tábla (`adat/bdb_vers_jelentes.tsv`, SEMA 2.29) sorainak minősítése (#104).

Az olvasó-szerver BDB-blokkja (`olvaso_szerver/blokkok.py`, `VersJelolo`) és a lexikon-generátor 4.2-es kártyája
(`lexikon_general.bdb_olvasoi_reteg`, `bdb_hivatkozas_szam`) ugyanezt a szabályt használja (egy szabály, egy hely):

- `vj_feloldott`: a pontos hivatkozásszám alapja (DT-F104d; a #104 brief 2.: „a feloldott, szűrt hivatkozásoké”);
- `BIZONYTALAN_OK`, `BIZONYTALAN_VERS`, `vj_bizonytalan`: a bizonytalan sor, amelynek pontja csak gyenge jelölést kap
  („vonatkozhat”; DT178, DT-F104e).

Szándékosan külön modul, nem a `olvaso_szerver/bdb_szelet.py`: az a `bdb_vers_jelentes.tsv` kód-hash bemenete
(`bdb_vers_jelentes.KOD_FAJLOK`), így minden ottani változás a tábla fejlécét is megváltoztatná. Csak standard könyvtár.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def vj_feloldott(r):
    """A pontos hivatkozásszám alapja: nem szűrt, feloldott (maszoréta versszámmal bíró) bibliai hivatkozás. A Károli-vers
    nem feltétel."""
    return r.get('szurt') != '1' and bool(r.get('mt_vers'))


# a táblában maradó bizonytalan sorok okkódjai (SEMA 2.29 `okkod`: „bizonytalan, a táblában marad”), a kézzel azonosított hibás
# forrás-hely és a bizonytalan versszám-megfeleltetés: az ilyen hivatkozás pontja csak gyenge jelölést kap
BIZONYTALAN_OK = {'sigla_kozel': 'a hely mellett kommentár-jel áll', 'tobbertelmu': 'a könyvnév rövidítése többértelmű',
                  'ismeretlen_alak': 'a könyvnév alakja ismeretlen', 'nincs_elozmeny': 'a könyv nem állapítható meg',
                  'orokles_hibas': 'az örökölt könyvben nincs ilyen fejezet', 'forras_hiba': 'a BDB nyomtatott igehelye hibás'}
BIZONYTALAN_VERS = {'atkulcsolt_bizonytalan': 'a héber és a Károli-versszámozás megfeleltetése bizonytalan'}


def vj_bizonytalan(r):
    """A sor bizonytalanságának okai (olvasói szöveg); üres lista: biztos sor."""
    okok = [BIZONYTALAN_OK[o] for o in (r.get('okkod') or '').split(',') if o in BIZONYTALAN_OK]
    if r.get('vers_feloldas') in BIZONYTALAN_VERS:
        okok.append(BIZONYTALAN_VERS[r['vers_feloldas']])
    return okok
