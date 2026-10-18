# F117.2 — teljes szöveg-összevetés: 8 bizonytalan pár (⛔)

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` · végrehajtó: claude-opus-5-5 · 2026-10-18*

proveniencia: scope=az A–D′ célhalmaz (346 Károli-vers, 20 fejezet, blokk-igazítással a Károli c-1..c+1 és a KJV c-2..c+2 fejezeteken) | forras=Karoli_1908.tsv + KJV_Strongs_teljes.tsv + TAHOT_kivonat.tsv (`eszkozok/versmegf_szoveg_osszevet.py --teljes`; a Karoli_versmegfeleltetes.tsv olvasása nélkül) | kimenet=naplok/F117_szoveg_osszevetes.tsv (483 sor, ebből 346 célvers, 137 kontextus) | itelet=naplok/F117_itelet.tsv (scope=manual, modell=claude-opus-5-5, n=346) | ts=2026-10-18

## 1. Eredmény osztályonként

| Osztály | Vers | Elfogadott pár | Azonos szám | Eltolt | Fejezetváltó | Nincs pár | Bizonytalan |
|---|---|---|---|---|---|---|---|
| A (13 fejezet, a C nélkül) | 261 | 261 | 103 | 153 | 5 | 0 | 4 (Hós 2:1, Jób 17:1–3) + 1 (Ézs 64:1) |
| C (Dán 3:31–33) | 3 | 3 | 0 | 0 | 3 (→ KJV 4:1–3) | 0 | 0 |
| B (Préd 9:21–23, Jób 39:34–38) | 8 | 8 | 0 | 0 | 8 (→ KJV 10:1–3, 40:1–5) | 0 | 0 |
| D | 67 | 67 | 0 | 64 | 3 (Ézs 3:1 → 2:22, Jón 2:1 → 1:17, 1Sám 24:1 → 23:29) | 0 | 1 (1Sám 20:43) |
| D′ (1Kir 22:43–45, 50–53) | 7 | 7 | 1 (22:43) | 6 | 0 | 0 | 2 (1Kir 22:43–44) |
| **Összesen** | **346** | **346** | **104** | **223** | **19** | **0** | **8** |

- **Ítélet:** mind a 346 célversnél elolvastam a Károli-szöveget és a KJV-verset (a KJV Strong-címkézett szavait). **Korlát:** a KJV-oldalon az „elolvasás” a `KJV_Strongs_teljes.tsv` Strong-címkézett szavainak olvasását jelenti (az `f19_ebible_import.py` csak a Strong-címkés szavakat vette át, teljes KJV-szöveg nincs a repóban), az ítélet ott kulcsszavakra épül (l. 5. pont). Az ítélet minden versen a teljes (szöveg + TAHOT) igazítás párja, eltérés nincs. Két KJV-vers egyformán illő esete nincs.
- **Árva KJV-vers:** nincs, egyik blokkban sem.
- **„Nincs pár”:** egyetlen célversnél sincs.
- **A brief 1. táblázatának várt párjai** mind teljesülnek:
  - Ézs 3:1 = KJV 2:22;
  - 1Sám 24:2 = KJV 24:1;
  - Préd 9:21 = KJV 10:1;
  - Jób 39:34 = KJV 40:1;
  - Jón 2:1 = KJV 1:17, Jón 2:9 = KJV 2:8;
  - Dán 3:31 = KJV 4:1;
  - 1Kir 22:46–49 = KJV 22:45–48, 1Kir 22:45 = KJV 22:44.

## 2. A bizonytalan párok (a DT205 (a) szerint: gépi eltérés, vagy 1-2 / 2-1 lépés)

| # | Károli-vers (szöveg eleje) | Teljes igazítás | Szöveg-igazítás | Ok | Kézi ítélet |
|---|---|---|---|---|---|
| 1 | Hós 2:1 „Pereljetek anyátokkal, pereljetek…” | 2:2 | 2:1;2:2 | a két igazítás eltér | **2:2**, egyértelmű (Plead with your mother); a KJV 2:1 („Say ye … Ammi … Ruhamah”) a Károli Hós 1:11 végén áll |
| 2 | Jób 17:1 „Még mindig csúfot űznek belőlem!…” | 17:2 | 17:1 | a két igazítás eltér | **17:2**, egyértelmű (mockers, provocation) |
| 3 | Jób 17:2 „Kezest magadnál rendelj…” | 17:3 | 17:2 | a két igazítás eltér | **17:3**, egyértelmű (surety, strike hands) |
| 4 | Jób 17:3 „Minthogy az ő szívöket elzártad…” | 17:4 | 17:3;17:4 | a két igazítás eltér | **17:4**, egyértelmű; a KJV 17:1 („My breath is corrupt…”) a Károli Jób 16:22 második fele |
| 5 | Ézs 64:1 „Oh, vajha megszakasztanád az egeket…” | 64:1;64:2 (1-2) | 64:2 | 1-2 lépés, és a két igazítás eltér | **KJV 64:1–2 egy Károli-versben**: az eleje = 64:1, a „mint a tűz … felforralja; hogy nevedet…” = 64:2 |
| 6 | 1Kir 22:43 „És jára Asának … útjában…” | 22:43 (2-1) | 22:43 (2-1) | 2-1 lépés | **KJV 22:43 első fele** |
| 7 | 1Kir 22:44 „Csakhogy a magaslatokat nem rombolták le…” | 22:43 (2-1) | 22:43 (2-1) | 2-1 lépés | **KJV 22:43 második fele** (nevertheless the high places) |
| 8 | 1Sám 20:43 „Felkele ezután és elméne. Jonathán…” | 20:42 (2-1, a 20:42-vel) | 20:42 (2-1) | 2-1 lépés | **KJV 20:42 második fele** (and he arose and departed) |

A gépi eltérés (1–4) mind olyan helyen áll, ahol a szomszéd Károli-fejezet utolsó verse két KJV-verset fog át (Hós 1:11, Jób 16:22). A csak szöveg-jelű igazítás ott egy verssel később „kapja el” a fejezetváltást. A kézi olvasás mind a négy helyen egyértelmű.

## 3. Kontextus: összevonások a célhalmazon kívül (tételesen, F91-szabály)

A blokk-igazítás szerint ezek a Károli-versek két KJV-verset fognak át. A célhalmazon kívül esnek, de rajtuk múlik, hogy a célfejezetek KJV-ablaka hézag nélkül fedett:

| Károli-vers | KJV | Az F91-szabály szerint („csak az első KJV-vers a pár”) |
|---|---|---|
| Hós 1:11 | 1:11 + 2:1 | pár: 1:11; a KJV Hós 2:1-nek nincs saját Károli-verse |
| Jób 16:22 | 16:22 + 17:1 | pár: 16:22; a KJV Jób 17:1-nek nincs saját Károli-verse |
| Péld 11:31 | 11:31 + 12:1 | pár: 11:31; a KJV Péld 12:1-nek nincs saját Károli-verse |
| Jób 36:33 | 36:33 + 37:1 | pár: 36:33; a KJV Jób 37:1-nek nincs saját Károli-verse |
| Ézs 64:1 (célvers) | 64:1 + 64:2 | pár: 64:1; a KJV Ézs 64:2-nek nincs saját Károli-verse |

Ezek a KJV-versek a `tsk_kulcs` KJV→Károli irányában „nincs pár”-t kapnak, ha az F91-szabály változatlan. A TSK-soraik így elvesznek, pedig a tartalmuk a Károli-versben megvan.

A célfejezetek nem célversei közül a Préd 9:1–20 (= KJV 8:16–9:18) és a Jób 39:1–33 (= KJV 38:39–39:30) eltolt a kontextus-igazítás szerint. Ezek nem tartoznak az A–D′ halmazba. A 4.4 halmaz-őre ellenőrzi, hogy a tábla ott ugyanezt adja-e; ha nem, ott megállás lesz.

## 4. Döntési kérdések (javaslattal)

1. **Az 1–4. pár (csak gépi eltérés, a kézi ítélet egyértelmű).**
   - Javaslat: a kézi ítélet szerinti pár kerül a javító bemenetbe, `megjegyzes`-ben a gépi eltérés okával.
   - Alternatíva: a két igazítás egyezését kikényszeríteni a szöveg-jel finomításával (névkulcs), és utána újrafuttatni.
2. **Az 5. pár (Ézs 64:1, 1-2).** Javaslat: az F91-szabály változatlan, a pár 64:1, `megjegyzes`: „KJV 64:1–2 egy Károli-versben”.
   - Ez a KJV 64:2-t (és a 3. pont négy KJV-versét) a KJV→Károli irányban pár nélkül hagyja.
   - Ennek a feloldása (a második KJV-vers visszafelé is a Károli-versre mutasson) a `tsk_kulcs` szabálya volna, külön N-tétel.
3. **A 6–8. pár (2-1: két Károli-vers egy KJV-versen).**
   - **(a) javasolt:** mindkét Károli-vers ugyanazt a KJV-verset kapja, `megjegyzes`: „KJV 22:43 két Károli-versben (22:43–44)”. A `tsk_kulcs` KJV→Károli iránya listát ad (`j2k`), ezért a KJV-vers mindkét Károli-versre visszamutat. A meglévő tábla is ismer egy KJV-versre eső több Károli-sort (a Préd 2:26 összevonási sora).
   - **(b)** Csak az első Károli-vers kapja a párt, a második „nincs pár” (a 1Kir 22:44 és az 1Sám 20:43 TSK nélkül marad).
   - **(c)** Csak a második kapja.

## 5. Korlát: a KJV-oldal csak Strong-címkézett szavakból — újraellenőrizendő ítéletek

A `konkordancia/KJV_Strongs_teljes.tsv` csak a Strong-címkézett szavakat tartalmazza (az `f19_ebible_import.py` szándékosan csak a `\w …|strong` szavakat vette át); teljes KJV-szöveg nincs a repóban. A kézi ítélet a KJV-oldalon ezért kulcsszavakra épült. Ahol az ítélet versfélen, mondathatáron vagy fejezetváltón múlik, a teljes KJV-szövegen újra kell ellenőrizni (N-F117c; a sorok jelölése: `naplok/F117_itelet.tsv` `ellenorizendo` oszlop). Összesen **28** ítélet:

| Jelölés | Darab | Károli-versek |
|---|---|---|
| versfél (2-1 / 1-2 lépés) | 4 | Ézs 64:1, 1Kir 22:43, 1Kir 22:44, 1Sám 20:43 |
| összevonás-szomszéd (a KJV-vers az előző Károli-vers második fele) | 5 | Hós 2:1, Jób 17:1, Jób 37:1, Péld 12:1, Ézs 64:2 |
| fejezetváltó pár | 19 | 2Móz 35:36, Dán 3:31, Dán 3:32, Dán 3:33, Hós 14:1, Én 5:17, Én 5:18, Én 5:19, Préd 9:21, Préd 9:22, Préd 9:23, Jób 39:34, Jób 39:35, Jób 39:36, Jób 39:37, Jób 39:38, Ézs 3:1, Jón 2:1, 1Sám 24:1 |

A célhalmazon kívüli összevonás-versek (Hós 1:11, Jób 16:22, Péld 11:31, Jób 36:33) nem célversek, ezért az ítélet-fájlban nincs sorruk; a rajtuk múló ítélet a célhalmaz első versénél van jelölve (összevonás-szomszéd). A 2–4. bizonytalan pár (Jób 17:2–3) párja a Jób 17:1-étől függ, külön nincs jelölve.
