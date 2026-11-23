# F239 átadó — U4 (ellenőrzés) → U5 (a szerkesztő átnézése)

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820). A lépések és a számok: `naplok/F239_jelentes.md`, „U4”; a független ellenőr: ugyanott, „Független ellenőrzés — 1. ellenőrzés”.*

## Az U5 bemenete

1. **A lapnézet** az új generátor előnézetéből, nem a repó `lexikon/` lapjából (az befagyasztott régi lap). Előállítása:
   - `python.exe`-lista (egyszerre egy lapgen-futás);
   - ideiglenes, nem commitolt kerülőút: az `adat/motivum_kapcsolatok.tsv`-ben `DT-F239a` → `DT9991`, az `eszkozok/lapgen/megjelenites/md/kizart.py`-ban a `round(arany) <= KIZART_ATLAG_HATAR` ág `ValueError` helyett kihagyja az arány-mondatot (N-F239a);
   - `python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívül>` (kb. 35 mp), utána a két fájl visszaállítva (`git status` tiszta);
   - lapnézet: a `eszkozok/lektor_felulet/lapnezet.py` `epit()`-je, a `_fajl` olvasást a `lexikon/<ID>_TUDOMANYOS.md` útvonalon az előnézetre irányítva (egy kis burkoló szkripttel; a kimenet a repón kívül, a brief szerint privát artifact, világos téma).
2. **A szerkesztő elé kerülő lista** (minden tétel nyitott): `naplok/KIADAS_TEREMT-001_lektor.md` — a lektor 23 kérdése (44 tételből) és a 3/b 119 olvasói kérdése, a blokkjelekkel (a jelek a fenti lapnézet jelei: `<szakasz>·<n>`). A tételek eredete: `naplok/F239_U4_lektor_munkafajl.md`.
3. **Az F2 hamis tételei** (a próza gazdájáé, az U6-ban): K2, K9, K19, K20, K36, K47, K69, K70, K99 (`naplok/ALLITAS_TEREMT-001_itelet.md`); és az F1 egy valódi ELTÉR-sora (a 79. sor idézete, 5Móz 33:13). Ezek nem a szerkesztő döntései, hanem javítandók; a szerkesztő a listán láthatja őket.

## Mit mutat az U4 (röviden)

- F2: 102 / 9 / 16 / 1 (igazolt / hamis / vitatott / nem eldönthető); nem eldönthető 0,8%; F2-megfogás a lektor pontossági kérdésein 14/17 = 82% (küszöb 80%).
- A próza ismétlődő mintái (mechanizmusként a javítókörnek): a TR Jel 20:3 olvasata (a sárkányt zárják be, nem a mélységet; K60, K127, lektor 18., 27., 30.); „Isten megnyitja és bezárja” szenvedő igéknél (K36, lektor 17., 21.); a Jón 2:6 „felhoz” (K2, lektor 24.); felsorolás teljesnek hatva (K9, K19, K20, K69, lektor 28.); a „95” szám (K70, ellenőr, olvasó 7.).
- A 3/b zöme generált blokk: az új generátor hibái (M-CSERE, M-NYERS, M-RÁRAKÓDÁS), gazdájuk a lapgenerátor (F218a / 218c), nem a próza.

## Nyitott, gazdát kér (az integrátornál)

- A CI a fejen piros: F217 (a `nyilt_mag_export.py` kódkönyv-címkéi az új zárt értékekhez) és E41 (a 8 ELTÉR; 7 a `proza_allitas.py` hozzárendelési hibája).
- A `tanu_kinyer.py` `ps` álneve (görög zsoltárszám Károli-alakban, „Zsolt 117:24”), a Vulgata-átvezetés teszt nélkül.
- A generált index két hivatkozása a törölt `tematikus_lezart/Tehom_tematikus.md`-re.
- A kiadás feltételei változatlanok: N-F239a (218c), N-F239b (218c), a BDB-versjelentés hibája (#240); a πόντος „Pontusz” címke (N-F240a).

## Mit NEM kell elolvasni

Az `ALLITAS_TEREMT-001.md` teljes kézi listáját (248 KB; az ítélet a `_itelet.md`-ben), a lektor tétellistáját (a munkafájl elég), a független ellenőr táblájának OK-sorait.
