# F117.3 — a javító bemenet, a modul és a tábla újragenerálása

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` · végrehajtó: claude-opus-5-5 · 2026-10-18*

proveniencia: scope=konkordancia/Karoli_versmegfeleltetes.tsv (teljes ÓSZ) | forras=naplok/KAROLI_KK4_tabla_veglegesit.py + eszkozok/versmegf_javitas.py + konkordancia/Karoli_versmegfeleltetes_javitas.tsv | ellenőrzés=naplok/F117_sor_osszevetes.py | ts=2026-10-18

## 1. Bemenet és szabály

- **Javító bemenet:** `konkordancia/Karoli_versmegfeleltetes_javitas.tsv`, 346 sor. Összeállította a `naplok/F117_javitas_bemenet_general.py` a kézi ítéletből (`naplok/F117_itelet.tsv`), az MT-levezetésből (`naplok/F117_mt_levezetes.tsv`) és a DT-F117a–e döntésekből.
- **Osztályok** (DT-F117e (c)):

  | Osztály | Sor | Mikor | `igehely_mt` |
  |---|---|---|---|
  | `KJV` | 104 | Károli = KJV = MT | üres |
  | `MT` | 68 | Károli = MT ≠ KJV | a Károli-szám |
  | `KEZI` | 174 | Károli ≠ KJV és ≠ MT | **kitöltött** (új kombináció) |

  Mindegyik sor `forras=szoveg_osszevetes_f117`.
- **Alkalmazó modul:** `eszkozok/versmegf_javitas.py`. A KK4 az F91 után importálja.
  - Felülír és pótol, az `igehely_karoli` szerinti rendezéssel.
  - A fejlécbe „# F117 javítás” jegyzetsort tesz; ez a javítást és a `KEZI` + `igehely_mt` kombinációt is kimondja.
  - Halmaz-őr: a bemeneten kívüli sor nem változhat, sor nem törlődhet.
  - Ellenőrzi a bemenetet is: oszlopszám, `forras`, osztály-szabály, `;`-os KJV-érték tilalma.

## 2. Írás előtti sor-összevetés (a mai tábla ↔ a KK4 új kimenete)

| Osztály | Változott | Hozzáadott | Törölt | Változatlan |
|---|---|---|---|---|
| A | 0 | 261 | 0 | 0 |
| C | 0 | 3 | 0 | 0 |
| B | 8 | 0 | 0 | 0 |
| D | 67 | 0 | 0 | 0 |
| D′ | 7 | 0 | 0 | 0 |
| az A–D′-n kívül | **0** | **0** | **0** | 22 849 |

- **Fejléc:** egy új sor (`# F117 javítás …`).
- **Méret:** a tábla 22 931 → **23 195** adatsor. A 346 célvers mindegyikének van sora.
- **HALMAZ-ŐR:** az A–D′ halmazon kívül 0 változás.

## 3. E1 — determinizmus

| Futás | sha256 |
|---|---|
| KK4, 1. száraz futás (repón kívül) | `6890db3cc8bb407d296159fb4705bd6bf6e480dfefe7369e5d7b3c4e079dbb58` |
| KK4, 2. száraz futás (repón kívül) | `6890db3cc8bb407d296159fb4705bd6bf6e480dfefe7369e5d7b3c4e079dbb58` |
| KK4, éles (`konkordancia/Karoli_versmegfeleltetes.tsv`) | `6890db3cc8bb407d296159fb4705bd6bf6e480dfefe7369e5d7b3c4e079dbb58` |

A két száraz futás bájtra azonos (`cmp`), és az éles tábla azonos velük. A javítás előtti tábla hash-e: `edd6b457…b562` (`naplok/F117_tabla_allapot.md`).

## 4. Tesztek

