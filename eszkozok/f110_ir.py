#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f110_ir.py — F110.4-5: a jóváhagyott DT-F110a szabály és a kézi olvasás eredményének
beírása az adat/jeloltek.tsv-be. Új sor csak `nyitva`; a 21 G1941-sor dontes/indoklas/datum
mezője változik. Írás előtt/után soronkénti összevetés: minden más sor bájtra azonos.
Olvasás/írás: split('\t') / '\t'.join (nem csv), bájt-szinten (sorvég megőrizve).
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATUM = '2026.10.21'
ID = 'ISTENTISZT-001'
FK_H = ('kollokacio H7121 H8034 | scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv '
        '| strong=H7121+H8034 | n=196 | ts=2026-10-21T09:18Z | csatorna=cli')

# kézi olvasás: a szűrőn átjutott héber helyek (csak nyitva), igehely a konyv_normalizalo_tabla szerint
HEBER_NYITVA = {
    'JSir 3:55': 'F110 szűrő (DT-F110a), K2 HATÁRESET, kézi olvasás: „segítségül hívtam a nevedet, Uram” (TAHOT: „I called name your O Yahweh”) — aktív ige, a שֵׁם Istené, funkció: hívás a gödörből; בְּ nincs, tárgyas szerkezet (קָרָא + שֵׁם + יְהוָה). Elbírálatlan: a motívum-menet dönt',
    '5Móz 32:3': 'F110 szűrő (DT-F110a), K2 HATÁRESET, kézi olvasás: „az Úr nevét hirdetem” (TAHOT: „the name of Yahweh I will proclaim”) — aktív ige, a שֵׁם Istené, funkció: kikiáltás-imádás (a 2Móz 33:19 és 34:5 בְּ-es párja); בְּ nincs. Elbírálatlan: a motívum-menet dönt',
    'Ézs 41:25': 'F110 szűrő (DT-F110a), B osztály, kézi olvasás: „napkelet felől (az) hívja a nevemet” (TAHOT: „from [the] rising of [the] sun he will call on name my”) — aktív קרא + בְּ + שֵׁם, az Úr a beszélő; értelmezés vitatott (Círusz hívja-e az Úr nevét). A szabály átengedi; elbírálatlan, a motívum-menet dönt',
    'Ézs 64:6': 'F110 szűrő (DT-F110a), B osztály, kézi olvasás: „nincs, aki segítségül hívja a nevedet” (TAHOT: „there not [is one who] calls on name your”) — aktív קרא + בְּ + שֵׁם, Isten neve, tagadott invokáció (a beépített Jer 10:25 precedens). Elbírálatlan: a motívum-menet dönt',
}
# a kiszűrt (nem íródó) héber helyek kézi okai (naplóba)
HEBER_ELUTASIT = {
    'Ézs 45:3': 'A osztály, kézi: Isten hívja Círust névvel („who calls by name your”) — az alany az Úr, nem invokáció',
    'Ézs 44:5': 'B, kézi: önazonosítás Jákob nevével, nem Isten neve',
    'Ézs 40:26': 'B, kézi: Isten névvel szólítja a csillagokat',
    'Ézs 43:1': 'B, kézi: Isten névvel szólítja Izraelt',
    'Ézs 45:4': 'B, kézi: Isten névvel szólítja Círuszt',
    '1Krón 6:65': 'B, kézi: városok megnevezése',
    'Józs 21:9': 'B, kézi: városok megnevezése',
    '4Móz 32:38': 'B, kézi: városok átnevezése',
    '4Móz 32:42': 'B, kézi: névadás (Nóbah)',
    'Bír 18:29': 'B, kézi: névadás (Dán városa)',
    '2Móz 31:2': 'B, kézi: Becalél névvel szólítása',
    '2Móz 35:30': 'B, kézi: Becalél névvel szólítása',
    '1Móz 16:13': 'K2 HATÁRESET, kézi: névadás (Hágár megnevezi az Urat)',
    '2Móz 17:15': 'K2 HATÁRESET, kézi: névadás (az oltár neve)',
}
GORKEZI = {
    'ApCsel 7:59': ('nyitva', 'F110 szűrő (DT-F110a), A osztály, kézi olvasás: István „hívja az Urat” (ἐπικαλούμενον … κύριε Ἰησοῦ) — aktív/középigés invokáció, a hívott Jézus; a besorolás a motívum-menetben dől el (nyitva marad)'),
    '2Kor 1:23': ('elutasítva', 'F110 szűrő (DT-F110a), A osztály, kézi olvasás: „Istent hívom tanúul a lelkemre” — esküformás tanúhívás, nem segítségül hívás/imádság; negatív kritérium: nem invokáció'),
    'Mt 10:25': ('elutasítva', 'F110 szűrő (DT-F110a), B osztály, kézi olvasás: „Beelzebubnak hívták a házigazdát” — megnevezés, nem invokáció; negatív kritérium: passzív/megnevezés jellegű használat'),
}


