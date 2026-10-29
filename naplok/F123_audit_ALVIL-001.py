"""F123 (ALVIL-001): a motívum B4-lekérdezéseinek tényleges futtatása önnaplózással (`lekerdez.py --naplo ALVIL-001
--lepes B4`, SEMA 2.9). Az audit-sort a lekérdező maga írja az `adat/auditok.tsv`-be, a saját proveniencia-sorával;
ez a szkript csak sorban lefuttatja a parancsokat, és kiírja a proveniencia-sorokat (DT84 (2): a prózából audit-sor
nem keletkezik). A parancsok a régi tanulmány Q2-jében leírt, de naplózatlan kutatást ismétlik meg a mai adaton:
a két gerinc-Strong teljes scanje, az igealak, az LXX-híd és a kereszthivatkozások a két fő ívre (Zsolt 16:10 →
ApCsel 2:27, 31; Hós 13:14 → 1Kor 15:55).

    python naplok/F123_audit_ALVIL-001.py
"""
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PARANCSOK = [
    ['scan', 'H7585'],
    ['scan', 'G0086'],
    ['igealak', 'H7585'],
    ['lxx-hid', 'Zsolt 16:10'],
    ['lxx-hid', 'Hós 13:14'],
    ['tsk', 'Zsolt 16:10'],
    ['tsk', 'Hós 13:14'],
    ['karoli', 'Zsolt 16:10'],
    ['karoli', 'Hós 13:14'],
]


def main():
    hiba = 0
    for p in PARANCSOK:
        r = subprocess.run([sys.executable, 'eszkozok/lekerdez.py', '--naplo', 'ALVIL-001', '--lepes', 'B4'] + p,
                           capture_output=True, text=True, encoding='utf-8')
        sorok = [s for s in r.stdout.strip().split('\n') if s.strip()]
        utolso = sorok[-1] if sorok else ''
        print('%s\trc=%d\t%s' % (' '.join(p), r.returncode, utolso))
        if r.returncode != 0 or 'scope=' not in utolso:
            hiba += 1
            print(r.stderr[-500:], file=sys.stderr)
    sys.exit(1 if hiba else 0)


if __name__ == '__main__':
    main()
