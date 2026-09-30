# ELLENŐR — F16 (BSB-import), merge-előkészítő kör (F16.8–F16.12), tömörítve

Ág: `claude/bsb-import` (#85). Ellenőr: `fuggetlen-ellenor`; a jelentés az orkesztrátor által mentett tömörítés (az ellenőrnek nincs írási eszköze). A `naplok/ELLENOR_F16.md` az F16.0–F16.7 három körét rögzíti; ez a fájl az utána következő két kört.

**1. menet (F16.8–F16.10) — ELTÉRÉS 8.** Rendben: Psa.3.3 = Károli 3:3, Psa.51.4 = Károli 51:4, 18/51/52/54/60 eltolása (k=1/2), a 3:1 felirat helyes hiánya, a régi sorok nem törlődtek, 242 638 sor, ÚSZ-őr és 0 G-sor, CC0-licenc.
Eltérések: (1) **Zsolt 13 hibás megfeleltetés** (a fejezetenként állandó k nem kezeli a belső versosztást: BSB 2–4 = MT 3–5, 5–6 = MT 6; 36 sor rossz igehelyen); (2) a hiány félre volt dokumentálva (nem a felirat, hanem a fejezet 1. versének érdemi szövege hiányzik a display-ből; MT-kulcsban 182); (3) elavult 27 043 (valós: 27 790); (4) a módosított mérési módszer felhasználói kérésre történt, nem volt rögzítve; (5) a történeti ELLENOR_F16.md szövegében a „DT-F16” „DT6”-re cserélődött; (6) hamis TAHOT-felirat állítás; (7) hiányzó rebase; (8) nem szó szerinti Károli-idézet.
**Javítás (F16.11):** Zsolt 13 kizárva a mérésből és az importból (41 sor), belső-osztás szabály a kódban, a hiány újradokumentálása, számok (242 597 sor, Zsolt 98,42%, 27 787 üres sor), történeti szöveg helyreállítva, idézetek szó szerintiek.

**2. menet (F16.11 után) — ELTÉRÉS 6.** Rendben: a Zsolt 13 helyes kizárása lekérdezéssel (BSB 2–4 = MT 3–5), 41 törölt sor és nincs `Psa.13.*`, számok (242 597 = napló összege = fájl; 31/8/27), 16 zsoltár és az összes k=0 feliratos zsoltár első versének mintavétele: nincs újabb Zsolt-13-szerű eset; E2–E16 0 találat merge-base-ről.
Eltérések: a DT6 „többi zsoltár” listája nem fedte a 37 nem egyező verset; a zárójelentés hivatkozási hibája; 182 → 187 elavult szám; az `ir:` mezőből hiányzik egy fájl; a rebase hiánya (4 commit, fájlátfedés nincs); az elavult `NYITOTT_FELADATOK.md:46`.
**Javítás (F16.12):** a 37 vers versenkénti listája (`naplok/F16_zsolt_nem_egyezo_versek.tsv`, 31 zsoltár), a hivatkozások és a számok, az `ir:` mező, a NYITOTT sor. Az orkesztrátor összevetette: a lista 37 sor, a `BSB_Strongs.tsv` és a lefedettségi napló nem változott, `feladatok.py ellenoriz` 0 hiba.

**Nyitva (felhasználói döntés, DT6):** a küszöb alatti 8 ÓSZ-könyv kezelése, a Zsolt 13 kézi megfeleltetése (g), az elided sorok jelölése, a hiányzó 187 MT-kulcs forrása (a `hebrew-tsv` licence nem kimondott; a `base/versification` CC-BY-SA 4.0).
**Nem ellenőrizhető:** a felhasználói A1-kérés (chat); a 37 nem egyező vers okának versenkénti vizsgálata (címkézési eltérésnek minősítve, a Károli-szöveggel nem egybevetve).
