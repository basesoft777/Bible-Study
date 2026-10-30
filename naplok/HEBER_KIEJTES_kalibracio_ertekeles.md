# Gépi héber kiejtés — a kalibrálás értékelése (N-F131w)

*Értékelés, nem döntés: szabály nem módosult, adat (`adat/`) és lexikonlap nem változott. A javasolt szabálymódosításokról a felhasználó dönt (⛔).*

- **Modell:** `claude-opus-5-5`
- **Bemenet:** a felhasználó kalibrációja a kalibráló oldalról (az orkesztrátor továbbította, 2026-10-30), szó szerint: `naplok/HEBER_KIEJTES_kalibracio_valasztas.txt`. Formátum: vesszővel az elfogadható változatok, `*` a preferált; ha nincs `*`, nincs preferált, és az egyetlen csillag nélküli változat az egyetlen elfogadható.
- **Kulcs:** `naplok/HEBER_KIEJTES_kalibracio_kulcs.json` (melyik betű gépi, javaslat, alternatíva).
- **Gépi kiértékelés:** `naplok/HEBER_KIEJTES_kalibracio_eredmeny.md`. Újrafuttatás:
  ```bash
  python naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --chat "$(cat naplok/HEBER_KIEJTES_kalibracio_valasztas.txt)"
  ```
- **Proveniencia:** `scope=naplok/HEBER_KIEJTES_kalibracio.json + _kulcs.json + a felhasználói választás | forras=naplok/HEBER_KIEJTES_kalibracio_kiertekel.py | ts=2026-10-30`. Az okok szerinti besorolás (3. szakasz) és a szabályjavaslatok (5. szakasz) `manual`: a session soronkénti elemzése.

**Mértékek:**
- **(a) valódi hiba:** a gépi változat nem elfogadható;
- **(b) konvenció-eltérés:** a gépi változat elfogadható, de nem a preferált;
- **elf.:** a gépi változat elfogadható, és a sorban nincs preferált.

## 1. Röviden

- **A gépi változat 25/50 sorban elfogadható** (6 preferált + 18 elfogadható, preferált nélkül + 1 konvenció-eltérés), **25 sorban hibás (a)**.
- **A 25 hiba okai** (egy sorban több ok is lehet; a sorszámok a 3. szakaszban):

  | ok | sor |
  |---|---|
  | ס = s | 9 |
  | sevá | 7 |
  | ketiv/qere (Jahve 3, Jeruzsálem 2) | 5 |
  | ב-előtag kemény | 3 |
  | ח = ch, ahol h volt az elfogadott | 3 |
  | kámec kátán | 2 |
  | cere + jod | 1 |

- **Biztos szabályok (nincs hiba):**
  - a dáges forte kettőzése (6/6 elfogadva);
  - a furtív patah (minden furtív sorban a mássalhangzó elé került a magánhangzó);
  - a kötőszói וּ = ú (2/2);
  - a makkef kezelése (6 sorból egy hiba, az is a ס miatt).
- **Az ס és a שׂ konvenciója:** a felhasználó mind a 9 érintett sorban az **sz**-t fogadta el, s-t sehol.
- **A kámec:** a felhasználó a **kámec gádolt (á)** választotta ott is, ahol a tibériási hagyomány kámec kátánt (o) olvas (3. sor בְּחָזְקָה „becházeká”, 6. sor אָהְָלוֹ „áháló”). A hátef-kámec o maradt (5. sor „sibbolím”).
- **A tetragramma:** mindhárom sorban a **„Jahve”** a preferált (nem a JHVH).
- **A javaslataim minősége:**
  - a javasolt változat **29/50** sorban elfogadható, a gépi pedig **25/50**;
  - a javaslat 11 sorban mentett meg gépi hibát (4, 7, 9, 26, 27, 33, 39, 44, 45, 49, 50);
  - 16 sorban a javaslat nem volt elfogadható, csak egy alternatíva (1, 3, 8, 10, 11, 12, 17, 19, 24, 28–30, 41, 46–48);
  - 5 sorban sem a javaslat, sem az alternatíva nem volt elfogadható, csak a gépi alak (6, 34, 37, 38, 43; ezek főleg kemény begadkefat és kámec gádol).

## 2. Kategóriánként (a minta kategóriái szerint)

A gépi változat pontossága az (a) szerint = elfogadható sorok / n. A javaslat és az alternatívák oszlopai azt mutatják, hány sorban volt az adott változat elfogadható (ebből preferált).

