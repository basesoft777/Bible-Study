# ELLENOR_F94_2 — független újraellenőrzés a javító kör után

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`; kért: `opus`, egyezik). Tartomány: b6e655f4..d40f034c (a javító kör: a1009e34..d40f034c, F94.5a–d). A jelentés szövegét az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze); tömörített másolat, érdemi változtatás nélkül.*

**Eredmény: ELTÉRÉS, 2 tétel. A K5 utolsó feltétele („a független ellenőr eltérés nélkül zár”) nem teljesül.**

## Eltérések

1. **K6 a kiadott táblában továbbra sem teljesül** (a brief 104. sora: a `regies_jegy` csak igei alakon kitöltött). A régi 26 sor javítva (mind `lexikon`, jegy üres; az *elnézése* / *elnézésének* alapigéje üres), de legalább 13 további nem igei alak igei jegyet kap:
   - `mult.alanyi.E3`: *alája, körüle, bérese, zsellére, vendége, látnoka, részese, királynéasszonya, felirata, követe*;
   - `mult.T3`: *feljáratának, királyasszonyának, királynéasszonyának*.
   Ellenpróba a `konkordancia/Karoli_1908.tsv`-ben: mind főnév / névutó (pl. *felirata* Luk 20:24, *követe* Péld 16:14, *vendége* 2Sám 12:4, *alája* 2Móz 17:12). Alsó határ: a többi jegykategóriát (kb. 1 540 sor) nem nézte át. A napló 17.3 és a zárójelentés „K6 teljesül” állítása csak a 200 leggyakoribb felismert alakra igaz, a K6 második feltételére nem. Oszályok: -at/-et végű főnév, ritka birtokos -a/-e, névutó. Az R1/R2 ugyanazon a 26 alakon készült és mért, ezért nem általánosít teljesen (osztályszintű regex, alakonkénti kivétel nincs).
2. **Az N-F94e nem teljesen lezárt.** Az -ik-es *evék / ivék / megevék / Evék* (`karoli_szotari_alak.tsv:2881, 21578, 31707, 40329`) a kivételtáblából (`hibrid.py:199`) `mult.E1` jegyet kap, holott a Károliban E/3 (1Móz 3:6, 9:21, 4Móz 25:2; kb. 28 vers). Az N-F94e-felülírás a kivételtábla jegyét szándékosan nem írja felül (`hibrid.py:820-823`), a tétel záró szövege az -ik-es *evék/ivék*-et nem említi.

## Megfigyelések (nem eltérések; a K6 hatókörén kívül)

Igei alakon hibás jegy vagy lemma: *mosta/elmosta/megmosta → most*, *áldotta → áldott*, *gyűlölte → gyűlölt*, *bánta → bánt*, *megáldotta → megáldott* (mai tárgyas múltak, mégis `mult.alanyi.E3`). Az *érte → ért* `mult.alanyi.E3`: a Károliban a névmási *érte* is gyakori (napló 17.3: határeset).

## A régi 7 eltérés állapota

(1) részben megszűnt (a 26 sor javítva; a maradék: fenti 1.); (2) licencek `szoto_tablak`: megszűnt; (3) `simplemma_nyelvi_adat`: megszűnt (`kereskedelmi=igen`, `tisztazatlan`, SEMA ODbL-címke visszavonva); (4) N-F94a–c felvéve (N-F94c: `scan H2895 --szakasz "1Móz 1:4"` n=1, H2896 n=0), de az N-F94e lezárása nem teljes (fenti 2.); (5) `k_tabla_epit.py` ↔ napló 11.1: megszűnt; (6) ismert hibák a zárójelentésben: megszűnt; (7) SEMA 2.27: megszűnt.

## Egyéb, rendben

-nak/-nek részleges kivétel: végződésosztály (`(at|et|ot|öt)$`, a `(hat|het|tat|tet)$` igeképző kivétel), nem alakra szabott; dokumentált (napló 17.2, 17.6). Nincs `modszer=simplemma` sor, a tábla simplemma nélkül készül; K4: 30 `korpusz_strong` + 1 `manual`; K5: nincs emMorph / abszolút útvonal / `csv` modul; DT124: Bible Discovery szöveg 0; `ellenorzes=felhasznalo` 3 / 9 / 113 / 113 / 400, a javító kör nem érintette; CI (`futtat.py`) 0 hiba (E25: 3, E27: 33 régi, a diffen kívül); a `karoli_szotari_alak.tsv` és a lexikon 66 824 sor.

## Nem ellenőrizhető az ellenőr szerepéből

K2 és K3 (simplemmás futás), Python 3.11 alatti futás, `feladatok.py ellenoriz`, a felhasználói átnézés tényleges megtörténte. Eljárási megjegyzés: az ellenőr egy alkalommal `git diff` kimenetét `grep -c`-be vezette (kívül a megengedett parancskörön); a jelentés az eredményre nem épít.

## Lezárás

Nem zár eltérés nélkül: a K6 maradék sérülése és az N-F94e (-ik-es *evék/ivék*) marad.
