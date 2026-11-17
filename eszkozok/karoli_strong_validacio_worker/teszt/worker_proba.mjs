// F175.V21 — a validációs Worker logikájának próbája Node-on, kitalált adattal (D1 helyett node:sqlite).
// Hívja: eszkozok/teszt_karoli_strong_validacio.py (Online). Kilépési kód 1 hibánál.
// Futtatás: node eszkozok/karoli_strong_validacio_worker/teszt/worker_proba.mjs
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { kezel, valasz_normal } from '../src/logika.js';
import { D1Utanzat, kitalalt_tetelek, betolt, minta_hash } from './d1_utanzat.mjs';

const ITT = path.dirname(fileURLToPath(import.meta.url));
const SEMA = path.join(ITT, '..', 'schema.sql');
const TA = 'a'.repeat(32), TB = 'b'.repeat(32), ADMIN = 'k'.repeat(40);
const hiba = [];
const ell = (f, uz) => { if (!f) hiba.push(uz); };

const d1 = new D1Utanzat(SEMA);
const tetelek = kitalalt_tetelek(5);
await betolt(d1, tetelek, [
  { id: 'E1', szerep: 'kulso', token: TA, tetelek: tetelek.map(t => t.id) },
  { id: 'E2', szerep: 'masodik', token: TB, tetelek: ['T01', 'T02', 'T03'] }]);
const html = '<!doctype html><title>x</title>';
const env = { DB: d1, ADMIN_KULCS: ADMIN,
  ASSETS: { fetch: async () => new Response(html, { headers: { 'Content-Type': 'text/html; charset=utf-8' } }) } };

async function hiv(ut, { modszer = 'GET', token, adat } = {}) {
  const h = {};
  if (token) h.Authorization = 'Bearer ' + token;
  if (adat !== undefined) h['Content-Type'] = 'application/json';
  const r = await kezel(new Request('https://proba.example' + ut,
    { method: modszer, headers: h, body: adat === undefined ? undefined : (typeof adat === 'string' ? adat : JSON.stringify(adat)) }), env);
  const s = await r.text();
  let d = null; try { d = JSON.parse(s); } catch (e) { d = s; }
  return { st: r.status, d, h: r.headers, s };
}
const valtozas = (id, it, ido, azon, extra) => ({ tetel_id: id, kliens_ido: ido, kliens_azon: azon,
  valasz: Object.assign({ itelet: it, hibatipus: '', helyes_forras: [], megjegyzes: '', karoli: false, karoli_megj: '', segedeszkoz: '' }, extra || {}) });
const naplo_db = () => d1.db.prepare('SELECT COUNT(*) AS n FROM naplo').get().n;

// 1. token nélkül, rossz és hibás alakú tokennel: 401, adat nélkül
for (const t of [undefined, 'c'.repeat(32), 'nem-token']) {
  const r = await hiv('/api/tetelek', { token: t });
  ell(r.st === 401 && !('tetelek' in (r.d || {})), 'token-elutasítás: ' + t + ' -> ' + r.st);
}
// 2. a saját tételek, azonosító-sorrendben, a minta-azonosítóval
{ const r = await hiv('/api/tetelek', { token: TA });
  ell(r.st === 200 && r.d.tetelek.length === 5 && r.d.tetelek[0].id === 'T01' && r.d.minta_hash === minta_hash(tetelek), 'E1 tételei');
  ell(r.d.szerep === 'kulso' && r.d.ellenor === 'E1' && Object.keys(r.d.valaszok).length === 0, 'E1 üres válaszok');
  const b = await hiv('/api/tetelek', { token: TB });
  ell(b.st === 200 && b.d.tetelek.map(t => t.id).join() === 'T01,T02,T03', 'E2 csak a sajátját látja');
  ell(r.h.get('X-Robots-Tag').includes('noindex') && r.h.get('Cache-Control') === 'no-store', 'fejlécek az API-n'); }
// 3. mentés és idempotencia: ugyanaz a köteg kétszer csak egyszer kerül a naplóba
const k1 = [valtozas('T01', 'helyes', '2026-11-20T10:00:00.000Z', 'azon0001'), valtozas('T02', 'hibas', '2026-11-20T10:00:01.000Z', 'azon0002', { hibatipus: 'rossz_forrasszo', helyes_forras: [1] })];
{ const r1 = await hiv('/api/valaszok', { modszer: 'POST', token: TA, adat: { valtozasok: k1 } });
  const r2 = await hiv('/api/valaszok', { modszer: 'POST', token: TA, adat: { valtozasok: k1 } });
  ell(r1.st === 200 && r1.d.elfogadva.length === 2 && r2.st === 200, 'mentés: ' + r1.st + ' ' + r2.st);
  ell(naplo_db() === 2, 'idempotens mentés: napló ' + naplo_db()); }
