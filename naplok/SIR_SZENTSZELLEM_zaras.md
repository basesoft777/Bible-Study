# F35 zárójelentés

- Ág: claude/f35-sir-szentszellem. Döntés: DT-F35a (a)(b)(c) jóváhagyva, alkalmazva.
- F35.2 (M4): SEMA 237–238. sor, sense → jelentés; E9 86 → 84, ellenoriz.py változatlan.
- F35.4 (M2) Sir → JSir: jeloltek.tsv:329; genezis/1Moz_10v1-11v32:121; motivumlog/PaRDeS_motivumok.md:142, 330, 382, 579 (egyik sem GENERÁLT blokkban, egyik sem idéz lekérdezés- vagy proveniencia-kulcsot, ezért mind cserélve). MARAD: adat/auditok.tsv:169–171 (scope=range:Sir 2:8, (a) szerint).
- F35.4 Szentlélek → Szent Szellem: genezis/1Moz_8v1-22_bovitett.md:144, 194, 204.
- MARAD (Károli-idézet / szabályidézet): 1Moz_1v2-2v3:93, 95; 1Moz_3v7-24:267.
- Generált lexikonfájlok vizsgálata (külön lista):
  - Károli-idézet, marad: ANTROP-001_TORZSCIKK:96; ANTROP-001_TUDOMANYOS:108; TEREMT-001_TORZSCIKK:88; TEREMT-001_TUDOMANYOS:159.
  - Forrásréteg-mező, NEM javítva, döntésre: `adat/elofordulasok.tsv` 169. sor (ANTROP-001, 1Kor 2:14) „kulcsszo” mezője: „Érzéki (pszükhikosz); Isten Lelkének (pneuma)”. Ez a Károli-vers szavait idézi (ugyanaz a sor `kapcsolodas`-a már „Isten Szellemének”), ezért idézetnek vettem; érinti ANTROP-001_TORZSCIKK:100 és TUDOMANYOS:71. Ha javítandó: a mező átírása + ANTROP-001 újrarenderelés (nem céleset).
  - Forrásréteg-mezőben javítandó Szentlélek/Isten Lelke más lexikonsor: nincs.
- Újrarenderelés: nem történt (nincs javított forrásmező).
- M3: teszt_lekerdez_sir 11/11 OK (rögzített n: 24, 15, 1, 38, 10 változatlan); ellenoriz.py SÉRTÉS 0 (RENDBEN 11, KÉZI 2, JELENTÉS 3); a forrásrétegben megmaradó „Szentlélek” csak a 3 jóváhagyott idézet/szabály helyen.
- Független ellenőrzés nem történt (az orkesztrátor futtatja).
