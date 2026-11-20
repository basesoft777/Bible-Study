// F175.V21 — a D1 kötés utánzata node:sqlite fölött a Worker-logika teszteléséhez (csak a használt felület:
// prepare().bind().first()/all()/run(), batch() egy tranzakcióban). Valódi D1 helyett, kitalált adattal.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';

class Utasitas {
  constructor(db, sql, args) { this.db = db; this.sql = sql; this.args = args || []; }
  bind(...a) { return new Utasitas(this.db, this.sql, a); }
  async first() { const r = this.db.prepare(this.sql).get(...this.args); return r === undefined ? null : { ...r }; }
  async all() { return { results: this.db.prepare(this.sql).all(...this.args).map(r => ({ ...r })) }; }
  async run() { const r = this.db.prepare(this.sql).run(...this.args); return { success: true, meta: { changes: r.changes } }; }
}

export class D1Utanzat {
  constructor(sema_ut) {
    this.db = new DatabaseSync(':memory:');
    this.db.exec('PRAGMA foreign_keys = ON');
    if (sema_ut) this.db.exec(readFileSync(sema_ut, 'utf8'));
  }
  prepare(sql) { return new Utasitas(this.db, sql); }
  async batch(lista) {
    this.db.exec('BEGIN');
    try { const ki = []; for (const u of lista) ki.push(await u.run()); this.db.exec('COMMIT'); return ki; }
    catch (e) { this.db.exec('ROLLBACK'); throw e; }
  }
  exec(sql) { this.db.exec(sql); }
}

// kitalált tételek az ellenőrző oldal formájában (a kliens-próbához is)
export function kitalalt_tetelek(n) {
  const ki = [];
  for (let i = 1; i <= n; i++) {
    ki.push({ id: 'T' + String(i).padStart(2, '0'), tipus: i % 4 === 0 ? 'parnelkuli' : 'par', vers: '1Móz 1:' + i,
      hu: 'Kezdetben teremté Isten az eget és a földet', hn: 2, hk: 11, hv: 18, hs: 'teremté', nyelv: 'heber',
      en: i % 4 === 0 ? 0 : 2, strong: 'H1254', szoto: 'בָּרָא', jel: 'teremt', tukor: 'he created', morf: 'HVqp3ms',
      mh: 'ige', kiej: 'bara', ntr: false, tsz: '',
      tok: [{ n: 1, a: 'בְּרֵאשִׁית', s: 'H7225', t: 'in beginning', k: 'reshit', m: '', mh: '', w: '', x: 0 },
        { n: 2, a: 'בָּרָא', s: 'H1254', t: 'he created', k: 'bara', m: '', mh: '', w: '', x: 0 }],
      parok: [[1, 'Kezdetben', 1, 'בְּרֵאשִׁית', 'H7225'], [2, 'teremté', 2, 'בָּרָא', 'H1254']] });
  }
  return ki;
}

// az oldal / a kiértékelő minta-azonosítója (FNV-1a, UTF-16 kódegységeken)
export function minta_hash(tetelek) {
  const s = tetelek.map(t => t.id + '|' + t.vers + '|' + t.hn + '|' + t.en).join(';');
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return (h >>> 0).toString(16);
}

export async function sha256hex(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}

// betöltés: ellenőrök [{id, szerep, token, tetelek:[id]}]
export async function betolt(d1, tetelek, ellenorok) {
  for (const t of tetelek) await d1.prepare('INSERT INTO tetel (id, adat) VALUES (?, ?)').bind(t.id, JSON.stringify(t)).run();
  for (const e of ellenorok) {
    const sajat = tetelek.filter(t => e.tetelek.includes(t.id));
    await d1.prepare('INSERT INTO ellenor (id, szerep, token_sha256, minta_hash, tetelszam) VALUES (?, ?, ?, ?, ?)')
      .bind(e.id, e.szerep, await sha256hex(e.token), minta_hash(sajat), sajat.length).run();
    for (const t of sajat) await d1.prepare('INSERT INTO kiosztas (ellenor, tetel) VALUES (?, ?)').bind(e.id, t.id).run();
  }
}
