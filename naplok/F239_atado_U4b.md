# F239 átadó — U4b (gépi javítások) → az U5-csomag (a szerkesztő nézésének előkészítése)

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820). A javítások és a gyökérokok: `naplok/F239_jelentes.md`, „U4b”. Az U4 bemenete változatlanul érvényes: `naplok/F239_atado_U4.md`.*

## Miért cserél a session

Az U4b végén a kontextus kb. 334 ezer token volt (plafon: 150–200 ezer, CLAUDE.md munkamód 10). Az U5-csomag új sessionben, ebből az átadóból indul; a session az U4b-ből csak ezt és az `F239_atado_U4.md`-t olvassa.

## Az U4b eredménye (röviden)

- CI F217: a kódkönyv 9 új sora (F239.27); az export helyben lefut.
- E41: az eszköz 7 hozzárendelési hibája javítva, teszttel (F239.28); a TEREMT-001-en 1 ELTÉR marad: a 79. sor idézete (5Móz 33:13) — **prózai, az U6-é**, az E41 addig piros.
- Számozás-átvezetés (görög/latin → Károli) közös függvényben, teszttel (F239.29); a két hibás tanúsor javítva (F239.30: Zsolt 118:24, Zsolt 29:7).
- Az index két hivatkozása: a forrás helyes, a generált blokkot a main-en az Action írja.
- Mérőtábla +5 sor; a brief `ir` és `kovetkezo` mezője frissítve (F239.31).
- **Nyitott, az integrátornál:** a SZIVARGAS-tábla `hol` értéke az U3b-ben megfogott hibához (szabályhiány; kérdés elküldve).

## Az U5-csomag (a következő session feladata; az integrátor döntése szerint)

1. **A lapnézet** az új generátor előnézetéből, pontosan az `F239_atado_U4.md` 1. pontja szerint: `python.exe`-lista (egyszerre egy lapgen-futás, más session folyamatát soha nem állítod le); a két ideiglenes kerülőút (`adat/motivum_kapcsolatok.tsv` `DT-F239a` → `DT9991`; `eszkozok/lapgen/megjelenites/md/kizart.py` arány-ág), `python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívül>`, utána a két fájl visszaállítva (`git status` tiszta); a lapnézet a `eszkozok/lektor_felulet/lapnezet.py` `epit()`-jével, a TUDOMANYOS-út az előnézetre irányítva. **Fájlként a repón kívül; nem publikálod**, a megjelenítést az integrátor végzi.
2. **A lektori lista három csoportban:** a `naplok/KIADAS_TEREMT-001_lektor.md` 142 tétele (lektor 23 + 3/b 119), tételenként egy olvasói mondattal:
   - (a) **a szerkesztő dönt:** a próza tartalma, a lektor kérdései, a 3/b tartalmi tételei;
   - (b) **javítandó, gazdával (U6), csak tájékoztatás:** az F2 hamis tételei (K2, K9, K19, K20, K36, K47, K69, K70, K99, `naplok/ALLITAS_TEREMT-001_itelet.md`), az F1 79. sora, és a független ellenőr prózai ELTÉRÉS-ei (az 1Móz 7:11 „csak itt és a 8:2-ben”, a „95”);
   - (c) **a generátor hibái** (M-CSERE, M-NYERS, M-RÁRAKÓDÁS stb.) → gazda a lapgenerátor; egy N-tétel helyőrzővel a `nyitott/uj/nervous-kare-9d2361.md`-be (a meglévő N-F239a/b mellé, a következő betűvel), a 218c bemeneteként, mechanizmusonként csoportosítva, a `naplok/HIBA_MECHANIZMUSOK.md`-vel összevetve.
   A csoportosítás nem dönt el tételt, csak a gazdát mutatja.
3. Commit (`F239.<n>:`), push a `claude/nervous-kare-9d2361`-re, a PR első sora, jelentés az integrátornak: a lapnézet fájlútja, a három csoport darabszáma, fej-hash.

## Mit NEM kell elolvasni

Az U4b diffjét, a `proza_allitas.py`-t és a visszhang-kinyerőket (kész, tesztelt), az `ALLITAS_TEREMT-001.md` teljes kézi listáját, a független ellenőr OK-sorait.
