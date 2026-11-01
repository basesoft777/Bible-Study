ELTÉRÉS: 8 tétel

# ELLENOR_ISTENTISZT001_SZEREP12_14

*A `fuggetlen-ellenor` jelentése, a végrehajtó mentette (az ellenőrnek nincs fájlíró eszköze). Az eltérés- és a lényegi OK-sorok a jelentés szerint, rövidítve; a végén a végrehajtó javítóköre.*

- **Megbízás:** a DT424 (a `DONTESEK.md` 12–14. szerep-sora); brieffájl nincs.
- **Tartomány:** `f9ec7400..b3b84efb`.
- **Ellenőr:** a tényleges modell `claude-opus-5-5`, a kért modell `opus`, tehát egyezik.

| pont | eredmény | indok |
|---|---|---|
| 14. rejtett párhuzam (4 hely) | OK | Mind a négy motívumsor, és egyikben sincs „hív…segítségül”. A kollokáció és a scan igazolja. |
| 14. hamis párhuzam: címke | **ELTÉRÉS (1)** | A 17 versből 16-ban ott a H7121 (`lekerdez.py scan H7121`), csak a H8034 hiányzik. Ez részleges gerinc, nem „más Strong”. |
| 14. hamis párhuzam: teljesség | **ELTÉRÉS (5, alacsony)** | A Jób 27:10 („hívhatja”) kimarad az `ELOTAG_MARADEK=3` miatt. |
| 13. Károli-megfelelők, +SZPA | OK | 33/33 vers; a hiány explicit. |
| 12. a Nave Károli-kulcsa | **ELTÉRÉS (2)** | Üres `igehely_karoli` esetén a kód a KJV-kulcsot vette Károlinak. Ezért kimaradt az Ézs 64:6 (KJV 64:7), és a KJV 64:6 hamisan találta el a motívumverset; a „113 téma” így torz. |
| 12. „témavers” nevező | **ELTÉRÉS (3)** | Az egész fejezet 1 egységként számított (OBLIGATION: 5Móz 6–11). |
| 12. a 22 döntéssor ↔ Nave-név; a GLORY altétele | OK | Mind egyezik. |
| a lapdiff; helyőrző a lapon, a kódban és a címsorban | OK | Csak a megengedett részek változtak; helyőrző sehol nincs. |
| Seól → Seol a táblában | OK | Csak a két sor. |
| Seol a partnerlapon | **ELTÉRÉS (4)** | Az ALVIL-001 generált lapján a két sor még „Seólban”. |
| tizedesjel | **ELTÉRÉS (6, alacsony)** | „2.6%” a „2,6%” helyett. |
| a forráslista sorrendje | **ELTÉRÉS (7, alacsony)** | TAHOT / Nave / TAGNT. |
| a commitok tárgysora | **ELTÉRÉS (8, alacsony)** | Nem tétel-azonosítóval kezdődik. |
| SEMA 2.41–2.42, a DONTESEK idézetei, oszlopszám | OK | – |

## Javítókör (végrehajtó, 2026-10-29)

1. **(1) A 14. címkéje** mostantól „Hamis párhuzam (ugyanaz a magyar szó, a gerinc-kombináció nélkül)”. Versenként kiíródik a versben álló gerinc-Strong: 16 versben „H7121”, 1 versben „nincs”. A DT424 ugyanígy javítva. A logika nem változott: a magyar kulcsszó mindkét szövetségben ugyanazt a formulát keresi, ezt a lap ki is mondja.
2. **(2), (3) Áttérés a közös szabályra.** A `szerep_nave.nave_sorai` mostantól az `eszkozok/nave_bontas.py` szabályával bont, ugyanazzal a bemenettel, mint az olvasó `nave_vers`-e: a LXX_OS KJV-kulcsa, a fejezeteltolás, végül a `Karoli_versmegfeleltetes.tsv`.
   - A fejezetszintű hely nem bomlik, a kihagyás számolt.
   - **Eredmény:** 107 téma (113 helyett). A PRAYERLESSNESS 3/15 (20%), az Ézs 64:6-tal; az OBLIGATION 2/19.
   - A jelöltek száma változatlanul 18, a 8 kiválasztott téma ugyanaz.
   - A `naplok/NAVE_tema_meres.py` ugyanezt a szabályt használja.
   - **Teszt:** `test_kjv_karoli_megfeleltetes`.
3. **(6)** A 12. blokk tizedesvesszőt ír.
4. **(5) A „hívhatja”:** ismert korlát; a modul docstringje és a DT424 is kimondja. Az `ELOTAG_MARADEK` 4 betűre emelése a KIRALY-001-en 19-ről 61-re növelné a zajt, ezért marad 3.
5. **(4) Az ALVIL-001 lap** a main-en eleve elavult: az újragenerálása 775 sort változtatna. A két „Seol”-sor a lap következő generálásakor kerül rá. Ebben a PR-ben nem generálódik újra, mert az ALVIL-001 nem ennek a menetnek a lapja.
6. **(7) A forráslista sorrendjét** a generátor közös függvénye adja, a menet nem nyúlt hozzá. **(8)** A commitok tárgysora a #506 és a #508 elfogadott mintáját követi. Mindkettő változatlan.
