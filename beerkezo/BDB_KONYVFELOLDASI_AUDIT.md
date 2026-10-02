# BDB könyvfeloldási audit

*Csonk a `/befogad`-nak · készült az F38 (BDB_FORDITAS) menetében, a DT-F38 döntés
kiegészítése alapján (felhasználó, 2026.10.01) · fejléc nélkül, a `beerkezo/README.md` szerint*

## Cél

A `konkordancia/BDB_teljes_unabridged.tsv` könyvfeloldási hibáinak teljes felmérése és
javítása: ahol a forrás egy igehelyet rossz bibliai könyvhöz kötött, ott a helyes könyv
megállapítása egy független BDB-forrással összevetve, versszám-ellenőrzéssel, majd a forrás
**és** a már elkészült fordítások (`adat/forditasok.tsv`) igehelyeinek gépi cseréje.

## Háttér

- **Az F34 a ψ-hibát javította** (a nyomtatott BDB `ψ` = Zsoltárok jelét a digitalizálás
  nehol más könyvnek oldotta fel): 159 hely javítva (`eszkozok/bdb_psi_javit.py`), 156 hely
  B/R maradék (N-F34, `naplok/F34_M2_maradek.tsv`). A ψ-n túli hibák nem voltak a hatókörében
  (N-F34c: `Dan c:v` = 5Móz, `Lev 28:17` típus; H3117, H6881, H8034, H8478, H9004 …).
- **Az F38 mérései** (`naplok/BDB_FORDITAS_naplo.md`):
  - A 13. kapu (a könyv fejezetszámánál nagyobb fejezet) a forráson az M0-ban 91 szócikkben
    jelzett (83 F34-maradék, 8 N-F34c). Az F38.13 könyvalak-bővítése (`Konyv_normalizalo_tabla.tsv`
    `Forrás-alakok` oszlopa) után **109 szócikkben** (86 F34-maradék, 23 nem); a 18 új jelzés
    mind most láthatóvá vált könyvalak hibás feloldása: pl. `1Chron 119:21`, `1Chron 145:9`
    (= Zsolt), `Ex 43:21`, `Ex 46:6`, `Ex 51:25`, `Ex 45:4` (2Móz-nak csak 40 fejezete van),
    `Nah 7:5`, `Nah 19:12`, `Nah 23:8`, `Nah 47:3`, `Nah 5:14`, `Cant 19`, `Cant 26`, `Cant 34`,
    `2 Chron 105`.
  - **A 13. kapu csak a fejezet-túllépést látja.** Létező fejezetre mutató rossz könyvet nem:
    H0413 a forrásban „1 Samuel 3:22; 5:26; 15:22; 29:19”, a nyomtatott BDB-ben „only in Job
    (3:22; 5:26; 15:22; 29:19)”; „Deut 37:36” = 1Móz 37:36 (a felhasználó jelzése); a
    fordításban H3068 „1Móz 21:83” (vö. 21:33). Gyanús versszám: `Proverbs 22:77` (a
    versszám-ellenőrzés még nem futott, a gyanú nem mérés). Ezek számát ma nem ismerjük.
  - Nem leképezett, többértelmű vagy hibás alakok (F38.13, nem felvéve): `Kings` (2), `Ki`,
    `Sam`, `Chron`, `Chronicles`, `Samuel`, `Ze`, `Jes`, `Esc`, `De`, `En` — a feloldásuk az
    audit dolga.
- **A fordítás hűen viszi tovább a forráshibát** (DT-F38, 2026.10.01): az F38 nem javít, a
  hibás igehely Károli-rövidítéssel kerül az `adat/forditasok.tsv`-be. A gépi csere ezért
  mindkét táblán kell.

## Lépések

1. **Független forrás kiválasztása.** Jelölt: az OpenScriptures Hebrew Lexicon BDB-XML-je
   (`BrownDriverBriggs.xml`, strukturált igehely-hivatkozásokkal). Licenc, verzió, letöltési
   út a `Rendszerfejlesztesi_playbook.md` 2. pontja szerint; `adat/licencek.tsv` sor.
   **⛔ a licenc és a letöltés előtt** (a felhasználó jóváhagyja a forrást és a licencet).
2. **Összevetés szócikkenként.** A két forrás igehely-listájának illesztése (sorrend és
   fejezet:vers alapján, könyvnév nélkül is); eltérő könyv → jelölt csere. Kimenet: tábla
   (`strong`, pozíció, forrásbeli alak, független alak, javasolt Károli-alak, bizonyosság).
3. **Versszám-ellenőrzés.** Minden javasolt igehelyre: létezik-e a fejezet és a vers (a
   könyv fejezetszáma és a fejezet versszáma MT-számozásban; forrás: TAHOT vagy Macula,
   proveniencia-sorral). Lehetetlen igehely nem kerülhet cserébe.
4. **Strong-próba (az F34 mintájára).** A javasolt helyen szerepel-e a szócikk Strong-száma
   (TAHOT, ±1 vers); ami nem igazolható, kézi nézetre megy.
5. **Mérés és jelentés:** hibatípusonként (ψ-maradék, más könyv érvényes fejezettel,
   fejezet-túllépés, vers-túllépés, összeolvadt alak) darabszám; a forrásban és a
   fordításokban érintett szócikkek.
6. **⛔ a gépi csere előtt:** a felhasználó jóváhagyja a csere-táblát (az egyértelmű
   esetek gépi cseréje, a kétesek kézi nézete).
7. **Gépi csere** mezőkulcsos, pozícióhoz kötött cserével (mint az F34): a
   `konkordancia/BDB_teljes_unabridged.tsv`-ben és az `adat/forditasok.tsv` érintett sorain
   (a `forras_hash` frissítésével, ahogy a DT-F34c (1) tette); `kezi` sor csak külön
   jóváhagyással. Utána a 11. és a 13. kapu mind a fordított sorokon, `ellenoriz.py`.

## Javasolt modell

`opus` (az F34 mintájára). A munka nagyobb része determinisztikus szkript; a kétes esetek
előkészítése igényel nyelvi ítéletet.

## Függés

- **F34** (kész): a ψ-javítás szkriptje és csere-mechanizmusa az alap; az N-F34 maradék és az
  N-F34c ebbe az auditba olvasztható (befogadáskor döntendő).
- **F38** (fut): ugyanazt az `adat/forditasok.tsv`-t írja — egyidejűleg nem futhat
  (kölcsönös kizárás). Minél később fut az audit, annál több lefordított sort kell cserélnie;
  a csere az F38 két adagja közötti megállási ponton vagy az F38 lezárása után futtatható.
  Az F38.13 könyvalak-leképezése (`Forrás-alakok`) az audit bemenete.

## Nem cél

- A BDB tartalmi (lexikai) hibáinak javítása, OCR-javítás a könyvneveken túl.
- A fordítások újrafordítása: csak az igehelyek könyve (és a hibás fejezet:vers) cserélődik.
- A Thayer hasonló auditja (külön feladat, ha kell).
- A 11./13. kapu logikájának átírása (új kapu csak külön jóváhagyással).
