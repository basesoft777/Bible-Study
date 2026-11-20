// F175.V21 — a Károli–Strong emberi validáció online mentése (Cloudflare Worker + D1), DT-F175vp.
//
// A Worker csak érvényes ellenőri tokenre adja ki az adott ellenőr tételeit, és tételenként fogadja a válaszokat.
// A D1-ben a token nem áll, csak az SHA-256-ja; a tételek tartalma a letétből töltődik be
// (eszkozok/karoli_strong_validacio_d1.py), a repóba nem kerül. A válaszok append-only naplóba mennek
// (a `naplo` táblán UPDATE és DELETE tiltva), az „utolsó érvényes” válasz az `utolso` nézet.
// Titok a kódban nincs: az admin-kulcs Cloudflare secret (ADMIN_KULCS).
//
// A logika futtatókörnyezet-független: a tesztek Node-on, a D1 helyett node:sqlite-tal hívják
// (eszkozok/karoli_strong_validacio_worker/teszt/worker_proba.mjs).

export const VERZIO = 'F175.V42';   // F175.V25: a hiányzó kapcsolat jelölője; F175.V42: a beküldés visszajelzése
const ITELETEK = new Set(['', 'helyes', 'hibas', 'bizonytalan']);
// A „Nem” altípusai (a hiányzó kapcsolat nem hiba: külön jelölő, `hianyzo_kapcsolat`, csak „helyes” ítélet mellett).
const HIBATIPUSOK = new Set(['', 'rossz_forrasszo', 'folosleges_par', 'egyeb', 'kimaradt_par']);
const ISO_IDO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const AZON = /^[A-Za-z0-9_-]{8,64}$/;
const TOKEN = /^[0-9a-f]{32}$/;
const MAX_SZOVEG = 4000;
const MAX_KOTEG = 100;
const MAX_TORZS = 512 * 1024;

const ROBOTS = 'User-agent: *\nDisallow: /\n';

function fejlecek(h, html) {
  h.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
  h.set('Referrer-Policy', 'no-referrer');
  h.set('X-Content-Type-Options', 'nosniff');
  h.set('X-Frame-Options', 'DENY');
  h.set('Cache-Control', 'no-store');
  if (html) {
    h.set('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; " +
      "connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'");
  }
}

