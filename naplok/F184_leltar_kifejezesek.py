"""F184.D0: szabály-kifejezések előfordulása a folyamat-dokumentumokban (azonosító nélküli másolatok)."""
import sys, os, glob, re
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
os.chdir(sys.argv[1])
fajlok = ['CLAUDE.md', 'MUNKAMENET.md', 'BRIEF_SABLON.md', 'adat/SEMA.md', 'Rendszerfejlesztesi_playbook.md']
fajlok += sorted(glob.glob('sablonok/*.md')) + sorted(glob.glob('.claude/commands/*.md')) + sorted(glob.glob('.claude/agents/*.md'))
KIF = [
    'első előfordulásnál',
    'commitEncoding',
    'Modell-ellenőrzés',
    'tényleges modellnév',
    'split(\'\\t\')',
    'csv.reader',
    'kerek mondat',
    'Funkció:',
    'U2/U3',
    'próza gazdája',
    'egy kézben',
    'Nave-blokk',
    'nincs közvetlen út',
    'Nincs közvetlen út',
    'szerkesztői döntés',
    'helyőrző',
    'dontesek/uj',
    'nyitott/uj',
    '_zaras.md',
    'F<nn>_jelentes',
    'jelentes.md',
    'Folytatási pont',
    'allapot: megallt',
    'Te: ',
    'GENERÁLT',
    'kiejtés nélkül',
    'Pesat-gerinc',
    'lánc-szó',
    'két kéz',
    'másik kéz',
    'Feed 8',
    'mind a 9 kapu',
    '9 kapuja',
    '0 BUKÁS',
]
for k in KIF:
    hely = []
    for f in fajlok:
        try:
            sorok = open(f, encoding='utf-8').read().split('\n')
        except FileNotFoundError:
            continue
        n = [str(i) for i, s in enumerate(sorok, 1) if k in s]
        if n:
            hely.append('%s:%s' % (f.replace('\\', '/'), ','.join(n[:8]) + ('…(%d)' % len(n) if len(n) > 8 else '')))
    print('%-22s %d dok | %s' % (k, len(hely), ' ; '.join(hely)))
