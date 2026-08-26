#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase A: TAHOT nyers -> STEPBible-kulcsos kivonat sorok generalasa (regi formatum),
a jelenlegi (README szerinti) modszertan alapjan, DE a zarojeles kettos hivatkozasu
sorokat is feldolgozva (nem dobja el oket).

Kimenet: minden generalt sor mezoi:
  ref_primary (pl. "Gen.1.1"), ref_secondary (pl. "Gen.32.1" vagy None),
  strong, hebrew, translit, gloss_short(=Rovid jelentes), root(=Szoto), english(=Angol tukorforditas)

Ezt hasznaljuk (a) regresszios ellenorzesre a meglevo TAHOT_kivonat.tsv-vel szemben
(csak a nem zarojeles sorokra), es (b) alapul a vegso, Karoli-kulcsos kivonathoz.
"""
import re, sys, os, csv

RAW_DIR = os.path.dirname(os.path.abspath(__file__)) + "/tahot"
RAW_FILES = ["GenDeu.txt", "JosEst.txt", "JobSng.txt", "IsaMal.txt"]

REF_RE = re.compile(r'^([A-Za-z0-9]+)\.(\d+)\.(\d+)(\((\d+)\.(\d+)\))?#(\d+)=(.*)$')

def clean_strong(seg):
    """dStrongs / Root Strong szegmensbol tiszta Strong-szamot general."""
    seg = seg.strip()
    if not seg:
        return None
    # {..} zarojel eltavolitasa
    seg = seg.replace('{', '').replace('}', '')
    if not seg:
        return None
    # + vegzodes (folytatodo cimke jelzese) levagasa
    if seg.endswith('+'):
        seg = seg[:-1]
    if not seg:
        return None
    # nem H-szammal kezdodik -> nem valodi Strong (pl ures Ketiv/Qere helyorzo)
    m = re.match(r'^H(\d{4})[A-Za-z]*(_[A-Za-z0-9]+)?$', seg)
    if not m:
        return None
    return 'H' + m.group(1)


def parse_expanded(seg):
    """STRONG=SZOTO=GLOSSZ szegmensbol (root, short_gloss) part."""
    seg = seg.strip()
    if not seg:
        return None, None
    seg = seg.replace('{', '').replace('}', '')
    if seg.endswith('+'):
        seg = seg[:-1]
    parts = seg.split('=', 2)
    if len(parts) < 3:
        return None, None
    strong_part, root, gloss = parts[0], parts[1], parts[2]
    # rovid jelentes: ha van "»", az utana / a kovetkezo ":" vagy "@" elotti resz
    if '»' in gloss:
        after = gloss.split('»', 1)[1]
        # levagjuk : vagy @ elott
        m = re.match(r'^([^:@]*)', after)
        short = m.group(1).strip() if m else after.strip()
    else:
        short = gloss
    # vezeto ": " levagasa
    short = re.sub(r'^:\s*', '', short).strip()
    return root.strip(), short


def split_bs(s):
    """Backslash menten vagas - csak az elso resz (szo resz) kell."""
    return s.split('\\')[0]


def process_raw_file(path, rows_out):
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) < 12:
                continue
            ref_field = fields[0]
            m = REF_RE.match(ref_field)
            if not m:
                continue
            book, chap, verse = m.group(1), m.group(2), m.group(3)
            chap2, verse2 = m.group(5), m.group(6)
            primary = f"{book}.{chap}.{verse}"
            secondary = f"{book}.{chap2}.{verse2}" if chap2 else None

            hebrew_f = fields[1]
            translit_f = fields[2]
            translation_f = fields[3]
            dstrongs_f = fields[4]
            expanded_f = fields[11]

            # backslash vagas (irasjel levalasztasa) a Hebrew / dStrongs / Expanded mezokon
            hebrew_w = split_bs(hebrew_f)
            dstrongs_w = split_bs(dstrongs_f)
            expanded_w = split_bs(expanded_f)
            translit_w = translit_f  # nincs irasjel-szegmens
            translation_w = translation_f

            heb_segs = hebrew_w.split('/')
            translit_segs = translit_w.split('/')
            translation_segs = translation_w.split('/')
            dstr_segs = dstrongs_w.split('/')
            exp_segs = expanded_w.split('/')

            n = len(heb_segs)
            # igazitas: ha a tobbi oszlop szegmensszama elter, ismeteljuk/ures-kitoltjuk
            def get(seglist, i):
                if i < len(seglist):
                    return seglist[i]
                return ''

            for i in range(n):
                strong = clean_strong(get(dstr_segs, i))
                if strong is None:
                    continue  # Ketiv/Qere ures helyorzo vagy nem-Strong szegmens
                heb = get(heb_segs, i).strip()
                translit = get(translit_segs, i).strip()
                translation = get(translation_segs, i).strip()
                root, short_gloss = parse_expanded(get(exp_segs, i))
                if root is None:
                    root = ''
                if short_gloss is None:
                    short_gloss = ''
                rows_out.append((primary, secondary, strong, heb, translit, root, short_gloss, translation))


def main():
    rows = []
    for fn in RAW_FILES:
        process_raw_file(os.path.join(RAW_DIR, fn), rows)
    print(f"Osszesen generalt sor (paren-nel egyutt): {len(rows)}", file=sys.stderr)
    out_path = os.path.dirname(os.path.abspath(__file__)) + "/phaseA_all.tsv"
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['ref_primary','ref_secondary','strong','hebrew','translit','root','short_gloss','english'])
        for r in rows:
            w.writerow(r)
    print("Kiirva:", out_path, file=sys.stderr)


if __name__ == '__main__':
    main()
