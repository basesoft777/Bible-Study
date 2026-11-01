# Főállású, átalányadózó, alanyi áfamentes egyéni vállalkozó – éves levezetés (2026, becslés).
MINBER_HO = 322_800
ADOMENTES = MINBER_HO * 12 // 2          # 1 936 800
KOLTSEGHANYAD = 0.45
def szamol(fo, havi_ar, eves_szamlazas):
    brutto = fo * havi_ar * 12
    tranz = fo * (1 if eves_szamlazas else 12)
    fizdij = brutto * 0.015 + tranz * 85            # Stripe EU kártya (harmadik feles adat)
    szamlazo = 29_880 + (tranz * 0)                  # Számlázz.hu #digital; API-díj ismeretlen
    konyvelo = 20_000 * 12
    hipa = brutto * 0.8 * 0.02                       # becslés: egyszerűsített alap, 2%
    kamara = 5_000
    jov = brutto * (1 - KOLTSEGHANYAD)
    adokoteles = max(jov - ADOMENTES, 0)
    szja = adokoteles * 0.15
    jar_alap = max(adokoteles, MINBER_HO * 12)       # főállás: legalább minimálbér
    tb = jar_alap * 0.185
    szocho = jar_alap * 0.13
    koltseg = fizdij + szamlazo + konyvelo + hipa + kamara
    ado = szja + tb + szocho
    netto = brutto - koltseg - ado
    return dict(brutto=brutto, fizdij=fizdij, szamlazo=szamlazo, konyvelo=konyvelo, hipa=hipa,
                kamara=kamara, jov=jov, adokoteles=adokoteles, szja=szja, jar_alap=jar_alap,
                tb=tb, szocho=szocho, netto=netto)
def e(x): return f"{x/1000:,.0f} e".replace(",", " ")
print("== Levezetés: 300 fő × 2 000 Ft/hó, havi számlázás ==")
r = szamol(300, 2000, False)
for k in ["brutto","fizdij","szamlazo","konyvelo","hipa","kamara","jov","adokoteles","szja","jar_alap","tb","szocho","netto"]:
    print(f"{k:12s} {e(r[k]):>12s}")
print()
print("== Forgatókönyvek (nettó/hó a zsebedben) ==")
for fo in (50, 100, 200, 300, 500):
    h = szamol(fo, 2000, False); y = szamol(fo, 2000, True)
    print(f"{fo:4d} fő  bruttó {e(h['brutto']/12):>8s}/hó  havi szla: {e(h['netto']/12):>8s}/hó   éves szla: {e(y['netto']/12):>8s}/hó")
# fedezeti pont: hány fő kell, hogy a nettó elérje a nullát / 200e / 300e
for cel in (0, 200_000, 300_000):
    fo = 1
    while szamol(fo, 2000, True)['netto']/12 < cel: fo += 1
    print(f"Nettó {cel/1000:.0f} e Ft/hó eléréséhez (éves számlázás): {fo} fő")
