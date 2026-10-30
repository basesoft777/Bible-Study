# Újramérés az első kalibráló mintán a DT-F131y szabályaival (N-F131w)

*A szabályok a kísérleti átíróban (`naplok/HEBER_KIEJTES_meres.py`, `dt_f131y()`); nincsenek az `eszkozok/` alatt, és a lapokba sincsenek bekötve. Adat nem változott.*

- **Proveniencia:** `scope=naplok/HEBER_KIEJTES_kalibracio.json (50 alak) + naplok/HEBER_KIEJTES_kalibracio_valasztas.txt | forras=naplok/HEBER_KIEJTES_kalibracio_ujrameres.py | ts=2026-10-30`
- **Mérték:** az új gépi alak egyezik-e egy elfogadott változattal. Ha egyik változattal sem egyezik („új alak”), arra a kalibrálás nem ad ítéletet.

**Eredmény: 41/50 elfogadható** (ebből 10 preferált), 7 nem elfogadott, 2 új alak (nincs ítélet). Előtte, a mai szabályokkal: 25/50.

| kategória | elfogadható (preferált) | elfogadható | nem elfogadott | új alak |
|---|---|---|---|---|
| kámec kátán (gyanú) | 4 | 2 | 1 | 0 |
| nem szókezdő sevá | 0 | 5 | 1 | 0 |
| furtív patah | 1 | 3 | 2 | 0 |
| dáges forte | 2 | 3 | 1 | 0 |
| ketiv/qere | 3 | 2 | 0 | 0 |
| makkef | 0 | 6 | 0 | 0 |
| szókezdő begadkefat dáges nélkül | 0 | 5 | 1 | 1 |
| ס és שׂ (sz vagy s) | 0 | 5 | 1 | 1 |
| **összesen** | **10** | **31** | **7** | **2** |

## Soronként

