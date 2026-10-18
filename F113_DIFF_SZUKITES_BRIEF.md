---
feladat: 113
cim: A diff-osztályozó blokk szerint döntő fajtáinak szűkítése a változás fajtája szerint
kod: DIFF_SZUKITES
tipus: feladat
fazis: 2
modell: opus
allapot: lezarva
ag: claude/diff-szukites
ad: a render_diff_osztalyoz.py minden ismert fajtája a változás fajtája szerint dönt, nem a blokk szerint (öt szűkítés, mindegyikhez negatív teszt); a mai próbán az S2.8 0 ismeretlen + 44 felhasznalo_elfogadva; az N-F09i lezárva
kovetkezo: merge a felhasználótól; utána az N-F09i lezárása külön tételben (DIFF_SZUKITES_zaras.md)
munka: folyamat
olvas: [eszkozok/render_diff_osztalyoz.py, eszkozok/teszt_render_diff_osztalyoz.py, naplok/ELLENOR_SZOTAR_S2_negyedik.md, naplok/SZOTAR_S2_zaras.md, F09_SZOTAR_S2_BRIEF.md, naplok/SZOTAR_S2_diff.tsv, naplok/SZOTAR_S2_ismeretlen.tsv, naplok/SZOTAR_S2_parositas_minta.md, adat/szotar_szerepek.tsv, adat/licencek.tsv, adat/kiejtes_kivetelek.tsv, eszkozok/kiejtes.py, generalt_proba/F09_szotar_s2_proba/, lexikon/]
ir: [eszkozok/render_diff_osztalyoz.py, eszkozok/teszt_render_diff_osztalyoz.py]
fugg: [9]
pr: #392
lezarva_osszegzes: "mind az öt ismert fajta a változás fajtája szerint dönt (DT-F113a/b); 73 teszt, a negatív tesztek a régi kódon elbuknak; a próbán 0 ismeretlen + 55 felhasznalo_elfogadva (44 + 11 név szerinti, DT-F113b); a blokk szerinti maradék ágak: N-F113a"
---

# F113_DIFF_SZUKITES_BRIEF.md — A diff-osztályozó blokk szerint döntő fajtáinak szűkítése

*FELADATOK #113 · Modell: opus · v1 · 2026.10.18 · forrás: N-F09i (`NYITOTT_FELADATOK.md`), `naplok/ELLENOR_SZOTAR_S2_negyedik.md` 1–2. eltérés, `naplok/SZOTAR_S2_zaras.md` 4b, `F09_SZOTAR_S2_BRIEF.md` K10, `DONTESEK.md` DT191 (a 2026-10-18-i (1) pont: „a nem kulcs cellák minden eltérése ismert kategória kell legyen, különben `ismeretlen`”).*

## 1. Cél

A #9 (SZOTAR S2, PR #381) S2.8 kapuja a `eszkozok/render_diff_osztalyoz.py`-val bizonyítja, hogy a régi és az új lexikon között nem tűnik el tartalom. A kapu cellánként vet össze, de néhány „ismert fajta” a **blokk** szerint dönt, nem a **változás fajtája** szerint, ezért elnyelhetne egy valódi cserét. A mostani adaton ilyet a négy független ellenőrzés nem talált (`manual`, a 16 próbafájl word-diff szúrópróbái, kb. 120 sor), de ez megfigyelés, nem kódgarancia. A felhasználó ezt kimondott korlátként fogadta el (zárójelentés 4b, K10), és a szűkítést kötelezővé tette, mielőtt egy következő menet a kapura támaszkodik (N-F09i).

A menet végére **minden ismert fajta a változás fajtája szerint dönt**: egy mezőpár csak akkor kap ismert kategóriát, ha maga a változás (a régi és az új érték viszonya) ismert fajtájú. Hogy a mező melyik blokkban vagy szakaszban áll, az a kategória *nevét* adhatja (`alap`), az *elfogadást* nem.

## 2. Hatókör

**Benne van:** az alábbi öt hely szűkítése a `render_diff_osztalyoz.py`-ban, mindegyikhez legalább egy negatív teszt a `teszt_render_diff_osztalyoz.py`-ban; a két meglévő teszt átírása, amely a tág viselkedést rögzíti; a mai próba újrafuttatása saját kimeneti fájlba.

A sorszámok a `main` `9b16603a` állapotán igazolva (2026-10-18); a menet elején újra igazolandók.

