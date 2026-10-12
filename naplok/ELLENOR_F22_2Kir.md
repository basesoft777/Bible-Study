# ELLENOR_F22_2Kir — F22_KAROLI_STRONG_BRIEF.md (D32, v2.26), `6c1acf69..7e1145af`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-2kir`; commitok: `1b5a6510`, `9b862823`, `7e1145af`.*

ELTÉRÉS: 1 tétel

## Igazolt (saját lekérdezéssel)

- **719/719 vers, 25 fejezet:** a `Karoli_1908.tsv` `^2Kir ` sorai 719; minden versnek van hu és er sora a szavak-táblában; a `minta_2Kir.tsv` 719 + fejléc; a 72. köteg `igehely_db=9`.
- **parok_2Kir 18 184:** mind `alacsony / S`, mindegyiknek van H-Strongja.
- **szavak_2Kir 36 736:** hu 18 102 (14 668 `parositva`, 3 434 `betoldas`), er 18 634 (16 625 `parositva`, 2 009 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^2Kir ` sorai (18 634); `kezi` / `fuggoben` 0.
- **Kapuhiba 21/719 → 0:** az 1. körben 12 köteg bukott (4, 5, 6, 7, 18, 21, 27, 28, 29, 38, 44, 47): 11 köteg 1-1 vers, a k047 10 vers (egész kötet formátumhibás), összesen 21; a javító kör 12 sora mind 0 / `igen`.
- **Költség:** 1. kör 5,294981, 2. kör 0,336335, összesen 5,631316 USD; a 2. kör tokenjei 175 020 / 32 263; kumulatív 73,960245 USD, a 2Kir-sorok `futo_osszeg_usd` értéke szigorúan monoton, a 68,328929-es kezdőérték az 1Kir és a Neh együttes összege. Plafon 7,98; versenként 0,0078.
- **Batchek:** 72 + 12 kérés, 12:16:12Z és 12:20:36Z.
- **K9:** `adat/datasetek.tsv` 8 sor (a 4 parok-sor jelentéslistájában is a 2Kir), `adat/SEMA.md` 2.20; az 1Kir és a Neh megmaradt, duplázás nincs.
- **`tokenek.py`:** `…, '1Kir', 'Neh', '2Kir')`.
- **Jóváhagyás:** a jóváhagyási naplóban és a D32 sorban a chat-idézet áll; a jóváhagyó commit (12:15:43Z) 29 másodperccel a batch (12:16:12Z) előtt készült.
- **Régi arany 1/1:** `2Ki.5.11 H7121+H8034`; `lekerdez.py scan` mindkettőre n=1. További szúrópróba: H6586 (2Kir 1:1), H1364 (2Kir 17:10): n=1.
- **Kulcs-grep:** 0. **E2–E16, E19, E20, E26:** 0; E25: 3 és E27: 32, repószintű, nem e diffből. **A6 (E12–E15):** 0.

## ELTÉRÉS

1. **(alacsony)** A „Dán (37 detektorsor) előtt versbeosztás-döntés kell” indoka elavult: a `f22/versmegfeleltetes.tsv`-ben 0 Dán-sor van az F85.6/F85.8 óta (`naplok/F85_jelentes.md`). A szöveg a base-ből öröklődött, a diff a jelentésben megismételte. **Javítva** a briefben és a jelentésben.

## Nem ellenőrizhető a szerepkörből

`egyesit.py --ellenoriz` és a K7 újraépítés (a fő session futása: „rendben”), a hu oldal tokenszáma (K1), az 1. kör tokenösszege (869 286 / 885 139), a BDB-mérés 413 / 87 értéke, a chatben adott jóváhagyás („mehet a 2Királyok”), a prompt-hash viszonya a `f21p/prompt_v3.sha256`-hoz (mind az 1 431 `api_termeles/` sor `84f12ca7aafb`).

## Megjegyzés (nem eltérés)

A futásnapló az 1297/1298. és az 1348/1349. sorhatáron soronként nem folytonos; a 2Kir-lánc értéke a helyes kumulatív összeg, a régi sorok a DT72 miatt nem íródtak át. A k047 egész kötege formátumhibás volt; a D32 ezt most kiírja.
