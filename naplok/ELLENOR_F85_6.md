ELTÉRÉS: 4 tétel

# ELLENOR_F85_6 — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main..claude/tahot-verskulcs` (fókusz: F85.6 = a4a09ba9..8ce6e95c)

*A `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott); az orkesztrátor mentette le, rövidítve, de érdemben változatlanul. Csak olvas; a 4–7. tétel még nem esedékes. Eljárási jelzés az ellenőrtől: két parancsot kiegészítő csővel futtatott (`| head -0`, `| cut`), csak olvasott, az eredményeket nem alapozza meg.*

| pont | eredmény | indok |
|---|---|---|
| (1a) sorszám | OK | `git diff --numstat`: 5885/5885 (Δ=0); a HEAD-fájl 469 301 sor fejléccel |
| (1b) csak a 9 könyv sorai változnak | OK | 5885 `-` és 5885 `+` sor, mind a 9 könyvben, 7 mezős, nincs `\r` |
| (1c) az Igehelyen kívüli mezők azonosak | NEM ELLENŐRIZHETŐ teljes körűen | a git diff a 445 véletlenül egyező sort összepárosítja (5885 ≠ 6330), szkript nem volt megengedett; részellenőrzések egyeznek (H9002 343/343, H3068 35/35, H0430 14/14, Préd 1337/1337, Dán 971/971), szúrópróbák (Jób 40:6→40:1, 4Móz 30:1/30:2) azonos tartalmat mutatnak |
| (1d) a diff = a napló 6330 sora | OK (összeg, szúrópróba) | könyvenként 781/405/641/270/1420/212/603/1055/943 = 6330; sorszám → HEAD-kulcs szúrópróbák egyeznek; soronkénti teljes egyeztetés nem ellenőrizhető |
| (2) 337 vers könyvenként | OK | 328 eltolás + 9 összevonás-sor = 38/17/59/28/66/13/31/37/48 |
| (2) új kulcs = létező Károli-vers | OK (célzottan) | a 27 régi árva kulcs 0 sor; a 18 korábban üres Károli-vers mind kapott sort; mind a ~337 új kulcs egyenkénti ellenőrzése nem ellenőrizhető |
| (3) a 17 összevonás | OK | 9 kulcsváltó + 8 nem váltó összevonás-partner = 17 sor (8 teljes pár + az Ézs 64:2, amelynek partnere az Ézs 64:1, bizonytalan sor); a 12 nem váltó sor = 8 partner + 4 bizonytalan |
| (4) adat-réteg, TAHOT-ból származó igehely a 337 vers között | ELTÉRÉS (csak lista) | `adat/elofordulasok.tsv:97, 98, 125`, `adat/jeloltek.tsv:113, 114, 141` (mind ALVIL-001): régi kulcson áll a **Jób 17:13** (→ 17:12), **Jób 17:16** (→ 17:15; Károli 17:16 nincs), **Préd 9:10** (→ 9:12). A Jób 17:13 sor eleve kevert volt (az idézet az MT 17:13 = K 17:12, a `karoli_szo` a K 17:13). A Hós 13:14 nincs a naplóban, rendben. Javítás nem kért. |
| (5) „17 747 vers, 0 eltérés” | szám NEM ELLENŐRIZHETŐ / hatókör OK | a `VERSBEOSZTAS_JOVAHAGYOTT` tartalmazza a 2Móz-t; az összevetést végző kód nincs a commitban |
| (5) KeyError '2Móz 36:38' → parok_* | OK | a `f22/versmegfeleltetes.tsv` detektor-tábla hivatkozik a már nem létező kulcsra; a `parok_2Moz`/`szavak_2Moz` bájtra változatlan, de az ágon a 4. tételig nem generálható újra |
| (5b) `f22/versosszevonas.tsv` | **ELTÉRÉS** | 5–11. sor: 7 `eredeti`-kulcs (4Móz 30:1, Ézs 9:20, Ézs 64:2, Péld 12:1, Jób 17:1, Jób 37:1, Hós 12:1) a HEAD-en létezik, de más tartalommal (pl. 4Móz 30:1 = a régi 30:2; Hós 12:1 = a régi 12:2). A beolvasztás nem KeyError-ral áll le, hanem csendben rossz vagy kettőzött szavakat adna. A jelentés „Ismert következmény” pontja csak a KeyError-t nevezi meg. |
| (6) fizikai szomszédosság | OK | 7 pár szomszédos (Jób 16:22+17:1, Jób 36:33+37:1, Péld 11:31+12:1, Préd 2:25+2:26, Ézs 9:19+9:20, Ézs 64:1+64:2, Hós 1:11+2:1); nem szomszédos: 4Móz 29:39 (93429–58) + 30:1 (440043–55) és Hós 11:11 (420239–57) + 12:1 (467186–205), de az első vers mindkettőnél előbb áll |
| (6) az áthelyezett blokk régi | OK (szúrópróba) / a 23-as szám NEM ELLENŐRIZHETŐ | a 4Móz 30 a régi fájlban is a Mal 3:18 utáni blokkban volt; mozgatás nincs |
| (7) változatlanság | OK | `adat/`, `f22/` diff az F85.6 commitban üres; 19 parok_* + 19 szavak_* fájl |
| T3 „a sorrend Károli-sorrend” | ELTÉRÉS (alacsony) | brief-ellentmondás: a fájlsorrend nem Károli-sorrend (23 törés); a végrehajtó a „csak az első oszlop változik” mondatot követte; a felhasználó elfogadta a fizikai szomszédosság hiányát a két kivételnél |
| T3 a szkript ellenőrzései | OK (kódolvasás) | `split`/`join`, csv nincs, idempotencia-őr, VART=337; a 131–137. sor zip-összevetése önigazoló, független bizonyítékot nem ad |
| ⛔ 1, E1–E5 javítása, A2–A6, Ell.1–5 | OK | a DT92 🟡 → 🟢 rögzíti a felhasználó chat-döntését; N-F85a nyitott; E12–E15: 0 találat; adattábla-Δ: csak a TAHOT 5885/5885, Δ=0 |
| A1 memória vs. lekérdezés | ELTÉRÉS (alacsony) | a „szkriptes bájt-összevetés” és a „17 747 vers” ellenőrző kódja nincs a repóban; a jelentés proveniencia-sora erre a két állításra nem pontos |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(5b)** a `f22/versosszevonas.tsv` 7 sorának `eredeti` kulcsa az átkulcsolás után eltolt tartalomra mutat (csendes hiba). A 4. tételben kezelendő; addig a beolvasztást használó kód (`tokenek.py:155–158`) az ágon ne fusson.
2. **(4)** az adat-rétegben régi kulcs áll: Jób 17:13, Jób 17:16, Préd 9:10 (`elofordulasok.tsv` / `jeloltek.tsv`). A Jób 17:16 már nem létező Károli-vers. A F85 jelentése nem jelezte.
3. **A1** a „17 747 vers, 0 eltérés” és a „szkriptes bájt-összevetés” kódja nincs a commitban.
4. **T3** a „sorrend Károli-sorrend” szó szerint nem teljesül, dokumentált, a felhasználó dönt.

Megfigyelés (nem eltérés): a `parok_Peld` már létezik, így a DT92 (5) „a Péld-menet előtt” javaslata tárgytalan.