| kategória | n | gépi elfogadható | gépi (a) | javaslat elfogadható (pref.) | alternatíva elfogadható (pref.) | 2. alternatíva elfogadható (pref.) |
|---|---|---|---|---|---|---|
| kámec kátán (gyanú) | 7 | 4 | 3 | 4 (3) | 4 (2) | 1 (0) |
| nem szókezdő sevá | 6 | 1 | 5 | 2 (0) | 3 (0) | 2 (0) |
| furtív patah | 6 | 4 | 2 | 4 (1) | 0 | 2 (0) |
| dáges forte | 6 | 5 | 1 | 5 (2) | 0 | 1 (0) |
| ketiv/qere | 5 | 0 | 5 | 2 (0) | 0 | 3 (3) |
| makkef | 6 | 5 | 1 | 5 (0) | 2 (0) | 0 |
| szókezdő begadkefat dáges nélkül | 7 | 6 | 1 | 3 (0) | 1 (0) | 0 |
| ס és שׂ | 7 | 0 | 7 | 4 (0) | 3 (0) | 0 |
| **összesen** | 50 | **25** | **25** | **29 (6)** | **13 (2)** | **9 (3)** |

A 2. alternatíva csak abban a 24 sorban szerepelt, ahol a gépi változat egyezett a javaslattal.

## 3. A 25 gépi hiba okok szerint

Az ok a gépi és az elfogadott változat összevetéséből következik (manual).

| ok | sorok | a gépi → az elfogadott |
|---|---|---|
| **ס = s** (a mai szabály) | 7, 33, 44, 45, 46, 47, 48, 49, 50 | nistárenú → nisztárnú/nisztárenú; vachamas → vachamasz; hakkesef → hakkeszef … |
| **sevá** | 4, 8, 10, 12, 17, 24, 47 | hojtá → hájetá; bisól → viseól; vekirú → vekireú; kithómót → kitehómót; mizbéach → mizebéach; misseól → missól; kisó → kiszeó |
| **ketiv/qere** | 26, 27 (Jeruzsálem); 28, 29, 30 (tetragramma) | úvírúsálim → úvírúsálajim; jerúsálim → jerúsálajim; JHVH → Jahve (3×) |
| **szókezdő begadkefat, ב-előtag** | 8, 9, 39 | bisól → viseól; besimchá → vesimchá; bismí → vismí |
| **ח = ch** | 11, 46, 48 | nischátá → nishátá; chámás → hámász; chamas → hamasz |
| **kámec kátán** | 3, 4 | bechozká → becházeká*/becházká; hojtá → hájetá* |
| **cere + jod (furtív előtt)** | 19 | réach → réjach |

## 4. A konvenció-kérdések: mit választott a felhasználó

**ס és שׂ.** Mind a 7 ס-sorban, valamint a 7. és a 33. sorban egyetlen elfogadható változatot jelölt, és az mindig az sz-es volt. Az s-es változatot sehol nem fogadta el. Preferáltat nem jelölt, mert az egyetlen elfogadható maga dönt. A mintában nem volt olyan sor, amely csak a שׂ-t tesztelte volna; az eddigi régi kézi lap (B halmaz) ott is sz-t ír.

**Szókezdő begadkefat dáges nélkül** (preferáltat egyik sorban sem jelölt):

| sor | szó | az előtag vagy a tő betűje | elfogadott |
|---|---|---|---|
| 37 | כִשְׁאוֹל | כ-előtag | csak kemény: kisól |
| 38 | כֹהֵן | a tő כ-ja | csak kemény: kóhén |
| 43 | בְרִית | a tő ב-je | csak kemény: berít |
| 31 | בְנֵי | a tő ב-je | mindkettő: vené, bené |
| 36 | וּפֶן | a tő פ-je | mindkettő: úpen, úfen |
| 8 | בִשְׁאוֹל | ב-előtag | csak lágy: viseól |
| 9 | בְשִׁמְךָ | ב-előtag | csak lágy: vesimchá |
| 39 | בִשְׁמִי | ב-előtag | csak lágy: vismí |
| 32, 40, 41, 42 | בְשֵׁם, בִשְׁמוֹ, בְשָׁלֵם, בְצִלּוֹ | ב-előtag | mindkettő |

**A minta:** a tő saját kezdőbetűje kemény maradhat (a szótári alak felismerhető: kóhén, berít), a ב-előtag lágy (v), a כ-előtag kemény. Ez mind a 13 érintett sorra illik. A pontozás szerinti szabály (mindig lágy) a 37., 38. és 43. sorban hibázna, a mai D34-es (mindig kemény) a 8., 9. és 39. sorban.

**ח.** A ch-t 10 sorban fogadta el (pl. chajjím, chattát*, vachamasz, vechámász, chaszdechá; a furtív sorokban -ach). A h-t 3 sorban: 11 nishátá, 46 hámász, 48 hamasz. A H2555 (חָמָס) öt ragozott alakjából három ch-s (33, 44, 45) és kettő h-s (46, 48). A H2555 nem következetes, ezt a felhasználónak kell eldöntenie.

