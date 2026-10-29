"""ISTENTISZT-001, ELLENOR_ISTENTISZT001_EZS64_ZSOLT99 javítókör: E1 (tokensorrend-proveniencia
a jeloltek.tsv két sorában) és A1 (az Ézs 64:6 elofordulasok-sorában a „nép” azonosítás
helyett a mért első személyű többes szám). split('\t') / '\t'.join(); írás előtt soronkénti
összevetés, eltérésnél megáll.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
TOK = ("scope=range:Ézs 64:6, range:Zsolt 99:6 | forras=TAHOT_kivonat.tsv+BSB_Strongs.tsv "
       "(naplok/ISTENTISZT001_ezs64_zsolt99_meres.py, split('\\t')) | n=43+12 | "
       "ts=2026-10-29T08:51Z")
LXX_EZS = ('scope=range:Ézs 64:6 | forras=LXX_OS/isaiah.tsv+TAGNT_kivonat.tsv | n=27 | '
           'ts=2026-10-29T08:32Z | csatorna=cli')
KAR_ZS = ('scope=range:Zsolt 99:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | '
          'n=2 | ts=2026-10-29T08:31Z | csatorna=cli')

JELOLT_CSERE = {
    'Ézs 64:6': (f'· {LXX_EZS}', f'· {LXX_EZS} · {TOK}'),
    'Zsolt 99:6': (f'· {KAR_ZS}', f'· {KAR_ZS} · {TOK}'),
}
ELOF_CSERE = {
    'kapcsolodas': ('a nép önmagáról mondott panaszban.',
                    'első személyű többes számú versben („tőlünk”, „minket”).'),
    'funkcio': ('a nép önmagáról mondva, egyenes szórenddel',
                'első személyű többes számú versben, egyenes szórenddel'),
}


def beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def kiir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok))


def fejlec(sorok):
    for i, s in enumerate(sorok):
        if not s.startswith('#'):
            return i, s.split('\t')
    raise SystemExit('nincs fejléc')


def csere(ut, kivalaszt, modosit):
    sorok = beolvas(ut)
    fi, fej = fejlec(sorok)
    ix = {n: i for i, n in enumerate(fej)}
    uj = list(sorok)
    erintett = []
    for i in range(fi + 1, len(sorok)):
        m = sorok[i].split('\t')
        if len(m) < len(fej) or not kivalaszt(m, ix):
            continue
        modosit(m, ix)
        uj[i] = '\t'.join(m)
        erintett.append(i)
    elter = [i for i in range(len(sorok)) if sorok[i] != uj[i]]
    if len(uj) != len(sorok) or elter != erintett:
        raise SystemExit(f'{ut}: váratlan eltérés {elter} / {erintett}')
    for i in elter:
        a, b = sorok[i].split('\t'), uj[i].split('\t')
        print(f'{ut} {i + 1}. sor: {[fej[k] for k in range(len(fej)) if a[k] != b[k]]}')
    kiir(ut, uj)
    return len(elter)


def jelolt_kivalaszt(m, ix):
    return (m[ix['id']] == ID and m[ix['jelolt_tipus']] == 'elofordulas'
            and m[ix['igehely']] in JELOLT_CSERE)


def jelolt_modosit(m, ix):
    regi, uj = JELOLT_CSERE[m[ix['igehely']]]
    ind = m[ix['indoklas']]
    if ind.count(regi) != 1 or TOK in ind:
        raise SystemExit(f'{m[ix["igehely"]]}: a csere helye nem egyértelmű')
    m[ix['indoklas']] = ind.replace(regi, uj)


def elof_kivalaszt(m, ix):
    return m[ix['id']] == ID and m[ix['igehely']] == 'Ézs 64:6'


def elof_modosit(m, ix):
    for mezo, (regi, uj) in ELOF_CSERE.items():
        if m[ix[mezo]].count(regi) != 1:
            raise SystemExit(f'{mezo}: a csere helye nem egyértelmű')
        m[ix[mezo]] = m[ix[mezo]].replace(regi, uj)


if __name__ == '__main__':
    if csere('adat/jeloltek.tsv', jelolt_kivalaszt, jelolt_modosit) != 2:
        raise SystemExit('jeloltek: nem két sor')
    if csere('adat/elofordulasok.tsv', elof_kivalaszt, elof_modosit) != 1:
        raise SystemExit('elofordulasok: nem egy sor')
