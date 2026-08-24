# Validációs napló — Károli-Strong join-tábla

*Ennek a naplónak a célja, hogy minden jövőbeli validációs esemény (akár mintavételes,
akár teljes körű) ide kerüljön, ne szórtan a különböző README-kbe. Lásd
`Join_tabla_folyamat_magyarazat.md` a join-tábla építésének folyamatáról és a döntési
fájl 4.13 pontját az önellenőrzési mechanizmusról (KJV/ASV kereszt-ellenőrzés,
megbízhatósági jelölés).*

---

| Dátum | Igehely(ek) | Módszer | Eredmény | Megjegyzés |
|---|---|---|---|---|
| 2026.08.23-24 körül | Pro.23.1-9 | Felhasználói külső referenciával összevetve | 43/44 egyezés | 1 tudatos eltérés (23:2, Károli szabad fordítása) |
| 2026.08.23-24 körül | Act.1.1-4 | KJV/ASV kereszt-ellenőrzés | 19/19 szó, kritikai kiadás is egyezik | nincs szövegkritikai eltérés ezen a szakaszon |
| 2026.08.23-24 körül | Gen.1.2-4 | Felhasználói "régi Strong" referenciával összevetve | 12/14, majd 13/14 egyezés | 1 dokumentált kettős Strong-lehetőség (H2895/H2896) |
| 2026.08.24 | Gen.1-16 (a `Konnyu_ellenorzes_1-16_osszesito_v2.md` megerősített szavai) | Betöltés a `Karoli_Strong_kivonat.tsv` join-táblába: tartalom-alapú azonosítás + KJV/ASV kereszt-ellenőrzés (4.13 szabály), majd minden Károli-szó szigorú, teljes szóhatáros egyezés-ellenőrzése a `Karoli_1908.tsv` tényleges vers-szövegével szemben | 178 sor ténylegesen betöltve (Reliability: magas=177, közepes=1) | KJV/ASV kereszt-ellenőrzés: 177 sor "magas" (talált egyező KJV vagy ASV Strong-adat ugyanarra a versre/Strong-számra), 1 sor "közepes" (Gen.12.1 H1980 "Eredj" — nincs KJV/ASV Strong-adat erre a vers/Strong-párra); ebben a körben ÚJ KJV/ASV ELTÉRÉS nem került elő (a meglévő párosítás minden fellelt esetben egyezett). 7 sor kihagyva "TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ" jelöléssel (צֶלֶם, גַּן, עֵזֶר כְּנֶגְדּוֹ, צֵלָע, אִשָּׁה, נָחָשׁ, מִזְבֵּחַ), 2 sor kihagyva nyitott ELTÉRÉS miatt (1Móz 3:7-24 עֵרֻמִּם/H6174, 1Móz 4:1-24 הֶבֶל/H1892) — egyik kihagyott tétel sem került be a join-táblába, emberi döntésre várnak |
