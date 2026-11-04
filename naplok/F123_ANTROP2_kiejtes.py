"""F123 ANTROP-001, 1. kiadás előtti javítókör (DT566): a kivétel-mondat két görög kifejezésének
kiejtése a Kivonatban és a motivumok.tsv-ben, szó szerint egyezően. Csak kiejtés, tartalom nem."""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = Path(__file__).resolve().parent.parent
REGI = '(ψυχικὸς ἄνθρωπος ↔ ὁ πνευματικός)'
UJ = '(ψυχικὸς ἄνθρωπος (pszükhikosz anthróposz) ↔ ὁ πνευματικός (ho pneumatikosz))'
for rel in ('adat/motivumok.tsv', 'motivumok/ANTROP-001.md'):
    p = G / rel
    t = p.read_text(encoding='utf-8')
    if t.count(REGI) != 1:
        sys.exit(f'HIBA: {rel}: {t.count(REGI)} találat')
    n0 = t.count('\n')
    t = t.replace(REGI, UJ)
    assert t.count('\n') == n0
    p.write_text(t, encoding='utf-8', newline='')
    print(rel, 'ok')
