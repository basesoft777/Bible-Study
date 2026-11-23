"""F239.U1b (C-vh): a TEREMT-001 öt alak nélküli LXX-sorának modell-kinyerése (első kéz; a gépi kinyerés nem volt
egyértelmű). A versszöveg: konkordancia/LXX_OS (a kinyerő olvasta: claude-sonnet-5-5, 2026-11-23). Kimenet:
naplok/F239_U1b_lxx_kinyert.tsv; a második kéz ítélete: naplok/F239_U1b_lxx_atnezes.tsv."""
import os, sys
GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
M, MODELL, TS = 'TEREMT-001', 'claude-sonnet-5-5', '2026-11-23'
OSZLOP = ['motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas', 'megjegyzes',
          'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
SOROK = [  # (igehely, alak, lemma, kiejtés, jelentés, megjegyzés)
    ('1Móz 49:25', '', '', '', '', 'a görög a „lent heverő mélység” kifejezést a „mindent bíró föld áldásaival” (εὐλογίαν γῆς ἐχούσης πάντα) '
     'adja vissza: a mélység szava nincs a versben'),
    ('2Móz 15:5', 'πόντῳ', 'πόντος', 'pontó', 'tenger', 'a héber „mélységek” helyén a „tenger” (πόντος) áll; a következő félvers '
     'βυθόν-ja (βυθός) a מְצוֹלֹת (mecólót) megfelelője'),
    ('2Móz 15:8', 'κύματα', 'κῦμα', 'kümata', 'hullám', 'a héber „mélységek” helyén „hullámok” (κύματα) áll'),
    ('Péld 8:27', '', '', '', '', 'a „mélységek színén” (עַל־פְּנֵי תְהוֹם) helyén a görög azt írja, hogy „kijelölte a maga trónját a szeleken” '
     '(ἀφώριζεν τὸν ἑαυτοῦ θρόνον ἐπ᾿ ἀνέμων): a mélység szava nincs a versben'),
    ('Péld 8:28', '', '', '', '', 'a „mélység forrásai” (עִינוֹת תְהוֹם) helyén a görög „az ég alatti források” '
     '(πηγὰς τῆς ὑπ᾿ οὐρανόν) kifejezést írja: a mélység szava nincs a versben'),
]
ki = os.path.join(GYOKER, 'naplok', 'F239_U1b_lxx_kinyert.tsv')
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\t'.join(OSZLOP) + '\n')
    for i, a, l, k, j, m in SOROK:
        r = {'motivum': M, 'strong': 'H8415', 'igehely': i, 'forras': 'lxx', 'alak': a, 'lemma': l, 'kiejtes': k,
             'jelentes': j, 'betoldas': 'nem', 'megjegyzes': m, 'kinyeres': 'modell', 'modell': MODELL, 'ellenorzes': '',
             'proveniencia': 'scope=K66 modell-kinyerés: LXX_OS versszöveg + TAHOT (a gépi kinyerés nem volt egyértelmű) | '
             'forras=konkordancia/LXX_OS (lxx-morph, CC BY 4.0) | ts=%s' % TS}
        f.write('\t'.join(r[o] for o in OSZLOP) + '\n')
print(ki)
