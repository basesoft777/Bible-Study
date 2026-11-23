# F239 átadó — U1b (visszhang 1–2 kinyerése) → U3 (próza) és az integrátor

*2026-11-23 · kinyerő: `claude-sonnet-5-5` · második kéz: `claude-opus-5-5` (subagent) · ág: `claude/nervous-kare-9d2361` (PR #820).*

## Mi készült (a TEREMT-001 sorai)

| tábla | sor | állapot |
|---|---|---|
| `adat/visszhang_megfelelok.tsv` | 88 | 77 ellenőrzött; 11 ellenőrizetlen (alább) |
| `adat/visszhang_tanuk.tsv` | 10 + 1 + 5 (HCF) | 10 Chain Lineage-sor (gépi, ellenőrzött); 1 Glossa-sor (két kéz, az ítélet a `naplok/F239_U1b_glossza_atnezes.tsv`-ben) |
| `adat/vitatott_forrasok.tsv` | 4 | 2 forrás-sor (Tsumura, JAOS 2021: a tehóm–Tiámat pont; Bekken, De Gruyter 2007: a Róm 10:7 pont), 2 hiány-sor (Jel 20:3 ↔ 1Móz 8:2; Tengeri ének ↔ özönvíz); mind átnézve |

A megfelelő-tábla bontása: Targum 8 (Onkelos, a Mózes-könyvek 8 láncverse), Vulgata 44 (35 ÓSZ-vers H8415 + 9 ÚSZ-vers G0012), LXX 35 (30 gépi, 5 modell-kinyert), BDB 1 (a H8415 szócikkében és a Sefaria-gyorsítótárban nincs rokon nyelvi adat: alak nélküli sor; a Tiámat-rokonság a repó szótáraiban nem áll, a próza a vallástörténeti irodalom felvetéseként mondja). A két kéz: a Targum/Vulgata/BDB 53 sorát és az 5 LXX-sort az Opus átnézte (`naplok/F239_U1b_megfelelok_atnezes.tsv`, `…_lxx_atnezes.tsv`; a Péld 8:27 LXX-sor első ítélete `elvet` volt, a megjegyzést javítottuk, újra `jo`).

A munkaanyag és a szkriptek: `naplok/F239_U1b_*` (kinyert, átnézés, `…_kinyeres.py`, `…_cl_spec.tsv`, `…_naplo.md`).

## Amit az U3-nak tudnia kell

1. **(Lezárva, DT-F239e: a lánc az 1Móz 1–8, láncversek 1Móz 1:2, 7:11, 8:2; a `negativ_kriterium` megnevezi: „az 1Móz 1–8 láncára”; a levezetés igazolva.)** *Az eredeti megállapítás: a generátor lánca csak 1Móz 1:2.* Mind a régi (`lexikon_general.lanc_szavak`), mind az új (`lapgen/szamitas/nyelvi_hatter._lanc_szavak`) a lánc-szót a beépített sorok *egyetlen héber Strongú* `gerinc_elem`-éből, a láncverset a motívum Pesat-gerincéből (`lanc_mag`: az első Pesat-sor könyvének fejezet-tartománya) veszi. A TEREMT-001 egyetlen Pesat-sora az 1Móz 1:2, ezért a 9. szakasz ÓSZ-blokkja **egy lánc-szó (H8415) × egy láncvers (1Móz 1:2)**, n/N = 1/1; a G0012 nem lánc-szó (görög). A 35 + 9 versre kinyert sor ezért nagyrészt nem renderel: az ÚSZ-tábla Vulgata-sorai (G0012, 9 vers) igen. Ha a lapnak az egész tehóm-lánc kell (35 vers), az a lánc-szabály (DT-F178g) vagy a `negativ_kriterium` láncot megnevező szövegének (`az 1Móz X–Y láncára`) kérdése: **az integrátor / szerkesztő dönti**, én nem nyúltam hozzá.
2. **A Targum csak az Onkelos** (a generátor a Tórán kívül „nincs Targum-forrás”-t mond; a Jonatan Ézs/Ez/Ámós/Hab/Jón-sorait nem kinyertem). A Zsoltárok, Jób, Példabeszédek Targuma nincs a szabad forrásban.
3. **Az LXX 2Móz 15:5** a tehómot πόντῳ-val adja (a βυθόν a מְצוֹלֹת-é, szórend szerint); az érvnapló A3 „2Móz 15:5 βυθός” mondata ezzel pontosítandó. Az **1Móz 49:25** LXX-sora hiány (a γῆς a „lent heverő mélység” átfogalmazásának része, nem a mélység fordítása; az Opus határesetként jelezte: ha a lap minden helyettesítést megfelelőnek akar, ez a sor γῆς-alakot kapna: tartalmi döntés, nem hoztam).
4. **A Vitatott pontok címe**: a `vitatott_forrasok.tsv` `pont` oszlopa a négy címet az érvnapló szerint hordozza („A tehóm és Tiámat: rokon-e, és ha igen, polémia-e az 1Móz 1:2?”; „A Jelenések bezárása (20:3) visszhangozza-e az 1Móz 8:2 bezárását?”; „A Tengeri ének (2Móz 15:5, 8) tudatosan visszautal-e a genezisi özönvízre?”; „A Róm 10:7 cseréjének forrása”). A generátor a forrásprózában a `**<pont>.**` alakot keresi: az U3 vagy pontosan ezeket a félkövér címeket írja, vagy a tábla `pont` oszlopát igazítja (és a bírálat után a két kéz átnézése változatlan marad, mert a cím nem tartalom).

## Mi maradt üres vagy ellenőrizetlen, és miért

- **(Javítva, F239.15: az eszköz a zsoltár- és Jób 41-számozást átvezeti, mind a 11 sor ellenőrzött.)** *Eredetileg: 11 ellenőrizetlen Vulgata-sor* (Zsolt 33:7, 36:7, 42:8, 71:20, 77:17, 78:15, 104:6, 106:9, 107:26, 135:6; Jób 41:32): a kinyerő táblája a Vulgata saját számozásán (Zsolt −1; Jób 41:23) áll, a `megfelelo_kinyer.versszoveg` pedig a Károli-kulcson keres, ezért a gépi összevetés nem egyezik (a F194-ben ugyanígy). A sorokat az Opus kézzel átnézte (`jo`), de a szabály szerint gépi egyezés nélkül az `ellenorzes` üres. Nem lánc-vers, a lapon nem renderel; a javítás (számozás-leképezés az eszközben) technikai tétel, nem tartalmi.
- **(Javítva, F239.16: a felhasználó engedélyével a HCF-adatbázist használtam; a `D:\pardes_tanu\hcf\commentaries.sqlite` már megvolt, a sha256 egyezik az indexével; licenc: a gyűjtemény közkincs, a jogvédett idézetek fair use alapon, szöveg nem kerül a repóba. 5 saját szavas atyai sor: Jeromos ×4 (Hab 3:10; 1Móz 1:2 és Zsolt 77:17 a Zsolt 76. homíliából; Jón 2:6), Órigenész ×1 (Luk 8:31); két kéz, Opus. A Zsolt 42:8 Jeromos-sora elvetve: a szövegrész csak a Krisztusra vonatkoztatott olvasatot adja.)** Eredetileg: a HCF-szöveget és a Sefaria-szövegeket olvasó modell-sorok nem készültek.** A HistoricalChristianFaith adatbázis (`commentaries.sqlite`, 176 MB) nincs a gépen, a letöltése külön engedélyt kér; a Sefaria-szöveg olvasása helyett a Chain Lineage tényadatát használtam (Eusebius ×3 hely, Gabalai Szeverianosz ×2, Nagy Szent Gergely, Hippolütosz, Oikumeniosz, Mekhilta ×2; hagyományonként helyenként egy). Ezek **együtt-idézések**, a lap a kapcsolatuk értelmezését nem állíthatja (SEMA 2.57). Ha a lapnak saját szavas olvasatú atyai tanú is kell, az HCF-letöltés engedélye és egy külön kör kell hozzá.
- **A vitatott pontok szakirodalma**: a Jel 20:3 és a Tengeri ének pontjánál a független (második kéz) keresés sem talált a kérdésről szóló lektorált forrást: hiány-sor. A keresés naplója `naplok/F239_U1b_naplo.md` (a kinyerő első keresése a Tsumura- és a Bekken-forrást nem hozta elő, a második kéz igen: a naplóban a „hiány-sor” a négy pont első eredménye).
- **A VISSZHANG olvasói kapu** a generált lapon fut; a lap nincs meg (U3), ezért nem futott. A két tábla szerkezeti ellenőrzése zöld: `megfelelo_kinyer.py ellenoriz` (0 hiba), `tanu_kinyer.py ellenoriz` (0 hiba), `szakirodalom_kinyer.py ellenoriz` (0 hiba).

## Az eszközön végzett javítás (a brief határán belül, technikai)

`eszkozok/visszhang/tanu_kinyer.py`: a Chain Lineage a zsoltárokat `ps`-szel jelöli, a normalizáló tábla `psa`-t ismer, ezért a `cl` a zsoltárhelyet nyers `ps 77.17` alakban írta a `tanu_hely`-be; a `karoli_alak` most `ps`-t is ismer (Zsolt).
