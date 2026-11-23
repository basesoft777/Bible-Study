# F239 — döntések (a TEREMT-001 cikke)

*Az integrátor döntései a menet kérdéseire (MUNKAMENET „Szereposztás”, #835); forrás: szerkesztői döntés (az integrátor, a felhasználó felhatalmazásával).*

**D1** (2026-11-23, U4b; az integrátor: `local_ee039369`). *Kérdés:* hova kerüljön a mérőtáblában az U3b-ben megfogott pontossági hiba (2Móz 15:5 βυθός → πόντος)? A SEMA 2.72 `hol` értékkészletében nem volt helye. — *Döntés:* (A) új `hol` érték: `visszhang` (a visszhang-réteg összevetése a prózával, U1b/U3b), és S022 sor a hibával, `sulyos=igen`. — *Indok:* a mérőtábla minden megfogott pontossági hibát számol; a kimaradó sor a „hol fogtuk meg” arányt torzítja, a lépés pedig a cikkírás menetének állandó része (C-vh a próza előtt, az összevetés utána). — *Végrehajtva:* S022 a `naplok/SZIVARGAS_TEREMT-001.tsv`-ben; a szabályhely a SEMA 2.72 és a MUNKAMENET C-sz (külön commit). Az értékkészletet gépi kapu nem ellenőrzi.
