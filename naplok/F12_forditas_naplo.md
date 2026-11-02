# F12.3 — TEREMT-002: nyolc rövid szótári egység magyarul (TERVEZET)

*2026.11.02, `claude-sonnet-5-5`. A `adat/forditasok.tsv` NEM módosult, nincs commit; jóváhagyásra vár. Minta: `naplok/F121_GOROG_ROVID_naplo.md`. Tervezet: `naplok/F12_forditas_tervezet.tsv`.*

- **Forrás (1. lépés):** mind a nyolc egyezik a megadott angollal (`tovabbi_forras` a TBESG-nél, `dbh_forras_idx` az UBS_DBH-nál); eltérés nincs.
- **Javasolt alakok:** G0094 igazságtalan; G0517 láthatatlan; G1373 szomjúság; G2048 puszta; G2756 üres; G3152 hiábavaló; H0922 üresség; pusztaság; H8414 pusztaság; elpusztítottság; káosz.
- **Precedensek** (`adat/glosszak_heber_hu.tsv`, a `forditasok.tsv`-ben azonos angol glosszájú sor nincs): H5767 unjust → igazságtalan; H6772 thirst → szomjúság; H0950/H3445/H4003 emptiness → üresség; H7385 vain → hiábavalóság; H2721 desolation → pusztaság; H2723, H3451, H4875, H4876, H5805, H7584 desolation → elpusztítottság; H2720 desolate → puszta. A `terminologia.tsv` (v4) egyik angol szóra sem tartalmaz sort.
- **Nyelvközi egység:** a hat görög szó a H8414 SECE-megfelelői; a görög „unjust/thirst/futile” a héber párjával azonos magyar tövű (igazságtalan, szomjúság, hiábavaló). A „pusztaság” a H0922 és H8414 közös szava (Károli: „kietlen és puszta”; Ézs 34:11 „pusztaság”).
- **Mankó** (rangsor szójegyzék > Károli > BDB): Károli mind a 8 soron egyezik; BDB egyezik a két héber soron. Két szójegyzék-ütközés, mindkettő kézi ítélettel feloldva (indok a TSV-ben): G2756 „empty” (H4198: kiürült, igeneves) → üres; H8414 „waste” (H1326: pusztulás, absztrakt folyamat) → pusztaság.
- **Kapuk** (`forditas_kapuk.kapuk_futtat`, nyolc soron): SÉRTÉS 0; mind átment (ATMENT). JELZÉS: `6_hosszarany` a G0094 és G2048 soron (egyszavas fordítás, informatív); a többi kapu RENDBEN. A 13. és 15. kapu RENDBEN.
- **Bizonytalan:** G2048 (puszta vs. szó szerinti elhagyatott) és H8414 „waste” (pusztaság vs. pusztulás); a döntés a felhasználóé/orkesztrátoré.
