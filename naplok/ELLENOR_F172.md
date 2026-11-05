# ELLENOR_F172 — F172_KAROLI_PONTOSSAG_BRIEF.md · aa61de89..8ff550e5

*A `fuggetlen-ellenor` subagent jelentése (claude-opus-5-5, 2026-11-05). A subagentnek nem volt fájlíró eszköze; a szöveget a végrehajtó session mentette változatlan tartalommal. Az eltérések átvezetése: `naplok/KAROLI_PONTOSSAG_jelentes.md` 10.*

```
ELTÉRÉS: 9 tétel
```

Modell-ellenőrzés: tényleges `claude-opus-5-5`, kért `opus` (a subagent-fájl szerint) — egyezik.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 / modell-mezők | OK | `f172/ellenor/valasz/*.json` | `Grep "modell": "claude-opus-5-5"` → 79/79 fájl (72 köteg + 7 `kulso_*`); ugyanez `"modell": "[^"]*"` mintával is 79 → nincs Sonnet/gemini érték. `pontossag_meres.py:141-144` meg is áll nem-Opus kötegnél. |
| 4.1 ellenőr-modell kötegenként | OK | ugyanott | a commit-üzenetek kötegenként `(claude-opus-5-5)` |
| (2) 70. köteg `javitas` | OK | `f172/ellenor/valasz/koteg_070.json:1` | a Jel 12:9 10. szavának jelölése elhagyva; a célok (`celok.tsv`) csak a 9. és a 13. szó; a 10. sem a mintában, sem az aranyban nincs → a mérést nem érinti. |
| 4.2 minta reprodukálható | OK | `eszkozok/karoli_strong/teszt_pontossag.py` | `Ran 16 tests … OK`, benne a `test_minta_fajl_reprodukalhato` és a Wilson-tesztek. |
| 4.3 réteg / súlyozott / ÓSZ–ÚSZ | OK | `f172/meres_eredmeny.tsv:3-13`; jelentés:40-52 | minden sor egyezik; kézi újraszámolás a `keret.tsv` súlyaival: ÓSZ 0,9450, ÚSZ 0,9707, összes 0,9506; a hibák rétegenként 2/16/10/10/14/4/9/7 = 72. |
| 4.4 kalibráció, hibatípusok | OK | `meres_eredmeny.tsv:18-59` | 362/374, 363/374, 371-es kizárásos, 9 kimaradt; 2 315 cél, 1 791 vers; a morféma-hibatípusok 17/5/4/2 = 28 (= 339−311). |
| 4.5 szúrópróba beépítve (DT-F172a (4″) szerint) | ELTÉRÉS | jelentés:93-100 | a külső összevetés bekerült, de a „végső becslés” nem korrigálja vele az Opus-számot, bár a lefedett 9 Opus-eltérésből ≥ 1 az Opus hibája (Róm 1:12); a „Nyitás: mehet” megelőzi a 6. pont kétes eseteinek eldöntését; a küszöböket (93%, 98%) a végrehajtó az eredmény ismeretében javasolta. |
| 4.6 `adat/` változatlan | OK | — | `git diff --stat aa61de89..HEAD -- adat/ konkordancia/` → üres |
| (3) jelentés ↔ külső táblák | OK | jelentés:64-85 | a fejezetsorok összegei, az osztályszámok (2580/197/34/522, Σ 3388), 217 vers, alakok Σ 4388, 2452/2525, 43; a külső pontosság és Wilson-határok kézzel újraszámolva egyeznek. |
| (4a) külső szám: túlzás | ELTÉRÉS | jelentés:14, 17, 83, 96, 100 | a „3 hiba 2 860 ellenőrzött párból” n-je tartalmazza a 197 másodlagos párt, amelyet a jelentés szerint „a forrás nem ellenőriz”, és 29 olyan eltérést, ahol a vak Opus a forrás ellen döntött. Tisztán a forrás szerint a fő-szó párokon (egyezik + konvenció) 2629/2663 = 98,72%, Wilson alsó ≈ 98,2%. A 99,8%-os főcím a háromutas ítéletet méri, nem a független forrást. |
| (4b) „egység határa” = konvenció | ELTÉRÉS | `pontossag_meres.py:82-90`; jelentés:17, 56, 97; `nyitott/uj/…md:2` | a szabály pusztán szomszédság (`abs(s-er)==1`); a 37 között van valódi felcserélés (Péld 3:18) és Opus-hiba (Róm 1:12 „egymás”) → a 97,45%-os felső érték és az N-F172b „37 rendszerhiba” állítása túloz. |
| (4c) „ugyanazon könyvekből” | ELTÉRÉS | jelentés:54 | az `OSZ_mozes` minta 200 párjából 12 jön 1–2Mózesből, 188 3–5Mózesből; a 99,0% vs 92,0% könyv-hatással is magyarázható. |
| (4d) Opus = „konzervatív alsó becslés” | ELTÉRÉS | jelentés:17, 34, 97 | csak akkor igaz, ha a közös hiba elhanyagolható; ezt csak 31 fő-szó páron mérték, a mellékszó/morféma párokon nem. |
| Számadat: morféma-arány | ELTÉRÉS | jelentés:25; `dontesek/uj/…md:1`; `nyitott/uj/…md:3` | 157 163 / 466 785 ÓSZ-pár = 33,7%; a 26,25% az összes párra vonatkozik. |
| Proveniencia | ELTÉRÉS | jelentés:5, 17, 56, 85, 97 | a 97,45% [96,52–98,38], a hibatípusok tartalmi/morféma bontása és az Opus-eltérések lefedési bontása nincs TSV-ben proveniencia-sorral. |
| Hatókör 3: `kezi` versek a keretből | ELTÉRÉS | `pontossag_minta.py:106-122` | a keret csak a `kezi` tokeneket hagyja ki, a vers többi párját nem (pl. Péld 11:31, 14 pár); a mintában nem szerepel, hatása elhanyagolható, de eltér a brief szövegétől. |
| DT32 / DT-F172a: forrásadat a repóban | ELTÉRÉS | jelentés:91; `nyitott/uj/…md:1` | a `f172/kulso/*` rendben (csak saját párok + osztály), de a jelentés és az N-F172a egyedi, forrás szerinti Strong-értéket közöl (Ez 43:13, Péld 3:18 „helyesen”); a DT-F172a csak összesítést és igehely-azonosítót enged. |
| N-F172a tartalom (A2) | OK | `nyitott/uj/…md:1` | `lekerdez.py scan`/`karoli` és `Grep` szerint a Péld 3:18 pár valóban felcserélt, az Ez 43:13 „közsinget” = H9002 + H2948; a hibák nyitottak. |
| N-F172b / N-F172c (A2) | ELTÉRÉS → (4b), morféma-arány | | |
| A1 memória vs. lekérdezés | OK (megjegyzéssel) | jelentés:89-91 | a kétes eseteket kérdésként teszi a felhasználó elé. |
| A3–A5 | NEM ELLENŐRIZHETŐ (nem értelmezett) | — | nincs ilyen állítás a diffben. |
| A6 E12–E15 | OK | — | 0 találat. |
| Vakság (brief 2.2) | OK | `f172/ellenor/utasitas.md`; `bemenet/koteg_001.txt:3-6` | a bemenetben nincs gépi pár; szabályok A–L. |
| CI | NEM ELLENŐRIZHETŐ (összevetés) | — | saját futtatás (`eszkozok/ellenorzes/futtat.py … --esemeny pull_request`): E2–E20, E26, E28, E29, E31–E33, E35 0 találat; E25 (3), E27 (42), E34 (45) a diff által nem érintett fájlokra; E30: 3 figyelmeztetés commit-üzenetekre. |
| Ellenőrzőlista 1–5 | OK | — | törlés csak a brief fejlécében; kulcstartomány teljes (66 könyv, 598 715 pár, 1 588 `fuggoben`); `adat/`, `konkordancia/` Δ = 0; a 3. lépés ⛔ döntése DT-F172a 🟢. |
| Fejezetválasztás (DT-F172a (4″)) | NEM ELLENŐRIZHETŐ (részben) | `f172/kulso/fejezetek.tsv` | a versszámok és a párösszegek stimmelnek; a kiválasztási szabályt csak a szkript futtatásával lehetne ellenőrizni. |

Súlyosság szerint: (1) 4a, (2) 4b, (3) 4c, (4) morféma-arány, (5) 4.5, (6) 4d, (7) DT-F172a forrás-Strong, (8) proveniencia, (9) `kezi` versek.
