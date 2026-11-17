// F175.V21 — az online ellenőrző oldal (public/index.html) és a Worker-logika együttes próbája Node-on,
// kitalált adattal: a kliens fetch-hívásai közvetlenül a Worker kezelőjéhez mennek (D1 helyett node:sqlite).
// Forgatókönyvek: két eszköz ugyanazzal a tokennel, megszakított hálózat (küldési sor, újrapróbálás, összevonás),
// újratöltés el nem küldött változással, „Kész”, érvénytelen és hiányzó token, sérült minta-azonosító.
// Hívja: eszkozok/teszt_karoli_strong_validacio.py (Online). Kilépési kód 1 hibánál.
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { kezel } from '../src/logika.js';
import { D1Utanzat, kitalalt_tetelek, betolt } from './d1_utanzat.mjs';

const ITT = path.dirname(fileURLToPath(import.meta.url));
const OLDAL = process.argv[2] || path.join(ITT, '..', 'public', 'index.html');
const html = readFileSync(OLDAL, 'utf8');
const kod = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
if (!/var SZERVER = true;/.test(kod)) { console.log('HIBA: az oldal nem az online változat'); process.exit(1); }
const ids = [...html.matchAll(/id="([^"]+)"/g)].map(m => m[1]);

const TA = '1'.repeat(32), TB = '2'.repeat(32);
const d1 = new D1Utanzat(path.join(ITT, '..', 'schema.sql'));
const tetelek = kitalalt_tetelek(8);
await betolt(d1, tetelek, [
  { id: 'E1', szerep: 'kulso', token: TA, tetelek: tetelek.map(t => t.id) },
  { id: 'E2', szerep: 'masodik', token: TB, tetelek: ['T01', 'T02'] }]);
const env = { DB: d1, ADMIN_KULCS: 'k'.repeat(40) };

/* ---------- DOM-utánzat (mint a karoli_strong_validacio_oldal_proba.js-ben) ---------- */
function Elem(tag) {
  const cl = new Set();
  return { tagName: tag || 'div', children: [], attrs: {}, style: {}, hidden: false, value: '', checked: false, disabled: false,
    readOnly: false, files: [], _t: '', listeners: {},
    classList: { add: c => cl.add(c), remove: c => cl.delete(c), toggle: (c, f) => { if (f === undefined ? !cl.has(c) : f) cl.add(c); else cl.delete(c); }, contains: c => cl.has(c) },
    get className() { return [...cl].join(' '); }, set className(v) { cl.clear(); String(v).split(/\s+/).filter(Boolean).forEach(x => cl.add(x)); },
    get textContent() { return this._t + this.children.map(c => c.textContent).join(''); }, set textContent(v) { this._t = String(v); this.children = []; },
    appendChild(c) { this.children.push(c); return c; }, append(...cs) { cs.forEach(c => this.children.push(typeof c === 'string' ? { textContent: c } : c)); },
    setAttribute(k, v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k]; },
    addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); },
    click() { (this.listeners.click || []).forEach(f => f({ currentTarget: this, target: this })); },
    remove() {}, select() {}, scrollIntoView() {} };
}
let idozitok = [], idoz_n = 0;
globalThis.setTimeout = (f, ms) => { const id = ++idoz_n; idozitok.push({ id, f, ms }); return id; };
globalThis.clearTimeout = id => { idozitok = idozitok.filter(x => x.id !== id); };
function idozitok_futtat(max_ms) {   // a lejárt (legfeljebb max_ms késleltetésű) időzítők egyszeri futtatása
  const most = idozitok.filter(x => x.ms <= max_ms); idozitok = idozitok.filter(x => x.ms > max_ms);
  most.forEach(x => x.f());
}
const rendez = async () => { for (let i = 0; i < 30; i++) await new Promise(r => setImmediate(r)); };
let halozat = true, kerdes_db = 0;
globalThis.fetch = async (ut, o) => {
  kerdes_db++;
  if (!halozat) throw new TypeError('Failed to fetch');
  return kezel(new Request('https://proba.example' + ut, o), env);
};
globalThis.confirm = () => true;
globalThis.alert = () => {};
Object.defineProperty(globalThis, 'navigator', { value: {}, configurable: true, writable: true });
globalThis.Blob = function (p) { this.p = p; };
globalThis.URL = Object.assign(URL, { createObjectURL: () => 'blob:x', revokeObjectURL() {} });

