# F83_zaras.md — #83 JOB_VERSBEOSZTAS zárójelentés

*2026.10.08 · ág: `claude/f83-job-versbeosztas` · modell: opus (`vegrehajto-opus`) · ellenőrzés: `naplok/ELLENOR_F83.md`*

**Eredmény.** A Károli Jób 38–42 versszáma 38/38/19/34/17, az MT-é 41/30/32/26/17, összesen mindkettő 146. A briefben szereplő „40 = 28, 41 = 25” téves volt. Mind a 146 vers 1:1, 1:2 / 2:1 eset nincs. A fejezethatár négy helyen tolódik (Károli 39:1–3 = MT 38:39–41; 39:34–38 = 40:1–5; 40:1–19 = 40:6–24; 41:1–34 = 40:25–41:26). A Jób 42:2–9 hiányának gyanúja nem igazolódott. A `TAHOT_kivonat` Jób 40-es kulcsai MT-számozásúak, a Jób 41-hez 0 sora van: ez kulcsgenerátor-hiba, a héber szöveg a Macula-ban megvan.

**Jóváhagyás** (felhasználó, chat, 2026.10.08): a megfeleltetés és a DT85 (1) opciója — nincs összevonás-támogatás, kézi tábla. Végrehajtva: `f22/versmegfeleltetes_kezi.tsv` +19 sor (Károli 40:n → TAHOT 40:(n+5)), jóváhagyási sor a `naplok/F22_versbeosztas_jovahagyas.md`-ben, DT85 ✅.

**Egyeztetett eltérés.** Az 1. ellenőrzés forrása a `Macula_heber_Job.tsv` volt (letöltés nélkül). Az N-F41g külön tétel maradt.

**Folyamati esemény.** Egy párhuzamos F23-session a közös munkakönyvtárban két commitot (4d6b469, fe9a870) tett erre az ágra. A force-push-t az automatikus mód letiltotta, ezért az F83.4 reverttel semlegesítette őket. A nettó diff csak az F83 fájljait tartalmazza (ELLENOR_F83 igazolja).

**Nyitott (a felhasználóé, `/befogad`).**
- **N-F83a [javaslat]:** a TAHOT-kulcsgenerátor (`eszkozok/tahot_karoli_kulcs_generalas.py`) Jób 40–41 javítása, a CLAUDE.md TAHOT-korlát mondatának pontosításával. Amíg ez nincs meg, a Jób 41 nem futtatható, és az `ad` csak részben teljesül.
- A #22 Jób-menetének első lépése a Jób felvétele a `VERSBEOSZTAS_JOVAHAGYOTT`-ba. Ugyanez a menet nézi át a detektor Jób 17 és 37 sorait (a jelentés 6. szakasza).
