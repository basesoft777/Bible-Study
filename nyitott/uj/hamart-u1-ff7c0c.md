Utolsó frissítés: 2026.11.03 (F123 HAMART-001 U1 — N-F63e lezárva)

### 2026.11.03 (F123 HAMART-001 U1):

* **LEZÁRVA — N-F63e: a HAMART-001 gerincének tartalmi felülvizsgálata** (a H7451, H7043, H6975 Strong gerinc-elem-e). A felhasználó döntése: „kivesszük” (DT-F123w). Nyitva marad belőle az U2 értelmező döntése: az 1Móz 6:5 és 8:21 `gerinc_elem`-jének átírása (`tematikus:…` vagy más gerinc-elem a versben), és a 651 blokk-kizárás beírása a `jeloltek.tsv`-be a #608 merge-e után.
* **ÚJ (F123 HAMART-001 U1, 2026-11-03) — N-F123p: a BDB „nyelvi háttér” (szócikk-fej) magyar szövege nem jut el a lapra, mert a generátor `nyelvi_hatter` kulcsot keres, a fordítás `teljes` kulcson áll.** Érinti a HAMART-001 H0127, H2403, H6975, H7043, H7451, H7843 szakaszát (a H0127 `entry_id`-ja `H127`), és minden lapot, ahol a szócikk-fejnek magyar szövege van; az ANTROP-001 H2416 esete rokon lehet. Teendő (külön PR, a #608 merge-e után): a `lexikon_general.py` tartaléka a `teljes` sorból a kézi határ szerint, entry_id-normalizálással; a H2403-ra kézi `nyelvi_hatter` sor a H7585 mintájára. Fordítani nem kell. *(Helyőrző; forrás: `naplok/F123_U1_HAMART-001_bdb_nyelvi_hatter_kulcs.md`.)*
