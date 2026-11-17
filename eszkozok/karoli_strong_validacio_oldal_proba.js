// F175.V — az ellenorzo.html szkriptjének próbája Node-on (DOM-utánzat), a megjelenítés nélkül.
// Hívja: eszkozok/teszt_karoli_strong_validacio.py (Oldal), ha a node elérhető. Kilépési kód 1 hibánál.
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const kod = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
const ids = [...html.matchAll(/id="([^"]+)"/g)].map(m => m[1]);
function Elem(tag) {
  const cl = new Set();
  const e = { tagName: tag || 'div', children: [], attrs: {}, style: {}, hidden: false, value: '', checked: false, files: [],
    _t: '', listeners: {}, open: false,
    classList: { add: c => cl.add(c), remove: c => cl.delete(c), toggle: (c, f) => { if (f === undefined ? !cl.has(c) : f) cl.add(c); else cl.delete(c); }, contains: c => cl.has(c) },
    get className() { return [...cl].join(' '); }, set className(v) { cl.clear(); String(v).split(/\s+/).filter(Boolean).forEach(x => cl.add(x)); },
    get textContent() { return this._t + this.children.map(c => c.textContent).join(''); }, set textContent(v) { this._t = String(v); this.children = []; },
    set innerHTML(v) { this._t = ''; this.children = []; },
    appendChild(c) { this.children.push(c); return c; }, append(...cs) { cs.forEach(c => this.children.push(typeof c === 'string' ? { textContent: c } : c)); },
    setAttribute(k, v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k]; },
    addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); },
    click() { (this.listeners.click || []).forEach(f => f({ currentTarget: this, target: this })); },
    remove() {}, select() {} };
  return e;
}
const elemek = {}; ids.forEach(i => elemek[i] = Elem());
const radiok = ['rossz_forrasszo', 'hianyzo_par', 'folosleges_par', 'egyeb'].map(v => { const r = Elem('input'); r.value = v; return r; });
const tar = {};
global.localStorage = { getItem: k => (k in tar ? tar[k] : null), setItem: (k, v) => { tar[k] = String(v); }, clear: () => { for (const k in tar) delete tar[k]; } };
let confirmValasz = true, confirmHivas = 0;
global.confirm = () => { confirmHivas++; return confirmValasz; };
global.alert = () => {};
global.window = { scrollTo() {} };
global.navigator = {};
global.FileReader = function () { this.readAsText = (f) => { this.result = f.tartalom; this.onload(); }; };
global.Blob = function (p) { this.p = p; };
global.URL = { createObjectURL: () => 'blob:x', revokeObjectURL() {} };
global.setTimeout = (f) => 0;
global.document = { getElementById: i => elemek[i], createElement: t => Elem(t), createTextNode: s => ({ textContent: s }),
  querySelectorAll: s => s.startsWith('input[name=hibatipus]') ? radiok : [], addEventListener() {}, body: Elem(), execCommand() {} };
// a szkript globális függvényei a teszthez
const futtat = new Function(kod + '\nreturn {get allapot(){return allapot}, set allapot(v){allapot=v}, uj_allapot, itelet_valt, lep, export_obj, betolt, betolt_adat, kesz_db, MINTA, MINTA_HASH, kulcs, tetel, valasz, ment};');
let A = futtat();
const hiba = []; const ell = (f, uz) => { if (!f) hiba.push(uz); };

// 1. indulás névvel, kitöltés
elemek['i-nev'].value = 'Próba Ellenőr'; elemek['b-indul'].click();
ell(A.allapot && A.allapot.ellenor === 'Próba Ellenőr', 'indulás');
const itelet = ['helyes', 'hibas', 'bizonytalan'];
for (let i = 0; i < 120; i++) {
  A.itelet_valt(itelet[i % 3]);
  if (i % 3 === 1 && A.tetel().tipus === 'par') { const r = radiok[i % 4]; r.listeners.change[0](); }
  if (i % 7 === 0) { elemek['t-megj'].value = 'megj ' + i; elemek['t-megj'].listeners.input[0](); }
  if (i % 13 === 0) { elemek['t-segedeszkoz'].value = 'BDB'; elemek['t-segedeszkoz'].listeners.input[0](); }
  if (i % 11 === 0) {   // fordítói észrevétel (nem ítélet)
    elemek['i-karoli'].checked = true; elemek['i-karoli'].listeners.change[0]();
    elemek['t-karoli-megj'].value = 'szabad fordítás ' + i; elemek['t-karoli-megj'].listeners.input[0]();
  }
  A.lep(1);
}
ell(A.kesz_db() === 120, 'kész 120: ' + A.kesz_db());
// közös blokk: minden ellenőrnél elöl, ugyanaz a halmaz, más sorrend
{ const kb = A.MINTA.filter(t => t.kb).length;
  const s1 = A.allapot.sorrend, s2 = A.uj_allapot('Másik Ellenőr').sorrend;
  const m1 = new Set(s1.slice(0, kb)), m2 = new Set(s2.slice(0, kb));
  ell(kb === 300, 'közös blokk mérete: ' + kb);
  ell(s1.slice(0, kb).every(id => A.MINTA.find(t => t.id === id).kb === 1), 'a közös blokk áll elöl');
  ell([...m1].every(id => m2.has(id)) && s1.slice(0, kb).join() !== s2.slice(0, kb).join(), 'ugyanaz a blokk, más sorrend'); }
