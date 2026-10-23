// Az olvasói felület kis JavaScriptje (#76 M2, #134 M1–M2). Nélküle is minden működik: a vers- és szó-kattintás, a fülek, a
// bezárás, a könyvválasztó, a ⚙ és az Aa menü sima hivatkozások vagy `details`-elemek (szerveroldali lap); 900 px alatt a navigációs
// lapot a `#navigacio` cél nyitja. Itt csak a gyorsítás: a részletek lapja (szó- és versmód, fülek, előzménylánc, húzás), a töredék-
// betöltés (/r/...), a navigációs lap és a tájoló pirula, a kereső javaslatai (DT-F134k (b)), a Ctrl+K és a helyi beállítások.
(function () {
  'use strict';

  // a JS jelenléte: a navigációs lap JS nélküli (:target) szabálya ilyenkor nem él (a lapot a body osztálya nyitja)
  document.documentElement.classList.add('js-van');

  // Ctrl+K: ugrás a gyorsugrás dobozra
  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && ev.key && ev.key.toLowerCase() === 'k') {
      var be = document.querySelector('.ugras input[name=q]');
      if (be) { ev.preventDefault(); navNyitHaKell(); be.focus(); be.select(); }
    }
  });

  // az olvasó helyi beállításai (csak a böngészőben, localStorage; sütit nem hoznak létre): a kapcsolt szavak jelölése, a színséma,
  // a szövegbeállítások (Aa) és a „Legutóbb” lista
  function tarol(kulcs, ertek) { try { window.localStorage.setItem(kulcs, ertek); } catch (e) { /* tiltott tároló: a beállítás csak az oldalra érvényes */ } }
  function olvas(kulcs) { try { return window.localStorage.getItem(kulcs); } catch (e) { return null; } }

  var kicsiMedia = window.matchMedia ? window.matchMedia('(max-width: 899.98px)') : null;
  function kicsi() { return kicsiMedia ? kicsiMedia.matches : false; }

  var jeloles = document.getElementById('jeloles');
  if (jeloles) {
    var jelolesAllit = function () {
      document.querySelectorAll('.szoveg-oszlop').forEach(function (o) { o.classList.toggle('nincs-jeloles', !jeloles.checked); });
    };
    jeloles.checked = olvas('pardes_jeloles') !== 'ki';
    jelolesAllit();
    jeloles.addEventListener('change', function () { tarol('pardes_jeloles', jeloles.checked ? 'be' : 'ki'); jelolesAllit(); });
  }

  // a színséma (#134 M3; DT295, DT-F134i (a)): az alap a világos; a tárolt választást az első rajzolás előtt a statikus/tema.js
  // alkalmazza, itt csak a választó állapota és a váltás. „Rendszer”: attribútum nélkül a rendszer-beállítás.
  var temaGombok = document.querySelectorAll('.tema button[data-tema]');
  function temaAllit(tema) {
    if (tema === 'dark') { document.documentElement.setAttribute('data-tema', 'dark'); }
    else if (tema === 'rendszer') { document.documentElement.removeAttribute('data-tema'); }
    else { document.documentElement.setAttribute('data-tema', 'light'); tema = 'light'; }
    temaGombok.forEach(function (g) { g.setAttribute('aria-pressed', g.getAttribute('data-tema') === tema ? 'true' : 'false'); });
  }
  if (temaGombok.length) {
    temaAllit(olvas('pardes_tema'));
    temaGombok.forEach(function (g) {
      g.addEventListener('click', function () { var t = g.getAttribute('data-tema'); tarol('pardes_tema', t); temaAllit(t); });
    });
  }

  // ---------------------------------------------------------------------------------------------------------------------
  // a fejléc lenyíló elemei (könyvválasztó, Aa, ⚙; `details`): egyszerre egy nyitott, kívülre kattintva vagy Esc-re zár
  // (900 px alatt a navigációs lapon belül maradnak nyitva)
  // ---------------------------------------------------------------------------------------------------------------------
  var lenyilok = document.querySelectorAll('.fejlec details');
  lenyilok.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open && !kicsi()) { lenyilok.forEach(function (m) { if (m !== d) { m.open = false; } }); }
    });
  });
  document.addEventListener('click', function (ev) {
    if (kicsi()) { return; }
    lenyilok.forEach(function (d) { if (d.open && !d.contains(ev.target)) { d.open = false; } });
  });

  // ---------------------------------------------------------------------------------------------------------------------
  // a navigációs lap (#134 M2): 900 px alatt a fejléc; a fejezetcím, a tájoló pirula és a Ctrl+K nyitja, a ✕, a fátyol és az Esc zárja
  // ---------------------------------------------------------------------------------------------------------------------
  var fejlec = document.querySelector('.fejlec.navlap');
  var beall = document.getElementById('beall');
  var konyvvalaszto = document.getElementById('konyvvalaszto');
  var navLapRejt = function () {};                                         // a részletek lapjának elrejtése (lent állítódik be)

  function navNyitva() { return document.body.classList.contains('navlap-nyitva'); }
  function navNyit() {
    if (!fejlec) { return; }
    navLapRejt();
    document.body.classList.add('navlap-nyitva');
    if (beall) { beall.open = true; }                                       // a mockup szerint a ⚙ menü a lapon kinyitva látszik
    fejlec.scrollTop = 0;
  }
  function navZar() {
    document.body.classList.remove('navlap-nyitva');
    zarJavaslat();
  }
  function navNyitHaKell() { if (fejlec && kicsi() && !navNyitva()) { navNyit(); } }
  if (fejlec && window.location.hash === '#navigacio') {                    // JS nélküli cél-hivatkozásból érkezve
    try { window.history.replaceState(null, '', window.location.pathname + window.location.search); } catch (e) { /* nem feltétel */ }
    if (kicsi()) { navNyit(); }
  }

  // a könyvválasztó: a könyvre koppintva (folytonos fejezetszámozásnál) helyben a fejezetrács; különben a könyv lapja nyílik
  var fejezetracs = document.getElementById('fejezetracs');
  var fejezetracsCim = document.getElementById('fejezetracs-cim');
  function fejezetracsRajzol(gomb) {
    var n = parseInt(gomb.getAttribute('data-fejszam'), 10);
    if (!fejezetracs || !n) { return false; }
    var slugK = gomb.getAttribute('data-slug');
    var itt = document.querySelector('.fejezetgomb.itt');
    var ittFej = itt && fejezetracs.getAttribute('data-kk') === gomb.getAttribute('data-kk') ? itt.textContent : null;
    while (fejezetracs.firstChild) { fejezetracs.removeChild(fejezetracs.firstChild); }
    for (var f = 1; f <= n; f++) {
      var a = document.createElement('a');
      a.classList.add('fejezetgomb');
      if (String(f) === ittFej) { a.classList.add('itt'); }
      a.href = '/' + slugK + '/' + f;
      a.textContent = String(f);
      fejezetracs.appendChild(a);
    }
    if (fejezetracsCim) { fejezetracsCim.textContent = (gomb.getAttribute('data-nev') || '') + ' · fejezetek'; }
    document.querySelectorAll('.konyvgomb.itt').forEach(function (k) { k.classList.remove('itt'); });
    gomb.classList.add('itt');
    if (konyvvalaszto) { konyvvalaszto.open = true; }
    fejezetracs.scrollIntoView({ block: 'nearest' });
    return true;
  }

  // ---------------------------------------------------------------------------------------------------------------------
  // a kereső javaslatai (DT-F134k (b)): könyvnév és igehely-minta a lapon már meglévő könyvlistából (a könyvválasztó gombjai),
  // új végpont nélkül. A javaslat hivatkozás; a többi bevitel (Strong-szám, szó, frázis) a szokásos keresésre megy.
  // ---------------------------------------------------------------------------------------------------------------------
  var urlap = document.querySelector('.ugras');
  var mezo = urlap ? urlap.querySelector('input[name=q]') : null;
  var javaslat = document.getElementById('javaslat');
  function norm(s) {
    return (s || '').toLocaleLowerCase('hu').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[\s.]+/g, '');
  }
  var konyvLista = [];
  document.querySelectorAll('.konyvgomb[data-kk]').forEach(function (g) {
    konyvLista.push({ kk: g.getAttribute('data-kk'), nev: g.getAttribute('data-nev') || '', slug: g.getAttribute('data-slug'),
      fejszam: parseInt(g.getAttribute('data-fejszam'), 10) || 0, a: norm(g.getAttribute('data-kk')), n: norm(g.getAttribute('data-nev')),
      s: norm(g.getAttribute('data-slug')) });
  });
  var jvAkt = -1;
  function zarJavaslat() { if (javaslat) { javaslat.hidden = true; jvAkt = -1; } }
  function javasol(q) {
    var s = (q || '').trim();
    var m = /^(\d?\s*[^\d\s:,.]+(?:\s+[^\d\s:,.]+)*)\.?\s*(\d{1,3})?(?:\s*[:,.\s]\s*(\d{1,3}))?$/.exec(s);
    if (!s || !m || /^[HhGg]\s*\d+$/.test(s)) { return []; }
    var b = norm(m[1]);
    if (!b) { return []; }
    var ki = [];
    // a pontos könyvkód-egyezés elöl („ez” → Ez, nem Ezsd), utána a kód- és a névkezdet a kánon sorrendjében
    var rang = function (k) { return k.a === b || k.s === b ? 0 : (k.a.indexOf(b) === 0 || k.s.indexOf(b) === 0 ? 1 : (k.n.indexOf(b) === 0 ? 2 : 3)); };
    konyvLista.filter(function (k) { return rang(k) < 3; }).sort(function (x, y) { return rang(x) - rang(y); }).forEach(function (k) {
      if (ki.length >= 6) { return; }
      var f = m[2] ? parseInt(m[2], 10) : null, v = m[3] ? parseInt(m[3], 10) : null;
      if (f && k.fejszam && f > k.fejszam) { return; }
      var ut = '/' + k.slug + (f ? '/' + f + (v ? '/' + v + '#v' + v : '') : '');
      ki.push({ ut: ut, fo: k.kk + (f ? ' ' + f + (v ? ':' + v : '') : ''), al: k.nev + (f ? '' : (k.fejszam ? ' · ' + k.fejszam + ' fejezet' : '')) });
    });
    return ki;
  }
  function jvJelol(i) {
    var elemek = javaslat.querySelectorAll('.javaslat-elem');
    elemek.forEach(function (e, j) { e.classList.toggle('aktiv', j === i); e.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
    jvAkt = i;
  }
  function mutatJavaslat() {
    if (!javaslat || !mezo) { return; }
    var lista = javasol(mezo.value);
    while (javaslat.firstChild) { javaslat.removeChild(javaslat.firstChild); }
    if (!lista.length) { zarJavaslat(); return; }
    lista.forEach(function (j) {
      var a = document.createElement('a');
      a.classList.add('javaslat-elem');
      a.setAttribute('role', 'option');
      a.href = j.ut;
      var fo = document.createElement('span'); fo.classList.add('javaslat-fo'); fo.textContent = j.fo;
      var al = document.createElement('span'); al.classList.add('javaslat-al'); al.textContent = j.al;
      a.appendChild(fo); a.appendChild(al);
      javaslat.appendChild(a);
    });
    javaslat.hidden = false;
    jvJelol(0);
  }
  if (mezo && javaslat && konyvLista.length) {
    mezo.addEventListener('input', mutatJavaslat);
    mezo.addEventListener('focus', function () { if (mezo.value) { mutatJavaslat(); } });
    mezo.addEventListener('keydown', function (ev) {
      var elemek = javaslat.hidden ? [] : javaslat.querySelectorAll('.javaslat-elem');
      if ((ev.key === 'ArrowDown' || ev.key === 'ArrowUp') && elemek.length) {
        ev.preventDefault();
        jvJelol((jvAkt + (ev.key === 'ArrowDown' ? 1 : -1) + elemek.length) % elemek.length);
      } else if (ev.key === 'Enter' && elemek.length && jvAkt >= 0) {
        ev.preventDefault();
        window.location.href = elemek[jvAkt].getAttribute('href');
      } else if (ev.key === 'Escape' && !javaslat.hidden) {
        ev.stopPropagation();
        zarJavaslat();
      }
    });
    document.addEventListener('click', function (ev) { if (!urlap.contains(ev.target)) { zarJavaslat(); } });
  }

  // ---------------------------------------------------------------------------------------------------------------------
  // szövegbeállítások (Aa, a mockup 4. változatából, amit a 9. átvett): betűméret, sorköz, versenként új sor; localStorage.
  // A méretet és a sorközt CSSOM-mal állítja a szövegoszlopon (a CSP ezt engedi; `style=""` a jelölésben nincs), a tokent nem írja.
  // ---------------------------------------------------------------------------------------------------------------------
  var AA_MERET = [0.85, 0.92, 1, 1.1, 1.2, 1.35, 1.5];
  var AA_SORKOZ = { szuk: 0.88, '': 1, tag: 1.15 };
  var aa = { meret: 2, sorkoz: '', versenkent: false };
  try { var aaT = JSON.parse(olvas('pardes_aa') || '{}'); if (aaT && typeof aaT === 'object') { for (var k in aa) { if (k in aaT) { aa[k] = aaT[k]; } } } } catch (e) { /* hibás tárolt érték: alapértékek */ }
  var oszlop = document.querySelector('.szoveg-oszlop');
  function aaAlkalmaz(ment) {
    if (!oszlop) { return; }
    if (!(aa.meret >= 0 && aa.meret < AA_MERET.length)) { aa.meret = 2; }
    if (!(aa.sorkoz in AA_SORKOZ)) { aa.sorkoz = ''; }
    oszlop.style.removeProperty('font-size');
    oszlop.style.removeProperty('line-height');
    var cs = window.getComputedStyle(oszlop);
    var alapMeret = parseFloat(cs.fontSize), alapSor = parseFloat(cs.lineHeight);
    var f = AA_MERET[aa.meret], s = AA_SORKOZ[aa.sorkoz];
    if (f !== 1) { oszlop.style.setProperty('font-size', (alapMeret * f).toFixed(2) + 'px'); }
    if ((f !== 1 || s !== 1) && alapSor && alapMeret) { oszlop.style.setProperty('line-height', ((alapSor / alapMeret) * s).toFixed(3)); }
    oszlop.classList.toggle('versenkent', !!aa.versenkent);
    var ertek = document.getElementById('aa-meret-ertek');
    if (ertek) { ertek.textContent = Math.round(f * 100) + '%'; }
    document.querySelectorAll('[data-aa-sorkoz]').forEach(function (g) { g.setAttribute('aria-pressed', g.getAttribute('data-aa-sorkoz') === aa.sorkoz ? 'true' : 'false'); });
    var vk = document.getElementById('aa-versenkent');
    if (vk) { vk.checked = !!aa.versenkent; }
    if (ment) { tarol('pardes_aa', JSON.stringify(aa)); }
  }
  if (document.getElementById('aa')) {
    document.querySelectorAll('[data-aa]').forEach(function (g) {
      g.addEventListener('click', function () {
        var mit = g.getAttribute('data-aa');
        if (mit === 'meret-') { aa.meret = Math.max(0, aa.meret - 1); }
        else if (mit === 'meret+') { aa.meret = Math.min(AA_MERET.length - 1, aa.meret + 1); }
        else if (mit === 'alap') { aa = { meret: 2, sorkoz: '', versenkent: false }; }
        aaAlkalmaz(true);
      });
    });
    document.querySelectorAll('[data-aa-sorkoz]').forEach(function (g) {
      g.addEventListener('click', function () { aa.sorkoz = g.getAttribute('data-aa-sorkoz'); aaAlkalmaz(true); });
    });
    var vkGomb = document.getElementById('aa-versenkent');
    if (vkGomb) { vkGomb.addEventListener('change', function () { aa.versenkent = vkGomb.checked; aaAlkalmaz(true); }); }
    aaAlkalmaz(false);
    if (kicsiMedia && kicsiMedia.addEventListener) { kicsiMedia.addEventListener('change', function () { aaAlkalmaz(false); }); }
  }

  // ---------------------------------------------------------------------------------------------------------------------
  // „Legutóbb” (a mockup előzménysora): az utoljára megnyitott versek, legfeljebb 6, localStorage; a navigációs lapon
  // ---------------------------------------------------------------------------------------------------------------------
  var legutobb = document.getElementById('legutobb');
  function legutobbRajzol() {
    if (!legutobb) { return; }
    var lista = [];
    try { lista = JSON.parse(olvas('pardes_legutobb') || '[]'); } catch (e) { lista = []; }
    if (!Array.isArray(lista)) { lista = []; }
    legutobb.querySelectorAll('.legutobb-hely').forEach(function (e) { legutobb.removeChild(e); });
    lista.forEach(function (x) {
      if (!x || typeof x.ut !== 'string' || x.ut.charAt(0) !== '/' || x.ut.charAt(1) === '/') { return; }
      var a = document.createElement('a');
      a.classList.add('legutobb-hely');
      a.href = x.ut;
      a.textContent = String(x.cim || '');
      legutobb.appendChild(a);
    });
    legutobb.hidden = !legutobb.querySelector('.legutobb-hely');
  }
  function legutobbHoz(ut, cim) {
    var lista = [];
    try { lista = JSON.parse(olvas('pardes_legutobb') || '[]'); } catch (e) { lista = []; }
    if (!Array.isArray(lista)) { lista = []; }
    lista = lista.filter(function (x) { return x && x.cim !== cim; });
    lista.unshift({ ut: ut, cim: cim });
    tarol('pardes_legutobb', JSON.stringify(lista.slice(0, 6)));
    legutobbRajzol();
  }
  legutobbRajzol();

  // ---------------------------------------------------------------------------------------------------------------------
  // a részletek lapja (#134 M1, DT293): egy komponens, két mód (szó / vers); 900 px alatt alsó lap, fölötte állandó oldalblokk.
  // Az állapot: {mod: 'ures'} | {mod: 'vers', vers, ful} | {mod: 'szo', strong, ig: [slug, fej, vers] | null}.
  // Az előzménylánc (‹): a korábbi állapotok verme, legfeljebb 20; az azonos egymás utáni állapot nem ismétlődik. A fülváltás is
  // új állapot (a mockup 9. változata szerint a ‹ az előző fülre is visszalép; #134 M2).
  // ---------------------------------------------------------------------------------------------------------------------
  var lap = document.getElementById('reszletek');
  if (!lap) { return; }
  var VERS_FULEK = ['vers', 'kh', 'temak', 'motivum'];
  var MAX_ELOZMENY = 20;
  var fejezet = (lap.getAttribute('data-fejezet') || '').split('/');      // [slug, fej]
  var slug = fejezet[0], fej = fejezet[1];
  var lapFej = lap.querySelector('.lap-fej');
  var cimFo = lap.querySelector('.lap-cim-fo');
  var cimAl = lap.querySelector('.lap-cim-al');
  var visszaGomb = lap.querySelector('.lap-vissza');
  var teljesGomb = lap.querySelector('.lap-teljes');
  var zarGomb = lap.querySelector('.lap-zar');
  var muvSor = document.getElementById('lap-muv');
  var uresResz = lap.querySelector('.lap-ures');
  var tartalom = lap.querySelector('.lap-tartalom');
  var tajolo = document.getElementById('tajolo');
  var tajoloVers = document.getElementById('tajolo-vers');
  var elozmeny = [];
  var keres = 0;                                                           // a késve érkező töredék ne írja felül a későbbit

  function kezdoAllapot() {
    var mod = lap.getAttribute('data-mod');
    if (mod === 'vers') { return { mod: 'vers', vers: lap.getAttribute('data-vers'), ful: lap.getAttribute('data-ful') || 'vers' }; }
    if (mod === 'szo') {
      var v = lap.getAttribute('data-vers');
      return { mod: 'szo', strong: lap.getAttribute('data-strong'), ig: v ? [slug, fej, v] : null };
    }
    return { mod: 'ures' };
  }
  var aktualis = kezdoAllapot();

  function azonos(a, b) {
    if (!a || !b || a.mod !== b.mod) { return false; }
    if (a.mod === 'vers') { return String(a.vers) === String(b.vers) && (a.ful || 'vers') === (b.ful || 'vers'); }
    if (a.mod === 'szo') { return a.strong === b.strong && String(a.ig) === String(b.ig); }
    return true;
  }
  function masol(a) { var b = {}; for (var k in a) { b[k] = a[k]; } return b; }
  function elozmenybeTesz(all) {
    if (all.mod === 'ures') { return; }
    if (elozmeny.length && azonos(elozmeny[elozmeny.length - 1], all)) { return; }
    elozmeny.push(masol(all));
    if (elozmeny.length > MAX_ELOZMENY) { elozmeny.shift(); }
  }

  function toredekUrl(all) {
    if (all.mod === 'vers') { return '/r/vers/' + slug + '/' + fej + '/' + all.vers; }
    return '/r/szo/' + encodeURIComponent(all.strong) + (all.ig ? '?ig=' + all.ig.join('/') : '');
  }

  // a lap címe (JS nélkül is ez a cím): a böngésző címsora az állapotot követi, így az újratöltés ugyanezt mutatja
  function lapUrl(all) {
    if (all.mod === 'vers') { return '/' + slug + '/' + fej + '/' + all.vers + (all.ful && all.ful !== 'vers' ? '?ful=' + all.ful : '') + '#v' + all.vers; }
    if (all.mod === 'szo') {
      var helyben = all.ig && all.ig[0] === slug && String(all.ig[1]) === String(fej);
      var alap = helyben ? '/' + slug + '/' + fej + '/' + all.ig[2] : '/' + slug + '/' + fej;
      return alap + '?szo=' + encodeURIComponent(all.strong) + '&ful=szo' + (helyben ? '#v' + all.ig[2] : '');
    }
    return '/' + slug + '/' + fej;
  }

  function helybeliVers(all) {
    if (all.mod === 'vers') { return all.vers; }
    return all.mod === 'szo' && all.ig && all.ig[0] === slug && String(all.ig[1]) === String(fej) ? all.ig[2] : null;
  }

  function kijelol(vers) {
    document.querySelectorAll('.szoveg-oszlop .kijelolt').forEach(function (e) { e.classList.remove('kijelolt'); });
    var el = vers ? document.getElementById('v' + vers) : null;
    if (el) { el.classList.add('kijelolt'); }
    if (tajoloVers) { tajoloVers.textContent = vers ? ':' + vers : ''; }
    return el;
  }

  function nyit(nyitva) {
    document.body.classList.toggle('lap-nyitva', nyitva);
    if (!nyitva) { teljes(false); }
  }
  function teljes(be) {
    document.body.classList.toggle('lap-egesz', be);
    if (teljesGomb) { teljesGomb.setAttribute('aria-pressed', be ? 'true' : 'false'); }
  }
  // a navigációs lap nyitása a részletek lapját elrejti, az állapotát megtartja (a mockup lapZar(true)-ja)
  navLapRejt = function () { if (kicsi()) { nyit(false); } };

  function fulValt(nev) {
    var cikk = tartalom.querySelector('.verslap');
    if (!cikk) { return; }
    var van = cikk.querySelector('.ful-tartalom[data-vful="' + nev + '"]');
    if (!van) { nev = 'vers'; }
    cikk.querySelectorAll('.fulek .ful[data-vful]').forEach(function (f) {
      var ez = f.getAttribute('data-vful') === nev;
      f.classList.toggle('aktiv', ez);
      f.setAttribute('aria-selected', ez ? 'true' : 'false');
    });
    cikk.querySelectorAll('.ful-tartalom[data-vful]').forEach(function (t) { t.hidden = t.getAttribute('data-vful') !== nev; });
    if (aktualis.mod === 'vers') { aktualis.ful = nev; }
  }

  // a műveletsor a lap fejsorában (a mockup .v9fmuv-ja): a szómód „A vers: … →” hivatkozása a töredékből ide költözik
  function muveletsor() {
    if (!muvSor) { return; }
    while (muvSor.firstChild) { muvSor.removeChild(muvSor.firstChild); }
    var sor = aktualis.mod === 'szo' ? tartalom.querySelector('.lap-versre-sor') : null;
    if (sor) { muvSor.appendChild(sor); }
  }

  function fejsor() {
    var cikk = tartalom.querySelector('[data-lapcim]');
    if (aktualis.mod === 'ures' || !cikk) {
      cimFo.textContent = lap.getAttribute('data-uresfo') || '';
      cimAl.textContent = lap.getAttribute('data-uresal') || '';
    } else {
      cimFo.textContent = cikk.getAttribute('data-lapcim') || '';
      cimAl.textContent = cikk.getAttribute('data-lapal') || '';
    }
    if (visszaGomb) { visszaGomb.hidden = elozmeny.length === 0; }
    if (zarGomb) {
      zarGomb.setAttribute('aria-label', kicsi() ? 'Bezárás' : 'Vissza az útmutatóhoz');
      zarGomb.setAttribute('title', kicsi() ? 'Bezárás' : 'Vissza az útmutatóhoz');
      zarGomb.hidden = aktualis.mod === 'ures' && !kicsi();             // nagy képernyőn az útmutatóból nincs hová visszamenni
    }
  }

  // kis képernyőn a koppintott vers a betekintő lap fölött maradjon látható (a mockup szabálya: csak ha a lap takarná)
  function versLathatova(el) {
    if (!el || !kicsi() || document.body.classList.contains('lap-egesz')) { return; }
    var r = el.getBoundingClientRect(), hatar = window.innerHeight * 0.5;
    if (r.top > hatar - 40 || r.top < 0) { window.scrollBy({ top: r.top - Math.min(80, hatar / 3), behavior: 'smooth' }); }
  }

  function megjelenit(all, html) {
    aktualis = all;
    lap.setAttribute('data-mod', all.mod);
    if (all.mod === 'ures') {
      tartalom.hidden = true;
      tartalom.innerHTML = '';
      uresResz.hidden = false;
    } else {
      tartalom.innerHTML = html;      // a szerver által escape-elt, regiszterből készült töredék
      tartalom.hidden = false;
      uresResz.hidden = true;
      if (all.mod === 'vers') { fulValt(all.ful || 'vers'); }
    }
    lap.scrollTop = 0;
    var vers = helybeliVers(all);
    var el = kijelol(vers);
    muveletsor();
    fejsor();
    try { window.history.replaceState(null, '', lapUrl(all)); } catch (e) { /* a címsor frissítése nem feltétele a működésnek */ }
    if (all.mod === 'vers') { legutobbHoz(lapUrl({ mod: 'vers', vers: all.vers }), (lap.getAttribute('data-kk') || slug) + ' ' + fej + ':' + all.vers); }
    return el;
  }

  function betolt(all, elozmenybe) {
    if (all.mod === 'ures') {
      if (elozmenybe) { elozmeny = []; }
      megjelenit(all, '');
      return;
    }
    var sorszam = ++keres;
    fetch(toredekUrl(all), { headers: { 'X-Requested-With': 'fetch' } }).then(function (r) {
      if (!r.ok) { throw new Error(r.status); }
      return r.text();
    }).then(function (html) {
      if (sorszam !== keres) { return; }
      if (elozmenybe && aktualis.mod !== 'ures' && !azonos(aktualis, all)) { elozmenybeTesz(aktualis); }
      navZar();
      var el = megjelenit(all, html);
      nyit(true);
      versLathatova(el);
    }).catch(function () { window.location.href = lapUrl(all); });      // hiba esetén a teljes lap
  }

  function uresre() {
    elozmeny = [];
    megjelenit({ mod: 'ures' }, '');
  }

  // egy hivatkozásból a lap állapota (vagy null: a hivatkozás a szokásos módon nyílik)
  function allapotHivatkozasbol(a) {
    var u;
    try { u = new URL(a.getAttribute('href'), window.location.href); } catch (e) { return null; }
    if (u.origin !== window.location.origin) { return null; }
    var m = /^\/([A-Za-z0-9]+)\/(\d+)\/(\d+)$/.exec(u.pathname);
    var szo = u.searchParams.get('szo');
    var ful = u.searchParams.get('ful');
    if (szo && ful !== 'vers' && VERS_FULEK.indexOf(ful) < 0) {
      return { mod: 'szo', strong: szo, ig: m ? [m[1], m[2], m[3]] : null };
    }
    if (m && m[1] === slug && m[2] === String(fej)) {
      return { mod: 'vers', vers: m[3], ful: VERS_FULEK.indexOf(ful) >= 0 ? ful : 'vers' };
    }
    return null;
  }

  document.addEventListener('click', function (ev) {
    if (ev.defaultPrevented || ev.button !== 0 || ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.altKey) { return; }
    var a = ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) { return; }
    // a navigáció: a fejezetcím és a tájoló pirula (kis képernyőn a navigációs lap, nagyon a könyvválasztó), a lap ✕-e
    if (a.matches('.navlap-nyito') || a === tajolo) {
      ev.preventDefault();
      if (kicsi()) { navNyit(); }
      else if (konyvvalaszto) { konyvvalaszto.open = true; var s = konyvvalaszto.querySelector('summary'); if (s) { s.focus(); } }
      return;
    }
    if (a.matches('.navlap-zar')) { ev.preventDefault(); navZar(); return; }
    // a kánon-sáv és a könyvválasztó könyve: a fejezetrács helyben (ha a számozás folytonos)
    if (a.closest('.kanon') || a.matches('.konyvgomb')) {
      var kk = a.getAttribute('data-kk');
      var gomb = a.matches('.konyvgomb') ? a : document.querySelector('.konyvgomb[data-kk="' + (window.CSS && CSS.escape ? CSS.escape(kk) : kk) + '"]');
      if (gomb && fejezetracsRajzol(gomb)) { ev.preventDefault(); }
      return;
    }
    // a fül a versmódban: nincs új töredék, de új állapot (az előzménylánc a fület is lépteti)
    if (a.matches('.verslap .fulek .ful[data-vful]') && lap.contains(a)) {
      ev.preventDefault();
      var uj = a.getAttribute('data-vful');
      if (aktualis.mod === 'vers' && (aktualis.ful || 'vers') !== uj) {
        elozmenybeTesz(aktualis);
        fulValt(uj);
        fejsor();
        try { window.history.replaceState(null, '', lapUrl(aktualis)); } catch (e) { /* nem feltétel */ }
      }
      return;
    }
    if (a === zarGomb) {
      ev.preventDefault();
      nyit(false);
      uresre();
      return;
    }
    if (a.matches('.lap-info')) {
      ev.preventDefault();
      uresre();
      nyit(true);
      return;
    }
    if (!(a.closest('.szoveg-oszlop') || lap.contains(a))) { return; }
    var all = allapotHivatkozasbol(a);
    if (!all) { return; }
    ev.preventDefault();
    betolt(all, true);
  });

  if (visszaGomb) {
    visszaGomb.addEventListener('click', function () {
      var elozo = elozmeny.pop();
      if (!elozo) { return; }
      // ugyanaz a vers, másik fül: a töredék már a lapon van
      if (elozo.mod === 'vers' && aktualis.mod === 'vers' && String(elozo.vers) === String(aktualis.vers) && tartalom.querySelector('.verslap')) {
        fulValt(elozo.ful || 'vers');
        fejsor();
        try { window.history.replaceState(null, '', lapUrl(aktualis)); } catch (e) { /* nem feltétel */ }
        return;
      }
      betolt(elozo, false);
    });
  }

  if (teljesGomb) {
    teljesGomb.addEventListener('click', function () { teljes(!document.body.classList.contains('lap-egesz')); });
  }

  // a fátyol: a navigációs lapot zárja, a teljes nézetből betekintésre vált
  var hatter = document.getElementById('hatter');
  if (hatter) {
    hatter.addEventListener('click', function () {
      if (navNyitva()) { navZar(); } else { teljes(false); }
    });
  }

  // húzás a lap fejsorán (900 px alatt): fel = teljes nézet, le = betekintés, majd zárás; rövid koppintás a fejsoron: váltás
  if (lapFej && window.PointerEvent) {
    var y0 = null, t0 = 0;
    lapFej.addEventListener('pointerdown', function (ev) {
      if (!kicsi() || (ev.target.closest && ev.target.closest('button, a'))) { return; }
      y0 = ev.clientY; t0 = Date.now();
      try { lapFej.setPointerCapture(ev.pointerId); } catch (e) { /* nem feltétel */ }
    });
    lapFej.addEventListener('pointerup', function (ev) {
      if (y0 === null) { return; }
      var dy = ev.clientY - y0; y0 = null;
      var egesz = document.body.classList.contains('lap-egesz');
      if (Math.abs(dy) < 8 && Date.now() - t0 < 300) { teljes(!egesz); return; }
      if (dy < -40) { teljes(true); }
      else if (dy > 40) {
        if (egesz) { teljes(false); }
        else { nyit(false); uresre(); }
      }
    });
    lapFej.addEventListener('pointercancel', function () { y0 = null; });
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') { return; }
    if (navNyitva()) { navZar(); return; }
    if (document.body.classList.contains('lap-nyitva') && kicsi()) {
      nyit(false);
      uresre();
    }
  });

  // a tájoló pirula (900 px alatt): felfelé görgetésre (300 px mélység fölött, 6 px-es küszöb) megjelenik, lefelé vagy 2,5 mp után eltűnik
  if (tajolo) {
    var utolso = window.scrollY, idozito = null;
    window.addEventListener('scroll', function () {
      if (!kicsi()) { return; }
      var y = window.scrollY;
      if (y < utolso - 6 && y > 300) {
        document.body.classList.add('tajolo-latszik');
        clearTimeout(idozito);
        idozito = setTimeout(function () { document.body.classList.remove('tajolo-latszik'); }, 2500);
      } else if (y > utolso + 6 || y <= 300) {
        document.body.classList.remove('tajolo-latszik');
      }
      utolso = y;
    }, { passive: true });
  }

  function szelessegValt() {
    if (!kicsi()) { navZar(); teljes(false); }
    fejsor();
  }
  if (kicsiMedia && kicsiMedia.addEventListener) { kicsiMedia.addEventListener('change', szelessegValt); }
  muveletsor();
  fejsor();
  if (aktualis.mod === 'vers') { legutobbHoz(lapUrl({ mod: 'vers', vers: aktualis.vers }), (lap.getAttribute('data-kk') || slug) + ' ' + fej + ':' + aktualis.vers); }
})();
