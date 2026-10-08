---
feladat: 83
cim: "Jób 38–42 Károli–héber versmegfeleltetés előkészítése a #22 Jób-futása előtt"
kod: JOB_VERSBEOSZTAS
tipus: feladat
fazis: 1
modell: opus
allapot: fut
ag: claude/f83-job-versbeosztas
ad: "Jóváhagyott Jób 38–42 versmegfeleltetés (1:2 / 2:1 esetekkel), a három ellenőrzés eredményével; a Jób bekerülhet a VERSBEOSZTAS_JOVAHAGYOTT-ba"
kovetkezo: "⛔ a kézi megfeleltetési táblázat előtt (a felhasználó jóváhagyása). Nyitott a befogadáskor: (a) az 1. ellenőrzés forrása — a nyers TAHOT-fájl nincs a repóban, csak a kivonat; a Macula_heber_Job.tsv (MT/WLC) vagy a STEPBible-fájl letöltése (külön engedély); (b) az 1:2 / 2:1 támogatásáról döntés DT-F83a helyőrzővel (l. naplok/F22_versbeosztas_jovahagyas.md, Jób-sor); (c) az N-F41g (Jób 38–41 MT-számozás a BSB-ben) átfedése: a jelentés lezárja-e, vagy külön tétel marad. A #22-vel nem fut párhuzamosan (KIZAR: f22/versmegfeleltetes_kezi.tsv)."
fugg: []
nem_fugg: [22]
olvas: [konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Macula_heber_Job.tsv, f22/versmegfeleltetes.tsv, naplok/F22_versbeosztas.md, eszkozok/karoli_strong/versbeosztas.py, eszkozok/tahot_karoli_kulcs_generalas.py]
ir: [naplok/F83_Job_versbeosztas_jelentes.md, f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv, naplok/F22_versbeosztas_jovahagyas.md]
---

# F83_JOB_VERSBEOSZTAS_BRIEF.md

A Jób-megfeleltetés tartalmi döntés. Azt kell eldönteni, melyik Károli-vers melyik héber vershez tartozik, az 1:2 és 2:1 összevonásokkal együtt. Ez a naplok/F22_versbeosztas_jovahagyas.md-be kerül, a te jóváhagyásoddal. Nem fér bele egy futtató session mellékszálába, és a „Egy session = egy feladat” szabály is a külön menet mellett szól.

* A CLAUDE.md is ezt a sorrendet írja elő. A Jób-futás (#22) előtt figyelmeztetést kér a TAHOT-hiányra. A külön előkészítő feladat ezt a figyelmeztetést intézi el formálisan, és nem kerülgeti meg.

A Jób-briefben három dolgot érdemes első lépésként ellenőriztetni, mert a jelentés ezeket kijelentette, de a repóból nem igazolta:

1. Valóban megvan-e a nyers TAHOT-fájlban a héber Jób 40:25–41:26. A jelentés szerint a hiba a kulcsgenerátorban van, nem a nyers adatban. Ezt egy lekérdezéssel kell megerősíteni, mielőtt bárki kézi táblázatot kezd.
2. A Jób 42:2–9 hiánya gyanús. A 42. fejezetben a héber és a Károli számozás általában együtt halad. Ha itt is hiányzik adat, az inkább a 41. fejezet hibájának továbbgyűrűzése lehet, nem önálló eltérés. Érdemes külön megnézni.
3. A Károli 40. és 41. fejezetének versszámát (28 és 25) a Károli-forrásból kell újra megszámolni, nem a detektor kimenetéből átvenni. Ezekre a számokra épül az egész megfeleltetés.
