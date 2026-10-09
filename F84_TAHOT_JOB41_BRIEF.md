---
feladat: 84
cim: "TAHOT_kivonat: a Jób 41 pótlása Károli-kulccsal a nyitott esetekből (N-F83a)"
kod: TAHOT_JOB41
tipus: feladat
fazis: 1
modell: sonnet
allapot: megallt
ag: claude/f84-tahot-job41
ad: "A TAHOT_kivonat.tsv-ben a Károli Jób 41:1–34 héber sorai Károli-kulccsal; a #22 a Jóbot egy menetben futtathatja; a CLAUDE.md TAHOT-korlát mondata a mért állapotot írja"
kovetkezo: "Te: ⛔ 1 — (a) a 332 nyitott sor törlése vagy ATVEVE_F84 státusz, (b) a Jób 41:25 kezelése (a szúrópróba nem mutat eltérést; javaslat: törlés, és a vers jelölés nélkül bekerül). Részletek és javaslat: naplok/F84_jelentes.md; döntéstétel: DT-F84a (DONTESEK.md). Utána F84.2. A #22 következő menete előtt fusson (FUGGES 22→84: TAHOT_kivonat.tsv)."
fugg: [83]
olvas: [konkordancia/TAHOT_kivonat_nyitott_esetek.tsv, konkordancia/Macula_heber_Job.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, naplok/F83_Job_versbeosztas_jelentes.md, eszkozok/tahot_lefedettseg_ellenoriz.py]
ir: [konkordancia/TAHOT_kivonat.tsv, konkordancia/TAHOT_kivonat_nyitott_esetek.tsv, eszkozok/tahot_karoli_kulcs_generalas.py, eszkozok/tahot_job41_potlas.py, CLAUDE.md, NYITOTT_FELADATOK.md, konkordancia/TAHOT_TAGNT_README.md]
---

# F84_TAHOT_JOB41_BRIEF.md — TAHOT_kivonat: a Jób 41 pótlása Károli-kulccsal (N-F83a)

*FELADATOK #84 · v1 · 2026.10.09 · alap: a #83 lelete (`naplok/F83_Job_versbeosztas_jelentes.md`, `naplok/F83_zaras.md`) · a #22 Jób-menetének előfeltétele*

## Mit ad, ha kész

A `konkordancia/TAHOT_kivonat.tsv`-ben a Károli Jób 41:1–34 mind a 34 versének lesz héber sora, Károli-kulccsal („Jób 41:n”). Így a #22 a Jóbot egy menetben, a 41. fejezettel együtt futtathatja. A CLAUDE.md TAHOT-korlát mondata a mért állapotot írja le.

## Háttér (a #83 leletéből, ellenőrizendő)

- A Károli Jób 41 34 vers, ugyanannyi, mint az angol (KJV) 41. Az MT-ben ez a 40:25–41:26.
- A `TAHOT_kivonat.tsv`-ben a „Jób 41:” kulcson 0 sor van.
- A `TAHOT_kivonat_nyitott_esetek.tsv`-ben 332 sor áll `ADATMINOSEGI_GYANU` státusszal, 34 különböző `STEPBible_elsodleges` kulccsal (`Job.41.1`–`Job.41.34`), a `STEPBible_masodlagos` oszlopban az MT-kulccsal (`Job.40.25` … `Job.41.26`).
- Az ok: a kulcsgenerátor (`eszkozok/tahot_karoli_kulcs_generalas.py`) `DONTES_FELULBIRALAS` táblája a `("Job", (40, 41))` csoportot téves Károli-versszámokkal (40 = 28, 41 = 25) `ADATMINOSEGI_GYANU`-ra állította. A valós Károli-szám 40 = 19, 41 = 34.
- A generátor bemenetei (`phaseA_all.tsv`, `step1_decisions.tsv`) a scratch-könyvtárban voltak, a repóban nincsenek. A generátor teljes újrafuttatása ezért nem reprodukálható, és nem is cél.

## Hatókör

**Benne van:** a Jób 41 34 versének sorai a nyitott esetekből a fő kivonatba kerülnek, Károli-kulccsal. A nyitott esetek fájljából ezek a sorok kikerülnek (vagy státuszt váltanak, l. ⛔ 1). A generátor felülbírálási bejegyzése a dokumentáció kedvéért javul. A CLAUDE.md TAHOT-mondata pontosodik, az N-F34b és az N-F83a rendeződik a `NYITOTT_FELADATOK.md`-ben.

