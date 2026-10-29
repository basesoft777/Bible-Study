# ISTENTISZT-001 — az Ézs 64:6 és a Zsolt 99:6 jelölt lezárása (2026-10-29)

Modell: `claude-opus-5-5`. Ág: `claude/istentiszt-ezs64-zsolt99-2a63f0`, alap: `origin/main` ea85486c (benne e86eb12d, PR #504).

## A döntés

A felhasználó az orkesztrátor chatjében, 2026-10-29-én, szó szerint: „Igen, így”. A kérdés: „Ézs 64:6 beépítve, Zsolt 99:6 elutasítva?” A gomb szövege: „Igen: az Ézs 64:6 beépítve (tagadó forma, a Jer 10:25 mintájára), a Zsolt 99:6 elutasítva a negatív kritérium szerint (nincs בְּ a név előtt; a DT283 JSir 3:55-előzménye), a kritérium nem változik.”

## Saját mérés (egyezik az orkesztrátor mérésével)

| Lekérdezés | Proveniencia |
|---|---|
| `lekerdez.py kollokacio H7121 H8034` (mindkét vers a 196 közt) | scope=TAHOT-teljes+TAGNT-teljes \| forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv \| strong=H7121+H8034 \| n=196 \| ts=2026-10-29T08:32Z \| csatorna=cli |
| `lekerdez.py karoli "Ézs 64:6"` | scope=range:Ézs 64:6 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=1 \| ts=2026-10-29T08:31Z \| csatorna=cli |
| `lekerdez.py karoli "Zsolt 99:6"` | scope=range:Zsolt 99:6 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=2 \| ts=2026-10-29T08:31Z \| csatorna=cli |
| `lekerdez.py lxx-hid "Ézs 64:6"` | scope=range:Ézs 64:6 \| forras=LXX_OS/isaiah.tsv+TAGNT_kivonat.tsv \| n=27 \| ts=2026-10-29T08:32Z \| csatorna=cli |

Mind a négy sor az `adat/auditok.tsv`-ben (`--naplo ISTENTISZT-001 --lepes adhoc`). A TAHOT-tokenek a Károli-kulcson, `split('\t')`-tel olvasva.

- **Ézs 64:6.** Károli: „S nem volt, a ki segítségül hívta volna nevedet”. TAHOT: וְ + אֵין (H0369) + קוֹרֵא (H7121) + בְ (H9003) + שִׁמְ (H8034) + ךָ (Ps2m). Aktív kárá + בְּ + a megszólított Isten neve, emberi alany, tagadó forma. LXX: οὐκ ἔστιν ὁ ἐπικαλούμενος (G1941) τὸ ὄνομά σου.
- **Zsolt 99:6.** TAHOT: וּשְׁמוּאֵל + בְּ (H9003) + קֹרְאֵי (H7121) + שְׁמוֹ (H8034 + Ps3m) + קֹרִאים (H7121) + אֶל (H0413) + יְהוָה. A בְּ az igenév előtt áll („azok között, akik hívják”), a név az igenév birtokos szerkezetében; a második tagban אֶל. Kárá + בְּ + név nincs, a negatív kritérium (`adat/motivumok.tsv`) kizárja; előzmény: DT283 (JSir 3:55, 5Móz 32:3). Mellékesen: a BDB a verset a H7121 Qal 3.b-hez („a nevet kihirdetni”) sorolja, nem a 2.c-hez (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, szótári szakasz).

## Az új `elofordulasok.tsv` sor mezőválasztása

Minta: a Jer 10:25 és a Zsolt 79:6 sora (`Remez`; `2.c (tagadva)`).

| Mező | Érték | Indok |
|---|---|---|
| `pardes_szint` | Remez | mint a két tagadó sor |
| `funkcio` | 🚫 tagadó forma — a formula elmulasztása, a nép önmagáról mondva, egyenes szórenddel | A Jer/Zsolt 79:6 funkciójából a „⇄ párhuzam” és a „vád, fordított szórenddel” nem illik: a két vers egymás párhuzama, az Ézs 64:6 nem; a TAHOT-ban az ige áll a név előtt; a vers első személyű többes (tőlünk, minket: Op1c, Pp1c), nem a nemzetek elleni vád. |
| `gerinc_elem`, `strong` | H7121+H8034 | |
| `lexikon_szotar` / `lexikon_entry_id` / `jelentes_szam` | BDB / H7121 / 2.c (tagadva) | mint a két tagadó sor |
| `jelentes_hu` | invokálni — tagadó szerkezetben | a Jer-sor „a mulasztás vádjaként” része nélkül (l. funkció) |
| `karoli_szo` | segítségül hívta volna nevedet | a jelölt-sorral azonos (SEMA 2.2: öröklődik) |
| `azonositas_modja` / `megbizhatosag` | tartalom-alapú / magas | nincs `karoli_variancia` megerősítés, így nem `szó-szintű-gépi` |
| `proveniencia` | a mai kollokáció-sor | precedens: TEREMT-002 Jer 4:23 |
| `igazolas` | TAHOT-igazolt | a H7121 és a H8034 a TAHOT Károli-kulcsú sorában áll |
| `forras_tanulmany` | üres | a lelet nem tanulmányban merült fel (F110 szűrő), mint a Jer 10:25-nél |

Szkript: `naplok/ISTENTISZT001_ezs64_zsolt99_ir.py` (írás előtt soronkénti összevetés: a `jeloltek.tsv` két sora, az `elofordulasok.tsv` egy új sora változott).
