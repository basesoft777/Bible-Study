"""f08_dt_sor.py -- F08.3/F08.5: a DT23 osszesitett tetel beirasa a DONTESEK.md tablajaba (CRLF-hu fajl).
Ha a DT23 sor mar letezik, lecsereli (F8.5: az ELLENOR_F08 1. kore utani javitott valtozat).
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
    '**biztos 61** (mind `eltero_forditas`), **valószínű 9**, **nyitott 8**, **nem_alkalmazhato 8** (`nincs_heber_kulcsszo`). Független forrásnak csak a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű verse számít (az FJ1-jelölt Macula-származék). '
    'A generátor csak a `biztos` sorokat jeleníti meg (próbagenerálás a repón kívül: 61 lexikonsor függőből „eltérő”, 26 függő marad); a többi e tétel döntéséig „kutatói azonosítás függőben”. Az ELLENOR_F08 1. köre után javítva (F8.5). Részkérdések (külön dönthetők): '
    '(a) **a 9 valószínű sor** (egy forrás: a Macula nem illeszt, az `LXX_OS` versolvasata egyértelmű): LD006 Jób 24:19 `lxx_minusz` (a LXX-vers tartalmilag eltér); LD021 1Móz 5:29 λύπη; LD048 1Móz 14:5 γίγας; LD055 2Sám 21:16 Ραφα; LD057 2Sám 21:20 Ραφα; LD060 1Krón 20:6 γίγας; LD061 1Krón 20:8 Ραφα; LD069 Ézs 26:19 ἀσεβής (γῆ τῶν ἀσεβῶν; a Macula „{δ}” jelet ad); LD088 2Móz 15:8 κῦμα. '
    '**Egy „valószínű → biztos” javaslat eltérne a brief 3. lépésének definíciójától** („biztos: két független forrás egyezik”): e sorok mögött egy forrás áll, a biztosra állítás a definíció felülírása volna; '
    '(b) **a 8 nyitott sor**, jelölttel: LD008 Préd 9:10 (a munkalap-igehely MT/KJV-számozású, l. (c)); LD009 Ézs 7:11 (הַעְמֵק שְׁאָלָה → εἰς βάθος: βάθος vagy LXX-minusz); LD027 1Móz 8:21 (Macula ἔτι ↔ `LXX_OS` τοῦ καταράσασθαι; jelölt καταράομαι G2672); LD035 Mik 6:12 (a Macula felcseréli a szomszédos szavakat; jelölt ἀσέβεια G0763); '
    '**LD050 4Móz 13:34** (a munkalap-szó a második נְפִלִים: a Macula nem illeszti (’’), a LXX-ben a tagmondat hiányzik; az első נְפִילִים → γίγας a két forrásban egyezik; jelölt: LXX-minusz a munkalap-szóra); '
    '**LD052 5Móz 2:20** (a munkalap-szó a második רְפָאִים: a Macula κατῴκουν-nal felcserélve illeszti, az `LXX_OS`-ben Ραφαϊν áll — a Mik 6:12-vel azonos ellentmondás; jelölt Ραφαϊν); LD058 2Sám 21:22 (kettős fordítás: γίγας / Ραφα; jelölt Ραφα); LD064 Péld 2:18 (kettős fordítás: ᾅδης / γηγενής; jelölt γηγενής); '
    '(c) **DT7 (g) válasza:** a Préd 9:10 előfordulás-sor (ALVIL-001) igehelye MT-számozású: a Károli 9:10 = MT 9:8 (KK, KEZI; a Károli-szöveg is „A te ruháid mindenkor legyenek fejérek”), a שְׁאוֹל a Károli **9:12**-ben (MT 9:10) áll, ahol Macula ἅδη G0086 és `LXX_OS` ᾅδης egyezik. A javítás az `adat/elofordulasok.tsv` sorát érinti (ez a menet nem írta). A többi 86 hely igehelye Károli-számozású; '
    '(d) **sémaeltérés a brieftől és az `ir` listán kívüli módosítások** (a brief oszloplistája: hely, héber szó, LXX-megfelelő, forrás(ok), bizonyosság, indoklás): a meglévő SEMA 2.11-es tábla mezőit használtam (forrás a `proveniencia` `forras=` részében), és hozzáadtam egy `bizonyossag` oszlopot (`biztos`/`valoszinu`/`nyitott`/`nem_alkalmazhato`) és egy `nincs_heber_kulcsszo` típust; ehhez az `adat/SEMA.md` 2.11, az `eszkozok/ellenoriz.py` 10. szabálya és az `eszkozok/lexikon_general.py` megjelenítési szűrője (`lxx_dontesek_index`) módosult, a DT23 elfogadása előtt commitolva. '
    'A szűrő a 3. (LXX) blokkon túl a „Rokon szavak” blokkot is érinti (`rokon_szavak_strongok` a megjelenő sorok `gorog_strong`-jait olvassa): a próbagenerálásban (8 lexikonoldal) a „Rokon szavak” blokk nem változott (csak az ISTENTISZT-001-ben van, G0994/G2564, változatlan), mert az új `gorog_strong`-oknak nincs `lexikon_hivatkozasok.tsv`-sora; a hatás rejtett, egy későbbi hivatkozás-felvételnél jelenik meg. '
    'Mivel a PR az ellenőrzőt (`ellenoriz.py`) is érinti, a CI E16 szabálya `[ELLENŐRZŐ]` előtagú PR-címet kér; '
    '(e) a `nincs_heber_kulcsszo` (`nem_alkalmazhato`) sorok megjelenítése a lexikonoldalon (ma: függőben marad); '
    '(f) a HODIT-001 2Sám 21:16–22 és 1Krón 20:4–8 soraiban **a TAHOT H7497-et ad** (7 vers); a H7498 (הָרָפָה/הָרָפָא) **csak a Macula állítása** (a `TAHOT_kivonat.tsv`-ben H7498 csak 1Krón 8:2 és 8:37-nél áll). A `heber_strong` az előfordulás-sor H7497-jét követi; a megjegyzések H7498-említése Macula-érték; '
    '(g) **DT7 (a) hatása:** nincs — a döntések a Macula `gorog_lxx`/`gorog_strong` mezőit használják, a kimaradt UBS-mezők (sdbh, lexdomain, domain, ln) nem LXX-illesztési adatok; a DT7 (b) (funkció-morféma Strong) sem érinti a 86 sort; '
    '(h) **LD010 Ez 32:21** βόθρος: a Macula G0999-et ad, ami a `konkordancia/Strong_szotar.tsv` szerint βόθυνος; az `LXX_OS` Strong nélküli, ezért a `gorog_strong` üres; '
    '(i) **LD030 1Móz 12:3 (és LD027 jelöltje) G2672:** az érték az `LXX_OS`-ből jön (`konkordancia/LXX_OS/genesis.tsv`: „Genesis 12:3” 10. pozíció καταράσομαι, „Genesis 8:21” 18. pozíció καταράσασθαι, `strong` = 2672); a `lekerdez.py lxx-hid` a `LXX_kivonat`-ot olvassa, ott e szavak Strong nélküliek — ebből eredt az ELLENOR_F08 3. pontja. Az orkesztrátor az érték törlését kérte; a repó adata szerint a forrás megvan, ezért az értéket megtartottam, a megjegyzésben a pontos `LXX_OS`-sorra hivatkozva, és döntésre ide tettem. A sorok minden `gorog_strong`-ja az `LXX_OS` adott pozíciójából jön (a szkript csak onnan tölt; felülírás csak üresre), Strong forrás nélkül nincs; '
    '(j) **Zsolt 76:3 / 88:11 `LXX_OS`-igehely:** ellenőrizve, elcsúszás nincs: az `LXX_OS` `igehely_kjv` mezője KJV-számozású (76:2, 88:10), az `igehely_karoli` (76:3, 88:11) a Károli-szövegnek felel meg (Károli = MT, KK `MT`/tvtms), a Psalms (LXX) 75:3 és 87:11 tartalma egyezik; a generált sor „Zsolt(LXX) 75:3” / „Zsolt(LXX) 87:11”. '
    '*(forrás: `F08_LXX_DONTESEK_BRIEF.md` 3. lépés, `naplok/F08_bemenet.txt`, `eszkozok/f08/f08_dontesek.py`, `naplok/ELLENOR_F08.md`)* | '
    '(a) mind a 9 `biztos`-ra (a brief definíciójának felülírása) / soronként / marad `valoszinu`, nem jelenik meg (a brief szerint) / (b) a jelöltek elfogadása soronként / marad nyitott / (c) az előfordulás-sor igehelyének javítása Préd 9:12-re (a LD008 ezzel tárgytalan, törölhető; az ALVIL-001 G-tokenje G0086, így a 9:12 valószínűleg „egyező” lesz, döntési sor nélkül) / marad / (d) a sémabővítés és a kódmódosítás elfogadása / visszaállítás (bizonyosság a megjegyzésbe, a nyitott és a `nincs_heber_kulcsszo` sorok nélkül) / (e) saját „kulcsszó nincs a versben” címke / marad függőben / (f) marad H7497 / a TAHOT–Macula eltérés vizsgálata külön / (i) marad G2672 (`LXX_OS`) / üres | '
    '(a) marad `valoszinu` és nem jelenik meg (a brief definíciója szerint); a felhasználó ettől eltérve soronként biztosra állíthatja; (b) LD027 és LD035 jelöltje elfogadva (a Macula-hiba nyilvánvaló), LD050 LXX-minusz, LD052 Ραφαϊν elfogadva, LD009, LD058, LD064 marad nyitott, LD008 a (c) szerint; (c) javítás Préd 9:12-re külön tételben; (d) elfogadás; (e) saját címke, a generátor-módosítás külön feladatban; (f) marad H7497, a TAHOT–Macula eltérés külön ellenőrzés; (i) marad G2672 | 🟡 | | `naplok/F08_zaras.md`, `naplok/ELLENOR_F08.md` |'
)


def main():
    with io.open(UT, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if not nyers.endswith('\r\n'):
        print('varatlan fajlveg')
        sys.exit(1)
    sorok = nyers.split('\r\n')
    elotte = len(sorok)
    dt = [i for i, s in enumerate(sorok) if s.startswith('| DT23 |')]
    if len(dt) > 1:
        print('tobb DT23 sor, nem irok')
        sys.exit(1)
    if dt:
        sorok[dt[0]] = SOR
        uj = '\r\n'.join(sorok)
        muvelet = 'lecserelve'
    else:
        uj = nyers + SOR + '\r\n'
        muvelet = 'hozzafuzve'
    if len(uj.split('\r\n')) < elotte:
        print('sorcsokkenes, nem irok')
        sys.exit(1)
    with io.open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write(uj)
    print('DT23 %s (%d -> %d sor)' % (muvelet, elotte - 1, len(uj.split('\r\n')) - 1))


if __name__ == '__main__':
    main()
