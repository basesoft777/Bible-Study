# ELLENOR_F73 — F73_BDB_SZELLEM_TESZT_BRIEF.md · 8f70e4f^..HEAD (8f70e4f, 54bd5ad, 4b31389, 7c1738b)

*A `fuggetlen-ellenor` jelentése (2026-10-06). Az ellenőr nem tudott fájlt írni, ezért a jelentést az orkesztrátor mentette el; a táblázat a jelentés szövege, a „Kezelés” szakasz az orkesztrátoré.*

**Eredmény: ELTÉRÉS, 3 tétel (mind alacsony vagy hatókörön kívüli).**

Az ellenőr a `teszt_bdb_zaras.py`-t és az `ellenoriz.py`-t a szerepe miatt nem futtatta. Ezeket a végrehajtó mérte (napló, „DT53 alkalmazása”).

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Hatókör | OK | — | `git diff --numstat 8f70e4f^..HEAD`: 6 fájl, mind a brief `ir` listáján. |
| forditasok.tsv bájtra változatlan | OK | `adat/forditasok.tsv` | `git diff --stat 8f70e4f^ HEAD -- adat/forditasok.tsv` üres; `git diff --numstat main...HEAD -- adat konkordancia` üres. A commitolt fát fedi, a munkafát nem. |
| ⛔ 2. lépés: a DT53 négy helye csak döntés után | OK | `naplok/BDB_FORDITAS_zaras3.py:62-66` | Az F73.1 csak a H4390, H5674, H6743 sort hozta; az F73.2 megállás; a négy hely az F73.3-ban. A felhasználói döntést a repóból nem ellenőrizhette. |
| SZELLEM_KOVETELT H2451 | OK | `zaras3.py:62`; `forditasok.tsv:371` | A kontextus egyszer áll. BDB `:2298`: „gives her pupils the divine spirit 1:23” → DT-F38g (3). |
| SZELLEM_KOVETELT H3847 | OK | `zaras3.py:63`; `forditasok.tsv:466` | BDB `:3590`: „the spirit of ׳י clothed itself with Gideon”. |
| SZELLEM_KOVETELT H5012 ×2 | OK | `zaras3.py:64-65`; `forditasok.tsv:454` | Mindkét kontextus egyszer áll; BDB `:4687`: kétszer „under influence of divine spirit”. |
| SZELLEM_KOVETELT H5117 | OK | `zaras3.py:66`; `forditasok.tsv:393` | BDB `:4788`: „of spirit of ׳י Num 11:25-26, (E), Isa 11:2”. |
| SZELLEM_KOVETELT H4390 | OK | `zaras3.py:71`; `forditasok.tsv:270` | A nagybetűt a DT-F38h (b) mondja ki, nem a BDB szövege; a 28:3 kisbetűs. |
| SZELLEM_KOVETELT H5674 | OK | `zaras3.py:72`; `forditasok.tsv:176` | BDB `:5314`, `:6834` (H7307 9a) → DT-F38h (c). |
| SZELLEM_KOVETELT H6743 | OK | `zaras3.py:73`; `forditasok.tsv:671` | BDB `:6314`: „Judg 14:6 the Spirit . . . rushed upon him”; a napló idézete egyezik. |
| `osszes`, kulcslefedettség | OK (statikusan) | `forditasok.tsv` | 21 nagybetűs alak 14 Strongon a `forditas_hu`-ban; a tábla 14 kulcs, 21 bejegyzés, kulcsonként egyezik. |
| `teszt_bdb_zaras.py` 21/21, `ellenoriz.py`, regresszió | NEM ELLENŐRIZHETŐ | — | A szerep nem engedi a futtatást. |
| H5674 gyökérok-elemzés | OK | napló 21–30; `zaras3.py:104-115` | A `replace(uj, regi)` a 9dea846 (F38.308) óta üres; a hiba nem (iv) típusú. |
| A H5674 tesztmódosítása nem gyengít | OK | `teszt_bdb_zaras.py:209-216, 162-168` | Az `assertIn(regi, uj)` helyére idempotencia-ellenőrzés került; a `count(regi)==0` erősebb. |
| A javítólista H5674-sorának átírása | **ELTÉRÉS** (alacsony) | `naplok/BDB_FORDITAS_zaras_javitasok.tsv:448` | A sor két szerkesztést (082c77a, majd 9dea846) egyetlen, valójában le nem futott cserévé von össze; a proveniencia-hűség sérül, a teszt ereje nem. |
| Elavult megjegyzések | **ELTÉRÉS** (alacsony) | `zaras3.py:107-108`; `teszt_bdb_zaras.py:167, 209` | „a `regi` az `uj` resze”, és a tesztnév `test_h5674_regi_resze_az_ujnak` az F73.1 után hamis. |
| 4. feltétel: a #38 `fugg` mezője tartalmazza a #73-at | **ELTÉRÉS** | `F38_BDB_FORDITAS_BRIEF.md:15` | `fugg: [34, 56, 72]`; a befogadáskor maradt ki, a fájl nincs a #73 `ir` listáján. |
| 3. feltétel: a hat Strong oka egyenként | OK | napló 9–17 | — |
| Helyőrző-szabály (DT53) | OK | `DONTESEK.md:128` | Végleges DT-szám nincs. |
| TSV-írás csv nélkül | OK | `zaras3.py:122-181` | `import csv` nincs; a 448. sor 6 mezős, LF. |
| Proveniencia | OK | napló 3., 42. sor | — |
| A1–A6 | OK / tárgytalan | — | E12–E15 0 találat. |
| CI (saját `futtat.py`) | OK | — | E2–E16, E19, E26 0; E25 3 JELENTÉS a diffen kívül; SÉRTÉS nincs. |
| Adattábla-sorszám Δ | OK | — | Minden `adat/`, `konkordancia/` táblán Δ = 0. |
| ⛔ pontok | OK | — | Az F73.2 után a menet megállt. |

## Kezelés (orkesztrátor, F73.4)

1. **Elavult megjegyzések** — javítva: a `zaras3.py` `alkalmaz` docstringje és a `teszt_bdb_zaras.py` 167. sorának megjegyzése; a teszt neve `test_h5674_csere_idempotens`. Utána `teszt_bdb_zaras.py` 21/21 OK.
2. **A javítólista H5674-sora** — nem javítva: a sor `iras` mezője a két döntést (DT-F38g 2; DT-F38h c) megnevezi, a teszt ezt a sort a jelenlegi szöveg ellenőrzésére használja. A felhasználó dönti el, kell-e kétsoros történeti bontás (lezáráskor jelezve).
3. **A #38 `fugg` mezője** — a #73 hatókörén kívül (`F38_BDB_FORDITAS_BRIEF.md` nincs az `ir` listán); a 6. lépés lezárásakor, a #38 fejlécének váltásával együtt, a felhasználó jóváhagyásával.
