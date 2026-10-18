# F117 4.2 — a szöveg-összevetés kis mintája (Hós 14, Én 6, Dán 3, Jón 2)

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` · végrehajtó: claude-opus-5-5 · 2026-10-18*

proveniencia: scope=Hós 14+Én 6+Dán 3+Jón 2 (64 Károli-vers) | forras=Karoli_1908.tsv + KJV_Strongs_teljes.tsv + TAHOT_kivonat.tsv (eszkozok/versmegf_szoveg_osszevet.py --minta; a Karoli_versmegfeleltetes.tsv olvasása nélkül) | kimenet=naplok/F117_szoveg_osszevetes.tsv | itelet=naplok/F117_itelet.tsv (scope=manual, modell=claude-opus-5-5) | szamlalas=naplok/F117_minta_kuszob.py | ts=2026-10-18

**Forrás-állapot (F117.8 (5)):** a napló minden száma a `33abc45a` commit állapotú `naplok/F117_szoveg_osszevetes.tsv`-ből jön (a 64 soros minta). A fájlt a teljes futás (4.3) azóta 483 sorra bővítette, ezért a mai fájlból a számok nem jönnek ki újra. Reprodukálás: `git show 33abc45a:naplok/F117_szoveg_osszevetes.tsv > minta.tsv`, majd `python naplok/F117_minta_kuszob.py minta.tsv` (2026-10-18 újrafuttatva: ugyanazok a számok).

## 1. Eredmény

| Fejezet | Károli-vers | Javasolt KJV | Fő horgony | Ítélet |
|---|---|---|---|---|
| Hós 14 | 10 | 14:1 → 13:16; 14:2–10 → 14:1–9 | Samaria (13:16), Israel/LORD (14:1), Asshur (14:3), Ephraim (14:8) | 10/10 egyezik |
| Én 6 | 10 | 6:1–10 → 6:4–13 | Tirzah (6:4), threescore/fourscore (6:8), Amminadib (6:12), Shulamite (6:13) | 10/10 egyezik |
| Dán 3 | 33 | 3:1–30 → 3:1–30; 3:31–33 → 4:1–3 | Dura (3:1), Shadrach/Meshach/Abed-nego, a „Peace be multiplied” levélnyitás (4:1) | 33/33 egyezik |
| Jón 2 | 11 | 2:1 → 1:17; 2:2–11 → 2:1–10 | three days and three nights (1:17), Jonah prayed (2:1), belly of hell (2:2), weeds (2:5) | 11/11 egyezik |

- **Egyezés:** a csak szöveg-jelű és a TAHOT-tal kiegészített igazítás mind a 64 versen ugyanazt a párt adja, és a kézi ítélet is ugyanezt. Minden lépés 1-1, a mintában nincs „nincs pár”, és összevonás sincs.
- **Következmény a 4.3-ra:**
  - A Hós 14:1 = KJV 13:16, ezért a Károli Hós 13 (15 vers) = KJV 13:1–15.
  - Az Én 6:1 = KJV 6:4, ezért a KJV 6:1–3 a Károli Én 5:17–19-re esik (az Én 5 is A-osztály).
  - A Dán 3:31–33 = KJV 4:1–3, ami összhangban áll a táblában már meglévő Dán 4:1 = KJV 4:4 sorral.
  - A Jón 2 a tábla mai identitás-sorait (D osztály) egy verssel eltolja.

## 2. A jelek viselkedése (a DT-F117b alapja)

- **A versenkénti szövegjel önmagában nem dönt.** A szomszéd-margó (a választott pár `s_szoveg`-e mínusz a ±1 eltolt KJV-versé) 7 helyes páron negatív, 16-on 0,05 alatt. Egy versszintű küszöb a 64 helyes párból ennyit jelölne bizonytalannak:
  - 20-at `s_szoveg ≥ 0,50` és `margó ≥ 0,05` mellett;
  - 13-at `≥ 0,50 / ≥ 0` mellett;
  - 8-at `≥ 0,40 / ≥ 0` mellett.
- **A döntést a monoton igazítás hozza.** A horgony-versek (`nev = 1` vagy `elso_utolso = 2`; Hós 14: 6/10, Én 6: 2/10, Dán 3: 9/33, Jón 2: 3/11) és a hosszprofil együtt rögzítik a sorrendet.
- **A TAHOT-Jaccard a választott páron erős** (min. 0,57, medián 0,95), de nem független jel (F85, `tahot_verskulcs_finomit.py`). A mintán nem változtatott a szöveg-igazításon.
- **Ismert gyengeség:** a névkulcs (mássalhangzóváz, első 3 mássalhangzó) a rövid nevekre gyenge (Jónás/Jonah: `ns`/`n`, Jón 2:1 `nev = 0,33`). A számnév-jel a mintában ritkán szól.
