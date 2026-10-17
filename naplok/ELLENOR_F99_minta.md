# ELLENŐR — F99_BDB_SZELETELO_BRIEF.md, aranyminta (szűkített feladat, DT170 (b))

*A `fuggetlen-ellenor` subagent jelentése; fájlba mentette az orkesztrátor (az ellenőrnek nincs író eszköze). Tartomány: `main`..`claude/bdb-szeletelo` (efa31894). Tényleges ellenőr-modell: `claude-opus-5-5`.*

**Hatókör:** csak az `adat/bdb_aranyminta.tsv` 32 szócikke (622 sor: 32 szócikk + 151 csoport + 439 egyéb) összevetve a forrással (`konkordancia/BDB_teljes_unabridged.tsv`; magyarul 14 szócikknél az `adat/forditasok.tsv` utolsó nem üres BDB-sora). Szabály: a DT167 (1)(a) eldöntött listája (a minta ennél szigorúbb, korábbi listán készült). Mind a 622 sor `modell_ellenorizetlen`. Egyik forrásfájl sem változott az ágon. Az ellenőr egyszeri szabályszegése: egy `grep` láncot futtatott (csak olvasott).

## Eltérések (11)

| # | szócikk | hely a mintában | forrás | lényeg |
|---|---|---|---|---|
| E1 | H3027 5/a–5/h | 491, 492, 509, 512 | BDB 2843, HU 117 | A „(1) after verb of motion” az 5/a (אֶליַֿד) tagja, a minta az 5/b alá tette; az 5/b valódi (1)/(2) tagja OCR-alakban áll („-1בְּיַד…”). A 492/509/512 „a (2) hiányzik” megjegyzése hamis; az 5/a-nak nincs csoportsora. |
| E2 | H0834 שֶׁ 3. jelentés | 561, 565 | BDB 779, HU 99 | A 3. jelölő tapadt alakban megvan („3as a conjunction”); a „hiányzik” állítás és a `kihagy -/2` indoka hamis, a 3. jelentés csomópontja hiányzik. |
| E3 | H0834 zárójeles 3. szint | 521–570 | BDB 779 | 0 csoportsor, holott 2. (a)(b), 6. (a)(b)(c), 8/a (a)(β)(γ), שֶׁ 4/b, שֶׁ 3/a van; a H6440/H0157 csoportként rögzíti → következetlen. |
| E4 | H0430 4/b (β) | 392 | BDB 401, HU 88 | A „(β) with nouns of attributes…” megvan; a „nincs a szövegben” hamis, a csoportsor hiányzik. |
| E5 | H0430 3. jelentés | 388 | BDB 401 | „(a) angel / (b) prophet” zárójeles szint, csoportsor nincs (alacsony súly). |
| E6 | H6440 II/7/a (ε) | 319–323 | BDB 6022, HU 111 | Az ötödik tag („with verbs implying direction”) csoportsor nélkül. |
| E7 | H6440 II/1/a | 267 | BDB 6022 | „with יָצָא” mondatkezdő, csoportsor nincs (alacsony). |
| E8 | H2490 III Hiph'il/2 | 600 | BDB 2336, HU 387 | 4 mondatkezdő „with …” bevezető (Infinitive, ו consecutive, בְּ, מן) → 4 csoport hiányzik (a DT167 eldöntött listájának következménye). |
| E9 | H1157 2. jelentés | 607 | BDB 1082 | „with כִּמֶּר” és „With לְ…” mondatkezdő with + héber, csoportsor egyikhez sincs. |
| E10 | H7307 4/d | 358 | BDB 6834, HU 214 | „; especially 104:29” csoportsor nélkül (alacsony). |
| E11 | H7121 4/a | 414–415 | BDB 6660 | „; with acc of roll, book” rövidített „with accusative”, csak a másik csoport rögzítve (alacsony, vitatható). |

Közös mintázat (E1, E2, E4): az OCR-torzult jelölőket (`-1`, `-2`, `3as`, `(β)`, `(ε)`) a minta hiányzónak vette.

## Nem eldönthető pontok (a felhasználó dönt)

- **B1 H5766** (`85–89`): a szócikk végén „I. עַלְוָה transposed from עַוְלָה (q. v.)” római számos utaló címszó áll; szakasz-e?
- **B2 H1242 1/b** (`126–127`): „; & especially” — mondatkezdő-e az „&” miatt?
- **B3 H6696 Qal/2** (`62–67`): az első „with עַל” vessző után áll (nem csoport), a párhuzamos 4 tag csoport — szabálykövető, de aszimmetrikus.
- **B4 H3176 Hiph'il** (`23–24`): két számozatlan jelentésblokk, a minta egyet sem rögzít.
- **B5 megjegyzés-pontatlanságok:** 498 (a forrásban van szóköz a „(4) בְּיַד” után), 562 (a שֶׁ 1. végén a „b.” hivatkozás: „see מָה 1e b.”), 234 (a Qal/4-ben is van könyvnév-jelölt: „1 Kings 5:20”).

## A beszélgetés nyolc szócikke

| Strong | minta-sorok | eredmény |
|---|---|---|
| H1242 בֹּקֶר | 121–136 | OK; bizonytalan: B2 |
| H0776 אֶרֶץ | 137–161 | OK (a 4. jelentés címében a héber sorrendje fordított a forrásban; héber nélkül egyezik) |
| H7451 רַע | 162–191 | OK |
| H3615 כָּלָה | 192–228 | OK (a Pi'el/1/d/+2 a DT167 szerint rendben) |
| H0559 אָמַר | 229–248 | OK; pontatlan megjegyzés: B5 (234) |
| H6440 פָּנֶה | 249–327 | ELTÉRÉS: E6, E7 |
| H7307 רוּחַ | 328–374 | ELTÉRÉS: E10 |
| H0430 אֱלֹהִים | 375–393 | ELTÉRÉS: E4, E5 |

## A többi 24 szócikk

- Eltérés nélkül: H0196, H0382, H5379, H5022, H4111, H2939, H5203, H6504, H4900, H4686, H5145, H8213, H4060, H1124, H5648, H0157 (és a fenti OK nyolcból H0776, H7451, H3615, H0559, H1242).
- Csak bizonytalan pont: H3176 (B4), H6696 (B3), H5766 (B1).
- Eltérés: H3027 (E1), H0834 (E2, E3), H2490 (E8), H1157 (E9), H7121 (E11).

## Hatókörön kívül

A CI-jelentés, az ellenőrzőlista 1–3 és 5. pontja, a `futtat.py` nem futott (szűkített feladat). A táblasor-Δ: egyetlen új tábla, `adat/bdb_aranyminta.tsv`, +622 adatsor.
