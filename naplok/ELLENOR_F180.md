ELTÉRÉS: 1 tétel

# Független ellenőrzés — F180 (MOTIVUMNAPLO_HAMART)

*Brief: `F180_MOTIVUMNAPLO_HAMART_BRIEF.md` · diff: `c48bba16..67ba0c7b` (merge-base..HEAD, F180.0–F180.3) · ellenőr: `fuggetlen-ellenor` (claude-opus-5-5), 2026-11-09. Az ellenőrnek nincs fájlíró eszköze; a jelentést az orkesztráló session írta ki szó szerint az ellenőr visszaadott szövegéből. Az ellenőr a szerepe szerinti `ELTÉRÉS: <n> tétel` első sort adta.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | session `claude-opus-5-5`, kért `opus`; adattábla nem változott, `modell` mező nem íródott. |
| Kész (1) HAMART-szakasz + kézi könyv-index | OK | `motivumlog/PaRDeS_motivumok.md:466-487`, `:544-584`, `:602` | `Grep ^HAMART-001\t[^\t]+ adat/elofordulasok.tsv` → 48 sor (200–247). Minden HAMART-leletként megnevezett hely vagy a 48 sor között van, vagy jelölt: 1Móz 9:25, Jón 3:8, Gal 3:10, Róm 8:20-22→8:21, Mt 15:19, Mk 7:21-23, 2Pét 3:6-7, Jer 17:5, Hab 2:8, Hab 2:17, 5Móz 27:15-26, 5Móz 28:16-19→28:18, 5Móz 21:23. A Jer 51:25 és a Mal 3:11 nem fordul elő a fájlban. A nyitott szálak és a Jer 4:23 (TEREMT-002) nem HAMART-leletként állnak. |
| Kész (2) jelölés, nem törlés | OK | a diff 16/16 sora | `git diff --numstat`: 16+/16−, mind ugyanazon sor átírt változata; igehely nem tűnt el. |
| Kész (3) Gal 3:13-14 prózája | OK | `:478` | A kiemelés kikerült; egyezik az `elofordulasok.tsv:243` sorral (Remez, `közepes`) és a DT-F123hd/he-vel. `lekerdez.py scan G1944 --szakasz "Gal 3:13"` → n=1; `lxx-hid "5Móz 21:23"` → G2672 κεκατηραμένος; `lxx-hid "5Móz 27:26"`, `lxx-hid "1Móz 3:17"` → G1944 ἐπικατάρατος; `tsk "Gal 3:14"` → 1Móz 12,3 (8 szavazat). |
| Kész (3) Galata indexsor | **ELTÉRÉS** | `:579` | A sor `Gal 3:13-14→1Móz 3:17` célt ad (közvetlen kapcsolat a föld átkához). A DT-F123he és az adatsor szerint: „nem a föld átkát … tipológiai úton … nem közvetlenül”, a kapcsolatot a 3:14 áldás-mondata adja (1Móz 12:3). A zárójeles „tipológiai kapcsolat” ellenére a nyíl célja ellentmond ennek. |
| Kész (4) generált blokkok, E28 | OK | `:13-42`, `:148-179`, `:243-259`, `:492-536` | A diff hunkjai (467–487, 549–584, 599–605) a blokkokon kívül. `futtat.py --valtozott … --diff-alap c48bba16 --diff-fej HEAD` → E28: 0 találat (5 migrált nézet), kilépési kód 0. |
| Kész (5) csak `ir` + brief | OK | – | `git diff --stat`: csak a brief és a `motivumlog/PaRDeS_motivumok.md`; végleges `DT<n>`/`N<n>` nincs. |
| Kész (6) nincs adat nélküli új állítás | OK | `:478`, `:579-580` | Az új mondatok a fenti lekérdezésekre vagy az adatsorra épülnek. |
| G/D pontok | NEM ELLENŐRIZHETŐ | brief | A brief nem tartalmaz G/D pontot; a Teendő 1–3. és a Kész pontjai ellenőrizve. |
| A1 | OK | `:481` | A tematikus/lexikai besorolás változatlan; Ézs 24:5-6, Hós 4:1-3 az adatban. |
| A2 | OK | – | A diff nem érint nyitott tételt. |
| A3 | OK | `:481`, `:560-562` | A „TEMATIKUS, nem lexikai” címkék megmaradtak. |
| A4 | NEM ELLENŐRIZHETŐ | – | A diffben nincs Remez/Sod-szöveg. |
| A5 | OK | `:483` | A tanítói hiányjelzés érintetlen. |
| A6 | OK | CI-kimenet | E12: 70, E13: 27 jelentés, a látható példák változatlan sorokra esnek; a teljes lista nem látszik („további 67/24”). E14/E15: 0. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | – | Külső CI-jelentés nem volt; az E30 figyelmeztet: `67ba0c7b:uzenet` `ellenoriz`→`ellenőriz`. |
| L1 | OK | – | napló 16+/16−, brief 3+/2−; 0 törölt hely, 13 hely jelölve, 1 sor átírva (Gal 3:13). |
| L2 | OK | – | HAMART-001: 48 sor, egyezik a generált fejsorral (`:27`). |
| L3 | OK | – | `adat/`, `konkordancia/`, tanulmány, generált blokkok változatlanok. |
| L4 | OK | – | Egyetlen `adat/*.tsv` / `konkordancia/*.tsv` sem változott (Δ=0). |
| L5 | OK | – | A brief nem tartalmaz ⛔ pontot; a tiltásokat a menet betartotta. |

**ELTÉRÉS:** 1 tétel, kis súlyú — a kézi könyv-index `:579` sorában a `Gal 3:13-14→1Móz 3:17` nyíl közvetlen kapcsolatot jelez a föld átkához, szemben a DT-F123he és az adatsor „nem közvetlen, az áldás-mondaton át” leírásával.

**Az ellenőr saját eltérése:** a közös ős megállapításához `git merge-base` és `git rev-parse` parancsot is futtatott, ezek kívül esnek a megengedett körén.
