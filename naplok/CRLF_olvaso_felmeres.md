# CRLF-sérülékeny táblaolvasók — jelöltlista (2026-10-29)

*Az E19 `KeyError: 'illesztes'` (`test_szabalyok`, csak Windowson) után, az orkesztrátor kérésére. Előállítja: `python naplok/CRLF_olvaso_felmeres.py`. Heurisztika: `newline=''`-es nyitás + `split('\n')`, a környéken `\r`-kezelés nélkül. Kézi átnézés kell: van köztük író oldali `sorveg.join(…split('\n'))` és tudatosan ellenőrzött eset (pl. `bdb_atvezet_m5.py:29`), ezek nem hibák. Ebben a PR-ben csak a `thayer_jelolt/thayer_bemenet.py` két olvasója javult (`tabla_olvas`, `javitas_olvas`); a többi külön feladat.*

```
sérülékeny jelölt: 58 (ebből teszt: 17)
eszkozok/bdb_aram_beemeles.py:64  sorok = [l.split('\t') for l in f.read().split('\n') if l]
eszkozok/bdb_aram_beemeles.py:74  for n, sor in enumerate(f.read().split('\n'), 1):
eszkozok/bdb_aram_potlas.py:62  sorok = [l.split('\t') for l in f.read().split('\n') if l]
eszkozok/bdb_aram_potlas.py:361  sorok = [l.split('\t') for l in f.read().split('\n') if l]
eszkozok/bdb_aram_potlas.py:412  for n, sor in enumerate(f.read().split('\n'), 1):
eszkozok/bdb_atvezet_m5.py:29  return szoveg.split('\n')  # \r\n eseten a sorveg a vegso mezoben maradna; lent ellenorizve
eszkozok/bdb_jelolt/forras_javit.py:101  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/forras_javit.py:157  sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
eszkozok/bdb_jelolt/forras_javit.py:220  tsv = {s.split('\t')[0]: s.split('\t')[2] for s in f.read().split('\n')[1:] if s}
eszkozok/bdb_jelolt/forras_osszevetes.py:161  tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
eszkozok/bdb_jelolt/hu_illeszt.py:245  s = f.read().split('\n')
eszkozok/bdb_jelolt/nezet_ellenoriz.py:54  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/nezet_ellenoriz.py:85  tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
eszkozok/bdb_jelolt/nezet_general.py:53  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/nezet_general.py:144  tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
eszkozok/bdb_jelolt/nezet_hatas.py:50  return {s.split('\t')[0]: s.split('\t')[2] for s in f.read().split('\n')[1:] if s}
eszkozok/bdb_jelolt/nezet_hatas.py:95  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/nezet_hatas.py:111  sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
eszkozok/bdb_jelolt/szerkezet_osszevet.py:77  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/teszt_bont.py:27  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/teszt_bont.py:192  sorok = f.read().split('\n')
eszkozok/bdb_jelolt/teszt_bont.py:263  s = f.read().split('\n')
eszkozok/bdb_jelolt/teszt_bont.py:287  s = f.read().split('\n')
eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py:220  sorok = f.read().split('\n')
eszkozok/bdb_konyv_javit.py:111  sorok = open(path, encoding='utf-8', newline='').read().split('\n')
eszkozok/bdb_konyv_javit.py:711  fs = open(FORD, encoding='utf-8', newline='').read().split('\n')
eszkozok/bdb_konyv_javit.py:1147  sorok = open(FORRAS, encoding='utf-8', newline='').read().split('\n')
eszkozok/bdb_psi_javit.py:282  sorok = nyers.split('\n')
eszkozok/bdb_psi_javit.py:325  fs = fnyers.split('\n')
eszkozok/bdb_sorrend_ujragen.py:41  sorok = f.read().split('\n')
eszkozok/bdb_strong_potlas.py:128  for sor in szoveg.split('\n')[1:]:
eszkozok/emeles.py:152  for sor in fh.read().split('\n'):
eszkozok/emeles.py:702  sorok = eredeti.split('\n')
eszkozok/emeles.py:962  sorok = eredeti.split('\n')
eszkozok/f08/f08_dontesek.py:326  sorok = nyers.split('\n')
eszkozok/f91_versmegf_javit.py:38  return data.split('\n')
eszkozok/g2_forrasreteg_levalasztas.py:282  f.write(sorveg.join(uj.split('\n')))
eszkozok/g7_index_atszervezes.py:230  f.write(sorveg.join(uj_szoveg.split('\n')))
eszkozok/general.py:146  sorok = fh.read().split('\n')
eszkozok/general.py:994  f.write(sorveg.join(szoveg_lf.split('\n')))
eszkozok/istentiszt_2b_d3_szerkeszt.py:32  sorok = f.read().split('\n')
eszkozok/karoli_strong/f22_c_futtat.py:270  sorok = uj.split('\n')
eszkozok/teszt_bdb_aram_potlas.py:20  sorok = [l.split('\t') for l in f.read().split('\n') if l]
eszkozok/teszt_bdb_strong_potlas.py:121  kulcsok = [l.split('\t')[0] for l in f.read().split('\n')[1:] if l]
eszkozok/teszt_feladatterkep.py:291  sorok = f.read().split('\n')
eszkozok/teszt_forditas_kapuk.py:650  sorok = [s for s in fh.read().split('\n') if s and not s.startswith('#')]
eszkozok/teszt_lekerdez_naplo.py:87  return f.read().split('\n')[:-1]
eszkozok/teszt_versmegf_javitas.py:30  s = f.read().split('\n')
eszkozok/thayer_jelolt/bont.py:250  sorok = [x for x in f.read().split('\n') if x and not x.startswith('#')]
eszkozok/thayer_jelolt/forditas.py:189  sorok = eredeti.split('\n')
eszkozok/thayer_jelolt/teszt_bont.py:30  sorok = f.read().split('\n')
eszkozok/thayer_jelolt/teszt_bont.py:165  for s in f.read().split('\n')[3:]:
eszkozok/thayer_jelolt/teszt_bont.py:176  sorok = f.read().split('\n')
eszkozok/thayer_jelolt/teszt_lanc.py:440  uj = f.read().split('\n')
eszkozok/thayer_jelolt/teszt_lanc.py:441  regi = eredeti.split('\n')
eszkozok/thayer_jelolt/teszt_vers_jelentes.py:30  s = f.read().split('\n')
eszkozok/versmegf_javitas.py:195  return data.split('\n')
eszkozok/zsolt_felirat_halmaz.py:41  return f.read().split('\n')
```
