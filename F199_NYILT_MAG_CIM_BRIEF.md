---
feladat: 199
cim: A nyílt mag helyőrzőinek cseréje — cím, szerző, DOI, közzétételi hely — és a HELYORZO kapu
kod: NYILT_MAG_CIM
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/nyilt-mag-cim
ad: a nyílt mag fejléceiben és szövegeiben a „[A LEXIKON CÍME]” és a „<KANONIKUS_FORRAS_URL>” helyőrző helyén a megállapított adat (magyar szövegben „Logosz-lexikon”, angolban „Logosz Lexikon”; Demeter Tamás, ORCID, DOI, logoszlexikon.hu); új kapu a nyers helyőrző ellen
kovetkezo: "Te: a draft PR áttekintése; merge-et az orkesztrátor végzi a felhasználó kérésére"
munka: folyamat
olvas: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py]
ir: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py, nyilt_mag/, F199_NYILT_MAG_CIM_BRIEF.md]
fugg: []
nem_fugg: [198]
---

# F199_NYILT_MAG_CIM_BRIEF.md — A nyílt mag címe, szerzője, DOI-ja

*FELADATOK #199 · Modell: sonnet · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó döntései, 2026-11-11, az orkesztrátor közvetítésében):** a lexikon címe „Logosz Lexikon”, a szerző „Demeter Tamás” (ORCID 0009-0005-9254-9731), a nyílt adatmag lefoglalt DOI-ja 10.5281/zenodo.24141612 (Zenodo-piszkozat, a HAMART `/kiadas` után közzétéve), a Károli–Strong DOI-ja 10.5281/zenodo.24141884, a kanonikus domain logoszlexikon.hu.

**Hatókör.** Csak a nyílt mag exportálója, kapuja és tesztje; a lexikonlap és a `lexikon_general.py` helyőrzői (`KANONIKUS_FORRAS_HELYORZO`, `LEXIKON_CIM_HELYORZO`) érintetlenek, a `CITATION.cff` nem része a nyílt magnak.

## Teendő
1. Konstansok és szövegek a generátorban (cím, szerző, ORCID, DOI-k, domain, közzétételi hely = `https://doi.org/<DOI>`), magyarul és angolul (OLVASSEL, README, KIADAS, RELEASE, a GENERÁLT-fejlécek, KODKONYV).
2. Kapu: `HELYORZO` (nyers helyőrző bukik; cím, szerző/ORCID, közzétételi hely kötelező); a `KANONIKUS` és `KETNYELV` ellenőrzés az új hellyel.
3. Tesztek, egy független ellenőrzés, legfeljebb egy javítókör, draft PR.

## Garanciák
- G1: a diff csak az `ir` fájlokat érinti; E28 0, nyílt mag kapuja 0 BUKÁS.
- ⛔ A merge nem ennek a sessionnek a dolga.
