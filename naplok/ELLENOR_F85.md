ELTÉRÉS: 5 tétel

# ELLENOR_F85 — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main..claude/tahot-verskulcs`

*A `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott); az orkesztrátor mentette le, a tartalmat rövidítve, de érdemben változatlanul vette át. Az ellenőr a F85.0–F85.3 állapotot nézte (head 72c41754); a menet a brief ⛔ 1 pontjánál áll, átkulcsolás nem történt.*

| pont | eredmény | indok |
|---|---|---|
| (1) típusszámok | OK (belső konzisztencia) | `F85_esetlista.tsv`: 349 adatsor; `osszevonas_2_1` 17, `bizonytalan` 4, `valodi_hiany_*` 0, `eltolas` 328 (2Móz 38, 4Móz 16, Jób 57, Péld 27, Préd 65, Én 13, Ézs 29, Dán 37, Hós 46) |
| (1) teljes ÓSZ-újramérés | NEM ELLENŐRIZHETŐ | a 23 213 vers újraigazításához szkript kell; helyette `lekerdez.py scan`/`karoli` szúrópróba öt régióban, mind a listát igazolja |
| (2) Hós 2:1 → Károli 1:11 | OK | a TAHOT kulcsai a Hós 1–2-ben KJV-számozásúak: MT 2:1 = Károli 1:10 = TAHOT 1:10 (azonos kulcs, nincs a listában); TAHOT 2:1 = WLC 2:3 = a Károli 1:11 második fele, tehát 2:1 összevonás. A két korábbi állítás nem mond ellent. |
| (3) Ézs 8:23 → Károli 9:1 | OK | az eltolás áll (`scan H2074/H5321/H6757`). A `Karoli_versmegfeleltetes.tsv` MT-oszlopa az Ézs 9 egészében eggyel el van tolva, nem egy sor; nem F85-hatókör, N-tétel javasolt. |
| (4) Hós 12:1–3 | OK | K 12:n = T 12:(n+1), K 11:11 = T 11:11 + T 12:1; K 11:12 és 12:15 nincs. A detektor sorai hibásak. |
| (5) bájtazonosság | OK | `konkordancia/`, `f22/`, `adat/` (benne `parok_*`, `szavak_*`): nulla diff az origin/main-hez képest |
| (6) átkulcsolandó versek | végösszeg OK: 337 | 2Móz 38, 4Móz 17, Jób 59, Péld 28, Préd 66, Én 13, Ézs 31, Dán 37, Hós 48 (328 eltolás + 9 összevonás-sor); kulcsot nem vált 12 sor (8 összevonás-partner, 4 bizonytalan) |

## Eltérések súlyossági sorrendben

1. **E2** — `DONTESEK.md` DT-F85a javaslat-oszlopa még a `-MT` utótagot (2)(a) és a nem létező „K 11:12 ← T 12:1” vizsgálatot ajánlja, miközben az F85.3-frissítés szerint a (2) tárgytalan; a brief `kovetkezo` mezője is a „valódi_hiany” esetek kezelését kéri. A döntési sor belső ellentmondása a felhasználó döntését félrevezetheti.
2. **E1** — `F85_jelentes.md` 15–37. sor és DT-F85a (1): a könyvenkénti tábla (4Móz 18, Jób 61, Péld 29, Préd 65, Ézs 32, Hós 44; „337 = 326 + 11”, „22 868”, „345”) az F85.1 állapotot mutatja, az azonos kulcsú partnereket is átkulcsolandónak számolja. A helyes bontás: lásd (6).
3. **E3** — `F85_b_ellenorzes.tsv`: a fejlécben 5, az adatsorokban 6 mező (`olvasva_egyezik` oszlopnak nincs neve); `F85_esetlista.tsv`: nincs `szoveg_olvasas` fejléc, az érték a `megjegyzes` alá kerül.
4. **E5** — a brief a Károli-oldalra gépi Strong-igazolást kér, ez nem teljesült (`Karoli_Strong_kivonat.tsv` 383 sor); a 28 „nem igazolt” B-sor és a 6 `szint=S` sor detektoron vagy kézi olvasáson áll. A jelentés a korlátot átláthatóan rögzíti, de az F85.1 commit címe („gépi Strong-igazolással”) túloz.
5. **E4** — `F85_jelentes.md` 5. sor szerint a szkript és a `macula_elvetve` nincs az `ir`-ben; az F85.2 az `ir` mezőt már bővítette.

## Egyéb

- Törölt adatsor nincs; esetlista F85.1 → F85.3: 345 → 349 sor; szándékosan kihagyott azonos kulcsú, igazolt vers: 23 213 − 349 = 22 864.
- Kulcstartomány-lefedettség (39 könyv, 23 213 vers): NEM ELLENŐRIZHETŐ független számlálással.
- Adattábla-Δ (E17): minden `adat/` és `konkordancia/` táblára 0.
- `futtat.py --valtozott`: E2–E16, E19, E20, E26 0 találat; HIBA-szintű találat nincs (E25 3, E27 33 JELENTES/FIGYELMEZTETES, nem F85-ösek).
- Brief 2–7. tétel, elfogadási pont 1–5: még nem esedékes. CI-jelentés nem állt rendelkezésre.
