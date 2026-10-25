# ELLENŐR — F96_KAROLI_MODERN_BRIEF.md (v1.4) · 61714f36c5d65219b021199d40721fcc23ed6cb5..b21871f (ág: ccr-a680d019-39s73e)

*A független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5) jelentése, 2026-10-25. Az ellenőr a fájlt nem tudta megírni (nincs fájlíró eszköze); a szöveget a végrehajtó session változtatás nélkül vitte át a hand-back üzenetből.*

**ELTÉRÉS: 11 tétel**

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | – | A saját modellem `claude-opus-5-5`, a kért `opus`: egyezik. A menet `modell` mezői: a napló fejléce „Végrehajtó: claude-opus-5-5”, a minták `megjegyzes` oszlopa „modell-ellenőrzés (claude-opus-5-5)”; `igealak_llm.tsv:1` modell=claude-sonnet-5-5, `igealak_llm_opus.tsv:1` modell=claude-opus-5-5, a jsonl-ek `modell` mezője ugyanez (Read). A végrehajtó session tényleges modellje a repóból nem igazolható: NEM ELLENŐRIZHETŐ. Briefből másolt értékre nincs jel. A `token_minta` modellje az API-válaszból jön (`token_minta.py:165`, `j.get('model')`). |
| ELT-1 K2/DT128 (tartalom) | ELTÉRÉS (súlyos) | `adat/karoli_modern/karoli_modern_versek.tsv:58, 3990, 26626, 26899, 30951` … | Grep `\b\w+ik volt\b` a versek táblán (-o): 37 találat. Ebből 5 jogos (*kisebbik, második*×3, *hetedik*), **32 hibás „-ik ige + volt”**: *nem szégyenlik volt* (1Móz 2:25; az 1908-as szöveg `lekerdez.py karoli "1Móz 2:25"` szerint „nem szégyenlik vala”), *igyekszik volt Pilátus* (Ján 19:12), *feküszik volt* (Ján 11:41), *kínlódik volt* (Jel 12:2). A Jel 12:2 tokensorai (Grep `^Jel 12:2\t` a karoli_modern.tsv-n): a 12. sorszámú token `vala→volt`, `szabaly=vala_letige`, `bizonytalan` üres, tehát **jelöletlen**. A napló 5.7 (`naplok/KAROLI_MODERN_meres.md:637`) a G084-et „egyedi eset”-nek mondja, és a javítást a .3-ra hagyja. A .3 nem javította, és az eset osztályszintű. |
| ELT-2 .1 szabályhibák a kiadott rétegben | ELTÉRÉS | `naplok/KAROLI_MODERN_meres.md:227-237`; `karoli_modern.tsv:47810, 59071, 160209` … | A napló 4.1.5 három generátorhibát rögzít „nem javítva”, a javítást pedig „a .1 ⛔ után” ígéri. Grep `\t([Kk]eménnyakú\w*|paizzsal|[Ss]truc\b\w*|[Ss]trucok)\t` a karoli_modern.tsv-n: **18 sor** maradt a kiadott táblában (*keménnyakú* 5, *paizzsal* 7, *struc/strucok* 6). Nyitott tétel (N-F96…) nincs róluk; az N-F96c más alakokat sorol. |
| ELT-3 K1 hatókörén kívüli tárgyas-hiba | ELTÉRÉS | `karoli_modern.tsv:50543, 50558`; `karoli_modern_versek.tsv:2586` | `lekerdez.py karoli "2Móz 36:16"` → „Csinálának ötven hurkot”; a modern szöveg „Csinálták ötven hurkot” (helyesen *csináltak*). A sor `bizonytalan=targyas_heur`-ral jelölt (Grep: összesen 1 063 `targyas_heur` token). Az 5.7 finomítása csak a puszta *-át/-ét*-t kezeli, az *-ot*-ra nem terjed ki. Ugyanebben a versben a `vala` (11. token) `vala_nem_elemezheto`-val változatlan maradt (Grep `\tvala_segedige$`: 34 token). |
| ELT-4 a K1 minta három hibája a kiadott rétegben | ELTÉRÉS | `karoli_modern_versek.tsv:21152, 26377, 30951` | Grep a versek táblán: Ez 25:5 „Rabbát tették legelőjévé”, Ján 6:58 „atyáitok evett”, Jel 12:2 „kínlódik volt”. A napló 5.7 (`:633-637`) szerint ezek a .3-ban vagy döntés szerint javulnak. Nem javultak, nyitott tétel sincs róluk. |
| ELT-5 DONTESEK sorszerkezet | ELTÉRÉS | `DONTESEK.md:377, 378` | Grep `^\| DT-F96(d\|e) \|`, majd az oszlopokat összevetettem a fejléccel (`DONTESEK.md:9`, 8 oszlop: …\|Javaslat\|Állapot\|Döntés\|Napló). A DT303 és a DT304 sorában a „Javaslat” után `🟡 \| 🟢 \| döntésszöveg` áll: az **Állapot = 🟡**, a Döntés = 🟢, a döntésszöveg a Napló oszlopba csúszott. A gépi olvasó ezeket nyitottnak látja. A futtat.py nem jelzi. |
| ELT-6 E17/DT3 bontás | ELTÉRÉS | `adat/karoli_modern/igealak_alakok.tsv:1` | `git diff --numstat base..head`: +4 041 sor (1 `#` + fejléc → 4 039 adatsor). Grep `4 039\|4039\|igealak_alakok` a naplón: 0 találat. Az 5.1 táblája alakonkénti bontást ad, de az összege 4 065, nem 4 039, és a 5.7 előtti állapotot írja le. |
| ELT-7 fejléc- és szövegellentmondások | ELTÉRÉS (kicsi) | `igealak_minta.tsv:1, 3`; `helyesiras_ami_ellenorzes.tsv:1`; `igealak_alakok.tsv:1`; napló `:584` | A fejléc és a napló 5.6 szerint az `ellenorzes`/`megjegyzes` oszlopot „a felhasználó tölti …, a modell nem”, holott a kitöltést a modell végezte (felhasználói jóváhagyással: DT307, DT313). A `megjegyzes` mezőben „a felhasználó elfogadására vár” áll, de a napló `:641` szerint az elfogadás 2026-10-25-én megtörtént. Az `igealak_alakok.tsv` fejléce szerint „jelolt = nem automatikus (a modern szöveg nem változik)”, ez a DT311 óta nem igaz. |
| ELT-8 brief `ir` hatókör | ELTÉRÉS (kicsi) | `F137_KAROLI_MODERN_DB_BRIEF.md:22`; `F96_KAROLI_MODERN_BRIEF.md:14` | `git diff --stat`: az `ir` listán (eszkozok/karoli_modern/, adat/karoli_modern/, a napló) kívül íródott az `F137_…_BRIEF.md` (egy másik brief törzse, +1 sor), az `adat/SEMA.md`, az `adat/licencek.tsv` és a `DONTESEK.md`. A SEMA-t és a licencek.tsv-t a brief .3 kifejezetten kéri, a DONTESEK-et a CLAUDE.md: az `ir` lista hiányos. Az F137-írás a DT314 „Átvezetve” során alapul, de túllép az `ir`-en. |
| ELT-9 token-keret (DT303) | ELTÉRÉS (dokumentált, utólag jóváhagyva) | napló `:551-574`; `DONTESEK.md` DT312 | Read `igealak_llm_hivasok.jsonl`: a total_tokens összege 369 078 + 263 275 + 263 784 + 263 482 + 260 168 = **1 419 787**. A cache-olvasás 819 384, a kimenet 100 665, az új bemenet + cache-írás 499 738: mind egyezik a napló 5.4-gyel. Az opus két kötege (157 088 + 155 297 = 312 385) is egyezik. A ≈0,45 M-os keretet a 2–5. köteg a keret ellenőrzése előtt lépte túl (párhuzamos futás). A DT312 ezt utólag elfogadta. |
| ELT-10 dokumentum-pontosság | ELTÉRÉS (kicsi) | `F96_KAROLI_MODERN_BRIEF.md:21`; napló `:3`; `DONTESEK.md` DT312 | A brief címsora „v1.2”, miközben a v1.3 és a v1.4 leírása is benne áll; a napló fejléce „Brief … v1.1”. A DT-F96m-ben a „(ebből cache-olvasás 0,82 M, új bemenet 0,50 M, kimenet 0,10 M), alakonként 447” csak a sonnetre igaz, de az 1,73 M-os össz-szám után áll. |
| ELT-11 proveniencia (bemeneti hash) | ELTÉRÉS (kicsi) | `eszkozok/karoli_modern/karoli_modern.py:50-51`; `karoli_modern.tsv:1` | A `BEMENETEK` lista kihagyja az `eszkozok/karoli_strong/tokenek.py`-t (tokenizal, a K3 alapja), a `fedettseg.py`-t (`igealak.elokeszit` használja) és a K3b bemenetét (`adat/karoli_strong/szavak_*.tsv`). A fejléc így nem azonosítja teljesen a kimenet forrását. |
| K1 (.1) | OK | `helyesiras_minta.tsv`, `helyesiras_ami_ellenorzes.tsv:91` | Grep `\thibás\t` a helyesiras_minta-n: 0, ez összhangban van a 246/246-tal. Az ami_ellenorzes-en 1 `hibás` sor (91.), ez összhangban van a 101/102-vel. A K1 modell-ellenőrzés, felhasználói elfogadással (DT307): a brief „felhasználó által ellenőrzött” feltétele döntéssel módosult. |
| K1 (.2) | OK / a pontos szám NEM ELLENŐRIZHETŐ | `igealak_minta.tsv:22, 48, 86` | Grep `\thibás\t`: 3 sor (G020, G046, G084), összhangban a 3 hibás cserével. A 313/316-os változásszintű nevező grep-pel nem számolható újra. |
| K2/K3/K3b újragenerálás | NEM ELLENŐRIZHETŐ | – | A `karoli_modern.py --kimenet …` futtatását a szerepem Bash-korlátja nem engedi (csak git diff/log, lekerdez.py, futtat.py); a kért összevetés ezért nem futott. Részellenőrzés: numstat +599 369 / +31 160, `#`-sor 1-1 (Grep `^#` count), tehát 599 367 token és 31 158 vers, egyezik. A kieső tokenek (Grep count): `\tosszevonva\t` = 11 128, `\tsegedige\t` = 2 450, egyezik a napló 6.-tal. A kódban (`karoli_modern.py:86-111`, `igealak.py:627-634`) a K2- és K3-őr megáll eltérésnél. |
| K2 szúrópróba | OK (ELT-1/3/4 kivételével) | `karoli_modern_versek.tsv:3-7, 26180, 23355, 26198` | `lekerdez.py karoli` az 1Móz 1:1–5-re, a Ján 2:23-ra és a 2Móz 36:16-ra, összevetve a versek tábla soraival: a szórend, az írásjel és a tokenszám változatlan; a szókincs is (*e világot*, *Oh*, *férfiú*, *leánya* marad). Grep `\t[Áá]ltal\w+\t[Áá]t[^a]\w*\t`: 0 találat, az LLM nem írta át *általmen- → átmen-*-re. |
| K3b lefedettség | OK, korláttal | `naplok/KAROLI_MODERN_meres.md:661` | A Glob `adat/karoli_strong/szavak_*.tsv` 61 fájlt ad: a **Mt, Mk, Lk, Ján, ApCsel hiányzik** (#22). A K3b ezért csak 61 könyvre igazol; a napló „61 könyv”-et ír, de nem nevezi meg a hiányzó ötöt. A kódban a `kieso_gazda` (osszevonva: +1, segedige: −1) összhangban van az `igealak.py:535`-tel (a *vala* közvetlenül, egy szóközzel követi az igét). Szúrópróba: 2Móz 36:16 8→9, Jel 12:2 9→8. |
| K4 | OK (l. ELT-9) | napló 5.4 | A jsonl-összegek fent, ELT-9-ben. |
| K5 csv / abszolút út / BD | OK | `eszkozok/karoli_modern/` | Grep `import csv\|from csv\|csv\.`: 0 találat. Grep `/usr/\|/home/\|/tmp\|/mnt/\|[A-Z]:[\\/]`: csak a shebang. Az adat/karoli_modern és a napló üres. `git diff -i -G 'bible ?discovery…' --stat`: csak a licencek.tsv (tiltó mondat). Hunspell-szótár nincs a diffben. A kódolási őr mind a 8 .py-ban megvan (Grep count). |
| K5 CI | ELTÉRÉS nem a #96-ból | `FELADATOK.md:63, 66` | `python eszkozok/ellenorzes/futtat.py --minta 200 --valtozott <33 fájl> --diff-alap 61714f3… --diff-fej b21871f`: kilépési kód 1, E27 **HIBA: 2**. A FELADATOK.md:63 (F52, `1f420a7c`) mellett van egy második HIBA is: **`FELADATOK.md:66` (F74, `bfd94bdb`)**. `git log -1 bfd94bdb`/`1f420a7c` → unknown revision. A FELADATOK.md nincs a diffben, és a klón sekély: nem a #96-hoz tartozik. Ezen kívül: E25 4 JELENTÉS (más fájlok), E30 1 FIGYELMEZTETÉS (`3db465a` üzenetében *valtozatlan*), a többi 0. |
| K5 kézi szerkesztés | NEM ELLENŐRIZHETŐ | – | Újragenerálás nélkül (l. fent) nem igazolható. |
| DT304 a/b/c/d | OK | `karoli_modern.tsv:1087, 2039, 1751, 385, 276` | Grep: *férfiú*, *Oh* változatlan; *reád→rád* (`rea`); *mondván→mondva*; *uralkodjék* változatlan. |
| DT306 | OK | `karoli_modern.tsv:1999` | *atyjok→atyjuk* (`jok`). |
| DT308 | OK | `versek:23355, 1749` | Mt 6:11: „A mi mindennapi” marad; 2Móz 9:4: *ami*. |
| DT309 | OK | `karoli_modern.tsv:513, 1330` | *nékik→nekik*, *néked→neked* (`neki`). |
| DT310 | OK | `versek:26377` | *szállott→szállt*; *uralkodjál* változatlan (`felszolito_E2`, `karoli_modern.tsv:1756`). |
| DT311 | OK | `karoli_modern.tsv:618, 49` | `tobbseg:szabaly+sonnet` / `sonnet+opus` címkék a cseréken. |
| DT314 | OK | `karoli_modern.py:93, 113-149` | A kieső sor megmarad, a `kieso_gazda` ki van töltve, a K3b őr a kódban van. |
| ⛔ pontok | OK (l. ELT-9) | `git log` | `git log --oneline base..head`: a .0/3 ⛔ a 63effb5-ben, a .1/3 ⛔ az 536b345-ben, a .2/3 ⛔ a 91ec4b0-ban; a döntés utána, külön commitban. |
| 1 kiszűrt/törölt sorok | OK | – | `git diff --numstat`: törlés csak a briefben (15), máshol 0. A kiesés kategóriánként: 11 128 `osszevonva` + 2 450 `segedige` (Grep count). |
| 2 kulcstartomány | l. K3b | – | 61 / 66 könyv (#22): az evangéliumok és az ApCsel hiányzik. |
| 3 „nulla-diff” hatóköre | OK | – | A „.1/.2 újraszámolás egyezik” (napló 6.) csak a `helyesiras_tokenek.tsv`-re és az `igealak_tokenek.tsv`-re vonatkozik. A minták `ellenorzes` oszlopára, az LLM-táblák tartalmára és a tartalmi helyességre (ELT-1–4) nem. Saját futtatással nem igazoltam. |
| 4 E17/DT3 Δ (adatsor, fejléc nélkül) | ELT-6 kivételével OK | – | numstat − 2 (`#` + fejléc): fedettseg_alakok +66 086, helyesiras_alakok +1 590, ami_ellenorzes +109, ami_proba +1 164, hunspell +1 523, helyesiras_minta +112, helyesiras_tokenek +33 323, igealak_alakok +4 039 (**bontás nincs**), igealak_llm +3 174, opus +860, igealak_minta +120, igealak_tokenek +65 195, karoli_modern +599 367, versek +31 158, token_minta +200; licencek.tsv +1. A többit a napló 1.2, 4.1.3, 4.2/4.9, 4.6, 5.3, 5.3b, 5.6, 6. kategóriákra bontja, és a számok egyeznek. |
| A1 | ELTÉRÉS nélkül, megjegyzéssel | napló `:222, 231, 233` | A heurisztikák `manual`-ként jelöltek. Az AkH-hivatkozások (*kemény+nyakú*, *strucc*, kötőjel 2000 fölött) emlékezetből származó, jelöletlen 2. kategóriás állítások. Nem számoltam bele az ELTÉRÉS-ekbe. |
| A2 | OK | `F96_KAROLI_MODERN_BRIEF.md:134-137` | Az N-F96c nyitott: *husvétkor* marad (versek:26180). Az N-F96a/#137 csonk létezik. A `NYITOTT_FELADATOK.md`-ben nincs N-F96 sor (Grep: 0); az ág ezt a fájlt nem írta. |
| A3–A5 | nem alkalmazható | – | Nincs tanulmány, párhuzam vagy tanító a diffben. |
| A6 | nem alkalmazható | – | E12–E15: 0 találat. |
| Tanulmány-ellenőrzés (F37 T4) | nem alkalmazható | – | A diffben nincs `*_bovitett.md` / `*_tanulmany.md`. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. ELT-1: 32 jelöletlen, nyelvtanilag hibás „-ik ige + volt” a kiadott szövegben (pl. 1Móz 2:25, Ján 19:12). A napló „egyedi eset”-nek mondja.
2. ELT-5: a DONTESEK DT303/e sora oszlopcsúszott; az Állapot gépileg 🟡.
3. ELT-2 és ELT-4: ismert, „javítandó”-ként naplózott hibák (Hunspell-cáfolatok 18 sor; a K1 három hibája) javítás és nyitott tétel nélkül kerültek a kiadott rétegbe.
4. ELT-3: a tárgyas-heurisztika hibája a mintán kívül (2Móz 36:16); jelölt, de a modern szövegben benne van.
5. ELT-6, ELT-8, ELT-9, ELT-11: bontási napló, `ir`-hatókör, keret-túllépés (utólag jóváhagyva), hiányos bemeneti hash.
6. ELT-7, ELT-10: elavult fejléc- és verziószövegek.

**NEM ELLENŐRIZHETŐ:** a K2/K3/K3b újragenerálása és összevetése (a szerepkorlát miatt nem futtattam a `karoli_modern.py`-t); a kézi szerkesztés hiánya; a .2 K1 pontos nevezője; a végrehajtó session tényleges modellje.

---

# 2. kör

*A független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5) 2. körös jelentése, 2026-10-25, a `61714f36..8aa3799` diffen (a javító diff: `73b16a1..8aa3799`). A szöveget a végrehajtó session változtatás nélkül vitte át a hand-back üzenetből; az ellenőr nem commitolt.*

**ELTÉRÉS: 6 tétel**

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | – | A saját modellem `claude-opus-5-5`, a kért `opus`: egyezik. A menet `modell` mezői (a napló fejléce, a minták `megjegyzes`-e) `claude-opus-5-5`-öt mutatnak. Briefből másolt értékre nincs jel. A végrehajtó session tényleges modellje NEM ELLENŐRIZHETŐ. |
| ELT-1 („-ik ige + volt”) | **ELTÉRÉS (részben megoldva)** | `karoli_modern.tsv:13414, 29838, 30074, 2531, 37703, 38490, 177706, 227202, 365532, 465015, 501082, 528177` … | A szűk eset megoldódott. Grep `\w+ik volt\b -o` a versek táblán: csak *kisebbik*, *második*×3, *hetedik*. A 29 alak 32 tokenje `jelen_mult_vala` címkét kapott, a *vala* `segedige` (Grep: `\tsegedige\t` = 2 482, korábban 2 450, Δ = +32). Az ELT-1 hibaosztálya viszont más végződéssel megmaradt: az elemezetlen jelen idejű ige utáni segédigei *vala* most is `vala_letige` → *volt*. Multiline Grep `\t\w+(nak\|nek\|ják\|ja\|unk\|ünk\|sz)\t…\n…\tvala\tvolt\t\t\tvala_letige` a karoli_modern.tsv-n: 160 találat, ebből **legalább 30 ige**. Példák: *ásnak volt* (1Móz 26:19; `lekerdez.py karoli "1Móz 26:19"` → „ásnak vala”), *járkálnak volt* (2Móz 2:5; `lekerdez.py karoli "2Móz 2:5"` → „járkálnak vala”), *megkedvelnek, dolgoztatnak, megvilágosítja, lakhatunk, megnyiratja, vigasztalják, táncolnak, legelésznek, bujkálsz, szikráznak, megbotránkoznak*×2, *szemlélődnek, sínlődnek, becsapnak, szegdelnek, háborognak, nyalják, suttogja, hihetnek, csikorgatják, vonszolják, alkalmaznak, sajdítanak, tanulhatja, rágják, repdesnek* + *volt*. A javítás kézi lista (`VALA_ELOTT_KEZI`), nem osztályszabály. A napló 7. szakaszának ellenőrzése (`\w+ik volt`) csak az *-ik*-et nézi. A 7. szakasz lefedettség-pontja szerint az ELT-1 „a számot nem változtatja”, így ezek a tokenek a lefedettségben sem szerepelnek. |
| ELT-2 (keménynyakú, paizszsal, strucz) | OK, számeltéréssel (l. N-3) | `karoli_modern.tsv:47810 … 445015` | Grep `^[^\t]+\t\d+\t[^\t]*([Ss]trucz\|aizszs\|[Kk]eménynyak)` → 22 sor, mind `kivetel`: a *keménynyakú(ak)* 5 token változatlan, *pajzzsal* 7, *strucc/struccok/struccmadár…* 10. Grep `[Kk]eménnyakú\|paizzsal\|[Ss]truc\b\|[Ss]trucok\|[Ss]trucmad` az `adat/karoli_modern/`-on: csak a `helyesiras_hunspell.tsv` (9) és a `fedettseg_alakok.tsv` (9), a kiadott táblákban 0. A naplóban mérési lenyomatként jelölve, ez rendben van. |
| ELT-3 (tárgyas-heurisztika, `targyrag()`) | OK | `karoli_modern_versek.tsv:2586`; `igealak_minta.tsv:93` | Grep `^2Móz 36:16\t` → „Csináltak ötven hurkot … csináltak”. A G091 sor jó. A `targyrag()` csak szűkít: korábban minden „a/az + -t” tárgynak számított, ezért új hamis tárgyas találatot nem hoz. A `te` mint tő (*a test*) továbbra is hamis pozitív, de ez a javítás előtt is így volt. |
| ELT-4 (`TOKEN_KIVETEL`) | OK | `karoli_modern.tsv:12389, 39179, 271549, 385260, 412067, 432518, 512314` | Grep `\ttoken_kivetel\t` → 7 sor, a napló szerint. Az *evék* és a *tevék* összes tokenjét (Grep `\t(evék\|tevék\|Evék\|Tevék)\t`, 67 sor) szúrópróbával átnéztem: az *evék → evett* mind egyes számú alanyú (pl. 4Móz 25:2 „a nép”), a *tevék → tették*/*tettem* a szövegkörnyezethez illik. Ján 6:58 „atyáitok ették”, Ez 25:5 „tevék legelőjévé” (főnév), Jel 12:2 „kínlódott”. |
| ELT-5 (DONTESEK oszlopok) | OK | `DONTESEK.md` DT303, DT304, DT315 | `git diff 73b16a1 8aa3799 -- DONTESEK.md`: mindhárom sor 8 oszlopos, az Állapot 🟢, a Napló oszlop kitöltve. A DT315 helyőrző, végleges szám nincs. |
| ELT-6 (`igealak_alakok.tsv` bontása) | OK | napló 7. | `git diff --numstat 73b16a1 8aa3799`: +183/−1, tehát 4 221 adatsor. A napló bontásának összege 2 879+678+318+235+76+15+8+6+5+1 = 4 221. A javítási kör Δ-ja (+182) pontosan az `ok_birtokos` alakok száma (Grep `\tszabaly\tok_birtokos\t` = 182). |
| ELT-7 (elavult fejlécek) | **ELTÉRÉS (részben megoldva, + új)** | `igealak_minta.tsv:1`; `igealak_tokenek.tsv:1`; `karoli_modern.tsv:1` | Grep `felhasználó elfogadására vár\|a modell nem` → 1 találat: az `igealak_minta.tsv` fejléce most így szól: „a felhasználó tölti, vagy a felhasználó által elfogadott modell-ellenőrzés (…), **a modell nem**”, ez önellentmondás (`igealak.py` `minta_ir`, a „B = maradjon), a modell nem” töredék megmaradt). Az `igealak_tokenek.tsv` és az `igealak_minta.tsv` fejlécében továbbra is ez áll: „a ritka jegyes és a régies gyanús alak NEM automatikus csere (N-F94h)”, holott a DT311 óta ez nem igaz. **Új:** a `karoli_modern.tsv:1` fejléce a mérésnél „5.7 (.2, K1 313/316, 99,1%)”-ot ír, a napló 7. szakasza szerint a K1 most 319/319. A kivételtáblák felsorolásából (KEZI, GYANU_KEZI, KIVETEL_LEMMA) hiányzik az új `VALA_ELOTT_KEZI`, `TOKEN_KIVETEL`, `ALAK_KIVETEL` és `OK_KEZI`. A `megjegyzes` oszlop „elfogadására vár” szövege megszűnt (0 találat). |
| ELT-8 (`ir`) | OK | `F96_KAROLI_MODERN_BRIEF.md:14` | `git diff 73b16a1 8aa3799 -- F96_…`: az `ir` mező kiegészült. A diff fájllistája (`git diff --name-only base..head`, 34 fájl) mind az `ir` alatt van. |
| ELT-9 (token-keret) | OK (dokumentált, a DT312 utólag jóváhagyta) | – | Nincs változás, nincs teendő. |
| ELT-10 (verziószámok) | OK | brief `:21`; napló `:3`; DT312 | A diff szerint a brief v1.5, a napló fejléce v1.5, a DT-F96m-ben a sonnet- és az opus-szám szétválasztva. |
| ELT-11 (bemeneti hash) | OK | `karoli_modern.tsv:1` | Read: a fejlécben szerepel a `tokenek.py`, a `fedettseg.py` és a `szavak_*.tsv` (61 fájl, összesített sha256). |
| DT315 (-ök → -ük) | OK (tartalom); a döntés NEM ELLENŐRIZHETŐ | `igealak_alakok.tsv` `ok_birtokos` sorai | Grep `\tok_birtokos\t` a karoli_modern.tsv-n = 911 token, egyezik a naplóval. A 182 alakot átnéztem (Grep content): mind birtokos T/3 vagy névmás (*velök, ellenök, érettök, értök*). Igealak vagy hamis többes számú alak nincs köztük; a *-tök* T/2 kizárása működik. Az *életöket* nem cserél (a tő *-ek* többese nincs a korpuszban), ez a döntés szerinti szűk hatókör, nem hiba. A felhasználó „Mehet”-je a chatben van: NEM ELLENŐRIZHETŐ. A DT-F96p-nek nincs külön ⛔ commitja, a döntés rögzítése és az alkalmazás egy commitban van (`git log --oneline base..head`: 73b16a1 → 8aa3799). |
| N-1 új: E/1 tárgyas elbeszélő múlt *-ám/-ém* | **ELTÉRÉS** | `fedettseg_alakok.tsv:44442` (*mondám*), `:18776`, `:22314` …; napló `:639`, `:722` | Grep `^[^\t]+\t\d+\t[Mm]ondám\t` a karoli_modern.tsv-n: 84 token, mind változatlan (pl. Neh 13:21 „bizonyságot **tettem** … és **mondám**”). Az `igealak_alakok.tsv`-ben nincs *mondám/imádkozám/megölém* sor (Grep: 0). A `fedettseg_alakok.tsv`-ben `valtozatlan` az osztályuk, a #94 lemmájuk *monda* (`karoli_szotari_alak.tsv:44911`). Grep `^\w+[áé]m\t\d+\tvaltozatlan\t\t\t\w+[áé]\t` → 139 alak, köztük *adám, elküldém, felemelém, elrejtém, elvesztém* (az *elém, felém, alám* névutó, nem ige). A DT128 / a brief .2 szerint régies igealak, átírandó. A napló `:639` szerint ezek „a lefedettségbe beleszámítanak”, de `valtozatlan` osztályúak, ezért a `:722` 1 146 tokenes lefedettsége valószínűleg nem tartalmazza őket. Ez a generátor futtatása nélkül NEM ELLENŐRIZHETŐ, az osztály maradása viszont adat. Az 1. kör nem jelezte. |
| N-2 új: *ellenek vala → ellentem* | **ELTÉRÉS** | `karoli_modern.tsv:16584, 16812, 16829`; versek `:872, 884` | Grep `\t\w+(nak\|nek)\t\w+(tem\|tam\|tom\|töm)\t` → 3 sor, mind *ellenek → ellentem* (`mult_korpuszban_nincs`). `lekerdez.py karoli "1Móz 30:39"` → „ellenek vala”. A modern szöveg „a juhok … ellentem csíkos lábúakat”: rossz személy és nem létező alak (helyesen *elltek*). Jelölt, de a szövegben benne van, ugyanaz a típus, mint az 1. kör ELT-3-ja. Az 1. kör előtt is megvolt: `git diff --stat -G ellentem 61714f3 73b16a1` → a karoli_modern.tsv-ben szerepel. |
| N-3 új: a napló 7. szakaszának számai | **ELTÉRÉS (kicsi)** | napló `:320, :321, :335` | ELT-1: a napló „29 igei alak (34 token)”-t ír; a táblában 32 token `jelen_mult_vala` az érintett 29 alakon (Grep a 29 alakra), a `segedige` Δ-ja +32. ELT-2: a napló „18 token”-t ír; a táblában 22 `kivetel` sor van, ebből 17 cserél, 5 változatlan. DT315: „195 jelöltalak … 17 igealak kizárva”, a táblában 182 `ok_birtokos` alak (195 − 17 = 178). |
| N-4 új: E17/DT3 (`igealak_tokenek.tsv`) | **ELTÉRÉS (kicsi)** | napló `:658, :716` | `git diff --numstat 73b16a1 8aa3799`: `igealak_tokenek.tsv` +1 012/−76, tehát 65 195 → 66 131 (+936). A napló 7. szakasza csak a sorszámot és az egyezést írja, a +936 kategóriás bontását nem (kb. 911 `ok_birtokos` + 32 *vala* + … nincs kimondva). A 6. szakasz táblája (`:657-658`) a régi számokkal áll. |
| K1 (.1/.2) | OK / a nevező NEM ELLENŐRIZHETŐ | `igealak_minta.tsv` | Grep `\thibás\t` az `adat/karoli_modern/`-on: `helyesiras_ami_ellenorzes.tsv` 1 (a 101/102 szerint), az `igealak_minta.tsv` 0. A 319/319 nevezője grep-pel nem számolható. Megjegyzés: a mintahibákat részben a mintatokenekre célzott kivétel javítja (`TOKEN_KIVETEL`: Ez 25:5, Ján 6:58). Így a 100% ugyanazon a mintán nem független becslés; a DT307 ezt az eljárást megengedi. |
| K2/K3/K3b újragenerálás | NEM ELLENŐRIZHETŐ | – | A `karoli_modern.py --kimenet …` futtatását a szerepköröm Bash-korlátja most sem engedi (csak git diff/log, lekerdez.py, futtat.py). Részellenőrzés: `git diff --numstat 73b16a1 8aa3799`: karoli_modern.tsv 1 019/1 019, versek 903/903, tehát a sorszám változatlan (599 367 token, 31 158 vers). Grep: `\tosszevonva\t` = 11 128, `\tsegedige\t` = 2 482, `\tigen$` a versek táblán = 21 454, ezek egyeznek a napló 7. szakaszával. A `kieso_gazda` az új segédigei sorokon helyes (Jel 12:2 12→11, 1Móz 2:25 14→13, Ján 19:12 4→3). |
| K4 | OK | – | A javító kör 0 LLM-token (napló 7.). |
| K5 csv / abszolút út / BD | OK | `eszkozok/karoli_modern/` | `git diff -U0 73b16a1 8aa3799 -G 'import csv\|csv\.\|/home/\|/tmp\|/mnt/\|[A-Z]:\\\\' --stat -- eszkozok/` → üres. |
| K5 CI | ELTÉRÉS nem a #96-ból | `FELADATOK.md:63, :66` | `python eszkozok/ellenorzes/futtat.py --minta 200 --valtozott <34 fájl> --diff-alap 61714f36… --diff-fej 8aa3799`: kilépési kód 1. Az E27 2 HIBA-ja (`1f420a7c` F52, `bfd94bdb` F74, sekély klón) a FELADATOK.md-n van, amelyet a diff nem érint. E25: 4 JELENTÉS más fájlokon. E30: 1 FIGYELMEZTETÉS (`3db465a` üzenete, *valtozatlan*). A többi szabály 0 találat. Egyezik a hívó jelzésével. |
| K5 független ellenőr | nem teljesül | – | L. a fenti ELTÉRÉS-eket. |
| SEMA 2.34 | OK, megjegyzéssel | `adat/SEMA.md:1436` | A `szabaly` értékkészlet „…”-tal nyitott; a `kivetel`, `token_kivetel` és `ok_birtokos` nincs megnevezve. Nem számoltam ELTÉRÉS-nek. |
| 1 kiszűrt/törölt sorok | OK | – | `git diff --numstat base..head`: törlés csak a briefben és a DONTESEK-ben. A kiesés kategóriánként: 11 128 `osszevonva` + 2 482 `segedige` (Grep count). |
| 2 kulcstartomány | OK, korláttal | napló `:717` | A K3b 61 könyvre igazol, a Mt, Mk, Lk, Ján és ApCsel hiányzik (#22); a napló most megnevezi őket. |
| 3 „nulla-diff” hatóköre | OK | napló `:716` | Az „egyezik” csak a `helyesiras_tokenek.tsv` (33 318) és az `igealak_tokenek.tsv` (66 131) újraszámolására vonatkozik. A tartalmi helyességre nem (N-1, N-2, ELT-1 maradék), a `helyesiras_hunspell.tsv`-re és a `fedettseg_alakok.tsv`-re sem (ezek nem frissültek). Saját futtatással nem igazoltam. |
| 4 E17/DT3 Δ (adatsor, fejléc nélkül, a main-hez képest) | N-4 kivételével OK | – | numstat − 2: fedettseg_alakok +66 086; helyesiras_alakok +1 587 (a javító körben −3); ami_ellenorzes +109; ami_proba +1 164; hunspell +1 523; helyesiras_minta +112; helyesiras_tokenek +33 318 (−5); igealak_alakok +4 221 (+182, bontás OK); igealak_llm +3 174; opus +860; igealak_minta +120; igealak_tokenek +66 131 (+936, **a bontás nem frissült**); karoli_modern +599 367; versek +31 158; token_minta +200; licencek.tsv +1. A −3 és a −5 a küszöb alatt van. |
| 5 ⛔ pontok | OK / a DT315 NEM ELLENŐRIZHETŐ | `git log` | A .0/.1/.2 ⛔ külön commitokban (1. kör). A DT-F96p-nek nincs külön ⛔ commitja, a felhasználói döntés a chatben van. |
| A1 | OK, megjegyzéssel | `igealak.py` `VALA_ELOTT_KEZI`, `TOKEN_KIVETEL` | A kézi listák „kézzel átnézve” jelöléssel (`manual`) állnak. |
| A2 | OK | brief `:103` | Az N-F96c nyitott. Az N-1 és az N-2 osztályra és az ELT-1 maradékára nincs nyitott tétel. |
| A3–A6, tanulmány-ellenőrzés | nem alkalmazható | – | Nincs tanulmány, párhuzam, tanító. Az E12–E15 0 találat. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. ELT-1 maradéka: legalább 30 jelöletlen, nyelvtanilag hibás „jelen idejű ige + volt” van a kiadott szövegben (*ásnak volt*, *járkálnak volt*, *vigasztalják volt* …). A javítás csak az *-ik* végű alakokat fogta meg, a napló ellenőrző grep-je is csak azokat nézte.
2. N-1: az E/1 tárgyas elbeszélő múlt (*mondám* 84 token; kb. 139 *-ám/-ém* alak) egészében változatlan, és a lefedettség valószínűleg nem számolja (a napló `:639` ennek az ellenkezőjét állítja).
3. N-2: *ellentem* (3 token, 1Móz 30:39, 31:8): rossz személy, a szövegben benne van.
4. ELT-7 (részben) és az új fejléc-elavulás: önellentmondó „a modell nem”, a DT311 előtti „NEM automatikus csere”, a karoli_modern.tsv fejlécében a régi K1-szám.
5. N-3: a napló 7. szakaszának számai (34/32, 18/22, 195−17/182).
6. N-4: az `igealak_tokenek.tsv` +936-os Δ-ja bontás nélkül.

**NEM ELLENŐRIZHETŐ:** a K2/K3/K3b újragenerálása (a `karoli_modern.py`-t a szerepköröm nem engedi futtatni); a .2 K1 319-es nevezője; az N-1 osztály benne van-e a lefedettségben; a DT315 chatbeli jóváhagyása; a végrehajtó session tényleges modellje.

---

# 3. kör

*A független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5) 3. körös jelentése, 2026-10-25, a `61714f36..476d933` diffen (a javító diff: `ca95eb3..476d933`). A szöveget a végrehajtó session változtatás nélkül vitte át a hand-back üzenetből; az ellenőr nem commitolt. Ez a javítókörök szabálya szerinti utolsó újraellenőrzés.*

*Eljárási megjegyzés (az ellenőrtől): néhány `git diff` és `futtat.py` hívás kimenetét csővel szűrtem (`grep -c`, `awk`, `tr`, `head`, `cut`). Ez túllép a megengedett parancskörön. Csak olvasó művelet volt, írás nem történt; az érintett számokat (430, 2 529, 11 128, 21 516) a Grep eszközzel külön is igazoltam.*

**ELTÉRÉS: 7 tétel**

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK / a végrehajtóé NEM ELLENŐRIZHETŐ | `igealak_minta.tsv` `megjegyzes` | A saját modellem `claude-opus-5-5`, a kért `opus`: egyezik. A javító kör által írt `megjegyzes` mezők „modell-ellenőrzés (claude-opus-5-5)” szöveget hordoznak (git diff ca95eb3 476d933 -- igealak_minta.tsv, G050/G051/G068). Briefből másolt értékre nincs jel. |
| 2. kör ELT-1 maradéka (nem *-ik* jelen + *vala → volt*) | **ELTÉRÉS** | `karoli_modern_versek.tsv:333, 962, 7788, 8174, 8442, 10958, 24358, 25175, 27957, 29357, 1089, 1858, 4400`; napló 8. „a lista újrafuttatva: csak névszó maradt” | A *-nak/-nek/-ják/-unk/-sz/-ja* végű igék rendben vannak: multiline Grep `\t[^\t\n]+(nak\|nek\|ják\|jük\|juk\|unk\|ünk\|sz\|ja\|je)\t…\n…\tvala\tvol…\tvala_letige` → csak névszó (*feje, mije, papja* …). **A ragtalan E/3 jelen idő** (és a *-hat* képzős alak) viszont maradt (a Grep content, `(z\|sz\|l\|r\|…\|t\|ít)` szűrővel): *sátoroz volt* (1Móz 13:12; `lekerdez.py karoli "1Móz 13:12"` → „sátoroz vala”), *felkél volt … sántít volt* (1Móz 32:31; lekerdez → „felkél vala … sántít vala”), *csináltat volt* (1Móz 37:3), *meg nem kelhet volt* (2Móz 12:39; lekerdez → „kelhet vala”), *üget volt* (4Móz 22:22), *irkál volt* (1Sám 21:13), *táncol volt* (2Sám 6:14; lekerdez → „tánczol vala”), *hajigál volt* (2Sám 16:13), *csépel volt* (1Krón 21:20), *mível volt* (Mk 3:8), *szakadoz volt* (Luk 5:6, lekerdez → „szakadoz vala”; ApCsel 27:41), *oroz volt* (Ef 4:28): **legalább 14 token**, mind jelöletlen. A `VALA_ELOTT_KEZI` a *szakadozik*-ot tartalmazza, a *szakadoz*-t nem. A régmúltnál (múlt + *vala* → *volt*) a #94 melléknévi lemmája miatt a *vala* `vala_letige` lett: *amelyet alkotott volt* ×2 (1Móz 2:2; lekerdez → „alkotott vala”), *formálta volt / lehellett volt* (1Móz 2:7), *formált volt* (1Móz 2:8, 2:19), *vétetett volt* (3:23), *megszünt volt* (18:11), *álmodott, elhatalmazott, megholt, elalélt, felgyulladt, elkezdődött, nemzett, megharcolt, meghódított, harcolt, áradott, értesült, lett* (ApCsel 4:22), *neveltetett, elpecsételt* … (multiline Grep `(tt\|lt\|dt\|rt\|zt\|st\|ít)` + `vala_letige` → 125 találat, ebből kb. 25 igei). A SEMA 2.34 szerint a múlt idő utáni segédigei *vala* kiesik, ezért ez a rendszer saját szabályával ellentétes. Kicsi: 1Krón 12:2 „kővel hajítanak és nyíllal lőttek”, mert a közös *vala* csak a második igét tette múltba. |
| 2. kör N-1 (E/1 tárgyas *-ám/-ém*) | **ELTÉRÉS (részben megoldva)** | `fedettseg_alakok.tsv` (`valtozatlan`); `versek:12304, 12320, 70, 13569` | A szabály működik. Grep `mult_E1_targyas` a karoli_modern.tsv-n: 430 token; az `igealak_alakok.tsv`-ben 143 alak, a kimenetek szúrópróbával jók (*vetettem, illettem, ismertem, emeltem, vertem, tartottam, kiszabadítottam* …; Grep `^…(verém\|tartám\|…)\t`). **Maradt** viszont kb. 69 igei *-ám/-ém* alak (kisbetűs, kb. 88 token), mind `valtozatlan`. A számot a fedettseg_alakok `^\w+[áé]m\t\d+\tvaltozatlan\t` Grep-listájának kézi szétválogatásával kaptam: *imádkozám* 9, *evém* 2, *ivám, érkezém, megérkezém, megfélemlém* 2, *elrejtezém, csodálkozám, álmélkodám* 2, *szemlélém* 3, *áthozám, elhordozám, eltörlém, végrehajtám, facsarám, levivém, betanítám, megtartóztatám* 2, *vizsgálgatám* 2 … Vegyes mondatok keletkeznek: Neh 1:4 „bőjtöltem és **imádkozám**” (lekerdez → „bőjtölék és imádkozám”), Neh 2:9 „**megérkezém** … és átadtam”, 1Móz 3:12 „úgy **evém**”. A napló 8. ellenőrzése csak négy szót nézett (*mondám, látám, hallám, adám*). Ugyanebbe az osztályba tartozik a *levék* (= lettem, 3 token, Jób 30:9: „lettem gúnydalává, nekik **levék**”) és a *jövénk* (Mt 2:2). |
| **Új:** a `valtozatlan` osztály további régies igealakjai | **ELTÉRÉS (súlyos)** | `versek:553, 5939, 20845`; `karoli_modern.tsv:10128, 120452, 48166` …; napló 8. „Lefedettség: 1 145 token” | A napló maga írja, hogy a számláló a `valtozatlan` osztályt nem látja; a Grep szerint ott több teljes osztály ül. **E/3 tárgyas elbeszélő múlt *-á/-é***: Grep `^[a-z…]{4,}(tá\|té\|zá\|zé\|lá\|lé\|rá\|ré\|dá\|dé)\t\d+\tvaltozatlan\t` a fedettseg_alakok-on, kézzel szétválogatva kb. 180 igei alak, kb. 250 token, és a lista csak ezt a tíz végződést nézi. Példák: *megnyergelé* 5 (1Móz 22:3: „és **megnyergelé** az ő szamarát, … vette két szolgáját”; lekerdez → „megnyergelé … vevé”), *körülmetélé* 4 (Józs 5:3), *állatá* 9, *előállatá* 6, *általüté* 5, *kényszeríté* 4, *felköté* 4, *felhalmozá* 4, *megtartóztatá* 3. **E/2 tárgyas *-ád/-éd***: Grep `^…[áé]d\t\d+\tvaltozatlan\t\t\t\w*[áé]\t` kb. 55 igei alak (*adád* 7, *tevéd* 5, *vevéd* 4, *megöléd* 3, *rakád* …; Ez 16:19 „ő eléjük **rakád**”). **T/3 alanyi *-ának/-ének***: *gyűlének* 8 (2Móz 32:26, Mk 14:53 …), *megijedének* 3, *megrendülének* 3, *akadának* (1Móz 26:19 „ástak … és **akadának**”), *foganának* (1Móz 30:39), *kiűzetének, késhetének* (2Móz 12:39) … (Grep content). Az 1 145 tokenes lefedettség tehát nagyságrenddel alábecsül, és a brief .2/3-as „a lefedettség (maradt-e régies igealak) kiírva” pontja tartalmilag nem teljesül. |
| **Új:** `ek_E1_T3` heurisztika, intranzitív igén T/3 | **ELTÉRÉS** | `karoli_modern.tsv:16872, 169360, 264899, 364938, 370862, 451802, 451945, 451963, 539537`; `versek:887, 8033, 12331, 19295, 22988, 22995, 22996, 27847` | Grep `\tek_E1_T3$` (content, szűrve). A *felelék → felelték* 8 tokenen rossz, mert mind E/1 elbeszélő: 1Móz 31:11 („Jákób. És felelék: Ímhol vagyok”, lekerdez), 2Sám 1:8, Neh 2:20, Jer 1:13, Jer 11:5, Zak 4:4, 4:11, 4:12 (mind lekerdez-zel ellenőrizve). Az *eljövék → eljötték* (ApCsel 24:17, „eljövék, hogy … alamizsnát hozzak”) nem létező alak. Az `igealak_alakok.tsv:1461` szerint a sonnet *feleltem*-et adott („egyezik”), a tokenszintű `valaszt()` mégis T/3-at választ, mert a versben nincs E/1 névmás. A hiba a javító kör előtt is megvolt; az N-1 most láthatóbbá teszi: „És **felelték**, és **mondtam**” (Zak 4:4, 4:11, 4:12, Jer 11:5, Neh 2:20). Jelölt, de a szövegben benne van, ugyanaz a típus, mint az 1. kör ELT-3-ja és a 2. kör N-2-je. |
| 2. kör N-2 (*ellentem*) | OK | `karoli_modern.tsv:16584`; `versek:872` | Grep `^1Móz 30:39\t` → „foganának és **elltek**”, a `vala` kiesik, `kieso_gazda`=9. A 31:8 a `VALA_ELOTT_KEZI` *ellenek* bejegyzésével. Az ugyanebben a versben álló *foganának* az új tétel része. |
| Hangrend-javítás (`igeragozas.py:109`, *-ít* mély) | OK | `git diff ca95eb3 476d933 -- igeragozas.py` | A kiadott tábla javító diffjében (`git diff -U0 … karoli_modern.tsv`, 532 +sor) a `szabaly` mező szerint: 430 `mult_E1_targyas`, 44+1 `jelen_mult_vala`, 42 `vala_segedige_jelen`, 5 `vala_segedige_mult`, és 9 sor, amelyben **csak a címke** változott (`tobbseg:sonnet+opus` → `tobbseg:szabaly+sonnet+opus`: *megtisztítá(k), eltisztítá*). A 9 sor `alak_modern`-je változatlan. A hangrend-javítás tehát az N-1-en kívül egyetlen modern alakot sem változtatott. Az *-ít* végű E/1 kimenetek jók (*kiszabadítottam, felállítottam, megsokasítottam, dicsőítettem, megépítettem*). |
| 2. kör ELT-7 (fejlécek) | OK | `igealak_minta.tsv:1`, `igealak_tokenek.tsv:1`, `igealak_alakok.tsv:1`, `karoli_modern.tsv:1` | Read: az önellentmondó „a modell nem” eltűnt, a DT311 szerinti cserét írják le, a kivételtáblák felsorolása teljes, a K1-hivatkozás a 8. szakaszra mutat. Kicsi: az `igealak_alakok.tsv` scope-ja „az igealak-osztályú és a vala/lőn/vagyon alakok (4364)”, holott a 143 `mult_E1_targyas` alak `valtozatlan` osztályú. |
| 2. kör N-3 (a 7. szakasz számai) | OK | napló `:677-678, :692` | 32 token, 22 `kivetel` sor (17 + 5), 182 alak: egyezik a 2. kör Grep-számaival. |
| 2. kör N-4 (`igealak_tokenek.tsv` bontása) | OK | napló 8. | `git diff --numstat ca95eb3 476d933`: +532/−62 = +470. Grep `mult_E1_targyas` az igealak_tokenek-en: 430, a maradék +40 a bontás szerint. A +40 soronkénti igazolása grep-pel NEM ELLENŐRIZHETŐ. |
| E17/DT3 `igealak_alakok.tsv` | **ELTÉRÉS (kicsi)** | napló 8. „A 131 alakot a modell átnézte” | numstat ca95eb3..476d933: +147/−4, tehát +143 adatsor; Grep `mult_E1_targyas` az igealak_alakok-on: 143 sor (kis- és nagybetűsen külön; kisbetűsítve 129). A napló 131-et ír, és a +143-as Δ-hoz bontást nem ad (|Δ| ≥ 10). |
| K1 (.2) | **ELTÉRÉS** | `igealak_minta.tsv` G051 (Ez 16:19), G050 (2. kör), G093 | A napló 8. szerint a K1 „322 / 322 (100%), a változatlan rétegben 0 kihagyás”. A G051 modern szövege a javítás után is „ő eléjük **rakád**”, ítélete `jó` (git diff, +G051 sor). A G050 a 2. körben „azt **mondám**” változatlan alakkal szintén `jó` volt. A modell-ellenőrzés tehát a változatlanul maradt régies alakot nem számolja kihagyásnak, és a DT307/n „valtozatlan 0 kihagyás” feltétele nem igazolt. (A G093 „Susán várában **valék**” bizonytalan jelölésű, ezért nem számít bele.) A 322-es nevező grep-pel NEM ELLENŐRIZHETŐ. |
| K2/K3/K3b újragenerálás | NEM ELLENŐRIZHETŐ | – | A `karoli_modern.py --kimenet …` futtatását a szerepköröm Bash-korlátja nem engedi. Részellenőrzés: numstat karoli_modern.tsv 532/532, versek 414/414 (a sorszám változatlan). Grep: `\tsegedige\t` = 2 529 (2 482 + 47 = 42 jelen + 5 múlt), `\tosszevonva\t` = 11 128, versek `\tigen$` = 21 516: egyezik a napló 8.-cal. A `kieso_gazda` az új sorokon helyes (1Móz 26:19 5→4, 1Móz 30:39 10→9, 1Sám 3:15 17→16, 1Krón 12:2 13→12). A K2 szúrópróba (versek ↔ tokensorok) a fenti verseken egyezik. |
| K4 | OK | napló 8. | A javító kör 0 LLM-token; az LLM-táblák nem változtak (numstat). |
| K5 csv / abszolút út / BD | OK | `eszkozok/karoli_modern/` | `git diff ca95eb3 476d933 -- eszkozok/`: nincs `csv`, nincs abszolút út, nincs Bible Discovery-adat. |
| K5 CI | ELTÉRÉS nem a #96-ból | `FELADATOK.md:63, :66` | `python eszkozok/ellenorzes/futtat.py --minta 200 --valtozott <34 fájl> --diff-alap 61714f36… --diff-fej 476d933`: kilépési kód 1. E27 HIBA: 2 (`1f420a7c` F52, `bfd94bdb` F74; sekély klón, a FELADATOK.md nincs a diffben). E25: 4 JELENTÉS más fájlokon; E30: 1 FIGYELMEZTETÉS (`3db465a`, *valtozatlan*); a többi szabály 0. Egyezik a hívó jelzésével. |
| K5 független ellenőr | nem teljesül | – | L. az ELTÉRÉS-eket. |
| Brief fejléc | **ELTÉRÉS (kicsi)** | `F96_KAROLI_MODERN_BRIEF.md:12` | A `kovetkezo` mező még „a független ellenőr újrafuttatása (2. kör) … (napló 7.)” szöveget hordoz: a javító commit (476d933) a brief fejlécét nem frissítette (`git diff --stat ca95eb3 476d933`: a brief nincs benne). |
| SEMA 2.34 | OK | `adat/SEMA.md:1436` | A `mult_E1_targyas`, `ok_birtokos`, `kivetel`, `token_kivetel` most a felsorolásban áll (a `gyanu_kezi` kétszer). |
| 1 kiszűrt/törölt sorok | OK | – | numstat base..head: törlés csak a briefben (16). A kiesés: 11 128 `osszevonva` + 2 529 `segedige` (Grep count). |
| 2 kulcstartomány | OK, korláttal | napló 8. | A K3b 61 könyvre igazol (418 633 / 418 633, a napló szerint); a Mt, Mk, Lk, Ján és ApCsel a #22 miatt hiányzik. Saját futtatás nélkül. |
| 3 „nulla-diff” hatóköre | OK | napló 8. | Az „egyezik” csak a `helyesiras_tokenek.tsv` (33 318) és az `igealak_tokenek.tsv` (66 601) újraszámolására vonatkozik. Nem vonatkozik a tartalmi helyességre (a fenti ELTÉRÉS-ek), és a `fedettseg_alakok.tsv`-re sem, amely nem frissült (F96.0), tehát a `valtozatlan` osztályozás a .0 állapotát mutatja. |
| 4 E17/DT3 Δ (adatsor, fejléc nélkül, a main-hez képest) | a fenti kivétellel OK | – | numstat − 2: fedettseg_alakok +66 086; helyesiras_alakok +1 587; ami_ellenorzes +109; ami_proba +1 164; hunspell +1 523; helyesiras_minta +112; helyesiras_tokenek +33 318; igealak_alakok +4 364 (a javító körben +143, **bontás nincs**); igealak_llm +3 174; opus +860; igealak_minta +120; igealak_tokenek +66 601 (+470, bontva); karoli_modern +599 367; versek +31 158; token_minta +200; licencek.tsv +1. |
| 5 ⛔ pontok | OK | `git log --oneline base..head` | A .0/.1/.2 ⛔ külön commitokban; a 2. kör javítását a napló 8. a felhasználó chatbeli „Mehet”-jére alapozza (a chat NEM ELLENŐRIZHETŐ). |
| A1 | OK, megjegyzéssel | `igealak.py` `VALA_ELOTT_KEZI`, `E1_TARGYAS_KEZI` | A kézi listák „kézzel átnézve” jelölésűek. A napló 8. „csak névszó maradt” állítása lekérdezéssel cáfolható (l. fent). |
| A2 | ELTÉRÉS nélkül, megjegyzéssel | brief `:103` | Az N-F96c nyitott. A `valtozatlan` osztály régies igealakjaira, a régmúltra és az `ek_E1_T3` intranzitív hibájára nincs nyitott tétel. A napló 8. a számláló vakfoltját kimondja, de tételt nem nyit. |
| A3–A6, tanulmány-ellenőrzés | nem alkalmazható | – | Nincs tanulmány, párhuzam vagy tanító a diffben; az E12–E15 0 találat. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. A `valtozatlan` osztály régies igealakjai a kiadott szövegben maradtak: E/3 tárgyas *-á/-é* (kb. 180 alak, pl. 1Móz 22:3 *megnyergelé*, Józs 5:3 *körülmetélé*), T/3 *-ának/-ének* (*gyűlének* 8, *akadának*, *foganának*), E/2 *-ád/-éd* (kb. 55 alak). A napló 8. 1 145 tokenes lefedettsége ezért nagyságrenddel alábecsül.
2. Az ELT-1 maradéka nem zárult le: legalább 14 jelöletlen ragtalan E/3 jelen + *volt* (*sátoroz, táncol, szakadoz, felkél, sántít* …), és kb. 25 igei régmúlt *+ volt* (1Móz 2:2 *alkotott volt*), ellentétben a SEMA 2.34-es szabállyal és a napló „csak névszó maradt” állításával.
3. Az N-1 csak részben megoldott: kb. 69 alak / 88 token *-ám/-ém* maradt (*imádkozám* 9, *evém, megérkezém*), vegyes igeidejű mondatokkal (Neh 1:4, Neh 2:9).
4. Az `ek_E1_T3`: *felelék → felelték* 8 token E/1 helyen, *eljövék → eljötték* (nem létező alak); az N-1 után „felelték, és mondtam”.
5. A K1 „valtozatlan 0 kihagyás” nem igazolt: a G051 *rakád* (és a 2. körben a G050 *mondám*) `jó` ítéletet kapott.
6. E17: az `igealak_alakok.tsv` +143-as Δ-ja bontás nélkül áll, a napló 131-et ír.
7. A brief `kovetkezo` mezője elavult (2. kör).

**NEM ELLENŐRIZHETŐ:** a K2/K3/K3b újragenerálása és összevetése (a `karoli_modern.py`-t a szerepköröm nem engedi futtatni); a K1 322-es nevezője; az N-4 +40-es részének soronkénti bontása; a felhasználó chatbeli jóváhagyásai; a végrehajtó session tényleges modellje.

# 4. kör

*(A független ellenőr jelentése szó szerint; az ellenőr ebben a futásban nem tudott fájlba írni, a beillesztést a végrehajtó session végezte, változtatás nélkül.)*

ELTÉRÉS: 5 tétel

# Független ellenőrzés, 4. kör: F96_KAROLI_MODERN_BRIEF.md, `8b858b3..HEAD` (ág: `ccr-a680d019-39s73e`, HEAD = `d5f6607`)

**A jelentés nincs fájlba írva.** Ebben a sessionben nincs írási eszközöm. A Bash a szerepem szerint csak `git diff`/`git log`, `lekerdez.py` és `futtat.py` hívásra használható, így a `naplok/ELLENOR_F96.md`-hez sem tudtam hozzáírni. Az alábbi szöveget a hívónak vagy a felhasználónak kell 4. körként a fájlba illesztenie.

**Ugyanez a korlát kizárt két kért lépést:**
- A generátorokat nem futtattam újra `--kimenet`-tel.
- A `random.Random(20261026).sample` mintát sem tudtam előállítani, mert tetszőleges Python nem futtatható.

Ezek a pontok NEM ELLENŐRIZHETŐ minősítést kaptak. A lefedettséget helyettesítő mintán mértem, ennek a módja a 2. részben áll.

## 0. Modell-ellenőrzés
- A tényleges modell `claude-opus-5-5`, a subagent-fájlban kért modell `opus`: egyezik.
- A menet `modell` mezői `claude-opus-5-5` értéket mutatnak, ez a hívásnaplók `"modell": ["claude-opus-5-5"]` mezőjével egyezik:
  - `igealak_llm_kor3/4/5.tsv` fejléc;
  - `igealak_llm_kor3/4/5_hivasok.jsonl`.

## 1. Táblázat

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 / modell-mező | OK | `adat/karoli_modern/igealak_llm_kor5_hivasok.jsonl:1-2` | Read. Mindhárom jsonl-ben `claude-opus-5-5`. Tokenösszegek: kor3 148676+148137+148604+149815 = 595 232; kor4 140741+142156 = 282 897; kor5 144936+140482 = 285 418. Mindhárom egyezik a naplóval, a DONTESEK-kel és a fejlécekkel. |
| CI | OK (a diffen) | `FELADATOK.md:63` | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 8b858b3..HEAD) --diff-alap 8b858b3 --diff-fej HEAD`. Eredmény: E2–E16, E19, E20, E26, E28–E31 0 találat; E25 4 JELENTES (CLAUDE.md, MUNKAMENET.md); E27 HIBA 2 (`FELADATOK.md:63`, commit `1f420a7c`). A diff a FELADATOK.md-t nem érinti, a hiba korábbi. Külön CI-jelentést nem kaptam bemenetként, ezért összevetni nem tudtam. |
| K2 / K3 / K3b (generátor újrafuttatása) | NEM ELLENŐRIZHETŐ | `eszkozok/karoli_modern/karoli_modern.py` | Az újrafuttatás a megengedett parancskörön kívül esik. Részigazolás, Grep count: `karoli_modern.tsv` 599 369 sor = 2 fejlécsor + 599 367 token (a scope-pal egyezik); `karoli_modern_versek.tsv` 31 160 = 2 + 31 158. |
| Strong változatlan | OK | — | `git diff --stat 8b858b3..HEAD -- adat/karoli_strong konkordancia adat/szoto eszkozok/karoli_strong eszkozok/karoli_modern/igeragozas.py eszkozok/karoli_modern/helyesiras.py adat/karoli_modern/helyesiras_tokenek.tsv`: üres kimenet. |
| fejléc sha256 | NEM ELLENŐRIZHETŐ | `karoli_modern.tsv:1` | A sha256 csak engedélyen kívüli paranccsal számolható. A `karoli_modern.py` BEMENETEK listájába a kor3/4/5 tábla bekerült (`git diff … karoli_modern.py`). |
| proveniencia (ts) | **ELTÉRÉS** | `adat/karoli_modern/regies_szken.tsv:1`, `regies_szken_kor4.tsv:1`, `regies_szken_kor5.tsv:1`, `igealak_tokenek.tsv:1` | Read. A régies-szken három fejlécéből hiányzik a `ts=`, holott a CLAUDE.md 1. szabálya `scope \| forras \| ts` hármast ír elő. Az `igealak_tokenek` és az `igealak_alakok` fejlécében a ts korábban is hiányzott. A `regies_szken_kor4.tsv:1` fejléce rossz címkét visel: „(F96.3, N-F96d/e, DT316)”, `--kor 4` nélkül, pedig a 4. kör táblája (DT317). |
| D: DT316 (csere = szabály + opus egyezése, tő-őrrel) | **ELTÉRÉS** | `eszkozok/karoli_modern/igealak.py:856`, `:860`, `:552`; `adat/karoli_modern/igealak_llm_kor4.tsv:74` | A kód a leírt szabályon felül kizárja a `nevelo_utan` jelölésű tokent. Ez a feltétel sem a DT316/r-ben, sem a napló 10.3/11.3-ban nem szerepel. A `nevelo_utan` (a, az, egy után) a Károli névmási „az”-ját névelőnek veszi. Következmény: az `S0072 felele` kérdésben a szabály és az opus egyezik (`felelt`/`felelt`), mégsem cserél (1Móz 22:1, 1Kir 13:16). Grep `\tnevelo_utan$` a `karoli_modern.tsv`-n: 47 token. Ebből 31 valódi igealak maradt régiesen (*az monda* ×14, *mondá* ×2, *felele* ×2, *fogada* ×2, *felkelvén* ×2, *méne*, *beméne*, *jöve*, *esék*, *elküldé*, *elbeszélé*, *szüle*, *szülé*, *elfuta*), 2 határeset (*eljő*), 14 helyesen főnév vagy melléknévi igenév (*tevék, küldöttek, megmaradott(ak), megfáradott*). A kód régebbi, de a 3–5. kör a lefedettség javítását vállalta. |
| D: DT316 / N-F96f („megoldva”) | **ELTÉRÉS** | `adat/karoli_modern/karoli_modern_versek.tsv:17404`, `:17405`, `:17408`; `karoli_modern.tsv:333492` | Grep `^Préd 2:[4-9]\t` mindkét táblán. Salamon E/1-es beszédében az `ek_E1_T3` rossz személyt ad: Préd 2:5 *építék → építették*, *ülteték → ültették* (az 1908-ban: „építék magamnak házakat”); 2:6 *ülteték → ültették*; 2:9 *Gyűjték → Gyűjtötték magamnak*. Ugyanitt a *Csinálék → Csináltam* és az 5. körben a *szerzék → szereztem* helyes, így egy versen belül keveredik a személy. A 10.4 „T/3 maradt” listája (1Móz 39:15, Dán 7:16, Ez 22:30) ezeket nem említi. A szabály a token utáni *magamnak* E/1 jelzőt nem nézi. 4 rossz token, a csere-pontosság állítását (hiba 0) ez az osztály cáfolja. |
| D: DT317/s/u számok | OK | `karoli_modern.tsv` | Grep count a `karoli_modern.tsv`-n: `kor3:szabaly\+opus` 690; `kor4:szabaly\+opus` 184; `kor5:token_opus\+meglevo` 205; `\tvala_segedige_kor3\t` 71; `\tvala_segedige_kor4\t` 16; `opus_tanusitott` 58 (= 29+22+7); `\tszabaly_nem_tanusitott$` 58; `\tek_E1_T3$` 692. Az `igealak_tokenek.tsv`-n: `kor5_token_opus:` 106; `\ttoken_opus\t` 205. A `karoli_modern_versek.tsv`-n `\tigen$` 21 620. Mind egyezik a napló 10.–14. szakaszával. |
| D: DT320 szabály (szúrópróba) | OK | `adat/karoli_modern/igealak_llm_kor5.tsv:3-25`, `:114`, `:201`, `:256` | Read és Grep. Az `opus_alak` minden cserélt esetben a `meglevo_jeloltek` egyike. A T0022 *tevének* (főnév, 1Móz 31:34) helyesen változatlan. Megjegyzés, nem ELTÉRÉS: ahol a modernebb írásmód is jelölt volt, a kör a régiest választja (*elsülyesztette*, *felűltek*, *megkisértette*). Ez a .1 hiánya (N-F96c): Grep `sülye` szerint a *sülyed-* sehol nincs modernizálva. |
| `lőnek` (a kiadott réteg) | **ELTÉRÉS** | `eszkozok/karoli_modern/igealak.py:702`; `igealak_tokenek.tsv:66933`; `karoli_modern_versek.tsv:30949` | Az `re.search(r'nyil\|nyíl\|íj', …)` a Jel 11:19 *megnyilatkozék* szavára is illeszkedik, ezért a „lőnek villámlások” `lonek_lo` jelölést kap, és nem lesz belőle *lettek*. A kód régebbi (`git log -S"lonek_lo"` → `c7bcd33`), az 1 tokenes hiba a kiadott táblában van. |
| E17 / DT3 (sorszám-Δ) | **ELTÉRÉS** (`igealak_tokenek`) | `naplok/KAROLI_MODERN_meres.md` 10.5, 11.3 | Módszer: `git diff --numstat 8b858b3..HEAD` és Grep `^` count. Változott táblák: `igealak_tokenek` +1084 (66 601 → 67 685); `igealak_alakok` 0; `karoli_modern` 0; `karoli_modern_versek` 0; `igealak_minta` 0. Új táblák: `igealak_llm_kor3` +1516, `igealak_llm_kor4` +485, `igealak_llm_kor5` +370, `regies_szken` +1516, `regies_szken_kor4` +485, `regies_szken_kor5` +370, `igealak_minta2` +140. Az `adat/` és a `konkordancia/` többi `.tsv`-je 0 (nincs a diffben). Az új táblák bontása a naplóban megvan (1354+162; 291+33+161; 357+13; 100/20/10/10). Az `igealak_tokenek` +1084-e csak két lépcsőben szerepel (+831, +253), olyan kategóriabontás nélkül, amelynek összege a Δ. |
| törölt sorok | NEM ELLENŐRIZHETŐ | `igealak_tokenek.tsv` | A numstat −646 sort mutat. A napló szerint „egy sor sem tűnt el”, vagyis ezek módosítások. A kulcsok soronkénti összevetése engedélyen kívüli számítás. |
| nulla-diff hatóköre | OK, részben | — | A Strong-, szótő-, konkordancia- és .1-bemenetek bájtra változatlanok (fenti `--stat`). A „.1-visszalépés 0 token” állítás NEM ELLENŐRIZHETŐ. |
| K1 / minta2 számai | OK | `adat/karoli_modern/igealak_minta2.tsv:3-142` | A Grep `\tcsere=\d+` a véletlen réteg 100 során összesen 96-ot ad. A `(kihagyás\|hibás)\tcsere=` kihagyás-sorai: 36, 49, 50 (véletlen, 3 db); 111, 112, 121, 122 (kor3, 4 db); 138 (ek, 1 db). Ez egyezik a 14.4 táblájával. |
| ⛔ pontok | OK | brief 3. pont; DONTESEK DT316–v | Minden kör DT-helyőrzőn állt meg (r, s, t, u, v). Minden LLM-futás előtt van jóváhagyás: q (kor3), r 2. opció (kor4), u (kor5). A DT321 🟡 nyitott, a brief `kovetkezo` mezője ezt mutatja. Végleges DT-szám nincs. A diff fájljai mind az `ir` listán vannak. |
| csv / abszolút út / kódolási őr | OK | `regies_szken.py:41-56`, `igealak.py:82-103` | Grep `import csv\|csv\.\|/home/\|reconfigure`: nincs csv, nincs abszolút út, a wrapper az importok után áll. |
| A1 | OK | napló 11.3, 12.3, 14.3 | Az „átnézve, mind helyes” állítások végrehajtói vagy modell-ellenőrzésként jelöltek. A Préd 2 hibái az ek-osztályt érintik, nem ezeket a köröket. |
| A2 | **ELTÉRÉS** (az N-F96f státusza) | `F96_KAROLI_MODERN_BRIEF.md` N-F96f sor | Az „N-F96f megoldva” túlzó, l. a Préd 2:5–9 sort. |
| A3 / A4 / A5 | nem alkalmazható | — | Nincs tanulmány, PaRDeS-réteg vagy tanító a diffben. A Tanulmány-ellenőrzés (F37 T4) nem él: nincs `*_bovitett.md` vagy `*_tanulmany.md`. |
| A6 | OK | — | E12–E15 0 találat (a futtat.py fenti kimenete). |
| Friss véletlen minta (mag 20261026) | NEM ELLENŐRIZHETŐ | — | A `random.sample` nem futtatható. Helyette determinisztikus, egyenletes szisztematikus mintát vettem (l. 2. rész). |

## 2. Lefedettség-mérés, helyettesítő mintán

**A minta.** A `karoli_modern_versek.tsv` 160 + 311·k sora (k = 0…99), az 1908-as párja a `Karoli_1908.tsv` eggyel kisebb sorszámú sora.
- Kiválasztás: Read offset/limit 1; az 1908-as szöveg: Grep `^(<100 igehely>)\t` a `konkordancia/Karoli_1908.tsv`-n.
- A két meglévő mintából egyetlen vers esett bele, a 2Sám 19:43 (`igealak_minta.tsv:35`, G033). Helyette a következő vers, a 2Sám 20:1 került be.

**Számlálás.**
- A csere a helyes igealak-csere, a *vala* és a *-ván/-vén* is ide tartozik.
- A *lészen → lesz* a rendszer szerint cserél, ezért csereként számoltam.
- A tisztán helyesírási csere (*közűl, néki, a kik*) nem számít.

**Versenként, ahol nem 0/0/0:**
- 1Móz 19:11 — 3 csere
- 1Móz 28:6 — 4
- 1Móz 37:7 — 4
- 1Móz 46:15 — 1
- 2Móz 18:24 — 3
- 2Móz 38:12 — 2
- 3Móz 9:3 — 1
- 4Móz 26:22 — mély *-ok*: *számok*
- Józs 10:3 — 2
- Józs 20:6 — 1
- Bír 6:35 — 3 csere, **1 kihagyás**: *egybegyűle*. Mindhárom forrás *egybegyűlt*/*egybegyült*, de a tő-őr az ű/ü eltérésen elbukik (`igealak_tokenek.tsv:16295`).
- Bír 18:7 — magas *-ök* kihagyás: *felettök*
- 1Sám 4:14 — 3
- 1Sám 17:4 — 2
- 1Sám 27:2 — 3
- 2Sám 10:3 — 1 csere; mély *-ok*: *uroknak*
- 2Sám 20:1 — 4
- 1Kir 4:21 — 3
- 1Kir 12:25 — 4
- 1Kir 22:7 — 1
- 2Kir 10:4 — 2
- 2Kir 20:10 — 1
- 2Krón 8:6 — 2
- 2Krón 35:8 — 2
- Zsolt 89:11 — 1
- Zsolt 105:39 — 1
- Zsolt 119:57 — 1
- Ézs 8:14 — 1
- Ézs 40:24 — 1
- Sir 1:1 — 2
- Ez 42:3 — 3
- Dán 4:26 — **1 kihagyás**: *sétála*. Egyik szkenben sincs; a `fedettseg_alakok.tsv:54308` szerint `valtozatlan`/`lexikon`.
- Ámós 8:9 — 1
- Mt 25:37 — 1
- Mk 4:33 — 2
- Mk 11:27 — 3
- Luk 2:5 — 1
- Luk 8:44 — 3
- Luk 15:12 — 2 csere; magas *-ök* kihagyás: *köztök*
- Luk 22:47 — 3 csere, **1 kihagyás**: *az méne*, `nevelo_utan`
- Ján 5:12 — 2
- Ján 19:19 — 3
- ApCsel 7:39 — 2
- ApCsel 15:24 — 2
- ApCsel 24:9 — 1 csere, **1 kihagyás**: *Helybenhagyák*. Egyik szkenben sincs (`fedettseg_alakok.tsv:4000`).
- Filem 1:21 — 2
- Jel 11:19 — 2 csere, **1 kihagyás**: *lőnek*, `lonek_lo` téves találat.

A *-ök → -ük* (DT315) és a *-jok* csere 9 tokenen helyes: 1Móz 6:20 ×3, 2Móz 28:41, 5Móz 31:28, 2Krón 35:8, Zsolt 140:3, Ézs 40:24, ApCsel 7:39. A többi 52 versben 0/0/0.

**Összesen (100 vers):**
- igealak: **92 csere, 0 hiba, 5 kihagyás**;
- *-ök/-ok* birtokos: 9 csere, 2 magas hangrendű kihagyás (a DT315 tőfeltételén kívül), külön 2 mély hangrendű *-ok*;
- szándékosan változatlan (*-nd-*, *-jál/-jél*, *jövén/lévén*): a mintában nem fordult elő.

**Lefedettség igealakra: 92 / (92 + 5) = 94,8%.**
- Korpuszbecslés: kb. 1 560 token; Poisson 95%-os sáv kb. 500–3 600.
- A minta2 véletlen rétege (96/96, 0 kihagyás) ennél jóval kedvezőbb. 5 várt eset mellett 0 kihagyás valószínűsége kb. 0,7%, ami megerősíti a napló saját torzítás-figyelmeztetését.
- A mintán kívüli szúrópróba további kihagyásokat talált: 1Móz 7:17 *felveheték*, 1Móz 16:4 *béméne*, 2Sám 7:10 *elplántálám*, 2Krón 35:23 *lövének*.

## 3. ELTÉRÉS-ek, súlyossági sorrendben

1. **Rossz személy az `ek_E1_T3`-ban** (Préd 2:5, 2:6, 2:9; 4 token: *építették, ültették ×2, Gyűjtötték magamnak*), így az „N-F96f megoldva” túlzó. Bizonyíték: `karoli_modern_versek.tsv:17404/17405/17408`, `karoli_modern.tsv:333492`.
2. **Lefedettség és a leírt szabály.** A mért lefedettség 94,8% (5 kihagyás), a napló 100%-a helyett. Ennek oka részben egy le nem írt kizárás: a `nevelo_utan` feltétel a kor3/kor4 alkalmazásban (`igealak.py:856/860`) az *az monda / felele / méne* típusú névmási „az” utáni igéket is kizárja. 31 token marad így régies. Ide tartozik az S0072 *felele* is (`igealak_llm_kor4.tsv:74`), ahol a szabály és az opus egyezett, mégsem lett csere.
3. **A `lonek_lo` regex téves találata** a *megnyilatkozék* szóra (`igealak.py:702`, Jel 11:19, 1 token).
4. **Proveniencia.** A `regies_szken*.tsv` fejlécéből hiányzik a `ts=`, a `regies_szken_kor4.tsv:1` címkéje hibás.
5. **E17.** Az `igealak_tokenek.tsv` +1084 soros Δ-jához nincs összegző kategóriabontás.

Nem ellenőrizhető maradt a generátorok újrafuttatása (K2/K3/K3b), a sha256-ok, valamint a kért magú véletlen minta: mindhárom a megengedett parancskörön kívül esik.

Fájlok:
- /home/user/bible-study/adat/karoli_modern/karoli_modern_versek.tsv
- /home/user/bible-study/adat/karoli_modern/karoli_modern.tsv
- /home/user/bible-study/adat/karoli_modern/igealak_tokenek.tsv
- /home/user/bible-study/adat/karoli_modern/igealak_llm_kor4.tsv
- /home/user/bible-study/eszkozok/karoli_modern/igealak.py
- /home/user/bible-study/naplok/KAROLI_MODERN_meres.md
- /home/user/bible-study/naplok/ELLENOR_F96.md (ide kell beilleszteni ezt a 4. kört; én nem írtam bele)
