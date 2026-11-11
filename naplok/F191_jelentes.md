# F191 jelentés — tanúindex a visszhang-réteghez

*2026-11-11 · modell: claude-sonnet-5-5 (a kért) · ág: `claude/tanuindex-8ed546` · brief: `F191_TANUINDEX_BRIEF.md`*

## Mi készült

- `konkordancia/Tanu_atyak_index.tsv` (97 572 sor) + `konkordancia/Tanu_atyak_mu.tsv` (21 790 sor): HCF `commentaries.sqlite` → Károli-alakú igehely-tartomány, atya, év, mű, forrás-URL. A `txt` (idézet) nincs benne. 6,1 + 3,4 MB.
- `konkordancia/Tanu_rabbinikus_index.tsv` (5 259 sor, 0,5 MB): Sefaria links → Midrash/Talmud/Mishnah/Tosefta/Targum hely; csak a lexikonmotívumok 289 versével átfedő sorok (a teljes Tanakh 254 250 sor / ~24 MB: N-F191a).
- `eszkozok/tanu_index.py` (`epit-atyak`, `epit-rabb`, `keres`, `minta`) + `eszkozok/teszt_tanu_index.py` (22 teszt, zöld).
- `konkordancia/Tanu_index_README.md`, `adat/datasetek.tsv` (2 sor), `adat/licencek.tsv` (2 sor), nyitott tételek: `nyitott/uj/tanuindex-8ed546.md` (N-F191a–d).

## Licenc (a letöltés előtt)

- **HCF:** `LICENSE`: a kompiláció (metaadat) közkincs-dedikáció; az idézetek fair use alapon, a dedikáción kívül → csak metaadat került az indexbe.
- **Sefaria links:** a fejlesztői oldal „Links License”: „CC-BY” (verzió nélkül) → letölthető és közölhető forrásmegjelöléssel; a szerkesztő (az orkesztrátor továbbításával, 2026-11-11) CC BY-ként elfogadta, forrásmegjelöléssel „Sefaria, CC BY” (DT-F191a; N-F191c lezárva). A Sefaria-szövegek (szövegenként külön licenc) nincsenek az indexben.
- Nyers adat: `D:\pardes_tanu\hcf\commentaries.sqlite` (sha256 `693e4a90…cd82`), `D:\pardes_tanu\sefaria\links0–17.csv` (sha256 a README-ben).

## HAMART-minta

| Vers | atya (pontos) | atya (fedő ≤10 vers) | rabbinikus (pontos) | rabbinikus (fedő ≤10) |
|---|---|---|---|---|
| 1Móz 3:17 | 8 | 16 | 48 sor / 46 mű (Midrash 38, Talmud 7, Targum 3) | 54 sor |
| 1Móz 4:7 | 4 | 7 | 48 sor / 47 mű (Midrash 22, Mishnah 2, Talmud 20, Targum 4) | 49 sor |
| 1Móz 4:11 | 2 | 5 | 9 sor / 9 mű (Midrash 6, Targum 3) | 10 sor |
| 1Móz 6:5 | 2 | 5 | 54 sor / 54 mű (Midrash 26, Mishnah 7, Talmud 16, Targum 3, Tosefta 4) | 58 sor |
| 1Móz 6:11 | 1 | 1 | 16 sor / 16 mű (Midrash 7, Mishnah 2, Talmud 3, Targum 4) | 16 sor |

Az atyai pontos számok egyeznek a felmérés kézi mérésével (8/4/2/2/1).

## Független ellenőrzés és javítókör

Az ellenőrzés (11 eltérés) után egy javítókör: (1) a Sefaria fejezetszintű ref vége az MT-fejezet hossza (Jóel 3 → Jóel 2:28–32); (2) a nem létező Károli-kezdővers sorai kimaradnak (107 sor: Dán 13–14, Eszt-kiegészítések, Jób 38:39–41 …); (3) a HAMART-tábla „mű” = különböző mű, a sorszám külön; (4) a Talmud/Mishnah kategória kommentárjai a README-ben jelezve; (5) a `licencek.tsv` HCF-sora szó szerinti idézettel és commit-hashes URL-lel; (6) a Google Books-URL `dq=`/`q=` paramétere (idézetszöveg) kivéve; (7) a `hcf_id` leírása és a veszteségnapló kiegészítve. Nem változott: a mu-tábla fejléce (a forrás/licenc a fő index fejlécében áll).

## Mutató a #183-nak (nem írtam az `eszkozok/visszhang/`-be, sem a `VISSZHANG_README.md`-be)

Javasolt sor a `VISSZHANG_README.md`-be: „A tanúréteg helyi indexe: `konkordancia/Tanu_index_README.md`; lekérdezés: `python eszkozok/tanu_index.py keres "1Móz 3:17" --max-szelesseg 10`.” A tanúállítás a lapra csak az `adat/visszhang_tanuk.tsv`-n át, saját szavas összefoglalóval kerülhet.

## Ismert korlátok

- UT-átvezetés nincs (63 972 sor `nt_feltetelezett`, N-F191b); a középkori Tanakh-kommentárok kimaradtak (N-F191d); a HCF nem csak atyákat tartalmaz: az `atya_kategoria` és az `ev` szűrésre való.
- A CI nem futtatja a `teszt_tanu_index.py`-t (a workflow-t a #183 szerkeszti); helyben: `python eszkozok/teszt_tanu_index.py`.