// 4. az utolsó érvényes: a kliens ideje szerint; a később beérkező régebbi (offline sorból) nem írja felül
{ await hiv('/api/valaszok', { modszer: 'POST', token: TA, adat: { valtozasok: [valtozas('T01', 'bizonytalan', '2026-11-20T11:00:00.000Z', 'azon0003', { megjegyzes: 'újabb' })] } });
  await hiv('/api/valaszok', { modszer: 'POST', token: TA, adat: { valtozasok: [valtozas('T01', 'hibas', '2026-11-20T10:30:00.000Z', 'azon0004', { hibatipus: 'egyeb' })] } });
  const r = await hiv('/api/tetelek', { token: TA });
  ell(r.d.valaszok.T01.itelet === 'bizonytalan' && r.d.valaszok.T01.megjegyzes === 'újabb', 'utolsó érvényes: ' + JSON.stringify(r.d.valaszok.T01));
  ell(r.d.valaszok.T02.helyes_forras.join() === '1' && r.d.valaszok.T02.ido === '2026-11-20T10:00:01.000Z', 'mezők és idő');
  ell(naplo_db() === 4, 'append-only: minden mentés sor (' + naplo_db() + ')'); }
// 5. idegen tétel: az egész köteg elutasítva, semmi nem kerül be
{ const n0 = naplo_db();
  const r = await hiv('/api/valaszok', { modszer: 'POST', token: TB, adat: { valtozasok: [valtozas('T01', 'helyes', '2026-11-20T10:00:00.000Z', 'azonB001'), valtozas('T04', 'helyes', '2026-11-20T10:00:00.000Z', 'azonB002')] } });
  ell(r.st === 403 && naplo_db() === n0, 'idegen tétel elutasítva: ' + r.st); }
// 6. hibás bemenetek: 400, semmi nem kerül be
{ const n0 = naplo_db();
  const rossz = [
    { valtozasok: [valtozas('T01', 'talan', '2026-11-20T10:00:00.000Z', 'azonR001')] },
    { valtozasok: [valtozas('T01', 'helyes', 'tegnap', 'azonR002')] },
    { valtozasok: [valtozas('T01', 'helyes', '2026-11-20T10:00:00.000Z', 'x')] },
    { valtozasok: [valtozas('T01', 'hibas', '2026-11-20T10:00:00.000Z', 'azonR003', { hibatipus: 'kitalalt' })] },
    { valtozasok: [valtozas('T01', 'hibas', '2026-11-20T10:00:00.000Z', 'azonR004', { megjegyzes: 'x'.repeat(5000) })] },
    { valtozasok: [] }, 'nem json'];
  for (const a of rossz) {
    const r = await hiv('/api/valaszok', { modszer: 'POST', token: TA, adat: a });
    ell(r.st === 400, 'hibás bemenet: ' + JSON.stringify(a).slice(0, 60) + ' -> ' + r.st);
  }
  ell(naplo_db() === n0, 'hibás bemenetből nincs naplósor'); }
// 7. a napló append-only: UPDATE és DELETE tiltva
{ let u = '', t = '';
  try { d1.db.exec("UPDATE naplo SET valasz = NULL"); } catch (e) { u = e.message; }
  try { d1.db.exec('DELETE FROM naplo'); } catch (e) { t = e.message; }
  ell(/append-only/.test(u) && /append-only/.test(t) && naplo_db() === 4, 'append-only napló: ' + u + ' / ' + t); }
// 8. „Kész”: csak teljes kitöltésnél; utána a mentés 409, a második „Kész” nem ír újra
{ const r1 = await hiv('/api/kesz', { modszer: 'POST', token: TB, adat: { kliens_azon: 'keszB001' } });
  ell(r1.st === 409 && r1.d.hiba === 'hianyos', 'hiányos kész: ' + r1.st);
  await hiv('/api/valaszok', { modszer: 'POST', token: TB, adat: { valtozasok: ['T01', 'T02', 'T03'].map((id, i) => valtozas(id, 'helyes', '2026-11-21T09:00:0' + i + '.000Z', 'azonB10' + i)) } });
  const r2 = await hiv('/api/kesz', { modszer: 'POST', token: TB, adat: { kliens_azon: 'keszB002' } });
  ell(r2.st === 200 && r2.d.kesz_ido, 'kész: ' + r2.st);
  const r3 = await hiv('/api/valaszok', { modszer: 'POST', token: TB, adat: { valtozasok: [valtozas('T01', 'hibas', '2026-11-22T00:00:00.000Z', 'azonB200', { hibatipus: 'egyeb' })] } });
  ell(r3.st === 409 && r3.d.hiba === 'lezarva', 'kész után nincs mentés: ' + r3.st);
  const r4 = await hiv('/api/kesz', { modszer: 'POST', token: TB, adat: { kliens_azon: 'keszB003' } });
  ell(r4.st === 200 && r4.d.mar_kesz === true && r4.d.kesz_ido === r2.d.kesz_ido, 'második kész');
  const t = await hiv('/api/tetelek', { token: TB });
  ell(t.d.kesz_ido === r2.d.kesz_ido, 'a kész-idő a tételekkel jön'); }
