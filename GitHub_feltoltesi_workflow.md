# GitHub kézi feltöltési workflow

*v1 — 2026.08.17*

Ez a dokumentum rögzíti, hogyan kerülnek fel az elkészült PaRDeS-tanulmányok és sablonfájlok GitHubra, a Claude Projects-en belüli meglévő munkafolyamat kiegészítéseként (nem helyette).

---

## Javasolt repó-mappastruktúra

```
pardes-tanulmanyok/
├── sablonok/
│   ├── 1_PaRDeS_alap_sablon.md
│   ├── 2_PaRDeS_bovitett_sablon.md
│   ├── 3_PaRDeS_research_sablon.md
│   ├── 4_PaRDeS_tematikus_sablon.md
│   ├── Melyelemzes_prompt_sablon.md
│   └── PaRDeS_gyorsreferencia.md
├── motivumlog/
│   └── PaRDeS_motivumok_vXX.md   (mindig csak a legfrissebb verzió felülírva, VAGY minden verzió megtartva — ld. lent)
├── genezis/
│   ├── 1Moz_1_bovitett.md
│   ├── 1Moz_14_bovitett.md
│   └── ...
├── ujszovetseg/
│   ├── Rom_8_10_bovitett.md
│   ├── Zsid_4_12_bovitett.md
│   └── ...
├── tematikus_lezart/
│   ├── Tehom_tematikus.md
│   ├── Segitsegul_hivni_az_Urat_tematikus.md
│   ├── Rafaim_Gibborim_Nefilim_tematikus.md
│   └── Tehóm-Abüsszosz-Hádész-Tartarosz_tematikus.md
├── melyelemzesek/
│   └── 1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md
└── Lezart_tematikus_tanulmanyok_index.md
```

**Motívumlog-verziózás — eldöntve: A) opció**

A motívumlog mindig egyetlen, állandó nevű fájlként (`motivumlog/PaRDeS_motivumok.md`, verziószám nélkül a fájlnévben) kerül fel, minden frissítéskor felülírva. A korábbi állapotokat a git history őrzi meg automatikusan — nincs szükség kézi vXX-fájlnevekre a GitHub-repóban.

Ha egy korábbi verzió megtekintésére van szükség: a fájl GitHub-oldalán a **History** gombbal minden korábbi commit/verzió külön-külön visszanézhető és letölthető, git-tudás nélkül is.

*(A Claude Projects-en belül a vXX-es fájlnév-konvenció [`PaRDeS_motivumok_v43.md` stb.] változatlanul megmarad — ez a GitHub-workflow csak a repóra vonatkozik.)*

---

## Lépésről lépésre — minden egyes elkészült fájlnál

1. **Claude elkészíti és kiteszi** a fájlt `/mnt/user-data/outputs/`-ba, letölthető linkkel — ez a jelenlegi workflow változatlan első lépése.
2. **Letöltöd** a fájlt a tabletedre/gépedre.
3. **GitHub webes felületén**, a megfelelő mappában (pl. `genezis/`):
   - Ha a mappa már létezik: nyisd meg, kattints **"Add file" → "Upload files"**.
   - Húzd be vagy válaszd ki a letöltött `.md` fájlt.
   - Görgess le, írj egy rövid commit-üzenetet (pl. `"1Móz 17 bővített tanulmány hozzáadva"`).
   - **Commit changes.**
4. **Ha a fájl egy már meglévő fájl frissítése** (pl. motívumlog vagy index-fájl az A) opció esetén): nyisd meg a meglévő fájlt a repóban, kattints a ceruza ikonra (**Edit**), töröld a régi tartalmat, illeszd be az újat, majd **Commit changes**.

---

## Mikor kerül sor feltöltésre

- Minden lezárt PaRDeS-tanulmány (alap/bővített/research) elkészülte után
- Minden motívumlog-frissítés után — a `motivumlog/PaRDeS_motivumok.md` fájl felülírásával (csak a legfrissebb verzió, git history őrzi a korábbiakat)
- Minden új tematikus lezárás vagy mélyelemzés után, egyúttal a `Lezart_tematikus_tanulmanyok_index.md` frissítésével
- Sablonfájlok módosításakor

---

## Mi NEM változik

- A Claude Projects-en belüli munkafolyamat (fájl elkészítése, letöltés, projektbe visszatöltés) **továbbra is az elsődleges**, működő rendszer marad.
- A GitHub-feltöltés egy **kiegészítő, párhuzamos archívum** — nem váltja ki a projektfájlok frissítését, mert Claude a `project_knowledge_search`-csal a Claude Projects-tartalmat éri el, nem a GitHub-repót.

---

## Opcionális kiegészítő eszköz: Gemini Notebook (korábban NotebookLM)

*A Google forrás-alapú kutatóeszköze 2026. július 16-án átnevezésre került NotebookLM-ről Gemini Notebookra (notebook.google.com), funkcionálisan változatlan.*

**Mire hasznosítható a lezárt tanulmányok utólagos feldolgozásában:**
- **Keresztkeresés** a lezárt tematikus tanulmányok között (feltöltve mint sources) — forrás-alapú chat, pontos idézetekkel visszavezethető válaszokkal.
- **Mind Map funkció** a motívumok közötti összefüggések vizuális feltárására (pl. hádész/seól ↔ rafeusok ↔ tehóm rokonsági háló).
- **Ellentmondás-keresés** két verzió/dokumentum között, pontos idézetekkel — hasznos lehet jövőbeli verzió-divergencia esetén.

**Korlátok, amiket figyelembe kell venni:**
- Adatkezelés: a feltöltött fájlok a Google szerverein dolgozódnak fel, nem helyben.
- **Nem helyettesíti a PaRDeS-tanulmányok elkészítését** — nem ismeri és nem kényszeríti ki a projekt egyedi szabályrendszerét (PaRDeS-rétegek arányai, ⭐ küszöb-logika, named teacher protokoll, Károli-idézési szabályok).
- Idézési pontosság nem feltétlenül igazodik a projekt szigorú Károli-only / rövid HGY-idézet szabályához.

**Szerepe a workflow-ban:** kizárólag **olvasás/áttekintés célú, opcionális, párhuzamos eszköz** a már lezárt anyagok utólagos böngészésére — a tanulmányok *elkészítése* továbbra is a Claude Projects + a sablonok feladata marad.
