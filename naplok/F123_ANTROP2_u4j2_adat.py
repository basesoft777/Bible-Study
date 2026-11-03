"""F123 ANTROP-001, U4 javítókör, az ellenőr 2. körének utójavítása (DT-F123r):
az elutasítási ok megjegyzése a kritérium szavaival; a 8 jelöltsor forras-nyoma nem a céltáblára mutat."""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = Path(__file__).resolve().parent.parent


def csere(nev, regi, uj, db):
    p = G / 'adat' / nev
    t = p.read_text(encoding='utf-8')
    if t.count(regi) != db:
        sys.exit(f'HIBA: {nev}: {t.count(regi)} találat, várt {db}')
    n0 = t.count('\n')
    t = t.replace(regi, uj)
    assert t.count('\n') == n0
    p.write_text(t, encoding='utf-8', newline='')
    print(nev, db)


csere('elutasitasi_okok.tsv',
      'de a mondat nem szembeállítja és nem különbözteti meg őket (például eszközként vagy párhuzamos tagként állnak egymás mellett)',
      'de a mondat nem szembeállítja és nem különbözteti meg őket', 1)
csere('jeloltek.tsv',
      '| scope=manual | forras=adat/elofordulasok.tsv (kapcsolodas, funkcio) | ts=2026-11-03',
      '| scope=manual | forras=a próza szerzője (claude-opus-5-5), a régi szöveg helyett: archivum/ANTROP-001/ANTROP-001_1a_proza_regi.tsv | ts=2026-11-03', 8)
