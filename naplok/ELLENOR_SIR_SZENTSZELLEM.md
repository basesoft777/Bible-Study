# F35 független ellenőri jelentés (tömör; a menet rögzítette, mert az ellenőr nem tudott fájlt írni)

Eltérések és javításuk (F35.6):
1. E9 HIBA: a zárójelentés 4. sora az angol szót leírta, a diff módú CI ezen bukott. Átfogalmazva, a szám újramérve (85 JELENTÉS).
2. `elofordulasok.tsv:169` `karoli_szo`: a SEMA.md:188 szerint Károli-szóalak, nem javítva; DT-F35b (🟡) nyitva, javaslat: marad. A DT26 feltevése ennél a sornál ütközik a SEMA.md:188-cal.
3. Az M2 a chatbeli jóváhagyás után futott, a DT státusza csak az F35.5-ben váltott: rögzítve a zárójelentésben.
4. M0 kiegészítve: forditasok.tsv:72, 73, 91 és a motivumlog CHANGELOG:152 Sirák fia / történeti napló, marad.

OK pontok: a cserék helye és tartalma egyezik a jóváhagyással; auditok.tsv érintetlen; generált fájl nem módosult; teszt_lekerdez_sir és ellenoriz.py rendben.
