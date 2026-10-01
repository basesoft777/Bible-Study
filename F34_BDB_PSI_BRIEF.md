---
feladat: 34
cim: BDB „ψ” (Zsoltárok) feloldási hiba javítása a forrásban és az érintett fordítások igehelyei
kod: BDB_PSI
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
ag: claude/bdb-psi
ad: a BDB_teljes_unabridged.tsv-ben a „ψ” (Zsoltárok) jel hibás feloldása javítva (Ez 73:23, Ézs 106:9, Ézs 71:20, Jób 97, Péld 57–75 …, rejtett esetek: Ez 16:10 = Zsolt 16:10); az érintett adat/forditasok.tsv-sorok igehelyei gépileg cserélve; a 13. kapu jelzése megszűnik
kovetkezo: független ellenőrzés (fuggetlen-ellenor), majd merge a felhasználótól
olvas: [konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, adat/lexikon_hivatkozasok.tsv, naplok/EMELES_naplo.md, eszkozok/forditas_kapuk.py, konkordancia/README.md, adat/datasetek.tsv]
ir: [konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, adat/forditasok.tsv, eszkozok/bdb_psi_javit.py, eszkozok/teszt_bdb_psi_javit.py, eszkozok/teszt_forditas_kapuk.py, naplok/, NYITOTT_FELADATOK.md, DONTESEK.md]
lezarva_osszegzes: 159 ψ-hely javítva a BDB-forrásban (TAHOT + MT-versszámozási tábla, 56 szócikk), forditasok.tsv 78/81/89 token; maradék 163 hely N-F34-be; 13. kapu a javított helyekre 0 (a 81/84 sor hash-e elavult: SÉRTÉS, N-F34); részletek naplok/F34_zaras.md
pr:
fugg: [28]
---

# BDB „ψ”-hiba (BDB_PSI)

## Háttér
Az F28 13. kapuja jelzi (nem bukás) a könyv fejezetszámánál nagyobb fejezetet; öt szócikkben a BDB „ψ” (Zsoltárok) jelének hibás feloldását találta (H6093, H7121, H1121, H8415, H7585 érintett; példák: Ez 73:23, Ézs 106:9, Ézs 71:20, Jób 97, Péld 57–75). Rejtett eset: Ez 16:10 = Zsolt 16:10 (a fejezetszám a könyvben létezik, ezért a kapu nem jelzi). A „Dán 22:14” a forrás saját hibája („Dan 22:14”), nem a ψ-feloldásé: külön kezelendő, nem ennek a feladatnak a hatóköre.

## Lépések
1. **M0 — felmérés (csak olvas):** a `BDB_teljes_unabridged.tsv` összes „ψ”-előfordulása és feloldása; hibás helyek listája igehelyenként (forrás-sor, hibás alak, javított alak), a rejtett esetekkel (ψ-ból feloldott igehely, amelynek a könyve/fejezete létezik, de a szövegkörnyezet Zsoltárt jelent). Szabály: csak ott javíts, ahol a „ψ” egyértelmű; a bizonytalan helyek külön listába.
2. **⛔ M1 — a lista jóváhagyása**, a forrásfájl javítása előtt. A konkordancia nyers adat: a javítás proveniencia-sora legyen a repóban (naplo), és a README jelezze a javított dataset-verziót.
3. **M2 — javítás a forrásban** (split('\t')/'\t'.join, csv modul nélkül; írás előtt sor-összevetés az eredetivel; minta: eszkozok/igazolas_migracio.py).
4. **M3 — az érintett `adat/forditasok.tsv` sorok igehelyei gépileg cserélődnek** (a forras_hash a forrásból számolódik: az újraszámolt hash-t a 13. szabály és az E19 elfogadja-e, ellenőrizd). `kezi` sort csak a jóváhagyás szerint érinthetsz: a H8415 (78. sor) és a H7585 (81. sor) `kezi`; ezeket külön listázd.
5. **M4 — kapu:** a 13. kapu jelzése a javított adaton 0; negatív teszt (hibás ψ-feloldás → jelzés marad).

## Nem cél
Az éles `lexikon/` újragenerálása (külön feladat); a Dán 22:14 forráshiba javítása; új fordítás.