| # | Hely (mai kód) | Mai viselkedés (blokk szerint) | Szűkítés (változás szerint) |
|---|---|---|---|
| 1 | `_mezo_kat` `:833-834` (`if szakasz.startswith('5. Szótári'): return 'szerep'`) | az `5. Szótári` szakaszban bármely cellacsere `szerep` | `szerep` csak akkor, ha a régi és az új érték is az `adat/szotar_szerepek.tsv` tényleges szerep- vagy forrásneve (`szerep`, `forras` oszlop, illetve a belőlük renderelt forrásnév), vagy állapotjelző (`allapot` oszlop értékei, `nincs adatosítva`, `nincs forrás`, `a forrás nem tárgyalja`). Minden más csere `ismeretlen` |
| 2 | `_mezo_kat` `:828-829` (`if alap == 'licenc': return 'licenc'`) | az `idezes`/`kolofon` blokkban bármely csere `licenc` | `licenc` csak akkor, ha a régi és az új érték is licencszöveg (az `adat/licencek.tsv` értékei: licencnév, licencjelzés) vagy licencjelző (`projekt-adat`, `minden jog fenntartva`, `CC …` alakú jelölés). Minden más csere `ismeretlen` |
| 3 | `_mezo_kat` `:826-827` (`re.sub(r'\d+', '#', a) == re.sub(r'\d+', '#', b)` → `alap`) | a csak számjegyben eltérő cella mindig elfogadott | csak a darabszám-, szavazatszám- és sorszám-jellegű szám frissülése elfogadott (pozitív lista, l. 3. lépés). A nem kulcs cellában álló **igehely** (`\d+:\d+`, `Zsolt(LXX) 87:11` → `87:12`), **jelentésszám** (pl. BDB `2.c`, LSJ jelentés-sorszám) és **verzifikációs szám** cseréje `ismeretlen` |
| 4 | `_mezo_kat` `:815-818` (az `_LXX_ALLAPOT` kivétel az eltűnés-próbából és az `a in _LXX_ALLAPOT` → `alap` ág) és `_kanon` `:801-807` (az állapotszavak `ALLAPOT`-ra normalizálása) | az LXX-állapot bármire cserélhető (`egyező` ↔ `eltérő`, `egyező` → `—`) | csak a **helyőrző → állapot** irány elfogadott (`''`/`—`/`-`/`–` → `_LXX_ALLAPOT` eleme). `egyező` ↔ `eltérő`, bármely állapot → másik állapot, állapot → helyőrző (`—`): `ismeretlen`. A `_kanon` nem olvaszthatja össze az állapotszavakat |
| 5 | `_par_kategoria` `:613-624` (a `:621-623` ág) és `_LATIN_ZAROJEL_RE` `:465`; ugyanez a hiba a `_kiejtes_kulonbseg` `:758-771`-ben (a zárójeles rész bármely nem-héber tartalma elfogadott) | írásjegyes sorban a zárójeles rész bármely latin cseréje `kiejtes`, magyar szót is enged (`כֹּהֵן (pap)` → `(király)`) | a zárójeles rész cseréje csak akkor `kiejtes`, ha **mindkét oldal átírásnak tűnik** (latin átírási karakterkészlet, nem magyar szó; l. 5. lépés). Az (1) lépés nem-None ága (`:931` hívás) és a cellánkénti ág **ugyanazt** a szűkített `_kiejtes_kulonbseg`-et futtatja |

**Nincs benne:**
- új kategória, új elfogadott sor, a `FELHASZNALO_ELFOGADOTT` / `ATKULCSOLT_SOROK` / `ISMERT_HIBA_TSK_VERSSZAM` táblák bővítése;
- a negyedik ellenőrzés 3. és 4. eltérése (a `FELHASZNALO_ELFOGADOTT` darabszám-kötése — a mai kódban már `FELHASZNALO_DARAB` —, illetve az elavult dokumentumrészek);
- a `_torzscikk_kat` `:687-688` (`5. Szótári` → `szerep`) mint *alap*: ez a párosítatlan törzscikksor kategóriája, amelyet a `tovabb_el` próba véd; a szűkítés a mezőpár-elfogadásra vonatkozik. Ha a végrehajtó szerint ez is blokk szerinti elfogadás, a zárójelentésben jelzi, nem javítja;
- a próbarender (`generalt_proba/F09_szotar_s2_proba/`) és az éles `lexikon/` módosítása; a verziózott `naplok/SZOTAR_S2_*` fájlok felülírása.

