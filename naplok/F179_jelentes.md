# F179 jelentés — a `general.py` újszövetségi könyvlistája

*Végrehajtó: claude-sonnet-5-5 (a kért modell: `sonnet`). Ág: `claude/usz-konyvlista`. Nem ellenőrzött: az ellenőrzést a `fuggetlen-ellenor` végzi.*

## 1. Felmérés

| Hely | Kézi ÚSZ-lista | Teendő |
|---|---|---|
| `eszkozok/general.py` `UJSZOVETSEGI_TOKENEK` | 12 könyv (1Kor, 1Pét, 1Thessz, 2Pét, 2Tim, ApCsel, Jel, Júd, Luk, Mt, Róm, Zsid); **15 hiányzik**: Mk, Ján, Gal, 2Kor, Ef, Fil, Kol, 2Thessz, 1Tim, Tit, Filem, Jak, 1Ján, 2Ján, 3Ján | cserélve (F179.1) |
| `eszkozok/n14_hamart_betoltes.py` 389. sor | 14 könyv (a fentiek + Gal, Mk); **13 hiányzik** (köztük a Ján; a HAMART-001-ben Ján-sor nincs) | **nem javítva**, l. 4. pont |
| `eszkozok/karoli_strong/pontossag_kulso.py` `USZ_KONYVEK` | teljes 27 (rövidítés-alakok) | nem érintett |
| `eszkozok/karoli_strong/egyesit.py` | a TAGNT-ból számolt | nem érintett |
| `eszkozok/olvaso_mockup/sablon.html` `NT` | mockup, a `Lk`/`Jn` alakokkal | nem érintett (nem a generátor) |

A `konyv_teszamentum()` hívói: `general.py` (indexblokk, ÓSZ/ÚSZ/ÓSZ+ÚSZ), `lexikon_general.py` (az előfordulás-blokk ÓSZ/ÚSZ-száma és olvasói mondata, a szócikk-blokk testamentum-szűrése, az LXX-tábla `osz_sorai` két helyen).

## 2. Javítás

- `general.py`: `UJSZOVETSEGI_TOKENEK = ujszovetsegi_tokenek_betolt()` — a `konkordancia/Konyv_normalizalo_tabla.tsv` `Mat`..`Rev` soraiból (27 könyv, `split('\t')` a repó `tsv_beolvas`-ával); őr: ha a tábla vége nem `Rev`, vagy nem 27 sor van a `Mat` után, a betöltés hibát dob.
- Teszt: `eszkozok/teszt_general_konyvlista.py` (5 teszt, zöld): mind a 27 ÚSZ-rövidítés, a tábla 39 nem-ÚSZ sora ÓSZ, `Gal 3:13` → ÚSZ, számozott/ékezetes tokenek.

## 3. Mérés (lapról lapra)

A módszer: ugyanazon a repón kétszer generáltam a `general.py --cel lexikon` kimenetét repón kívüli `--kimenet` könyvtárba, a mai `lexikon/*_TUDOMANYOS.md` lapok másolatára (a javítás nélküli és a javított `general.py`-val). Az „adat” oszlop az `adat/elofordulasok.tsv` helyes (27 könyves) számolása.

| Lap | adat ÓSZ/ÚSZ | lap mondata ELŐTTE (régi lista) | lap mondata UTÁNA | LXX-sorok előtte | LXX-sorok utána | ebből ÚSZ-sor a LXX-táblában előtte → utána |
|---|---|---|---|---|---|---|
| ALVIL-001 | 64/10 | 64/10 | 64/10 | 64 | 64 | 0 → 0 |
| ANTROP-001 | 1/10 | 1/10 | 1/10 | 1 | 1 | 0 → 0 |
| **HAMART-001** | **43/9** | **46/6** | **43/9** | **67** | **62** | **5 → 0** (Gal 3:10, Gal 3:13, Mk 7:21, 7:22, 7:23) |
| HODIT-001 | 33/0 | — | — | 33 | 33 | 0 → 0 |
| ISTENTISZT-001 | 16/6 | 16/6 | 16/6 | 16 | 16 | 0 → 0 |
| KIRALY-001 | 5/4 | 5/4 | 5/4 | 7 | 7 | 0 → 0 |
| MENNY-001 | 6/3 | 6/3 | 6/3 | 6 | 6 | 0 → 0 |
| TEREMT-001 | 35/7 | 35/7 | 35/7 | 35 | 35 | 0 → 0 |
| TEREMT-002 | 3/0 | — | — | 3 | 3 | 0 → 0 |

