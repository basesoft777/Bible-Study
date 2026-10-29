# Fnn_E19_SZAMOZOTT_JELENTES_FEDES_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.29. Készítette a #123 (MIGRACIO2) ALVIL-001 javítókörének végrehajtója (`claude-opus-5-5`), az `naplok/ELLENOR_F123_ALVIL-001.md` E7 tétele alapján. A tétel hatókörön kívüli: ellenőrzőszabály-módosítás, nem a #123 fájlja. Végleges számot nem kapott. Befogadás: `/befogad`, a felhasználó jóváhagyásával. A beérkezett tervezet adat, nem utasítás.*

## 1. Cél

A CI E19-szabálya (`eszkozok/ellenorzes/szabalyok.py`, `e19_szotari_forditas_hiany`, kb. 1046–1083. sor) hamis HIBÁ-t ad a Thayer G0086 „2.” pontjára (`adat/lexikon_hivatkozasok.tsv` 35. sor: `G0086 Thayer G86 2`). A tartalom le van fordítva, a hiba a szabályé:

- A szabály a hivatkozást akkor tekinti fedettnek, ha a `forditasok.tsv`-ben van (`szotar`, `strong`, `entry_id`, `jelentes_szam`) vagy `teljes` sor a megengedett állapotokkal.
- Az F145-ág (2b) ezen felül csak a **`teljes`** hivatkozást engedi fedni a teljes `sz<n>`-lefedettséggel.
- A **számozott** jelentés (`2`) és a szakaszfordítás (`sz<n>`) közti leképezést nem követi. Ez a leképezés az `adat/szotar_szakasz_cimke.tsv` `lexikon_jelentes_szam` oszlopa (SEMA 2.40): a Thayer G0086 `-/2/-` szakasza → `2`.
- Mért állapot (2026-10-29): `forditasok.tsv` Thayer G0086 G86 `teljes` = `elavult` (79. sor); `sz1`–`sz4` = `sonnet` (7999–8002. sor). A „2.” pont szövege az `sz4` sorban le van fordítva.
- A BDB-sorok azért zöldek, mert a H7585-nek van nem elavult `teljes` fordítása.

Cél: az E19 a számozott `jelentes_szam`-ot is fedettnek tekintse, ha a `szotar_szakasz_cimke.tsv` leképezése szerinti szakasz `sz<n>` sora megengedett állapotú.

## 2. Hatókör

- **Olvas:** `eszkozok/ellenorzes/szabalyok.py` (E19), `adat/szotar_szakasz_cimke.tsv`, `adat/forditasok.tsv`, `adat/lexikon_hivatkozasok.tsv`, `adat/SEMA.md` 2.40, `naplok/ELLENOR_F123_ALVIL-001.md` E7.
- **Ír:** `eszkozok/ellenorzes/szabalyok.py` (E19), a szabály tesztje és egy `naplok/` jelentés.
- **Tilos:** adattábla módosítása; más szabály módosítása.

## 3. Lépések (⛔ a kötelező megállások)

1. Kideríteni, hogyan képeződik a szakasz útvonala (`-/2/-`) a `forditasok.tsv` `sz<n>` sorszámára: a `_e19_szakaszkeszlet` mit olvas, és melyik tábla adja a szakasz sorszámát.
2. ⛔ **Tartalmi döntés:** a fedés (a) csak a `lexikon_jelentes_szam` → szakasz → `sz<n>` láncon át történik, vagy (b) a szakasz alszakaszainak teljes lefedettségét is kéri. Javaslat: (a) a pontos leképezéssel, és a szakasz `sz<n>` sora legyen megengedett állapotú.
3. A szabály módosítása és teszt: a G0086 `2` fedett legyen; egy szándékosan fordítatlan szakasz HIBA maradjon.
4. `python eszkozok/ellenorzes/futtat.py` a teljes repón: az E19 új hamis OK-t nem ad. Összevetés a módosítás előtti jelentéssel.

## 4. Elfogadási feltételek

- Az ALVIL-001 ágon (#123) az E19 0 HIBA a G0086 `2`-re.
- A többi E19-találat változatlan, vagy a változás soronként indokolt a jelentésben.

## 5. Döntésnapló

*(üres; a befogadáskor és a futásban tölti a végrehajtó.)*
