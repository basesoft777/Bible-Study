ELTÉRÉS: 4 tétel

# ELLENOR_F145 — F145_THAYER_KAPU_JAVITAS_BRIEF.md · be19583..f2fff7c (ág ccr-4d66ac1d-v5f9un)

Ellenőr modellje: `claude-opus-5-5`, a kért `opus`, egyezik. (A jelentést az ellenőr nem tudta fájlba írni; az orkesztrátor rögzítette, tartalmilag változatlanul, tömörítve.)

ELTÉRÉSEK súlyossági sorrendben:

1. **G-1(a) / ⛔(i), műcím-átvétel túl tág** (`eszkozok/thayer_jelolt/thayer_kapuk.py`, `ellenoriz_sigla` / `_atvett`): a kivétel minden sigla-típusra érvényes, a `cf.`, `Sept.`, `i. e.` rövidítésekre és az antik szerzők idézeteire is. Kódolvasásból levezetett eset (futtatással nem igazolt): forrás és fordítás `cf. Winers Grammar, § 12` → az ablak szó szerint megvan, a `cf.` „átvett”, a kapu RENDBEN, pedig nem lett `vö.`; a régi kapu SERTES-t adott. Kiterjedés (`adat/thayer_szakaszok.tsv`, Grep): 3717 sor a `cf./Sept./i. e.` + nagybetűs szó + 2 szó mintára, 676 sor az antik szerzős mintára. A napló/docstring „ismert határa” ennél szűkebb. A teszt nem fedi a `cf.` + változatlan esetet. Javaslat (a döntés a felhasználóé): a kivétel csak a műcímre/szerző-típusra szóljon, és az ablakban legyen nem szám, nem sigla szó; teszt a `cf. Winers Grammar` esetre.
2. **CI E16 HIBA:** a PR érinti az ellenőrzőt (`ellenoriz.py`, `szabalyok.py`, `test_szabalyok.py`), a PR címének `[ELLENŐRZŐ]` előtaggal kell kezdődnie. (Továbbá E30 FIGYELMEZTETÉS: `e1f2688` üzenetében `naplo` → `napló`; az E27 hiba a FELADATOK.md generált blokkjában nem e diffé.)
3. **`eszkozok/teszt_ellenoriz_13.py:120`:** a meglévő fixture fejlécében `illeszes` → `illesztes` javítás történt, a napló/zárójelentés nem említi.
4. **E19 tesztek helye:** a brief az `E19Teszt` osztályt írja elő, a tesztek új `E19SzakaszTeszt` osztályba kerültek; a zárójelentés „eltérés nincs” állítása ezt nem tartalmazza.

Rendben: modell-egyezés (a menet modellje nem igazolható, de a nyomok egyeznek), sortörlés (adatsor nem), táblasor-Δ 0, hatókörön kívüli fájlok érintetlenek, D1/D2, 16. kapu (b) ragozás-tűrés és (c) számjegy-előtag, 13. szabály Thayer-ága (kód), E19 (0 találat ezen a fán), állapotfüggő tesztek, SEMA + docstring, E12–E15 0. Nem ellenőrizhető: a #142 fáján mért értékek (SÉRTÉS 0, E19 HIBA 3→0), a hash-eltérés okának N-F tétele.
