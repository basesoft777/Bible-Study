# F21 — véletlen helyi éles hívás (F8V3, 2 köteg), 2026.10.01

*Kézi rögzítés. Proveniencia: manual (az orkesztrátor jegyzete a végrehajtó jelentése és a munkafa alapján).*

- **Mi történt:** az F8V3 építése közben egy végrehajtó ügynök ellenőrzésképpen `futtat.py --vezerlo <teszt-fájl>` parancsot futtatott `| head -3` csővel. A helyi környezetben ott volt az `OPENROUTER_API_KEY`, ezért a futtató élesen elindult, és két köteg (az 1. és a 2., mind R1) lefutott, mielőtt a cső megszakította. Ez a futás nem a workflow-trigger útján, helyben történt, a felhasználó megbízásán kívül.
- **Költség:** 0,023232 USD (0,010915 + 0,012317); a futásnapló két F8V3 sora rögzíti (`futo_osszeg` 1,876119, majd 1,888435).
- **Döntés (az orkesztrátor, visszafordítható):** az adat megmarad a pilot rekordjában: a naplósorok valós költséget rögzítenek, és a két köteg érvényes F8V3-adat (azonos futtató, `prompt_v3`, `prompt_sha256_12` 84f12ca7aafb, a teljes KJV-tábla, a C `minimal` lánca). Az Actions-futás a kész kötegeket kihagyja, így a maradék 18 köteg fut. Ha tiszta lap kell, a `f21p/valaszok/F8V3.jsonl` és a két naplósor elhagyható, és a két köteg újrafuttatása kb. 0,023 USD.
- **Megelőzés:** a `futtat.py` (F21.64) éles OpenRouter-hívást helyben nem engedélyez: csak `GITHUB_ACTIONS=true` mellett vagy kifejezett `F21_ELES_HELYI=igen` beállítással. A mock-küldős tesztek nem érintettek.
- **Mellékhatás (visszaállítva):** a mérő szkriptek (`meres.py`, `jelentes_f21p.py`) az `--onteszt` mellett is valódi kimenetet írtak; három követett fájl módosult (`meres_eredmeny.tsv`, `F21P_jelentes.md`, `F21P_meres_v1.md`), ezeket a végrehajtó `git checkout`-tal visszaállította.
