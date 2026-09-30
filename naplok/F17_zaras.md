# F17 zárójelentés (FELADATOK #17; ág: `claude/macula-import`)

**Elkészült:** Macula héber (475 911 morféma-sor, commit 47db250b) és görög (N1904 137 779, SBLGNT 137 741 sor, commit 8423afe4) import, a Károli-kulcshoz (KK) kötve: `konkordancia/Macula_heber_<Konyv>.tsv` (39 könyvfájl, F17.9; 475 911 sor összesen) és `Macula_gorog.tsv` (egy fájl, 32,6 MB); illesztetlen lista (`naplok/F17_illesztetlen.tsv`, 1 531 sor, mind `javaslat`); a 87 hely (`naplok/F17_87_hely.tsv`); napló, statisztika; eszközök `eszkozok/f17/`; `datasetek.tsv` +8 sor; N31 lezárva. Licenc: CC BY 4.0; az UBS-mezők (sdbh, lexdomain, domain, ln stb.) nincsenek importálva.

**A #8 bemenete:** a 87 függő helyből **38** kap görög Strong-számos LXX-megfelelőt (F06: 39). Három sor tér el (4Móz 13:34 ×2, Préd 9:10): az F06 a KK `igehely_kjv`-t figyelmen kívül hagyta, a 87/87 egyezés közös módszerhiba volt. Új lelet: a Préd 9:10 munkalap-igehelye valószínűleg MT-számozású (a שְׁאוֹל a Macula szerint MT 9:10 = Károli 9:12).

**Leletek:** a Macula betűs `strongnumberx` kódja funkció-morfémánál nem Strong-szám (170 429 sor üres `strong`, a nyers kód `strong_x`); a `LXX_versificacios_terkep.tsv` `EGYIK_SEM` sorai megbízhatatlanok; Dán 4 KJV≠MT (34 Károli-vers `javaslat`); 44 Károli-vers eltolódás-gyanúja (Préd 5, 4Móz 30, Zsolt 13 stb.) üres értékkel.

**Nyitott (DONTESEK `DT7`, 🟡, (a)–(h)):** UBS-mezők (F24), funkció-morféma Strong leképezése, KK–terkep ütközés (1 048 vers), Dán 4, interpoláció, a héber fájl mérete (a 65 MB-os fájl az F17.9-ben 39 könyvfájlra bontva, a döntés (e) így is nyitott), szerepmátrix (SEMA 2.13) és `datasetek.tsv`, az `allapot`/Strong-jelzés külön oszlopa. Azonosító `DT7` (a `main` utolsó azonosítója DT4, a #85 DT-F16-ja DT5; a korábbi ideiglenes azonosító DT7-ra számozva, F17.12).

**Figyelem:** a `datasetek.tsv` és a `DONTESEK.md` közös fájl a #16-tal (rebase-nél mindkét oldal sorai maradnak); a `SEMA.md` 2.6 dataset-száma (#16: 18) a Macula +2 dataset miatt tovább nő.

**Ellenőrzés:** `naplok/ELLENOR_F17.md` (3 kör).
