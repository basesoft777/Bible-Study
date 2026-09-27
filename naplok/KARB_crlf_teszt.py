import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

"""
KARB_crlf_teszt.py -- KARBANTARTAS_BRIEF.md SS1 (CRLF-tures) merőszkriptje
a KB2 4 erintett soraahoz.

A brief merceje soronkenti ("sor"): minden erintett szkript egyetlen,
a mezobontast kozvetlenul vegzo sorat vizsgalja -- azt, amelyiket a KB0
mar azonositott (l. naplok/KARB_KB0_kiindulas.md 0.4). A teszt egy
LF-vegu es egy CRLF-vegu szintetikus ket-mezos sort futtat at a REGI
(rstrip("\\n")) es az UJ (rstrip("\\r\\n")) valtozaton, es megnezi,
bennemarad-e a \\r az utolso mezoben.

A negyedik szkriptnel (tahot_zarojeles_phaseA_kivonat.py) a sor 12
tab-elvalasztott mezot var (fields[11] a legutolso, "Expanded" mezo) --
a szintetikus sor ezt a szerkezetet koveti.
"""


def regi_ket_mezos(sor_szoveg):
    """A KB0 elotti alak: elofordulas_szamlalo.py:37, f3_4_zaro_ellenoriz.py:17
    (regi allapotaban), frazis_kereses_pozicio_alapon.py:58."""
    return sor_szoveg.rstrip("\n").split("\t")


def uj_ket_mezos(sor_szoveg):
    """A KB2 utani alak (G3): rstrip("\\r\\n")."""
    return sor_szoveg.rstrip("\r\n").split("\t")


def regi_tahot(sor_szoveg):
    """tahot_zarojeles_phaseA_kivonat.py:84 regi allapota: line.rstrip('\\n')."""
    line = sor_szoveg.rstrip("\n")
    return line.split("\t")


def uj_tahot(sor_szoveg):
    """tahot_zarojeles_phaseA_kivonat.py:84 uj allapota: line.rstrip('\\r\\n')."""
    line = sor_szoveg.rstrip("\r\n")
    return line.split("\t")


def van_r(mezok):
    return any("\r" in m for m in mezok)


def main():
    eredmenyek = []

    # 1-3. ket-mezos sorok (Strong-szam vagy hasonlo az UTOLSO mezoben)
    ketmezos_esetek = [
        ("elofordulas_szamlalo.py", 37, "Gen.1.1\tG1941"),
        ("f3_4_zaro_ellenoriz.py", 17, "1Móz 1:1\tteremté"),
        ("frazis_kereses_pozicio_alapon.py", 58, "Gen.1.1\tH7225"),
    ]
    for szkript, sor, adatsor in ketmezos_esetek:
        crlf_sor = adatsor + "\r\n"
        regi_mezok = regi_ket_mezos(crlf_sor)
        uj_mezok = uj_ket_mezos(crlf_sor)
        regi_eredmeny = "HIBAS: utolso mezo = %r" % regi_mezok[-1] if van_r(regi_mezok) else "OK"
        uj_eredmeny = "HIBAS: utolso mezo = %r" % uj_mezok[-1] if van_r(uj_mezok) else "OK"
        eredmenyek.append((szkript, sor, regi_eredmeny, uj_eredmeny))
        print("%s:%d | LF-en mindket valtozat OK (nem tesztelt itt, trivialis) | CRLF-en: regi=%s, uj=%s"
              % (szkript, sor, regi_eredmeny, uj_eredmeny))

    # 4. tahot_zarojeles_phaseA_kivonat.py -- 12 mezos raw TAHOT-sor,
    #    fields[11] ("Expanded") az utolso mezo.
    raw_12mezo = "\t".join([
        "Gen.1.1#1=x",       # fields[0] -- REF_RE-nek megfelelo (nem hasznaljuk itt kulon)
        "heber", "translit", "translation", "dStrongs",
        "f5", "f6", "f7", "f8", "f9", "f10",
        "H0430=El=Isten",    # fields[11] -- Expanded mezo
    ])
    crlf_raw = raw_12mezo + "\r\n"
    regi_mezok_t = regi_tahot(crlf_raw)
    uj_mezok_t = uj_tahot(crlf_raw)
    regi_eredmeny_t = "HIBAS: fields[11] = %r" % regi_mezok_t[11] if "\r" in regi_mezok_t[11] else "OK"
    uj_eredmeny_t = "HIBAS: fields[11] = %r" % uj_mezok_t[11] if "\r" in uj_mezok_t[11] else "OK"
    eredmenyek.append(("tahot_zarojeles_phaseA_kivonat.py", 84, regi_eredmeny_t, uj_eredmeny_t))
    print("tahot_zarojeles_phaseA_kivonat.py:84 | CRLF-en: regi=%s, uj=%s"
          % (regi_eredmeny_t, uj_eredmeny_t))

    # LF-teszt kontrollkent: mindket valtozatnak hibatlannak kell lennie
    # LF-vegu bemeneten (nincs regresszio a nem-CRLF esetre).
    print("\nLF-kontroll (mindket valtozatnak OK-nak kell lennie):")
    for szkript, sor, adatsor in ketmezos_esetek:
        lf_sor = adatsor + "\n"
        r = regi_ket_mezos(lf_sor)
        u = uj_ket_mezos(lf_sor)
        print("  %s:%d | regi=%s | uj=%s" % (
            szkript, sor,
            "OK" if not van_r(r) else "HIBAS", "OK" if not van_r(u) else "HIBAS"))
    lf_raw = raw_12mezo + "\n"
    r_t = regi_tahot(lf_raw)
    u_t = uj_tahot(lf_raw)
    print("  tahot_zarojeles_phaseA_kivonat.py:84 | regi=%s | uj=%s" % (
        "OK" if "\r" not in r_t[11] else "HIBAS", "OK" if "\r" not in u_t[11] else "HIBAS"))

    ki = "naplok/KARB_KB2_crlf.tsv"
    with open(ki, "w", encoding="utf-8", newline="\n") as f:
        f.write("szkript\tsor\tregi_eredmeny_CRLF\tuj_eredmeny_CRLF\n")
        for szkript, sor, regi_e, uj_e in eredmenyek:
            f.write("%s\t%d\t%s\t%s\n" % (szkript, sor, regi_e, uj_e))
    print("\nEredmenytabla: %s" % ki)


if __name__ == "__main__":
    main()