def main():
    p = ROOT / 'adat/jeloltek.tsv'
    raw = p.read_bytes()
    lines = raw.split(b'\n')
    tail_empty = lines[-1] == b''
    if tail_empty:
        lines = lines[:-1]
    eredeti = list(lines)
    sim = {}
    for l in open(ROOT / 'naplok/F110_szuro_szimulacio.tsv', encoding='utf-8'):
        if l.startswith('#') or l.startswith('csoport'):
            continue
        c = l.rstrip('\n').split('\t')
        sim[(c[0], c[1])] = c
    modositott, utolso_elof = [], None
    for n, b in enumerate(lines):
        eol = b'\r' if b.endswith(b'\r') else b''
        f = b[:len(b) - len(eol)].decode('utf-8').split('\t')
        if b.startswith(b'#') or f[0] == 'id':
            continue
        if len(f) != 13:
            sys.exit('mezoszam != 13: sor %d' % (n + 1))
        if f[0] == ID and f[9] == 'elofordulas':
            utolso_elof = n
        if f[0] == ID and f[2].startswith('scan G1941') and f[3] == 'nyitva' and ('G1941', f[1]) in sim:
            s = sim[('G1941', f[1])]
            if f[1] in GORKEZI:
                d, ind = GORKEZI[f[1]]
            else:
                if s[2] != 'K':
                    sys.exit('nem K osztály kézi nélkül: ' + f[1])
                d, ind = 'elutasítva', 'F110 szűrő (DT-F110a), %s: %s; negatív kritérium: passzív/megnevezés jellegű vagy jogi használat, nem aktív invokáció' % (s[3], s[4])
            f[3], f[4], f[8] = d, ind, DATUM
            lines[n] = ('\t'.join(f)).encode('utf-8') + eol
            modositott.append(n)
    if len(modositott) != 21:
        sys.exit('G1941 sorok: %d != 21' % len(modositott))
    eol = b'\r' if lines[utolso_elof].endswith(b'\r') else b''
    uj = []
    for ih, ind in HEBER_NYITVA.items():
        ref = ih if ih != 'JSir 3:55' else 'Sir 3:55'
        assert ('H7121+H8034', ref) in sim, ih
        f = [ID, ih, FK_H, 'nyitva', ind, '', '', '', DATUM, 'elofordulas', '', '', '']
        uj.append(('\t'.join(f)).encode('utf-8') + eol)
    kulcsok = {(x.split(b'\t')[0], x.split(b'\t')[1]) for x in eredeti if b'	' in x}
    for u in uj:
        k = tuple(u.split(b'\t')[:2])
        assert k not in kulcsok, k
    lines = lines[:utolso_elof + 1] + uj + lines[utolso_elof + 1:]
    # ellenőrzés: a nem érintett sorok bájtra azonosak, sorrendben
    mod = set(modositott)
    ki = [x for i, x in enumerate(lines) if not (utolso_elof < i <= utolso_elof + len(uj))]
    assert len(ki) == len(eredeti)
    for i, (a, b) in enumerate(zip(eredeti, ki)):
        if i not in mod:
            assert a == b, i
    p.write_bytes(b'\n'.join(lines) + (b'\n' if tail_empty else b''))
    print('modositott', len(modositott), 'uj', len(uj), 'sorok', len(eredeti), '->', len(lines))


if __name__ == '__main__':
    main()
