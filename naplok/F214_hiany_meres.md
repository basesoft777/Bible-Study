# F214 — hiánymérés (csak mérés, import nem történt)

*Forrás: BSB `a4a2c0558c26e0281ba4e3f0e5479398459e2183`, `base/display/` (CC0); a 95%-os küszöb és a „TAGNT/TAHOT ⊆ BSB” definíció változatlan (DT6). Mérés: 2026-11-12, scratchpad-szkriptekkel; a kód (`bsb_import.py`) még nem használja a normalizálást, a `BSB_Strongs.tsv` változatlan.*

## 1. 2Sám, Ezsd, Dán — Strong-egyenértékűséggel (TBESH: `a Spelling of` / `a form of` / `in Aramaic of`, 765 szám; a konfliktusos számok kimaradnak)

| Könyv | Előtte | Utána | Maradék eltérő vers | Okkategória (F41-besorolás) |
|---|---|---|---|---|
| 2Sám | 94,96% | **95,40%** | 32 | egyéb 31, címkézés 1 |
| Ezsd | 94,64% | **96,43%** | 10 | egyéb 7, arámi 3 |
| Dán | 89,64% | **97,76%** | 8 | arámi 3, címkézés 3, egyéb 2 |

Mindhárom eléri a 95%-ot. A 2Sám szűk (a szélesebb viszonytípus-készlettel 95,54–95,68%). A 36 bent lévő könyv: 18-nál nő a százalék (legfeljebb +1,2 pont, pl. 1Krón 95,54→96,71), egyik sem esik a küszöb alá, az importált sorok nem változnak.

## 2. Újszövetség — ugyanaz a mérce (teljes TAGNT ⊆ BSB), TBESG-normalizálással

Egyik könyv sem éri el a 95%-ot (a legjobb a 3Ján 92,86%). Nyers → normalizált (a nyers az F16-naplóból):

| Könyv | Mért vers | Normalizált % |
|---|---|---|
| Mt | 1068 | 79.49 |
| Mk | 673 | 62.41 |
| Luk | 1149 | 76.07 |
| Ján | 878 | 75.06 |
| ApCsel | 1002 | 76.35 |
| Róm | 432 | 82.18 |
| 1Kor | 437 | 79.63 |
| 2Kor | 256 | 78.12 |
| Gal | 149 | 77.85 |
| Ef | 155 | 84.52 |
| Fil | 104 | 82.69 |
| Kol | 95 | 78.95 |
| 1Thessz | 89 | 76.40 |
| 2Thessz | 47 | 76.60 |
| 1Tim | 113 | 82.30 |
| 2Tim | 83 | 87.95 |
| Tit | 46 | 80.43 |
| Filem | 25 | 84.00 |
| Zsid | 303 | 81.85 |
| Jak | 108 | 75.00 |
| 1Pét | 105 | 78.10 |
| 2Pét | 61 | 85.25 |
| 1Ján | 105 | 83.81 |
| 2Ján | 13 | 84.62 |
| 3Ján | 14 | 92.86 |
| Júd | 25 | 76.00 |
| Jel | 404 | 71.04 |

Fő ok: a BSB a lefordítatlan szavakat (G2532 kai 161 vers, G3004 157, G1161 124, G846, G3588…) nem címkézi, ez nem számozási egyenértékűség, ezért normalizálással nem pótolható. Tájékoztató (NEM a mérce): csak a TAGNT NA28-címkés sorait véve normalizálással 8 könyv ≥95% (Ef 96,1; 1Tim 97,3; Filem 96,0; 1Pét 95,2; 1Ján 96,2; 2Ján 100; 3Ján 100; Jel 96,0) — ez a mérce megváltoztatása, a felhasználó döntése (DT-F214b).

## 3. A 117 hiányzó első vers

116 feliratos zsoltár 1. verse + Zak 12:1 (a `base/text-only/`-hoz képest hiányzik a `base/display/` JSON-ból; fejezetenként pontosan 1 vers). A `base/text-only/` megvan a szövegük (Strong nélkül). Strong-számos alak van a `base/hebrew-tsv/`-ben (pl. Zsolt 3:1 = a felirat, 13 szó H-számokkal; Zak 12:1: 15 szó), MT-számozással. Ennek licence a repó README licenc-táblázatában NEM szerepel (csak `display`, `concordance`, `index-pd` CC0) — licenc-ellenőrzés kell használat előtt (N-F71b). A hiány kb. 117 vers a ~31 000-ből (0,4%), az OT-ban 116 zsoltár-felirat.

## 4. Összegzés

A BSB **nem lehet teljes (66 könyv)** a mostani mércével: a 3 ószövetségi könyv bekerülhet (39 ÓSZ-könyv), de mind a 27 ÚSZ-könyv küszöb alatt marad. Versszintű hiány is marad (117 első vers, amíg a `hebrew-tsv` licence nincs tisztázva). A felhasználó szabálya szerint („ha hiányoznak könyvek nem kell”) a BSB ekkor kikerül a bibliaválasztóból; az adat a `konkordancia/`-ban marad. A szürkítés a hatókörből törölve. Döntés a felhasználóé: (a) a BSB kimarad a választóból; (b) NA28-szűrt NT-mérce (DT-F214b) — ekkor is csak 8 NT-könyv, tehát a 66 nem jön ki; (c) versszintű hiány mellett maradhat-e.
