// A BPRP magyar moduljának könyvnév-regexeit (csak a regex-literálokat, a modul kódját nem)
// veti össze a repó Konyv_normalizalo_tabla.tsv magyar rövidítéseivel és teljes neveivel.
import fs from 'fs';
const [huPath, tablaPath] = process.argv.slice(2);
const src = fs.readFileSync(huPath, 'utf8');
const re = /osis: \[([^\]]*)\][\s\S]*?regexp: (\/(?:\\.|[^\/\n])+\/[a-z]*)/g;
const minta = [];
for (const m of src.matchAll(re)) {
  const osis = m[1].replace(/"/g, '').split(',').map(s => s.trim());
  const lit = m[2];
  const i = lit.lastIndexOf('/');
  minta.push({ osis, rx: new RegExp(lit.slice(1, i), lit.slice(i + 1).replace('g', '')) });
}
const step2osis = {Gen:'Gen',Exo:'Exod',Lev:'Lev',Num:'Num',Deu:'Deut',Jos:'Josh',Jdg:'Judg',Rut:'Ruth','1Sa':'1Sam','2Sa':'2Sam','1Ki':'1Kgs','2Ki':'2Kgs','1Ch':'1Chr','2Ch':'2Chr',Ezr:'Ezra',Neh:'Neh',Est:'Esth',Job:'Job',Psa:'Ps',Pro:'Prov',Ecc:'Eccl',Sng:'Song',Isa:'Isa',Jer:'Jer',Lam:'Lam',Ezk:'Ezek',Dan:'Dan',Hos:'Hos',Jol:'Joel',Amo:'Amos',Oba:'Obad',Jon:'Jonah',Mic:'Mic',Nam:'Nah',Hab:'Hab',Zep:'Zeph',Hag:'Hag',Zec:'Zech',Mal:'Mal',Mat:'Matt',Mrk:'Mark',Luk:'Luke',Jhn:'John',Act:'Acts',Rom:'Rom','1Co':'1Cor','2Co':'2Cor',Gal:'Gal',Eph:'Eph',Php:'Phil',Col:'Col','1Th':'1Thess','2Th':'2Thess','1Ti':'1Tim','2Ti':'2Tim',Tit:'Titus',Phm:'Phlm',Heb:'Heb',Jas:'Jas','1Pe':'1Pet','2Pe':'2Pet','1Jn':'1John','2Jn':'2John','3Jn':'3John',Jud:'Jude',Rev:'Rev'};
function felismer(szoveg) {
  const t = new Set();
  for (const { osis, rx } of minta) { const m = rx.exec(szoveg); if (m && m.index === 0 && m[1] && szoveg.startsWith(m[1])) osis.forEach(o => t.add(o)); }
  return [...t];
}
const sorok = fs.readFileSync(tablaPath, 'utf8').split(/\r?\n/).slice(1).filter(Boolean);
let hiba = 0;
console.log(`minták: ${minta.length}`);
for (const sor of sorok) {
  const [step, rov, teljes] = sor.split('\t');
  const vart = step2osis[step];
  for (const [nev, alak] of [['rövidítés', rov], ['teljes', teljes]]) {
    const kap = felismer(`${alak} 1:1`);
    const ok = kap.includes(vart) && kap.length === 1;
    if (!ok) { hiba++; console.log(`HIÁNY/ELTÉRÉS\t${nev}\t${alak}\tvárt=${vart}\tkapott=${kap.join(',') || '—'}`); }
  }
}
console.log(`eltérés: ${hiba}`);