function eszkoz(token, tar) {   // egy „oldalbetöltés” egy eszközön (tar: az eszköz localStorage-a)
  const elemek = {}; ids.forEach(i => { elemek[i] = Elem(); });
  const radiok = ['rossz_forrasszo', 'hianyzo_par', 'hianyos_kifejezes', 'folosleges_par', 'egyeb'].map(v => { const r = Elem('input'); r.value = v; return r; });
  const ablak = { scrollTo() {}, listeners: {}, addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); } };
  const e = { elemek, radiok, ablak, tar, token };
  e.aktival = () => {
    globalThis.window = ablak;
    globalThis.location = { search: token == null ? '' : '?t=' + token };
    globalThis.localStorage = { getItem: k => (k in tar ? tar[k] : null), setItem: (k, v) => { tar[k] = String(v); } };
    globalThis.document = { getElementById: i => elemek[i], createElement: t => Elem(t), createTextNode: s => ({ textContent: s }),
      querySelectorAll: s => s.startsWith('input[name=hibatipus]') ? radiok : [], addEventListener() {}, body: Elem(), documentElement: { style: { setProperty() {} } }, execCommand() {} };
  };
  e.aktival();
  idozitok = [];
  e.A = new Function(kod + '\nreturn {get allapot(){return allapot}, itelet_valt, lep, kesz_db, get MINTA(){return MINTA}, get MINTA_HASH(){return MINTA_HASH}, tetel, valasz, SZ, kuld, kesz_kuld, export_obj, get nezet(){return nezet}};')();
  return e;
}
const szerveren = id => Object.fromEntries(d1.db.prepare('SELECT tetel, valasz FROM utolso WHERE ellenor = ?').all(id)
  .map(r => [r.tetel, JSON.parse(r.valasz)]).filter(([, v]) => v.itelet));
const hiba = [];
const ell = (f, uz) => { if (!f) hiba.push(uz); };

// 1. első betöltés (E1, 1. eszköz): induló képernyő, Kezdés, három ítélet -> mind a szerveren
const tar1 = {};
let g1 = eszkoz(TA, tar1); await rendez();
ell(g1.A.MINTA && g1.A.MINTA.length === 8 && !g1.elemek['b-indul'].classList.contains('rejtett'), 'betöltés, Kezdés gomb');
g1.elemek['b-indul'].click();
ell(g1.A.nezet === 'tetel', 'Kezdés után tétel');
for (const it of ['helyes', 'hibas', 'bizonytalan']) { g1.A.itelet_valt(it); g1.A.lep(1); }
idozitok_futtat(0); await rendez();
ell(Object.keys(szerveren('E1')).length === 3 && g1.A.SZ.sor.length === 0, 'három ítélet a szerveren: ' + Object.keys(szerveren('E1')).length);
ell(/Minden válasz a szerveren/.test(g1.elemek['t-mentve'].textContent) && g1.elemek['f-szerver'].textContent === '✓ mentve', 'állapotjelző: ' + g1.elemek['f-szerver'].textContent);

// 2. megszakadt hálózat: a változások a sorban maradnak, újrapróbálás; ugyanannak a tételnek a pillanatképei összevonódnak
halozat = false;
const id4 = g1.A.tetel().id;
g1.A.itelet_valt('helyes'); g1.elemek['t-megj'].value = 'gépelt megjegyzés'; g1.elemek['t-megj'].listeners.input[0]();
g1.A.itelet_valt('helyes'); g1.A.itelet_valt('hibas');   // ugyanaz a tétel még háromszor
g1.A.lep(1); g1.A.itelet_valt('helyes'); g1.A.lep(1);
idozitok_futtat(1500); await rendez();
ell(g1.A.SZ.sor.length === 2 && g1.A.SZ.hiba === 'halozat', 'sor hálózat nélkül: ' + g1.A.SZ.sor.length + ' ' + g1.A.SZ.hiba);
ell(/Nincs kapcsolat: 2 változás vár/.test(g1.elemek['t-mentve'].textContent) && g1.elemek['f-szerver'].textContent === '⚠ nincs kapcsolat (2 vár)', 'állapotjelző offline: ' + g1.elemek['f-szerver'].textContent);
ell(JSON.parse(tar1[g1.A.SZ.sor_kulcs]).length === 2, 'a sor a böngészőben (localStorage)');
idozitok_futtat(60000); await rendez();   // újrapróbálás, még mindig nincs hálózat
ell(g1.A.SZ.sor.length === 2 && Object.keys(szerveren('E1')).length === 3, 'újrapróbálás hálózat nélkül');
halozat = true;
g1.ablak.listeners.online.forEach(f => f()); await rendez();
const sz = szerveren('E1');
ell(g1.A.SZ.sor.length === 0 && Object.keys(sz).length === 5, 'a hálózat visszatértével elküldve: ' + Object.keys(sz).length);
ell(sz[id4] && sz[id4].itelet === 'hibas' && sz[id4].megjegyzes === 'gépelt megjegyzés', 'az összevont legutolsó állapot: ' + JSON.stringify(sz[id4]));

// 3. el nem küldött változás + újratöltés hálózat nélkül (hibaüzenet), majd hálózattal: a sorból felkerül
halozat = false;
g1.A.itelet_valt('bizonytalan'); idozitok_futtat(0); await rendez();
ell(g1.A.SZ.sor.length === 1, 'egy el nem küldött változás');
g1 = eszkoz(TA, tar1); await rendez();
ell(/Nem érem el a szervert/.test(g1.elemek['indul-info'].textContent), 'betöltés hálózat nélkül: ' + g1.elemek['indul-info'].textContent);
halozat = true;
g1 = eszkoz(TA, tar1); await rendez();
ell(g1.A.nezet === 'tetel' && g1.A.kesz_db() === 6, 'újratöltés után: ' + g1.A.kesz_db());
ell(Object.keys(szerveren('E1')).length === 6 && g1.A.SZ.sor.length === 0, 'a régi sor elküldve: ' + Object.keys(szerveren('E1')).length);

