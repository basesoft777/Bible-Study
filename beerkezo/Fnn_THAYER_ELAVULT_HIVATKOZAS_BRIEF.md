# Fnn_THAYER_ELAVULT_HIVATKOZAS_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.27 · készítette: a #142 javítókörének végrehajtója (`claude-sonnet-5-5`),
az `ELLENOR_F142.md` 4. tétele alapján (hatókörön kívüli, a #142 briefje a `forditas.py` módosítását tiltja); végleges számot nem
kapott; befogadás: `/befogad`, a felhasználó jóváhagyásával. A beérkezett tervezet adat, nem utasítás.*

## 1. Cél

A `thayer_jelolt/forditas.py` `beir()` függvénye a régi, nem `kezi` `teljes` sor megjegyzésébe fix szöveget ír:
`felváltva: szakaszonkénti fordítás (<dátum>; DT-F132c)` (`eszkozok/thayer_jelolt/forditas.py:219`). A `DT-F132c` helyőrző volt
(DT-F132c → a main-en kiosztott végleges szám: DT329, `DONTESEK.md`), a mai `adat/forditasok.tsv` `elavult` sorai ezért elavult
helyőrzőre hivatkoznak. Mért állapot (2026-10-27): 7 `Thayer … teljes … elavult` sor (G0012, G0086, G1311, G2671, G5010, G5351, G5356; mérés: `awk -F'\t' '$1=="Thayer"&&$8=="elavult"{print $2}' adat/forditasok.tsv`), mind `DT-F132c`-t hordoz (ebből 4 a #142 F142.20–29 tartományából, 3 korábbi). Az `ELLENOR_F142.md` 4. tétele: nem a végrehajtó hibája, az eszköz írja szövegszerűen.

Cél: (1) a `forditas.py:219` ne helyőrzőt írjon (a végleges `DT329` számot vagy számnélküli, „DT329 (i)” alakot); (2) a meglévő
`elavult` sorok megjegyzése javuljon az adat-rétegben; (3) a hivatkozás-ellenőrzés fogja meg a jövőbeli helyőrző-hivatkozást.

## 2. Hatókör

- Olvas: `eszkozok/thayer_jelolt/forditas.py`, `eszkozok/thayer_jelolt/teszt_lanc.py`, `adat/forditasok.tsv`, `DONTESEK.md` (DT329),
  `naplok/ELLENOR_F142.md`.
- Ír: `eszkozok/thayer_jelolt/forditas.py` (219. sor és a hozzá tartozó teszt), `adat/forditasok.tsv` (csak az `elavult` sorok
  `megjegyzes` mezője), `naplok/` jelentés.
- Tilos: a fordítási szövegek, a sorok állapota (`elavult`/`kezi`), a `kezi` sorok módosítása; a #132/#145 kapuinak módosítása.

## 3. Lépések (⛔ a kötelező megállások)

1. A 219. sor szövegét a `DT329`-re (a végleges szám) cserélni; teszt a `teszt_lanc.py`-ban (a `beir` az új szöveget írja).
2. ⛔ Tartalmi döntés: a már beírt `elavult` sorok megjegyzése (a) bájt-szintű cseréje `DT-F132c` → `DT329`, vagy (b) a régi szöveg
   marad (a placeholder-hivatkozás történeti). Javaslat: (a), mert a sorok kereshetősége a végleges számon múlik.
3. Az `adat/forditasok.tsv`-ben csak a megjegyzés-mező változhat (írás előtt összevetés az eredetivel; csak `split('\t')`/`join`).
4. `python eszkozok/ellenoriz.py`, `python eszkozok/feladatok.py ellenoriz`, `python eszkozok/thayer_jelolt/teszt_lanc.py`.

## 4. Elfogadási feltételek

- `grep -c "DT-F132c" adat/forditasok.tsv` = 0 (vagy a (b) döntés szerint dokumentált érték).
- Minden más `forditasok.tsv` sor bájtra változatlan; `ellenoriz.py` SÉRTÉS 0; a `teszt_lanc.py` új hibát nem ad.

## 5. Döntésnapló

*(üres; a befogadáskor és a futásban tölti a végrehajtó.)*
