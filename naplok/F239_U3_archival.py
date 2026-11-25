"""F239 U3 — a TEREMT-001 régi fájljainak archiválása (nem törlés; DT215, a HAMART-001 és az ALVIL-001 mintája).

1. `git mv` az `archivum/TEREMT-001/` alá, ARCHÍV fejléccel (alatta a fájl bájtra változatlan):
   - tematikus_lezart/Tehom_tematikus.md → archivum/TEREMT-001/Tehom_tematikus.md
   - tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md → archivum/TEREMT-001/Tehom_kereszthivatkozas_naplo.md
   - motivumok/TEREMT-001.md (a régi forrásréteg) → archivum/TEREMT-001/TEREMT-001_forrasreteg_regi.md
   - lexikon/TEREMT-001_TORZSCIKK.md → archivum/TEREMT-001/TEREMT-001_torzscikk_regi.md
2. A régi 1/a-próza (`elofordulasok.tsv` `kapcsolodas`, `funkcio`, a HEAD állapotából) →
   archivum/TEREMT-001/TEREMT-001_1a_proza_regi.tsv.
3. `adat/motivumok.tsv` `forras_study` → `motivumok/TEREMT-001.md`.
4. A régi útvonalra mutató hivatkozások (E27): a briefek `olvas` mezője; a NYITOTT_FELADATOK.md N58 tétele lezárva
   (a régi tanulmány archiválásával zárul, a határ-fájl B2 pontja szerint).
A régi forrásréteg helyére az új kézi forrás a hívó lépésben kerül (ez a szkript csak archivál).
Futtatás a repó gyökeréből: python naplok/F239_U3_archival.py"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

DATUM = '2026-11-23'
CEL = 'archivum/TEREMT-001'
MOZGAT = [
    ('tematikus_lezart/Tehom_tematikus.md', CEL + '/Tehom_tematikus.md'),
    ('tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md', CEL + '/Tehom_kereszthivatkozas_naplo.md'),
    ('motivumok/TEREMT-001.md', CEL + '/TEREMT-001_forrasreteg_regi.md'),
    ('lexikon/TEREMT-001_TORZSCIKK.md', CEL + '/TEREMT-001_torzscikk_regi.md'),
]
OLVAS_CSERE = [(r, u) for r, u in MOZGAT if not r.startswith('motivumok/')]
BRIEFEK = ['F109_TEHOM_JOB41_BRIEF.md', 'F123_MIGRACIO2_BRIEF.md', 'F127_LEXIKON_HALO_RES_BRIEF.md',
           'F12_TEREMT002_PROZA_BRIEF.md', 'F239_TEREMT001_CIKK_BRIEF.md']


def git(*a):
    return subprocess.run(['git'] + list(a), capture_output=True, check=True).stdout.decode('utf-8').strip()


def olvas(ut):
    nyers = open(ut, encoding='utf-8', newline='').read()
    return nyers, ('\r\n' if '\r\n' in nyers else '\n')


def main():
    if git('status', '--porcelain', '--', *[r for r, _u in MOZGAT]):
        sys.exit('HIBA: az archiválandó fájlok egyikének helyi változása van')
    fej = git('rev-parse', '--short=8', 'HEAD')
    os.makedirs(CEL, exist_ok=True)
    # 2. a régi 1/a-próza a HEAD-ből
    head = git('show', 'HEAD:adat/elofordulasok.tsv').replace('\r\n', '\n').split('\n')
    fejsor = next(l for l in head if l and not l.startswith('#')).split('\t')
    ix = {k: i for i, k in enumerate(fejsor)}
    ki = ['# ARCHÍV: adat/elofordulasok.tsv (TEREMT-001, kapcsolodas + funkcio) @ %s · F239 TEREMT-001 új cikk, U3 · %s · '
          'nem forrás, nem szerkesztendő' % (fej, DATUM), 'igehely\tkapcsolodas\tfuncio_regi']
    ki[1] = 'igehely\tkapcsolodas\tfunkcio'
    for l in head:
        m = l.split('\t')
        if len(m) > 4 and m[0] == 'TEREMT-001':
            ki.append('\t'.join([m[ix['igehely']], m[ix['kapcsolodas']], m[ix['funkcio']]]))
    open(CEL + '/TEREMT-001_1a_proza_regi.tsv', 'w', encoding='utf-8', newline='').write('\n'.join(ki) + '\n')
    print('régi 1/a-próza: %d sor' % (len(ki) - 2))
    # 1. git mv + ARCHÍV fejléc
    for regi, uj in MOZGAT:
        git('mv', regi, uj)
        t, nl = olvas(uj)
        open(uj, 'w', encoding='utf-8', newline='').write(
            '<!-- ARCHÍV: %s @ %s · F239 TEREMT-001 új cikk, U3 · %s · nem forrás, nem szerkesztendő -->%s%s'
            % (regi, fej, DATUM, nl, t))
        print('%s → %s' % (regi, uj))
    # 3. motivumok.tsv forras_study
    t, nl = olvas('adat/motivumok.tsv')
    s = t.split(nl)
    fi = next(i for i, l in enumerate(s) if l and not l.startswith('#'))
    mix = {k: i for i, k in enumerate(s[fi].split('\t'))}
    n = 0
    for i, l in enumerate(s):
        m = l.split('\t')
        if m[0] == 'TEREMT-001':
            print('forras_study: %r → motivumok/TEREMT-001.md' % m[mix['forras_study']])
            m[mix['forras_study']] = 'motivumok/TEREMT-001.md'
            s[i] = '\t'.join(m)
            n += 1
    assert n == 1
    open('adat/motivumok.tsv', 'w', encoding='utf-8', newline='').write(nl.join(s))
    # 4. a briefek olvas mezője
    for b in BRIEFEK:
        t, nl = olvas(b)
        s = t.split(nl)
        oi = next(i for i, l in enumerate(s) if l.startswith('olvas:'))
        regi_sor = s[oi]
        for r, u in OLVAS_CSERE:
            s[oi] = s[oi].replace(r, u)
        # a „tematikus_lezart/TEREMT-001*” minták maradnak: a feladatkövető (feladatok.py ellenoriz) a motívumot író
        # brief `olvas` mezőjében megköveteli őket
        if s[oi] != regi_sor:
            open(b, 'w', encoding='utf-8', newline='').write(nl.join(s))
            print('olvas: %s' % b)
    # N58 lezárása
    t, nl = olvas('NYITOTT_FELADATOK.md')
    s = t.split(nl)
    ni = [i for i, l in enumerate(s) if l.startswith('- **N58 — ')]
    assert len(ni) == 1
    l = s[ni[0]]
    cim_vege = l.index('**', len('- **')) + 2
    s[ni[0]] = ('- ~~' + l[2:cim_vege] + '~~ **LEZÁRVA (F239 U3, %s):** a régi tanulmány archívumba került '
                '(`archivum/TEREMT-001/Tehom_tematikus.md`, ARCHÍV fejléccel); a TEREMT-001 új cikke a mai adatból '
                'számol (35 héber vers, 36 előfordulás); a régi szöveget nem javítjuk (`naplok/F239_hatar.md` 2. pont, '
                'B2). *(Eredeti bejegyzés, történeti:)*' % DATUM + l[cim_vege:])
    open('NYITOTT_FELADATOK.md', 'w', encoding='utf-8', newline='').write(nl.join(s))
    print('N58 lezárva')


if __name__ == '__main__':
    main()
