"""ISTENTISZT-001: az Ézs 64:6 (beépítve) és a Zsolt 99:6 (elutasítva) döntés átvezetése.

jeloltek.tsv: a két sor dontes/indoklas/datum mezője (az Ézs 64:6-nál a Károli-triplet is);
elofordulasok.tsv: új Ézs 64:6 sor a Zsolt 79:6 után. split('\t') / '\t'.join(); írás
előtt soronkénti összevetés az eredetivel, eltérésnél megáll. Napló:
naplok/ISTENTISZT001_ezs64_zsolt99_naplo.md.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
DATUM = '2026.10.29'
DONTES = ('Döntés (felhasználó, 2026-10-29, orkesztrátor-chat, szó szerint: „Igen, így”; '
          'a kérdés: „Ézs 64:6 beépítve, Zsolt 99:6 elutasítva?”)')
KOLL = ('scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | '
        'strong=H7121+H8034 | n=196 | ts=2026-10-29T08:32Z | csatorna=cli')
KAR_EZS = ('scope=range:Ézs 64:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | '
           'n=1 | ts=2026-10-29T08:31Z | csatorna=cli')
KAR_ZS = ('scope=range:Zsolt 99:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | '
          'n=2 | ts=2026-10-29T08:31Z | csatorna=cli')
LXX_EZS = ('scope=range:Ézs 64:6 | forras=LXX_OS/isaiah.tsv+TAGNT_kivonat.tsv | n=27 | '
           'ts=2026-10-29T08:32Z | csatorna=cli')

EZS_REGI_VEG = ' Elbírálatlan: a motívum-menet dönt'
EZS_UJ = (f' {DONTES}: beépítve. Saját mérés: TAHOT וְאֵין קוֹרֵא בְשִׁמְךָ (H0369 + H7121 + '
          f'H9003 + H8034, 2. sz. birtokos rag) — aktív kárá + בְּ + Isten neve, emberi alany, '
          f'tagadó forma; az LXX-ben οὐκ ἔστιν ὁ ἐπικαλούμενος τὸ ὄνομά σου (G1941). '
          f'Precedens: Jer 10:25, Zsolt 79:6 (beépítve, tagadó forma). '
          f'Mérés 2026-10-29: {KOLL} · {KAR_EZS} · {LXX_EZS}')

ZS_REGI_VEG = (' Elbírálatlan (az Ézs 64:6-tal azonos eljárás, F110): a beépítésről a '
               'motívum-menet dönt; a próza addig nem szól róla')
ZS_UJ = (f' {DONTES}: elutasítva a negatív kritérium szerint (adat/motivumok.tsv: '
         f'קָרָא + בְּ aktív, invokáló szerkezet kell). Saját mérés, TAHOT: '
         f'וּשְׁמוּאֵל בְּקֹרְאֵי שְׁמוֹ קֹרִאים אֶל־יְהוָה — a בְּ (H9003) az igenév előtt áll '
         f'(„azok között, akik hívják”), a név (H8034 + 3. sz. birtokos rag) az igenév '
         f'birtokos szerkezetében, a második tagban אֶל (H0413) + יְהוָה; kárá + בְּ + név '
         f'szerkezet nincs, így a fenti „A-minta” olvasat nem áll. Előzmény: DT283 (JSir 3:55, '
         f'5Móz 32:3: a בְּ nélküli szerkezet kiszűrve marad, a kritérium nem változik). '
         f'Mérés 2026-10-29: {KOLL} · {KAR_ZS}')

UJ_SOR = {
    'id': ID,
    'igehely': 'Ézs 64:6',
    'kapcsolodas': '"S nem volt, a ki segítségül hívta volna nevedet" — a formula tagadó '
                   'formában, a nép önmagáról mondott panaszban.',
    'pardes_szint': 'Remez',
    'funkcio': '🚫 tagadó forma — a formula elmulasztása, a nép önmagáról mondva, '
               'egyenes szórenddel',
    'gerinc_elem': 'H7121+H8034',
    'strong': 'H7121+H8034',
    'lexikon_szotar': 'BDB',
    'lexikon_entry_id': 'H7121',
    'jelentes_szam': '2.c (tagadva)',
    'jelentes_en': '',
    'jelentes_hu': 'invokálni — tagadó szerkezetben',
    'karoli_szo': 'segítségül hívta volna nevedet',
    'azonositas_modja': 'tartalom-alapú',
    'megbizhatosag': 'magas',
    'proveniencia': KOLL,
    'igazolas': 'TAHOT-igazolt',
    'fo_elofordulas': '',
    'felmerult_tanulmany': '',
    'forras_tanulmany': '',
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


def jeloltek(ut):
    sorok = beolvas(ut)
    fi, fej = fejlec(sorok)
    ix = {n: i for i, n in enumerate(fej)}
    uj = list(sorok)
    talalt = {}
    for i in range(fi + 1, len(sorok)):
        m = sorok[i].split('\t')
        if len(m) < len(fej) or m[ix['id']] != ID or m[ix['jelolt_tipus']] != 'elofordulas':
            continue
        hely = m[ix['igehely']]
        if hely not in ('Ézs 64:6', 'Zsolt 99:6'):
            continue
        if m[ix['dontes']] != 'nyitva':
            raise SystemExit(f'{hely}: dontes nem nyitva ({m[ix["dontes"]]})')
        ind = m[ix['indoklas']]
        regi, uj_szoveg, dontes = ((EZS_REGI_VEG, EZS_UJ, 'beépítve') if hely == 'Ézs 64:6'
                                   else (ZS_REGI_VEG, ZS_UJ, 'elutasítva'))
        if ind.count(regi) != 1:
            raise SystemExit(f'{hely}: a lecserélendő szakasz nem egyszer szerepel')
        m[ix['indoklas']] = ind.replace(regi, uj_szoveg)
        m[ix['dontes']] = dontes
        m[ix['datum']] = DATUM
        if hely == 'Ézs 64:6':
            m[ix['karoli_szo']] = UJ_SOR['karoli_szo']
            m[ix['azonositas_modja']] = UJ_SOR['azonositas_modja']
            m[ix['megbizhatosag']] = UJ_SOR['megbizhatosag']
        uj[i] = '\t'.join(m)
        talalt[hely] = i
    if len(talalt) != 2:
        raise SystemExit(f'nem két sor: {talalt}')
    elter = [i for i in range(len(sorok)) if sorok[i] != uj[i]]
    if len(sorok) != len(uj) or sorted(elter) != sorted(talalt.values()):
        raise SystemExit(f'váratlan eltérés: {elter}')
    for i in elter:
        a, b = sorok[i].split('\t'), uj[i].split('\t')
        valt = [fej[k] for k in range(len(fej)) if a[k] != b[k]]
        print(f'jeloltek.tsv {i + 1}. sor: változott mezők: {valt}')
    kiir(ut, uj)


def elofordulasok(ut):
    sorok = beolvas(ut)
    fi, fej = fejlec(sorok)
    if list(UJ_SOR) != fej:
        raise SystemExit('mezősorrend')
    ix = {n: i for i, n in enumerate(fej)}
    hova = None
    for i in range(fi + 1, len(sorok)):
        m = sorok[i].split('\t')
        if len(m) < 2 or m[ix['id']] != ID:
            continue
        if m[ix['igehely']] == 'Ézs 64:6':
            raise SystemExit('Ézs 64:6 már bent van')
        if m[ix['igehely']] == 'Zsolt 79:6':
            hova = i + 1
    if hova is None:
        raise SystemExit('nincs Zsolt 79:6 sor')
    uj = sorok[:hova] + ['\t'.join(UJ_SOR.values())] + sorok[hova:]
    if uj[:hova] != sorok[:hova] or uj[hova + 1:] != sorok[hova:]:
        raise SystemExit('váratlan eltérés')
    print(f'elofordulasok.tsv: új sor a {hova + 1}. helyen (a Zsolt 79:6 után)')
    kiir(ut, uj)


if __name__ == '__main__':
    jeloltek('adat/jeloltek.tsv')
    elofordulasok('adat/elofordulasok.tsv')
