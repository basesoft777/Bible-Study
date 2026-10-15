// A tervező mód kliense (#98 M2). Csak a belso kiadásban linkelődik (alap.html, `tervezo`), és a szerver a /tervezo/... útvonalakat
// is csak ott jegyzi be. CSP: saját fájl (script-src 'self'); inline szkript és inline stílus nincs. Az előnézet a :root
// CSS-változóit állítja CSSOM-mal (style.setProperty), csak ebben a böngészőben; a szerverre csak a „Küldés a szerverre” gomb ír.
// A panel elemei createElement/textContent-tel készülnek (HTML-szöveg beillesztése nincs).
(function () {
  'use strict';

  var kapcsolo = document.getElementById('tervezo-kapcsolo');
  if (!kapcsolo || !window.fetch || !window.JSON || !Element.prototype.matches || !Element.prototype.closest) { return; }

  var gyoker = document.documentElement;
  var TAROLO = 'pardes_tervezo_valtozasok';
  var TEMA_NEV = { light: 'világos', dark: 'sötét' };
  var SZIN = /^(?:#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|hsl\(\s*\d{1,3}(?:\.\d{1,2})?\s*,\s*\d{1,3}(?:\.\d{1,2})?%\s*,\s*\d{1,3}(?:\.\d{1,2})?%\s*\))$/;
  var BIZTONSAGOS_ERTEK = /^[#a-zA-Z0-9.,%() ]{1,40}$/;
  var TOKEN_NEV = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  var TULAJDONSAG_HU = {
    'font': 'betű (méret, sorköz)', 'font-size': 'betűméret', 'line-height': 'sorköz', 'color': 'szín', 'background': 'háttér',
    'background-color': 'háttér', 'border': 'keret', 'border-color': 'keret színe', 'border-top': 'felső keret', 'border-bottom': 'alsó vonal',
    'border-left': 'bal vonal', 'border-radius': 'lekerekítés', 'padding': 'belső térköz', 'padding-bottom': 'alsó belső térköz',
    'margin': 'margó', 'margin-bottom': 'alsó margó', 'gap': 'köz', 'min-width': 'legkisebb szélesség', 'text-decoration-color': 'aláhúzás színe',
    'outline': 'körvonal'
  };

  var terkep = null;          // a /tervezo/terkep.json: regiszter, tokenek, tartományok, szabálytérkép
  var be = false;             // a tervező mód be van-e kapcsolva
  var valtozasok = {};        // kulcs: token vagy token|téma → {token, tema, regi, uj}
  var kivalasztott = null;    // {el, sorok, szabalyok, idx}
  var kiemelt = null;
  var ui = null;              // a panel elemei

  // -- segédek -----------------------------------------------------------------------------------------------------------
  function h(tag, osztaly, szoveg) {
    var e = document.createElement(tag);
    if (osztaly) { e.className = osztaly; }
    if (szoveg !== undefined && szoveg !== null) { e.textContent = szoveg; }
    return e;
  }
  function gomb(osztaly, szoveg, cim, fv) {
    var b = h('button', osztaly, szoveg);
    b.type = 'button';
    if (cim) { b.title = cim; }
    b.addEventListener('click', fv);
    return b;
  }
  function uiElem(el) { return !!(el && el.closest && (el.closest('.tz-ui') || el.closest('#tervezo-kapcsolo'))); }
  function illik(el, szelektor) { try { return el.matches(szelektor); } catch (e) { return false; } }
  function spNagyobb(a, b) { for (var i = 0; i < 3; i++) { if (a[i] !== b[i]) { return a[i] > b[i]; } } return false; }
  function leiro(el) {
    var s = el.tagName.toLowerCase();
    for (var i = 0; i < el.classList.length; i++) { s += '.' + el.classList[i]; }
    return s;
  }

  // -- tárolás (sessionStorage: lapváltáskor az előnézet követi a felhasználót) -------------------------------------------
  function tarolBe() { try { window.sessionStorage.setItem(TAROLO, JSON.stringify(valtozasok)); } catch (e) { /* tiltott tároló */ } }
  function tarolKi() {
    var ki = {};
    try {
      var v = JSON.parse(window.sessionStorage.getItem(TAROLO) || '{}');
      Object.keys(v || {}).forEach(function (k) {
        var x = v[k];
        if (x && typeof x.token === 'string' && TOKEN_NEV.test(x.token) && typeof x.uj === 'string' && BIZTONSAGOS_ERTEK.test(x.uj) &&
            (x.tema === null || x.tema === 'light' || x.tema === 'dark')) {
          ki[kulcs(x.token, x.tema)] = { token: x.token, tema: x.tema, regi: typeof x.regi === 'string' ? x.regi : '', uj: x.uj };
        }
      });
    } catch (e) { /* üres */ }
    return ki;
  }

  // -- téma és előnézet --------------------------------------------------------------------------------------------------
  function aktivTema() {
    var t = gyoker.getAttribute('data-tema');
    if (t === 'light' || t === 'dark') { return t; }
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
  }
  function kulcs(token, tema) { return tema ? token + '|' + tema : token; }

  function elonezet() {
    var tema = aktivTema();
    var latott = {};
    Object.keys(valtozasok).forEach(function (k) {
      var v = valtozasok[k];
      if (v.tema && v.tema !== tema) { return; }
      gyoker.style.setProperty('--' + v.token, v.uj);
      latott[v.token] = true;
    });
    for (var i = gyoker.style.length - 1; i >= 0; i--) {
      var p = gyoker.style[i];
      if (p.indexOf('--') === 0 && !latott[p.slice(2)]) { gyoker.style.removeProperty(p); }
    }
    kapcsoloFelirat();
  }

  function kapcsoloFelirat() {
    var n = Object.keys(valtozasok).length;
    kapcsolo.textContent = 'Tervező' + (n ? ' (' + n + ')' : '');
  }

  function eredeti(token, tema) {
    var t = terkep && terkep.tokenek[token];
    if (!t) { return ''; }
    return t.tipus === 'szin' ? t.ertek[tema || aktivTema()] : t.ertek;
  }
  function jelenlegi(token, tema) {
    var v = valtozasok[kulcs(token, tema)];
    return v ? v.uj : eredeti(token, tema);
  }
  function allit(token, uj) {
    var t = terkep.tokenek[token];
    var tema = t.tipus === 'szin' ? aktivTema() : null;
    var k = kulcs(token, tema);
    var regi = eredeti(token, tema);
    if (uj === regi) { delete valtozasok[k]; } else { valtozasok[k] = { token: token, tema: tema, regi: regi, uj: uj }; }
    tarolBe();
    elonezet();
    listaRajzol();
  }

  // -- az elem feloldása: a regiszter, különben a tartalék (a stíluslap tokenes szabályai) ----------------------------------
  function sorok(el) {
    var ki = [];
    terkep.regiszter.forEach(function (s, i) {
      var legjobb = null;
      s.reszek.forEach(function (r) { if (illik(el, r.alap) && (!legjobb || spNagyobb(r.sp, legjobb))) { legjobb = r.sp; } });
      if (legjobb) { ki.push({ sor: s, sp: legjobb, i: i }); }
    });
    ki.sort(function (a, b) { return spNagyobb(a.sp, b.sp) ? -1 : (spNagyobb(b.sp, a.sp) ? 1 : b.i - a.i); });
    return ki;
  }
  function szabalyok(el) {
    return terkep.szabalyok.filter(function (r) { return r.reszek.some(function (p) { return illik(el, p.alap); }); });
  }
  function feloldas(t) {
    for (var el = t; el && el.nodeType === 1 && el !== gyoker; el = el.parentElement) {
      if (uiElem(el)) { return null; }
      var s = sorok(el);
      if (s.length) { return { el: el, sorok: s, szabalyok: [], idx: 0 }; }
      var r = szabalyok(el);
      if (r.length) { return { el: el, sorok: [], szabalyok: r, idx: 0 }; }
    }
    return null;
  }
  function hatas(token) {
    var r = terkep.szabalyok.filter(function (x) { return x.deklaraciok.some(function (d) { return d[1].indexOf(token) >= 0; }); });
    var elemek = new Set();
    r.forEach(function (x) {
      x.reszek.forEach(function (p) {
        try { document.querySelectorAll(p.alap).forEach(function (e) { if (!uiElem(e)) { elemek.add(e); } }); } catch (e) { /* nem illeszthető */ }
      });
    });
    return { szabaly: r.length, elem: elemek.size };
  }

  // -- kiemelés ----------------------------------------------------------------------------------------------------------
  function kiemel(res) {
    if (kiemelt && (!res || kiemelt !== res.el)) { kiemelt.removeAttribute('data-tz-kiemelt'); kiemelt = null; }
    if (!res) { ui.cimke.hidden = true; return; }
    kiemelt = res.el;
    kiemelt.setAttribute('data-tz-kiemelt', res.sorok.length ? 'reg' : 'nem');
    ui.cimke.textContent = res.sorok.length ? res.sorok[0].sor.nev : 'nem regisztrált elem: ' + leiro(res.el);
    ui.cimke.classList.toggle('tz-nem', !res.sorok.length);
    ui.cimke.hidden = false;
    var b = res.el.getBoundingClientRect();
    var fent = b.top - ui.cimke.offsetHeight - 4;
    if (fent < 2) { fent = b.bottom + 4; }
    ui.cimke.style.top = Math.max(2, Math.min(fent, window.innerHeight - ui.cimke.offsetHeight - 2)) + 'px';
    ui.cimke.style.left = Math.max(2, Math.min(b.left, window.innerWidth - ui.cimke.offsetWidth - 4)) + 'px';
  }

  function valaszt(res, idx) {
    if (kivalasztott && kivalasztott.el) { kivalasztott.el.removeAttribute('data-tz-kivalasztott'); }
    kivalasztott = res;
    if (res) {
      res.idx = idx || 0;
      res.el.setAttribute('data-tz-kivalasztott', '');
    }
    elemRajzol();
  }

  // -- a panel -----------------------------------------------------------------------------------------------------------
  function uiLetrehoz() {
    if (ui) { return; }
    ui = {};
    ui.cimke = h('div', 'tz-ui tz-cimke');
    ui.cimke.hidden = true;
    ui.cimke.setAttribute('aria-hidden', 'true');
    ui.probe = h('span', 'tz-ui tz-probe');
    var p = ui.panel = h('aside', 'tz-ui tz-panel');
    p.setAttribute('aria-label', 'Tervező panel');
    p.hidden = true;
    var fej = ui.fej = h('div', 'tz-fej');
    ui.cim = h('strong', 'tz-cim', 'Tervező mód');
    ui.szulo = gomb('tz-gomb tz-kis', 'Szülő elem ↑', 'A következő regisztrált elem feljebb', function () {
      if (kivalasztott) { var r = feloldas(kivalasztott.el.parentElement); if (r) { valaszt(r, 0); } }
    });
    fej.appendChild(ui.cim);
    fej.appendChild(ui.szulo);
    fej.appendChild(gomb('tz-gomb tz-kis', '×', 'A tervező mód kikapcsolása (Esc)', kikapcs));
    p.appendChild(fej);
    ui.alcim = h('div', 'tz-alcim');
    ui.tobb = h('div', 'tz-tobb');
    ui.tul = h('div', 'tz-tulajdonsagok');
    p.appendChild(ui.alcim);
    p.appendChild(ui.tobb);
    p.appendChild(ui.tul);
    var vs = h('section', 'tz-valtozasok');
    ui.vcim = h('div', 'tz-szakasz', 'Változások (0)');
    ui.mindVissza = gomb('tz-gomb tz-kis', 'Mindet vissza', 'Minden előnézeti változás visszavonása', function () {
      valtozasok = {}; tarolBe(); elonezet(); listaRajzol(); elemRajzol();
    });
    var vfej = h('div', 'tz-vfej');
    vfej.appendChild(ui.vcim);
    vfej.appendChild(ui.mindVissza);
    vs.appendChild(vfej);
    ui.vlista = h('ul', 'tz-vlista');
    vs.appendChild(ui.vlista);
    p.appendChild(vs);
    var gs = h('div', 'tz-gombok');
    ui.kuld = gomb('tz-gomb tz-fo', 'Küldés a szerverre', 'A változások írása a konfig/arculat.json-ba', kuldes);
    gs.appendChild(ui.kuld);
    gs.appendChild(gomb('tz-gomb', 'Előző mentés vissza', 'A legutóbbi mentés előtti állapot visszaállítása a szerveren', visszaallitas));
    p.appendChild(gs);
    ui.uzenet = h('div', 'tz-uzenet');
    ui.uzenet.setAttribute('role', 'status');
    p.appendChild(ui.uzenet);
    document.body.appendChild(ui.cimke);
    document.body.appendChild(ui.probe);
    document.body.appendChild(p);
    huzhato(fej, p);
  }

  function huzhato(fogo, doboz) {
    fogo.addEventListener('mousedown', function (ev) {
      if (ev.target.closest('button')) { return; }
      var b = doboz.getBoundingClientRect();
      var dx = ev.clientX - b.left, dy = ev.clientY - b.top;
      function mozog(e) {
        doboz.style.left = Math.max(0, Math.min(e.clientX - dx, window.innerWidth - 60)) + 'px';
        doboz.style.top = Math.max(0, Math.min(e.clientY - dy, window.innerHeight - 30)) + 'px';
        doboz.style.right = 'auto';
        doboz.style.bottom = 'auto';
      }
      function enged() { document.removeEventListener('mousemove', mozog, true); document.removeEventListener('mouseup', enged, true); }
      document.addEventListener('mousemove', mozog, true);
      document.addEventListener('mouseup', enged, true);
      ev.preventDefault();
    });
  }

  function uzen(szoveg, hiba) {
    if (!ui) { return; }
    ui.uzenet.textContent = szoveg;
    ui.uzenet.classList.toggle('tz-hiba', !!hiba);
  }

  function hexre(v) {
    if (/^#[0-9a-fA-F]{6}$/.test(v)) { return v.toLowerCase(); }
    if (/^#[0-9a-fA-F]{3}$/.test(v)) { return ('#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3]).toLowerCase(); }
    ui.probe.style.color = '';
    ui.probe.style.color = v;
    var m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(window.getComputedStyle(ui.probe).color);
    if (!m) { return '#000000'; }
    return '#' + [m[1], m[2], m[3]].map(function (x) { return ('0' + parseInt(x, 10).toString(16)).slice(-2); }).join('');
  }

  function hosszBont(v) {
    var m = /^(\d+(?:\.\d+)?)(px|rem|em)?$/.exec(v || '');
    return m ? { n: parseFloat(m[1]), e: m[2] || '' } : null;
  }
  function kerekit(n, lepes) {
    var d = lepes < 0.01 ? 3 : (lepes < 0.05 ? 3 : (lepes < 0.5 ? 2 : 1));
    return String(parseFloat(n.toFixed(d)));
  }

  function szinVezerlo(cel, token, tema) {
    var ertek = jelenlegi(token, tema);
    var minta = h('span', 'tz-minta');
    minta.style.background = ertek;
    var valaszto = h('input', 'tz-szinvalaszto');
    valaszto.type = 'color';
    valaszto.value = hexre(ertek);
    valaszto.setAttribute('aria-label', 'Színválasztó');
    var mezo = h('input', 'tz-mezo');
    mezo.type = 'text';
    mezo.value = ertek;
    mezo.maxLength = 40;
    mezo.spellcheck = false;
    mezo.setAttribute('aria-label', 'Színérték (#rgb, #rrggbb, rgb(), hsl())');
    valaszto.addEventListener('input', function () { mezo.value = valaszto.value; minta.style.background = valaszto.value; allit(token, valaszto.value); });
    mezo.addEventListener('change', function () {
      var v = mezo.value.trim();
      if (!SZIN.test(v)) { uzen('A szín alakja: #rgb, #rrggbb, rgb(r, g, b) vagy hsl(h, s%, l%).', true); mezo.value = jelenlegi(token, tema); return; }
      minta.style.background = v;
      valaszto.value = hexre(v);
      allit(token, v);
      uzen('');
    });
    var sor = h('div', 'tz-szinsor');
    sor.appendChild(minta);
    sor.appendChild(valaszto);
    sor.appendChild(mezo);
    sor.appendChild(h('span', 'tz-tema', 'a ' + TEMA_NEV[tema] + ' témában'));
    cel.appendChild(sor);
    var paletta = h('div', 'tz-paletta');
    paletta.setAttribute('aria-label', 'Paletta');
    Object.keys(terkep.tokenek).filter(function (n) { return terkep.tokenek[n].tipus === 'szin'; }).forEach(function (n) {
      var v = jelenlegi(n, tema);
      var b = gomb('tz-szinminta', '', '--' + n + ': ' + v, function () { allit(token, v); elemRajzol(); });
      b.style.background = v;
      b.setAttribute('aria-label', n + ' ' + v);
      paletta.appendChild(b);
    });
    cel.appendChild(paletta);
  }

  function hosszVezerlo(cel, token, t) {
    var ertek = jelenlegi(token, null);
    var b = hosszBont(ertek);
    var tart = b && (terkep.tartomany[t.csoport] || {})[b.e];
    if (!b || !tart) { cel.appendChild(h('span', 'tz-megj', ertek + ' (nem állítható)')); return; }
    var lepes = b.e === 'px' ? 0.5 : (b.e === '' ? 0.01 : 0.025);
    var csuszka = h('input', 'tz-csuszka');
    csuszka.type = 'range';
    csuszka.min = tart[0];
    csuszka.max = tart[1];
    csuszka.step = lepes;
    csuszka.value = b.n;
    csuszka.setAttribute('aria-label', 'Érték');
    var szam = h('input', 'tz-szam');
    szam.type = 'number';
    szam.min = tart[0];
    szam.max = tart[1];
    szam.step = lepes;
    szam.value = b.n;
    szam.setAttribute('aria-label', 'Érték számmal');
    function beallit(n) { allit(token, kerekit(n, lepes) + b.e); }
    csuszka.addEventListener('input', function () { szam.value = csuszka.value; beallit(parseFloat(csuszka.value)); });
    szam.addEventListener('change', function () {
      var n = parseFloat(szam.value);
      if (isNaN(n) || n < tart[0] || n > tart[1]) { uzen('Tartományon kívül: ' + tart[0] + '–' + tart[1] + b.e + '.', true); szam.value = csuszka.value; return; }
      csuszka.value = n;
      beallit(n);
      uzen('');
    });
    var sor = h('div', 'tz-hosszsor');
    sor.appendChild(csuszka);
    sor.appendChild(szam);
    sor.appendChild(h('span', 'tz-egyseg', b.e || '×'));
    cel.appendChild(sor);
    cel.appendChild(h('div', 'tz-megj', 'tartomány: ' + tart[0] + '–' + tart[1] + (b.e || '') + (b.e === 'em' ? ' (a környezethez viszonyítva)' : '')));
  }

  function tulajdonsagSor(nev, token) {
    var t = terkep.tokenek[token];
    var sor = h('div', 'tz-sor');
    var fej = h('div', 'tz-sorfej');
    fej.appendChild(h('span', 'tz-nev', nev));
    fej.appendChild(h('code', 'tz-token', '--' + token));
    sor.appendChild(fej);
    if (!t) { sor.appendChild(h('div', 'tz-figy', 'ismeretlen token')); return sor; }
    var vez = h('div', 'tz-vezerlo');
    if (t.tipus === 'szin') { szinVezerlo(vez, token, aktivTema()); }
    else if (t.tipus === 'hossz' || t.tipus === 'szam') { hosszVezerlo(vez, token, t); }
    else { vez.appendChild(h('span', 'tz-megj', String(t.ertek) + ' (betűcsalád: nem állítható)')); }
    sor.appendChild(vez);
    var hat = hatas(token);
    var szoveg = 'ez a token ' + hat.szabaly + ' szabályban, ' + hat.elem + ' elemen hat ezen a lapon';
    if (t.tipus === 'szin') { szoveg += ' · világos: ' + jelenlegi(token, 'light') + ' · sötét: ' + jelenlegi(token, 'dark'); }
    sor.appendChild(h('div', 'tz-hatas', szoveg));
    if (!t.irhato) { sor.appendChild(h('div', 'tz-figy', 'csak előnézet: a token nincs a regiszterben, a szerver nem menti')); }
    return sor;
  }

  function tomlResz(res) {
    var alap = '';
    res.szabalyok.some(function (r) { return r.reszek.some(function (p) { if (illik(res.el, p.alap)) { alap = p.alap; return true; } return false; }); });
    var id = alap.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'uj-elem';
    var szel = alap.indexOf('"') >= 0 ? "'" + alap + "'" : '"' + alap + '"';
    var tok = [];
    res.szabalyok.forEach(function (r) { r.deklaraciok.forEach(function (d) { d[1].forEach(function (t) { if (tok.indexOf(t) < 0) { tok.push(t); } }); }); });
    return '[[elem]]\nid = "' + id + '"\nnev = "(magyar név)"\ncsoport = "(csoport)"\nszelektor = ' + szel + '\ntulajdonsag = [\n' +
      tok.map(function (t) { return '  { nev = "(magyar név)", token = "' + t + '" },'; }).join('\n') + '\n]\n';
  }

  function nemRegisztralt(res) {
    ui.cim.textContent = 'Nem regisztrált elem';
    ui.alcim.textContent = leiro(res.el);
    ui.tul.appendChild(h('p', 'tz-figy', 'Ez az elem nincs a regiszterben: a tokenből jövő tulajdonságai gépi névvel állíthatók (előnézet; '
      + 'a szerver csak a regiszterben szereplő tokent menti). Felvétel a regiszterbe: az alábbi részlet magyar névvel az elemek.toml-ba másolható.'));
    var tok = {};
    var sorrend = [];
    res.szabalyok.forEach(function (r) {
      var allapot = '';
      r.reszek.forEach(function (p) { if (p.allapot && illik(res.el, p.alap)) { allapot = p.allapot; } });
      r.deklaraciok.forEach(function (d) {
        d[1].forEach(function (t) {
          if (!tok[t]) { tok[t] = []; sorrend.push(t); }
          var leir = (TULAJDONSAG_HU[d[0]] || d[0]) + (allapot ? ' (' + allapot + ')' : '') + (r.media ? ' (' + r.media.replace(/^@media\s*/, '') + ')' : '');
          if (tok[t].indexOf(leir) < 0) { tok[t].push(leir); }
        });
      });
    });
    sorrend.forEach(function (t) { ui.tul.appendChild(tulajdonsagSor(tok[t].join(', '), t)); });
    var ta = h('textarea', 'tz-toml');
    ta.readOnly = true;
    ta.rows = Math.min(12, sorrend.length + 7);
    ta.value = tomlResz(res);
    ta.setAttribute('aria-label', 'Felvétel a regiszterbe: elemek.toml-részlet');
    ui.tul.appendChild(h('div', 'tz-szakasz', 'Felvétel a regiszterbe'));
    ui.tul.appendChild(ta);
  }

  function elemRajzol() {
    if (!ui) { return; }
    ui.tobb.textContent = '';
    ui.tul.textContent = '';
    var res = kivalasztott;
    if (!res) {
      ui.cim.textContent = 'Tervező mód';
      ui.alcim.textContent = 'Mutass egy elemre, majd kattints rá. A kattintás ilyenkor nem navigál. Esc: kilépés.';
      ui.szulo.disabled = true;
      return;
    }
    ui.szulo.disabled = !feloldas(res.el.parentElement);
    if (!res.sorok.length) { nemRegisztralt(res); return; }
    var s = res.sorok[res.idx].sor;
    ui.cim.textContent = s.nev;
    ui.alcim.textContent = s.csoport + ' · ' + s.szelektor;
    if (res.sorok.length > 1) {
      ui.tobb.appendChild(h('span', 'tz-megj', 'Ugyanezen az elemen: '));
      res.sorok.forEach(function (x, i) {
        if (i === res.idx) { return; }
        ui.tobb.appendChild(gomb('tz-gomb tz-kis', x.sor.nev, x.sor.szelektor, function () { valaszt(res, i); }));
      });
    }
    s.tulajdonsag.forEach(function (t) { ui.tul.appendChild(tulajdonsagSor(t.nev, t.token)); });
  }

  function listaRajzol() {
    if (!ui) { return; }
    ui.vlista.textContent = '';
    var kk = Object.keys(valtozasok).sort();
    ui.vcim.textContent = 'Változások (' + kk.length + ')';
    kk.forEach(function (k) {
      var v = valtozasok[k];
      var li = h('li', 'tz-vsor');
      li.appendChild(h('code', 'tz-token', '--' + v.token + (v.tema ? ' (' + TEMA_NEV[v.tema] + ')' : '')));
      li.appendChild(h('span', 'tz-ertekek', (v.regi || '?') + ' → ' + v.uj));
      if (terkep && (!terkep.tokenek[v.token] || !terkep.tokenek[v.token].irhato)) { li.appendChild(h('span', 'tz-figy', 'csak előnézet')); }
      li.appendChild(gomb('tz-gomb tz-kis', '↶', 'Visszavonás', function () {
        delete valtozasok[k]; tarolBe(); elonezet(); listaRajzol(); elemRajzol();
      }));
      ui.vlista.appendChild(li);
    });
    ui.mindVissza.disabled = !kk.length;
    ui.kuld.disabled = !kk.length;
  }

  // -- szerver ----------------------------------------------------------------------------------------------------------
  function valaszJson(r) {
    return r.json().catch(function () { return {}; }).then(function (j) {
      if (!r.ok) { throw new Error((j && j.hiba) || ('HTTP ' + r.status)); }
      return j;
    });
  }
  function postol(ut, torzs) {
    return fetch('/tervezo/kod', { credentials: 'same-origin', cache: 'no-store' }).then(valaszJson).then(function (j) {
      return fetch(ut, { method: 'POST', credentials: 'same-origin', cache: 'no-store',
        headers: { 'Content-Type': 'application/json', 'X-Tervezo-Kod': j.kod }, body: torzs || '{}' });
    }).then(valaszJson);
  }

  function kuldes() {
    var tok = {}, kimarad = [], n = 0;
    Object.keys(valtozasok).forEach(function (k) {
      var v = valtozasok[k], t = terkep.tokenek[v.token];
      if (!t || !t.irhato) { if (kimarad.indexOf(v.token) < 0) { kimarad.push(v.token); } return; }
      if (v.tema) { tok[v.token] = tok[v.token] || {}; tok[v.token][v.tema] = v.uj; } else { tok[v.token] = v.uj; }
      n++;
    });
    if (!n) {
      uzen('Nincs menthető változás' + (kimarad.length ? ' (a regiszteren kívüli tokenek csak előnézetben állíthatók: ' + kimarad.join(', ') + ')' : '') + '.', true);
      return;
    }
    var kerdes = 'Küldés a szerverre: ' + n + ' érték a konfig/arculat.json-ba (a változás a git-diffben látszik).' +
      (kimarad.length ? '\nKimarad, mert nincs a regiszterben: ' + kimarad.join(', ') : '') + '\nFolytatod?';
    if (!window.confirm(kerdes)) { return; }
    ui.kuld.disabled = true;
    uzen('Küldés…');
    postol('/tervezo/mentes', JSON.stringify({ tokenek: tok })).then(function (j) {
      Object.keys(valtozasok).forEach(function (k) {
        var t = terkep.tokenek[valtozasok[k].token];
        if (t && t.irhato) { delete valtozasok[k]; }
      });
      tarolBe();
      uzen('Mentve: ' + j.valtozas + ' érték. Az oldal újratölt…');
      window.location.reload();
    }).catch(function (e) { uzen('A mentés nem sikerült: ' + e.message, true); listaRajzol(); });
  }

  function visszaallitas() {
    if (!window.confirm('A szerveren a legutóbbi mentés előtti arculat áll vissza (konfig/arculat.json.elozo). Folytatod?')) { return; }
    uzen('Visszaállítás…');
    postol('/tervezo/visszaallit', '{}').then(function () {
      uzen('Visszaállítva. Az oldal újratölt…');
      window.location.reload();
    }).catch(function (e) { uzen('A visszaállítás nem sikerült: ' + e.message, true); });
  }

  // -- be- és kikapcsolás ------------------------------------------------------------------------------------------------
  function terkepBetolt() {
    if (terkep) { return Promise.resolve(terkep); }
    return fetch('/tervezo/terkep.json', { credentials: 'same-origin' }).then(valaszJson).then(function (j) {
      terkep = j;
      Object.keys(valtozasok).forEach(function (k) { if (!terkep.tokenek[valtozasok[k].token]) { delete valtozasok[k]; } });
      tarolBe();
      elonezet();
      return j;
    });
  }

  function ra(ev) {
    if (!terkep || !ui) { return; }
    if (uiElem(ev.target)) { kiemel(null); return; }
    kiemel(feloldas(ev.target));
  }
  function kattint(ev) {
    if (uiElem(ev.target)) { return; }
    ev.preventDefault();
    ev.stopPropagation();
    if (!terkep) { return; }
    var r = feloldas(ev.target);
    if (r) { valaszt(r, 0); }
  }
  function tilt(ev) { if (!uiElem(ev.target)) { ev.preventDefault(); ev.stopPropagation(); } }
  function bill(ev) {
    if (ev.key === 'Escape') {
      if (kivalasztott) { valaszt(null); } else { kikapcs(); }
      ev.preventDefault();
    }
  }
  function gorget() { if (kiemelt && ui) { ui.cimke.hidden = true; } }

  function bekapcs() {
    be = true;
    kapcsolo.setAttribute('aria-pressed', 'true');
    gyoker.setAttribute('data-tervezo', '');
    window.addEventListener('mouseover', ra, true);
    window.addEventListener('click', kattint, true);
    window.addEventListener('auxclick', tilt, true);
    window.addEventListener('submit', tilt, true);
    window.addEventListener('scroll', gorget, true);
    document.addEventListener('keydown', bill, true);
    terkepBetolt().then(function () {
      if (!be) { return; }
      uiLetrehoz();
      ui.panel.hidden = false;
      elemRajzol();
      listaRajzol();
    }).catch(function (e) {
      kapcsolo.title = 'A tervező térképe nem tölthető be: ' + e.message;
      kikapcs();
    });
  }

  function kikapcs() {
    be = false;
    kapcsolo.setAttribute('aria-pressed', 'false');
    gyoker.removeAttribute('data-tervezo');
    window.removeEventListener('mouseover', ra, true);
    window.removeEventListener('click', kattint, true);
    window.removeEventListener('auxclick', tilt, true);
    window.removeEventListener('submit', tilt, true);
    window.removeEventListener('scroll', gorget, true);
    document.removeEventListener('keydown', bill, true);
    kiemel(null);
    valaszt(null);
    if (ui) { ui.panel.hidden = true; ui.cimke.hidden = true; }
  }

  // -- indulás -----------------------------------------------------------------------------------------------------------
  valtozasok = tarolKi();
  elonezet();
  kapcsolo.hidden = false;
  kapcsolo.addEventListener('click', function (ev) { ev.preventDefault(); if (be) { kikapcs(); } else { bekapcs(); } });
  new MutationObserver(function () { elonezet(); if (be) { elemRajzol(); listaRajzol(); } }).observe(gyoker, { attributes: true, attributeFilter: ['data-tema'] });
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var valt = function () { elonezet(); if (be) { elemRajzol(); } };
    if (mq.addEventListener) { mq.addEventListener('change', valt); } else if (mq.addListener) { mq.addListener(valt); }
  }
})();