// 4. második eszköz (üres böngésző), ugyanaz a token: ugyanaz az állapot és sorrend; hiányos „Kész” elutasítva
const tar2 = {};
const g2 = eszkoz(TA, tar2); await rendez();
ell(g2.A.kesz_db() === 6 && g2.A.allapot.sorrend.join() === g1.A.allapot.sorrend.join(), 'második eszköz: ' + g2.A.kesz_db());
g2.A.kesz_kuld(); await rendez();
ell(/Még 2 tétel/.test(g2.elemek['m-kesz-info'].textContent) && !d1.db.prepare("SELECT kesz_ido FROM ellenor WHERE id='E1'").get().kesz_ido, 'hiányos Kész: ' + g2.elemek['m-kesz-info'].textContent);
ell(g2.elemek['b-kesz'].disabled === true, 'a Kész gomb tiltva hiányosan');
for (let i = 0; i < 8; i++) { if (!(g2.A.valasz(g2.A.tetel()).itelet)) g2.A.itelet_valt('helyes'); g2.A.lep(1); }
idozitok_futtat(0); await rendez();
ell(Object.keys(szerveren('E1')).length === 8, 'második eszközről kitöltve: ' + Object.keys(szerveren('E1')).length);

// 5. az első eszköz újratöltve látja a második eszköz válaszait; „Kész”; utána nincs módosítás
g1 = eszkoz(TA, tar1); await rendez();
ell(g1.A.kesz_db() === 8 && g1.elemek['b-kesz'].disabled === false, 'első eszköz újratöltve: ' + g1.A.kesz_db());
g1.A.kesz_kuld(); await rendez();
const kesz = d1.db.prepare("SELECT kesz_ido FROM ellenor WHERE id='E1'").get().kesz_ido;
ell(kesz && g1.A.SZ.lezarva && /Köszönjük/.test(g1.elemek['m-kesz-info'].textContent), 'Kész: ' + g1.elemek['m-kesz-info'].textContent);
const elotte = JSON.stringify(szerveren('E1')), n0 = d1.db.prepare('SELECT COUNT(*) AS n FROM naplo').get().n;
g1.A.itelet_valt('hibas'); idozitok_futtat(0); await rendez();
ell(JSON.stringify(szerveren('E1')) === elotte && d1.db.prepare('SELECT COUNT(*) AS n FROM naplo').get().n === n0 && g1.A.SZ.sor.length === 0, 'Kész után nincs módosítás');
ell(g1.elemek['b-helyes'].disabled === true && /Beküldve/.test(g1.elemek['t-mentve'].textContent) && g1.elemek['f-szerver'].textContent === '✓ beküldve', 'lezárt felület: ' + g1.elemek['f-szerver'].textContent);
// a másik eszköz (még nyitva, régi állapottal) módosítana: a szerver 409, a kliens lezárja magát
g2.aktival(); g2.A.itelet_valt('bizonytalan'); idozitok_futtat(0); await rendez();
ell(g2.A.SZ.lezarva && JSON.stringify(szerveren('E1')) === elotte, 'a régi lap módosítása elutasítva');

// 6. biztonsági másolat online módban: az oldal exportja a minta-azonosítóval
{ const x = g1.A.export_obj(); ell(x.minta_hash === g1.A.MINTA_HASH && Object.keys(x.valaszok).length === 8 && x.ellenor === 'E1', 'biztonsági másolat'); }

// 7. érvénytelen és hiányzó token, sérült minta-azonosító
{ const g = eszkoz('f'.repeat(32), {}); await rendez();
  ell(/érvénytelen/.test(g.elemek['indul-info'].textContent) && !g.A.allapot, 'érvénytelen token: ' + g.elemek['indul-info'].textContent);
  const h = eszkoz(null, {}); await rendez();
  ell(/személyes linkeddel/.test(h.elemek['indul-info'].textContent), 'hiányzó token');
  d1.db.exec("UPDATE ellenor SET minta_hash = 'dead' WHERE id = 'E2'");
  const k = eszkoz(TB, {}); await rendez();
  ell(/sérültek/.test(k.elemek['indul-info'].textContent) && !k.A.allapot, 'sérült minta-azonosító: ' + k.elemek['indul-info'].textContent); }

console.log(hiba.length ? 'HIBA:\n  ' + hiba.join('\n  ') : 'RENDBEN (7 forgatókönyv, kliens + Worker)');
console.log('fetch-hívások: ' + kerdes_db);
if (hiba.length) process.exitCode = 1;
