# SZOTAR S1.7 — héber kiejtés-jelöltek (D28, 26 lemma)

*2026.09.28 · `SZOTAR_BRIEF.md` v1.7 §3 S1.7. Csak jelölt-lista, nem ír a
kivétel-táblába — a jóváhagyás az S1.7 utáni ÁLLJ tárgya.*

## 1. 24 vagy 26? — az eltérés oka

A `SZOTAR_BRIEF.md`-ben **mindkét szám előfordul**, mert két, egymást
felülíró döntésréteg van benne:

- A **8. szakasz (Döntésnapló) D13 sora** — a brief v1-es, 2026.09.23-i
  eredeti szövege — **24/24 lemmát** ír célként. Ez a bejegyzés a
  döntésnapló append-only konvenciója szerint **nem lett utólag
  átírva** (a projekt szokása: a döntésnapló historikus, a hatályát egy
  későbbi D-sor vonja vissza vagy pontosítja, a régi sor szövege marad).
- A **D28 (2026.09.27)** ezt kifejezetten felülírja: a `T2.2` (`ed79575`)
  két új héber tokent (H8414 *tohu*, H0922 *bohu*, a `TEREMT-002`
  motívumhoz) vitt be a jóváhagyott brief előtt — a felhasználó a
  szűkítés helyett a bővítést választotta, és rögzítette az általános
  hatókör-szabályt: *„a szótári réteg héber hatóköre a menet indító
  commitjának tokenhalmaza; a szám ebből származik, nem rögzített”*
  (D28). Ez a szám **24 → 26**.
- A brief minden **más** helye — a §0 0.4/0.5/0.11/0.17 sora, az S3/S9/S14
  szerep-leírás, a **§3 S1.7 tétel maga** („26 lemmájára”), a §3 ÁLLJ-sor,
  a §4 Várt számok táblája („héber kiejtés-jelöltek: 26 (D28)”) és a §7
  1. menet prompt záró sora — **26-ra van frissítve** (l. a fejléc „v1.2 →
  v1.3 változásai” bekezdését: „D28 új” és a §3/§4/§7 26-ra igazítva).

**Következtetés: az irányadó szám 26, nem 24.** A D13 24-es száma
történeti maradvány egy már felülírt döntésből, nem érvényes cél. Ez a
menet a **26**-os hatókört állítja elő.

## 2. Hatókör-ellenőrzés (D28 szabálya: „a menet indító commitjának
tokenhalmaza”)

Az `adat/elofordulasok.tsv` `strong` mezőjének `+`-on szétbontott,
H-kezdetű, egyedi értékei (a `lexikon_general.py` `strong_tokens =
strong.split('+')` logikájával, minden motívumon át) **jelen menetben
(2026.09.28, `claude/szotar-s1-menet`) pontosan 26 tokent adnak** — nincs
eltérés a D28-nál mért 26-tól, tehát **nincs ok új ÁLLJ-ra** (a D28
szabálya csak akkor kívánna megállást, ha egy token kiesne vagy a
G-halmaz változna).

| Strong | Motívum(ok) | OSHL lemma |
|---|---|---|
| H0127 | HAMART-001 | אֲדָמָה |
| H0430 | MENNY-001 | אֱלֹהִים |
| H0779 | HAMART-001 | אָרַר |
| H0922 | TEREMT-002 | בֹּהוּ |
| H1121 | MENNY-001 | בֵּן |
| H2403 | HAMART-001 | חַטָּאָה |
| H2416 | ANTROP-001 | חַי |
| H2555 | HAMART-001 | חָמָס |
| H3548 | KIRALY-001 | כֹּהֵן |
| H3678 | KIRALY-001 | כִּסֵּא |
| H4467 | KIRALY-001 | מַמְלָכָה |
| H5303 | HODIT-001, MENNY-001 | נְפִלִים |
| H5315 | ANTROP-001 | נֶ֫פֶשׁ |
| H6093 | HAMART-001 | עִצָּבוֹן |
| H6975 | HAMART-001 | קוֹץ |
| H7043 | HAMART-001 | קָלַל |
| H7121 | ISTENTISZT-001 | קָרָא |
| H7451 | HAMART-001 | רַע |
| H7496 | HODIT-001 | רְפָאִים |
| H7497 | HODIT-001 | רָפָה |
| H7585 | ALVIL-001 | שְׁאוֹל |
| H7843 | HAMART-001 | שָׁחַת |
| H8004 | KIRALY-001 | שָׁלֵם |
| H8034 | ISTENTISZT-001 | שֵׁם |
| H8414 | TEREMT-002 | תֹּ֫הוּ |
| H8415 | TEREMT-001 | תְּהוֹם |

