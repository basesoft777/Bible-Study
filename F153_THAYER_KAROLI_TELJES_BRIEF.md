---
feladat: 153
cim: A Thayer-fordítás Károli-mankója a teljes Újszövetségre — a kész Thayer-sorok újraellenőrzése a teljes #22 párosítással
kod: THAYER_KAROLI_TELJES
tipus: feladat
fazis: 2
munka: adat
modell: sonnet
allapot: dontesre_var
ad: a kész Thayer-fordítások (forditasok.tsv, szotar = Thayer) soronként újraellenőrizve a teljes ÚSZ Károli–Strong párosításával (az evangéliumok és az ApCsel is); az eltérő sorok jóváhagyott döntés szerint újrafordítva (M3-lánc) vagy kézi ítéletre listázva; az adatblokk elavult könyvlistája javítva
kovetkezo: "/kovetkezo (M0 mérés, ⛔ a mérés után: az eltérő sorok sorsa)"
ag: claude/f153-thayer-2f248a
olvas: [adat/forditasok.tsv, adat/karoli_strong/, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_sigla.tsv, adat/terminologia.tsv, adat/tiltott_fordulatok.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, forditas/prompt_v5_1.md, eszkozok/thayer_jelolt/, eszkozok/glossza_lexikon_forditas.py, eszkozok/forditas_kapuk.py, F142_THAYER_M3_BRIEF.md, F132_THAYER_SZAKASZ_BRIEF.md]
ir: [adat/forditasok.tsv, eszkozok/thayer_jelolt/adatblokk.py, eszkozok/thayer_jelolt/karoli_ujraellenoriz.py, eszkozok/thayer_jelolt/teszt_lanc.py, naplok/THAYER_KAROLI_TELJES_naplo.md, naplok/THAYER_KAROLI_TELJES_meres.tsv]
fugg: []
nem_fugg: [7, 12, 27, 38, 121, 131]
---

# Fnn_THAYER_KAROLI_TELJES_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.11.01 · készítette: `claude-opus-5-5` a felhasználó kérésére (chat,
2026-11-01: „A károli strongozás a teljes újszövetségre kész. Legyen teljes a thayer forditás mankó is”; a brief megírása és
befogadása: „Igen, brief”); befogadás: `/befogad`, a felhasználó jóváhagyásával.*

## 1. Cél

A Thayer szakaszonkénti fordításának adatblokkja (`eszkozok/thayer_jelolt/adatblokk.py`, 1. rész: Károli-szóalakok, #132 brief
2a/3) a #22 Károli–Strong párosításából veszi a Strong magyar alakjait. A #132 és a #142 (THAYER_M3) futásakor a párosítás az ÚSZ-ből
**nem fedte le a Mt, Mk, Luk, Ján és ApCsel könyvet**. Ezeket a #22 D–F csomagja pótolta (PR #537, `b8a1a59a`, F22.48–F22.54).

Az adatblokk a `parok_*.tsv` fájlokat dinamikusan olvassa, ezért **a mankó a jövőbeli futásokra kódmódosítás nélkül teljes**:
`adatblokk.py G1941` ma azt írja, hogy „az ÚSZ-ből le nem fedett könyvek: nincs”. Két dolog marad hátra, ezekről szól a feladat:

1. A **kész Thayer-sorok** a hiányos mankóval készültek. Újra kell ellenőrizni őket a teljes Károli-alakokkal, és ahol a teljes
   adat mást mutat, döntés kell.
2. Az `adatblokk.py` docstringje elavult tényt állít („ma: Mt, Mk, Lk, Jn, ApCsel”), ráadásul nem Károli-rövidítéssel.

## 2. Felmérés (2026-11-01, a brief írásakor; csak olvasva)

*(proveniencia: scope=adat/karoli_strong/parok_*.tsv (G-Strongok), adat/forditasok.tsv (szotar = Thayer) | forras=eseti olvasó
szkript a brief írójának scratchpadjében (`adatblokk.parok_g()`; „régi” = a Mt, Mk, Luk, Ján, ApCsel sorai nélkül) | ts=2026-11-01)*

**A Thayer-sorok a `forditasok.tsv`-ben** (mind `mezo = forditas_hu`): `sonnet` 71 sor / 13 Strong; `kezi` 5 (G0282, G1941, G1944,
G4151, G5590); `opus` 2 (G0813, G0994); `elavult` 7 (ezek nem tárgyai a feladatnak).

**A mankó változása Strongonként:**

| Strong | link (régi → teljes) | alak (régi → teljes) | új az első 10 alakban |
|---|---|---|---|
| G1941 | 14 → 41 | 7 → 21 | neveztetik, appellált, mellékneve, appellálni, appellálok, appelláltál, appellálván |
| G5590 | 39 → 106 | 30 → 49 | lelkem, lelket, lelke, lelketeket, élet |
| G4151 | 218 → 392 | 36 → 43 | lélektől, lelkek |
| G0994 | 1 → 10 | 1 → 7 | kiálta, kiáltó, kiáltónak, kiáltanak, kiáltozva, kiáltva |
| G0086 | 4 → 8 | 2 → 4 | pokolig, pokolban |
| G1311 | 4 → 6 | 4 → 6 | emészti, nem |
| G5010 | 10 → 11 | 4 → 5 | sorában |
| G0012, G0282, G0540, G0813, G1944, G2671, G5351, G5356 | változatlan | változatlan | — |

