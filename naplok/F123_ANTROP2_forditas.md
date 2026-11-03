# F123 ANTROP-001 — a lap fordítatlan Thayer-szócikkeinek fordítása (DT-F123l)

*2026-11-03 · ág: `claude/confident-brahmagupta-93518c` · a felhasználó döntése: „ezeket a szócikkaket atljeséghez forditsuk most előfizetői keretből”; „de ugyanazzal a promptal és szabályokkal mint a batch api-t”; „csak azokat vinném most amit most a lexikon cikkek legenerálása érint. csak azik a szócikkek menjenek most / mérni nem kell”. A végrehajtás módja: az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket és hozza is meg« (2026-11-03).*

## Hatókör (a lap mérése)

A lap hat szavának Thayer- és BDB-szakaszai közül fordítatlan volt: **Thayer G4152 πνευματικός (7 szakasz)** és **Thayer G5591 ψυχικός (4 szakasz)**. A Thayer G4151 (17), G5590 (10), a BDB H2416 (30) és H5315 (43) minden szakaszának van érvényes `sz<n>` fordítása. A lapon egy BDB H2416-blokk ennek ellenére angolul, „(fordításra vár)” jelöléssel áll: generátor-hiba (a 1Móz 2:7 BDB-példájának útvonala), fordítással nem javítható (N-F123f). A „Megfelelők” táblák TBESG-glosszái nem Thayer/BDB-szakaszok, nem tartoznak a hatókörbe.

## Menet

1. `eszkozok/thayer_api_koteg.py --adag 9001 --cimke antrop1 --strongok … --munka <scratchpad> szaraz`: 2 Strong, 2 kérés (egycsoportos), G4152-c1-p1 (34 474 kar.), G5591-c1-p1 (25 704 kar.); a `bekuld` params-a (modell claude-sonnet-5-5, effort high, thinking adaptive, egy user-üzenet) bájtra kiírva, hálózat nélkül. Az `--adag` csak egész számot fogad, ezért 9001 + `antrop1` címke.
2. Futtatás: `general-purpose` subagent `model: sonnet`, a prompt a kérés user-szövege szó szerint, semmi más (a `vegrehajto-sonnet` a saját modell-ellenőrzése miatt nem adna nyers választ). Gépi összevetés a subagent-átirattal: a kérés bájtra egyezik, a záró sortörés kivételével. Eltérés a batch-től: a Claude Code alap rendszerutasítása, effort és max_tokens nem állítható. A válaszokat a subagentek maguk írták fájlba; tényleges modell: claude-sonnet-5-5.
3. `kapuz` (1. próba): mindkettő javítandó — G4152: `5_terminologia: the Spirit -> a Szellem hianyzik`; G5591: `4_formazas: tobb nyito zarojel (15 / 14)`.
4. `javit`: hálózat nélküli rögzítő hívóval az eszköz egy B-javító kérést állított össze (J001-p2, 44 560 kar.); ugyanígy futtatva (a kérés bájtra egyezik, a záró sortörés kivételével), `b_szetbont` → `kapuz` (2. próba): **mindkettő kész, BUKÁS 0**; kétszer bukott: nincs.
5. `rogzit` a repó munkatáblájának scratch-másolatán (a `naplok/F132_*` nem változott); a megjegyzés a beírás előtt: „Code-session (előfizetői keret), general-purpose subagent claude-sonnet-5-5, a batch user-kérése szó szerint (thayer_api_koteg.py szaraz, adag 9001 antrop1; 2. próba: a javit B-javító kérése, J001-p2); eltérés: Claude Code alap rendszerutasítás, effort/max_tokens nem állítható”. `forditas.beir(…, 'sonnet')`: **11 sor** az `adat/forditasok.tsv`-ben (G4152 sz1–sz7, G5591 sz1–sz4). Költségnapló nem íródott (API-pénz nem ment el).

## Eredmény

A lapon a két melléknév szakaszai magyarul állnak; a CI E19 a G4152/G5591 kulcsokra zöld.

## C0 szúrópróba (a felhasználóé)

Javasolt sorok: **G4152 sz3** (1. jelentés, a ψυχή-vel szembeállítás, 1Kor 15:44, 46), **G4152 sz7** (3.b, a Szellemtől vezetett ember, 1Kor 2:15 — a javító kör ide tette be „a Szellem” alakot), **G5591 sz3** (a., 1Kor 15:44–46, a javító kör zárójel-javítása), **G5591 sz4** (b., 1Kor 2:14, Júd 1:19, Jak 3:15; a páratlan ASCII-idézőjel a forrás szerint maradt).
