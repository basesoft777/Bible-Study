# F22_1Moz_jelentes.md — Károli–Strong párosítás: 1Mózes

*A számok kizárólag szkriptkimenetből jönnek (`eszkozok/karoli_strong/f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`). Állapot: a menet közben épül; a 2. szakasz a 22.5-ben készül.*

## 1. Próbaszakasz (22.2): az első 14 köteg

**Hatókör.** A brief „1Móz 1–5, 138 vers, 14 köteg” megnevezése és a 10 verses kötegelés nem esik egybe: az első 14 köteg 140 vers (az 1–5. fejezet 138 verse + 1Móz 6:1–2). Mindkét modell ugyanezt a 14 kötegét futtatta; a vetítés a ténylegesen futtatott 140 versre épül (×1 533/140).

**Beállítások.** Prompt: `f21p/prompt_v3.md` (hash a futás elején rendben). Bemenet KJV-támpont nélkül (a brief szerint a KJV a promptban nem igazolt; a pilot Sonnet- és C-futásai a KJV-sort ott adták, ahol volt). Sonnet: `vegrehajto-sonnet` subagentek, kötegenként egy, sorban. C: `google/gemini-3.8-flash`, GitHub Actions, kötelező minimális gondolkodási szint (`kotelezo_effort=minimal`).

**Szkriptkimenet (`f22_statisztika.py --konyv 1Móz --ig-koteg 14 --vetit 1533`):**

```
Sonnet: 14 köteg, 140 vers; kapuhiba első próbára 0.7% (1/140); végleg 0.0% (0/140)
C: 14 köteg, 140 vers; kapuhiba első próbára 6.4% (9/140); végleg 0.0% (0/140)
C költség: 0.183644 USD, 17 hívás, bemenet 146937, kimenet 21053 (ebből gondolkodás 0) token
C költség vetítve 1533 versre: 2.0109 USD
```

**A /usage állása** (`get_usage`, a heti keret „all models” ablaka; az érték egész százalék):

| időpont | heti keret | 5 órás ablak |
|---|---|---|
| a menet kezdetén (az 1. köteg előtt, az előkészítés — minta, szkriptek, workflow — után) | 36% | 22% |
| a 14 köteg után | 37% | 25% |

A mért heti fogyás a 14 kötegre 1 százalékpont (az egész százalékos kerekítés miatt 0–2 pont közötti valódi érték), az 5 órás ablakban 3 pont. Vetítés a teljes 1Mózesre (×1 533/140 ≈ 10,95): kb. 11 százalékpont (0–22 pont sáv) a heti keretből. A 30%-os küszöb a heti keret százalékpontjára vonatkozik; a mérés durvasága miatt a 22.3 alatt a `/usage`-t kötegcsoportonként újramérem.

**⛔ 1. megállás feltételei** (egyik sem teljesül):

| feltétel | mért/vetített | küszöb | teljesül? |
|---|---|---|---|
| vetített keretfogyás | kb. 11 pont (sáv: 0–22) | > 30% | nem |
| Sonnet végleges kapuhiba | 0,0% | > 5% | nem |
| C költségének vetítése | 2,01 USD | > 3,90 USD | nem |

A 22.3 megállás nélkül folytatódik.
