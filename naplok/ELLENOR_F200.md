ELTÉRÉS: 2 tétel

# ELLENOR_F200 — F200_PROZA_ALLITAS_BRIEF.md · 9926ae54..2de13efd

*Független ellenőr: `fuggetlen-ellenor` subagent (opus), 2026-11-11. A jelentést a subagent válaszként adta; a hívó session mentette, tartalmi változtatás nélkül, a táblát tömörítve. A javítókör: F200.4 (`naplok/F200_jelentes.md`, „Független ellenőrzés és javítókör”).*

**A futtatás korlátja.** A szerep csak `git diff`, `git log`, `lekerdez.py` és `ellenorzes/futtat.py` hívást enged; a `gh run`, a `teszt_proza_allitas.py` és a `proza_allitas.py` futtatása NEM ELLENŐRIZHETŐ.

| pont | eredmény | indok (röviden) |
|---|---|---|
| 0 modell | OK | session `claude-opus-5-5`, kért `opus`; a commitok `Co-Authored-By` sora egyezik |
| G1 | OK | 10 fájl, mind az `ir` listán; `lexikon/`, `lexikon_general.py`, `motivumok/`, `adat/`, `DONTESEK.md`, `NYITOTT_FELADATOK.md`, `FELADATOK.md` diffje üres |
| G2 | OK (kód), NEM ELLENŐRIZHETŐ (futtatás) | `return 1 if (a.szigoru and elter) else 0`; a `--szigoru`-ra nincs teszt |
| G3 | OK | mindenütt `split('\t')`, `csv` 0 találat; a wrapper a stdlib-importok után |
| G4 / D3 | OK, megjegyzéssel | a párosítás csak magyar szó → Strong feloldás; az ELTÉR a TAHOT-soron áll |
| D1, D2, D4 | OK | `kapcsolodas` egység; a CI csak a tesztet futtatja, E-szám nincs; a szám csak „a lap/a motívum” alanyra gépi |
| **„más szó” a következő igehelyre kerül** | **ELTÉRÉS** | a záradék az előző és a következő csoport közötti szöveg; a `HAMART-001.md:21` „más héber szóval (álá)” mellékmondata (Ézs 24:5-6) a Hós 4:1-3-ra adott ítéletet (`lekerdez.py scan H0779 --szakasz "Hós 4:1-3"` → n=0, itt véletlenül „egyezik”); ugyanígy a `POZITIV` |
| **saját Strong-normalizáló** | **ELTÉRÉS** | `^([HG])0*(\d{1,4})` → G20447 → G2044 (létező másik szám); az F62 `strong_util` az egyetlen normalizáló; 3 TAGNT-sor (ApCsel 24:12, 2Kor 11:28, 1Thessz 2:8); a HAMART-próbát nem érinti |
| 10 ELTÉR-sor valódisága | OK | mind a 10 a TAHOT szerint igazolva (`lekerdez.py scan`): H0127 az 1Kir 13:34-ben és a 2Kir 17:23-ban; H6440 az 1Kir 14:15-ben n=0, a 2Kir 17:23-ban nem szomszédos; H4390 az Ez 12:19-ben n=0 (H4393 n=1); az Ez 7:23-ban H0127 n=0, H0776 és H5892 n=1; H7093 az Ez 7:2, 7:6, Ámós 8:2-ben n=1; a lektor 5, 6, 32, 41, 43. tételével egyezik |
| 34 pontossági tétel | OK | az 1. vagy 4. kérdést 34 tétel nevezi; a többi 12: 1, 2, 3, 4, 7, 16, 20, 24, 39, 44, 45, 46 |
| a próba számainak összhangja | OK | 5 + 18 + 11 = 34; 113 kézi, 53 ⚑, 10 ELTÉR, 109 egyezik (a javítókör előtt) |
| reprodukálhatóság | NEM ELLENŐRIZHETŐ | a bemenetek közül 7095bc63 óta csak az `olvasoi_kapu.py` változott, az eszköz által használt függvényei nem |
| CI | NEM ELLENŐRIZHETŐ | a saját `futtat.py`: **E16 HIBA**, ha a PR címe nem `[ELLENŐRZŐ]` előtagú (a workflow változik); E25/E27/E34 jelentések a diffen kívül |
| A1, A2, A6 | OK | proveniencia; N-F200a–d új; E12–E15 0 |
| 1–5. (törlés, kulcstartomány, nulla-diff, TSV Δ, ⛔) | OK | adatsort a diff nem töröl; TSV Δ = 0; a merge a felhasználóé |
| 10-es sablon, C-a | OK, megjegyzéssel | „a lektor csak az ELTÉR-sorok javítása után indul” szigorúbb a DT785 „kilépőkód 0”-jánál, de nem ellentétes |
| DT784/c/d | OK, megjegyzéssel | „a végrehajtó döntése” 🟢, van előzménye; a felhasználó a merge-nél dönt |

**Nem ELTÉRÉS, de figyelendő:** E16 (a PR címe); a „más kulcsszóval” próba egyetlen közös tartalmi szóra is ELTÉR-t ad; az idézetpróba csak a mondaton belüli igehelyekhez mér (az előző mondatban megnevezett vers idézetére téves ELTÉR adódhat).

**A javítókör (F200.4) kezelése:** mindkét ELTÉRÉS javítva, teszttel; a „más kulcsszó” küszöbe: az idézet tartalmi szavainak legalább fele; a PR címe `[ELLENŐRZŐ]` előtagú; az idézetpróba korlátja nyitott (a kézi lista fogja).
