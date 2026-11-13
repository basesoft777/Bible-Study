# F218a — jelentés (menet-, ellenőri és zárójelentés egy fájlban)

*FELADATOK #218 · brief: `F218_GENERATOR_UJ_A_BRIEF.md` · ág: `claude/f218-generator-uj-a`.*

## F218.0 — modell-ellenőrzés, függések, keret

- **Modell.** Az építő session tényleges modellje `claude-fable-5-2`; a brief fejléce `modell: fable`. Egyezik. (Az első indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt, munka nélkül.)
- **Függések.** `python eszkozok/feladatok.py fuggesek` (main `37f087cc`): a 218-as tételhez `KIZAR` sor áll a 38, 123, 178, 179, 194 és 212 tétellel (közös fájl: `Konyv_normalizalo_tabla.tsv`, `elofordulasok.tsv`, a 6-os sablon, `general.py`). Ezek közül egy sem fut ténylegesen: a 38, 123, 178, 179 `megallt`, a 194 `dontesre_var`, a 212 `fut`, de `Folytatás:` kezdetű `kovetkezo` mezővel (félbemaradt, nem aktív). A fejléc (`fugg: []`, `nem_fugg: [121, 123, 146, 178, 179]`) a #728 befogadás szerint áll. **Megjegyzés az orkesztrátornak:** a 194 és a 212 a brief `nem_fugg` indoklásában nem szerepel; mindkettővel csak additív érintkezés van (`elofordulasok.tsv` új oszlop, `general.py` új `--cel` érték).
  *Proveniencia: `scope=feladatok.py fuggesek | forras=37f087cc | ts=2026-11-13`.*
- **Ellenőrzési szint.** `feladatok.py szint 218`: `teljes`, 2 kör.
- **Keret** (`get_usage`, 2026-11-13 09:05 UTC): heti (minden modell) 83%, heti Fable 15%, 5 órás 19%; a heti nullázás 2026-11-14 14:00 UTC.
- **A független ellenőr modellje** (`.claude/agents/fuggetlen-ellenor.md`): `opus`, tehát nem Fable.
