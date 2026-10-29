ELTÉRÉS: 4 tétel

# ELLENOR_ISTENTISZT001_BDB_FRISSITES

*A `fuggetlen-ellenor` jelentése, a végrehajtó mentette, mert az ellenőrnek nincs fájlíró eszköze. Az eltérés- és a lényegi OK-sorok a jelentés szerint, rövidítve; a végén a végrehajtó javítóköre.*

- **Megbízás:** a DT-F131r (a `DONTESEK.md` BDB-frissítés sora), valamint az N-F131f és az N-F131g. Brieffájl nincs.
- **Tartomány:** `6f30ab03..3d747af4` (8 commit), ág: `claude/istentiszt-bdb-hu-frissites`.
- **Modell:** a tényleges `claude-opus-5-5` egyezik a kért `opus`-szal.
- **Korlát:** az ellenőr teszteket és mérőszkripteket a szerepe szerint nem futtathat; a futtatást igénylő pontok NEM ELLENŐRIZHETŐ minősítést kaptak.

| pont | eredmény | fájl:sor | indok |
|---|---|---|---|
| E19 (b), `thayer_bemenet` | OK | `eszkozok/thayer_jelolt/thayer_bemenet.py:78, 96` | Mindkét olvasóban csak a `x.rstrip('\r')` került be; LF-bemeneten semmit nem változtat. |
| E19 (b), regressziós teszt | OK | `eszkozok/thayer_jelolt/teszt_bont.py:228` | A teszt LF és CRLF bemenetet ír, két fájlnévvel (a gyorsítótár nem takarja el a különbséget). A javítás nélkül a CRLF-ág eltérne. |
| E19 (a), `_ir` | OK | `eszkozok/ellenorzes/tesztek/test_szabalyok.py:73-74` | Csak a `newline=''` és egy megjegyzés változott. |
| „5 bukás, LF-írással 0”, „192 teszt zöld” | NEM ELLENŐRIZHETŐ | – | A forrás a végrehajtó próbafuttatása, az ellenőr nem futtathatott tesztet. |
| `--strong`, `general(ts, csak)`, `reszleges_szoveg` | OK | `eszkozok/bdb_jelolt/hu_illeszt.py:242-258, 300-325, 340-357` | Csak a megnevezett Strongok sorait cseréli. A `--ts` token megmarad, a jelölés nem halmozódik. CRLF-táblán megáll. A személy-szabály nincs a kódban. |
| a tábla diffje | OK | `adat/bdb_szakasz_hu.tsv` | 45 sor: 1 fejlécsor és a H4397/H8034/H9004 44 sora. Ebből 6 tartalmi változás (H4397 2–3, H8034 2–3, H9004 2, 6), 38 csak proveniencia-ts. A hash és a hosszösszegek megmaradnak. |
| a 6 tartalmi sor | OK | `adat/bdb_szakaszok.tsv:18165-18166, 33915-33916, 36486-36488` | A „Kö^ii. 1. NNN” a fejbe került, az 1. szakasz a valódi jelentésponttal kezdődik. Ez szakaszhatár-javítás. |
| H9004 | OK (nem regresszió) | `adat/bdb_szakaszok.tsv:36483-36488` | A 3–5. sor a frissítés előtt is üres volt. |
| a lexikonlap | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:631, 636, 656` | Pontosan 3 sor változott; helyőrző a lapon 0. |
| 101 = 98 + 3; 49 rontás-jelölt; a minta | OK | `naplok/BDB_HU_frissites_naplo.md:28-29, 134, 137-186, 188, 311-316, 350` | A számok egyeznek a napló kimenetével. |
| N-F131g számai | **ELTÉRÉS (E1)** | `NYITOTT_FELADATOK.md:55` | A 3 424 / 173 / 665 / 576, a 367–401 / 245–272 és a 201 / 125 egyik hivatkozott szkriptből sem vezethető le. |
| helyőrző címsorban | **ELTÉRÉS (E2)** | `naplok/BDB_HU_frissites_naplo.md:1` | A címsorban `DT-F131r, N-F131f, N-F131g` áll; a szamkiosztas és az E5 ütközése miatt ez tilos. |
| a CRLF-lista | **ELTÉRÉS (E3, kicsi)** | `naplok/CRLF_olvaso_felmeres.md:17` | A lista a 2fa792b2 állapotát rögzíti; a HEAD-en a `hu_illeszt.py:245` sor `:247`. |
| E16 | **ELTÉRÉS (E4)** | `eszkozok/ellenorzes/tesztek/test_szabalyok.py` | Ellenőrzőt érint a PR, ezért a címe `[ELLENŐRZŐ]` előtaggal kell kezdődjön. |
| a DONTESEK oszlopszáma, idézetek, helyőrző a kódban | OK / NEM ELLENŐRIZHETŐ | `DONTESEK.md:471` | Az oszlopszám 8, rendben; a „vedd át a döntéseket” idézet megvan; helyőrző a kódban 0. A „első prio arany cikk teljes” idézet a repóban nem ellenőrizhető. |

## Javítókör (végrehajtó, 2026-10-29)

1. **E1:** új mérőszkript: `naplok/BDB_HU_szakaszos_meres.py`. Kimenete:
   - szakaszonként fordított 3 424 Strong, ebből 173-ban van `elakad` sor (665 sor);
   - egyben fordított 576 Strong, `elakad` sor 0;
   - nyelvtani személy jelölőnek véve: a mai generálásban 367 sor / 245 Strong, a repóbeli táblában 199 sor / 124 Strong (a részleges frissítés után);
   - valódi szakaszfej: 86 sor.

   Az N-F131g ezekre a számokra javítva (a „367–401 / 245–272” és a „201 / 125” egy másik definícióból jött, ezek kikerültek), a proveniencia a szkriptre mutat.
2. **E2:** a napló címsorából kikerültek a helyőrzők; a hivatkozás a címsor alatti dőlt sorba került.
3. **E3:** a `CRLF_olvaso_felmeres.md` a HEAD-en újragenerálva (`hu_illeszt.py:247`), a darabszám továbbra is 58.
4. **E4:** a PR címe `[ELLENŐRZŐ]` előtaggal indul.
