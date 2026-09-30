# F08 zárójelentés (FELADATOK #8; ág: `claude/lxx-dontesek`)

**Elkészült:** a 87 függő hely (`naplok/F17_87_hely.tsv`) 86 sort kapott az `adat/lxx_dontesek.tsv`-ben (LD005–LD090; a 4Móz 13:34 a HODIT-001 és a MENNY-001 közös sora); a régi LD001–LD004 változatlan (4 → 90 adatsor). Bizonyosság (F8.5 után): **biztos 61** (mind `eltero_forditas`), **valószínű 9**, **nyitott 8**, **nem_alkalmazhato 8** (`nincs_heber_kulcsszo`). Bemenet: `naplok/F08_bemenet.txt`, szkriptek: `eszkozok/f08/`.

**Módszer:** független forrás csak a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű verse; az FJ1-jelölt Macula-származék. A Macula 38 gépi megfelelőjéből 36 megerősítve, 2 ellentmondó (1Móz 8:21, Mik 6:12 → nyitott); a munkalap-szóra ellentmondó vagy nem illesztett 4Móz 13:34 és 5Móz 2:20 szintén nyitott (F8.5). Minden `gorog_strong` az `LXX_OS` adott pozíciójából jön.

**Sémaeltérés, `ir` listán kívüli módosítás (DT23 (d)):** `bizonyossag` oszlop és `nincs_heber_kulcsszo` típus (SEMA 2.11); `ellenoriz.py` 10. szabálya és a `lexikon_general.py` szűrője (csak `biztos`/régi sor jelenik meg; a 3. blokkon túl a „Rokon szavak” blokkot is érinti — próbagenerálásban változás nélkül). **A PR-cím `[ELLENŐRZŐ]` előtagú legyen (CI E16), mert az ellenőrző is módosult.** Próbagenerálás a repón kívül: 61 lexikonsor függőből eltérő, 26 függő marad; a lexikonoldalak nincsenek újragenerálva.

**Leletek:** Préd 9:10 igehely MT-számozású (Károli 9:12; DT7 (g)); HODIT-001 2Sám 21 / 1Krón 20: a TAHOT H7497, a H7498 csak Macula-állítás; LD010 Macula G0999 = βόθυνος; a G2672 (LD030/LD027) forrása az `LXX_OS`, a `LXX_kivonat`-ban Strong nélküli (az ellenőri 3. pont oka, DT23 (i)); Zsolt 76:3/88:11 `LXX_OS`-igehely rendben; a DT7 (a) nem hat ki.

**Ellenőrzés:** `naplok/ELLENOR_F08.md` (1. kör: 8 eltérés, F8.5-ben kezelve; a 3. pontnál az értéket bizonyítékkal megtartottam, DT23 (i)).

**Nyitott (DONTESEK `DT23`, 🟡, (a)–(j)).**