- **`eszkozok/teszt_versmegf_javitas.py`:** 16 teszt, mind zöld. Lefedi:
  - a felülírást, a pótlást, a rendezést, az idempotenciát, a rendezetlen tábla megállítását és a hibás bemenet elutasítását (3 eset);
  - a generált táblán:
    - pótolt fejezet: Hós 14;
    - KEZI-pár: Préd 9:21, Jób 39:34;
    - Dán 3:31;
    - D-eltolás: Jón 2:3, Ézs 3:1;
    - D′-szomszéd: 1Kir 22:45, valamint a 2-1 pár (1Kir 22:43–44);
    - változatlan sor: 1Móz 1:1;
    - KEZI + `igehely_mt`: Hós 2:1;
  - hogy a teljes bemenet a táblában van, az idempotenciát a táblán és a fejléc-jegyzetet.
- **`eszkozok/teszt_render_diff_osztalyoz.py`:** 74 teszt, zöld.
- **`eszkozok/teszt_sqlite_epit.py`:** 70 tesztből 1 bukik: `Pozitiv.test_mai_adat_zold` (`13 != 12` jelentéssor).
  - A 13. sor a „15. kapcsolatok.tsv fejléc (SEMA 2.3)” szabály, amely az alapcommiton (89b30c2e, `eszkozok/ellenoriz.py:750`; a #11 F11.S2 munkája) már megvan.
  - Az ág nem módosította az `eszkozok/ellenoriz.py`-t, a `sqlite_epit.py`-t, a tesztet és az `adat/`-ot. A bukás tehát a main-en is fennáll, nem F117-hatás.
  - Sértés nincs (0).
- **`eszkozok/teszt_tsk_kulcs.py`:** 14 tesztből 6 bukik. Ez a javítás várt következménye; a brief szerint a 4.5 (F117.4) írja át ezeket:
  - `test_1kir_22_kivetel_nincs_par`, `test_kivetel_fejezetek_nincs_par`, `test_kjv_vers_karoli_par_nelkul` (Hós 2:23), `test_mt_tartalek_negativ` (Hós 14:2) és `test_karoli_sorok` (Hós 2:23 → 2:22): a régi „nincs pár” állapotot rögzítik.
  - `test_egy_a_tobbhoz`: a táblát kölcsönösen egyértelműnek feltételezi. A DT-F117c (3) (a) ezt szándékosan feloldja: a KJV 1Kir 22:43 és az 1Sám 20:42 két-két Károli-versre mutat.

## 5. Váratlan leletek és feljegyzések

1. **Öt további tábla-lyuk az A–D′ halmazon kívül.** A Préd 9:1–2 és a Jób 39:1–3 Károli-versnek nincs sora a táblában. A szöveg-összevetés szerint ezek a KJV Préd 8:16–17 és Jób 38:39–41 versei (`naplok/F117_szoveg_osszevetes.tsv`, kontextus-sorok). A célfejezetek többi 132 kontextusverse egyezik a táblával. A halmazon kívül ezeket nem pótoltam; új tételt kell nyitni róluk.
2. **Az Ézs 64:1 MT-értéke számra egyezik a KJV-párral** (64:1, `KJV` osztály). Tartalmilag azonban a Károli 64:1 = MT 63:19b + 64:1 = KJV 64:1–2. Ez a versfél-korlát esete (N-F117c).
3. **A 4.6-ban kifejezetten ellenőrizni kell**, hogyan kezelik a fogyasztók a `KEZI` + kitöltött `igehely_mt` kombinációt: `f17/macula_kk.py`, `fj2/bsb_import.py` (MT-maximum, „a KJV-osztály soraiból nem”), `sqlite_epit.py` (`mt_kk`), `olvaso_pilot/bdb_szelet_m0.py`, `olvaso_szerver/bdb_vers_jelentes.py`, `lexikon_general.py`.
4. **Egyeztetett eltérés:** a `konkordancia/README.md` írása a brief `ir` mezőjén kívül esik; a felhasználó kérése (DT-F117e). Az `adat/SEMA.md` nem változott.
