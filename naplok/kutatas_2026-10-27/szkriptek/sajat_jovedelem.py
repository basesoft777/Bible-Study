# Becslés: mennyi jut a munkanélküli alapítónak évi bruttó befolyó támogatásból.
# Feltevések (nem ellenőrzött, könyvelővel egyeztetendő): 2026-os kulcsok.
MIN = 322_800 * 12          # minimálbér éves
ADOMENTES = 1_936_800       # átalányadó adómentes része
def alapitvany_koltseg(b):  # fizetési díj 2% + könyvelés 300e
    return b * 0.02 + 300_000
def munkaviszony(b):
    elerheto = b - alapitvany_koltseg(b)
    brutto = elerheto / 1.13            # szocho 13% a munkáltatónál
    netto = brutto * (1 - 0.185 - 0.15) # TB 18,5% + SZJA 15%
    return netto
def ev_atalany(b, alapitvanyon_at=True):
    bev = b - alapitvany_koltseg(b) if alapitvanyon_at else b - b*0.02
    jov = bev * 0.55                    # 45% költséghányad
    szja = max(jov - ADOMENTES, 0) * 0.15
    alap = max(jov - ADOMENTES, MIN)    # főállás: legalább minimálbér
    tb = alap * 0.185
    szocho = max(jov - ADOMENTES, MIN) * 0.13
    konyv = 200_000
    return bev - szja - tb - szocho - konyv
for b in (3_600_000, 7_200_000):
    print(f"Bruttó befolyó: {b/1e6:.1f} M Ft/év")
    print(f"  alapítványi munkaviszony:          {munkaviszony(b)/1e6:.2f} M/év  ({munkaviszony(b)/12/1e3:.0f} e/hó)")
    print(f"  EV átalány, alapítványnak számláz: {ev_atalany(b)/1e6:.2f} M/év  ({ev_atalany(b)/12/1e3:.0f} e/hó)")
    print(f"  EV átalány, közvetlen bevétel:     {ev_atalany(b,False)/1e6:.2f} M/év  ({ev_atalany(b,False)/12/1e3:.0f} e/hó)")
