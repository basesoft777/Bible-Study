import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# nem-zsoltar (KK1-bol)
nem_zsolt = Counter()
with open("naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 5:
            continue
        nem_zsolt[parts[4]] += 1

# zsoltar (KK1b-bol)
zsolt = Counter()
with open("naplok/KAROLI_KK1b_ok_besorolas.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 5:
            continue
        zsolt[parts[4]] += 1

print("Nem-Zsoltar:", dict(nem_zsolt), "osszesen:", sum(nem_zsolt.values()))
print("Zsoltar:", dict(zsolt), "osszesen:", sum(zsolt.values()))

nz_meg = nem_zsolt.get("H1_importer_kezi_none_fallthrough", 0) + nem_zsolt.get("H2_karoli_mt_szamozas", 0)
nz_nem = nem_zsolt.get("H3_egyeb_karoli_sajatossag", 0) + nem_zsolt.get("H5_valodi_verstartalmi_elteres", 0)
z_meg = zsolt.get("H1_importer_kezi_none_fallthrough", 0) + zsolt.get("H2_karoli_mt_szamozas", 0)
z_nem = zsolt.get("H3_egyeb_karoli_sajatossag", 0) + zsolt.get("H5_valodi_verstartalmi_elteres", 0)

osszes_mert = sum(nem_zsolt.values()) + sum(zsolt.values())
osszes_meg = nz_meg + z_meg
osszes_nem = nz_nem + z_nem

print(f"\nOsszesen mert vers: {osszes_mert}")
print(f"Megoldodna (H1+H2): {osszes_meg} ({100*osszes_meg/osszes_mert:.1f}%)")
print(f"Nem oldodik meg (H3+H5): {osszes_nem} ({100*osszes_nem/osszes_mert:.1f}%)")