## 3. Lépések

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév kiírása, összevetés a fejléc `modell` mezőjével; eltérésnél megállás. Saját ág az `origin/main`-ből. A fenti sorszámok újraigazolása a mai kódon; eltérésnél a brief táblázata szerinti *helyet* (függvény + feltétel) keresd, ne a számot.
1. **Kiinduló mérés** (a módosítás előtt): `python eszkozok/render_diff_osztalyoz.py --proba generalt_proba/F09_szotar_s2_proba --tsv naplok/DIFF_SZUKITES_kiindulo_diff.tsv`; elvárt: `ismeretlen` 0, `felhasznalo_elfogadva` 44, a kategóriák darabszáma egyezik a `naplok/SZOTAR_S2_diff.tsv`-vel. Ha nem egyezik, megállás és jelzés (a kiinduló állapot nem a #9 lezárt állapota).
2. **Szerep-szűkítés (1. hely).** A szerep- és forrásnevek és az állapotjelzők listája az `adat/szotar_szerepek.tsv`-ből töltődik (`split('\t')`, nem `csv`; CLAUDE.md), nem a kódba írt literálokból. Negatív teszt: az `5. Szótári` szakaszban egy szerepmátrixon kívüli szöveg cseréje (pl. a cellában egy szabad magyar mondat → másik mondat) `ismeretlen`; pozitív teszt: a mai éles eset („Cremer (1895)” → „unfoldingWord …”, `HAMART-001_TORZSCIKK.md`) továbbra is `szerep`, ha mindkét név a mátrixban vagy a renderelt forrásnevek között van — ha nincs, az ⛔ (4. lépés). A konstruált példa az ellenőrzésből: „UBS DNTG” → „Mounce” csak akkor `szerep`, ha mindkettő a mátrix forrásneve **és** a cella szerepe a mátrix szerint változott; ezt a végrehajtó teszttel rögzíti, és a zárójelentésben megnevezi, hogyan döntött.
3. **Licenc-szűkítés (2. hely) és szám-szűkítés (3. hely).**
   - Licenc: az értékkészlet az `adat/licencek.tsv`-ből (`split('\t')`) + a licencjelzők (`projekt-adat`, `minden jog fenntartva`, `CC BY…`/`CC BY-SA…`/`CC0` alak). Negatív teszt: az `idezes`/`kolofon` blokkban `| Jób 1:1 | régi sor |` → `| Jób 1:1 | új sor |` `ismeretlen` (a mai `teszt_render_diff_osztalyoz.py:80-82` ennek az ellenkezőjét rögzíti: átírandó). Pozitív teszt: `(projekt-adat)` → `(minden jog fenntartva)` `licenc` (éles eset, 8 fájlban).
   - Szám: pozitív lista — darabszám (önálló egész a cellában, `n=…`, `… db`, `… sor`, `… előfordulás`), szavazatszám (`(Votes: N)`, `(N)` a TSK-sorban), sorszám (a szerep-fejléc `#### N.` száma). Minden más számváltozás nem ismert fajta. Negatív tesztek: nem kulcs cellában `Zsolt(LXX) 87:11` → `87:12` `ismeretlen`; `BDB 2.c` → `BDB 3.c` `ismeretlen`; `1Móz 3:16` → `1Móz 3:17` `ismeretlen`. Pozitív teszt: `Votes: 15` → `Votes: 17` és egy darabszám-cella frissülése továbbra is elfogadott.
4. **LXX-állapot (4. hely).** Az `_LXX_ALLAPOT` kivétel kivétele az eltűnés-próbából (`egyező` → `—` = eltűnés), az `a in _LXX_ALLAPOT` → `alap` ág szűkítése a helyőrző → állapot irányra, és a `_kanon`-ból az állapotszavak összevonásának kivétele (vagy: csak a módszerjelző `MODSZER`-normalizálása maradjon). Negatív tesztek: `egyező` → `eltérő` `ismeretlen` (a mai `:84-85` ennek az ellenkezőjét rögzíti: átírandó); `eltérő` → `egyező` `ismeretlen`; `egyező` → `—` `ismeretlen`; `kutatói azonosítás függőben` → `egyező` `ismeretlen` (a mai próba ilyen sorai a `FELHASZNALO_ELFOGADOTT`-ban név szerint állnak, ezért a próbán nem okoznak új `ismeretlen`-t). Pozitív teszt: `—` → `egyező` `lxx_korpusz`.
5. **Zárójeles átírás (5. hely).** Egy `_atirasnak_tunik(x)` próba, amelyet a `_par_kategoria` (1) ága és a `_kiejtes_kulonbseg` is hív, mindkét oldalra:
   - csak latin átírási karakterkészlet (a mai `_LATIN_ZAROJEL_RE` osztálya, pont, aposztróf, kötőjel), **és**
   - nem magyar szó: az ajánlott, adatalapú próba, hogy az új oldal megegyezik a cella héber/görög szavának kiejtésével (görög: `eszkozok/kiejtes.py`; héber: `adat/kiejtes_kivetelek.tsv`), a régi oldal pedig vagy ugyanennek a szónak egy korábbi átírása (SBL-diakritika: `ā ē ī ō ū ḥ ṭ ṣ š ś ʾ ʿ ə`, vagy a próbán mért régi→új párok alakja), vagy a sor egy másik mezőjében álló átírással azonos. Ha az adatalapú próba nem valósítható meg, a végrehajtó a karakter-alapú változatot választja, és a zárójelentésben megnevezi, melyiket követte és miért.
   Negatív tesztek: `כֹּהֵן (pap)` → `כֹּהֵן (király)` `ismeretlen` az (1) lépés nem-None ágán **és** a cellánkénti ágon; görög cellában `ἀβύσσου (mélység)` → `ἀβύσσου (szakadék)` `ismeretlen`. Pozitív tesztek (éles esetek, `naplok/SZOTAR_S2_parositas_minta.md`): `ἐπικαλέσηται (epikalesētai)` → `(epikaleszétai)` és `ἀβύσσου (abussou)` → `(abüsszú)` továbbra is `kiejtes`.
6. **Mérés a módosítás után:** `python eszkozok/render_diff_osztalyoz.py --proba generalt_proba/F09_szotar_s2_proba --tsv naplok/DIFF_SZUKITES_diff.tsv` (az esetleges `ismeretlen` sorok: `naplok/DIFF_SZUKITES_ismeretlen.tsv`); a teljes tesztkészlet (`python eszkozok/teszt_render_diff_osztalyoz.py`) zöld; az éles `lexikon/` 16 fájlja bájtra változatlan (a kód hash-ellenőrzése, `naplok/F09_S0_lexikon_hash.tsv`). A kimenet proveniencia-sora: `scope=generalt_proba/F09_szotar_s2_proba vs lexikon | forras=eszkozok/render_diff_osztalyoz.py --proba | ts=…`.
7. **⛔ Ha új `ismeretlen` jelenik meg:** a menet megáll, és a sorokat tételesen (fájl, sor, a régi és az új mező, melyik szűkítés fogta meg) a felhasználó elé teszi. **Új szabályt, új kategóriát vagy új elfogadott sort a menet nem ír**; a döntés a felhasználóé (`DONTESEK.md`-tétel helyőrzővel: `DT-F113a`, …).
8. **⛔ Független ellenőrzés** (`fuggetlen-ellenor`, `naplok/ELLENOR_DIFF_SZUKITES.md`) a base..head diffen: mind az öt szűkítés a változás fajtája szerint dönt-e; a negatív tesztek valóban a szűkített ágat érik-e (nem egy korábbi feltétel fogja meg őket); van-e még blokk vagy szakasz szerint elfogadó ág a `_mezo_kat`-ban és a `_par_kategoria`-ban.
9. **Lezárás:** `NYITOTT_FELADATOK.md` N-F09i (vagy a számkiosztás adta végleges N-szám) lezárva, a mérés hivatkozásával; zárójelentés `naplok/DIFF_SZUKITES_zaras.md` (mi változott helyenként, a tesztek száma, a mérés, a választott változat az 5. lépésben); brief-fejléc `allapot`, `lezarva_osszegzes`. PR-cím `[ELLENŐRZŐ]`; push és merge csak a felhasználótól.

Commit tételenként (`F113.0:`, `F113.1:` …), UTF-8 fájlból.

## 4. Elfogadási feltételek

| | Feltétel |
|---|---|
| E1 | Mind az öt helyen a mezőpár elfogadása a régi→új érték viszonyán múlik; blokk- vagy szakasznév önmagában nem ad ismert kategóriát |
| E2 | Mindegyik szűkítéshez legalább egy negatív teszt (a 3. lépés konstruált példái), és a mai éles esetekre pozitív teszt; a `:80-82` és a `:84-85` teszt átírva; a teljes tesztkészlet zöld |
| E3 | A szerep-, forrás- és licencértékek az `adat/szotar_szerepek.tsv`-ből és az `adat/licencek.tsv`-ből töltődnek (`split('\t')`), nem kódbeli literálból (a licencjelzők kivételével) |
| E4 | A mai próbán (`generalt_proba/F09_szotar_s2_proba` vs `lexikon/`) az S2.8: **0 `ismeretlen` + 44 `felhasznalo_elfogadva`**; ha nem, a 7. lépés ⛔ |
| E5 | Az éles `lexikon/` és a `generalt_proba/` bájtra változatlan; a verziózott `naplok/SZOTAR_S2_*` fájlok változatlanok |
| E6 | `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; CI zöld |

## 5. Döntésnapló

- **A brief írásakor (2026-10-18):** a kapura támaszkodó következő feladat a #36 (LEXIKON_UJRAGEN, M1 diff-elemzés: „minden eltérés oka megnevezve … váratlan eltérés → megállás”), és a #10 (LEXIKON_LEZARAS), mert a DT186 szerint az éles `lexikon/`-t a #11 1. lépcsője után a #36 vagy a #10 generálja. A #11 a `nulladiff.sh`-t használja (M4), nem ezt az osztályozót. A #113 a befogadáskor a #36 és a #10 `fugg` mezőjébe került (felhasználó, 2026-10-18, chat).
- Új döntés a menet közben helyőrzővel: `DT-F113a`, `DT-F113b` …; új nyitott tétel: `N-F113a` ….
