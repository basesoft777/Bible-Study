# A Károli-biblia szavanként az eredeti nyelvekhez kötve — mért pontossággal

*Közlemény-tervezet · Károli 1908 – Strong szóillesztés · Logosz-lexikon · DOI: 10.5281/zenodo.24141884*

Aki a Károli-bibliát olvasva azt kérdezi, milyen héber vagy görög szó áll egy magyar szó mögött, eddig nem talált
olyan szabad adatot, amely ezt szavanként, mért pontossággal megmondja. A Logosz-lexikon most szabad licenccel közreadja a Károli 1908-as szövegének szavankénti
párosítását az eredeti szöveggel: az 598 715 szópár mindegyike megmondja, melyik héber vagy görög szót fordítja az adott
magyar szó, és mi a Strong-száma.

**Hogyan készült.** A párosítást nyelvi modellek végezték, versenként, egy írott szabálykészlet szerint: mikor betoldás a
magyar névelő, hová tartozik a héber birtokos rag, mit kezdjünk a kettéírt *a mely*-vel. A modell csak azt jelölte,
melyik szó melyikhez tartozik; Strong-számot nem írt, azt a STEPBible nyílt héber és görög szövege adja. Minden választ
program ellenőrzött, hogy egy szó se maradjon ki, és egy se álljon kétszer. Mózes első két könyvét két független modell
párosította; ahol egyeztek, a pár „magas” bizonyosságot kapott.

**Mennyire pontos.** A párosítás nem hibátlan, és ezt nem is állítjuk. Azt állítjuk, hogy megmértük, és a mérés minden
számát közöljük. Nyolc rétegből húzott véletlen mintán egy harmadik, a párokat nem látó modell 95,06%-ban értett
egyet a párosítással (95%: 93,81–96,32%). A fő szavak párjait egy független, Strong-számos
Károli-kiadással is összevetettük: 98,72% egyezett (95%: 98,22–99,08%). A gyengébb pont a héber előtagok és ragok
párosítása (90,74%), és a megerősített hibákat név szerint felsoroljuk.

**Miért most.** Mert a mérés dokumentált: aki az adatot használja, tudja, mennyire bízhat benne, rétegenként és
kapcsolattípusonként. A következő kiadás a feltárt hibákat javítja, és ugyanazzal a módszerrel újra mér; a minőségi
célját előre rögzítettük.

**Kinek.** Bibliaolvasóknak, akik a Károli egy szava mögött az eredetit keresik; kutatóknak, akik a magyar bibliai
szóhasználatot a héber és görög szöveggel együtt vizsgálják; fejlesztőknek, akik szavanként kulcsolt, szabad magyar
bibliai adatra építenének. Ugyanezek a párok a Károli modernizált szövegén is elérhetők
(https://doi.org/10.5281/zenodo.24141950).

Az adatkészlet CC BY 4.0 licenccel szabadon felhasználható: https://doi.org/10.5281/zenodo.24141884
