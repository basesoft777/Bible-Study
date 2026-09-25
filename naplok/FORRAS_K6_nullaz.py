import sys
import re
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# K6: a Strong-szamok nullazva (SEMA 1.2: H/G + 4 szamjegy, balrol nullazva).
# Ez a szkript a FJ1/FJ3 munkalapok Strong-oszlopait normalizalja utolagosan.

num_re = re.compile(r"^(\d+)([a-z]?)$")


def pad(token, prefix=""):
    token = token.strip()
    if not token:
        return token
    m = num_re.match(token)
    if not m:
        return token
    digits, suffix = m.groups()
    return f"{prefix}{digits.zfill(4)}{suffix}"


def pad_list(cell, prefix=""):
    if not cell:
        return cell
    parts = cell.split(",")
    return ",".join(pad(p, prefix) for p in parts)


def process_file(path, columns):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    header = lines[0].rstrip("\n").split("\t")
    out_lines = [lines[0]]
    for line in lines[1:]:
        cells = line.rstrip("\n").split("\t")
        for col_name, prefix, is_list in columns:
            if col_name in header:
                idx = header.index(col_name)
                if idx < len(cells):
                    val = cells[idx]
                    if prefix and val.startswith(prefix):
                        val = val[len(prefix):]
                    if is_list:
                        cells[idx] = pad_list(val, prefix)
                    else:
                        cells[idx] = pad(val, prefix)
        out_lines.append("\t".join(cells) + "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"OK: {path}")


process_file("naplok/FORRAS_FJ1_lxx_jeloltek.tsv", [
    ("heber_strong", "H", False),
    ("javasolt_gorog_strong", "G", False),
])
process_file("naplok/FORRAS_FJ1_mtlxx_teszt.tsv", [
    ("vart_strong", "G", False),
    ("vers_strongjai", "G", True),
])
process_file("naplok/FORRAS_FJ1_macula_teszt.tsv", [
    ("vart_strong", "G", False),
    ("vers_strongjai", "G", True),
])
process_file("naplok/FORRAS_FJ3_bsb_minta.tsv", [
    ("tahot_strongok", "H", True),
    ("bsb_strongok", "H", True),
])
