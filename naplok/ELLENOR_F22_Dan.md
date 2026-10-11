# ELLENOR_F22_Dan — F22_KAROLI_STRONG_BRIEF.md (D33, v2.27), `fb31802e..55c3db96`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-dan`; commitok: `c3623ed6`, `b5ecd858`, `55c3db96`.*

ELTÉRÉS: 1 tétel

## Igazolt (saját lekérdezéssel)

- **357/357 vers, 12 fejezet:** a `Karoli_1908.tsv` `^Dán ` sorai 357, a `1:1` sorok 12; a `minta_Dan.tsv` 357 adatsor.
- **parok_Dan 9 499:** 9 501 sor = 1 proveniencia + 1 fejléc + 9 499 adat; mind `alacsony / S`, a Strong mindenhol H-szám.
- **szavak_Dan 18 377:** hu 8 848 (7 357 `parositva`, 1 491 `betoldas`), er 9 529 (8 766 `parositva`, 763 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^Dán ` sorai; minden versnek van hu 1 és er 1 sora (357/357); `kezi` / `fuggoben` / `magas` 0 adatsorban.
- **Kapuhiba 7/357 → 0:** a k13 1, k12 4, k21 1, k8 1 vers (összesen 7); a javító kör 4 sora mind 0 / `igen`; a `_munka` fájlok megvannak.
- **Költség:** 1. kör 2,570994, 2. kör 0,109589, összesen 2,680583 USD; tokenek 431 629 / 427 873 és 60 414 / 9 835 (kézzel összeadva); kumulatív 76,640828 USD, a 40 `futo_osszeg_usd` érték szigorúan monoton, a 73,960245-ről indul. Plafon 3,96; versenként 0,0075.
- **Batchek:** 36 + 4 kérés, 14:06:28Z és 14:10:51Z. **10 verses kötegek:** 35 × 10 + 7.
- **Versbeosztás:** a `versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv`, `versosszevonas.tsv` fájlokban 0 Dán-sor; a jóváhagyási naplósor a diffben.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere, a 4 parok-sor jelentéslistájában a Dán), `adat/SEMA.md` 2.20; az 1Kir/Neh/2Kir megmaradt, duplázás nincs. **`tokenek.py`:** `…, '1Kir', 'Neh', '2Kir', 'Dán')`.
- **Jóváhagyás időrendje:** a jóváhagyó commit (14:06:09Z) 19 másodperccel az 1. batch (14:06:28Z) előtt készült.
- **A 16 kis könyv:** a `parok_*.tsv` 23 fájl, a 16 könyvé nincs köztük; versszámuk összege 1 625.
- **Szúrópróba (lekerdez.py scan):** H3079 (Dán 1:1), H4430 és H5648 (Dán 3:1): n=1 mind. **Arámi rész:** az `adat/morf_nyelv_aramai.tsv` szerint Dán 2:4b–7:28.
- **Kulcs-grep:** üres. **CI-eszköz:** exit 0; E2–E16, E19, E20, E26: 0; E25: 3 és E27: 32, repószintű, nem e diffből; E12–E15: 0.

## ELTÉRÉS

1. **A 16 kis könyv „a detektor szerint mind tiszta” állítása pontatlan:** a `f22/versosszevonas.tsv` 12–14. sora három jóváhagyott 2:1 beolvasztást rögzít (Hós 1:11 = TAHOT 2:1, Hós 11:11 = TAHOT 12:1, Préd 2:26 = TAHOT 2:25), amelyek a korábbi könyvekben kézi átnézési pontot adtak; az állítás a jelentés „tiszta jelöltek elfogytak” mondatával is ellentmondott. **Javítva** a briefben és a jelentésben.

## Nem ellenőrizhető a szerepkörből

A detektor 2026.10.11-i újrafuttatása (ideiglenes könyvtárba futott, nyoma nincs), a BDB-mérés 1644 / 312 értéke, a K1 hu-oldala és a K7 újraépítés (`egyesit.py`, a fő session futása: „rendben”), a chatben adott jóváhagyás („mehet a Dániel”), a CI-jelentés részletei (az E27 maradék 29 tétele csonkolt).

## Megfigyelés (nem eltérés)

A Dán 3:1 linkjei közt az „arany” (hu 5) a H1768 (er 6) tokenhez is kapcsolódik, nem csak a H1722-höz; modell-kimenet, `alacsony`.
