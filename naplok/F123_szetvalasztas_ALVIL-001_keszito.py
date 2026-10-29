"""F123 X.M1: az ALVIL-001 leképezési táblájának előállítása (`naplok/F123_szetvalasztas_ALVIL-001.tsv`).

A tábla oszlopai a #11 `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv`-éi. A sorokat kézzel ítéltük meg
(a régi tematikus tanulmány és a kereszthivatkozás-napló minden nem üres, nem címsor blokkja; a vegyes
blokkok részegységekre bontva, DT84 (11); a 【NAPLO】-k egyenként, DT84 (10)). A szkript csak összerakja
a táblát, és ellenőrzi, hogy a hivatkozott sorok léteznek, és minden nem üres, nem címsor sor pontosan egy
blokkhoz tartozik (a részegységes blokkok egy sortartományt többször fednek, részenként).

    python naplok/F123_szetvalasztas_ALVIL-001_keszito.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = __file__.replace('\\', '/').rsplit('/naplok/', 1)[0] + '/'
T = 'tematikus_lezart/Hadesz_Seol_tematikus.md'
N = 'tematikus_lezart/naplok/Hadesz_Seol_kereszthivatkozas_naplo.md'
F = 'motivumok/ALVIL-001.md'
SABLON = 'sablon 9 v0.3 (tervezet; az első motívum a sablon-próba, DT-F123a)'

ARCH = 'a régi fájl változatlan, archív fejlécű példánya (archivum/ALVIL-001/, DT215, M3 előtt)'
STUDY = 'general.py --cel study (1. Előfordulások, ADAT-NÉZET) (forrás: adat/elofordulasok.tsv igehely, kapcsolodas, pardes_szint, megjegyzés)'


def fs(szakasz, szint, *tobb):
    return ' · '.join([F, 'sablon 9 §4 ' + szakasz, szint] + list(tobb))


# (fajl, szakasz, blokk, resz, tol, ig, kategoria, cel, indoklas)
S = [
    # ---------------- Hadesz_Seol_tematikus.md ----------------
    (T, '(fejléc)', 1, '', 1, 1, 'generalt', 'general.py --cel lexikon / motívumcikk (forrás: adat/motivumok.tsv cim, id)',
     'alap: sablon 9 §4 F — a cím (Hádész (Seól) — a halottak birodalma) a motivumok.tsv cim mezőjével azonos'),
    (T, 'Kivonat', 2, '', 5, 5, 'forras', fs('K Kivonat', 'olvasoi', 'jelölő: RÉS-KEZDET: kivonat'),
     'alap: sablon 9 §6 (a RÉS-jelölő szerkezeti; a res_forras.tsv kivonat-sorának tanulmany mezője a motivumok/ALVIL-001.md-re vált)'),
    (T, 'Kivonat', 3, '', 7, 7, 'forras', fs('K Kivonat', 'olvasoi'),
     'alap: értelmező összefoglaló. A benne álló számok adatból számoltak, ADAT-ÉRTÉK-kel ellenőrizendők: 64 ÓSZ-igehely = count(elofordulasok id=ALVIL-001, strong=H7585); „tíz ᾍδης-előfordulás” = a TAGNT G0086-scan száma (nem táblaszám: az adat 8 sora a Jel 20:13-14 tartományt egynek veszi, a Mt 16:18 elutasított jelölt) — az utóbbira ADAT-ÉRTÉK nem írható, a szám marad, proveniencia-lábjegyzettel (P)'),
    (T, 'Kivonat', 4, '', 9, 9, 'forras', fs('K Kivonat', 'olvasoi', 'jelölő: RÉS-VÉGE: kivonat'), 'alap: sablon 9 §6'),
    (T, '(fejléc alatti címsor)', 5, '', 11, 11, 'archivum', ARCH,
     'alap: DT84 (8), sablon 9 §7 (verzió-címke: adat, motivumok.tsv sablon_verzio/statusz_verzio) — a „Tematikus PaRDeS-tanulmány (4_ v14 szerint)” címsor a régi sablonverzió tanúsítása; a forrásban nem ismétlődik'),
    (T, '(fejléc alatti címsor)', 6, '', 13, 13, 'archivum', ARCH,
     'alap: L2 (eredet- és folyamatmondat) — a Tehom_Abusszosz_… fájlból való kiszervezés leírása; tartalmi állítást nem hordoz („Tartalmi következtetés nem változik”)'),
    (T, '(fejléc alatti címsor)', 7, '1', 15, 15, 'generalt', 'general.py --cel naplo (6. Napló-frissítés, ADAT-NÉZET) (forrás: adat/motivumok.tsv statusz, statusz_verzio, statusz_datum)',
     'alap: sablon 9 §4 6 — 1. részegység: a „v1” verzió-jelölés; a verzió ma a motivumok.tsv statusz_verzio (v2) mezőjében áll'),
    (T, '(fejléc alatti címsor)', 7, '2', 15, 15, 'archivum', ARCH,
     'alap: L2 — 2. részegység: a v1 keletkezés- és bővítéstörténete (2026.08.14, 08.25, 09.10); a bővítés tartalma (Jel 6:8; Luk 10:15/Mt 11:23) az elofordulasok.tsv sora'),
    (T, '(fejléc alatti címsor)', 8, '', 17, 17, 'archivum', ARCH,
     'alap: L2, DT84 (8) — a v2 változásleírás (G0086 javítás, 66 előfordulás, Hós 13:14, a Q2-állítás cseréje): folyamatmondat; minden tartalmi eleme máshol él (adat: elofordulasok/jeloltek; forrás: a 2/b Hós 13:14-bekezdés, Kivonat)'),
    (T, '(elválasztó)', 9, '', 19, 19, 'archivum', ARCH, 'alap: sablon 9 §4 (a tagolást a 4. pont szakaszrendje adja) — formázási elválasztó'),
    (T, '0. Forrás-összegyűjtés a meglévő anyagból', 10, '', 23, 23, 'archivum', ARCH,
     'alap: sablon 9 §4 7.N — a modszertan rés a B-ben a 7. szakaszban áll (csak a tartalmi nyitott tételek); a régi lapon négy helyen (0., 6., Önellenőrzés, Minőségi kapu) nyitott modszertan-rés jelölője megszűnik'),
    (T, '0. Forrás-összegyűjtés a meglévő anyagból', 11, '', 24, 28, 'archivum', ARCH,
     'alap: pilot-terv 4.3, DT84 (2) (auditok-sor a prózából nem keletkezik), sablon 9 §4 0 — az öt vizsgált forrás listája, jelölt nem került elő; a 0. szakasz helyén ADAT-NÉZET (örökölt motívum)'),
    (T, '0. Forrás-összegyűjtés a meglévő anyagból', 12, '1', 30, 30, 'archivum', ARCH,
     'alap: L4 — 1. részegység: „Elhatárolási forrás: l. a Tehom_tematikus.md »Lásd is« jegyzetét”: mutató egy másik motívum (TEREMT-001) régi forrására, amely a saját migrációjában archiválódik; az elhatárolás maga a 2. szakaszban (53. sor) és a motivumok.tsv negatív kritériumában áll'),
    (T, '0. Forrás-összegyűjtés a meglévő anyagból', 12, '2', 30, 30, 'archivum', ARCH,
     'alap: L2 — 2. részegység: a zárójeles 2026.09.10-i fájlösszevonási megjegyzés; folyamatmondat'),
    (T, '0. Forrás-összegyűjtés a meglévő anyagból', 13, '', 31, 31, 'archivum', ARCH, 'alap: a 10. blokk párja (RÉS-VÉGE: modszertan)'),
    (T, '(elválasztó)', 14, '', 33, 33, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '1. Előfordulások összegyűjtése', 15, '', 37, 38, 'generalt', STUDY, 'alap: sablon 9 §4 1.T — a tábla fejléce; a 7 oszlopos táblát a --cel study írja'),
    (T, '1. Előfordulások összegyűjtése', 16, '', 39, 41, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — Zsolt 16:10 → ApCsel 2:27, 31; Luk 16:23; Jel 1:18: az elofordulasok.tsv 5 sora (Zsolt 16:10, ApCsel 2:27, ApCsel 2:31, Luk 16:23, Jel 1:18). A régi cella („Zsolt 16:10 → ApCsel 2:27, 31”) a fo_elofordulas csoportban él; D-eltérés: a könyvnév rövidítve (Luk, Jel)'),
    (T, '1. Előfordulások összegyűjtése', 17, '1', 42, 42, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — 1. részegység: Jel 6:8 sora; a PaRDeS-cella értelmező kiegészítése („a Halál+Hádész páros első megjelenése …”) az elofordulasok.tsv megjegyzés-oszlopában szó szerint áll'),
    (T, '1. Előfordulások összegyűjtése', 17, '2', 42, 42, 'archivum', ARCH,
     'alap: Á8 (DT219), L2 — 2. részegység: „*(felvéve Konnyu_ellenorzes_4_lezart_tanulmany.md alapján, 2026.08.25)*” eredetmondat'),
    (T, '1. Előfordulások összegyűjtése', 18, '', 43, 43, 'generalt', STUDY, 'alap: sablon 9 §4 1.T — Jel 20:13-14 (az adatban egy tartomány-sor)'),
    (T, '1. Előfordulások összegyűjtése', 19, '1', 44, 44, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — 1. részegység: Luk 10:15 és Mt 11:23 (az adatban két sor, mindkettő megjegyzésében „második, önálló hádész-használati mintázat, ld. lent”)'),
    (T, '1. Előfordulások összegyűjtése', 19, '2', 44, 44, 'archivum', ARCH, 'alap: Á8 (DT219) — 2. részegység: „*(felvéve 2026.08.25)*”'),
    (T, '1. Előfordulások összegyűjtése', 20, '1', 46, 46, 'generalt', 'general.py --cel lexikon (minosites rés, 7.K ADAT-NÉZET) (forrás: adat/jeloltek.tsv ALVIL-001 Mt 16:18 dontes=elutasítva, indoklas)',
     'alap: sablon 9 §4 7.K — 1. részegység: a Mt 16:18 kizárása és oka (ekkleziológiai kontextus) a jeloltek.tsv meglévő elutasított sora'),
    (T, '1. Előfordulások összegyűjtése', 20, '2', 46, 46, 'forras', fs('7.N Nyitott kérdések', 'apparatus', 'RÉS: modszertan'),
     'alap: sablon 9 §4 7.N (tartalmi nyitott kérdés) — 2. részegység: „külön motívumként kezelendő, ha valaha sorra kerül” — a Mt 16:18 (a pokol kapui) lehetséges önálló motívuma; javaslat: egy tételként a Nyitott kérdések közé, saját mondattal (a mondat bájtra átvihető)'),
    (T, '(elválasztó)', 21, '', 48, 48, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '2. Eredeti nyelvi összevetés', 22, '', 52, 52, 'forras', fs('2.M Miért fontos ez a lelet', 'apparatus', 'jelölő: RÉS-KEZDET: miert_fontos'), 'alap: sablon 9 §6'),
    (T, '2. Eredeti nyelvi összevetés', 23, '', 53, 53, 'forras', fs('2 Eredeti nyelvi összevetés / 2.M Miért fontos', 'apparatus'),
     'alap: sablon 9 §4 2, 2.M — a két szó (kiejtéssel) és a tehóm/abüsszosz-elhatárolás értelmező kifejtése (L3 lexikai vs. tematikus); a negatív kritérium adat-alakja a motivumok.tsv-ben áll, a próza az indoklás'),
    (T, '2. Eredeti nyelvi összevetés', 24, '', 54, 54, 'forras', fs('2.M Miért fontos ez a lelet', 'apparatus', 'jelölő: RÉS-VÉGE: miert_fontos'), 'alap: sablon 9 §6'),
    (T, '(elválasztó)', 25, '', 56, 56, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 26, '', 60, 60, 'archivum', ARCH,
     'alap: sablon 9 §4 2/b (adat: lexikon_hivatkozasok.tsv, nincs kézi blokk) — a régi 2b rés itt előfordulás-táblát hordozott, nem szótári adatot; az ALVIL-001-nek nincs lexikon_hivatkozasok-sora (0), ezért a 2b rés a B-ben generált, explicit hiányjelöléssel; a res_forras.tsv 2b-sora forras=adat-ra vált (az ISTENTISZT-001 mintája)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 27, '', 61, 61, 'archivum', ARCH,
     'alap: L2 — a dőlt eredet- és folyamatmondat (TAHOT-scan alapján felvéve, sablon-konform táblázatra alakítva, 2 igehellyel kiegészítve, 2026.09.10)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 28, '', 63, 63, 'forras', fs('1 Előfordulások — kísérő próza', 'apparatus'),
     'alap: sablon 9 §4 1 (az ADAT-NÉZET mellett) — a H7585-mező mérete és a Hós 13:14 kettős előfordulása (64 vers / 66 szóelőfordulás). A „63 egyedi igehely” és a „64 egyedi vers” ADAT-ÉRTÉK-kel ellenőrizendő (64 = count(elofordulasok id=ALVIL-001; strong=H7585)); a „fenti egyetlen (Zsolt 16:10) genezisi-ívbeli előforduláson túl” keret a régi tanulmány-szerkezetre utal — a mondat bájtra kerül át, a keretet az értelmező menet a 9_ v0.3 próba tapasztalataként jelzi (DT-F123c)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 29, '', 65, 66, 'generalt', STUDY, 'alap: sablon 9 §4 1.T — a második tábla fejléce; a B-ben egyetlen 7 oszlopos tábla'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 30, '', 67, 73, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — 7 sor (1Móz 37:35 … 5Móz 32:22). D-eltérés: a régi cellák „שְׁאוֹל (seól) — ” és „ua. — ” előtagja az adatban nincs (az 1Móz 44:31 „ua.” helyett „Júda közbenjárása, folytatás”); az adat az irányadó'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 31, '1', 74, 74, 'generalt', STUDY, 'alap: 1Sám 2:6 sora — 1. részegység: igehely, kapcsolódás, szint'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 31, '2', 74, 74, 'archivum', ARCH,
     'alap: DT84 (10) (ii), egyenként ítélt 【NAPLO】 — 2. részegység: „e sor 2026.09.10-én pótolva — kimaradt az eredeti, prózai felsorolásból”: tisztán folyamat-nyom, belso; a forrásba nem kerül (a pótlás ténye a napló archív példányában megmarad)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 32, '', 75, 111, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — 37 sor (2Sám 22:6 … Ézs 5:14). D-eltérés: a Jób 17:13, 17:16 és a Préd 9:10 a régi (MT/TAHOT) számozás; az adat Károli-kulcsa Jób 17:12, 17:15, Préd 9:12 (F87.3, DT-F87b; Károli 1908 szövege igazolja) — a generált tábla a helyes kulcsot adja'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 33, '1', 112, 112, 'generalt', STUDY, 'alap: Ézs 7:11 sora — 1. részegység'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 33, '2', 112, 112, 'archivum', ARCH, 'alap: DT84 (10) (ii) — 2. részegység: a 31.2-vel azonos 【NAPLO】 (folyamat-nyom)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 34, '', 113, 125, 'generalt', STUDY,
     'alap: sablon 9 §4 1.T — 13 sor (Ézs 14:9 … Ez 32:27). D-eltérés: az Ézs 14:9 cellájában a `Rafaim_tematikus.md` fájlmutató helyett az adatban „(refáím) … l. HODIT-001” (motívum-ID, nem fájl: L4)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 35, '', 126, 126, 'generalt', STUDY,
     'alap: Hós 13:14 sora. D-eltérés: a „(l. 3. pont, ⭐ kiemelt lelet)” helyett az adatban „, ⭐ kiemelt lelet” (a belső szakaszmutató a B-ben nem érvényes)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 36, '', 127, 129, 'generalt', STUDY, 'alap: sablon 9 §4 1.T — Ámós 9:2, Hab 2:5, Jón 2:3'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 37, '1', 131, 131, 'archivum', ARCH,
     'alap: L2 — 1. részegység: a félkövér cím „⭐ Hós 13:14 — a legfontosabb ÚSZ-visszhang, eddig hiányzott a study-ból.”: az „eddig hiányzott” folyamatmondat; a „legfontosabb ÚSZ-visszhang” ítélet a Kivonatban (7. sor) és a 2. részegységben áll'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 37, '2', 131, 131, 'forras', fs('3.U Új felismerés', 'olvasoi', 'a 3. szakaszon belül, a RÉS: ertelmezes-ben'),
     'alap: sablon 9 §4 3.U — 2. részegység: a Hós 13:14 → 1Kor 15:55 lelet kifejtése („Megváltom őket … »Pokol«-lal (= hádész) adja vissza.”); értelmező lelet, a motívum fő ívét erősíti; a forrásban saját ### alcím alá (a mondatok bájtra)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 37, '3', 131, 131, 'generalt', 'general.py --cel lexikon (minosites rés, 7.K ADAT-NÉZET) (forrás: adat/jeloltek.tsv ALVIL-001 1Kor 15:55 dontes=elutasítva, indoklas)',
     'alap: DT84 (10) (ii), egyenként ítélt 【NAPLO】 — 3. részegység, első fele: a G0086-scan eredménye (NA28: θάνατος, nem ᾅδης; az 1Kor 15:55 nem G0086-előfordulás) a jeloltek.tsv meglévő elutasított sorának indoklása'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 37, '4', 131, 131, 'forras', fs('7 Módszertan (RÉS: modszertan)', 'apparatus'),
     'alap: sablon 9 §2 („az állítás megbízhatóságát érintő módszertani figyelmeztetés nem 【NAPLO】: apparatus-szöveg”), CLAUDE.md 3. szabály — 3. részegység, második fele: a TR/Byzantinus-olvasatról szóló állítás nem a repó adatából, hanem általános szövegkritikai ismeretből származik; ez a 3.U lelet megbízhatósági jelzése, a 7. szakaszba saját mondattal (a NAPLO-zárójel nélkül, a mondat bájtra)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 38, '', 133, 133, 'forras', fs('1 Előfordulások — kísérő értelmező próza', 'apparatus'),
     'alap: sablon 9 §4 1 (az ADAT-NÉZET mellett) — az ÓSZ-mező regiszter szerinti összegzése és viszonya a fő ívhez: értelmező próza. A „63 új igehely” ADAT-ÉRTÉK-kel ellenőrizendő (l. 28. blokk)'),
    (T, '2/b. Kiterjesztés — a seól teljes bibliai előfordulási mezője', 39, '', 134, 134, 'archivum', ARCH, 'alap: a 26. blokk párja (RÉS-VÉGE: 2b)'),
    (T, '(elválasztó)', 40, '', 136, 136, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 41, '', 140, 140, 'forras', fs('3 PaRDeS', 'olvasoi', 'jelölő: RÉS-KEZDET: ertelmezes'), 'alap: sablon 9 §6'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 42, '', 141, 141, 'forras', fs('3 PaRDeS', 'olvasoi'), 'alap: sablon 9 §4 3 — Peshat'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 43, '', 143, 143, 'forras', fs('3 PaRDeS', 'olvasoi'),
     'alap: sablon 9 §4 3 — Remez; a tehóm-párhuzam „csak tartalmi, nem lexikai” jelölése megvan (L3)'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 44, '', 145, 145, 'forras', fs('3 PaRDeS', 'olvasoi', 'Á8 (DT219): a dátum-rész („*(felvéve 2026.08.25)*”) archivum'),
     'alap: sablon 9 §4 3 — a második hádész-használati mintázat (hübrisz és megaláztatás, Luk 10:15 / Mt 11:23, Ézs 14:9-15); a címben álló dátumcímke Á8 szerint archívum, a többi bájtra'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 45, '', 147, 147, 'forras', fs('3 PaRDeS', 'olvasoi'), 'alap: sablon 9 §4 3 — Drash'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 46, '', 149, 149, 'forras', fs('3 PaRDeS', 'olvasoi'), 'alap: sablon 9 §4 3 — Sod (tömör)'),
    (T, '3. A PaRDeS keretrendszer — a motívum egészére alkalmazva', 47, '', 150, 150, 'forras', fs('3 PaRDeS', 'olvasoi', 'jelölő: RÉS-VÉGE: ertelmezes'), 'alap: sablon 9 §6'),
    (T, '(elválasztó)', 48, '', 152, 152, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '4. Kapcsolódás a kutatási sablonhoz', 49, '1', 156, 156, 'forras', fs('4 Kapcsolódás a kutatási sablonhoz', 'apparatus', 'jelölő: INAKTÍV: 4 — ok kötelező (DT84 (6))'),
     'alap: sablon 9 §3 (értelmezői aktiválás: az inaktív állapot a „nincs adat” tényt rögzíti) — 1. részegység: a hiány ténye („dedikált … szakirodalmi feldolgozás nem áll rendelkezésre elegendő mennyiségben”) az INAKTÍV sor indoka lesz'),
    (T, '4. Kapcsolódás a kutatási sablonhoz', 49, '2', 156, 156, 'archivum', ARCH,
     'alap: L6 (hangnem: harmadik személy) — 2. részegység: „Ezt a pontot ezért nem erőltetem — gyengébb anyaggal nem pótolom.” első személyű folyamatmondat; a CLAUDE.md 3. szabályát az INAKTÍV sor maga érvényesíti'),
    (T, '(elválasztó)', 50, '', 158, 158, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '5. Alkalmazás és tanítványság', 51, '', 162, 162, 'forras', fs('5 Alkalmazás és tanítványság', 'olvasoi', 'jelölő: RÉS-KEZDET/VÉGE: alkalmazas (új, DT276)'),
     'alap: sablon 9 §4 5, DT276 — a tanulmány saját megállapításaiból levont alkalmazás; a res_forras.tsv alkalmazas-sora adat → tanulmany (motivumok/ALVIL-001.md)'),
    (T, '5. Alkalmazás és tanítványság', 52, '1', 164, 164, 'forras', fs('5.T Nevesített tanítói egyezés', 'olvasoi', 'jelölő: INAKTÍV: 5.T — a 7. lépés nem futott'),
     'alap: sablon 9 §4 5.T, X.M7 — 1. részegység: a tanítói hiány ténye; az ALVIL-001-nek nincs 7. lépés-fájlja (motivumok/naplok/ALVIL-001_tanitoi_kereses.md nem létezik), beemelt tanítói sor nincs; a tanitoi rés explicit hiányjelöléssel (res_forras tanitoi: adat). A DT249 (b) itt nem alkalmazandó (nincs szétválasztandó tanítói anyag)'),
    (T, '5. Alkalmazás és tanítványság', 52, '2', 164, 164, 'archivum', ARCH,
     'alap: L6 — 2. részegység: „ezt itt explicit jelzem, nem pótolom …” első személyű folyamatmondat'),
    (T, '(elválasztó)', 53, '', 166, 166, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, '6. Napló-frissítés', 54, '', 170, 170, 'archivum', ARCH, 'alap: a 10. blokkal azonos (a modszertan-rés régi jelölője)'),
    (T, '6. Napló-frissítés', 55, '1', 171, 171, 'generalt', 'general.py --cel naplo (6. Napló-frissítés, ADAT-NÉZET) (forrás: adat/motivumok.tsv statusz)',
     'alap: sablon 9 §4 6 — 1. részegység: a „lezárva” státusz (a motivumok.tsv statusz=publikálható)'),
    (T, '6. Napló-frissítés', 55, '2', 171, 171, 'archivum', ARCH,
     'alap: L2 — 2. részegység: a 2026.09.10-i fájlszervezési kiszervezés és a 4→6 előfordulás-korrekció leírása (folyamat-nyom)'),
    (T, '6. Napló-frissítés', 56, '', 173, 173, 'archivum', ARCH,
     'alap: sablon 9 §4 7.K — mutató a kereszthivatkozás-naplóra, amely maga archiválódik; a teljes jelöltlista a jeloltek.tsv-ből generált (7.K ADAT-NÉZET)'),
    (T, '6. Napló-frissítés', 57, '', 174, 174, 'archivum', ARCH, 'alap: az 54. blokk párja'),
    (T, '(elválasztó)', 58, '', 176, 176, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (T, 'Önellenőrzés', 59, '', 180, 188, 'archivum', ARCH,
     'alap: DT84 (8), sablon 9 §4 7.Q (a régi kézi kapu-eredmény archívum) — az önellenőrző checklist a RÉS-jelölőkkel; a forrás kapuja a sablon 9 §8 (L1–L7, DT2), a független ellenőrzés az M6'),
    (T, 'Minőségi kapu (Quality Gate)', 60, '1', 192, 199, 'archivum', ARCH,
     'alap: DT84 (8) — a Q1–Q6 kézi kapu-eredmény a RÉS-jelölőkkel és a Q2 sorában álló 【NAPLO】-val (a 2026.09.09-i hibás állítás és az első javítás története: folyamat-nyom)'),
    (T, 'Minőségi kapu (Quality Gate)', 60, '2', 194, 194, 'adat', 'adat/auditok.tsv · ALVIL-001 · B4 scan H7585 és G0086 — NEM a prózából (DT84 (2)): a lekérdezést futtató fő szál írja, az F123 X.A újrafuttatott scanjeiből (naplok/F123_lekerdezesek.tsv)',
     'JÓVÁHAGYANDÓ (M3 előtt): az ALVIL-001-nek nincs auditok.tsv-sora (0), ezért a 7.M ADAT-NÉZET üres lenne, és a lapról eltűnne, hogy a 2026.09.10-i teljes scan megtörtént. Javaslat: a Q2 tartalma (H7585 teljes ÓSZ-scan: 64 vers; G0086 teljes ÚSZ-scan: 10) nem a prózából kerül az adatba, hanem az F123 X.A 2026-10-28/29-i, ténylegesen lefutott scanjeinek audit-sorából (fő szál, valódi proveniencia); alternatíva: a 7.M üres, explicit hiányjelöléssel'),
    # ---------------- Hadesz_Seol_kereszthivatkozas_naplo.md ----------------
    (N, '(fejléc)', 1, '', 1, 1, 'archivum', ARCH, 'alap: a napló címe; a B-ben a napló nem önálló kézi forrás (7.K generált)'),
    (N, '(fejléc)', 2, '', 3, 3, 'archivum', ARCH, 'alap: L2 — retroaktív pótlás (F0.5, 2026.09.13) leírása'),
    (N, '(elválasztó)', 3, '', 5, 5, 'archivum', ARCH, 'alap: formázási elválasztó'),
    (N, 'Vizsgált kulcsszavak', 4, '', 9, 9, 'archivum', ARCH,
     'alap: a két Strong (H7585, G0086) az elofordulasok.tsv strong mezőjében áll; a G86→G0086 javítás folyamat-nyom'),
    (N, 'Nyers találatok forrásonként', 5, '', 13, 22, 'archivum', ARCH,
     'alap: pilot-terv 4.3, DT84 (2) — a TAGNT/TAHOT nyers scan-eredmény (számok, javítások, a két kimaradt igehely története); a számok az adatból generáltak, a szövegkritikai megjegyzés a 37.3/37.4 egységben (a tanulmányban) kerül át, itt nem ismétlődik'),
    (N, 'Tartalmi minősítés minden jelöltre', 6, '', 26, 26, 'generalt', 'general.py --cel lexikon (minosites rés, 7.K ADAT-NÉZET) (forrás: adat/jeloltek.tsv)',
     'alap: sablon 9 §4 7.K — a RÉS-KEZDET: minosites; a res_forras.tsv minosites-sora tanulmany → adat (az ISTENTISZT-001 mintája)'),
    (N, 'Tartalmi minősítés minden jelöltre', 7, '', 27, 32, 'generalt', 'general.py --cel lexikon (minosites rés) (forrás: adat/jeloltek.tsv dontes=beépítve, indoklas)',
     'alap: sablon 9 §4 7.K — Hós 13:14 (⭐), a 62 H7585-igehely, 1Sám 2:6, Ézs 7:11: mind beépített jelöltsor (72 beépítve). D-eltérés: a „62 + 1Sám 2:6 + Ézs 7:11” csoportosítás helyett soronkénti nézet'),
    (N, 'Tartalmi minősítés minden jelöltre', 8, '', 33, 34, 'generalt', 'general.py --cel lexikon (minosites rés) (forrás: adat/jeloltek.tsv 1Kor 15:55, Mt 16:18 dontes=elutasítva)',
     'alap: sablon 9 §4 7.K — a két elutasított jelölt, indoklással (a jeloltek.tsv meglévő sorai)'),
    (N, 'Tartalmi minősítés minden jelöltre', 9, '', 35, 35, 'archivum', ARCH,
     'alap: L4 — a tehóm/abüsszosz-elhatárolás nem igehely-kulcsú (jelöltsor nem írható, sablon 9 §6); a tartalma a 2. szakaszban (tanulmány 53. sor) és a motivumok.tsv negatív kritériumában áll — itt duplikátum'),
    (N, 'Tartalmi minősítés minden jelöltre', 10, '', 36, 36, 'archivum', ARCH, 'alap: a tanítói hiány az 5.T INAKTÍV sorában áll (tanulmány 52.1)'),
    (N, 'Tartalmi minősítés minden jelöltre', 11, '', 37, 37, 'generalt', 'general.py --cel lexikon (minosites rés)', 'alap: a 6. blokk párja (RÉS-VÉGE: minosites)'),
    (N, 'Végső döntés és indoklás', 12, '', 41, 43, 'archivum', ARCH,
     'alap: DT84 (8) — a döntések prózai összefoglalója a minosites-rés második blokkjában; minden eleme a jeloltek.tsv-ből generált (7.K) vagy a tanulmány átvitt egységeiben áll; a második minosites-rés megszűnik'),
    (N, 'Összegzés', 13, '', 47, 47, 'archivum', ARCH, 'alap: számösszegzés (66/64/10, 1 javítás, 2 elhatárolás, 1 kizárás, 1 gap); az adatból generált'),
    (N, 'Összegzés', 14, '', 49, 49, 'archivum', ARCH, 'alap: DT84 (10) (ii) — 【NAPLO】: a napló rekonstrukció voltáról (F0.5); folyamat-nyom'),
]

# Kiegészítés (F123 M3, 2026-10-29): a régi forrásréteg (`motivumok/ALVIL-001.md`, F4.4/G2 kivonat a motívumnaplóból) a
# jóváhagyott táblából kimaradt; a #11 is leképezte (sablon 9 §4 „Örökölt motívum blokkjai”). Forrás-egység nincs benne.
R = 'motivumok/ALVIL-001.md (régi forrásréteg)'
R_UT = 'motivumok/ALVIL-001.md'
RARCH = 'a régi forrásréteg változatlan, archív fejlécű példánya (archivum/ALVIL-001/ALVIL-001_forrasreteg_regi.md, DT215)'
S += [
    (R, '(fejléc)', 1, '', 1, 1, 'archivum', RARCH, 'kiegészítés: a régi cím; az új forrás címe a motivumok.tsv cim mezőjével azonos'),
    (R, '(fejléc)', 2, '', 3, 3, 'archivum', RARCH, 'kiegészítés: a régi FORRÁSRÉTEG-jelölő; az új forrás saját jelölőt kap'),
    (R, '(fejléc)', 3, '', 5, 5, 'archivum', RARCH, 'kiegészítés: L2 — a 2026-09-15-i átemelés proveniencia-mondata (folyamat-nyom)'),
    (R, 'Tematikus áttekintés', 4, '', 9, 9, 'archivum', RARCH,
     'kiegészítés: sablon 9 §4 (örökölt blokk: generált, a #11-ben archívum) — a napló régi tétele („4 előfordulás”), elavult szám'),
    (R, '⭐ Emlékeztető küszöb', 5, '1', 13, 13, 'generalt', 'general.py --cel naplo (⭐-bekezdés) (forrás: adat/motivumok.tsv, adat/elofordulasok.tsv)',
     'kiegészítés: sablon 9 §4 — 1. részegység: a cím, a státusz, a szám és az igehely-lista generált'),
    (R, '⭐ Emlékeztető küszöb', 5, '2', 13, 13, 'archivum', RARCH,
     'kiegészítés: 2. részegység: az értelmező mondat („lexikailag élesen elkülönített: a seól/hádész az egyéni halottak '
     'birodalma (nem a kozmikus ős-mélység)”) a 2. szakaszban (tanulmány 53. sor) bővebben áll — duplikátum; a fájltörténet L2'),
    (R, 'Kulcsszó-index', 6, '', 17, 17, 'archivum', RARCH, 'kiegészítés: sablon 9 §4 (örökölt blokk: generált, archívum)'),
    (R, 'Lezárt tanulmányok indexe', 7, '', 21, 23, 'archivum', RARCH,
     'kiegészítés: sablon 9 §4 — az index Fájlnév-cellája a motivumok.tsv forras_study mezőjéből generált; a fájltörténeti megjegyzés L2'),
]

# új (nem a régi fájlból jövő) forrás-egységek: nem leképezés, hanem a terv; a táblában tájékoztató sorként
UJ = [
    (F, '(új)', 1, '', 0, 0, 'forras', fs('F Forrásréteg-fejléc', 'belso', 'jelölő: FORRÁSRÉTEG'), 'új szerkezeti egység (sablon 9 §4 F)'),
    (F, '(új)', 2, '', 0, 0, 'forras', fs('0 / 1.T / 2.S / 2/b / 6 / 7.K / 7.A / 7.M / 7.Q', 'a saját SZINT-jével', 'jelölő: ADAT-NÉZET'),
     'új szerkezeti egységek (sablon 9 §4, az ISTENTISZT-001 mintája); a 1.L INAKTÍV (van tartomány-sor: Jel 20:13-14 — a bontás szükségességét az értelmező menet ítéli meg)'),
    (F, '(új)', 3, '', 0, 0, 'forras', fs('3 PaRDeS — ↳ alpont', 'olvasoi'),
     'DT-F123d (2), 2e. 5.: a „kiáltás a Seól szorításából” ↳ alpont (magversek: 2Sám 22:6, Zsolt 18:6, Jón 2:3, Zsolt 116:3; minimális jegy: a Seól a hívót szorongatja, és ő az Úrhoz kiált; kizárva: Zsolt 55:16, 31:18; hígulás: „ima bajban”, mért példája a Zsolt 107:18–19, DT-F123e) — új értelmező próza az M3-ban, az értelmező menet írja'),
    (F, '(új)', 4, '', 0, 0, 'forras', fs('P Proveniencia-sorok', 'belso'),
     'a Kivonat és az 1. szakasz számainak proveniencia-lábjegyzetei (a „tíz ᾍδης-előfordulás”, a 64 vers) — a lekérdezések sorai szó szerint'),
    ('motivumok/naplok/ALVIL-001_proza_lefedettseg.md', '(új)', 5, '', 0, 0, 'forras', 'motivumok/naplok/ · a motívum naplója (2d. 2.)',
     'a próza-lefedettség mérése (naplok/F123_adat_ALVIL-001_proza_lefedettseg.tsv: 2 tárgyalt, 13 érintett, 57 meg nem nevezett előfordulás) átvitele a motívum naplójába, proveniencia-sorral'),
]


def main():
    # a régi fájlok az M3 után az archívumban állnak, ARCHÍV fejléccel (a sorszámok a régi fájléi)
    utak = {T: [T, 'archivum/ALVIL-001/Hadesz_Seol_tematikus.md'],
            N: [N, 'archivum/ALVIL-001/Hadesz_Seol_kereszthivatkozas_naplo.md'],
            R: ['archivum/ALVIL-001/ALVIL-001_forrasreteg_regi.md', R_UT]}
    sorok = {}
    for f, jeloltek in utak.items():
        for u in jeloltek:
            if os.path.exists(ROOT + u):
                x = open(ROOT + u, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
                if x[0].startswith('<!-- ARCHÍV:'):
                    x = x[1:]
                elif f == R and not x[0].endswith('forrásréteg `[ID: ALVIL-001]`'):
                    continue  # az új forrás, nem a régi forrásréteg
                sorok[f] = x
                break
    fedett = {T: set(), N: set(), R: set()}
    hiba = []
    for f, sz, b, r, tol, ig, kat, cel, ind in S:
        if not (1 <= tol <= ig <= len(sorok[f])):
            hiba.append('tartomány: %s %d-%d' % (f, tol, ig))
        for n in range(tol, ig + 1):
            fedett[f].add(n)
    for f in (T, N, R):
        for n, l in enumerate(sorok[f], 1):
            if l.strip() and not l.startswith('#') and n not in fedett[f]:
                hiba.append('nem besorolt sor: %s:%d %s' % (f, n, l[:80]))
    if hiba:
        print('\n'.join(hiba))
        sys.exit(1)
    fej = ['fajl', 'szakasz', 'blokk', 'resz', 'sor_tol', 'sor_ig', 'kategoria', 'cel', 'indoklas', 'forras_parancs']
    ki = ['# F123 X.M1 — az ALVIL-001 leképezési táblája | sablon: %s | forrás: %s, %s | a „(új)” sorok nem leképezések, hanem a forrás új szerkezeti és értelmező egységei (tájékoztató) | készítő: naplok/F123_szetvalasztas_ALVIL-001_keszito.py' % (SABLON, T, N),
          '\t'.join(fej)]
    for f, sz, b, r, tol, ig, kat, cel, ind in S + UJ:
        parancs = "sed -n '%d,%dp' %s" % (tol, ig, f) if tol else '—'
        mezok = [f, sz, str(b), r, str(tol) if tol else '—', str(ig) if ig else '—', kat, cel, ind, parancs]
        assert all('\t' not in m and '\n' not in m for m in mezok)
        ki.append('\t'.join(mezok))
    open(ROOT + 'naplok/F123_szetvalasztas_ALVIL-001.tsv', 'w', encoding='utf-8', newline='').write('\n'.join(ki) + '\n')
    from collections import Counter
    c = Counter((x[0].rsplit('/', 1)[-1], x[6]) for x in S)
    for k in sorted(c):
        print('%s\t%s\t%d' % (k[0], k[1], c[k]))
    print('SOROK\t%d leképezés + %d új' % (len(S), len(UJ)))


if __name__ == '__main__':
    main()
