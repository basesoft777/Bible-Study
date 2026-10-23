// Az olvasói felület kis JavaScriptje (#76 M2, #134 M1). Nélküle is minden működik: a vers- és szó-kattintás, a fülek és a
// bezárás sima hivatkozások (szerveroldali lap, a részletek lapja a szerverről nyitott állapotban érkezik). Itt csak a gyorsítás:
// a részletek lapja (szó- és versmód, fülek, előzménylánc), a töredék-betöltés (/r/...), a Ctrl+K és a helyi beállítások.
(function () {
  'use strict';

  // Ctrl+K: ugrás a gyorsugrás dobozra
  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && ev.key && ev.key.toLowerCase() === 'k') {
      var be = document.querySelector('.ugras input[name=q]');
      if (be) { ev.preventDefault(); be.focus(); be.select(); }
    }
  });

  // az olvasó helyi beállításai (csak a böngészőben, localStorage; sütit nem hoznak létre): a kapcsolt szavak jelölése és a színséma
  function tarol(kulcs, ertek) { try { window.localStorage.setItem(kulcs, ertek); } catch (e) { /* tiltott tároló: a beállítás csak az oldalra érvényes */ } }
  function olvas(kulcs) { try { return window.localStorage.getItem(kulcs); } catch (e) { return null; } }

  var jeloles = document.getElementById('jeloles');
  if (jeloles) {
    var jelolesAllit = function () {
      document.querySelectorAll('.szoveg-oszlop').forEach(function (o) { o.classList.toggle('nincs-jeloles', !jeloles.checked); });
    };
    jeloles.checked = olvas('pardes_jeloles') !== 'ki';
    jelolesAllit();
    jeloles.addEventListener('change', function () { tarol('pardes_jeloles', jeloles.checked ? 'be' : 'ki'); jelolesAllit(); });
  }

  var temaGombok = document.querySelectorAll('.tema button[data-tema]');
  function temaAllit(tema) {
    if (tema === 'light' || tema === 'dark') { document.documentElement.setAttribute('data-tema', tema); }
    else { document.documentElement.removeAttribute('data-tema'); tema = 'rendszer'; }
    temaGombok.forEach(function (g) { g.setAttribute('aria-pressed', g.getAttribute('data-tema') === tema ? 'true' : 'false'); });
  }
  if (temaGombok.length) {
    temaAllit(olvas('pardes_tema'));
    temaGombok.forEach(function (g) {
      g.addEventListener('click', function () { var t = g.getAttribute('data-tema'); tarol('pardes_tema', t); temaAllit(t); });
    });
  }

  // ---------------------------------------------------------------------------------------------------------------------
  // a részletek lapja (#134 M1, DT293): egy komponens, két mód (szó / vers); 900 px alatt alsó lap, fölötte állandó oldalblokk.
  // Az állapot: {mod: 'ures'} | {mod: 'vers', vers, ful} | {mod: 'szo', strong, ig: [slug, fej, vers] | null}.
  // Az előzménylánc (‹): a korábbi állapotok verme, legfeljebb 20; az azonos egymás utáni állapot nem ismétlődik.
  // ---------------------------------------------------------------------------------------------------------------------
  var lap = document.getElementById('reszletek');
  if (!lap) { return; }
  var VERS_FULEK = ['vers', 'kh', 'temak', 'motivum'];
  var MAX_ELOZMENY = 20;
  var fejezet = (lap.getAttribute('data-fejezet') || '').split('/');      // [slug, fej]
  var slug = fejezet[0], fej = fejezet[1];
  var cimFo = lap.querySelector('.lap-cim-fo');
  var cimAl = lap.querySelector('.lap-cim-al');
  var visszaGomb = lap.querySelector('.lap-vissza');
  var teljesGomb = lap.querySelector('.lap-teljes');
  var zarGomb = lap.querySelector('.lap-zar');
  var uresResz = lap.querySelector('.lap-ures');
  var tartalom = lap.querySelector('.lap-tartalom');
  var kicsiMedia = window.matchMedia ? window.matchMedia('(max-width: 899.98px)') : null;
  var elozmeny = [];
  var keres = 0;                                                           // a késve érkező töredék ne írja felül a későbbit

  function kicsi() { return kicsiMedia ? kicsiMedia.matches : false; }

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
    if (a.mod === 'vers') { return String(a.vers) === String(b.vers); }
    if (a.mod === 'szo') { return a.strong === b.strong && String(a.ig) === String(b.ig); }
    return true;
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

  function kijelol(vers) {
    document.querySelectorAll('.szoveg-oszlop .kijelolt').forEach(function (e) { e.classList.remove('kijelolt'); });
    var el = vers ? document.getElementById('v' + vers) : null;
    if (el) { el.classList.add('kijelolt'); }
    return el;
  }

  function nyit(nyitva) {
    document.body.classList.toggle('lap-nyitva', nyitva);
    if (!nyitva) { document.body.classList.remove('lap-egesz'); if (teljesGomb) { teljesGomb.setAttribute('aria-pressed', 'false'); } }
  }

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
    }
  }

  function megjelenit(all, html, gorget) {
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
    var vers = all.mod === 'vers' ? all.vers : (all.mod === 'szo' && all.ig && all.ig[0] === slug && String(all.ig[1]) === String(fej) ? all.ig[2] : null);
    var el = kijelol(vers);
    fejsor();
    try { window.history.replaceState(null, '', lapUrl(all)); } catch (e) { /* a címsor frissítése nem feltétele a működésnek */ }
    if (gorget && el && kicsi()) { el.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
  }

  function betolt(all, elozmenybe) {
    if (all.mod === 'ures') {
      if (elozmenybe) { elozmeny = []; }
      megjelenit(all, '', false);
      return;
    }
    var sorszam = ++keres;
    fetch(toredekUrl(all), { headers: { 'X-Requested-With': 'fetch' } }).then(function (r) {
      if (!r.ok) { throw new Error(r.status); }
      return r.text();
    }).then(function (html) {
      if (sorszam !== keres) { return; }
      if (elozmenybe && aktualis.mod !== 'ures' && !azonos(aktualis, all)) {
        elozmeny.push(aktualis);
        if (elozmeny.length > MAX_ELOZMENY) { elozmeny.shift(); }
      }
      megjelenit(all, html, true);
      nyit(true);
    }).catch(function () { window.location.href = lapUrl(all); });      // hiba esetén a teljes lap
  }

  // egy hivatkozásból a lap állapota (vagy null: a hivatkozás a szokásos módon nyílik)
  function allapotHivatkozasbol(a) {
    var u;
    try { u = new URL(a.href, window.location.href); } catch (e) { return null; }
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
    // a fül a versmódban: nincs új állapot, csak a fül vált
    if (a.matches('.verslap .fulek .ful[data-vful]') && lap.contains(a)) {
      ev.preventDefault();
      fulValt(a.getAttribute('data-vful'));
      try { window.history.replaceState(null, '', lapUrl(aktualis)); } catch (e) { /* nem feltétel */ }
      return;
    }
    if (a === zarGomb) {
      ev.preventDefault();
      elozmeny = [];
      nyit(false);
      megjelenit({ mod: 'ures' }, '', false);
      return;
    }
    if (a.matches('.lap-info')) {
      ev.preventDefault();
      elozmeny = [];
      megjelenit({ mod: 'ures' }, '', false);
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
      if (elozo) { betolt(elozo, false); }
    });
  }

  if (teljesGomb) {
    teljesGomb.addEventListener('click', function () {
      var egesz = !document.body.classList.contains('lap-egesz');
      document.body.classList.toggle('lap-egesz', egesz);
      teljesGomb.setAttribute('aria-pressed', egesz ? 'true' : 'false');
    });
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && document.body.classList.contains('lap-nyitva') && kicsi()) {
      elozmeny = [];
      nyit(false);
      megjelenit({ mod: 'ures' }, '', false);
    }
  });

  if (kicsiMedia && kicsiMedia.addEventListener) { kicsiMedia.addEventListener('change', fejsor); }
  fejsor();
})();
