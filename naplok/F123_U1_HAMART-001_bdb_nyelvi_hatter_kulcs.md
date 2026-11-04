# F123 U1 — HAMART-001: a 6 BDB „nyelvi háttér” szakasz fordítása megvan, de más kulcson

*Vizsgálat, nem javítás (az orkesztrátor kérésére, 2026-11-03). Modell: claude-sonnet-5-5. Fordítás nem futott, prompt nem készült.*

| Strong | A lap által keresett kulcs (`forditas_ehhez`) | A meglévő fordítás kulcsa (`adat/forditasok.tsv`) | Van-e magyar szöveg | A fej magyar megfelelője az em-dash-határral |
|---|---|---|---|---|
| H0127 | `BDB \| H0127 \| H0127 \| nyelvi_hatter \| forditas_hu` | `BDB \| H0127 \| H127 \| teljes \| forditas_hu` (4 101 kar., opus) | **igen** | 268 kar. (angol fej: 267) |
| H2403 | `BDB \| H2403 \| H2403 \| nyelvi_hatter \| forditas_hu` | `BDB \| H2403 \| H2403 \| teljes \| forditas_hu` (11 165) | **igen** | **nem illeszkedik**: a fej `jovahagyott` kézi határa a „sin, sin-offering” után áll (127 kar.), a magyarban nincs ott em-dash (az em-dash-szabály 720 karaktert adna) |
| H6975 | `… H6975 \| H6975 \| nyelvi_hatter …` | `BDB \| H6975 \| H6975 \| teljes …` (822) | **igen** | 62 kar. (angol fej: 63) |
| H7043 | `… H7043 …` | `BDB \| H7043 \| H7043 \| teljes …` (5 129) | **igen** | 600 kar. (angol fej: 540) |
| H7451 | `… H7451 …` | `BDB \| H7451 \| H7451 \| teljes …` (11 292) | **igen** | 173 kar. (angol fej: 149) |
| H7843 | `… H7843 …` | `BDB \| H7843 \| H7843 \| teljes …` (6 390) | **igen** | 533 kar. (angol fej: 514) |

Mind a hat szócikk magyar fordítása megvan, `opus`, kész sor. Hiányzó magyar szöveg szakaszonként: **nincs**.

## Ok
A generátor (`eszkozok/lexikon_general.py`, `_tartalom_heber_etimologia`, kb. 1927. sor) a fejhez külön kulcsot keres: `forditas_ehhez('BDB', t, t, 'nyelvi_hatter', 'forditas_hu')`. A #38 BDB-fordítás viszont szócikkenként egy `teljes` sort írt (`jelentes_szam = teljes`; a H0127-nél az `entry_id` is csupasz `H127`, nem `H0127`). A `nyelvi_hatter` kulcsú sorból a teljes táblában egyetlen van (BDB H7585, ALVIL-001, kézi). A szócikk feje a teljes szócikk eleje: a fordítása a `teljes` sor elején áll.

## Hol kellene javítani (nem javítottam)
1. **Generátor:** ha nincs `nyelvi_hatter` sor, a fej magyar szövege a `teljes` sorból vehető: a `BDB_etimologia_kezi_hatarok.tsv` határa (az első zárójelen kívüli em-dash) a magyar szövegen ugyanúgy alkalmazható. Öt szócikknél (H0127, H6975, H7043, H7451, H7843) a levágott magyar fej hossza a forrás fejével összemérhető (62–600 kar.). A kulcs-keresésnek az `entry_id`-t is kezelnie kell (`H127` ↔ `H0127`).
2. **Kivétel:** a `jovahagyott` kézi határú szócikkeknél (itt H2403) a magyar határ nem vezethető le automatikusan, mert a kézi határ nem em-dash-nál áll; ott a magyar fej vágása kézi (vagy a H7585 mintájára egy `nyelvi_hatter` sor).
3. **Kulcstábla alternatíva:** a `teljes` sorokból `nyelvi_hatter` sorok előállítása egyszeri adatlépésként. Ez írja az `adat/forditasok.tsv`-t, ezért az ütközés miatt a #608 merge-e után.

Az ANTROP-001 H2416-ját nem vizsgáltam részletesen; a `forditasok.tsv`-ben a H2416-nak van `teljes` és `sz1`–`sz…` BDB-sora, `nyelvi_hatter` sora viszont egyetlen szócikknek sincs (a teljes táblában 1 ilyen sor van: H7585). Ha a H2416 hibája a nyelvi háttéré, ugyanaz az ok; ha szakasz-kulcsé (`sz<n>`), külön vizsgálat kell. A közös javításról az orkesztrátor dönt.
