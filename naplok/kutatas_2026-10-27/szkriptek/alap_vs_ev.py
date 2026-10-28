# Alapítványi (részmunkaidős) munkaviszony vs. főállású átalányadós EV – nettó a zsebedben (becslés).
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ev", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "ev_levezetes.py"))
MINBER_HO = 322_800
def alapitvany(fo, ar=2000):
    brutto = fo * ar * 12
    fizdij = brutto * 0.015 + fo * 85            # éves befizetés
    fix = 25_000 * 12 + 3_000 * 12               # könyvelés + bank (becslés)
    elerheto = max(brutto - fizdij - fix, 0)
    ber = elerheto / 1.13                        # szocho 13%
    netto = ber * (1 - 0.185 - 0.15)
    return netto / 12, ber / 12
def ev(fo, ar=2000):
    import io, contextlib
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(spec.origin).read(), g)
    return g['szamol'](fo, ar, True)['netto'] / 12
for fo in (0, 50, 100, 150, 200, 300, 500):
    n, b = alapitvany(fo)
    print(f"{fo:4d} fő | alapítványi bér: bruttó {b/1000:6.0f} e, nettó {n/1000:6.0f} e/hó | EV főállás nettó {ev(fo)/1000:6.0f} e/hó")