## 3. Módszer

- Forrás: `konkordancia/OSHL_lexikalis_index.tsv` `atiras` mezője (SBL
  Academic-stílusú, Unicode diakritikus jelekkel), **nem** a nyers
  niqqud-szöveg — a D24 szerint ez a jobb irányú módszer, mert a nehéz
  esetek (néma *he*, shuruk/holam-vav mint magánhangzó-hordozó, dagesh)
  már eldöntöttek az OSHL-átírásban (l. a `naplok/
  SZOTAR_S0_heber_jeloltek.tsv` korábbi, nyers-niqqud-alapú próbájának
  tanulsága, amely pontosan ezt a következtetést vonta le 55,6%-os
  egyezéssel, D24).
- Szabálytábla: `adat/kiejtes_heber_jeloltszabalyok.tsv` — 20 szekvenciális,
  literális karakter-csere (aleph/ayin elesik; š→s, ṣ→c, ṭ→t, ḥ→h, q→k,
  y→j; a makron/cirkumflex hosszú magánhangzók á/é/í/ó/ú-ra; a redukált
  a/e rövidre). A két meglévő, jóváhagyott `adat/kiejtes_kivetelek.tsv`
  sor (H7121 *qārāʾ*→„kárá", H8034 *šēm*→„sém") igazolja a fő szabályokat
  — mindkettő pontosan visszaadva.
- Generátor: `eszkozok/heber_kiejtes_jeloltek.py` → `naplok/
  SZOTAR_S1_heber_jeloltek.tsv` (26 sor, nem ír a kivétel-táblába).
- **Homográf/inflektált OSHL-változatok** (5 Strong-nál van több OSHL-sor:
  H1121, H2403, H2416, H7451, H7497): a fájl-sorrend szerinti **első**
  bejegyzés a reprezentatív (nincs gyakorisági mező a választáshoz) — a
  további változat(ok) a `megjegyzes` oszlopban fel vannak sorolva, hogy a
  jóváhagyó ne veszítse el őket.

## 4. Egyezési arány — méréshatár

A brief a „26 lemmán mért egyezési arányt" kéri. **Létező, jóváhagyott
magyar referencia jelenleg csak 2 a 26 tokenből** van (`adat/
kiejtes_kivetelek.tsv`, KIEJT-migráció): H7121 és H8034. A projektben
elérhető másik héber „arany" készlet (`naplok/
SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`, 49 pár, raw niqqud-alapú) csak
ugyanezt a két Stronggot fedi a 26-os készletből (a többi arany pár más
lemmákhoz tartozik — l. a `naplok/SZOTAR_S0_heber_jeloltek.tsv` régi
próbájának 36 egyedi párja, amelyből is csak ugyanez a kettő egyezik
Stronggal). **Ez a korlát nem új felismerés — a D24 már rögzítette, hogy
„az 55,6%-os próba nem mérföldkő", és a S1.7-nek éppen ez a szerepe: az
OSHL-alapú módszertan újramérése, amelyhez ez a menet minden elérhető
referenciát felhasznált.**

| Mérőszám | Érték |
|---|---|
| Jóváhagyott referenciával rendelkező token | 2/26 (H7121, H8034) |
| Ezekre az egyezés | **2/2 (100%)** |
| Referencia nélküli (új jelölt, jóváhagyásra vár) | 24/26 |

**A 24 új jelölt helyessége emberi jóváhagyást igényel** — ez pontosan az
S1.7-utáni ÁLLJ tárgya, nem gépi mérhető ezen a mintaméreten.

## 5. Eredmény

`naplok/SZOTAR_S1_heber_jeloltek.tsv`: 26 sor, mind a 26 Stronghoz van
OSHL-referencia (0 hiányzó), 2/2 egyezés a meglévő jóváhagyott
mintákon, 0 eltérés.
