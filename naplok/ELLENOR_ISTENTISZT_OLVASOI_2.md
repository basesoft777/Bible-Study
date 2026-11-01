# Független ellenőrzés, 2. kör: ISTENTISZT-001 olvasói forma (DT426, DT427; brief-fájl nincs)

Tartomány: c6340e30..b16c7e5a (5 commit). Ellenőr: `fuggetlen-ellenor` subagent, `claude-opus-5-5` (kért: `opus`).
A jelentést az ellenőr a válaszában adta (fájlíró eszköze nem volt); a végrehajtó mentette, tömörítve, a tételek
változatlan tartalmával. Szerepkorlát miatt az ellenőr nem futtatta a teszteket, az `ellenoriz.py`-t és a repón kívüli
próbát (ezeket a végrehajtó futtatta, l. alább).

ELTÉRÉS: 11 tétel

| # | súly | eltérés | hely |
|---|---|---|---|
| 1 | közepes–magas | az ALVIL-001 12. bevezetője 34 témát ígér, a blokk üres (javaslat); a példa-téma angolul | `ALVIL-001 :883–886` |
| 2 | közepes | ISTENTISZT-specifikus példa („a H7121 a H8034 nélkül”) az ALVIL-001 14. szerepében | `szerep_karoli.py:340` |
| 3 | közepes | a görög kiejtés-pótlás a kiírt alakhoz a lemma kiejtését teszi: „ἐπικαλέομαι (epikaleó)” | `ISTENTISZT :375,447,1465` |
| 4 | közepes | a gépi átírás elhagyja a spiritus aspert: ᾅδης → „adész” | `ALVIL :854` |
| 5 | alacsony–közepes | a héber 8. rövid formájából a H7585-nél hiányzik az alapjelentés; az „asszír” kétséges volta elveszett | `ALVIL :863` |
| 6 | alacsony | a 9. szerep „egyértelmű” számlálója a több jelentéskódú DBH-cellát is ide sorolja | `ISTENTISZT :972,974` |
| 7 | alacsony | a G1941 LSJ jelölt hiánya megszűnt, repóadat nélküli értelmezéssel | `ISTENTISZT :695` |
| 8 | alacsony | kiejtés a magyar toldalék elé szúrva: „θάνατος (thanatosz)-t” | `ALVIL :625` |
| 9 | alacsony | a Rokon szavak SECE-alblokkjai bevezető nélkül | `ISTENTISZT :1107,1156` |
| 10 | alacsony | helyőrző `##` címsorban | `naplok/ELLENOR_ISTENTISZT_OLVASOI.md:38` |
| 11 | alacsony (áthozott) | a commit-üzenetekben nincs tétel-azonosító | – |

Rendben (az ellenőr szerint): a „+SZPA” eltűnt, adatkapcsoló vezérli; a 2/b. kizárja a SECE-t, `LN:`/`GK:` 0 a
`lexikon/` alatt; a TAHOT-átírás 0 az ISTENTISZT-001 és az ALVIL-001 1. és 3. szakaszában; a kézi forrásban csak a
„(besém)” került be; a forrásidézetek érintetlenek; az előző kör 1–6. javítása rendben (a 6. részben, l. 3.); TSV
`split('\t')`; CI 0 HIBA. Mérési gyengeség (a végrehajtó javította): a táblázatsor következő latin cellája (pl. „egyező”)
kiejtésnek számított.

## A végrehajtó válasza

Döntés: DT427 (a felhasználó felhatalmazásával az orkesztrátor). Javítva:
1. A 12. olvasói mondat csak akkor áll, ha a blokk épül (van témadöntés); a magyar név nélküli példa-téma „(fordításra vár)”.
2. A 14. szerep szövege általános („a kombináció egy része”).
3. A kiírt görög alak, ha nem a lemma, a saját gépi kiejtését kapja: „ἐπικαλέομαι (epikaleomai)”.
4. A szókezdő spiritus asper „h”: ᾅδης → hadész.
5. A héber 8.: ha a BDB-fej nem mondja ki az alapjelentést, a TBESH rövid magyar jelentése áll, jelölve; a kétséges
   rokon nyelvi adat „(kétséges)”.
6. A 9.: „egy jelentés” / „több vagy jelölt, nem egyértelmű jelentés” / hozzárendelés nélkül.
7. A G1941 mondata a repó adatát idézi: a `konkordancia/LSJ_teljes.tsv` G1941-sora („… Middle voice from G1909 and
   G2564”) maga az utaló sor; az alapige LSJ-szócikke a Rokon szavaknál áll (az orkesztrátor kérése szerint).
8. A kiejtés a toldalék után: „θάνατος-t (thanatosz)”.
9. A Rokon szavak SECE-alblokkja is bevezetőt kap.
10. A címsorból a helyőrző kikerült.
11. Nem javítva: a #131 utómunka-menetek közös előtagja („ISTENTISZT-001 arany, …”, l. DT424).

A végrehajtó futtatta: a tesztek zöldek; `ellenoriz.py` SÉRTÉS 0; a repón kívüli próbában mind a 8 lap hibátlan
(0 `LN:`, 0 „SZPA”, 0 „H7121 a H8034” más lapon; az ALVIL-001-en a 12. bevezető az általános mondat).
