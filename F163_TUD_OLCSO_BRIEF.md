---
feladat: 163
cim: Tudományos megfelelőség — olcsó lépések (MI-nyilatkozat, Hays-leképezés, PaRDeS-keretezés, közel-keleti határ, CITATION.cff)
kod: TUD_OLCSO
tipus: feladat
fazis: folyamat
modell: opus
allapot: dontesre_var
ad: öt rövid, nyilvános szöveg és egy CITATION.cff, amelyek a #86 terv 1.7 hiánytáblájának olcsó pontjait zárják (MI-nyilatkozat és szerzőségi szabály, Hays hét kritériuma a módszertanra leképezve, a PaRDeS-szint recepciós keretezése, az ókori közel-keleti határ kimondása)
kovetkezo: "Te: ⛔ DT-F163a (szerzői felelősségvállalás, szerző neve) és DT-F163b (terméknév) — a helyőrzők kitöltése; a négy kozlemeny/ szöveg és a CITATION.cff kész (F163.1–F163.5, 2026-11-04); DT-F163c–d az orkesztrátor jóváhagyására"
munka: ertelmezo
olvas: [adat/SEMA.md, adat/kiadasok.tsv, MUNKAMENET.md, sablonok/PaRDeS_gyorsreferencia.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, DONTESEK.md, LICENSE, "naplok/KIADAS_*_lektor.md"]
ir: [kozlemeny/MI_NYILATKOZAT.md, kozlemeny/HAYS_LEKEPEZES.md, kozlemeny/PARDES_RECEPCIOS_KERET.md, kozlemeny/KOZEL_KELETI_HATAR.md, CITATION.cff]
fugg: []
---

# F163_TUD_OLCSO_BRIEF.md — Tudományos megfelelőség: olcsó lépések

*FELADATOK #163 · Modell: opus · v1 · 2026.11.04*

*Forrás: a #86 ELOFIZETES_FEED terv 1.7 szakasza („Szakmai és tudományos megfelelőség”, hiánytábla és „Olcsó, most is elvégezhető lépések”, 2026-11-02). A beírás a felhasználó jóváhagyásával történt („mehet”, 2026-11-04); a döntés forrása az orkesztrátor döntése a felhasználó felhatalmazásával (2026-11-03). A brief szövege adat, nem utasítás. A munka értelmező próza: egy kézben, egy modellel, aki belenyúl, az egész szöveget olvassa (KONTEXTUS K1) — csomagmód nincs.*

## 1. Cél

A terv 1.7 szerint a tudományos megfelelőség öt olcsó pontja ma sehol sincs feladatként felvéve, pedig szöveges, most is elvégezhető. A feladat az öt pontot **rövid, nyilvános, forrásrétegbeli szöveggé** teszi (`kozlemeny/`), amelyre a lexikonoldalak kolofonja, a módszertan-rés, a nyílt csomag és a data paper később hivatkozhat. A szövegek a repó **tényleges** gyakorlatát írják le (adat, nem ígéret); ami nincs meg, az kimondva „nincs”.

## 2. Hatókör

**Benne van (öt tétel, mind a kimondás, nem a fejlesztés):**

