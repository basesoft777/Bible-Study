# ELLENOR_F197 — F197_BDB_HARMADIK_TANU_BRIEF.md · 7095bc63..59846773

*A független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5, friss kontextus) jelentése. Fájlíró eszköze nem volt, ezért a szöveget a
végrehajtó rögzítette, változtatás nélküli tartalommal, összevonva; a „Javítás” oszlop a végrehajtóé (F197.4, `7eab15a2`).*

```
ELTÉRÉS: 8 tétel
```

| # | eltérés (az ellenőr súlyossági sorrendjében) | Javítás (F197.4) |
|---|---|---|
| 1 | **CI E35:** a PR módosítja az `adat/` táblákat, a nyílt mag exportja (`eszkozok/nyilt_mag_export.py`) nincs újragenerálva (8 fájl). | újragenerálva |
| 2 | **⛔ kapu:** a 40 soros próba szabályát (v2, v3) ugyanazon a mintán hangolták; a „0 téves riasztás” mintán belüli; a v1 zajánál a ⛔ szerint meg kellett volna állni. | nem javítható utólag; a jelentés 2. szakasza nyíltan leírja, a v1 utólag lemérve (40 soron 4 / 28 téves riasztás, 8 / 12 megfogva; 200 ponton 28 / 188); DT776 🟡, a döntés a felhasználóé (azóta 🟢, F197.6) |
| 3 | **Kód 1b:** a több Sefaria-bejegyzés `rid`-sorrendű összefűzése a `pontos` illesztéssel hibás pontot rendelhet a sorhoz (10 479 linkelt sor több `rid`-ből, 3 189 `+hom` nélkül); a mintán kívüli 652-t torzíthatja, a seed-103-at nem. | több bejegyzésben álló vers: `barmely`; a mintán kívüli szám 635 |
| 4 | **E32 + félrevezető szöveg:** a `kiir` bekapcsolt fejlécében string-literálban áll a `DT776`, és „egyezés → biztos” szöveg; a modul docstringje ugyanígy. | a szöveg „eltérés → ketes, egyezésnél változatlan, F197”; docstring javítva |
| 5 | **E26:** „s103-N182” (a seed-103 mintaazonosítója) nyitott-tétel számnak látszik. | minden mintaazonosító `s103-` előtaggal |
| 6 | **Kód 1a + G4:** a nem törzs jellegű `form` fejléc („With other prepositions:—”, H0996) törzsként kezelődik: kötelező téves riasztás, és fejlécszöveg a táblában (22 sor). | `TORZS_FORM` minta (egyszavas törzsnév); a táblában 0 ilyen sor |
| 7 | **Napló:** a jelentés 209 kérést említ, a `lekeresek.tsv` 210 sort. | 210 |
| 8 | (a CI-sor része) E30: két ékezet nélküli szó (`ketes`, `forras`) az `1a061261` commit-üzenetében. | nem javítva (a commit-üzenet csak történetírással változna); a szavak kódnevek (`ketes:jp_tanu_sefaria`, `# forras`) |

**OK pontok (kivonat):** modell; G2 (a 2.29-ben csak a `# forras` sor változott); bekötés (`SEFARIA_TANU = False`, csak a `bizonyossag`,
`jp_kezi` érintetlen, egyezésnél nem emel); `ref_versek` / `SEF_KONYV` (39 könyv); `osszevet` = SEMA 2.29.1; arany = F185 szabálya
(188 helyes); a mérés számai a részletfájlokból újraszámolva mind egyeznek; a H8081, H3847, s103-N087 állítások a forrással és a
gyorsítótárral igazolva; licenc (DT631 idézetei); tiltott helyek érintetlenek; adatsor nem törlődött.
**Nem ellenőrizhető (a szerep tiltotta):** G1 `--ellenoriz`, G3 tesztfuttató, a `meres` futtatása, a 652-es szám.
**Diffen kívüli CI-találatok:** E28 `lexikon/HAMART-001_TUDOMANYOS.md:1147` (dátumfüggő, a diff nem érinti a `lexikon/`-t); E25, E27,
E34, E36 jelentés meglévő fájlokra.