// a kimaradt-pár tétel: „Van párja” -> hibás, automatikus hibatípussal
{ const p0 = A.allapot.poz; const ki = A.allapot.sorrend.findIndex(id => A.MINTA.find(t => t.id === id).tipus === 'kimaradt' && !A.allapot.valaszok[id]);
  ell(ki >= 0, 'van kimaradt-pár tétel');
  A.allapot.poz = ki; A.itelet_valt('hibas');
  ell(A.valasz(A.tetel()).hibatipus === 'kimaradt_par', 'kimaradt: hibatípus');
  A.itelet_valt('hibas');   // visszavonás (ugyanaz a gomb)
  A.allapot.poz = p0; }
// ítélet nélküli tétel, csak a fordítói jelölővel: nem számít késznek, de exportálódik
const csakKaroliId = A.tetel().id;
elemek['i-karoli'].checked = true; elemek['i-karoli'].listeners.change[0]();
ell(A.kesz_db() === 120, 'a jelölő nem ítélet');
ell(!elemek['emlek'].classList.contains('rejtett') && /100 tétel/.test(elemek['emlek-szoveg'].textContent), 'emlékeztető 100-nál: ' + elemek['emlek-szoveg'].textContent);
ell(A.allapot.emlek === 100, 'emlék küszöb: ' + A.allapot.emlek);
// 2. export
elemek['b-export'].click();
const exp = JSON.parse(elemek['m-json'].value);
ell(exp.kesz === 120 && Object.keys(exp.valaszok).length === 121 && exp.minta_hash === A.MINTA_HASH, 'export: ' + Object.keys(exp.valaszok).length);
ell(exp.valaszok[csakKaroliId] && exp.valaszok[csakKaroliId].karoli === true && !exp.valaszok[csakKaroliId].itelet, 'a csak jelölős tétel exportálva');
ell(Object.values(exp.valaszok).filter(x => x.segedeszkoz === 'BDB').length === 10, 'segédeszköz: ' + Object.values(exp.valaszok).filter(x => x.segedeszkoz).length);
ell(Object.values(exp.valaszok).filter(x => x.karoli && /szabad fordítás/.test(x.karoli_megj)).length === 11, 'jelölők megjegyzéssel: ' + Object.values(exp.valaszok).filter(x => x.karoli).length);
// 3. tiszta állapot (localStorage törlése, új oldalbetöltés), azonos név, betöltés
localStorage.clear();
ids.forEach(i => { elemek[i] = Elem(); }); radiok.forEach(r => { r.listeners = {}; }); A = futtat();
elemek['i-nev'].value = 'Próba Ellenőr'; elemek['b-indul'].click();
ell(A.kesz_db() === 0, 'tiszta állapot');
elemek['i-betolt'].files = [{ tartalom: JSON.stringify(exp) }];
elemek['i-betolt'].listeners.change[0]({ target: elemek['i-betolt'] });
const exp2 = A.export_obj();
{ const k1 = Object.keys(exp.valaszok), k2 = Object.keys(exp2.valaszok); const elt = k1.filter(k => JSON.stringify(exp.valaszok[k]) !== JSON.stringify(exp2.valaszok[k])); ell(k1.length === k2.length && elt.length === 0, 'minden válasz visszajött: ' + k1.length + '/' + k2.length + ' eltér: ' + elt.slice(0,3).map(k => JSON.stringify(exp.valaszok[k]) + ' vs ' + JSON.stringify(exp2.valaszok[k])).join(' ; ')); }
ell(JSON.stringify(exp2.sorrend) === JSON.stringify(exp.sorrend), 'sorrend azonos');
const info1 = elemek['m-betolt-info'].textContent;
// 4. ütközés: egy tétel itt később módosul, a fájlban régebbi -> az itteni marad; a fájlban újabb -> a fájlé
const [id1, id2] = exp.sorrend;
A.allapot.valaszok[id1] = Object.assign({}, A.allapot.valaszok[id1], { itelet: 'bizonytalan', ido: '2099-01-01T00:00:00.000Z' });
const exp3 = JSON.parse(JSON.stringify(exp));
exp3.valaszok[id2] = Object.assign({}, exp3.valaszok[id2], { itelet: 'hibas', hibatipus: 'egyeb', ido: '2099-01-02T00:00:00.000Z' });
A.ment();
const uz = A.betolt_adat(exp3);
ell(A.allapot.valaszok[id1].itelet === 'bizonytalan', 'az itteni újabb válasz megmaradt');
ell(A.allapot.valaszok[id2].itelet === 'hibas', 'a fájl újabb válasza átjött');
ell(/1 tételnél/.test(uz), 'üzenet a megtartottról: ' + uz);
// 5. más mintához tartozó fájl: elutasítás, állapot változatlan
const elotte = JSON.stringify(A.allapot);
let rossz = ''; try { A.betolt_adat(Object.assign({}, exp, { minta_hash: 'deadbeef' })); } catch (e) { rossz = e.message; }
ell(/másik mintához/.test(rossz) && JSON.stringify(A.allapot) === elotte, 'idegen minta elutasítva: ' + rossz);
// 6. más ellenőr fájlja: rákérdez; "Mégsem" -> nincs változás
confirmValasz = false;
const masik = Object.assign({}, exp, { ellenor: 'Másik Ember' });
const uz2 = A.betolt_adat(masik);
ell(confirmHivas === 1 && /Mégsem/.test(uz2) && JSON.stringify(A.allapot) === elotte, 'más ellenőr: rákérdezés, Mégsem');
console.log(hiba.length ? 'HIBA:\n  ' + hiba.join('\n  ') : 'RENDBEN (9 forgatókönyv)');
if (hiba.length) process.exitCode = 1;
console.log('minta_hash: ' + A.MINTA_HASH);
console.log('betöltési üzenet: ' + info1);
console.log('ütközés: ' + uz);
