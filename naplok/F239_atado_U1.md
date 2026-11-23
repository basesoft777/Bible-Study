# F239 átadó — U1 (gépi adat-előkészítés) → U2 (határ és érvvázlat)

*2026-11-23 · végrehajtó: `claude-sonnet-5-5` · ág: `claude/nervous-kare-9d2361` (PR #820).*

**Mi kész, mely fájlokban.** Az összesítő: `naplok/F239_U1_TEREMT-001.md` (pontonként a parancs, a számok, az eltérés-lista, a proveniencia-sor). A részletes TSK-k és a bizonyítéklap: `naplok/F239_U1_TEREMT-001_*` és `naplok/BIZONYITEK_TEREMT-001.md`. A lekérdezés-napló: `naplok/F239_lekerdezesek.tsv`.

**Adatváltozás.** Egyetlen: 28 `nyitva` jelölt-blokksor az `adat/jeloltek.tsv`-ben (a teljesség-mérés Károli-szó hálója 27, a szótár-háló 1). A sorok vers-listái: `naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv`. Döntés nincs bennük; az elbírálás az U2 dolga. A `DONTESEK.md`-be, a `nyitott/uj/` alá semmi nem került (nem volt tartalmi döntés).

**Az U2 bemenete.** `F239_U1_TEREMT-001.md` „Átadás az U2-nek” szakasza sorolja a fájlokat. A régi tanulmányból csak célzott szakasz kell.

**Mit NEM kell elolvasni.** A nyers `naplok/F239_U1_TEREMT-001_lekerdezesek.txt`-t (a TSK-k és az összesítő tartalmazzák), a `…_felmeres_kiserok.tsv`-t (251 sor, csak ha a kísérő-szavak kellenek), a `…_igealak.tsv`-t (főnév: nincs igealak-döntés).

**Nem sikerült / kimaradt (okkal).** (1) fordítás-lista: a TEREMT-001 lapja BEFAGYASZTVA, a `glossza_lexikon_forditas.py lista` nem renderel; (2) `visszhang/megfelelo_kinyer.py lxx`: csak írni tud, kihagytam; (3) igeszakasz-blokk: a három érintett genezisi tanulmányban nincs `IGEHELY-BLOKK` jelölő, 0 blokk; (4) `szakasz_cimke_levezet`: 42 jelzés (üres szótár-mezők); (5) az `lxx-hid` ÚSZ-versre nem fut.

**Az U2 kérdései (nem döntöttem).** A 30 eltérés-blokk elbírálása a lexikai negatív kritérium szerint (a mélység-szavak: עָמֹק, מְצוֹלָה, בּוֹר, βάθος, βυθός …); az LXX-többlet (4 ἄβυσσος-vers H8415 nélkül) és a 5 H8415-vers ἄβυσσος nélkül; a Jób 42:8 a szótár-hálóban; a 11 Nave-jelölt; az ALVIL-001 és a TEREMT-002 közös versei (a TEREMT-002 adatához nem nyúlunk); N58 és a régi `scan H8415` alakú forras_kereses-sor a Jób 41:32-n; a `res_forras.tsv` sorai (kivonat → B47).

**Mérés (a brief szerint).** `get_usage` előtte/utána nem futott (nincs ilyen eszközöm ebben a sessionben); a `naplok/F239_meres.md` sort az integrátor / a brief szerinti mérő tölti. Futások: a `lekerdez.py` 64 hívása (54 naplózott proveniencia-sor), 1 `teljesseg_meres`, 1 `motivum_felmeres`, 1 `bizonyiteklap`, 3 `tanulmany_kinyer` (írás nélkül), 1 `motivum_hatar` (repón kívülre), 1 `proza_lefedettseg`, 1 `szakasz_cimke_levezet` (írás nélkül), 1 `glossza_lexikon_forditas lista` (nem renderelt).