// 9. admin: kulcs nélkül, rossz kulccsal, túl rövid szerveroldali kulccsal zárva; a haladás ítéletet nem mutat
{ ell((await hiv('/api/admin/haladas')).st === 401, 'admin kulcs nélkül');
  ell((await hiv('/api/admin/haladas', { token: 'x'.repeat(40) })).st === 401, 'admin rossz kulccsal');
  ell((await hiv('/api/admin/haladas', { token: TA })).st === 401, 'admin ellenőri tokennel');
  const rovid = env.ADMIN_KULCS; env.ADMIN_KULCS = 'rovid';
  ell((await hiv('/api/admin/haladas', { token: 'rovid' })).st === 401, 'túl rövid admin-kulcs: zárva');
  env.ADMIN_KULCS = rovid;
  const h = await hiv('/api/admin/haladas', { token: ADMIN });
  const e1 = h.d.ellenorok.find(x => x.ellenor === 'E1'), e2 = h.d.ellenorok.find(x => x.ellenor === 'E2');
  ell(h.st === 200 && e1.itelet_db === 2 && e1.tetelszam === 5 && !e1.kesz_ido && e2.itelet_db === 3 && e2.kesz_ido, 'haladás: ' + JSON.stringify(h.d.ellenorok));
  ell(!/helyes|hibas|bizonytalan|megjegyzes/.test(h.s), 'a haladás nem mutat ítéletet'); }
// 10. export: JSON (ellenőrönként az utolsó érvényes + a teljes napló) és CSV (a napló)
{ const r = await hiv('/api/admin/export?formatum=json', { token: ADMIN });
  ell(r.st === 200 && r.d.formatum === 'F175V-szerver-export/1', 'export formátum');
  const e1 = r.d.ellenorok.find(x => x.ellenor === 'E1');
  ell(e1.minta_hash === minta_hash(tetelek) && e1.minta_meret === 5 && e1.valaszok.T01.itelet === 'bizonytalan' && Object.keys(e1.valaszok).length === 2, 'export E1');
  ell(r.d.naplo.length === naplo_db() && r.d.naplo.filter(x => x.esemeny === 'kesz').length === 1, 'export napló: ' + r.d.naplo.length);
  const c = await hiv('/api/admin/export?formatum=csv', { token: ADMIN });
  const sorok = c.s.replace(/^﻿/, '').trim().split('\r\n');
  ell(c.st === 200 && sorok[0].startsWith('n,ellenor,tetel,esemeny') && sorok.length === naplo_db() + 1, 'CSV: ' + sorok.length);
  ell(c.s.includes('"' + 'újabb' + '"') || c.s.includes(',újabb,'), 'CSV mezők');
  ell((await hiv('/api/admin/export?formatum=xml', { token: ADMIN })).st === 400, 'ismeretlen formátum'); }
// 12. a hiányzó kapcsolat jelölője (F175.V25): csak „helyes” mellett marad meg; a megszűnt hibatípusok és a nem
// logikai érték elutasítva; a CSV-ben külön oszlop
{ ell(valasz_normal({ itelet: 'helyes', hianyzo_kapcsolat: true }, 't').hianyzo_kapcsolat === true, 'jelölő: helyes mellett megmarad');
  ell(valasz_normal({ itelet: 'hibas', hibatipus: 'egyeb', hianyzo_kapcsolat: true }, 't').hianyzo_kapcsolat === false, 'jelölő: hibás mellett törlődik');
  ell(valasz_normal({ itelet: 'bizonytalan', hianyzo_kapcsolat: true }, 't').hianyzo_kapcsolat === false, 'jelölő: bizonytalan mellett törlődik');
  ell(valasz_normal({ itelet: 'helyes' }, 't').hianyzo_kapcsolat === false, 'jelölő: alapérték hamis');
  for (const v of [{ itelet: 'hibas', hibatipus: 'hianyzo_par' }, { itelet: 'hibas', hibatipus: 'hianyos_kifejezes' },
                   { itelet: 'helyes', hianyzo_kapcsolat: 'igen' }]) {
    let dobott = false; try { valasz_normal(v, 't'); } catch (e) { dobott = true; }
    ell(dobott, 'elutasítva: ' + JSON.stringify(v));
  }
  const c = await hiv('/api/admin/export?formatum=csv', { token: ADMIN });
  ell(c.s.replace(/^\uFEFF/, '').split('\r\n')[0].includes(',helyes_forras,hianyzo_kapcsolat,karoli,'), 'CSV: hianyzo_kapcsolat oszlop'); }
// 11. statikus tartalom és robots.txt: noindex, CSP a HTML-en; ismeretlen végpont 404
{ const r = await hiv('/');
  ell(r.st === 200 && r.h.get('X-Robots-Tag').includes('noindex') && r.h.get('Content-Security-Policy').includes("frame-ancestors 'none'") && r.h.get('Referrer-Policy') === 'no-referrer', 'statikus fejlécek');
  const rb = await hiv('/robots.txt');
  ell(rb.st === 200 && /Disallow: \//.test(rb.s), 'robots.txt');
  ell((await hiv('/api/semmi', { token: TA })).st === 404, '404'); }

console.log(hiba.length ? 'HIBA:\n  ' + hiba.join('\n  ') : 'RENDBEN (12 forgatókönyv, Worker-logika)');
if (hiba.length) process.exitCode = 1;
