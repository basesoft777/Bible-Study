# F22_USZ_B_jelentes.md — a 22.9 B csomag összesítője (Gal, Ef, Zsid; a 2Kor visszatartva)

*A számok szkriptkimenetből jönnek: a 3 könyvjelentés (`naplok/F22_<könyv>_jelentes.md`), `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py --ellenoriz`, a `f22/api_termeles/futasnaplo.tsv` és a `f22/api_termeles/high/_munka/*.json`. Ág: `claude/f22-usz-b` (a #309 merge-e után a main-ből; a B-commitok átvéve). Módszer: D45 (csak Sonnet, Message Batches API, `effort=high`, `prompt_v3`, 10 verses kötegek, soros futtatás). Indítás: felhasználói utasítás (chat, 2026.10.12: „Gal, Ef, Zsid mehet. A 2Kor-t tartsd vissza …”; a folytatás: „A B csomag folytatódik …”).*

## 1. Könyvenként

| könyv | Károli-vers | modellhez | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körbe került köteg | `[nem TR]` | ebből párosított | régi arany (kizárás nélkül) |
|---|---|---|---|---|---|---|---|---|---|---|
| Gal | 149 | 149 | 17 | 0.6915 | 0.0046 | 11/149 | k002 (versenkénti, 1 vers); k007 (egész köteg: érvénytelen JSON, 10 vers) | 40 | 1 | nincs hármas |
| Ef | 155 | 155 | 18 | 0.7711 | 0.0050 | 11/155 | k003 (versenkénti, 1 vers); k012 (egész köteg: érvénytelen JSON, 10 vers) | 54 | 2 | nincs hármas |
| Zsid | 303 | 303 | 35 | 1.6045 | 0.0053 | 6/303 | k016 (versenkénti, 1 vers); k028 (versenkénti, 1 vers); k030 (versenkénti, 1 vers); k031 (egész köteg: érvénytelen JSON, 3 vers) | 92 | 9 | 75.0% (6/8) |
| **össz** | **607** | **607** | **70** | **3.0671** | **0.0051** | **28/607** | | **186** | **12** | |

Végleges kapuhiba: Gal 3:23 (`kezi`, átnézésre). Az `egyesit.py --konyv <könyv> --ellenoriz` mind a 3-ra „rendben”. A futásnapló minden új sorában `prompt_sha256_12 = 84f12ca7aafb` (a `prompt_v3` változatlan).

## 2. A 48 zárójeles csoport (N-F22c): a jelölés az egyesítés előtt

A felhasználó döntése szerint (chat, 2026.10.12) az egyesítés **előtt** a három könyv verseit összevetettük a 48 csoporttal (`naplok/F22_TAGNT_zarojeles_sorok.md`). Az érintett versek `kezi` bizonyosságúak, `fuggoben` állapotúak, link nélkül (`f22/kezi_versek_<könyv>.tsv`), mert a részleges görög szöveg hamis `betoldas` jelölést adna; mindkét kulcs (NRSV és KJV/egyéb) verse, mert a Károli-kulcs a kivonat javításáig nem dönthető el. A modell ezeket a verseket is megkapta (a minta nem változott), de a válaszuk nem kerül a táblákba.

- Gal: Gal 2:19, Gal 2:20.
- Ef: Ef 1:10, Ef 1:11, Ef 2:14, Ef 2:15, Ef 5:14, Ef 5:13.
- Zsid: Zsid 3:10, Zsid 3:9, Zsid 7:20, Zsid 7:21, Zsid 12:22, Zsid 12:23.

## 3. Költség, keret, újravetítés

- A B (Gal, Ef, Zsid) költsége **3.0671 USD** (0.0051 USD/vers). A futó összeg 94.504948 USD; a 18 USD-s ÚSZ-keretből (86,3698 + 18) **9.86 USD maradt** (a kódbeli plafon 104,36 USD).
- A vetítés módszere: **egyszerű arány** (a mért összköltség osztva a modellhez ment versek számával, szorozva a hátralevő versszámmal), nem illesztés; a könyvenkénti egységár 0,0046 és 0,0053 USD/vers között szór (a 22.8 és az A: 0,0040–0,0066).
- Mért egységár a 22.8, az A és a B együtt: 0.005226 USD/vers (1638 vers).

| hátralevő | vers | vetítés | ×1,2 tartalékkal |
|---|---|---|---|
| 2Kor (visszatartva, a kivonat javításáig) | 256 | 1.34 USD | 1.61 USD |
| C (Róm, 1Kor, Jel) | 1272 | 6.65 USD | 7.98 USD |
| 2Kor + C | 1528 | 7.99 USD | 9.58 USD |

A 2Kor + C ×1,2 tartalékkal (9.58 USD) nem több a maradék 9.86 USD-nél.

## 4. Kapuhiba

Első próbára 28/607 vers (4.6%). Ebből **23 vers egész köteg formátumhibából**, **5 vers versenkénti kapuhibából**. A javító kör után 1 vers maradt kapuhibás (`kezi`, átnézésre): Gal 3:23.

**Hiányzó versek a formátumhibás válaszokban** (a `nyers1` alapján): Gal k007: a válaszból hiányzik Gal 3:20, Gal 3:21, Gal 3:22, Gal 3:23, Gal 3:24, Gal 3:25.

## 5. A `[nem TR]` tokenek: 186, ebből 12 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve). A `fuggoben` állapotú (a 2. pont szerint jelölt versekbe eső) `[nem TR]` token nem számít párosítottnak.

| vers | er | alak | Strong | angol tükör | Károli-szó (partner; a többszavas partner szóközzel) |
|---|---|---|---|---|---|
| Gal 4:30 | 16 | κληρονομήσει | G2816 | will inherit | örököl |
| Ef 3:6 | 15 | Ἰησοῦ | G2424 | Jesus | Jézusban |
| Ef 6:19 | 6 | δοθῇ | G1325 | may be given | adassék |
| Zsid 2:1 | 10 | παραρυῶμεν. | G3901 | we may drift away. | el sodortassunk |
| Zsid 4:2 | 16 | συγκεκερασμένους | G4786 | united with | párosították |
| Zsid 4:7 | 13 | προείρηται, | G4280 | it has been predicted, | előbb mondva volt |
| Zsid 9:14 | 19 | ἡμῶν | G3165 | of us | ti lelkiismereteteket |
| Zsid 10:2 | 16 | κεκαθαρισμένους. | G2511 | cleansed! | megtisztult |
| Zsid 11:12 | 18 | ἡ | G3588 | the | fövény |
| Zsid 13:15 | 8 | παντὸς | G3956 | all [times] | mindenkor |
| Zsid 13:18 | 4 | πειθόμεθα | G3982 | we are assured | vagyunk meggyőződve |
| Zsid 13:21 | 15 | ἡμῖν | G3165 | us | bennetek |

## 6. Régi arany

Hármas csak a Zsid-ben van (8). A mért érték 6/8; a két nem egyező hármasnál a Károli-szó a vers tokenjei közt nem található, mert a régi arany pontosvesszővel fűz össze több kifejezést, és az `f22_elemzes.py` ezt egy kifejezésként keresi (ugyanaz a műtermék, mint az A-ban az 1Thessz 5:23-nál): (a) `Heb.4.12 G4151+G5590 „szívnek; léleknek”` — a `parok_Zsid.tsv` szerint „szívnek” (hu 16) → ψυχῆς G5590, „léleknek” (hu 18) → πνεύματος G4151, a halmaz tehát egyezik; (b) `Heb.7.17 G5010 „rendje szerint; Apa nélkül; anya nélkül; nemzetség nélkül való”` — a régi arany sora négy kifejezést fűz egybe, amelyből három a Zsid 7:3-é (ott külön hármasként is szerepelnek): ez a régi arany adathibája, nem a párosításé. Az `f21p/regi_arany_hibas.tsv`-be felvétele tartalmi döntés, a felhasználóé.

## 7. ⛔ Megállás

- Független ellenőr: `naplok/ELLENOR_F22_USZ_B.md`; draft PR.
- A 2Kor a kivonat javításáig (N-F22c, külön feladat) visszatartva; a C-re nincs jóváhagyás.