Egyetlen lap érintett: a HAMART-001. Mellékhatás ugyanott: a szócikk-blokk UBS-összegzése (G1944 ἐπικατάρατος: „nincs újszövetségi helye” → 2 újszövetségi hely, a Gal 3:10 és 3:13).

**Eltérés a briefhez:** a brief 42/6-ot ír (48 sor, a #639 állapota). A main-beli `adat/elofordulasok.tsv`-ben a HAMART-001-nek 52 sora van, 43 ÓSZ és 9 ÚSZ. A 9 ÚSZ-sor könyvenként: Róm 1, Gal 2, Zsid 1, Jel 2, Mt 1, Mk 1, 2Pét 1; Ján-sor nincs (*proveniencia: scope=adat/elofordulasok.tsv HAMART-001 | forras=split('	') | ts=2026-11-08T12:54Z*). A main-en tehát a helyes szám 43/9. A 42/6 a #639 ágán fog megjelenni, ha az a javított `general.py`-val generál. *(Javítva az F179 ellenőrzése nyomán, ELLENOR_F179 3.: a korábbi „Mk 1, Gal 2, Ján 3, Mt 3” téves volt.)*

## 4. Nyitott pontok

1. **A `lexikon/HAMART-001_TUDOMANYOS.md` NINCS újragenerálva — döntés kell.** A main-beli HAMART-lap régi állapotú (utolsó teljes generálás előtti: az F168.5 óta csak a jelmagyarázat, a kolofon és a 8. blokk frissül „gépi blokkcseréjjel”, mert a teljes újragenerálás E5/E9-hibákat hozna). A javított generátor kimenete a `lxx` és `elofordulasok` blokkban a számokon túl más eltéréseket is hoz (kiejtés-átírás a héber oszlopban, új olvasói mondat, 67 → 62 LXX-sor); a `szocikkek` blokk 146 → 2125 sor. A #639 ága (`claude/sweet-goldwasser-00aa45`), amelyhez nem nyúltam, valószínűleg úgyis újragenerálja a lapot, és ütközne.
   - (A) javaslat: **nem nyúlunk a main-beli HAMART-laphoz;** a javított `general.py` a #639 újragenerálásával hozza a helyes számot (42/6 ott, 43/9 a main-adaton), és a #639 ellenőre ezt méri. A F179 „kész” feltételéből a HAMART-lap 42/6-a ekkor a #639-re tolódik.
   - (B) gépi blokkcsere (F168.5 mintára) a HAMART `lxx` és `elofordulasok` blokkjára, a többi eltérés (kiejtés, olvasói mondat) beemelésével; ütközhet a #639-cel.
   - (C) teljes újragenerálás: nem ajánlott (F168.5 indoklása).
2. **`eszkozok/n14_hamart_betoltes.py`** (389. sor) saját kézi listája 13 újszövetségi könyvet még mindig nem tartalmaz (köztük a Ján-t). Az `ir`-en kívül van, és egyszeri betöltő; nem módosítottam. Hatás a HAMART-001 lapján: nincs, mert a lap mind a 9 ÚSZ-sora (Róm, Gal, Zsid, Jel, Mt, Mk, 2Pét) a betöltő listájában szereplő könyvben áll (*proveniencia: scope=adat/elofordulasok.tsv HAMART-001 | forras=split('	') | ts=2026-11-08T12:54Z*); más motívumra a hatás nem mért. Javaslat: külön tétel (N-F179a), ha a betöltő még fut.
3. A brief 105. sor/2221–2222. sor hivatkozásai elavultak (a mai lapon az előfordulás-táblázat a 91. sor után van, az LXX-blokk a 719. sor körül).

## 5. Ellenőrzések

- `python eszkozok/teszt_general_konyvlista.py`: 5/5 zöld.
- `python eszkozok/general.py --cel lexikon --kimenet <repón kívüli>`: rc=0, a K13/K15 őr („minden könyvnév feloldva”) zöld.
- `python eszkozok/feladatok.py ellenoriz` és az olvasói kapu: l. a PR-leírást / a lezárás alatt.

Kiegészítés az ellenőrzésekhez: a `teszt_general_ellenorzo.py` `test_eles_sema` tesztje (`37 != 23` kulcs) és az `olvasoi_kapu.py --osszes` BUKÁS-ai (pl. PONT 3, PROZA_1A 1) a javítástól független, a main-beli lapokon és a `SEMA.md`-n alapuló állapot; a F179 nem módosított lapot vagy sémát, tehát nem okozta őket. A CI (E28) futását a PR-on kell látni.
