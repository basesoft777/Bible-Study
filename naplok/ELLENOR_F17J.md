# ELLENOR_F17J — F17.J (DT7 javító menet)

*Az ügynök jelentése, a session mentette (az ügynöknek nincs írási eszköze). Független ellenőr (fuggetlen-ellenor), tartomány: `origin/main..HEAD` (F17.J1–J3); a szöveget a fő szál változtatás nélkül másolta ide, az összefoglalóval és a válaszokkal kiegészítve.*

**Eredmény: TISZTA a tartalmi pontokon; 3 eltérést jelzett, ebből 1 javítva, 2 magyarázva.**

## Igazolt pontok (saját lekérdezéssel)
- A Dán 3–4 sorain kívül minden sor bájtra azonos az `allapot` oszlop nélkül (39 héber fájl, Siralmak is: 0 eltérés); a görögben 4 sor `allapot`-a változott (`javaslat:strong_nincs_strong` → `rendben`), a `strong_illesztes` változatlan.
- Dán 3–4: 1 964/1 964 sor `identitas` / `rendben`, Károli Dán 3:1–33 és 4:1–34 teljes; 3 szöveg-szintű szúrópróba egyezik (Dán 4:1, 3:31, 4:34); a többi 64 vers szövege nem volt összevetve.
- Az `allapot` oszlopban nincs `strong_` tag (héber, görög).
- Illesztetlen MT-vers 242 → 182; `karoli_vers_nincs_macula|heber` 233 → 173; régi KK-javaslat 6 705 (régi fájlból), új 4 996, különbség 1 709 = a régi Dán 3–4 KK-javaslat sorok (régi fájlból); héber sorok 475 911.
- Sir/JSir alias kétirányú, a Siralmak 2 303/2 303 sora `Sir`-címkét őriz, `kk_mod=nincs` sor 0; az `F17_87_hely.tsv` és az `F17_illesztetlen.tsv` mellékhatás nélkül.
- Sorvégek, fejlécek (`GENERÁLT`, ts), proveniencia, `csv` modul (nincs), commit-üzenetek: rendben; CI-szabályok E2–E16, E19: 0 találat.

## Eltérések és válaszok
1. **DT7 🟡 az ágon.** Az ág a DT7 lezárását rögzítő PR (#118) merge-e előtti `main`-ről indult; a döntés rögzítése a #118-ban van (✅). Nem hiba, a merge sorrendje: #118, majd ez.
2. **Dán 3 az identitás-körben.** A felhasználó chat-döntése (DT7 c, 2026.10.02) kifejezetten kimondja: „Dán 3 szintén identitás (Károli 3:31–33 = MT 3:31–33, a fejezet MT-számozású)”; a hatókör a döntésből következik, nem az ellenőr által látott korábbi javaslat-szövegből.
3. **`N-F17a`, `N-F17b`, `N-F35a` hiányzott a `NYITOTT_FELADATOK.md`-ből.** Javítva: a három tétel felvéve (a számot a F30 helyőrző-szabálya szerint a main-Action osztja ki).

## Nem ellenőrizhető
A generátor újrafuttatása az ellenőrnek nem megengedett parancs (a fő szál futtatta, az eredményt a fenti bájt-összevetés igazolja); a CI-jelentéssel való egyezés (CI még nem futott); a 64 további Dán-vers szöveg-szintű összevetése. Kockázati megjegyzés: a `RAW_NEV` lustán töltődik, a `karoli_cimke` csak `kanoni_nev` hívás után ad helyes címkét (a mostani futási sorrendben teljesül; az alias a #35 után törlendő).
