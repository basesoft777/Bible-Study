# F22_C_elokeszites.md — a 22.9 C csomag (Róm, 1Kor, Jel) előkészítése (futtatás nélkül)

*Proveniencia: scope=Róm, 1Kor, Jel (Károli 1908, TAGNT-kivonat), valamint az ÚSZ minden könyve a tokenszintű vizsgálatban | forras=`konkordancia/Karoli_1908.tsv`, `konkordancia/TAGNT_kivonat.tsv`, `eszkozok/karoli_strong/tokenszint_vershatar.py`, `versbeosztas.py`, `sonnet_koteg.py minta` (szkriptkimenetek) | ts=2026-10-19. Ág: `claude/f22-2kor` (a #433 merge-e után a main-ből újraindítva). API-hívás és költség nem volt; a C nem indult.*

## 1. Kulcstáblázat a versbeosztás-jóváhagyáshoz (⛔: a felhasználó közvetlen ellenőrzése)

| könyv | Károli-vers | TAGNT-vers | fejezet | versszám-eltérő fejezet | Károli-szó | eredeti token | ebből `[nem TR]` |
|---|---|---|---|---|---|---|---|
| Róm | 431 | 433 | 16 | 3 (30/31), 8 (38/39) | 7 489 | 7 261 | 107 |
| 1Kor | 436 | 437 | 16 | 3 (22/23) | 7 287 | 6 986 | 180 |
| Jel | 405 | 405 | 22 | – | 9 744 | 10 185 | 641 |
| **össz** | **1 272** | **1 275** | | | **24 520** | **24 432** | **928** |

A többi fejezetben a Károli- és a TAGNT-versszám azonos. A három többlet TAGNT-vers (Róm 3:31, Róm 8:39, 1Kor 3:23) a Károli két versét vonja egybe (2:1 beolvasztás); a Róm 16:25–27 és a Jel 12:18 görög szövege az F90 óta megvan. A Jel `[nem TR]` aránya kiugró (641 / 10 185 = 6,3%): a `nem_tr_lista.py` jelölése itt a legtöbb sort érinti.

## 2. A három Károli-összevonás: javasolt `f22/versosszevonas.tsv`-sorok (⛔ jóváhagyásra, nem kerültek be)

A Hós 11:11 és az Ézs 9 mintájára (DT92): a Károli-vers második mondatának tokenjei (`hu_tol`–`hu_ig`) és a beolvasztott TAGNT-vers tokenjei (`er_tol`–`er_ig`, a saját versük szavai után folytatott sorszámmal) `kezi` állapotban, link nélkül.

| karoli | hu_tol | hu_ig | eredeti | er_tol | er_ig | indok |
|---|---|---|---|---|---|---|
| Róm 3:30 | 16 | 31 | Róm 3:31 | 15 | 25 | a Károli 3:30 „A törvényt tehát hiábavalóvá tesszük a hit által? Távol legyen. Sőt inkább a törvényt megerősítjük” (16–31. szó) = a TAGNT 3:31 (11 token: „νόμον οὖν καταργοῦμεν …”) |
| Róm 8:38 | 20 | 41 | Róm 8:39 | 18 | 40 | a Károli 8:38 „Sem magasság, sem mélység … Krisztusban” (20–41. szó) = a TAGNT 8:39 (23 token: „οὔτε ὕψωμα …”) |
| 1Kor 3:22 | 20 | 25 | 1Kor 3:23 | 20 | 25 | a Károli 3:22 „Ti pedig Krisztusé, Krisztus pedig Istené” (20–25. szó) = a TAGNT 3:23 (6 token: „ὑμεῖς δὲ Χριστοῦ …”) |

A tokenhatárok a `tokenek.tokenizal`-lal számoltak; a sorok beírása és a `VERSBEOSZTAS_JOVAHAGYOTT` bővítése csak a felhasználó jóváhagyása után történhet.

## 3. Tokenszintű vershatár-vizsgálat (N-F22e)

Eszköz: `eszkozok/karoli_strong/tokenszint_vershatar.py` (új; jelölt-lista a szomszédos versek Károli/eredeti hossz-többletének ellentétes előjeléből; a jelölteket szemrevételezés dönti el, a hiányzó jelzés nem bizonyíték).

**A C három könyvében nincs megerősített eltérés:** a Jel és az 1Kor-ban 0 jelölt (alap és lazább küszöb is); a Róm egyetlen jelöltje (Róm 4:16–17: Károli 27/32, eredeti 33/23 szó) **téves jelzés**: a Károli 4:16 vége „a ki mindnyájunknak atyánk” = az eredeti 4:16 vége („ὅς ἐστιν πατὴρ πάντων ἡμῶν”), a 4:17 mindkét oldalon „καθὼς γέγραπται” / „(A mint meg van írva …” kezdetű; a hosszkülönbség fordítási bővülés.

**Hitelesítés és a már mergelt könyvek:** az eszköz megtalálta az ismert 2Kor 8:13–14-et, és **négy további valódi eltérést** a már lefutott/mergelt könyvekben (szövegen igazolva):

| hely | mi a Károli-vers határa | állapot |
|---|---|---|
| 2Kor 2:12–13 | a Károli 2:12 vége („nem volt lelkemnek nyugodalma … Titust, az én atyámfiát”) = az eredeti 2:13 1–11. tokenje | mergelve, javítatlan |
| 2Kor 5:14–15 | a Károli 5:15 eleje („Úgy vélekedvén, hogy ha egy meghalt mindenkiért, tehát mindazok meghaltak”) = az eredeti 5:14 vége (κρίναντας … ἀπέθανον) | mergelve, javítatlan |
| 2Kor 8:13–14 | a Károli 8:13 vége = az eredeti 8:14 eleje | `kezi` kényszerben (F22.24) |
| Zsid 1:1–2 | a Károli 1:1 vége („ez utolsó időkben szólott nékünk Fia által”) = az eredeti 1:2 1–7. tokenje | mergelve, javítatlan |
| Fil 3:13–14 | a Károli 3:14 eleje („De egyet cselekszem, azokat … nékik dőlvén,”) = az eredeti 3:13 vége („ἓν δέ … ἐπεκτεινόμενος”) | mergelve, javítatlan (lazább küszöb) |
| ApCsel 13:32–33, 24:2–3 | (még nem párosított könyv) | az ApCsel külön keretdöntés |

Következmény: ezekben a versekben a vershatáron átnyúló szavak téves `betoldas` / `forditatlan` jelölést kaptak (mint az első 2Kor 8:13–14-nél: 9 + 11 token). Javaslat (a felhasználó döntésére): ugyanaz a kezelés, mint a 2Kor 8:13–14-nél (`f22/kezi_versek_<könyv>.tsv`, link nélkül, N-F22e), a 2Kor (2:12–13, 5:14–15), a Zsid (1:1–2) és a Fil (3:13–14) 8 versére, API nélkül; hosszabb távon a tokenszintű vershatár-megfeleltetés (N-F22e). A lazább küszöbön a Ján 1:39–40, 1:42–43, 1:48–49 is jelölt (kis eltérés, még nem párosított könyv, nem vizsgált).

## 4. Minta és költség (száraz próba, API nélkül)

`sonnet_koteg.py minta`: `f22/minta_Rom.tsv` (431 vers, **44 köteg**), `f22/minta_1Kor.tsv` (436 vers, **44 köteg**), `f22/minta_Jel.tsv` (405 vers, **41 köteg**); összesen 1 272 vers, 129 kérés. A minta a jelenlegi (jóváhagyatlan) versbeosztás szerint épült: a három összevonásban a Károli-vers második mondata a jóváhagyásig még nincs a `versosszevonas.tsv`-ben, ezért a jóváhagyás után a három minta-sort újra kell építeni.

A költség: mért egységár 0,005238 USD/vers → 6,66 USD, ×1,2 tartalékkal 7,995 USD; a maradék 8,306 USD (futó összeg 96,0540 USD, plafon 104,36 USD). Az `api_koteg.bekuld` felső becslése (0,16 USD/kérés): Róm 44 kérés ≈ 7,0 USD, 1Kor ≈ 7,0 USD, Jel ≈ 6,5 USD; a Róm után az 1Kor beküldését az őr a plafon fölöttinek venné, noha a tényleges költség belefér (**DT-F22h**, a javaslat: a vagy b).

## 5. Mire vár a felhasználó (a C indítása előtt)

1. A kulcstáblázat (1.) jóváhagyása: Róm, 1Kor, Jel.
2. A három `versosszevonas.tsv`-sor (2.) jóváhagyása.
3. A DT-F22h eldöntése (a plafon-őr kezelése).
4. A tokenszintű eltérések kezelése a már mergelt könyvekben (3.): `kezi` a 8 versre, vagy külön tétel.
