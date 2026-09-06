# Görög oldal erősítése — lehetséges irányok (dokumentálva, döntés nélkül)

Készült: 2026.09.05, a Motívumlexikon-pilot (ISTENTISZT-001) munkája közben szerzett tapasztalat alapján. Ez a fájl kizárólag a lehetőségek rögzítésére szolgál — egyik irány sem lett elindítva vagy jóváhagyva. A folytatás Basesoft külön kezdeményezésére történik, hasonlóan a `motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md` már bevált mintájához.

## Háttér

A héber oldalon a projekt már két mélységi szinttel dolgozik: `Strong_szotar.tsv` (rövid gloss) + `BDB_teljes_unabridged.tsv` (teljes, sense-szintre bontott szótár). A görög oldalon eddig csak a rövid Strong-gloss szintje volt szisztematikusan használva — a `TBESG.txt` (Abbott-Smith/Middle Liddell alapú, sense-szintű) létezik és dokumentált (`TBESH_TBESG_README.md`, 2026-09-01 óta), de eddig egyetlen tényleges study/motívum sem használta ki szisztematikusan.

## 1. lehetőség — LXX-híd 2 ismert hibájának javítása

Mit old meg: a `LXX_kivonat_Zsoltarok.tsv`-ben talált két konkrét hiba (2026.09.05, a "Segítségül hívni" motívum auditja során):

* Zsolt 116:4: ἐπεκαλεσάμην tévesen G4506-tal (ῥύομαι) címkézve
* Zsolt 116:17: a görög kivonat hiányos, a vers második fele (a "segítségül hívom nevét" tagmondat) nincs a kinyert adatban

Jellege: gyors, konkrét, pontosan körülhatárolt javítás — nem feltáró munka, a hiba már azonosítva van.
Korlát: csak ezt a két konkrét esetet oldja meg — nem javítja a mögöttes, rendszerszintű okot (ha van ilyen más zsoltároknál is hasonló hiba, azt nem deríti fel).

## 2. lehetőség — TBESG strukturált TSV-vé alakítása

Mit old meg: a `TBESG.txt` jelenleg nyers, HTML-szerű jelölésekkel teli szöveg (`<b>`, `<BR />`, `<ref='...'>`). Egy tisztított `TBESG_strukturalt.tsv` (pl. oszlopok: Strong-szám | Alsor-jelölő | Sense-szám | Angol gloss | Idézett igehelyek | Forrás [AS/ML]) a BDB-feldolgozáshoz hasonló minőségű, gyorsan lekérdezhető adatot adna.

Jellege: nagyobb, egyszeri feldolgozási munka (script-alapú parszolás, hasonlóan a `eszkozok/tahot_karoli_kulcs_generalas.py`-hoz vagy a BDB-import korábbi munkájához), utána tartós, ismétlődő haszonnal minden jövőbeli study számára.
Korlát: a TBESG maga is csak egy "Brief" (rövidített) lexikon — ez a feldolgozás nem ad mélyebb tartalmat, csak gyorsabban hozzáférhetővé teszi a már meglévőt.

## 3. lehetőség — LSJ (Liddell-Scott-Jones) beszerzése, a BDB párjaként

Mit old meg: a BDB a héber oldalon teljes, kibontott (unabridged) szótár. A TBESG ezzel szemben saját maga is csak rövidített lexikon a görög oldalon — nincs jelenleg a göröghöz olyan mélységű forrás, mint a BDB a héberhez. Az LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) a klasszikus filológia standard, teljes ógörög szótára — közkincs (public domain), digitalizált változatban elérhető (pl. Perseus Project, CC BY-SA vagy hasonló nyílt licenc).

Jellege: a legnagyobb léptékű az 5 közül — új forrás beszerzése, licenc-ellenőrzés (hasonlóan ahhoz, ahogy a BDB-nél és a TBESH/TBESG-nél is történt), majd feldolgozási/lekérdezési mechanizmus kialakítása.
Korlát: LSJ elsősorban klasszikus (nem koiné/újszövetségi) görögre fókuszál — Újszövetség-specifikus árnyalatokra (pl. szemita hatás, LXX-beágyazottság) a TBESG/Abbott-Smith jellemzően relevánsabb marad; az LSJ inkább kiegészítő, nem helyettesítő szerepet töltene be.

## 4. lehetőség — A többsoros Strong-szám kérdés lezárása

Mit old meg: egy alap Strong-szám (héberre és görögre is) gyakran több TBESH/TBESG-sort kap (pl. H7121 → 4 alsor: G/H/I/J, mind ugyanazt az alap sense-listát ismétli, eltérő súlyponti gloss-szal). A `TBESH_TBESG_README.md` már jelzi: nincs még véglegesített konvenció, hogy egy study-nál a teljes alsor-készletet nézzük-e át, vagy csak az elsőt/"fő"-t (a 2026.08.31-i pilot az első alsort használta, `grep -m1`-lel, de ez "nem az egyetlen lehetséges konvenció").

Jellege: tisztán módszertani döntés, nem adatfeldolgozás — gyors lezárható, ha egyszer napirendre kerül.
Korlát: amíg nyitva marad, két különböző study következetlenül kezelheti ugyanazt a Strong-számot (az egyik az első alsort idézi, a másik egy eltérőt) — ez pontosan az a fajta inkonzisztencia, amit a projekt más területeken (pl. lexikai vs. tematikus fegyelem) következetesen elkerül.

## 5. lehetőség — Cross-referencia join-tábla a göröghöz

Mit old meg: a héber oldalon már van kumulatív, tanulmány-vezérelt join-tábla (`Karoli_Strong_kivonat.tsv`, jelenleg Gen 1-16 tartomány, 178+ sor) — minden study, ami egyszer már felkutatott egy héber szót/verset, hozzáadja a sorát, a következő study már nem generál újra semmit. A görög oldalon nincs ilyen ekvivalens — minden study újra a nyers `TAGNT_kivonat.tsv`-ből és `Strong_szotar.tsv`-ből (vagy most már TBESG-ből) dolgozik, a korábbi studyk görög elemzése nem gyűlik egy központi, újrafelhasználható fájlba.

Jellege: közepes méretű, de leginkább szervezési munka — maga a fájlformátum egyszerű (a Karoli_Strong_kivonat.tsv mintáját követve), a nehézség inkább a visszamenőleges feltöltésben van (mely studyk görög elemzését vegyük fel most, melyiket csak ezután keletkezőket).
Korlát: amíg kevés study használja aktívan a görög oldalt mélyen (eddig gyakorlatilag csak a mai "Segítségül hívni" pilot), a join-tábla haszna korlátozott — inkább akkor éri meg, ha a TBESG-használat (2. és 4. pont) már rendszeressé vált.

## Összegzés — függőségek a lehetőségek között

* Az 1. lehetőség teljesen független a többitől — bármikor, külön elvégezhető.
* A 2. lehetőség hasznosabbá teszi a 3.-at (egy strukturált TBESG mellett egy strukturált LSJ még könnyebben integrálható lenne egységesen), és előfeltétele az 5.-nek (a join-tábla forrása logikusan a strukturált TBESG lenne, nem a nyers szöveg).
* A 4. lehetőség tisztán döntési kérdés, bármelyik másikkal párhuzamosan lezárható, és érdemes a 2. előtt eldönteni, hogy a strukturált TSV már a helyes konvenciót kövesse.

Egyik irány sem lett elindítva. Ha bármelyiket folytatni szeretnéd, jelezd, és külön Code-prompt/terv készül hozzá.