function json(obj, status = 200) {
  const r = new Response(typeof obj === 'string' ? obj : JSON.stringify(obj),
    { status, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  fejlecek(r.headers, false);
  return r;
}

function hiba(status, kod, uzenet) { return json({ hiba: kod, uzenet: uzenet || kod }, status); }

export async function sha256hex(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}

function egyenlo(a, b) {   // állandó idejű összevetés (azonos hosszú hex-kivonatokon)
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

function bearer(req) {
  const m = /^Bearer (\S+)$/.exec(req.headers.get('Authorization') || '');
  return m ? m[1] : '';
}

async function ellenor_token(req, env) {
  const t = bearer(req);
  if (!TOKEN.test(t)) return null;
  const h = await sha256hex(t);
  return env.DB.prepare('SELECT id, szerep, minta_hash, tetelszam, kesz_ido FROM ellenor WHERE token_sha256 = ?')
    .bind(h).first();
}

async function admin_e(req, env) {
  const k = env.ADMIN_KULCS || '';
  if (k.length < 32) return false;   // admin-kulcs nélkül (vagy túl rövid kulccsal) az admin-végpontok zárva
  const t = bearer(req);
  if (!t) return false;
  return egyenlo(await sha256hex(t), await sha256hex(k));
}

async function torzs(req) {
  const s = await req.text();
  if (s.length > MAX_TORZS) throw new Error('túl nagy kérés');
  return JSON.parse(s);
}

function szoveg(x) {
  if (x == null) return '';
  if (typeof x !== 'string') throw new Error('szöveg kell');
  if (x.length > MAX_SZOVEG) throw new Error('túl hosszú szöveg');
  return x;
}

// Egy válasz-pillanatkép ellenőrzése és normalizálása (csak az ismert mezők maradnak).
export function valasz_normal(v, kliens_ido) {
  if (!v || typeof v !== 'object' || Array.isArray(v)) throw new Error('a válasz objektum');
  const itelet = v.itelet == null ? '' : v.itelet;
  if (!ITELETEK.has(itelet)) throw new Error('ismeretlen ítélet');
  const hibatipus = v.hibatipus == null ? '' : v.hibatipus;
  if (!HIBATIPUSOK.has(hibatipus)) throw new Error('ismeretlen hibatípus');
  const hf = v.helyes_forras == null ? [] : v.helyes_forras;
  if (!Array.isArray(hf) || hf.length > 30 || hf.some(n => !Number.isInteger(n) || n < 1 || n > 500)) {
    throw new Error('hibás helyes_forras');
  }
  if (v.karoli != null && typeof v.karoli !== 'boolean') throw new Error('a karoli logikai érték');
  if (v.hianyzo_kapcsolat != null && typeof v.hianyzo_kapcsolat !== 'boolean') {
    throw new Error('a hianyzo_kapcsolat logikai érték');
  }
  return {
    itelet, hibatipus, helyes_forras: hf,
    hianyzo_kapcsolat: itelet === 'helyes' && !!v.hianyzo_kapcsolat,   // a jelölő csak az „Igen” alpontja
    megjegyzes: szoveg(v.megjegyzes), karoli: !!v.karoli,
    karoli_megj: szoveg(v.karoli_megj), segedeszkoz: szoveg(v.segedeszkoz), ido: kliens_ido,
  };
}

// a szerveren ítélettel álló, ennek az ellenőrnek kiosztott tételek száma (a beküldés visszajelzéséhez)
async function megerkezett(env, id) {
  const r = await env.DB.prepare('SELECT COUNT(*) AS n FROM kiosztas k WHERE k.ellenor = ? AND EXISTS ' +
    '(SELECT 1 FROM utolso u WHERE u.ellenor = k.ellenor AND u.tetel = k.tetel AND ' +
    "json_extract(u.valasz, '$.itelet') <> '')").bind(id).first();
  return r.n;
}

async function tetelek(req, env) {
  const e = await ellenor_token(req, env);
  if (!e) return hiba(401, 'token', 'érvénytelen hozzáférési link');
  const t = await env.DB.prepare('SELECT t.id, t.adat FROM kiosztas k JOIN tetel t ON t.id = k.tetel ' +
    'WHERE k.ellenor = ? ORDER BY t.id').bind(e.id).all();
  const v = await env.DB.prepare('SELECT tetel, valasz FROM utolso WHERE ellenor = ?').bind(e.id).all();
  const n_szerveren = e.kesz_ido ? await megerkezett(env, e.id) : null;
  // a tételek JSON-ja a D1-ben kész szövegként áll; összefűzés, nem újraértelmezés (CPU-keret)
  const s = '{"verzio":' + JSON.stringify(VERZIO) + ',"ellenor":' + JSON.stringify(e.id) +
    ',"szerep":' + JSON.stringify(e.szerep) + ',"minta_hash":' + JSON.stringify(e.minta_hash) +
    ',"tetelszam":' + e.tetelszam + ',"kesz_ido":' + JSON.stringify(e.kesz_ido || null) +
    ',"megerkezett":' + JSON.stringify(n_szerveren) +
    ',"tetelek":[' + t.results.map(r => r.adat).join(',') + ']' +
    ',"valaszok":{' + v.results.map(r => JSON.stringify(r.tetel) + ':' + r.valasz).join(',') + '}}';
  return json(s);
}

async function valaszok_ment(req, env) {
  const e = await ellenor_token(req, env);
  if (!e) return hiba(401, 'token', 'érvénytelen hozzáférési link');
  if (e.kesz_ido) return hiba(409, 'lezarva', 'az ellenőr késznek jelölte a munkát; további módosítás nem mentődik');
  let d;
  try { d = await torzs(req); } catch (x) { return hiba(400, 'torzs', x.message); }
  const lista = d && d.valtozasok;
  if (!Array.isArray(lista) || !lista.length || lista.length > MAX_KOTEG) return hiba(400, 'valtozasok', 'valtozasok: 1–100 elem');
  const sorok = [];
  try {
    for (const x of lista) {
      if (!x || typeof x.tetel_id !== 'string' || x.tetel_id.length > 64) throw new Error('hibás tetel_id');
      if (!AZON.test(x.kliens_azon || '')) throw new Error('hibás kliens_azon');
      if (!ISO_IDO.test(x.kliens_ido || '')) throw new Error('hibás kliens_ido');
      sorok.push([x.tetel_id, JSON.stringify(valasz_normal(x.valasz, x.kliens_ido)), x.kliens_ido, x.kliens_azon]);
    }
  } catch (x) { return hiba(400, 'valasz', x.message); }
  const ids = [...new Set(sorok.map(s => s[0]))];
  const van = await env.DB.prepare('SELECT tetel FROM kiosztas WHERE ellenor = ? AND tetel IN (' +
    ids.map(() => '?').join(',') + ')').bind(e.id, ...ids).all();
  const kiosztott = new Set(van.results.map(r => r.tetel));
  const idegen = ids.filter(i => !kiosztott.has(i));
  if (idegen.length) return hiba(403, 'tetel', 'nem ennek az ellenőrnek kiosztott tétel: ' + idegen.slice(0, 3).join(', '));
  const most = new Date().toISOString();
  const st = env.DB.prepare('INSERT OR IGNORE INTO naplo (ellenor, tetel, esemeny, valasz, kliens_ido, szerver_ido, ' +
    'kliens_azon) VALUES (?, ?, \'valasz\', ?, ?, ?, ?)');
  await env.DB.batch(sorok.map(s => st.bind(e.id, s[0], s[1], s[2], most, s[3])));
  return json({ ok: true, elfogadva: sorok.map(s => s[3]), szerver_ido: most });
}

async function kesz(req, env) {
  const e = await ellenor_token(req, env);
  if (!e) return hiba(401, 'token', 'érvénytelen hozzáférési link');
  if (e.kesz_ido) return json({ ok: true, kesz_ido: e.kesz_ido, mar_kesz: true, megerkezett: await megerkezett(env, e.id),
    tetelszam: e.tetelszam });
  let d;
  try { d = await torzs(req); } catch (x) { return hiba(400, 'torzs', x.message); }
  if (!AZON.test((d && d.kliens_azon) || '')) return hiba(400, 'kliens_azon', 'hibás kliens_azon');
  const hiany = await env.DB.prepare('SELECT COUNT(*) AS n FROM kiosztas k WHERE k.ellenor = ? AND NOT EXISTS ' +
    '(SELECT 1 FROM utolso u WHERE u.ellenor = k.ellenor AND u.tetel = k.tetel AND ' +
    "json_extract(u.valasz, '$.itelet') <> '')").bind(e.id).first();
  if (hiany.n > 0) return hiba(409, 'hianyos', hiany.n + ' tétel még ítélet nélkül áll a szerveren');
  const most = new Date().toISOString();
  await env.DB.batch([
    env.DB.prepare('UPDATE ellenor SET kesz_ido = ? WHERE id = ? AND kesz_ido IS NULL').bind(most, e.id),
    env.DB.prepare('INSERT OR IGNORE INTO naplo (ellenor, tetel, esemeny, valasz, kliens_ido, szerver_ido, kliens_azon) ' +
      "VALUES (?, NULL, 'kesz', NULL, NULL, ?, ?)").bind(e.id, most, d.kliens_azon),
  ]);
  return json({ ok: true, kesz_ido: most, megerkezett: await megerkezett(env, e.id), tetelszam: e.tetelszam });
}

// A szervező csak a haladást látja: hány tételnél van ítélet, mikor volt utoljára mentés, kész-e. Ítéletet nem.
async function haladas(env) {
  const r = await env.DB.prepare(
    'SELECT e.id AS ellenor, e.szerep, e.tetelszam, e.kesz_ido, ' +
    "(SELECT COUNT(*) FROM utolso u WHERE u.ellenor = e.id AND json_extract(u.valasz, '$.itelet') <> '') AS itelet_db, " +
    "(SELECT MAX(szerver_ido) FROM naplo n WHERE n.ellenor = e.id) AS utolso_mentes, " +
    "(SELECT COUNT(*) FROM naplo n WHERE n.ellenor = e.id) AS naplo_db " +
    'FROM ellenor e ORDER BY e.id').all();
  return json({ verzio: VERZIO, ido: new Date().toISOString(), ellenorok: r.results });
}

function csv_mezo(x) {
  const s = x == null ? '' : String(x);
  return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

// Teljes export: ellenőrönként az utolsó érvényes válaszok (az oldal exportjával azonos alakban, a kiértékelő
// így olvassa), és a teljes append-only napló. CSV-ben csak a napló, soronként egy mentés.
async function export_(url, env) {
  const formatum = url.searchParams.get('formatum') || 'json';
  if (formatum === 'csv') {
    const n = await env.DB.prepare(
      'SELECT n, ellenor, tetel, esemeny, kliens_ido, szerver_ido, kliens_azon, ' +
      "json_extract(valasz, '$.itelet') AS itelet, json_extract(valasz, '$.hibatipus') AS hibatipus, " +
      "json_extract(valasz, '$.helyes_forras') AS helyes_forras, " +
      "json_extract(valasz, '$.hianyzo_kapcsolat') AS hianyzo_kapcsolat, json_extract(valasz, '$.karoli') AS karoli, " +
      "json_extract(valasz, '$.segedeszkoz') AS segedeszkoz, json_extract(valasz, '$.megjegyzes') AS megjegyzes, " +
      "json_extract(valasz, '$.karoli_megj') AS karoli_megj FROM naplo ORDER BY n").all();
    const fej = ['n', 'ellenor', 'tetel', 'esemeny', 'kliens_ido', 'szerver_ido', 'kliens_azon', 'itelet', 'hibatipus',
      'helyes_forras', 'hianyzo_kapcsolat', 'karoli', 'segedeszkoz', 'megjegyzes', 'karoli_megj'];
    const s = [fej.join(',')].concat(n.results.map(r => fej.map(k => csv_mezo(r[k])).join(','))).join('\r\n') + '\r\n';
    const resp = new Response('﻿' + s, { headers: { 'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': 'attachment; filename="validacio_naplo.csv"' } });
    fejlecek(resp.headers, false);
    return resp;
  }
  if (formatum !== 'json') return hiba(400, 'formatum', 'formatum: json | csv');
  const e = await env.DB.prepare('SELECT id, szerep, minta_hash, tetelszam, kesz_ido FROM ellenor ORDER BY id').all();
  const u = await env.DB.prepare('SELECT ellenor, tetel, valasz FROM utolso ORDER BY ellenor, tetel').all();
  const n = await env.DB.prepare('SELECT n, ellenor, tetel, esemeny, valasz, kliens_ido, szerver_ido, kliens_azon ' +
    'FROM naplo ORDER BY n').all();
  const per = {};
  for (const r of u.results) (per[r.ellenor] = per[r.ellenor] || []).push(JSON.stringify(r.tetel) + ':' + r.valasz);
  const ell = e.results.map(x => '{"oldal":' + JSON.stringify(VERZIO + '-szerver') + ',"ellenor":' + JSON.stringify(x.id) +
    ',"szerep":' + JSON.stringify(x.szerep) + ',"minta_hash":' + JSON.stringify(x.minta_hash) +
    ',"minta_meret":' + x.tetelszam + ',"kesz_ido":' + JSON.stringify(x.kesz_ido || null) +
    ',"valaszok":{' + (per[x.id] || []).join(',') + '}}');
  const naplo = n.results.map(r => '{"n":' + r.n + ',"ellenor":' + JSON.stringify(r.ellenor) + ',"tetel":' +
    JSON.stringify(r.tetel) + ',"esemeny":' + JSON.stringify(r.esemeny) + ',"valasz":' + (r.valasz || 'null') +
    ',"kliens_ido":' + JSON.stringify(r.kliens_ido) + ',"szerver_ido":' + JSON.stringify(r.szerver_ido) +
    ',"kliens_azon":' + JSON.stringify(r.kliens_azon) + '}');
  const s = '{"formatum":"F175V-szerver-export/1","verzio":' + JSON.stringify(VERZIO) + ',"export_ido":' +
    JSON.stringify(new Date().toISOString()) + ',"ellenorok":[' + ell.join(',') + '],"naplo":[' + naplo.join(',') + ']}';
  return json(s);
}

export async function kezel(req, env) {
  const url = new URL(req.url);
  const p = url.pathname;
  try {
    if (p === '/robots.txt') {
      const r = new Response(ROBOTS, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
      fejlecek(r.headers, false);
      return r;
    }
    if (p.startsWith('/api/')) {
      const m = req.method;
      if (p === '/api/tetelek' && m === 'GET') return await tetelek(req, env);
      if (p === '/api/valaszok' && m === 'POST') return await valaszok_ment(req, env);
      if (p === '/api/kesz' && m === 'POST') return await kesz(req, env);
      if (p.startsWith('/api/admin/')) {
        if (!(await admin_e(req, env))) return hiba(401, 'admin', 'érvénytelen admin-kulcs');
        if (p === '/api/admin/haladas' && m === 'GET') return await haladas(env);
        if (p === '/api/admin/export' && m === 'GET') return await export_(url, env);
      }
      return hiba(404, 'nincs', 'ismeretlen végpont');
    }
    if (!env.ASSETS) return hiba(404, 'nincs', 'nincs statikus tartalom');
    const a = await env.ASSETS.fetch(req);
    const r = new Response(a.body, a);
    fejlecek(r.headers, (r.headers.get('Content-Type') || '').startsWith('text/html'));
    return r;
  } catch (x) {
    return hiba(500, 'szerver', 'belső hiba');
  }
}