**Nincs benne:**
- A Jób 40 TAHOT-kulcsainak átszámozása. A Jób 40 kulcsai ma MT-számozásúak (TAHOT 40:(n+5) = Károli 40:n), és a #83 kézi táblája (`f22/versmegfeleltetes_kezi.tsv`, 19 sor) erre épül. Ha a Jób 40 kulcsa megváltozna, az a kézi táblát érvénytelenítené. Ez külön döntés, és az N-F41g-hez tartozik.
- A generátor újrafuttatása más könyvekre, és más könyv adatai.

## Tételek

**F84.1 — Ellenőrzés, olvasás.** Saját lekérdezéssel, proveniencia-sorral:
1. A 332 nyitott sor versenkénti bontása (34 kulcs), és a `STEPBible_elsodleges` → Károli-kulcs leképezése a `Konyv_normalizalo_tabla.tsv`-n át.
2. Tartalmi szúrópróba legalább 5 versen: a nyitott sorok Strong-halmaza ugyanaz, mint a `Macula_heber_Job.tsv` megfelelő MT-versének Strong-halmaza (Károli 41:1–8 = MT 40:25–32, Károli 41:9–34 = MT 41:1–26). Ellenőrizd, hogy a Károli 41:n szövege tartalmilag illik-e.
3. Az oszlopszerkezet megfeleltetése: a nyitott fájl 10 oszlopa és a fő kivonat 7 oszlopa (`Igehely` + 6 adatoszlop).
4. Van-e a nyitott esetek között más Jób-sor (40. fejezet). Ha van, csak jelentésbe kerül, nem nyúlsz hozzá.

**⛔ 1 — Megállás a táblaírás előtt.** Jelentés: `naplok/F84_jelentes.md`. A felhasználó dönt:
- (a) a nyitott sorok törlődnek a nyitott fájlból, vagy (b) ott maradnak `ATVEVE_F84` státusszal;
- a Jób 41:25 kérdése: a felülbírálás indoklása szerint egy korábbi audit „összeolvadt versnek” jelölte. Ha a szúrópróba itt eltérést mutat, a verset kihagyod, vagy `javaslat` jelöléssel külön kezeled.

**F84.2 — Pótlás.** Szkript: `eszkozok/tahot_job41_potlas.py`.
- Olvasás `split('\t')`, írás `'\t'.join()`, `csv` modul nélkül.
- A fő kivonatba a „Jób 40:…” utolsó sora után és a „Jób 42:1” elé kerülnek, versen belül az eredeti szósorrendben.
- Írás előtt összeveti az eredetivel: a fő kivonat minden meglévő sora bájtazonos marad, csak a beszúrt sorok újak. A beszúrt sorok száma egyezik a nyitott sorokéval, a ⛔ 1 kihagyásait leszámítva. Bármilyen eltérésnél leáll.
- Utána `eszkozok/tahot_lefedettseg_ellenoriz.py`, és a `lekerdez.py scan H3882 --szakasz "Jób 41:1-41:34"` legyen nem üres (leviátán).

**F84.3 — A generátor és a dokumentáció.**
- `tahot_karoli_kulcs_generalas.py`: a `("Job", (40, 41))` felülbírálás indoklásához a mért Károli-szám (40 = 19, 41 = 34) és az F84 hivatkozása kerül. Hogy a döntés-érték változzon-e, az a végrehajtó [javaslat]-a, mert a generátor a repóból nem futtatható.
- `CLAUDE.md`: a „`TAHOT_kivonat.tsv` nem teljes … (hiányzik legalább Jób 40:1–5 és a Jób 41 …)” mondat a mért állapotra javul. A Jób 40:1–5 a #83 szerint nem hiányzik (TAHOT 39:34–38 = MT 40:1–5), a Jób 41 az F84 után megvan. A Jób 40 MT-kulcsú számozása maradó korlátként szerepeljen.
- `konkordancia/TAHOT_TAGNT_README.md`: ha teljességet állít, a mondat a mért állapothoz igazodik.
- `NYITOTT_FELADATOK.md`: N-F83a felvéve és lezárva, helyőrzővel; az N-F34b a CLAUDE.md-javítással lezárul vagy szűkül.

**F84.4 — Zárás.** `naplok/F84_zaras.md`, független ellenőrzés: `naplok/ELLENOR_F84.md`.

## Kapcsolatok

- A #22 a `TAHOT_kivonat.tsv`-t olvassa. A Jób-menet az F84 merge-e után indul, a többi könyvét az F84 nem érinti: a beszúrt sorok csak a Jób 41-et adják hozzá.
- A #41 (BSB) `Számozás` oszlopa a Jób 41-et `kjv`-nek jelölte, mert a TAHOT-ban nem volt. Ezt az F84 nem írja át, a következményt az N-F41g kapja meg megjegyzésként.