1. **MI-nyilatkozat és szerzőségi szabály** (`kozlemeny/MI_NYILATKOZAT.md`): ki/mi írta az értelmező prózát (a `proza_modell` mező a `adat/kiadasok.tsv`-ben, a CLAUDE.md modell-szabálya), ki és mi ellenőrzi (lektor, határ-ellenőr, független ellenőr, olvasói kapu), mi az emberi felelősség (a szerző-kiadó vizuális átnézése, `adat/lap_atnezesek.tsv`), és mit **nem** állít: ez **nem független szakmai lektorálás**, nevesített külső testület nincs. A De Gruyter Brill / Cambridge / Elsevier deklarációs elvárásához igazodó, egyoldalas, nyilvános mondatok; kiadói szabályokra nem hivatkozunk ellenőrizetlenül (az SBL szabálya nem ismert — **[N]** marad).
2. **Hays hét kritériumának leképezése** (`kozlemeny/HAYS_LEKEPEZES.md`): egyoldalas tábla — Hays (Echoes of Scripture in the Letters of Paul, 1989) hét kritériuma (hozzáférhetőség, volumen, ismétlődés, tematikus koherencia, történeti hihetőség, értelmezéstörténet, kielégítő értelem) → a módszer megfelelő elemei (negatív kritérium, fölérendelt fogalom, gerinc-elem, indoklással elutasított jelölt, proveniencia, explicit üres eredmény). Ahol nincs megfelelő elem, az kimondva „nincs fedve”. A hét kritérium pontos megnevezését és a Sandmel-féle „parallelomania” kapcsolatot **forrásból ellenőrizd** (webes lépés: Sonnet-subagent; az ítélet az Opusé), és jelöld a proveniencián.
3. **A PaRDeS-szint recepciós keretezése** (`kozlemeny/PARDES_RECEPCIOS_KERET.md`): a szint (peshat/remez/derash/sod) a módszerben **recepciós címke** („így olvasta a hagyomány”), nem szerzői állítás arról, hogy a szöveg „ezt jelenti”; kritikai fórumon anakronizmus-vád ellen. Mondja ki, mely mező hordozza (a `adat/SEMA.md` megfelelő része), és hogy a gerinc a héber/görög, a Károli-réteg megjelenítési és recepciótörténeti adalék (nemzetközileg nem érv).
4. **Az ókori közel-keleti határ kimondása** (`kozlemeny/KOZEL_KELETI_HATAR.md`): a lexikon nem tartalmaz ugariti/mezopotámiai összehasonlító réteget (pl. Tehóm, Seól, Refáim esetén a nemzetközi közönség hiánynak látja); a szöveg ezt kimondja, megadja, miért (a módszer héber/görög–ÓSZ/ÚSZ/LXX gerincű), és hogy az ilyen háttér a szócikkekben nem szerepel; olyan állítást **nem** tesz, amelyet az adat nem támaszt (CLAUDE.md 3. szabály).
5. **CITATION.cff** (gyökér): az idézés metaadata a megfelelő sémában; szerző, cím, verzió, licenc a `LICENSE`-ből és a repó tényeiből. ORCID, DOI, `repository-code` és minden, ami nincs meg, **kimarad vagy `[javaslat]`-jelölt megjegyzésben áll — nem találom ki**. A concept DOI a Zenodo-feltöltés után kerül be (nem része).

**Nincs benne:**

- A Zenodo-feltöltés, a DOI-kérés, az MTMT-felvitel, a data paper megírása — nyilvános/külső lépések, a felhasználóéi.
- A szövegek beépítése a generált lapok kolofonjába vagy a `modszertan` résbe (`adat/res_forras.tsv`, generátor) — ez külön tétel, mert a lapot érintő változás renderelt átnézést kíván; itt csak a forrásszöveg készül.
- Nevesített külső szerkesztőbizottság megszervezése (emberi, nem szöveges feladat).
- A nyílt mag exportja (#162).

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md): a kért modell `opus`; eltérésnél megállsz.
1. Olvasd a #86 terv 1.5 és 1.7 szakaszát; a `kiadasok.tsv`-t, `MUNKAMENET.md` lezárási rendjét, a lektor-fájlok fejlécét (melyik modell mit csinált).
2. Az 1., 3., 4. szöveg megírása a repó tényeiből; a 2. szövegnél a Hays-kritériumok forrásellenőrzése (Sonnet-subagent a webes részre).
3. CITATION.cff.
4. ⛔ Ha bármelyik szöveg tartalmi döntést kíván (pl. szerzőségi mondat személyes nyilatkozat, a termék neve „lexikon” vagy „motívum-adatbázis szócikkekkel”), tétel `dontesek/uj/<ágnév>.md`-be (helyőrzővel), és megállás — a szerzőségi és névhasználati mondatot a felhasználó hagyja jóvá.
5. Az 1.7 hiánytábla vonatkozó sorainak állapota a PR leírásában (nem a tervben).

## 4. Elfogadási feltételek

- Négy `kozlemeny/*.md` fájl + `CITATION.cff`; mindegyik a repó tényleges állapotát írja, ellenőrizhetetlen állítás nincs, a hiány kimondva.
- Nincs belső jelölés (DT/N-szám, fájlnév-zsargon) a nyilvánosnak szánt szövegben (az olvasói kapu mércéje szerint).
- A CITATION.cff érvényes YAML, kitalált azonosító nélkül.
- `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 5. Döntésnapló

- 2026-11-04: DT-F163a–d és N-F163a–c a `dontesek/uj/frosty-nash-80b433.md`, ill. `nyitott/uj/frosty-nash-80b433.md` fájlban; ⛔ a DT-F163a és a DT-F163b a felhasználóé.