Hét Strongnál bővült érdemben a mankó, nyolcnál nem változott. A G4151 és a G5590 sorai `kezi` állapotúak is (DT290 (3), DT329).

**Az eszköz.** A `glossza_lexikon_forditas.py manko` (DT395) a menetjel (`megjegyzes`-előtag) szerint választ sort, a hosszú
`forditas_hu` mezőt a terminológiai kulcsok szintjén ellenőrzi, és a forrást a TBESG/lexikon-hivatkozásból veszi. A Thayer
szakaszsorokra (`jelentes_szam = sz<n>`, forrás: `thayer_szakaszok.tsv`) így nem közvetlenül alkalmazható. Az M0 dönti el,
hogy ezt a parancsot kell-e kiterjeszteni, vagy elég egy kis, Thayer-specifikus ellenőrző (`eszkozok/thayer_jelolt/karoli_ujraellenoriz.py`).

## 3. Hatókör

**Benne van:** minden nem `elavult` Thayer-sor (`sonnet`, `kezi`, `opus`). Az ellenőrzés soronként, régi és teljes mankóval is fut.
A jóváhagyott döntés szerint az eltérő `sonnet`/`opus` sorok újrafordulnak a #142 láncán (`thayer_jelolt/forditas.py`, prompt v5.1,
kapuk). Javul az `adatblokk.py` docstringje. Az új ellenőrzőhöz teszt készül.

**Nincs benne:**
- `kezi` sor átírása. Az eltérés listára kerül, a felhasználó ítél (DT290 (3)).
- A kapuk (#132, #145), a prompt és a `parok_*.tsv` módosítása.
- Új Strong fordítása (az a #142 újrafuttatása, DT332 (1)).
- A teljes Thayer fordítása (#7, D46).

## 4. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md).
1. **M0 — mérés.** Soronként: a fordítás magyar kulcsszavai (az M0-ban rögzített módszer szerint, a `karoli_ellenorzes` /
   `kulcsszo_ellenorzes` mintájára: négybetűs tő) egyeznek-e a Strong Károli-alakjaival a régi és a teljes mankóval. Kimenet:
   `naplok/THAYER_KAROLI_TELJES_meres.tsv` (Strong, szakasz, állapot, régi eredmény, teljes eredmény, az új alakok, összegzés),
   proveniencia-sorral. Ha az ellenőrzés üres, azt is ki kell írni, nem kitölteni (3. szabály).
   **⛔ a mérés után:** a felhasználó dönt a `nem_talal` → `egyezik` váltásokról (ezek megerősítések: nincs teendő), az új
   `nem_talal`-okról és arról, ahol a teljes mankó más uralkodó alakot mutat. Lehetőségek soronként: (a) marad, (b) az M3-lánc
   újrafordítja, (c) kézi ítélet. A döntés tétele: `DT-F<nn>a`.
2. **M1 — az eszköz.** A döntött módszer kódja és tesztje (`teszt_lanc.py` vagy saját teszt). A docstring javítása: „a
   párosítás le nem fedett ÚSZ-könyveit a fájlok alapján méri; 2026-11-01 óta nincs ilyen (PR #537)”.
3. **M2 — újrafordítás** (csak a (b) sorokra). A #142 lánca és kapui változatlanul futnak. A régi sor a DT329 (i) szerint `elavult`
   lesz, felváltás-jelöléssel. Az `adat/forditasok.tsv` írása `split('\t')`/`'\t'.join()`-nal történik, és írás előtt össze kell
   vetni az eredetivel: csak a kijelölt sorok változhatnak.
4. **Mz — zárás.** Napló, a független ellenőr (`fuggetlen-ellenor`), PR. A merge a felhasználóé. A `kezi` sorok listája a
   `kovetkezo` mezőbe kerül („Te: …”).

## 5. Elfogadási feltételek

- A mérés minden nem `elavult` Thayer-sort lefed (ma 78), és mindkét mankóval futott.
- Csak jóváhagyott sor változik a `forditasok.tsv`-ben; `kezi` sor nem változik; a bájt-összevetés naplózva.
- Az újrafordított sorok minden gátoló kapun átmentek; a `modell` mező a ténylegesen futott modell.
- Az `adatblokk.py` docstringje nem állít elavult lefedettségi hiányt; a tesztek zöldek.

## 6. Döntésnapló

- `DT-F153a` (⛔ M0): az eltérő sorok sorsa: szűk (b), a felhasználó „b” válasza; a G1941 sz1–sz4 újrafordítása nem változtatott a szövegen. *Alkalmazva.*
