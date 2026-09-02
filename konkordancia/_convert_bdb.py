import json, re, html

data = json.load(open(r'C:\Users\bases\AppData\Local\Temp\DictBDB.json', encoding='utf-8'))

def strip_html(txt):
    txt = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', txt)
    txt = re.sub(r'<ref0[^>]*>(.*?)</ref0>', r'\1', txt)
    txt = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', txt)
    txt = re.sub(r'<heb>|</heb>', '', txt)
    txt = re.sub(r'<grk>|</grk>', '', txt)
    txt = re.sub(r'<sup>(.*?)</sup>', r'^\1', txt)
    txt = re.sub(r'<sub>(.*?)</sub>', r'_\1', txt)
    txt = re.sub(r'<i>|</i>', '', txt)
    txt = re.sub(r'<b>|</b>', '', txt)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'‎', '', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

rows = []
for item in data:
    top = item.get('top', '')
    m = re.match(r'^H(\d+)', top)
    if not m:
        continue  # kihagyja a "DictInfo" fejléc-bejegyzést
    num = int(m.group(1))
    padded = f"H{num:04d}" + top[len(m.group(0)):]  # pl. H8415, H90a -> H0090a
    plain = strip_html(item.get('def', ''))
    if plain:
        rows.append((padded, top, plain))

with open('BDB_teljes_unabridged.tsv', 'w', encoding='utf-8') as f:
    f.write("Strong_padded\tStrong_eredeti\tTeljes_szocikk\n")
    for padded, orig, plain in rows:
        f.write(f"{padded}\t{orig}\t{plain.replace(chr(9), ' ')}\n")

print(f"Kesz: {len(rows)} sor")
