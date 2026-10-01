# F21P_hosszarany.md — a prompt_v3 / prompt_v2 hosszarány (R)

<!-- GENERÁLT: eszkozok/karoli_strong/hosszarany.py | scope=a prompt_v3/prompt_v2 hosszarány (R = Σ L_v3 / Σ L_v2, a 20 köteg első próbálkozásának teljes bemeneti üzenete, KJV a minta szerint), 200 verses minta, v2 sha a9f0f07c67b9, v3 sha 84f12ca7aafb | forras=f21p/prompt_v2.md, f21p/prompt_v3.md, f21p/minta.tsv, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_*.tsv; a törölt ág értékei MANUAL (koordinátori közlés) | ts=2026-10-01T05:54:33+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

## Definíció

**R = Σ_k L_v3(k) / Σ_k L_v2(k)**, ahol k a 200 verses minta 20 kötegének (10 vers/köteg) egyike, és L(k) a k. köteg **első próbálkozásának teljes bemeneti üzenete**: a prompt utasításrésze (a példaversblokkokkal kibontva) + a keret + az összes versblokk, ahogy a `bemenet.kotegszoveg` összeállítja, KJV-támponttal a minta szerint. L = **karakterszám (Unicode kódpont)**; mellette az **UTF-8 bájtszám** (a héber/görög/magyar szöveg miatt a kettő eltér).

## Eredmény (a befagyasztott promptokra)

| mérőszám | v2 (a9f0f07c67b9) | v3 (84f12ca7aafb) |
|---|---|---|
| utasításrész, 1 köteg (karakter) | 7006 | 8435 |
| utasításrész, 1 köteg (bájt) | 7654 | 9260 |
| utasításrész, 20 köteg (karakter) | 140120 | 168700 |
| versblokkok, 20 köteg (karakter) | 161950 | 161950 |
| keret, 20 köteg (karakter) | 800 | 800 |
| **összhossz, 20 köteg (karakter)** | **302870** | **331450** |
| összhossz, 20 köteg (bájt) | 338049 | 370169 |

**R (karakter) = 1.0944; R (UTF-8 bájt) = 1.0950.** A versblokkok összhossza a két prompttal azonos (161950 karakter); a különbség (28580 karakter) kizárólag az utasításrészből jön (1429 karakter/köteg).

## A törölt ág 1,0491-es értéke

A törölt ág (`claude/f21-regresszio`) 1,0491-et mért (MANUAL, koordinátori közlés). Ennek oka **nem a definíció, hanem a prompt**: az ő prompt_v3-ja rövidebb volt (a 20 köteg összhossza 317730 karakter), a mienk a befagyasztott prompt_v3 (331450 karakter). A különbség 13720 karakter, azaz kötegenként ~686 karakter. A v2 összhossza (302870) ugyanaz, így a két arány a prompt eltéréséből adódik; a pilot aranya és promptja a befagyasztott (R = 1.0944). A szárazbecslés (`futtat.py --szaraz`) ezt az R-t használja.

