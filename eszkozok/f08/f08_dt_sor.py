"""f08_dt_sor.py -- F08.3: a DT23 osszesitett tetel hozzafuzese a DONTESEK.md tablajahoz (CRLF-hu fajl).
Futtatas: python eszkozok/f08/f08_dt_sor.py
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UT = os.path.join(GYOKER, 'DONTESEK.md')

SOR = (
    '| DT23 | #8 LXX-döntések (összesített) | '
    'A 87 függő hely 86 sort kapott az `adat/lxx_dontesek.tsv`-ben (LD005–LD090; a 4Móz 13:34 a HODIT-001 és a MENNY-001 közös sora): '
    '**biztos 71** (63 `eltero_forditas`, 8 `nincs_heber_kulcsszo`), **valószínű 9**, **nyitott 6**. Független forrásnak csak a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű verse számít (az FJ1-jelölt Macula-származék). '
    'A generátor csak a `biztos` sorokat jeleníti meg; a többi e tétel döntéséig „kutatói azonosítás függőben”. Részkérdések (külön dönthetők): '
    '(a) **a 9 valószínű sor** (egy forrás: a Macula nem illeszt, az `LXX_OS` versolvasata egyértelmű): LD006 Jób 24:19 `lxx_minusz` (a LXX-vers tartalmilag eltér); LD021 1Móz 5:29 λύπη; LD048 1Móz 14:5 γίγας; LD055 2Sám 21:16 Ραφα; LD057 2Sám 21:20 Ραφα; LD060 1Krón 20:6 γίγας; LD061 1Krón 20:8 Ραφα; LD069 Ézs 26:19 ἀσεβής (γῆ τῶν ἀσεβῶν; a Macula „{δ}” jelet ad); LD088 2Móz 15:8 κῦμα; '
    '(b) **a 6 nyitott sor**, jelölttel: LD008 Préd 9:10 (a munkalap-igehely MT/KJV-számozású, l. (c)); LD009 Ézs 7:11 (הַעְמֵק שְׁאָלָה → εἰς βάθος: βάθος vagy LXX-minusz); LD027 1Móz 8:21 (Macula ἔτι ↔ LXX τοῦ καταράσασθαι; jelölt καταράομαι G2672); LD035 Mik 6:12 (a Macula felcseréli a szomszédos szavakat; jelölt ἀσέβεια G0763); LD058 2Sám 21:22 (kettős fordítás: γίγας / Ραφα; jelölt Ραφα); LD064 Péld 2:18 (kettős fordítás: ᾅδης / γηγενής; jelölt γηγενής); '
    '(c) **DT7 (g) válasza:** a Préd 9:10 előfordulás-sor (ALVIL-001) igehelye MT-számozású: a Károli 9:10 = MT 9:8 (KK, KEZI; a Károli-szöveg is „A te ruháid mindenkor legyenek fejérek”), a שְׁאוֹל a Károli **9:12**-ben (MT 9:10) áll, ahol Macula ἅδη G0086 és `LXX_OS` ᾅδης egyezik. A javítás az `adat/elofordulasok.tsv` sorát érinti (ez a menet nem írta). A többi 86 hely igehelye Károli-számozású (a KK-kötés 4Móz 13:34-nél, Zsolt 74:20/76:3/88:11-nél is rendben); '
    '(d) **sémaeltérés a brieftől** (a brief oszloplistája: hely, héber szó, LXX-megfelelő, forrás(ok), bizonyosság, indoklás): a meglévő SEMA 2.11-es tábla mezőit használtam (forrás a `proveniencia` `forras=` részében), és hozzáadtam egy `bizonyossag` oszlopot és egy `nincs_heber_kulcsszo` típust (8 sor: ige-tartományú előfordulás-sor olyan verse, amelyben a kulcsszó nem áll, ill. tematikus sor); ehhez az `ellenoriz.py` 10. szabálya és a `lexikon_general.py` megjelenítési szűrője is módosult (a brief `ir` listáján kívül); '
    '(e) a `nincs_heber_kulcsszo` sorok megjelenítése a lexikonoldalon (ma: függőben marad); '
    '(f) a HODIT-001 2Sám 21:16–22 és 1Krón 20:6–8 soraiban a versben álló szó הָרָפָה/הָרָפָא H7498, az előfordulás-sor Strong-ja H7497 (a `heber_strong` az előfordulás-sorét követi, a `megjegyzes` jelzi); '
    '(g) **DT7 (a) hatása:** nincs — a döntések a Macula `gorog_lxx`/`gorog_strong` mezőit használják, a kimaradt UBS-mezők (sdbh, lexdomain, domain, ln) nem LXX-illesztési adatok; a DT7 (b) (funkció-morféma Strong) sem érinti a 86 sort. '
    '*(forrás: `F08_LXX_DONTESEK_BRIEF.md` 3. lépés, `naplok/F08_bemenet.txt`, `eszkozok/f08/f08_dontesek.py`)* | '
    '(a) mind a 9 elfogadva `biztos`-ként / soronként / marad `valoszinu` és nem jelenik meg / (b) a jelöltek elfogadása soronként / marad nyitott / (c) az előfordulás-sor igehelyének javítása Préd 9:12-re (a LD008 ezzel tárgytalan, törölhető; az ALVIL-001 G-tokenje ᾅδης, így a 9:12 valószínűleg „egyező” lesz, döntési sor nélkül) / marad / (d) a sémabővítés elfogadása / visszaállítás (bizonyosság a megjegyzésbe, a nyitott és a `nincs_heber_kulcsszo` sorok nélkül) / (e) saját „kulcsszó nincs a versben” címke / marad függőben / (f) a sorok Strong-ja H7498-ra / marad | '
    '(a) mind a 9 elfogadva, a `bizonyossag` `biztos`-ra állítva (a versolvasat egyértelmű, a Macula csak hallgat); (b) LD027 és LD035 jelöltje elfogadva (a Macula-hiba nyilvánvaló), LD009, LD058, LD064 marad nyitott, LD008 a (c) szerint; (c) javítás Préd 9:12-re külön tételben; (d) elfogadás; (e) saját címke, a generátor-módosítás külön feladatban; (f) külön ellenőrzés a HODIT-001 motívumnaplójában | 🟡 | | `naplok/F08_zaras.md` |'
)


def main():
    with io.open(UT, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '| DT23 |' in nyers:
        print('a DT23 mar szerepel, nem irok')
        return
    if not nyers.endswith('\r\n'):
        print('varatlan fajlveg')
        sys.exit(1)
    elotte = nyers.count('\r\n')
    uj = nyers + SOR + '\r\n'
    with io.open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write(uj)
    print('DT23 hozzafuzve (%d -> %d sor)' % (elotte, uj.count('\r\n')))


if __name__ == '__main__':
    main()