## 5. Javasolt szabálymódosítások (⛔ a felhasználó dönt; még nincs alkalmazva)

| # | szabály ma | javasolt | a mintából | mit javít / kockázat |
|---|---|---|---|---|
| **R1** | ס = s, שׂ = sz | **ס és שׂ = sz** | 9/9 sor egyértelmű | 9 hibát javít; a `kiejtes_kivetelek.tsv` két ס-sora (kissé, hámás) is ennek megfelelően javítandó (adatváltozás, külön lépés) |
| **R2** | a kámec kátán heurisztika (meteg nélküli zárt szótag → o) | **a kámec mindig á**; o csak kifejezett kámec kátán jelre (U+05C7) és hátef-kámecre | 3, 4, 6 (á), 5 (hátef → o); az 1. sorban mindkettő elfogadott | 2 hibát javít, a 6. sor preferáltját megtartja. Kockázat: a kánoni kátán-szavak (כָּל → kol, חָכְמָה → chochmá) á-val jönnének; ha ezeket o-val kéri, kivétellista kell. A makkef-szabály (makkef előtti zárt szótag → o) a mintában nem fordult elő; R2 mellett kérdéses, hogy maradjon-e. |
| **R3** | a sevá torokhang előtt a szótagszabály szerint (sokszor néma) | **sevá kiejtett, ha utána torokhang (א, ה, ע) következik** | 8, 10, 12, 47 (4/4) | 4 hibát javít. Ellenpélda: 24 (מִשְּׁאוֹל → missól, ott a kettőzött betű alatt a felhasználó némának vette) |
| **R4** | sevá hosszú magánhangzó után: meteg szerint | **kiejtett** (`hangzo`) | 2, 3, 4 (preferált); az 1. sorban a néma a preferált | 1 hibát javít (4.). Az 1. és a 2. sor ellentmond egymásnak (hárfáím* / vehárefáím*); mindkét szabállyal marad egy elfogadható, de nem preferált sor |
| **R5** | szókezdő begadkefat dáges nélkül mindig kemény (D34) | **a tő kezdőbetűje kemény (a lemma alakja), a ב-előtag lágy (v), a כ-előtag kemény** | 13/13 sor (4. szakasz) | 3 hibát javít; a pontozás szerinti változattal szemben a 37., 38. és 43. sort is megtartja |
| **R6** | tetragramma → JHVH | **→ Jahve** (az Adonáj JHVH-ban is) | 28, 29, 30 (3/3 preferált) | 3 hibát javít; a lapokon ma JHVH áll (DT426 és a régi kézi lap konvenciója), ezt is érinti |
| **R7** | Jeruzsálem: a pontozás szerint (jerúsálim) | **kivétel: jerúsálajim** (minden előtaggal) | 26, 27 | 2 hibát javít; kivétellista-sor (adatváltozás, külön lépés) |
| **R8** | ח = ch | **ch marad**; a H2555 (és a 11. sor H7843) h-ja a felhasználó döntése | ch: 10 sor; h: 3 sor | a H2555-nél a minta megosztott (3 ch, 2 h) |
| **R9** | cere + mater jod → é | (nincs javaslat; 1 eset: 19 רֵיחַ → réjach) | 1 sor | egyetlen eset, ezért nem javaslok szabályt; ha a felhasználó általánosnak tartja (a furtív előtti „éj”), szabály lehet |

**Egyéb megfigyelések (nincs javasolt szabály):**
- **17. sor (מִזְבֵּחַ → mizebéach):** a felhasználó a zajin alatti sevát kiejtette, holott torokhang nem követi; R3 nem fedi.
- **24. sor (מִשְּׁאוֹל → missól):** a kettőzött betű alatti sevát nem ejtette ki; ez ellentmond a mai szabálynak és R3-nak is.
- **41. sor:** a „vesalém” (rövid a) elfogadott, a „vesálém” nem; ez az egyetlen hosszúság-eltérés a mintában.
- **35. sor:** az „ap” és az „af” is elfogadott (אַף, szóvégi פ dáges nélkül).

**Ha R1–R7 mind bekerül,** a mintán a becsült gépi elfogadhatóság 25/50-ről kb. 45/50-re nő. Ez kézi becslés a fenti sorlistákból, nem futtatás: a szabályok nincsenek alkalmazva. A maradék a 17., 19. és 24. sor, valamint a H2555 ח-kérdése (46., 48. és 11. sor). A becslés a kalibráló mintán készült, ezért optimista. Bekötés előtt egy friss, a mostanitól független minta kell (más seed vagy más versek).
