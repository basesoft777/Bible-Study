# ELLENOR_F94 — független ellenőrzés

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`; kért: `opus`, egyezik). Tartomány: b6e655f4..6f6f5c32 (30 commit, 35 fájl). A jelentés szövegét az orkesztrátor mentette a fájlba, az ellenőr nem rendelkezett fájlíró eszközzel; a tartalom az ellenőr jelentésének tömörített másolata, érdemi változtatás nélkül.*

**Eredmény: ELTÉRÉS, 7 tétel. A K5 utolsó feltétele („a független ellenőr eltérés nélkül zár”) nem teljesül.**

## Eltérések súlyossági sorrendben

1. **K6 sérül a kiadott táblában.** A `adat/szoto/karoli_szotari_alak.tsv`-ben legalább 26 névszói alak (pl. *születése*, *teremtésének*, *lakossága*, *okossága*, *istensége*, *keresése*, *felekezete*, *felekezetének*; sorok: 17016, 19317, 19318, 22413, 22415, 26929, 31555, 32470, 33426, 36526, 37458, 40464, 42900, 42902, 43768, 47308, 49784, 49868, 54448, 54456, 56315, 56904, 56907, 57409, 66430, 66433) igei `regies_jegy`-et kap (pl. `mult.alanyi.E3`, `mult.T3`), néhol hibás `alapige`-vel (*elnézés → nézés*). A becslés alsó határ. Ok: a C/CK változatban az `_ismert()` mindig hamis (`hibrid.py:604`, `:306-314`), így az -a/-e névszószűrő kiesik, és ritka névszónál a `-nak/-nek` feltételes attesztáció átengedi a tövet. A K6 200 alakos listája csak a v3 A (simplemmás) változaton készült, nem a kiadott C+K-n. Érinti a DT128 modernizálás bemenetét.
2. **`licencek.tsv`, `szoto_tablak` sor:** komponensként csak a Károli 1908 és a `simplemma_nyelvi_adat` szerepel, ami ellentmond a sor saját „ODbL-összetevő nincs” állításának; hiányzik a TAHOT/TAGNT (CC BY 4.0, kötelező forrásmegjelöléssel), pedig a minták `strong` oszlopa és a `szabaly_ellenorzes.tsv` az `adat/karoli_strong/`-ból származik; a `kotelezo_megjeloles` értéke `—`, a SEMA szerint ilyenkor üres kell.
3. **`licencek.tsv`, `simplemma_nyelvi_adat` sor:** `kereskedelmi=nem`, holott az ODbL megengedi (a SEMA 2.19 szerint a mező a licencről szól, a CC BY-SA sorok is `igen`); `allapot=tisztazott`, miközben a licenc oszlop „nyelvenként nem azonosított forrásokat” is említ (a SEMA 2. szabálya szerint ez legalább részben `tisztazatlan`).
4. **Nyitott tételek (A2):** az N-F94e javítva van (`hibrid.py`, zárójelentés), mégis nyitottként áll a `NYITOTT_FELADATOK.md:58`-ban; az N-F94a–c csak a briefben szerepel, önálló tételként nincs a `NYITOTT_FELADATOK.md`-ben, az N-F94c (*jó*, 1Móz 1:4) a brief lezárásával elveszne (`lekerdez.py scan H2895 --szakasz "1Móz 1:4"` n=1, H2896 n=0).
5. **Proveniencia-ellentmondás:** a `k_tabla_epit.py:8-9` docstringje szerint a K tábla kitöltésekor sem a simplemma, sem a hibrid kimenete nem volt a modell előtt; a napló 11.1 („Őszinte korlát”, `naplok/SZOTOVEZES_meres.md:572`) szerint a 9. szakasz A- és C-hibalistái a kitöltés előtt a modell előtt voltak. A DT-F94c ODbL-kérdése miatt lényeges.
6. **A brief .2 hibaosztályai a kiadott C+K-ban hibásak** (v3 A-ban javultak): *Melkié → Melkié* (helyesen *melki*; `karoli_szotari_alak.tsv:7613`), *atyámnak → atyám* (helyesen *atya*; `:13003`), *meggyarapodnak → meggyarapod* (helyesen *meggyarapodik*; `:40622`). A zárójelentés nem nevesíti.
7. **`adat/SEMA.md` 2.27 elavult sorai:** az `alapige` sor („a 2. mintának nincs ilyen oszlopa”) a DT-F94a E-7/E-8 után nem igaz; a `strong` sor forrása „a régi `token_karoli`”, az F94.1b óta `adat/karoli_strong`.

Megfigyelés (nem eltérés): az *összegyűlekezik* lemma fő Strongja a napló 15.2 szakaszában H6950, a 16.3-ban H0622.

## Ami rendben van (saját lekérdezéssel igazolva)

- CI (`futtat.py`, E2–E16, E19, E20, E26): 0 találat; E25 3 (régi, a diffben nem szereplő fájlok); E27: 33 (régi ághivatkozások, nincsenek a diffben; 30 sor csonkolva, nem ellenőrizhető).
- K1: a minták 213 / 180 / 113 / 113 sorral, `ellenorzes` sehol üres; a `felhasznalo` 12 sor az 1–2. mintán (6 eredeti + a DT-F94a új sorai). DT-F94b: *Seregek* 119, *Seregeknek* 104, kisbetűs *seregeknek* 85 előfordulás; Ézs 44:6 „a seregeknek Ura”.
- DT-F94a Strong-ellenőrzés: H5414 (1Móz 1:17), H8085 (Ézs 41:26), H0006 (Ézs 41:11) a `scan`-ben n=1.
- K4: `KORPUSZ_STRONG` 30 elem, `MANUAL={'cz → c'}`; 9 + 44 = 53 szabály; a kimenetben 14 947 sor `korpusz_strong|manual|modell_ellenorizetlen`; a simplemma-licencidézet szó szerinti.
- K5: nincs emMorph-/hfst-hivatkozás kódban vagy adatban (csak két „nem része” docstring); nincs abszolút `C:`/`D:`/`/mnt` útvonal; nincs `csv` modul, `split('\t')` / `'\t'.join`; kódolási őr mind a 19 .py-ban.
- Simplemma nélküli előállítás: `sys.modules['simplemma']=None` + őr; `modszer=simplemma` sor 0; a `karoli_szotari_alak.tsv` 66 824 sora = a lexikon; a fejléc `# GENERÁLT` sora és a Kiegészítés B figyelmeztetés megvan.
- `regies_jegy`: 3 297 sor; lexikon- és név-sorban 0.
- DT124: Bible Discovery szöveg/Strong az `adat/` és `eszkozok/` alatt 0.
- CLAUDE.md három szabálya: rendben. Ell.lista 1–5 (kiszűrt sorok, kulcstartomány, nulla-diff hatóköre, sorszám-Δ, ⛔ pontok sorrendje): rendben.

## Nem ellenőrizhető az ellenőr szerepéből

K2 és K3 számai (a `meres.py` + simplemma WSL-ben futna, nem megengedett parancs; a v3 a mérés után +9/−2 sorral módosult, ez a naplóban 16.2–16.3 jelölve), Python 3.11 alatti futás (f-string-szintaxis 3.12+: 0 találat), DT-F94a törzsállítások (Qal / Hif'íl), a felhasználói átnézés bizonyítéka (claude.ai-oldal, repóadatból nem igazolható), hogy a hibridet a javaslatok előtt helyben nem futtatták-e.

## Lezárás

Nem zár eltérés nélkül. Az 1–3. eltérés tartalmi és licencügyi (a felhasználó dönt), a 4–7. formai javítás.