| # | kategória | héber | gépi (régi) | gépi (DT-F131y) | elfogadható (* preferált) | eredmény | ok |
|---|---|---|---|---|---|---|---|
| 1 | kámec kátán (gyanú) | הָרְפָאִים | horfáím | hárfáím | hárfáím*, horfáím | elfogadható (preferált) |  |
| 2 | kámec kátán (gyanú) | וְהָרְפָאִים | vehárefáím | vehárefáím | vehárefáím*, vehárfáím | elfogadható (preferált) |  |
| 3 | kámec kátán (gyanú) | בְּחָזְקָה | bechozká | becházká | becházeká*, becházká | elfogadható |  |
| 4 | kámec kátán (gyanú) | הָיְתָה | hojtá | hájtá | hájetá* | nem elfogadott | a döntés következménye: R4 elutasítva (a meteg nélküli kámec utáni sevá néma) |
| 5 | kámec kátán (gyanú) | שִׁבֳּלִים | sibbolím | sibbolím | sibbolím* | elfogadható (preferált) |  |
| 6 | kámec kátán (gyanú) | אָהְָלוֹ | áháló | áháló | áháló* | elfogadható (preferált) |  |
| 7 | kámec kátán (gyanú) | נִסְתָּרְנוּ | nistárenú | nisztárenú | nisztárnú, nisztárenú | elfogadható |  |
| 8 | nem szókezdő sevá | בִשְׁאוֹל | bisól | viseól | viseól | elfogadható |  |
| 9 | nem szókezdő sevá | בְשִׁמְךָ | besimchá | vesimchá | vesimchá | elfogadható |  |
| 10 | nem szókezdő sevá | וְקִרְאוּ | vekirú | vekireú | vekireú | elfogadható |  |
| 11 | nem szókezdő sevá | נִשְׁחָתָה | nischátá | nischátá | nishátá | nem elfogadott | a döntés következménye: R8 (ח = ch); a felhasználó itt h-t választott |
| 12 | nem szókezdő sevá | כִּתְהֹמוֹת | kithómót | kitehómót | kitehómót | elfogadható |  |
| 13 | nem szókezdő sevá | הַנְּפִילִים | hannefílím | hannefílím | hannefílím, hannefilím | elfogadható |  |
| 14 | furtív patah | יְהוֹשֻׁעַ | jehósua | jehósua | jehósua* | elfogadható (preferált) |  |
| 15 | furtív patah | הַמִּזְבֵּחַ | hammizbéach | hammizbéach | hammizbéach | elfogadható |  |
| 16 | furtív patah | תַּצְמִיחַ | tacmíach | tacmíach | tacmíach | elfogadható |  |
| 17 | furtív patah | מִזְבֵּחַ | mizbéach | mizbéach | mizebéach | nem elfogadott | nyitott: a zajin alatti sevát a felhasználó kiejtette; szabály nem fedi |
| 18 | furtív patah | יָנוּחַ | jánúach | jánúach | jánúach | elfogadható |  |
| 19 | furtív patah | רֵיחַ | réach | réach | réjach | nem elfogadott | nyitott: cere + jod furtív előtt (réjach); R9 nem lett szabály |
| 20 | dáges forte | וּמִתְּהוֹם | úmittehóm | úmittehóm | úmittehóm | elfogadható |  |
| 21 | dáges forte | חַיִּים | chajjím | chajjím | chajjím | elfogadható |  |
| 22 | dáges forte | וַיִּקְרָא | vajjikrá | vajjikrá | vajjikrá* | elfogadható (preferált) |  |
| 23 | dáges forte | חַיָּה | chajjá | chajjá | chajjá | elfogadható |  |
| 24 | dáges forte | מִשְּׁאוֹל | misseól | misseól | missól | nem elfogadott | nyitott: a kettőzött betű alatti sevát a felhasználó nem ejtette (missól); R3 itt ellentétes |
| 25 | dáges forte | חַטָּאת | chattát | chattát | chattát* | elfogadható (preferált) |  |
| 26 | ketiv/qere | וּבִירוּשָׁלִַם | úvírúsálim | úvírúsálajim | úvírúsálajim | elfogadható |  |
| 27 | ketiv/qere | יְרוּשָׁלִָם | jerúsálim | jerúsálajim | jerúsálajim | elfogadható |  |
| 28 | ketiv/qere | יְהוִה | JHVH | Jahve | Jahve* | elfogadható (preferált) |  |
| 29 | ketiv/qere | יְהֹוָה | JHVH | Jahve | Jahve* | elfogadható (preferált) |  |
| 30 | ketiv/qere | יְהוָה | JHVH | Jahve | Jahve* | elfogadható (preferált) |  |
| 31 | makkef | בְנֵי | bené | bené | vené, bené | elfogadható |  |
| 32 | makkef | בְשֵׁם | besém | vesém | vesém, besém | elfogadható |  |
| 33 | makkef | וַחֲמַס | vachamas | vachamasz | vachamasz | elfogadható |  |
| 34 | makkef | אַתְּ | att | att | att | elfogadható |  |
| 35 | makkef | אַף | af | af | ap, af | elfogadható |  |
| 36 | makkef | וּפֶן | úfen | úfen | úpen, úfen | elfogadható |  |
| 37 | szókezdő begadkefat dáges nélkül | כִשְׁאוֹל | kisól | kiseól | kisól | új alak | nyitott: R3 kiejtett sevát ad (kiseól), a felhasználó itt kisól-t fogadott el; új alak, nincs ítélet |
| 38 | szókezdő begadkefat dáges nélkül | כֹהֵן | kóhén | kóhén | kóhén | elfogadható |  |
| 39 | szókezdő begadkefat dáges nélkül | בִשְׁמִי | bismí | vismí | vismí | elfogadható |  |
| 40 | szókezdő begadkefat dáges nélkül | בִשְׁמוֹ | bismó | vismó | bismó, vismó | elfogadható |  |
| 41 | szókezdő begadkefat dáges nélkül | בְשָׁלֵם | besálém | vesálém | vesalém, besálém | nem elfogadott | nyitott: hosszúság (a felhasználó vesalém-et fogadott el, a gép vesálém-et ad) |
| 42 | szókezdő begadkefat dáges nélkül | בְצִלּוֹ | becilló | vecilló | vecilló, becilló | elfogadható |  |
| 43 | szókezdő begadkefat dáges nélkül | בְרִית | berít | berít | berít | elfogadható |  |
| 44 | ס és שׂ (sz vagy s) | וְחָמָס | vechámás | vechámász | vechámász | elfogadható |  |
| 45 | ס és שׂ (sz vagy s) | הֶחָמָס | hechámás | hechámász | hechámász | elfogadható |  |
| 46 | ס és שׂ (sz vagy s) | חָמָס | chámás | chámász | hámász | új alak | a döntés következménye: R1 + R8 (chámász); a felhasználó itt hámász-t fogadott el; új alak |
| 47 | ס és שׂ (sz vagy s) | כִּסְאוֹ | kisó | kiszeó | kiszeó | elfogadható |  |
| 48 | ס és שׂ (sz vagy s) | חֲמַס | chamas | chamasz | hamasz | nem elfogadott | a döntés következménye: R8 (ח = ch); a felhasználó itt h-t választott |
| 49 | ס és שׂ (sz vagy s) | חַסְדְּךָ | chasdechá | chaszdechá | chaszdechá | elfogadható |  |
| 50 | ס és שׂ (sz vagy s) | הַכֶּסֶף | hakkesef | hakkeszef | hakkeszef | elfogadható |  |

**A 9 nem elfogadott vagy új alakból 4 a DT-F131y egyenes következménye** (4: R4; 11, 46, 48: R8), **5 nyitott** (17, 19, 24, 37, 41). A nyitottak közül egy sem egyezik egy másikkal annyira, hogy szabályt lehetne rá építeni; a 2. minta mutatja meg, ismétlődnek-e.
